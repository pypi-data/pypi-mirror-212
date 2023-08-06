
from generalpackager.api.shared.files.file import File


class GitExcludeFile(File):
    _relative_path = ".git/info/exclude"
    is_file = True
    aesthetic = True

    def _generate(self):
        return "\n".join(self.packager.git_exclude_lines)

