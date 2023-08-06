from generalfile import Path
from generallibrary import Terminal, Log
from generalpackager.api.shared.decos import deco_path_as_working_dir


class _LocalRepo_Git:
    # https://github.com/actions/checkout/issues/13#issuecomment-724415212
    RUNNER_NAME = "github-actions[bot]"
    RUNNER_EMAIL = "<41898282+github-actions[bot]@users.noreply.github.com>"

    def commit_message(self):
        """ :param generalpackager.LocalRepo self: """
        return self.commit_editmsg_file.path.text.read()

    @deco_path_as_working_dir
    def init(self):
        """ :param generalpackager.LocalRepo self: """
        Terminal("git", "init")

    @staticmethod
    def git_missing_credentials(terminal):
        return terminal.fail and "Please tell me who you are." in terminal.string_result

    @staticmethod
    def git_nothing_to_commit(terminal):
        return terminal.fail and "Your branch is up to date with" in terminal.string_result

    def git_config(self):
        """ :param generalpackager.LocalRepo self: """
        Terminal("git", "config", "--global", "user.name", self.RUNNER_NAME)
        Terminal("git", "config", "--global", "user.email", self.RUNNER_EMAIL)

    @deco_path_as_working_dir
    def commit(self, message=None, _recurse=True):
        """ Tries to commit. If credentials are missing then it sets them and tries once more.

            :param generalpackager.LocalRepo self: """
        Log(__name__).debug(f"Commiting for {self} in working dir {Path.get_working_dir()}")
        Terminal("git", "add", ".")
        terminal = Terminal("git", "commit", "-a", "-m", message or "No commit message", error=False)
        if terminal.success:
            Log(__name__).debug(f"Commit success")
            return True
        elif self.git_nothing_to_commit(terminal=terminal):
            Log(__name__).debug(f"Nothing to commit")
            return False
        elif _recurse and self.git_missing_credentials(terminal=terminal):
            Log(__name__).debug(f"Missing credentials for commit, trying again")
            self.git_config()
            return self.commit(message=message, _recurse=False)
        else:
            raise terminal.error_result

    @deco_path_as_working_dir
    def push(self, url, tag=None):
        if tag:
            Terminal("git", "tag", tag)
            tag = ("tag", tag)
        else:
            tag = ()

        Terminal("git", "remote", "add", "origin", url, error=False)
        Terminal("git", "push", "-u", "origin", "HEAD", *tag)

    @deco_path_as_working_dir
    def clone(self, url):
        Terminal("git", "clone", url)

    @deco_path_as_working_dir
    def commit_sha(self):
        """ Defaults to 'master' if missing.

            :param generalpackager.LocalRepo self: """
        return Terminal("git", "rev-parse", "--verify", "HEAD", default="master").string_result

    def commit_sha_short(self):
        """ Defaults to 'master' if missing.

            :param generalpackager.LocalRepo self: """
        return self.commit_sha()[0:8]

    @deco_path_as_working_dir
    def changed_files(self):
        """ :param generalpackager.LocalRepo self: """
        ls_files = Terminal("git", "ls-files", "--modified").string_result
        return [Path(file) for file in ls_files.splitlines()]

    def get_all_versions(self):
        """ :param generalpackager.LocalRepo self: """
        with self.path.as_working_dir():
            terminal = Terminal("git", "tag", "-l", "--sort=-v:refname")
        return terminal.string_result.splitlines()





























