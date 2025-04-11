# visualization/Dockerfile
FROM python:3.11-slim

WORKDIR /usr/app/streamlit

# Installation des dépendances
RUN pip install --upgrade pip && \
    pip install streamlit snowflake-connector-python pandas plotly

# Copie de l'application Streamlit
COPY app.py /usr/app/streamlit/

# Exposer le port Streamlit
EXPOSE 8501

# Démarrer l'application Streamlit
CMD ["streamlit", "run", "app.py"]