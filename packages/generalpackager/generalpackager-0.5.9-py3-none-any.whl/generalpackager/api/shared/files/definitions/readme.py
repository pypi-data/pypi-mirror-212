import re

from generalfile import Path
from generallibrary import Markdown, deco_cache, flatten, exclusive, Date, comma_and_and
from generalpackager.api.shared.files.file import File


class ReadmeFile(File):
    _relative_path = "README.md"
    aesthetic = True


    CROSS = "❌"
    CHECK = "✔️"
    NO_DEP = "*No dependencies*"

    def get_badges_dict(self):
        """ Get badges as a dict. """
        return {
            "UnitTests": f"[![workflow Actions Status](https://github.com/ManderaGeneral/{self.packager.name}/workflows/workflow/badge.svg)](https://github.com/ManderaGeneral/{self.packager.name}/actions)",
            "Commit": f"![GitHub last commit](https://img.shields.io/github/last-commit/ManderaGeneral/{self.packager.name})",
            "Release": f"[![PyPI version shields.io](https://img.shields.io/pypi/v/{self.packager.name}.svg)](https://pypi.org/project/{self.packager.name}/)",
            "Python": f"[![PyPI pyversions](https://img.shields.io/pypi/pyversions/{self.packager.name}.svg)](https://pypi.python.org/pypi/{self.packager.name}/)",
            "Operating System": f"[![Generic badge](https://img.shields.io/badge/platforms-{'%20%7C%20'.join(self.packager.os)}-blue.svg)](https://shields.io/)",
        }

    def get_description_markdown(self):
        return Markdown(self.packager.localrepo.metadata.description, header=self.packager.name)

    def _get_package_string(self, name):
        if name == self.NO_DEP:
            return self.NO_DEP
        else:
            return Markdown.link(name, url=f"https://pypi.org/project/{name}", href=True)

    def _checked(self, packages, dependency):
        if dependency in packages:
            return self.CHECK
        elif dependency == self.NO_DEP:
            return self.CHECK
        else:
            return self.CROSS

    def get_installation_markdown(self):
        """ Get install markdown. """
        markdown = Markdown(header="Installation showing dependencies")

        dependencies_required = self.packager.localrepo.metadata.install_requires.copy()
        dependencies_optional = list(set().union(*self.packager.localrepo.metadata.extras_require.values()))
        dependencies_optional.sort()

        options = {self.packager.name: dependencies_required}
        options.update({f"{self.packager.name}[{key}]": value + dependencies_required for key, value in self.packager.localrepo.metadata.extras_require.items()})

        list_of_dicts = []

        all_deps = dependencies_required + dependencies_optional
        if not all_deps:
            all_deps = [self.NO_DEP]

        for dependency in all_deps:
            row = {"`pip install`": self._get_package_string(name=dependency)}
            for command, packages in options.items():
                pip_install = f"`{command}`"
                row[pip_install] = self._checked(packages=packages, dependency=dependency)
            list_of_dicts.append(row)

        markdown.add_table_lines(*list_of_dicts)

        return markdown

    def _header_from_path(self, path):
        stem = path.stem()
        if stem[0].isdigit():
            stem = stem[1:]
        header = stem.replace("_", " ").title()
        return header

    @staticmethod
    def _docstring_markdown(docstrings, index, parent):
        if len(docstrings) > index:
            docstring = docstrings[index]
            docstring = docstring.replace('"""', "")
            docstring_lines = [line.strip() for line in docstring.splitlines(keepends=True)]
            docstring_markdown = Markdown(parent=parent)
            docstring_markdown.add_lines(*docstring_lines)
            return docstring_markdown

    def get_examples_markdown(self):
        """ Read examples folder and convert to markdown. """
        markdown = Markdown(header="Examples")
        paths = self.packager.localrepo.get_examples_path().get_children()
        sorted_paths = sorted(paths, key=lambda path: path.name())
        for i, path in enumerate(sorted_paths):
            collapsible = i > 0
            example = Markdown(header=self._header_from_path(path=path), parent=markdown, collapsible=collapsible)

            lines = path.text.read()
            docstrings = re.findall(r'""".*?"""', lines, flags=re.S)

            self._docstring_markdown(docstrings=docstrings, index=0, parent=example)

            code = re.sub(r'""".*?"""', "", lines, flags=re.S)
            code_lines = code.strip().splitlines(keepends=True)
            if code_lines:
                code_markdown = Markdown(parent=example)
                code_markdown.add_code_lines(*code_lines, lang="python")

            self._docstring_markdown(docstrings=docstrings, index=1, parent=example)
        return markdown

    def _attr_repr(self, objInfo):
        """ Return a nice representation of each attribute made by this module, in this case a link to code definition. """
        text = repr(objInfo)
        path = objInfo.file(relative=True)

        line = objInfo.get_definition_line()
        return self.github_link_path_line(text=text, path=path, line=line)

    def _get_attributes_view(self):
        if self.packager.localmodule.module is None:
            return "No module to get attributes"
        return self.packager.localmodule.objInfo.view(custom_repr=self._attr_repr, print_out=False)

    def get_attributes_markdown(self):
        """ Get a recursive view of attributes markdown. """
        return Markdown(header="Attributes", collapsible=True).add_pre_lines(self._get_attributes_view())

    def _create_todo_dict(self, text, path, line):
        path = Path(path)
        return {
            "Package": Markdown.link(text=self.packager.name, url=self.packager.github.url),
            "Module": self.github_link_path_line(text=path.name(), path=path, line=1),
            "Message": self.github_link_path_line(text=text, path=path, line=line),
        }

    def github_link_path_line(self, text, path, line=None):
        if line is None:
            line = 1
        path = Path(path)
        return self.github_link(text=text, suffix=f"blob/{self.packager.localrepo.commit_sha_short()}/{path.encode()}#L{line}")

    def _get_codeline_todos(self):
        todos = []
        for path in self.packager.path.get_children(depth=-1, gen=True):
            if path.match(*self.packager.git_exclude_lines, "shelved.patch", "readme.md"):
                continue
            try:
                text = path.text.read()
            except:
                continue

            relative_path = path.relative(self.packager.path)

            for i, line in enumerate(text.splitlines()):
                result = re.findall("todo+: (.+)", line, re.I)
                if result:
                    text = re.sub('[" ]*$', "", result[0])
                    todos.append(self._create_todo_dict(text=text, path=relative_path, line=i + 1))
        return todos

    @deco_cache()
    def get_todos(self):
        """ Get a list of dicts containing cleaned up todos. """
        todos = self._get_codeline_todos()
        # Todo: Sort todos by name to decrease automatic commit changes.
        return todos

    def get_todos_markdown(self, *packagers, drop_package_col=False):
        todos = flatten([packager.get_todos() for packager in packagers])
        if drop_package_col:
            todos = [exclusive(todo, "Package") for todo in todos]

        markdown = Markdown(header="Todo", collapsible=True)
        if todos:
            markdown.add_table_lines(*todos)
        return markdown

    @staticmethod
    def _filt(markdown):
        return markdown.header and (markdown.lines or markdown.get_children())

    def _configure_contents_markdown(self, markdown):
        """ Configure table of contents lines from markdown. """
        parent_markdown = markdown.get_parent(-1, -1)
        markdown.add_pre_lines(parent_markdown.view(custom_repr=lambda md: md.link(md.header, href=True), print_out=False, filt=self._filt))
        return markdown

    @staticmethod
    def set_collapsible(markdown):
        for child in markdown.get_children(include_self=True):
            if child.collapsible is None and child.header:
                child.collapsible = False

    def get_footnote_markdown(self, commit=True):
        """ Get a markdown for footnote containing date, time and commit link. """
        line = f"Generated {Date.now()}"
        if commit:
            sha = self.localrepo.commit_sha_short()
            line += f" for commit {self.github_link(text=sha, suffix=f'commit/{sha}')}."

        return Markdown(line).wrap_with_tags("<sup>", "</sup>")

    def github_link(self, text, suffix):
        """ Get an HREF link to this repo's github. """
        url = f"{self.packager.github.url}/{suffix}"
        return Markdown.link(text=text, url=url, href=True)

    def get_mermaid_markdown(self):
        nodes = self.packager.get_ordered_packagers(include_private=False)
        # nodes = self.get_parents(depth=-1, include_self=True)
        repr_func = lambda pkg: pkg.simple_name
        url_func = lambda pkg: pkg.github.url
        highlight_self = True
        markdown = self.packager.mermaid(nodes=nodes, repr_func=repr_func, url_func=url_func, highlight_self=highlight_self)
        markdown.header = "Dependency Diagram for ManderaGeneral"
        return markdown

    def get_information_markdown(self, *packagers):
        if not packagers:
            packagers = (self.packager, )

        markdown = Markdown(header="Information")
        python_url = "https://www.python.org/downloads/release/python-"

        list_of_dicts = []
        for packager in packagers:
            package = Markdown.link(text=packager.name, url=packager.github.url)
            ver = Markdown.link(text=packager.localrepo.metadata.version, url=packager.pypi.url)
            latest_release = packager.get_latest_release()
            python = ", ".join([Markdown.link(text=ver, url=f"{python_url}{str(ver).replace('.', '')}0/") for ver in packager.python])
            platform = ", ".join(map(str.capitalize, packager.os))
            cover = self.CROSS if packager.localrepo.coverage is None else f"{packager.localrepo.coverage} %"

            list_of_dicts.append({
                "Package": package,
                "Ver": ver,
                "Latest Release": latest_release,
                "Python": python,
                "Platform": platform,
                "Cover": cover,
            })
        markdown.add_table_lines(*list_of_dicts, sort_by=["Package"])
        return markdown

    def get_contributions_markdown(self):
        markdown = Markdown(header="Contributions")
        welcome = ["Issue-creation", "discussions"]
        contribute = self.packager.localrepo.metadata.contribute

        if contribute:
            welcome.append("pull requests")
        markdown.add_lines(f"{comma_and_and(*welcome, period=False)} are most welcome!",)
        if not contribute:
            markdown.add_lines("", "Please hold off on submitting pull requests until all the necessary legal issues have been sorted out.")
        return markdown

    def _generate(self):
        # Description
        markdown = self.get_description_markdown()

        # Table of contents
        contents = Markdown(header="Table of Contents", parent=markdown, collapsible=True)

        # Mermaid
        self.get_mermaid_markdown().set_parent(parent=markdown)

        # Installation
        self.get_installation_markdown().set_parent(parent=markdown)

        # Information
        self.get_information_markdown().set_parent(parent=markdown)

        # Examples
        self.get_examples_markdown().set_parent(parent=markdown)

        # Attributes
        self.get_attributes_markdown().set_parent(parent=markdown)

        # Contributions
        self.get_contributions_markdown().set_parent(parent=markdown)

        # Todos
        self.get_todos_markdown(self, drop_package_col=True).set_parent(parent=markdown)

        # Table of contents - Configuration
        self._configure_contents_markdown(markdown=contents)

        # Generation timestamp
        self.get_footnote_markdown().set_parent(parent=markdown)

        self.set_collapsible(markdown)

        return markdown

