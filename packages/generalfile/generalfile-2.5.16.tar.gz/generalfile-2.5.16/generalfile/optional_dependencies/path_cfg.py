
from generallibrary import deco_cache, initBases, depth
from generalfile.optional_dependencies._extension import _Extension

import configparser
import json


class Path_Cfg:
    """ Cfg methods for Path. """
    @property
    @deco_cache()
    def cfg(self):
        """ Easily modify cfg files with a dictionary. """
        return _Cfg(self)


@initBases
class _Cfg(_Extension):
    _OBSCURE = "obscure_name_that_wont_match"
    _JSON_CAST = {
        "None": None,
        "True": True,
        "False": False,
    }
    _JSON_CAST_WRITE = {
        None: "None",
    }

    def _basic_write(self, dict_, overwrite):
        return self.path.text.write("\n".join(f"{key} = {value}" for key, value in dict_.items()), overwrite=overwrite)

    def write(self, dict_=None, overwrite=False):
        """ Write to this path with a given dictionary. """
        if depth(dict_) == 1:
            return self._basic_write(dict_=dict_, overwrite=overwrite)

        config = configparser.ConfigParser()
        # config = configparser.ConfigParser(converters={'list': lambda x: [i.strip() for i in x.split(',')]})

        cast_dict = self._write_cast_dict(dict_)

        config.read_dict(dictionary=cast_dict)
        with self.WriteContext(self.path, overwrite=overwrite) as write_path:
            return write_path.open_operation("w", lambda stream: config.write(stream))

    def _write_cast_dict(self, dict_):
        cast_dict = {}
        for section_name, section in dict_.items():
            cast_dict[section_name] = {key: self._write_json_cast(value=value) for key, value in section.items()}
        return cast_dict

    def _write_json_cast(self, value):
        try:
            if value in self._JSON_CAST_WRITE:
                return self._JSON_CAST_WRITE[value]
        except TypeError:
            pass

        return value

    def _read_json_cast(self, value):
        if value in self._JSON_CAST:
            return self._JSON_CAST[value]

        try:
            return json.loads(value.replace("'", '"'))
        except json.decoder.JSONDecodeError:
            return value

    def _read(self, config, path):
        string = path.text.read()
        try:
            config.read_string(string)
        except configparser.MissingSectionHeaderError:
            string = f"[{self._OBSCURE}]\n{string}"
            config.read_string(string)

    def _config_to_dict(self, config):
        dict_ = {section: {key: self._read_json_cast(value) for key, value in config.items(section)} for section in config.sections()}
        if self._OBSCURE in dict_:
            return dict_[self._OBSCURE]
        return dict_

    def read(self, default=...):
        """ Read from this path to get a dictionary. """
        config = configparser.ConfigParser()
        with self.ReadContext(self.path) as path:
            if not path.exists():
                if default is Ellipsis:
                    raise FileNotFoundError
                else:
                    return default
            self._read(config=config, path=path)
        return self._config_to_dict(config=config)

    def append(self, dict_):
        """ Update this cfg with a dictionary. """
        # append_path.cfg.write(dict_=append_path.cfg.read() | dict_, overwrite=True)  # 3.9
        self.write(dict_={**self.path.cfg.read(), **dict_}, overwrite=True)









































