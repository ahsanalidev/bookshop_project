# Bookshop Data Pipeline Project

A modern data pipeline for book sales analysis, implementing a complete ELT (Extract, Load, Transform) process using Snowflake, DBT, Airflow, and Streamlit.

## Project Overview

This project implements a complete data pipeline for analyzing book sales data. It follows a modern ELT approach where data is first loaded into Snowflake and then transformed using DBT. The pipeline is orchestrated by Airflow and visualized through a Streamlit dashboard.

### Architecture Components

- **Data Source**: PostgreSQL database with sample book sales data
- **Data Warehouse**: Snowflake for data storage and transformation
- **Transformation**: DBT for data modeling and transformation
- **Orchestration**: Airflow for workflow management
- **Visualization**: Streamlit for interactive dashboards

## Prerequisites

- Docker and Docker Compose
- Snowflake account
- Python 3.8+
- Git

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/username/bookshop_project.git
cd bookshop_project
```

### 2. Snowflake Configuration

1. Create a Snowflake account if you don't have one
2. Create a new database and warehouse in Snowflake
3. Note down your Snowflake credentials:
   - Account name
   - Username
   - Password
   - Warehouse name
   - Database name
   - Role

### 3. Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# PostgreSQL Configuration
POSTGRES_DB=bookshop
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password

# Snowflake Configuration
SNOWFLAKE_ACCOUNT=your_snowflake_account
SNOWFLAKE_USER=BOOKSHOP_USER
SNOWFLAKE_ROLE=BOOKSHOP_ROLE
SNOWFLAKE_PASSWORD=your_snowflake_password
SNOWFLAKE_WAREHOUSE=BOOKSHOP_WH
SNOWFLAKE_DATABASE=BOOKSHOP
SNOWFLAKE_DEFAULT_SCHEMA=RAW

# Airflow Configuration
AIRFLOW_UID=1000
AIRFLOW_GID=0
```

Note: The Snowflake configuration uses predefined values for USER, ROLE, WAREHOUSE, and DATABASE as specified in the project. You only need to provide your specific account and password information.

### 4. Build and Start Docker Containers

```bash
# Build and start all services
docker-compose up --build
```

This will start the following services:
- PostgreSQL database
- Airflow webserver (port 8080)
- Airflow scheduler
- DBT container (witness container for image building)
- Streamlit application (port 8501)

**Note about DBT Container**: The DBT container started by docker-compose serves only as a witness container for building the DBT image. The actual DBT transformations are executed using the `bookshop_dbt_image` through the DockerOperator in the Airflow DAG. This image is used to run DBT commands in isolated containers for each transformation task.

### 5. Initialize Snowflake Structure

1. Access the Airflow web interface at http://localhost:8080
   - Default credentials: airflow/airflow
2. Navigate to the DAGs section
3. Find and enable the `init_snowflake` DAG
4. Trigger the DAG manually
5. Monitor the execution in the Airflow UI

### 6. Run Data Ingestion

1. In the Airflow UI, find and enable the `ingestion` DAG
2. Trigger the DAG manually
3. Monitor the execution to ensure data is successfully loaded into Snowflake RAW schema

### 7. Run Data Transformation

1. In the Airflow UI, find and enable the `bookshop_data_transform_dag` DAG
2. Trigger the DAG manually
3. Monitor the execution as data flows through the transformation layers:
   - RAW → STAGGING (executed in isolated DBT container)
   - STAGGING → WAREHOUSE (executed in isolated DBT container)
   - WAREHOUSE → MARTS (executed in isolated DBT container)

Each transformation step runs in its own container using the `bookshop_dbt_image`, ensuring isolation and reproducibility of the transformations.

### 8. Access the Visualization Dashboard

1. Once all transformations are complete, access the Streamlit dashboard at http://localhost:8501
2. The dashboard will display:
   - Key performance indicators
   - Sales trends over time
   - Customer segmentation
   - Product analysis

## Project Structure

```
bookshop_project/
├── airflow/                # Airflow configuration and DAGs
│   ├── dags/               # Workflow definitions
│   ├── logs/               # Execution logs
│   └── plugins/            # Custom plugins
├── data/                   # Data and initialization scripts
│   ├── init/               # Table creation and data population scripts
│   └── raw/                # Source database schemas
├── dbt_pipeline/           # DBT transformation models
│   ├── models/             # SQL transformation definitions
│   └── dbt_project.yml     # DBT project configuration
├── ingestion/              # Data ingestion scripts
├── logs/                   # General execution logs
├── snowflake_config/       # Snowflake initialization scripts
├── visualization/          # Streamlit visualization application
├── docker-compose.yml      # Container orchestration
├── requirements.txt        # Python dependencies
└── .env                    # Environment variables
```

## Troubleshooting

### Common Issues

1. **Airflow Connection Issues**
   - Check if all services are running: `docker-compose ps`
   - Verify Airflow logs: `docker-compose logs airflow-webserver`

2. **Snowflake Connection Problems**
   - Verify credentials in `.env` file
   - Check Snowflake account status and permissions
   - Ensure warehouse is running

3. **DBT Transformation Failures**
   - Check DBT logs in Airflow
   - Verify Snowflake table permissions
   - Ensure data exists in source tables

### Logs

- Airflow logs: `docker-compose logs airflow-webserver`
- DBT logs: `docker-compose logs dbt`
- Streamlit logs: `docker-compose logs streamlit`

## Maintenance

### Updating Dependencies

```bash
# Update Python dependencies
pip install -r requirements.txt

# Rebuild containers
docker-compose up --build
```

### Stopping the Project

```bash
# Stop all containers
docker-compose down

# Stop and remove volumes (if needed)
docker-compose down -v
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 