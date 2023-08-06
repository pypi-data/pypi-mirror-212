

def deco_path_as_working_dir(func):
    def _wrapper(self, *args, **kwargs):
        with self.path.as_working_dir():
            return func(self, *args, **kwargs)
    return _wrapper
