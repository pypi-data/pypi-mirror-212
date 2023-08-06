from generallibrary import interconnect

from generalpackager.other.envvars import GH_TOKEN, TWINE_USERNAME, TWINE_PASSWORD

from generalpackager.packager import Packager

from generalpackager.api.localrepo.base.localrepo import LocalRepo
from generalpackager.api.localrepo.python.localrepo_python import LocalRepo_Python
from generalpackager.api.localrepo.node.localrepo_node import LocalRepo_Node

from generalpackager.api.localmodule import LocalModule
from generalpackager.api.package_hosts.github import GitHub
from generalpackager.api.package_hosts.pypi import PyPI

from generalpackager.api.venv import Venv

interconnect(Packager, LocalRepo, LocalModule, GitHub, PyPI)

