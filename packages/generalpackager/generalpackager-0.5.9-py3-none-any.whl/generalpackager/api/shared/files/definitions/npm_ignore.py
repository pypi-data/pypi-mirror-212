
from generalpackager.api.shared.files.file import File


class NpmIgnoreFile(File):
    _relative_path = ".npmignore"
    aesthetic = True
    target = File.targets.node

    def _generate(self):
        return "\n".join(self.packager.npm_ignore_lines)

