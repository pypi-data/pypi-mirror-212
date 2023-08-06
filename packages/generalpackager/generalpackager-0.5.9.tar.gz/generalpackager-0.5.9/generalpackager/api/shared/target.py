from typing import Literal

from generallibrary import deco_cache, flatten
from generallibrary.objinfo.objinfo import DataClass

_TARGETS_LITERAL = Literal["python", "node", "django", "exe"]

class Targets(DataClass):
    python = "python"
    node = "node"
    django = "django"
    exe = "exe"

_DEFAULT_TARGET = Targets.python

class _SharedTarget:
    Targets = Targets

    """ Used by LocalRepo and Packager """
    def is_python(self):
        """ :param generalpackager.Packager or generalpackager.LocalRepo self: """
        return self.target == Targets.python

    def is_node(self):
        """ :param generalpackager.Packager or generalpackager.LocalRepo self: """
        return self.target == Targets.node

    def is_django(self):
        """ :param generalpackager.Packager or generalpackager.LocalRepo self: """
        return self.target == Targets.django

    def is_exe(self):
        """ :param generalpackager.Packager or generalpackager.LocalRepo self: """
        return self.target == Targets.exe


class Packages(Targets):
    """ Purpose is to easily see if name is general and what target it has.
        Todo: Generate Python file in generalpackager containing general packages. """
    python = [
        "generaltool",
        "generalimport",
        "generallibrary",
        "generalfile",
        "generalvector",
        "generalgui",
        "generalbrowser",
        "generalpackager",
    ]
    node = [
        "genlibrary",
        "genvector",
    ]
    django = [

    ]
    exe = [
        "generalmainframe",
    ]

    @classmethod
    @deco_cache()
    def all_packages(cls):
        return flatten(cls.field_values_defaults())

