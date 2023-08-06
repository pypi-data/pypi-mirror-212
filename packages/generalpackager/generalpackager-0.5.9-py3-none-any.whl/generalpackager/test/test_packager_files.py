from generalfile import Path
from generalfile.test.test_path import PathTest

from generalpackager import Packager


class TestPackager(PathTest):
    """ Inside workflow:
        generate_localfiles """

    def test_relative_path_is_aesthetic(self):
        packager = Packager()
        self.assertEqual(False, packager.setup_file.aesthetic)
        self.assertEqual(True, packager.readme_file.aesthetic)

    def test_compare_local_to_github(self):
        packager = Packager()
        packager.compare_local_to_github()

    def test_compare_local_to_pypi(self):
        packager = Packager()
        packager.compare_local_to_pypi()

    def test_generate_setup(self):
        packager = Packager()
        text = packager.setup_file._generate()
        self.assertIn(str(packager.localrepo.metadata.version), text)
        self.assertIn(str(packager.localrepo.name), text)

    def test_generate_manifest(self):
        packager = Packager()
        text = packager.manifest_file._generate()
        self.assertIn("include metadata.json", text)

    def test_generate_git_exclude(self):
        packager = Packager()
        text = packager.git_exclude_file._generate()
        self.assertIn(".idea", text)

    def test_generate_license(self):
        packager = Packager()
        text = packager.license_file._generate()
        self.assertIn("Mandera", text)

    def test_generate_workflow(self):
        packager = Packager()
        text = packager.workflow_file._generate()
        self.assertIn("runs-on", text)

    def test_generate_readme(self):
        packager = Packager()
        text = str(packager.readme_file._generate())
        self.assertIn("pip install", text)

    def test_generate_personal_readme(self):
        packager = Packager()
        self.assertIsNotNone(packager.path)
        text = str(packager.org_readme_file._generate())
        self.assertIn("generallibrary", text)

    def test_generate_generate(self):
        packager = Packager()
        text = str(packager.generate_file._generate())
        self.assertIn("Packager", text)

    def test_generate_init(self):
        packager = Packager()
        text = str(packager.init_file._generate())
        self.assertEqual(True, len(text) > 2)

    def test_generate_test_python(self):
        packager = Packager()
        text = str(packager.test_template_file._generate())
        self.assertIn("unittest", text)

    def test_all_files_by_relative_path(self):
        self.assertIn(Path("README.md"), Packager().get_files_by_relative_path())
        self.assertIn(Path("setup.py"), Packager().get_files_by_relative_path())

    def test_create_blank_locally_python(self):
        Packager("newblank").create_blank_locally(install=False)
        self.assertEqual(True, Path("newblank/README.md").exists())
        self.assertEqual(True, Path("newblank/newblank").exists())

    def test_file_by_relative_path(self):
        self.assertIs(Packager().readme_file, Packager().get_file_from_path("README.md"))
        self.assertIs(None, Packager().get_file_from_path("doesntexist"))

    def test_file_secret_readme(self):
        self.assertIs(Packager(), Packager().org_readme_file.packager)

    def test_run_ordered_methods(self):
        x = []
        def a(_): x.append(1)
        def b(_): x.append(2)
        Packager().run_ordered_methods(a, b)
        length = len(Packager().workflow_packagers())
        self.assertEqual([1] * length + [2] * length, x)


