
from generalfile import Path
from generallibrary import Date
from requests import ConnectionError


class _PackagerPypi:
    def get_latest_release(self):
        """ Use current datetime if bumped, otherwise fetch.

            :param generalpackager.Packager self: """
        try:
            bumped = self.is_bumped()
        except ConnectionError:
            return "Failed fetching"

        if bumped:
            return Date.now()
        else:
            return self.pypi.get_date()

    @classmethod
    def reserve_name(cls, name):
        """ Reserve a name on PyPI with template files.

            :param generalpackager.Packager or any cls:
            :param name: """
        path = Path.get_cache_dir() / "python/pypi_reserve/" / name
        packager = cls(path=path, target=cls.Targets.python)
        packager.create_blank_locally(install=False)
        packager.localrepo.publish()
        path.delete()




























