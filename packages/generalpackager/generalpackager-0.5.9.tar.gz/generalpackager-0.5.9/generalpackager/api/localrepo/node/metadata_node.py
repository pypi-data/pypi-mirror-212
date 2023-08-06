from generalpackager.api.localrepo.base.metadata import _Metadata
from generalpackager.api.shared.target import Targets


class Metadata_Node(_Metadata):
    target = Targets.node
    dependencies = []
    devDependencies = []

    def read_hook_post(self):
        devDependencies = self.halt_getattr("devDependencies")
        for dep in ("jest-environment-jsdom", "parcel"):
            if dep not in devDependencies:
                devDependencies.append(dep)

































