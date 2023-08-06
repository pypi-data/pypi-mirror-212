from generallibrary import Terminal


class _PackagerGitHub:
    """ Sync metadata. """
    def sync_github_metadata(self):
        """ Sync GitHub with local metadata.

            :param generalpackager.Packager self: """
        assert self.github.set_website(self.pypi.url).ok
        assert self.github.set_description(self.localrepo.metadata.description).ok
        assert self.github.set_topics(*self.get_topics()).ok

    def push(self, version=None):
        """ :param generalpackager.Packager self: """
        if version is True:
            version = self.localrepo.metadata.version

        version = self.GitHub.format_version(version=version)
        self.localrepo.push(url=self.github.ssh_url, tag=version)

    def commit_and_push(self, message=None, version=None):
        """ Commit and push this local repo to GitHub.
            Return short sha1 of pushed commit.

            :param generalpackager.Packager self: """
        # Bad hard-coded quick fix
        if "Sync" in message and version:
            message = message.replace("Sync", "Publish")

        if self.localrepo.commit(message=message):
            self.push(version=version)

    def create_github_repo(self):
        """ :param generalpackager.Packager self: """
        Terminal("gh", "repo", "create", f"{self.github.owner}/{self.name}")

    def create_master_branch(self):
        """ :param generalpackager.Packager self: """
        # repo = self.localrepo.repo
        # Create remote somehow first
        # print(repo.remote().push("head"))

    # Todo: Setup env vars for project.






