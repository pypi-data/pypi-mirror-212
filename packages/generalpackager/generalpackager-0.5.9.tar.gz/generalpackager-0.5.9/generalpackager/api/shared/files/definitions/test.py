
from generalpackager.api.shared.files.file import File


class TestFile(File):
    @property
    def _relative_path(self):
        return f"{self.packager.name}/test"

    aesthetic = False
    is_file = False


