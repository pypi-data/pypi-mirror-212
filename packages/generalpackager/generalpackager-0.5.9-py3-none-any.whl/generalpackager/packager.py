
from generallibrary import NetworkDiagram, deco_cache

from generalpackager.api.shared.target import _SharedTarget, _TARGETS_LITERAL
from generalpackager.api.shared.files.shared_files import _Files
from generalpackager.api.shared.path import _SharedPath
from generalpackager.api.shared.name import _SharedName, _SharedAPI
from generalpackager.packager_api import _PackagerAPIs
from generalpackager.packager_environment import _PackagerEnvironment
from generalpackager.packager_files import _PackagerFiles
from generalpackager.packager_github import _PackagerGitHub
from generalpackager.packager_metadata import _PackagerMetadata
from generalpackager.packager_pypi import _PackagerPypi
from generalpackager.packager_relations import _PackagerRelations
from generalpackager.packager_workflow import _PackagerWorkflow

class Packager(NetworkDiagram,
               _Files, _SharedAPI, _SharedTarget, _SharedPath,
               _PackagerGitHub, _PackagerFiles, _PackagerMetadata, _PackagerPypi, _PackagerWorkflow, _PackagerRelations, _PackagerAPIs, _PackagerEnvironment):
    """ Uses APIs to manage 'general' package.
        Contains methods that require more than one API as well as methods specific for ManderaGeneral. """

    author = 'Rickard "Mandera" Abraham'
    email = "rickard.abraham@gmail.com"
    license = "mit"
    python = "3.8", "3.9", "3.10", "3.11"  # Only supports basic definition with tuple of major.minor
    os = "windows", "ubuntu"  # , "macos"

    def __init__(self, name=None, path=None, target: _TARGETS_LITERAL = None, github_owner=None, pypi_owner=None):
        """ Storing pars as is. Name and target have some custom properties. """
        self._target = target
        self._github_owner = github_owner
        self._pypi_owner = pypi_owner

    @classmethod
    @deco_cache()
    def summary_packagers(cls):
        """ Packagers to hold summary of environment. """
        return [
            Packager(name="Mandera", github_owner="Mandera"),
            Packager(name=".github", github_owner="ManderaGeneral"),
        ]

    def spawn_children(self):
        """ :param generalpackager.Packager self: """
        for packager in self.get_dependants(only_general=True):
            if packager.localrepo.metadata.enabled:
                packager.set_parent(parent=self)

    def spawn_parents(self):
        """ :param generalpackager.Packager self: """
        for packager in self.get_dependencies(only_general=True):
            if packager.localrepo.metadata.enabled:
                self.set_parent(parent=packager)

    def __repr__(self):
        """ :param generalpackager.Packager self: """
        info = [self.target or "No Target"]
        info = str(info).replace("'", "")
        return f"<Packager {info}: {self.name}>"

















































