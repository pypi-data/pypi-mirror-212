import re
import sys

from generalfile import Path
from generallibrary import deco_cache, Ver, Terminal, debug, DecoContext, deco_require, VerInfo, Log
from generalpackager.api.venv_cruds import _Venv_Cruds


class Venv(DecoContext, _Venv_Cruds):
    """ Standalone API of Python venv, unlike the other APIs this one is not included in Packager. """
    ver_info = VerInfo()

    def __init__(self, path=None):
        self.path = Path(path)
        self.previous_venv = None

    @classmethod
    def get_active_venv(cls):
        active_venv_path = Path.get_active_venv_path()
        if active_venv_path is not None:
            return Venv(path=active_venv_path)

    @classmethod
    def get_active_venv_path(cls):
        active_venv = cls.get_active_venv()
        if active_venv:
            return active_venv.path

    @classmethod
    def get_active_python(cls, local):
        active_venv = cls.get_active_venv()
        if active_venv is None:
            if local is True:
                raise EnvironmentError("A local python path was requested but there's no active venv. Returning global instead.")
                # Log(__name__).warning("A local python path was requested by there's no active venv. Returning global instead.")
            return cls.python_sys_executable_path()
        return active_venv.python_path(local=local)

    def before(self, *args, **kwargs):
        self.activate()

    def after(self, *args, **kwargs):
        if self.previous_venv:
            self.previous_venv.activate()
        else:
            self.deactivate()

    def exe_name(self): return "python.exe" if self.ver_info.windows else "python"  # This is similar to Terminal requiring .cmd

    def pyvenv_cfg_path(self):  return self.path / "pyvenv.cfg"
    def scripts_path(self):     return self.path / self.ver_info.venv_script_path
    def python_exe_path(self):  return self.scripts_path() / self.exe_name()
    def site_packages_path(self):  return self.path / "Lib/site-packages"
    def easy_install_path(self):  return self.site_packages_path() / "easy-install.pth"
    def python_home_path(self): return Path(path=self.cfg()["home"])
    def python_home_exe_path(self): return self.python_home_path() / self.exe_name()
    @classmethod
    def python_sys_executable_path(cls): return Path(path=sys.executable)

    def python_path(self, local):
        if local:
            return self.python_exe_path()
        else:
            return self.python_home_exe_path()

    def exists(self):
        return self.path.is_venv()

    def active(self):
        return Path.get_active_venv_path() is self.path

    def create_venv(self, python_path=None, ver=None):
        assert self.path.empty()

        if python_path:
            python = python_path
        elif ver:
            python = self.list_python_versions()[ver]
        else:
            python = True

        return Terminal("-m", "venv", self.path, python=python).string_result

    @classmethod
    def deactivate(cls):
        active_venv = Venv.get_active_venv()
        if active_venv:
            active_venv.cruds.EnvVar_PATH.unset()
            active_venv.cruds.EnvVar_VENV.unset()
            active_venv.cruds.sys_path_scripts.unset()
            active_venv.cruds.sys_path_site.unset()
            return active_venv

    @deco_require(exists)
    def activate(self):
        self.previous_venv = self.deactivate()
        self.cruds.EnvVar_PATH.set()
        self.cruds.EnvVar_VENV.set()
        self.cruds.sys_path_scripts.set()
        self.cruds.sys_path_site.set()

        # Not sure these two do anything, doubt you can change interpreter during runtime
        # https://github.com/ManderaGeneral/generalpackager/issues/60
        sys.prefix = self.path
        sys.executable = self.python_exe_path()

    @deco_require(exists)
    def upgrade(self):
        return Terminal("-m", "ensurepip", "--upgrade", capture_output=False, python=self.python_exe_path()).string_result

    @deco_require(exists)
    @deco_cache()
    def cfg(self):
        r""" Example: https://github.com/ManderaGeneral/generalpackager/issues/57#issuecomment-1399402211 """
        return self.pyvenv_cfg_path().cfg.read()

    def python_version(self):
        return Ver(self.cfg().get("version") or self.cfg().get("version_info"))

    @staticmethod
    def list_venv_paths(path=None):
        """ Search parent folder of active venv path for venvs. """
        active_venv_path = Path.get_active_venv_path()
        if path is None and active_venv_path:
            path = active_venv_path.get_parent()
        else:
            path = Path(path)
        return path.get_children(filt=lambda p: p.is_venv())

    @classmethod
    def list_python_versions(cls):
        """ Examples here: https://github.com/ManderaGeneral/generalpackager/issues/58 """
        if cls.ver_info.windows:
            pythons = cls._list_python_versions_windows()
        else:
            pythons = cls._list_python_versions_linux()

        return {version: path for version, path in pythons.items() if path.is_file() and not path.get_parent_venv()}

    @staticmethod
    def _list_python_versions_windows():
        info_string = Terminal("py", "--list-paths").string_result
        versions = {}
        for line in info_string.splitlines():
            version, *_, path = line.split()  # Example: '-V:3.11 *        C:\Users\ricka\AppData\Local\Programs\Python\Python311\python.exe'
            version = version.split(":")[-1]  # Example: '-V:3.11'
            path = Path(path=path)
            versions[version] = path
        return versions

    @classmethod
    def _list_python_versions_linux(cls):
        versions = {}
        info_string = Terminal("whereis", "python").string_result
        for path_str in info_string.split()[1:]:
            path = Path(path=path_str)
            if not path.is_file():
                continue
            if not re.search("python(\d\.\d+)?$", path_str):
                continue
            terminal = Terminal(path, "--version", error=False)
            if terminal.fail:
                continue
            version = ".".join(terminal.string_result.split(" ")[1].split(".")[:2])  # Example: "Python 3.11.0"
            versions[version] = path
        return versions

    def __str__(self):
        return f"<Venv: {self.path}>"

    @staticmethod
    def debug():

        debug(locals(),
              "os.environ['PATH']",
              "os.environ['VIRTUAL_ENV']",
              "sys.prefix",
              "sys.path",
              "sys.executable",
              )

