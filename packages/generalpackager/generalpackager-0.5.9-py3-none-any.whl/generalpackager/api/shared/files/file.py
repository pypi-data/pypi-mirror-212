from logging import getLogger

from generalfile import Path
from generallibrary import deco_cache, CodeLine
from generalpackager.api.shared.target import Targets


class DynamicRelativePath:
    def __get__(self, instance, owner):
        if instance:
            return Path(instance._relative_path)
        else:
            assert not instance.requires_instance(), f"Only an instantialized Packager can access '{owner.__name__}'."
            return Path(owner._relative_path)


class File:
    """ Instantiated if its owner is. """
    targets = Targets

    _relative_path = ...
    aesthetic = ...

    remove = False
    overwrite = True
    is_file = True
    target = Targets.python  # Should probably default to None, and then I put python on most files

    def _generate(self):
        return "" or CodeLine()

    def __init__(self, owner):
        """ :param generalpackager.Packager or generalpackager.LocalRepo owner: """
        self.owner = owner

    @property
    def name(self):
        return self.fullname[:-4] if self.fullname.endswith("File") else self.fullname
        # return self.fullname.removesuffix("File") # 3.9+

    @property
    def fullname(self):
        return type(self).__name__

    @property
    @deco_cache()
    def packager(self):
        return self.owner if type(self.owner).__name__ == "Packager" else None

    @property
    @deco_cache()
    def localrepo(self):
        return self.packager.localrepo if self.packager else self.owner

    relative_path = DynamicRelativePath()

    @classmethod
    def requires_instance(cls):
        return hasattr(cls._relative_path, "fget")

    @property
    @deco_cache()
    def path(self):
        return self.owner.path / self._relative_path

    def _cant_write(self, msg):
        logger = getLogger(__name__)
        logger.info(f"Can't write '{self.fullname}' - {msg}")
        return False

    def can_write(self):
        if not self.is_file:
            return self._cant_write(".is_file is False")

        elif self.remove:
            return self._cant_write(".remove is True")

        elif type(self)._generate is File._generate:
            return self._cant_write("._generate is undefined")

        elif self.target != self.owner.target:
            return self._cant_write(f".target {self.target} doesn't match it owner's {self.owner}")

        elif self.overwrite is False and self.path.exists():
            return self._cant_write(f".overwrite is False and path {self.path} exists")

        else:
            return True

    def get_generate_text(self):
        """ Make all top children have one space after. """
        text = self._generate()
        if type(text) is CodeLine:
            for codeline in text.get_children():
                last_child = codeline.get_child(depth=-1, index=-1, include_self=True)
                last_child.space_after = 1
        return text

    def generate(self):
        logger = getLogger(__name__)

        if self.can_write():
            logger.info(f"Writing to '{self.relative_path}' for '{self.owner.name}'")
            return self.path.text.write(text=f"{self.get_generate_text()}\n", overwrite=self.overwrite)

        elif self.remove:
            logger.info(f"Deleting '{self.relative_path}' for '{self.owner.name}'")
            self.path.delete()

    def __str__(self):
        return f"<File: {self.owner.name} - {self.relative_path}>"
