from generalfile.test.test_path import PathTest
from generallibrary import Log
from generalpackager.api.venv import Venv


class TestVenv(PathTest):
    def test_create_venv(self):
        prev_venv_path = Venv.get_active_venv_path()

        venv = Venv("new_venv")
        self.assertEqual(False, venv.exists())

        venv.create_venv()
        self.assertEqual(True, venv.exists())

        self.assertEqual(False, venv.active())
        with venv:
            self.assertEqual(True, venv.active())
            self.assertIn(venv.path, venv.list_venv_paths())
        self.assertEqual(False, venv.active())

        self.assertEqual(prev_venv_path, Venv.get_active_venv_path())
        venv.upgrade()
        venv.python_version()
        self.assertEqual(prev_venv_path, Venv.get_active_venv_path())


    def test_list_python_versions(self):
        Log("root").configure_stream()  # Would be nice to configure artifact for github actions https://github.com/ManderaGeneral/generallibrary/issues/25
        self.assertGreaterEqual(len(Venv.list_python_versions()), 1)


















