import subprocess
import os
import sys
from json import dumps as json_dumps
from json import load as json_load

from google.cloud.dataproc_v1 import ClusterControllerClient
from google.cloud.dataproc_v1 import WorkflowTemplatePlacement
from google.cloud.dataproc_v1.types import OrderedJob
from google.cloud.dataproc_v1.types import PySparkJob
from google.cloud.dataproc_v1.services.workflow_template_service.async_client import WorkflowTemplateServiceClient
from google.cloud.dataproc_v1.types.workflow_templates import WorkflowTemplate


##
# @file
# @brief Defines workflow base class.
class DS_Workflow():
    def __init__(self, pip_packages):
        """! DS_Workflow initializer.
        Loads config file and initializes parameters.

            ARGS:
                 pip_packages: A list of pip packages read from requirements file.
        """

        file_path = sys.modules[self.__class__.__module__].__file__
        curr_path = file_path[:file_path.rfind("batch_files")]

        with open(curr_path + '/batch_files/batch_config.json') as batch_cfg_file:
            self.config = json_load(batch_cfg_file)

        self.user_email = ''
        env_type = os.environ.get('SPRING_PROFILES_ACTIVE')
        if (not env_type == 'production') and (not env_type == 'staging'):
            command = 'gcloud config get-value account'
            user_email = subprocess.check_output(command, shell=True).decode(sys.stdout.encoding)
            self.user_email = user_email.split("@")[0]

        if self.user_email:
            self.config['user_email'] = self.user_email

        self.default_args = [json_dumps(self.config), "start_date_placeholder", "end_date_placeholder"]

        self.region = self.config['region']
        self.zone = self.region + '-b'
        self.project_id = self.config['project_id']
        self.template_id = self.config['template_id']
        self.bucket_name = self.config['bucket_name']
        self.project_name = self.config['project_name']
        self.whl_file_name = self.project_name + '.zip'
        self.autoscaling_policy_id = self.project_name + '-auto-scaling-policy'

        self.unique_iteration_id = self.config['unique_iteration_id']
        self.unique_template_id = self.config['unique_template_id']
        if self.unique_template_id:
            self.template_id = self.template_id + '_' + self.unique_template_id

        if self.unique_iteration_id:
            self.folder_path = self.project_name + '/' + self.user_email + '/unique_iteration_id_' + self.unique_iteration_id
        else:
            self.folder_path = self.project_name + '/' + self.user_email + '/main'

        self.bucket_path = f'gs://{self.bucket_name}/{self.folder_path}'
        self.project_path = 'projects/{project_id}/regions/{region}'.format(project_id=self.project_id,
                                                                            region=self.region)

        if self.config['cluster_conf']['managed_cluster']:
            self.config['cluster_conf']['managed_cluster']['config']['gce_cluster_config']['metadata'][
                'PIP_PACKAGES'] = pip_packages

    def check_cluster(self):
        """! DS_Workflow get_cluster.
        Tries to locate existing cluster that should be set up by this point.
        """
        clusterClient = ClusterControllerClient(
            client_options={"api_endpoint": f"{self.region}-dataproc.googleapis.com:443"}
        )
        cluster_name = self.config['cluster_conf']['managed_cluster']['cluster_name']
        try:
            exist_cluster = clusterClient.get_cluster(
                project_id=self.project_id,
                region=self.region,
                cluster_name=cluster_name,
            )
            if exist_cluster:
                del self.config['cluster_conf']['managed_cluster']
                self.config['cluster_conf']['cluster_selector'] = {
                    "cluster_labels": {
                        "goog-dataproc-cluster-name": cluster_name
                    }
                }
        except Exception as e:
            print(f'error getting cluster: {e}')

    def create_template_structure(self) -> (WorkflowTemplate, WorkflowTemplateServiceClient):
        """! DS_Workflow create_template_structure.
        Tries to create a workflow template, containing all available stages.

            Returns:
                WorkflowTemplate() - Created template with basic arguments
                WorkflowTemplateServiceClient() - Service client for template handling
        """
        cluster_config = WorkflowTemplatePlacement(self.config['cluster_conf'])

        client = WorkflowTemplateServiceClient(
            client_options={"api_endpoint": f"{self.region}-dataproc.googleapis.com:443"}
        )
        # if results not exist
        template = WorkflowTemplate()
        template.id = self.template_id
        template.name = self.project_path + '/workflowTemplates/' + template.id
        template.placement = cluster_config
        return client, template

    def create_ordered_job(self, stage_dir) -> OrderedJob:
        """! DS_Workflow create_ordered_job.
        Create an ordered job from a stage directory

            ARGS:
                stage_dir: Stage directory, should hold the main.py file and configuration
                           example: batch_files/stages/stage_write_page_list_to_big_query
            RETURNS:
                An ordered job
        """

        # Assume that the last part of the path is the stage name
        stage_name = stage_dir.rsplit('/', 1)[-1]

        created_stage = OrderedJob()
        pyJob = PySparkJob()
        pyJob.main_python_file_uri = f'{self.bucket_path}/{stage_dir}/main.py'
        pyJob.archive_uris = [f'{self.bucket_path}/dist/{self.whl_file_name}']
        pyJob.python_file_uris = [f'{self.bucket_path}/dist/{self.whl_file_name}']
        pyJob.args = self.default_args + []
        pyJob.jar_file_uris = self.default_jars + []
        created_stage.step_id = f'{self.project_name}-stage_{stage_name}'
        created_stage.pyspark_job = pyJob
        return created_stage

    @staticmethod
    def check_template(serv_client, template):
        """! Check for an existing template. If found, delete it.
            ARGS:
                serv_client: WorkflowTemplateServiceClient()
                template: WorkflowTemplate()
        """

        exist_template = None

        # Getting template if it exists
        try:
            exist_template = serv_client.get_workflow_template(
                name=template.name,
            )
            print(f'template {template.id} retrieved successfully')
        except Exception as e:
            print(f'Error getting template: {e}')

        # Deleting template if it exists
        if exist_template:
            try:
                serv_client.delete_workflow_template(
                    name=template.name,
                )
                print(f'template {template.id} deleted successfully')
            except Exception as e:
                print(f'Error deleting template: {e}')

    def create_template(self, serv_client, template):
        """! Create the complete template on the remote location.
            ARGS:
                serv_client: WorkflowTemplateServiceClient()
                template: WorkflowTemplate()
        """
        try:
            result = serv_client.create_workflow_template(
                parent=self.project_path,
                template=template
            )
            print(f'template {template.id} created successfully')
        except Exception as e:
            print(f'Error creating template: {e}')

    @staticmethod
    def instantiate_template(serv_client, template):
        """! Instantiate the template into a working workflow, overriding DAG
        Do this only on dev mode
            ARGS:
                serv_client: WorkflowTemplateServiceClient()
                template: WorkflowTemplate()
        """
        try:
            serv_client.instantiate_workflow_template(
                name=template.name,
                parameters={"START_DATE": '2022-02-23T00:00:00+00:00', "END_DATE": '2022-02-24T00:00:00+00:00'}
            )
            print(f'template {template.id} instantiated successfully')
        except Exception as e:
            print(f'Error instantiating template: {e}')

    def create_workflow_template(self):
        """! Create the workflow template, along with all relevant stages
        """
        raise NotImplementedError
