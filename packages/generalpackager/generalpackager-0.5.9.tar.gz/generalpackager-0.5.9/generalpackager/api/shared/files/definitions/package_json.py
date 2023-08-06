import json

from generalpackager.api.shared.files.file import File


class PackageJsonFile(File):
    _relative_path = "package.json"
    aesthetic = False
    target = File.targets.node

    def _generate(self):
        info = {
            "name": self.packager.localrepo.name,
            "version": str(self.packager.localrepo.metadata.version),
            "description": self.packager.localrepo.metadata.description,
            "scripts": {
                "start": "parcel index.html",
                "build": "parcel build index.html",
                "test": "jest"
            },
            "dependencies": {dep: "latest" for dep in self.packager.localrepo.metadata.dependencies},
            "devDependencies": {dep: "latest" for dep in self.packager.localrepo.metadata.devDependencies},
            "keywords": self.packager.get_topics(),
            "license": self.packager.license,
            "author": self.packager.author,
        }
        return json.dumps(info, indent=4)

