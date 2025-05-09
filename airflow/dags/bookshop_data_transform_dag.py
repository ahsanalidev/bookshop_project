from airflow.providers.docker.operators.docker import DockerOperator
from airflow import DAG
from datetime import datetime
from docker.types import Mount
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()

# Absolute path to the DBT project on the host
DBT_PROJECT_HOST_PATH = str(
  '/home/mr.ahsanali/bookshop_project/dbt_pipeline'
)

dag = DAG(
  'bookshop_data_transform_dag',
  description="Bookshop Data Transform Pipeline",
  start_date=datetime.now(), 
  schedule_interval=None,
  tags=["elt", "dbt", "transform"],
  catchup=False
)

docker_environment_vars = {
  'SNOWFLAKE_ACCOUNT': os.environ.get('SNOWFLAKE_ACCOUNT'),
  'SNOWFLAKE_ROLE': os.environ.get('SNOWFLAKE_ROLE'),
  'SNOWFLAKE_USER': os.environ.get('SNOWFLAKE_USER'),
  'SNOWFLAKE_PASSWORD': os.environ.get('SNOWFLAKE_PASSWORD'),
  'SNOWFLAKE_WAREHOUSE': os.environ.get('SNOWFLAKE_WAREHOUSE'),
  'SNOWFLAKE_DATABASE': os.environ.get('SNOWFLAKE_DATABASE'),
  'SNOWFLAKE_DEFAULT_SCHEMA': os.environ.get('SNOWFLAKE_DEFAULT_SCHEMA'),
  'DBT_LOG_PATH': './logs'
}

docker_common_config = {
  'image': 'bookshop_dbt_image',
  'api_version': 'auto',
  'docker_url': 'unix://var/run/docker.sock',
  'network_mode': 'container:bookshop_dbt',
  'auto_remove': True,       
  'mounts': [Mount(source=DBT_PROJECT_HOST_PATH, target="/dbt_pipeline", type="bind")],
  'working_dir': '/dbt_pipeline',
  'mount_tmp_dir': False,
  'environment': docker_environment_vars,
}

run_raw_stag_task = DockerOperator(
  task_id='raw_stag_run',
  command='sh -c "dbt run --models staging.* --project-dir . --profiles-dir ."',
  **docker_common_config,
  dag=dag
)


run_stag_warehouse_task = DockerOperator(
  task_id='stag_warehouse_run',
  command='sh -c "dbt run --models warehouse.* --project-dir . --profiles-dir ."',
  **docker_common_config,
  dag=dag
)


run_warehouse_marts_task = DockerOperator(
  task_id='warehouse_marts_run',
  command='sh -c "dbt run --models marts.* --project-dir . --profiles-dir ."',
  **docker_common_config,
  dag=dag
)


run_raw_stag_task >> run_stag_warehouse_task >> run_warehouse_marts_task
