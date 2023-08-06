from generalfile import Path
from generallibrary import Log

from generalpackager.api.venv import Venv


class _PackagerEnvironment:
    @classmethod
    def new_clean_environment(cls, path=None, python_version=None):
        """ Creates a new clean environment for the packages.
            - Create, upgrade, and activate venv
            - Clone repos
            - Editable repo installs in venv

            :param generalpackager.Packager or any cls: """
        path = Path(path=path)
        path.open_folder()

        if python_version is None:
            python_version = cls.python[-1]

        # This could be a general Path method
        if not path.empty():
            if input("Warning: Folder isn't empty, clear it? ").lower() != "y":
                return
            path.delete_folder_content()
        elif input("Proceed with creating a new clean environment in this folder? ").lower() != "y":
            return

        Log("root").configure_stream()

        repos_path = path / "repos"
        venvs_path = path / "venvs"
        venv_path = venvs_path / f"python{python_version.replace('.', '')}"

        node_modules_string = cls.localrepo._cls_target_classes[cls.Targets.node].NODE_MODULES
        (path / node_modules_string).create_folder()

        venv = Venv(path=venv_path)
        venv.create_venv(ver=python_version)
        venv.upgrade()
        venv.activate()

        for packager in cls.packagers_from_packages():  # This will get all packages
            packager.github.download(path=repos_path)

        for packager in cls.get_ordered_packagers():  # This will only get python packages
            new_packager = cls(name=packager.name, path=repos_path / packager.name)
            new_packager.localrepo.install(editable=True)






