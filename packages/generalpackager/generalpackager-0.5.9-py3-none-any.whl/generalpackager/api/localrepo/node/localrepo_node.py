from typing import List

from generalfile import Path
from generallibrary import Terminal, Log, deco_require
from generalpackager.api.localrepo.base.localrepo import LocalRepo
from generalpackager.api.localrepo.node.metadata_node import Metadata_Node


class LocalRepo_Node(LocalRepo):
    target = LocalRepo.Targets.node
    _cls_metadata = Metadata_Node

    NODE_MODULES = "node_modules"
    GLOBAL = "-g"

    @classmethod
    def _terminal(cls, cli, *args, local=None, **kwargs):
        if local:
            args = [s for s in args if s != cls.GLOBAL]

        Log(__name__).debug(args)
        return Terminal(cli, *args, **kwargs)

    @classmethod
    def _filt(cls, path):
        return (path / cls.NODE_MODULES).exists()

    def _node_modules_parent_path(self):
        contains_node_modules = self.path.get_parent(depth=-1, include_self=True, traverse_excluded=True, filt=self._filt)
        return contains_node_modules or self.path

    def package_folder(self, local=True):
        if local:
            return self._node_modules_parent_path() / self.NODE_MODULES

        npm_root = self._terminal("npm", "root", "-g").string_result
        return Path(path=npm_root)

    def run_tests(self):
        with self.path.as_working_dir():
            self._terminal("jest", capture_output=False)

    INSTALL = "install"
    UNINSTALL = "uninstall"

    def _stall(self, local, editable, cmd):
        if not editable:
            raise NotImplementedError("NPM does not support non-editable installs with local source.")

        if cmd == self.UNINSTALL:
            name = self.name
        else:
            name = self.path.absolute()

        package_folder = self.package_folder(local=local)
        with package_folder.as_working_dir():
            self._terminal("npm", cmd, self.GLOBAL, name, capture_output=False)

    @deco_require(LocalRepo.exists)
    def install(self, local=True, editable=True):
        self._stall(local=local, editable=editable, cmd=self.INSTALL)

    @deco_require(LocalRepo.exists)
    def uninstall(self, local=True, editable=True):
        self._stall(local=local, editable=editable, cmd=self.UNINSTALL)

    @deco_require(LocalRepo.exists)
    def publish(self, public=True):
        with self.path.as_working_dir():
            self._terminal("npm", "publish", capture_output=False)

    def _list_packages_gen(self, local=True, editable=None) -> List[str]:
        package_folder = self.package_folder(local=local)
        with package_folder.as_working_dir():
            terminal = self._terminal("npm", "list", "-g", error=False)

        if terminal.fail:
            return

        for line in terminal.string_result.splitlines():
            if "-- " in line and "@" in line:
                base, *link = line.split(" -> ")
                if editable is None or editable is bool(link):
                    *scoped, name, version = base.split()[1].split("@")
                    yield f"@{name}" if scoped else name

















