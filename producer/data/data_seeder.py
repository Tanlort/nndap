import os
import polars as pl
import requests
from typing import Dict, Any
import json
import argparse
import logging

def setup_logger(log_filename: str) -> logging.Logger:
    """Set up a logger that writes to a specific file"""
    logger = logging.getLogger(log_filename)
    handler = logging.FileHandler(log_filename)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

class DataSeeder:
    def __init__(self, api_base_url: str = "http://localhost:5001"):
        self.api_base_url = api_base_url

    def send_request(self, session: requests.Session, endpoint: str, data: Dict[str, Any], logger: logging.Logger) -> None:
        """Send a single request"""
        try:
            response = session.post(f"{self.api_base_url}/{endpoint}", json=data)
            result = response.json()

            # Serialize both data and result to JSON strings
            data_json = json.dumps(data, separators=(',', ':'))  
            result_json = json.dumps(result, separators=(',', ':'))  
            
            
            log_message = (
                f"endpoint={endpoint} "
                f"status_code={response.status_code} "
                f"request_data={data_json} "
                f"response_data={result_json}"
            )
            logger.info(log_message)

            return response.status_code
        
        except Exception as e:
            logger.error(f"Error sending {data_json}: {str(e)}")
            return None

    def seed_data(self, parquet_path: str, endpoint: str, transform_func, logger: logging.Logger):
        """Seed data from parquet file one by one"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        full_parquet_path = os.path.join(current_dir, parquet_path)
        
        if not os.path.exists(full_parquet_path):
            logger.error(f"Error: The file {full_parquet_path} does not exist!")
            return

        # Read parquet using polars
        df = pl.read_parquet(full_parquet_path)
        
        # Transform data
        records = [transform_func(row) for row in df.to_dicts()]
        
        # Process one by one
        with requests.Session() as session:
            for record in records:
                self.send_request(session, endpoint, record, logger)

    @staticmethod
    def transform_cow(row) -> Dict[str, Any]:
        """Transform cow data"""
        return {
            "id": str(row['id']),
            "name": str(row['name']),
            "birthdate": str(row['birthdate'])
        }

    @staticmethod
    def transform_measurement(row) -> Dict[str, Any]:
        """Transform measurement data"""
        return {
            "sensor_id": str(row['sensor_id']),
            "cow_id": str(row['cow_id']),
            "value": str(row['value']),
            "timestamp": str(row['timestamp'])
        }

    @staticmethod
    def transform_sensor(row) -> Dict[str, Any]:
        """Transform sensor data"""
        return {
            "id": str(row['id']),
            "unit": str(row['unit'])
        }

def main():
    # Add argument parsing
    parser = argparse.ArgumentParser(description='Seed data to Kafka')
    parser.add_argument('--type', type=str, choices=['sensors', 'cows', 'measurements', 'all'],
                      help='Type of data to seed', default='all')
    args = parser.parse_args()

    seeder = DataSeeder()

    if args.type in ['sensors', 'all']:
        sensor_logger = setup_logger('data_seeder_sensor.log')
        sensor_logger.info("New Run - Seeding sensors...")
        seeder.seed_data(
            parquet_path="files/sensors.parquet",
            endpoint="sensor",
            transform_func=DataSeeder.transform_sensor,
            logger=sensor_logger
        )
    
    if args.type in ['cows', 'all']:
        cow_logger = setup_logger('data_seeder_cow.log')
        cow_logger.info("New Run - Seeding cows...")
        seeder.seed_data(
            parquet_path="files/cows.parquet",
            endpoint="cow",
            transform_func=DataSeeder.transform_cow,
            logger=cow_logger
        )
    
    if args.type in ['measurements', 'all']:
        measurement_logger = setup_logger('data_seeder_measurement.log')
        measurement_logger.info("New Run - Seeding measurements...")
        seeder.seed_data(
            parquet_path="files/measurements.parquet",
            endpoint="measurement",
            transform_func=DataSeeder.transform_measurement,
            logger=measurement_logger
        )

if __name__ == "__main__":
    main()
