#!/bin/bash

# Run the data_seeder.py script with different types
docker exec -it pipelines-pipelines-1 rm -rf airflow/dags/
docker exec -it pipelines-pipelines-1 cp -r pipelines/ airflow/dags/

echo "All Dags are currently updated!"