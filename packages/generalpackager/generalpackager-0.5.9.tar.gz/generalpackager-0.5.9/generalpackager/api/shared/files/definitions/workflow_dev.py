from generalpackager.api.shared.files.definitions.workflow import WorkflowFile


class WorkflowDevFile(WorkflowFile):
    _relative_path = ".github/workflows/workflow_dev.yml"

    ON_MASTER = False
    INCLUDE_ENVS = False

    def _generate(self):
        workflow = self.codeline()
        workflow.add_node(self._get_name())
        workflow.add_node(self._get_triggers())
        workflow.add_node(self._get_defaults())

        jobs = workflow.add_node("jobs:")
        jobs.add_node(self._get_unittest_job())

        return workflow