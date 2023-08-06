


class _Context:
    def __init__(self, path):
        self.path = path
        self.lock = self.path.lock()

    def __enter__(self):
        self.lock.__enter__()
        return self.path

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lock.__exit__(exc_type, exc_val, exc_tb)


class _SharedWriteAppend(_Context):
    SUFFIX = ".tmp"

    def __init__(self, path):
        super().__init__(path)
        assert path.suffix() != self.SUFFIX, f"High level operation on {self.SUFFIX} isn't allowed. Use open_operation in most cases."
        self.temp_path = self.path.with_suffix(self.SUFFIX)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.temp_path.exists():
            self.temp_path.rename(self.path, overwrite=True)
        super().__exit__(exc_type, exc_val, exc_tb)


class WriteContext(_SharedWriteAppend):
    """ A context manager used for every write method. """
    def __init__(self, path, overwrite=False):
        super().__init__(path)
        self.overwrite = overwrite

    def __enter__(self):
        """ :rtype: generalfile.Path """
        if not self.overwrite and self.path.exists():
            raise FileExistsError(f"Path '{self.path}' already exists and overwrite is 'False'.")
        super().__enter__()
        self.path.get_parent().create_folder()
        return self.temp_path


class AppendContext(_SharedWriteAppend):
    """ A context manager used for every append method. """
    def __enter__(self):
        super().__enter__()
        if self.path.exists():
            self.path.copy(self.temp_path)
        else:
            self.path.get_parent().create_folder()
        return self.temp_path


class ReadContext(_Context):
    """ A context manager used for every read method. """



class _Extension:
    WriteContext = WriteContext
    ReadContext = ReadContext
    AppendContext = AppendContext

    def __init__(self, path):
        self.path = path


