
from generalpackager.api.shared.files.file import File


class ManifestFile(File):
    _relative_path = "MANIFEST.in"
    aesthetic = False

    def _generate(self):
        default_manifest = [
            self.packager.metadata_file.relative_path
        ]
        paths = self.packager.localrepo.metadata.manifest + default_manifest
        return "\n".join([f"include {path}" for path in paths])

