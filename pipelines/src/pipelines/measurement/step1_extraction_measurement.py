from config import mysql, kafka
from utils.base_consumer import BaseConsumer
from utils.base_log import setup_logger
from pydantic import BaseModel
from typing import Optional, ClassVar

logger = setup_logger('measurement_data_consumer.log')

class MeasurementsDataModel(BaseModel):
    """Model for user input"""
    sensor_id: Optional[str] = None
    cow_id: Optional[str] = None
    timestamp: Optional[str] = None
    value: Optional[str] = None

    TABLE_NAME: ClassVar[str] = "measurements"

class MeasurementDataConsumer(BaseConsumer):
    logger.info("Starting Measurement Data Consumer")
    def __init__(self, db_config: dict, kafka_config: dict):
        super().__init__(MeasurementsDataModel, db_config['bronze_layer'], kafka_config['measurements'], logger)

if __name__ == "__main__":
    consumer = MeasurementDataConsumer(mysql, kafka)
    consumer.consume()
