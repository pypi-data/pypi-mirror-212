from generalpackager.api.shared.target import Targets
from generallibrary import CodeLine, comma_and_and, plur_sing

from generalpackager.api.shared.files.file import File


class WorkflowFile(File):
    target = File.targets.python
    _relative_path = ".github/workflows/workflow.yml"
    aesthetic = False

    ON_MASTER = True
    INCLUDE_ENVS = True

    def codeline(self):
        workflow = CodeLine()
        workflow.indent_str = " " * 2
        return workflow

    def _generate(self):
        workflow = self.codeline()
        workflow.add_node(self._get_name())
        workflow.add_node(self._get_triggers())
        workflow.add_node(self._get_defaults())

        jobs = workflow.add_node("jobs:")
        jobs.add_node(self._get_unittest_job())
        jobs.add_node(self._get_sync_job())

        return workflow

    _commit_msg = "github.event.head_commit.message"
    # _action_checkout = "actions/checkout@v2"
    _action_setup_python = "actions/setup-python@v4"
    _action_setup_ssh = "webfactory/ssh-agent@v0.7.0"
    _matrix_os = "matrix.os"
    _matrix_python_version = "matrix.python-version"
    _branch = "github.ref_name"
    _owner = "github.repository_owner"  # The repository owner's username. For example, octocat.
    _repository = "github.repository"  # The owner and repository name. For example, octocat/Hello-World.

    PIP_NECESSARY_PACKAGES = (
        "setuptools",
        "wheel",
        "twine",
    )
    REPOS_PATH = "repos"
    MASTER_BRANCHES = (
        "master",
        "main",
    )


    def _step_install_necessities(self):
        run = CodeLine("run: |")
        run.add_node("python -m pip install --upgrade pip")
        run.add_node(f"pip install --upgrade {' '.join(self.PIP_NECESSARY_PACKAGES)}")
        return self._get_step(f"Install necessities", run)

    @staticmethod
    def _var(string):
        return f"${{{{ {string} }}}}"

    @staticmethod
    def _commit_msg_if(*literals, **conditions):
        checks = [f"contains(github.event.head_commit.message, '[CI {key}]') == {str(value).lower()}" for key, value in conditions.items()]
        checks += list(literals)
        return f"if: {' && '.join(checks)}"

    def _get_name(self):
        name = CodeLine(f"name: {self.name}")
        return name

    def _get_triggers(self):
        on_branch_key = "branches" if self.ON_MASTER else "branches-ignore"

        on = CodeLine("on:")
        branches = on.add_node("push:").add_node(f"{on_branch_key}:")
        for branch in self.MASTER_BRANCHES:
            branches.add_node(f"- {branch}")
        return on

    def _get_defaults(self):
        defaults = CodeLine("defaults:")
        defaults.add_node("run:").add_node("working-directory: ../../main")
        return defaults

    def _get_step(self, name, *codelines):
        step = CodeLine(f"- name: {name}")
        for codeline in codelines:
            if codeline:
                step.add_node(codeline)
        return step

    def _step_make_workdir(self):
        step = CodeLine("- name: Create folder")
        step.add_node("working-directory: ../../")
        step.add_node("run: mkdir main")
        return step

    def _step_setup_ssh(self):
        with_ = CodeLine("with:")
        with_.add_node("ssh-private-key: ${{ secrets.GIT_SSH }}")
        return self._get_step(f"Set up Git SSH", f"uses: {self._action_setup_ssh}", with_)

    def _step_setup_python(self, version):
        with_ = CodeLine("with:")
        with_.add_node(f"python-version: '{version}'")
        return self._get_step(f"Set up python version {version}", f"uses: {self._action_setup_python}", with_)

    def _step_install_package_pip(self, *packagers):
        """ Supply Packagers to create pip install steps for. """
        names = [p.name for p in packagers]
        run = CodeLine(f"run: pip install {' '.join(names)}")
        return self._get_step(f"Install pip packages {comma_and_and(*names, period=False)}", run)

    def _packagers(self, include_summary_packagers=None, target=None):
        packagers = self.packager.get_ordered_packagers(include_private=False, include_summary_packagers=include_summary_packagers)
        if not self.ON_MASTER:
            dependencies = self.packager.get_parents(-1, include_self=True)
            packagers = [packager for packager in packagers if packager in dependencies]

        if target is not None:
            packagers = [packager for packager in packagers if packager.target == target]
        return packagers

    @staticmethod
    def _chain_bash(*commands, new_line=True):
        delimiter = " || \\\n" if new_line else " || "
        return delimiter.join(commands)

    def _step_clone_repos(self, include_summary_packagers):
        """ Supply Packagers to create git install steps for. """
        packagers = self._packagers(include_summary_packagers=include_summary_packagers)

        step = CodeLine(f"- name: Clone {plur_sing(len(packagers), 'repo')}")
        run = step.add_node(f"run: |")
        run.add_node(f"mkdir {self.REPOS_PATH}")
        run.add_node(f"cd {self.REPOS_PATH}")


        owner = self._var(self._owner)
        branch = self._var(self._branch)

        for packager in packagers:
            if self.ON_MASTER:
                run.add_node(packager.github.git_clone_command(ssh=self.ON_MASTER))
            else:
                clone_commands = (
                    packager.github.git_clone_command(ssh=self.ON_MASTER, owner=owner, branch=branch),
                    packager.github.git_clone_command(ssh=self.ON_MASTER, owner=owner),
                    packager.github.git_clone_command(ssh=self.ON_MASTER, branch=branch),
                    packager.github.git_clone_command(ssh=self.ON_MASTER),
                )
                # new_line not working on windows
                # https://stackoverflow.com/questions/59954185/github-action-split-long-command-into-multiple-lines
                run.add_node(self._chain_bash(*clone_commands, new_line=False))

        return step

    def _step_install_repos(self):
        """ Supply Packagers to create git install steps for. """
        packagers = self._packagers(target=Targets.python)

        step = CodeLine(f"- name: Install {plur_sing(len(packagers), 'repo')}")
        run = step.add_node(f"run: |")
        run.add_node(f"cd {self.REPOS_PATH}")

        for packager in packagers:
            if packager.target == Targets.python:
                run.add_node(f"pip install -e {packager.name}[full]")
        return step

    def _get_env(self):
        env = CodeLine("env:")
        for packager in self.packager.get_all():
            for env_var in packager.localmodule.get_env_vars(error=False):
                if env_var.actions_name and env_var.name not in str(env):
                    env.add_node(f"{env_var.name}: {env_var.actions_name}")
        if not env.get_children():
            return None
        return env

    def _steps_setup(self, python_version, include_summary_packagers):
        steps = CodeLine("steps:")
        steps.add_node(self._step_make_workdir())
        if self.ON_MASTER:
            steps.add_node(self._step_setup_ssh())
        steps.add_node(self._step_setup_python(version=python_version))
        steps.add_node(self._step_install_necessities())
        steps.add_node(self._step_clone_repos(include_summary_packagers=include_summary_packagers))
        steps.add_node(self._step_install_repos())
        return steps

    def _get_strategy(self):
        strategy = CodeLine("strategy:")
        matrix = strategy.add_node("matrix:")
        matrix.add_node(f"python-version: {list(self.packager.python)}")
        matrix.add_node(f"os: {[f'{os}-latest' for os in self.packager.os]}".replace("'", ""))
        return strategy

    def _get_unittest_job(self):
        job = CodeLine("unittest:" if self.ON_MASTER else "dev_unittest:")
        job.add_node(self._commit_msg_if(SKIP=False, AUTO=False))
        job.add_node(f"runs-on: {self._var(self._matrix_os)}")
        job.add_node(self._get_strategy())

        python_version = self._var(self._matrix_python_version)
        steps = job.add_node(self._steps_setup(python_version=python_version, include_summary_packagers=False))
        if self.ON_MASTER:
            steps.add_node(self._step_run_packager_method("workflow_unittest"))
        else:
            steps.add_node(self._step_run_simple_unittest())
        return job

    def _get_sync_job(self):
        job = CodeLine("sync:")
        job.add_node("needs: unittest")
        job.add_node(f"runs-on: ubuntu-latest")
        steps = job.add_node(self._steps_setup(python_version=self.packager.python[-1], include_summary_packagers=True))
        steps.add_node(self._step_run_packager_method("workflow_sync"))
        return job

    def _step_run_packager_method(self, method):
        step = self._get_step(f"Run Packager method '{method}'")

        run = step.add_node(f'run: |')
        run.add_node(f"cd {self.REPOS_PATH}")
        run.add_node(f'python -c "from generalpackager import Packager; Packager().{method}()"')

        if self.INCLUDE_ENVS:
            step.add_node(self._get_env())
        return step

    def _step_run_simple_unittest(self):
        step = self._get_step(f"Run unittests")

        run = step.add_node(f'run: |')
        run.add_node(f"cd {self.REPOS_PATH}/{self.packager.name}/{self.packager.name}/test")

        run.add_node(f'python -m unittest discover -v')
        return step



















