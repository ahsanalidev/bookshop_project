# dbt/Dockerfile
FROM python:3.11-slim

WORKDIR /usr/app/dbt

# Installation des dépendances
RUN pip install dbt-core dbt-snowflake

# Create alias for dbt-set-profile
RUN echo "alias dbt-set-profile='unset DBT_PROFILES_DIR && export DBT_PROFILES_DIR=\$PWD'" >> .bashrc

CMD ["dbt", "--version"]