# Use the official Airflow image as the base image
FROM apache/airflow:2.8.1

# Set the environment variable to non-interactive mode to avoid prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install additional Python libraries for MySQL (including pymysql)
RUN pip install --no-cache-dir \
    mysql-connector-python \
    apache-airflow-providers-mysql \
    pymysql \
    && pip install --no-cache-dir apache-airflow[mysql,kafka] \
    && pip install --no-cache-dir pandas \
    && pip install --no-cache-dir sqlalchemy \
    && pip install --no-cache-dir pydantic \
    && pip install apache-airflow-providers-openlineage>=1.8.0


    
# Set the custom entrypoint
ENTRYPOINT ["airflow"]
CMD ["standalone"]