from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta, datetime
import os
import pandas as pd
from sqlalchemy import create_engine
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv
import logging

# Load env vars
load_dotenv()

# Basic logging
logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)

# Tables to sync
TABLES = ["category", "books", "customers", "factures", "ventes"]

# Get env variable safely
def get_env(key, default=None):
    val = os.environ.get(key, default)
    if val is None:
        raise ValueError(f"Missing env variable: {key}")
    return val

# PostgreSQL connection
def get_postgres_engine():
    user = get_env("POSTGRES_USER")
    password = get_env("POSTGRES_PASSWORD")
    host = get_env("POSTGRES_HOST", "postgres")
    db = get_env("POSTGRES_DB", "bookshop")
    return create_engine(f"postgresql://{user}:{password}@{host}/{db}")

# Snowflake connection
def get_snowflake_conn():
    return snowflake.connector.connect(
        user=get_env("SNOWFLAKE_USER"),
        password=get_env("SNOWFLAKE_PASSWORD"),
        account=get_env("SNOWFLAKE_ACCOUNT"),
        warehouse=get_env("SNOWFLAKE_WAREHOUSE"),
        database=get_env("SNOWFLAKE_DATABASE"),
        schema="RAW"
    )

# Extract data from Postgres
def extract_table(table_name, **context):
    engine = get_postgres_engine()

    # Get last run time from XCom (if exists)
    last_ts = context['ti'].xcom_pull(key=f"{table_name}_last_run", task_ids=None)
    if last_ts:
        query = f"SELECT * FROM {table_name} WHERE created_at > '{last_ts}'"
    else:
        query = f"SELECT * FROM {table_name}"

    df = pd.read_sql(query, engine)
    context['ti'].xcom_push(key=f"{table_name}_df", value=df.to_json())  # Pass via XCom
    if 'created_at' in df.columns and not df.empty:
        latest = df['created_at'].max()
        context['ti'].xcom_push(key=f"{table_name}_last_run", value=str(latest))

# Load data into Snowflake
def load_table(table_name, **context):
    df_json = context['ti'].xcom_pull(key=f"{table_name}_df", task_ids=None)
    if not df_json:
        logger.info(f"No data to load for {table_name}")
        return

    df = pd.read_json(df_json)
    if 'created_at' in df.columns:
        df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M:%S.%f')

    conn = get_snowflake_conn()
    success, nchunks, nrows, _ = write_pandas(conn, df, table_name, auto_create_table=True)
    if success:
        logger.info(f"Loaded {nrows} rows into {table_name} in Snowflake.")
    else:
        logger.error(f"Failed to load {table_name}.")

# DAG definition
default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="bookshop_data_ingest_dag",
    description="Bookshop Data Ingestion Pipeline",
    default_args=default_args,
    start_date=datetime.now(), 
    schedule_interval=None,
    catchup=False,
    tags=["elt", "postgres", "snowflake"],
) as dag:

    for table in TABLES:
        extract = PythonOperator(
            task_id=f"extract_{table}",
            python_callable=extract_table,
            op_kwargs={"table_name": table},
        )

        load = PythonOperator(
            task_id=f"load_{table}",
            python_callable=load_table,
            op_kwargs={"table_name": table},
        )

        extract >> load