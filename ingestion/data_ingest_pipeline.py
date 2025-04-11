import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd
import snowflake.connector
import psycopg2
from snowflake.connector.pandas_tools import write_pandas
from time import sleep

# Load the .env file
load_dotenv()

# Configure logging
logger = logging.getLogger('__main__')
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logging.getLogger('snowflake.connector').setLevel(logging.ERROR)

# Utility function to fetch environment variables
def get_env_variable(key, default=None):
    value = os.environ.get(key, default)
    if value is None:
        logger.error(f"Environment variable {key} is missing!")
    return value

# Verify environment variables before proceeding
def verify_env_variables():
    required_vars = ["POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DB"]
    for var in required_vars:
        if get_env_variable(var) is None:
            logger.error(f"Missing required environment variable: {var}")
            return False
    return True

# Wait for PostgreSQL to be ready
def wait_for_postgres(max_retries=30, delay=2):
    retries = 0
    while retries < max_retries:
        try:
            conn = psycopg2.connect(
                host=get_env_variable("POSTGRES_HOST", "localhost"),
                port=get_env_variable("POSTGRES_PORT", 5432),
                database=get_env_variable("POSTGRES_DB", "bookshop"),
                user=get_env_variable("POSTGRES_USER"),
                password=get_env_variable("POSTGRES_PASSWORD"),
            )
            conn.close()
            logger.info("PostgreSQL is ready")
            return True
        except psycopg2.OperationalError:
            retries += 1
            logger.warning(f"Waiting for PostgreSQL... ({retries}/{max_retries})")
            sleep(delay)
    return False

# Get a PostgreSQL connection using SQLAlchemy
def get_postgres_connection():
    # Fetch environment variables with defaults
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    host = os.getenv('POSTGRES_HOST', 'localhost')  # Default to localhost
    db = os.getenv('POSTGRES_DB', 'bookshop')  # Default to bookshop
    
    # Check if the required variables are provided
    if not user or not password:
        raise ValueError("Missing required environment variables: POSTGRES_USER and POSTGRES_PASSWORD")
    
    # Construct the connection string
    conn_str = f"postgresql://{user}:{password}@{host}/{db}"
    
    # Return the SQLAlchemy engine
    return create_engine(conn_str)

# Connect to Snowflake
def get_snowflake_connection():
    return {
        'user': get_env_variable("SNOWFLAKE_USER"),
        'password': get_env_variable("SNOWFLAKE_PASSWORD"),
        'account': get_env_variable("SNOWFLAKE_ACCOUNT"),
        'warehouse': get_env_variable("SNOWFLAKE_WAREHOUSE"),
        'database': get_env_variable("SNOWFLAKE_DATABASE"),
        'schema': "RAW",
    }

# Extract data from PostgreSQL table using SQLAlchemy
def extract_table(table_name, engine):
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql(query, engine)

# Load data into Snowflake
def load_to_snowflake(df, table_name, sf_params):
    with snowflake.connector.connect(**sf_params) as conn:
        success, nchunks, nrows, _ = write_pandas(conn, df, table_name, auto_create_table=True)
    return success, nrows

def convert_timestamp_column(df):
    if 'created_at' in df.columns:
        df['created_at'] = df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S.%f')
    return df

# Main ingestion function
def ingest_data():
    if not verify_env_variables():
        logger.error("Exiting due to missing environment variables.")
        return

    tables = ["category", "books", "customers", "factures", "ventes"]

    if not wait_for_postgres():
        logger.error("Unable to connect to PostgreSQL after several attempts")
        return

    try:
        # Connect to PostgreSQL and Snowflake
        pg_conn = get_postgres_connection()  # Using SQLAlchemy to create the connection
        snow_conn = get_snowflake_connection()

        # Process each table
        for table in tables:
            logger.info(f"Processing table {table}...")

            # Extract data from PostgreSQL
            df = extract_table(table, pg_conn)

            if df.empty:
                logger.warning(f"No data found in table {table}")
                continue

            logger.info(f"Data extracted from {table}: {len(df)} rows")

            # Convert timestamps in the DataFrame (if necessary)
            df = convert_timestamp_column(df)

            # Load data into Snowflake
            success, nrows = load_to_snowflake(df, table, snow_conn)
            if success:
                logger.info(f"Data loaded into Snowflake {table}: {nrows} rows")
            else:
                logger.error(f"Error loading data into Snowflake {table}")

            sleep(1)  # Prevent overwhelming the system

        # Close connections
        pg_conn.dispose()  # Manually dispose of the SQLAlchemy connection
        logger.info("Data ingestion completed successfully")
    
    except Exception as e:
        logger.error(f"Error during ingestion: {e}")

if __name__ == "__main__":
    try:
        ingest_data()
    except KeyboardInterrupt:
        logger.info("Data ingestion process was interrupted by the user.")
        exit(0)