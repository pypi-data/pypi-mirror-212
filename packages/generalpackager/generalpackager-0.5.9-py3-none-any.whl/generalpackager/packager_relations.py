
from generallibrary import deco_cache, Log, flatten, remove_duplicates

from generalpackager.api.shared.target import Packages


class _PackagerRelations:
    Packages = Packages

    @classmethod
    def packagers_from_packages(cls):
        """ Get all packagers defined in Packages even if they don't exist.
            Paths are set to working_dir / name.

            :param generalpackager.Packager or any cls: """
        packagers = []
        for target, names in cls.Packages.field_dict_defaults().items():
            for name in names:
                packager = cls(name=name, path=name, target=target)
                packagers.append(packager)
        return packagers

    def get_dependencies(self, only_general=False):
        """ Get a list of dependencies as Packagers.
            Combines localmodules dependencies with localrepos install_requires.
            Optionally only return general packages.

            :param generalpackager.Packager self:
            :param bool only_general: Whether to only return general packages. """

        names = {localmodule.name for localmodule in self.localmodule.get_dependencies()}

        if self.target == self.Targets.python:
            names.update(self.localrepo.metadata.install_requires)

        return [type(self)(name) for name in names if not only_general or self.name_is_general(name)]

    def get_dependants(self, only_general=False):
        """ Get a list of dependants as Packagers.
            Same as localmodules but Packager instead of localmodule.
            Optionally only return general packages.

            :param generalpackager.Packager self:
            :param bool only_general: Whether to only return general packages. """
        packagers = {type(self)(localmodule.name) for localmodule in self.localmodule.get_dependants() if not only_general or self.name_is_general(localmodule.name)}
        return list(packagers)

    @classmethod
    @deco_cache()
    def get_ordered_packagers(cls, include_private=True, include_summary_packagers=False):
        """ Get a list of enabled ordered packagers from the dependency chain, sorted by name in each lvl.

            :param generalpackager.Packager or Any cls:
            :param include_private:
            :param include_summary_packagers:
            :rtype: list[generalpackager.Packager] """
        packagers_by_layer = cls().get_ordered(flat=False)
        sorted_layers = [sorted(layer, key=lambda pkg: pkg.name) for layer in packagers_by_layer]
        packagers = remove_duplicates(flatten(sorted_layers))

        if not include_private:
            packagers = [packager for packager in packagers if not packager.localrepo.metadata.private]

        if include_summary_packagers:
            packagers.extend(cls.summary_packagers())

        Log().debug("Ordered packagers:", packagers)

        return packagers

    def get_owners_package_names(self):
        """ Return a set of owner's packages with intersecting PyPI and GitHub, ignores enabled flag.

            :param generalpackager.Packager self: """
        return self.pypi.get_owners_packages().intersection(self.github.get_owners_packages())

    def general_bumped_set(self):
        """ Yield general packagers that have been bumped.

            :param generalpackager.Packager self: """
        for packager in self.get_ordered_packagers():
            if packager.is_bumped():
                yield packager

    def general_changed_dict(self, aesthetic=None):
        """ Return a dict of general packagers with changed files comparing to GitHub.

            :param generalpackager.Packager self:
            :param aesthetic: """
        return {packager: files for packager in self.get_ordered_packagers() if (files := packager.compare_local_to_github(aesthetic=aesthetic))}
