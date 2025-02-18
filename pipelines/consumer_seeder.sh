#!/bin/bash

# Run the data_seeder.py script with different types
docker exec -d pipelines-pipelines-1 python3 pipelines/cow/step1_extraction_cow.py
docker exec -d pipelines-pipelines-1 python3 pipelines/measurement/step1_extraction_measurement.py
docker exec -d pipelines-pipelines-1 python3 pipelines/sensor/step1_extraction_sensor.py

echo "All Consumers are currently running!"