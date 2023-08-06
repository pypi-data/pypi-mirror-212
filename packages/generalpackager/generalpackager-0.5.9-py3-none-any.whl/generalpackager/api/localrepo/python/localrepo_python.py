import sys
from typing import List

from coverage import Coverage

from generalfile import Path
from generallibrary import Terminal, deco_require, Log, RedirectStdout
from generalpackager.api.localrepo.base.localrepo import LocalRepo
from generalpackager.api.localrepo.python.metadata_python import Metadata_Python


class LocalRepo_Python(LocalRepo):
    target = LocalRepo.Targets.python
    _cls_metadata = Metadata_Python

    # Put in generalfile?
    @staticmethod
    def get_python_exe_path():
        """ Return an absolute path to the current python exe file. """
        return Path(sys.executable)

    def run_tests(self):
        """ Run unittests for this repository.
            Sets self.coverage to total percentage with one decimal. """

        with self.get_test_path().as_working_dir():
            Terminal("coverage", "run", "-m", "unittest", "discover", capture_output=False)
            coverage = Coverage()
            coverage.load()
            with RedirectStdout():
                self.coverage = round(coverage.report(), 1)

        # Terminal("-m", "unittest", "discover", str(self.get_test_path()), python=True)

    @staticmethod
    def _venv_and_python(local):
        active_venv = Venv.get_active_venv()
        python = Venv.get_active_python(local=local)
        return active_venv, python

    @deco_require(LocalRepo.exists)
    def install(self, local=True, editable=False):
        """ Install this repository with pip. """
        active_venv, python = self._venv_and_python(local=local)

        args = [python, "-m", "pip", "install", "-e", self.name]
        if not editable:
            args.remove("-e")

        with self.path.get_parent().as_working_dir():
            Log().debug(f"Pip install for {self}")

            with active_venv.easy_install_path().as_renamed("TEMP_easy_install", overwrite=True):
                Terminal(*args, capture_output=False)
            self.set_easy_install_value()

    def set_easy_install_value(self, venv):
        venv.cruds.Path_easy_install.set_value(value=self.path)

    @deco_require(LocalRepo.exists)
    def uninstall(self, local=True):
        """ Uninstall this repository with pip. """
        active_venv, python = self._venv_and_python(local=local)

        Terminal(python, "-m", "pip", "uninstall", "-y", self.metadata.name)
        active_venv.cruds.Path_easy_install.unset_value(value=self.path)

    @deco_require(LocalRepo.exists)
    def _create_sdist(self):
        """ Create source distribution. """
        with self.path.as_working_dir():
            Terminal("setup.py", "sdist", "bdist_wheel", python=True)

    @deco_require(LocalRepo.exists)
    def publish(self, public=True):
        """ Upload local repo to PyPI.
            Todo: Make sure twine is installed when trying to upload to pypi.
            Todo: Look into private PyPI server where we could also do dry runs for test.
            https://github.com/pypa/twine/issues/207"""
        if not public:
            raise NotImplementedError

        if self.metadata.private:
            raise AttributeError("Cannot upload private repo.")

        self._create_sdist()
        with self.path.as_working_dir():
            Terminal("-m", "twine", "upload", "dist/*", python=True)

    @deco_require(LocalRepo.exists)
    def generate_exe(self, file_path=None):
        """ Generate an exe file for target file_path python file. """
        if file_path is None:
            file_path = self.get_exetarget_path()
        assert file_path.exists()

        with self.path.as_working_dir():
            Terminal("-m", "PyInstaller", file_path, "--onefile", "--windowed", python=True)

    def _list_packages_gen(self, local=True, editable=None):
        active_venv, python = self._venv_and_python(local=local)
        pip_list_result = Terminal(python, "-m", "pip", "list").string_result
        for line in pip_list_result.splitlines()[2:]:
            split_line = line.split()
            if len(split_line) not in (2, 3):
                continue

            name, version, *editable_path = split_line
            if editable is None or editable is bool(editable_path):
                yield name

    def package_folder(self, local=True):
        venv = Venv.get_active_venv()
        if local:
            return venv.path
        elif venv:
            return venv.python_home_path()
        return Venv.python_sys_executable_path().get_parent()


from generalpackager.api.venv import Venv

