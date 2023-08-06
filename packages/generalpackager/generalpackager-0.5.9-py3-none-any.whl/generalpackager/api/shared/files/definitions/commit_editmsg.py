
from generalpackager.api.shared.files.file import File


class CommitEditmsgFile(File):
    _relative_path = ".git/COMMIT_EDITMSG"
    is_file = True
    aesthetic = True


