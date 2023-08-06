from generalfile.test.test_path import PathTest
from generalpackager.api.localrepo.python.localrepo_python import LocalRepo_Python


class TestLocalRepo_Python(PathTest):
    def test_list_packages_global(self):
        list(LocalRepo_Python().list_packages(local=False))

