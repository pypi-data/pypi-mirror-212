from generalfile import Path
from generallibrary import deco_cache, Log


class _SharedPath:
    """ Shared by Packager and LocalRepo. """
    _recycle_keys = {"path": lambda cls, name, path: str(cls._scrub_path(name=name, path=path))}

    def __init__(self, name=None, path=None):
        self.path = self._scrub_path(name=name, path=path)  # type: Path

    @classmethod
    @deco_cache()
    def _resolve_path_localmodule(cls, name):
        """ :param generalpackager.Packager cls:
            :rtype: Path or None """
        localmodule = cls.LocalModule(name=name)
        if localmodule.exists():
            path = localmodule.path.get_parent_repo()

            Log().debug(f"Found path {path} for {name}. Modules path is {localmodule.path}, module is {localmodule.module}.")
            return path

    @classmethod
    @deco_cache()
    def _resolve_path_workingdir_traverse_parents(cls, name):
        """ :param generalpackager.Packager cls:
            :rtype: Path or None """
        repo_parent_path: Path = Path().absolute().get_parent(depth=-1, include_self=True, traverse_excluded=True, filt=lambda path, name_=name: (path / name_).is_repo())
        if repo_parent_path is not None:
            return repo_parent_path / name

    @classmethod
    @deco_cache()
    def _resolve_path(cls, name):
        """ :param generalpackager.Packager cls:
            :rtype: Path or None """
        for method in (cls._resolve_path_localmodule, cls._resolve_path_workingdir_traverse_parents):
            path = method(name=name)
            if path and path.endswith(name):
                Log().debug(f"Resolved path with '{method.__name__}' for '{name}', got '{path}'.")
                return path
        return Path(name)

    @classmethod
    @deco_cache()
    def _scrub_path(cls, name, path):
        """ :param generalpackager.Packager cls:
            :rtype: Path or None """
        name = cls._scrub_name(name=name, path=path)
        if path is None:
            return cls._resolve_path(name=name)
        else:
            path = Path(path).absolute()
            if not path.endswith(name):
                raise AttributeError(f"Path '{path}' seems to be wrong for '{name}'. Workdir is '{Path().absolute()}'.")
            return path
