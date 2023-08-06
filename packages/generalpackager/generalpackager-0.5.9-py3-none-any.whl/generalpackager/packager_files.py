
from generalfile import Path
from generallibrary import deco_cache, Timer


class _PackagerFiles:
    def create_blank_locally(self, install=True):
        """ Create a new general package locally only.
            Todo: Fix create_blank, it overwrites current projects pip install.
            :param generalpackager.Packager self:
            :param install: Whether to pip install. """
        assert self.path.empty()
        self.localrepo.metadata.write_config()
        self.generate_localfiles()
        if install:
            self.localrepo.install(editable=True)

    @deco_cache()
    def _compare_local(self, package_host, aesthetic):
        """ :param generalpackager.Packager self:
            :param generalpackager.api.shared.protocols.PackageHostProtocol package_host: """
        def filt(path):
            """ Filter to return True for files we want to compare. """
            if path.match(*self.git_exclude_lines):
                return False
            if aesthetic is not None:
                file = self.get_file_from_path(path=path)
                if file is None:
                    return True  # Probably a python file
                return file.aesthetic is aesthetic
            return True

        unpack_target = Path.get_cache_dir() / "Python"
        version = package_host.get_version()
        package_path = package_host.download(path=unpack_target, version=version, overwrite=True)
        return self.path.get_differing_files(target=package_path, filt=filt)

    def compare_local_to_github(self, aesthetic=None):
        """ Get a list of changed files compared to remote with optional aesthetic files.

            :param generalpackager.Packager self:
            :param aesthetic: """
        return self._compare_local(package_host=self.github, aesthetic=aesthetic)

    def compare_local_to_pypi(self, aesthetic=None):
        """ Get a list of changed files compared to pypi with optional aesthetic files.

            :param generalpackager.Packager self:
            :param aesthetic: """
        return self._compare_local(package_host=self.pypi, aesthetic=aesthetic)

    def _error_on_change(self, files):
        """ :param generalpackager.Packager self: """
        file_paths = {file.path for file in files}
        changed_files = {path.absolute() for path in self.localrepo.changed_files()}

        changed_generated_files = file_paths.intersection(changed_files)
        if changed_generated_files:
            raise EnvironmentError(f"Files changed: {changed_generated_files}")

    def generate_localfiles(self, include_aesthetic=True, print_out=False, error_on_change=False):
        """ Generate all local files.
            Returns True if any file is changed.

            :param generalpackager.Packager self: """
        with Timer(print_out=print_out):
            # Not in files because it writes with json not text, it's also a bit unique
            self.localrepo.metadata.name = self.name
            self.localrepo.metadata.write_config()

            files = [file for file in self.get_files() if include_aesthetic or not file.aesthetic]

            for file in files:
                file.generate()

        if error_on_change and "[CI SKIP]" not in self.localrepo.commit_message():
            self._error_on_change(files=files)

    # https://coda.io/@rickard-abraham/python-dunders/ignored-files-2
    git_exclude_lines = npm_ignore_lines = (
        "__pycache__/",
        "*.py[cod]",
        "*$py.class",
        "*.so",
        "celerybeat-schedule",
        ".Python",
        "build/",
        "develop-eggs/",
        "dist/",
        "downloads/",
        "eggs/",
        ".eggs/",
        "lib/",
        "lib64/",
        "parts/",
        "sdist/",
        "var/",
        "wheels/",
        "pip-wheel-metadata/",
        "share/python-wheels/",
        "*.egg-info/",
        ".installed.cfg",
        "*.egg",
        "MANIFEST",
        "*.log",
        "local_settings.py",
        "db.sqlite3",
        "db.sqlite3-journal",
        "docs/pydoc/temp/",
        ".env",
        ".venv",
        "env/",
        "venv/",
        "ENV/",
        "env.bak/",
        "venv.bak/",
        "instance/",
        ".webassets-cache",
        "pip-log.txt",
        "pip-delete-this-directory.txt",
        "profile_default/",
        "ipython_config.py",
        ".ipynb_checkpoints",
        ".git/",
        "**test/tests/",
        "PKG-INFO/",
        "setup.cfg",
        "node_modules/",
        ".parcel-cache",
        "/site",
        ".mypy_cache/",
        ".dmypy.json",
        "dmypy.json",
        "#Pipfile.lock"
        "target/",
        ".idea/",
        ".python-version",
        "__pypackages__/",
        "*.manifest",
        "*.spec",
        ".pyre/",
        ".ropeproject",
        "*.sage.py",
        ".scrapy",
        ".spyderproject",
        ".spyproject",
        "*.mo",
        "*.pot",
        "htmlcov/",
        ".tox/",
        ".nox/",
        ".coverage",
        ".coverage.*",
        ".cache",
        "nosetests.xml",
        "coverage.xml",
        "*.cover",
        "*.py,cover",
        ".hypothesis/",
        ".pytest_cache/",
        ".vscode",
    )























