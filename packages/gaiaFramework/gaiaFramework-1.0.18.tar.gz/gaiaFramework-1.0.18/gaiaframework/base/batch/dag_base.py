"""! @brief DS_Dag base class for the batch dag class.
The DAG (Directed acyclic graph) will trigger the workflow, derived from the workflow template"""

from json import load as json_load
import sys
from typing import List, Any
import os


##
# @file
# @brief Defines dag base class.
class DS_Dag():
    def __init__(self):
        """! DS_Dag initializer.
        Loads config file.
        """

        file_path = sys.modules[self.__class__.__module__].__file__
        curr_path = file_path[:file_path.rfind("batch_files")]

        dag_config = None
        with open(curr_path + '/batch_files/batch_config.json') as batch_cfg_file:
            dag_config = json_load(batch_cfg_file)

        self.environment = dag_config['environment']
        self.bucket_name = dag_config['bucket_name']
        self.project_id = dag_config['project_id']
        self.project_name = dag_config['project_name']
        self.orig_project_name = self.project_name
        self.template_id = dag_config['template_id']
        self.region = dag_config['region']
        self.unique_template_id = dag_config['unique_template_id']
        self.unique_iteration_id = dag_config['unique_iteration_id']

        # For Stg and Prd environments, we want DAG to be created and immediately be active
        self.start_as_paused = False

        env_type = os.environ.get('SPRING_PROFILES_ACTIVE')
        if (not env_type == 'production') and (not env_type == 'staging'):
            self.start_as_paused = True

    def get_basic_dag_code(self) -> str:
        """! Get basic code for dag creation
        Returns:
            A string, containing tailored code for creation of a DAG
        """
        dag_str = '''
        # STEP 1: Libraries needed
        from datetime import timedelta, datetime
        from airflow import models
        from airflow.providers.google.cloud.operators.dataproc import DataprocInstantiateWorkflowTemplateOperator

        region = "''' + self.region + '''"
        zone = region + '-b'
        project_id = "''' + self.project_id + '''"
        template_id = "''' + self.template_id + '''"
        bucket_name = "''' + self.bucket_name + '''"
        project_name = "''' + self.project_name + '''"
        orig_project_name = project_name
        unique_iteration_id = "''' + self.unique_iteration_id + '''"
        unique_template_id = "''' + self.unique_template_id + '''"
        if unique_template_id:
            template_id = template_id + '_' + unique_template_id
            orig_project_name = orig_project_name + '_' + unique_template_id
        if unique_iteration_id:
            project_name = project_name + '/unique_iteration_id_' + unique_iteration_id
        else:
            project_name = project_name + '/main'

        dags_bucket_path = f'gs://{bucket_name}/dags'

        now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        now = now - timedelta(days=1)
        # STEP 3: Set default arguments for the DAG
        default_dag_args = {
            'start_date': now,
            'depends_on_past': False,
            'email_on_failure': False,
            'email_on_retry': False,
            'retries': 1,
            'retry_delay': timedelta(minutes=5)
        }
        # Define a DAG (directed acyclic graph) of tasks.
        # Any task you create within the context manager is automatically added to the
        # DAG object.
        with models.DAG(
            orig_project_name + '_workflow_dag',
            description='DAG for deployment a Dataproc Cluster for ' + project_id,
            # schedule_interval=timedelta(days=1),
            schedule_interval='@daily',
            default_args=default_dag_args,
            is_paused_upon_creation=''' + str(self.start_as_paused) + '''
        ) as dag:

            start_template_job = DataprocInstantiateWorkflowTemplateOperator(
                # The task id of your job
                task_id="dataproc_workflow_dag_python",
                # The template id of your workflow
                template_id=template_id,
                project_id=project_id,
                # The region for the template
                region=region,
                parameters={"START_DATE": "{{ execution_date }}","END_DATE": "{{ next_execution_date }}"}
            )

        '''
        return dag_str

    def create_dag(self):
        """! DS_Dag main function.
        This function is the "entrypoint" for the dag creation.
        """

        raise NotImplementedError

