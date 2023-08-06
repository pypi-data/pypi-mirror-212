from typing import Union

from generalpackager.api.localrepo.base.localrepo import LocalRepo
from generalpackager.api.localrepo.node.localrepo_node import LocalRepo_Node
from generalpackager.api.localrepo.python.localrepo_python import LocalRepo_Python


def localrepo(name=None, path=None, target=None) -> Union[LocalRepo_Python, LocalRepo_Node]:
    repo = LocalRepo(name=name, path=path)
    if target is None:
        target = repo.metadata.target
    return repo.targetted(target=target)
