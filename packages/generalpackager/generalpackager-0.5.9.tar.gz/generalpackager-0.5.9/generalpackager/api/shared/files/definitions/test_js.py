from generallibrary import CodeLine

from generalpackager.api.shared.files.file import File


class TestJsFile(File):
    _relative_path = "test.js"
    aesthetic = False
    overwrite = False
    target = File.targets.node

    def _generate(self):
        top = CodeLine()
        top.add_node("/**")
        top.add_node(" * @jest-environment jsdom")
        top.add_node(CodeLine(" */", space_after=1))
        top.add_node(CodeLine("// https://jestjs.io/docs/configuration#testenvironment-string", space_after=1))
        top.add_node(CodeLine('const Vec2 = require("./vec2");', space_after=1))
        top.add_node('test("Vec2 initializing", () => {').add_node("expect(new Vec2().x).toBe(0);")
        top.add_node("})")
        return top

