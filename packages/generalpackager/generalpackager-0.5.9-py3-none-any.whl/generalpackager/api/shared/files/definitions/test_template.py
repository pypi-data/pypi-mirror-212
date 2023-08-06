from generallibrary import CodeLine

from generalpackager.api.shared.files.file import File


class TestTemplateFile(File):
    @property
    def _relative_path(self):
        return f"{self.packager.name}/test/test_{self.packager.name}.py"

    overwrite = False
    is_file = True
    target = File.targets.python
    aesthetic = True

    def _generate(self):
        top = CodeLine()
        top.add_node(CodeLine("from unittest import TestCase", space_after=2))
        top.add_node("class Test(TestCase):").add_node("def test(self):").add_node("pass")
        return top

