import re

from generalfile import Path
from generallibrary import deco_cache, Recycle, AutoInitBases
from generalpackager.api.shared.target import Packages


class _SharedName:
    """ Inherited by _SharedAPI which is shared by all (Packager and APIs) """
    DEFAULT_NAME = "generalpackager"

    _recycle_keys = {"name": lambda name, path: _SharedName._scrub_name(name=name, path=path)}

    def __init__(self, name=None, path=None):
        self.name = self._scrub_name(name=name, path=path)

    @classmethod
    @deco_cache()
    def _trim_partial(cls, name):
        if name:
            return re.match("(\w|[-.])+", name).group()

    @classmethod
    @deco_cache()
    def _scrub_name(cls, name, path):
        name = cls._trim_partial(name=name)

        if path and hasattr(cls, "_scrub_path"):
            path = Path(path)
            if name and not path.endswith(name):
                raise AttributeError(f"Both path and name was set for {cls} but {path} doesn't end with {name}.")

            return path.stem()
        return name or cls.DEFAULT_NAME

    @staticmethod
    def name_is_general(name):
        return name in Packages.all_packages()

    def is_general(self):
        """ :param generalpackager.Packager self: """
        return self.name_is_general(name=self.name)

    @property
    def simple_name(self):
        """ :param generalpackager.Packager self: """
        if self.name.startswith("general"):
            return self.name.replace("general", "")
        elif self.name.startswith("gen"):
            return self.name.replace("gen", "")
        else:
            return self.name


class _SharedAPI(_SharedName, Recycle, metaclass=AutoInitBases):
    """ Shared by all (Packager and APIs). """
