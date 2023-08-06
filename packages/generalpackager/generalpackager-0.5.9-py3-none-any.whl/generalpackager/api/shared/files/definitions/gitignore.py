
from generalpackager.api.shared.files.file import File


class GitignoreFile(File):
    _relative_path = ".gitignore"
    aesthetic = False

    def _generate(self):
        return "\n".join(self.packager.git_exclude_lines)