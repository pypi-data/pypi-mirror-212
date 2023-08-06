
from generalpackager.api.shared.files.file import File
from generalpackager.other.licenses import License


class LicenseFile(File):
    _relative_path = "LICENSE"
    aesthetic = True

    def _generate(self):
        """ Generate LICENSE by using Packager.license. """
        return License(self.packager).apache2()

