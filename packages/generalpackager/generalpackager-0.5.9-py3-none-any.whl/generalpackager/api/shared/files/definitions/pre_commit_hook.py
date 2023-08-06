from generalpackager.api.shared.files.file import File


class PreCommitHookFile(File):
    _relative_path = ".git/hooks/pre-commit"
    aesthetic = True
    remove = True

