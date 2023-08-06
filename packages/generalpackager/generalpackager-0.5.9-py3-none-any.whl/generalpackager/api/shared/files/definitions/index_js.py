from generallibrary import CodeLine

from generalpackager.api.shared.files.file import File


class IndexJsFile(File):
    _relative_path = "index.js"
    overwrite = False
    aesthetic = True
    target = File.targets.node

    def _generate(self):
        top = CodeLine()
        top.add_node(CodeLine('exports.Vec2 = require("./vec2");', space_before=1, space_after=1))
        return top

