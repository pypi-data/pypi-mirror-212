from generallibrary import CodeLine

from generalpackager.api.shared.files.file import File


class SetupFile(File):
    _relative_path = "setup.py"
    aesthetic = False

    def _topics_to_classifiers(self, *topics):
        classifiers = []
        for topic in topics:
            if topic.startswith("python"):
                major = topic[6]
                minor = topic[7:]
                classifiers.append(f"Programming Language :: Python :: {major}.{minor}")
            else:
                classifiers.append(self._lib[topic])
        return classifiers

    def get_classifiers(self):
        """ Get a complete list of classifiers generated from topics and other metadata. """
        return self._topics_to_classifiers(*self.packager.get_topics())

    def _generate(self):
        setup_kwargs = {
            "name": f'"{self.packager.localrepo.name}"',
            "author": f"'{self.packager.author}'",
            "author_email": f'"{self.packager.email}"',
            "version": f'"{self.packager.localrepo.metadata.version}"',
            "description": f'"{self.packager.localrepo.metadata.description}"',
            "long_description": "long_description",
            "long_description_content_type": '"text/markdown"',
            "install_requires": self.packager.localrepo.metadata.install_requires,
            "url": f'"{self.packager.github.url}"',
            "license": f'"{self.packager.license}"',
            "packages": 'find_namespace_packages(exclude=("build*", "dist*"))',
            "extras_require": self.packager.localrepo.metadata.extras_require,
            "classifiers": self.packager.get_classifiers(),
        }

        top = CodeLine()
        top.add_node(CodeLine("from setuptools import setup, find_namespace_packages", space_before=1))
        top.add_node(CodeLine("from pathlib import Path", space_after=1))

        top.add_node(CodeLine("try:")).add_node(CodeLine("long_description = (Path(__file__).parent / 'README.md').read_text(encoding='utf-8')"))
        top.add_node(CodeLine("except FileNotFoundError:")).add_node(CodeLine("long_description = 'Readme missing'", space_after=1))

        setup = top.add_node(CodeLine("setup("))
        for key, value in setup_kwargs.items():
            if isinstance(value, list) and value:
                list_ = setup.add_node(CodeLine(f"{key}=["))
                for item in value:
                    list_.add_node(CodeLine(f"'{item}',"))
                setup.add_node(CodeLine("],"))
            elif isinstance(value, dict) and value:
                dict_ = setup.add_node(CodeLine(f"{key}={{"))
                for k, v in value.items():
                    dict_.add_node(CodeLine(f"'{k}': {v},"))
                setup.add_node(CodeLine("},"))
            else:
                setup.add_node(CodeLine(f"{key}={value},"))

        top.add_node(CodeLine(")"))

        return top.text()

    _lib = {
        "planning": "Development Status :: 1 - Planning",
        "pre-alpha": "Development Status :: 2 - Pre-Alpha",
        "alpha": "Development Status :: 3 - Alpha",
        "beta": "Development Status :: 4 - Beta",
        "production/Stable": "Development Status :: 5 - Production/Stable",
        "mature": "Development Status :: 6 - Mature",
        "inactive": "Development Status :: 7 - Inactive",

        "utility": "Topic :: Utilities",

        "tool": "Topic :: Software Development :: Build Tools",
        "library": "Topic :: Software Development :: Libraries",
        "gui": "Topic :: Software Development :: User Interfaces",

        "file-manager": "Topic :: Desktop Environment :: File Managers",

        "mit-license": "License :: OSI Approved :: MIT License",

        "windows": "Operating System :: Microsoft :: Windows",
        "macos": "Operating System :: MacOS",
        "ubuntu": "Operating System :: POSIX :: Linux",
    }
