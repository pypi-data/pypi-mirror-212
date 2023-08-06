from generallibrary import deco_cache

from generalpackager.api.shared.files.file_fetcher import FileFetcher
from generalfile import Path


class _Files:
    """ LocalRepo and Packager inherits this.
        Only an instance of Packager will return file instances. """
    @classmethod
    @deco_cache()
    def get_filenames(cls):
        """ :param generalpackager.Packager or generalpackager.LocalRepo cls: """
        return [filename for filename in dir(_Files) if filename.endswith("_file")]

    @deco_cache()
    def get_files(self):
        """ :param generalpackager.Packager or generalpackager.LocalRepo self: """
        return [getattr(self, filename) for filename in self.get_filenames()]

    @deco_cache()
    def get_files_by_relative_path(self):
        """ :param generalpackager.Packager or generalpackager.LocalRepo self: """
        return {file.relative_path: file for file in self.get_files()}

    @deco_cache()
    def get_file_from_path(self, path):
        """ :param generalpackager.Packager or generalpackager.LocalRepo self: """
        path = Path(path).relative(self.path)
        return self.get_files_by_relative_path().get(path)


    commit_editmsg_file = FileFetcher()
    examples_folder = FileFetcher()
    exeproduct_folder = FileFetcher()
    exetarget_file = FileFetcher()
    generate_file = FileFetcher()
    git_exclude_file = FileFetcher()
    gitignore_file = FileFetcher()
    index_js_file = FileFetcher()
    init_file = FileFetcher()
    license_file = FileFetcher()
    manifest_file = FileFetcher()
    metadata_file = FileFetcher()
    npm_ignore_file = FileFetcher()
    org_readme_file = FileFetcher()
    package_json_file = FileFetcher()
    pre_commit_hook_file = FileFetcher()
    pre_push_hook_file = FileFetcher()
    readme_file = FileFetcher()
    setup_file = FileFetcher()
    test_folder = FileFetcher()
    test_js_file = FileFetcher()
    test_template_file = FileFetcher()
    workflow_file = FileFetcher()
    workflow_dev_file = FileFetcher()



# Helper function to generate Files
if __name__ == "__main__":
    definitions = Path("./definitions").get_children()
    definitions = sorted(definitions, key=lambda path: path.name())
    for definition in definitions:
        stem = definition.stem()
        if stem.startswith("_"):
            continue

        filefetcher = FileFetcher()
        filefetcher.name = stem
        file = filefetcher.cls

        suffix = "file" if file.is_file else "folder"
        print(f"    {stem}_{suffix} = FileFetcher()")

