import os
from typing import List
from google.cloud.dataproc_v1.types.workflow_templates import WorkflowTemplate, TemplateParameter
from google.cloud.dataproc_v1.types import OrderedJob, PySparkJob
from gaiaframework.base.batch.workflow_base import DS_Workflow


class Workflow(DS_Workflow):

    def __init__(self):
        """! Loads config file and initializes parameters.
        """
        self.default_jars = ['gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar']
        main_project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

        self.pip_packages = ''
        with open(main_project_path + '/requirements_docker.txt') as req_file:
            required_pkg = req_file.read().splitlines()
            required_pkg = [x for x in required_pkg if "#" not in x]
            self.pip_packages = ' '.join(required_pkg)

        super().__init__(self.pip_packages)

    def create_job(self, stage_name, prerequisite_list=None) -> OrderedJob():
        """! create a job from a given stage

            ARGS:
                stage_name: Name of the stage to create
                prerequisite_list: list of stage id's that are mandatory to run before current stage

            Returns:
                An Ordered Job, to be inserted into the workflow template
        """
        stage_dir = f'batch_files/stages/{stage_name}'

        stage_job = self.create_ordered_job(stage_dir)

        if prerequisite_list is not None:
            stage_job.prerequisite_step_ids = prerequisite_list

        return stage_job

    def create_stages(self) -> List[OrderedJob]:
        """! create the stages for the workflow stages
            Returns:
                A List of Ordered Jobs, to be inserted into the workflow template
        """
        # stage get_data
        stage_get_data_job = self.create_job("get_data")

        # stage run_pipeline
        prerequisite_list = [self.project_name + '-stage_get_data']
        stage_run_pipeline_job = self.create_job("run_pipeline", prerequisite_list)

        # stage set_data
        prerequisite_list = [self.project_name + '-stage_run_pipeline']
        stage_set_data_job = self.create_job("set_data", prerequisite_list)

        return [stage_get_data_job, stage_run_pipeline_job, stage_set_data_job]

    def finalize_jobs(self, workflow_template):
        """! create the stages for the workflow stages
            ARGS:
                workflow_template: Workflow templates. Includes jobs that we wish to modify
        """

        # Set start and end dates from Airflow composer
        workflow_template.parameters = []
        for job in workflow_template.jobs:
            start_date_param = TemplateParameter()
            start_date_param.description = "start date from airflow composer"
            start_date_param.name = "START_DATE"
            start_date_param.fields = [
                "jobs['" + job.step_id + "'].pysparkJob.args[1]"
            ]
            end_date_param = TemplateParameter()
            end_date_param.description = "end date from airflow composer"
            end_date_param.name = "END_DATE"
            end_date_param.fields = [
                "jobs['" + job.step_id + "'].pysparkJob.args[2]"
            ]
            workflow_template.parameters.append(start_date_param)
            workflow_template.parameters.append(end_date_param)

        # Make sure to change jobs according to specific configuration
        if self.config['specific_jobs_to_run'] and len(self.config['specific_jobs_to_run']):
            specific_jobs_to_run = []
            for job in workflow_template.jobs:
                if job.step_id in self.config['specific_jobs_to_run']:
                    specific_jobs_to_run.append(job)
                    if len(job.prerequisite_step_ids) and not all(
                            elem in specific_jobs_to_run for elem in job.prerequisite_step_ids):
                        raise Exception("job depends on another job not in specific_jobs_to_run list")
            workflow_template.jobs = specific_jobs_to_run

    def create_workflow_template(self):
        """! Create the workflow template, along with all relevant stages
        """
        service_client = None
        template = None

        # Make sure that a cluster exists
        self.check_cluster()

        # Define template structure
        service_client, template = self.create_template_structure()
        template.jobs = self.create_stages()
        self.finalize_jobs(template)
        # print(template)
        # print(f"project_path: {self.project_path}")

        # Make sure that the template does not exist
        self.check_template(service_client, template)

        # Create template
        self.create_template(service_client, template)

        # When working on "dev" mode, instantiate the template with this function
        self.instantiate_template(service_client, template)


if __name__ == "__main__":
    """! Triggers the creation of the workflow template, starting from
    basic configuration, defining and creating jobs from the existing stages, 
    and up to creating and instantiating the workflow, if needed.
    """

    workflow = Workflow()
    workflow.create_workflow_template()
