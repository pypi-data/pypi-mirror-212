""" Not using typing.Protocol because that's for type checking only.
    Not using abc because I can't define another metaclass.
        The only thing that'd be nice is if it'd detect unchanged stubs without calling them. """
from typing import List

from generallibrary import Ver


class PackageHostProtocol:
    """ GitHub.com, PyPI.org, NPMjs.com"""
    DEFAULT_OWNER = ...
    def __init__(self, name=None, owner=None): pass
    def download(self, path=None, version=None, overwrite=False): raise NotImplementedError
    def url(self): raise NotImplementedError
    def exists(self): raise NotImplementedError
    def get_owners_packages(self): raise NotImplementedError
    def get_version(self): raise NotImplementedError

    def get_all_versions(self) -> List[Ver]:
        """ Return a list of Vers in descending order. """
        raise NotImplementedError

    def get_date(self): raise NotImplementedError


class LocalRepoProtocol:
    """ Python and Node target. """
    target = None
    def install(self, local=True, editable=False): raise NotImplementedError
    def uninstall(self, local=True, editable=False): raise NotImplementedError
    def run_tests(self): raise NotImplementedError
    def publish(self, public=True): raise NotImplementedError
    def package_folder(self, local=True): raise NotImplementedError
    def _list_packages_gen(self, local=True, editable=None): raise NotImplementedError

    def list_packages(self, local=True, editable=None) -> List[str]:
        return list(self._list_packages_gen(local=local, editable=editable))

