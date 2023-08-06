import re

import requests

from generalfile import Path
from generallibrary import Ver, Date, get, remove_duplicates, Log
from generalpackager.api.shared.name import _SharedAPI
from generalpackager.api.shared.owner import _SharedOwner
from generalpackager.api.shared.protocols import PackageHostProtocol


def download(url, path):
    """ Todo: Move download to it's own package. """
    data = requests.get(url)
    if data.status_code != 200:
        raise AttributeError(f"Request for url {url} did not yield a status code of 200, it's {data.status_code}.'")

    path = Path(path)

    with path.lock():
        path.get_parent().create_folder()
        with open(str(path), "wb") as file:
            file.write(data.content)
    return path


class PyPI(PackageHostProtocol, _SharedAPI, _SharedOwner):
    """ Tools to interface pypi.org """
    DEFAULT_OWNER = "Mandera"

    @property
    def url(self):
        return f"https://pypi.org/project/{self.name}/"

    @property
    def json_endpoint(self, version=None):
        if version:
            version = f"/{version}"
        else:
            version = ""
            Log(__name__).warning("The releases key is deprecated: https://warehouse.pypa.io/api-reference/json.html")

        url = f"https://pypi.org/pypi/{self.name}{version}/json"
        request = requests.get(url)
        request.raise_for_status()
        return requests.get(url).json()

    def exists(self):
        """ Return whether this API's target exists. """
        return requests.get(url=self.url).status_code == 200

    def _get_tarball_url(self, version=None):
        """ Get URL to download tarball. """
        if version is None:
            version = self.get_version()
        return f"https://pypi.io/packages/source/{self.name[0]}/{self.name}/{self.name}-{version}.tar.gz"

    def download(self, path=None, version=None, overwrite=False):
        """ Download tar ball to cache, extract it, remove tar ball.
            Returns target folder tarball is extracted in. """
        if version is None:
            version = self.get_version()

        path = Path(path)
        temp = Path.get_cache_dir() / "Python/temp.tar.gz"
        download(self._get_tarball_url(version=version), path=temp)
        temp.unpack(base=path, overwrite=overwrite)
        temp.delete(error=False)
        return (path / f"{self.name}-{version}").rename(self.name, overwrite=overwrite)

    def get_owners_packages(self):
        """ Get a set of a owner's packages' names on PyPI. """
        return set(re.findall("/project/(.*)/", requests.get(f"https://pypi.org/user/{self.owner}/").text))

    def get_version(self):
        """ Get version of latest publish on PyPI.

            Todo: Find a faster fetch for latest PyPI version and datetime. """
        version = get(re.findall(f"{self.name} ([.0-9]+)\n", requests.get(self.url).text), 0)
        return Ver(version) if version else None

    def _json_metadata(self):
        return requests.get(self.url_json).json()

    def get_all_versions(self):
        url = f"https://pypi.org/simple/{self.name}"
        text = requests.get(url=url).text

        find = re.findall(rf">{self.name}-(\d+(?:\.\d+){{0,2}})", text)
        unique = remove_duplicates(find)
        versions = [Ver(version) for version in unique]
        versions.sort(reverse=True)
        return versions

    def get_date(self):
        """ Get datetime of latest release. """
        date = get(re.findall('Generated (.+) for commit', requests.get(self.url).text), 0)
        return Date(date) if date else None



























