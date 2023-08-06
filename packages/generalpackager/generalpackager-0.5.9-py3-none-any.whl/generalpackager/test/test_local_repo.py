from generalfile import Path
from generalfile.test.test_path import PathTest
from generallibrary import Ver
from generalpackager.api.localrepo.base.localrepo import LocalRepo
from generalpackager.api.localrepo.python.localrepo_python import LocalRepo_Python
from generalpackager.api.localrepo.top.target_helper import localrepo


class TestLocalRepo(PathTest):
    def test_metadata_exists(self):
        self.assertEqual(True, localrepo().metadata_exists())
        self.assertEqual(False, localrepo("doesntexist").metadata_exists())

    def test_load_metadata(self):
        self.assertEqual(True, localrepo().metadata.enabled)
        self.assertEqual("generalpackager", localrepo().name)
        self.assertIsInstance(localrepo().metadata.version, Ver)
        self.assertIsInstance(localrepo().metadata.description, str)
        self.assertIsInstance(localrepo().metadata.topics, list)
        self.assertIsInstance(localrepo().metadata.manifest, list)

        self.assertIsInstance(localrepo().metadata.install_requires, list)
        self.assertIsInstance(localrepo().metadata.extras_require, dict)

    def test_exists(self):
        self.assertEqual(True, localrepo().exists())
        self.assertEqual(True, LocalRepo.repo_exists(localrepo().path))

        self.assertEqual(False, localrepo("doesntexist").exists())

    def test_get_test_paths(self):
        self.assertLess(2, len(list(localrepo().get_test_paths())))
        self.assertIn(localrepo().get_test_path() / "test_local_repo.py", localrepo().get_test_paths())

    def test_get_package_paths(self):
        package_paths = list(localrepo().get_package_paths_gen())
        self.assertIn(localrepo().get_test_path(), package_paths)
        self.assertIn(localrepo().path / localrepo().name, package_paths)
        self.assertNotIn(localrepo().path, package_paths)

    def test_get_changed_files(self):
        local_repo = LocalRepo_Python()
        version = local_repo.metadata.version

        local_repo.bump_version()
        self.assertNotEqual(local_repo.metadata.version, version)
        self.assertIn("metadata.json", local_repo.changed_files())

        local_repo.metadata.version = version
        self.assertEqual(local_repo.metadata.version, version)

    def test_wrong_localrepo_for_target(self):
        local_repo = LocalRepo()
        self.assertRaises(AssertionError, local_repo.bump_version)

    def test_targets(self):
        self.assertEqual(localrepo().metadata.target, LocalRepo.Targets.python)

    def test_format_file_function(self):
        Path("foo").text.write(
            "def camelCase():\n"
            '    """ '
            '        Bad docstrings\n'
            '    """'
        )

        LocalRepo.format_file("foo")

        self.assertEqual(
            'def camel_case():\n'
            '    """ Bad docstrings """',
            Path("foo").text.read())

    def test_format_file_method(self):
        Path("foo").text.write(
            "class FooBar:\n"
            "    def camelCase(self):\n"
            '        """ '
            '            Bad docstrings\n'
            '        """'
        )

        LocalRepo.format_file("foo")

        self.assertEqual(
            'class FooBar:\n'
            '    def camel_case(self):\n'
            '        """ Bad docstrings """',
            Path("foo").text.read())

    def test_get_paths(self):
        self.assertIn("generalpackager", LocalRepo().get_readme_path())
        self.assertIn("generalpackager", LocalRepo().get_org_readme_path())
        self.assertIn("generalpackager", LocalRepo().get_metadata_path())
        self.assertIn("generalpackager", LocalRepo().get_git_exclude_path())
        self.assertIn("generalpackager", LocalRepo().get_setup_path())
        self.assertIn("generalpackager", LocalRepo().get_manifest_path())
        self.assertIn("generalpackager", LocalRepo().get_license_path())
        self.assertIn("generalpackager", LocalRepo().get_workflow_path())
        self.assertIn("generalpackager", LocalRepo().get_test_path())
        self.assertIn("generalpackager", LocalRepo().get_test_template_path())
        self.assertIn("generalpackager", LocalRepo().get_init_path())
        self.assertIn("generalpackager", LocalRepo().get_generate_path())
        self.assertIn("generalpackager", LocalRepo().get_exetarget_path())
        self.assertIn("generalpackager", LocalRepo().get_exeproduct_path())
        self.assertIn("generalpackager", LocalRepo().get_git_ignore_path())
        self.assertIn("generalpackager", LocalRepo().get_npm_ignore_path())
        self.assertIn("generalpackager", LocalRepo().get_index_js_path())
        self.assertIn("generalpackager", LocalRepo().get_test_js_path())
        self.assertIn("generalpackager", LocalRepo().get_package_json_path())

    def test_is_target(self):
        self.assertEqual(True, localrepo().is_python())
        self.assertEqual(False, localrepo().is_exe())
        self.assertEqual(False, localrepo().is_node())
        self.assertEqual(False, localrepo().is_django())

    def test_repo_init(self):
        repo = localrepo(path="hi")
        self.assertIs(False, repo.exists())
        repo.init()
        self.assertIs(True, repo.exists())























