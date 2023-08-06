from generallibrary import CodeLine

from generalpackager.api.shared.files.file import File


class PrePushHookFile(File):
    _relative_path = ".git/hooks/pre-push"
    aesthetic = True

    def _generate(self):
        top = CodeLine()

        top.add_node(CodeLine("#!/usr/bin/env python"))
        top.add_node(CodeLine(f"from generalpackager import Packager", space_before=1))
        top.add_node(CodeLine(f"Packager(\"{self.packager.name}\").generate_localfiles(include_aesthetic=False, error_on_change=True)", space_before=1))

        return top
