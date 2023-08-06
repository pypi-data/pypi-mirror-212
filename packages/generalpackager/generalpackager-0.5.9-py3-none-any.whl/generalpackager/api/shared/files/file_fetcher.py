import importlib

from generallibrary import deco_cache


class FileFetcher:
    """ Descriptor to return instance of a File if instance owner is Packager.
        Otherwise, return class of File.
        Caches File instance to instance of Packager. """

    def __init__(self):
        self.name = None

    def __set_name__(self, owner, name):
        if "_file" in name:
            self.name = name.split("_file")[0]
        else:
            self.name = name.split("_folder")[0]

    @property
    @deco_cache()
    def cls(self):
        module = importlib.import_module(name=f"generalpackager.api.shared.files.definitions.{self.name}")
        return getattr(module, self.cls_name)

    @property
    @deco_cache()
    def cls_name(self):
        return "".join(part.capitalize() for part in self.name.split("_")) + "File"

    @property
    def protected_cls_name(self):
        return f"_{self.cls_name}"

    def cache_file(self, instance):
        cached_file = getattr(instance, self.protected_cls_name, None)
        if cached_file:
            return cached_file
        else:
            new_file = self.cls(owner=instance)
            setattr(instance, self.protected_cls_name, new_file)
            return new_file

    def __get__(self, instance, owner):
        """ :rtype: generalpackager.api.shared.files.file.File or Any """
        if instance:
            return self.cache_file(instance=instance)
        else:
            return self.cls
