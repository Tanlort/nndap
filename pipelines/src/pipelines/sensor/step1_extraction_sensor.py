from config import mysql, kafka
from utils.base_consumer import BaseConsumer
from utils.base_log import setup_logger
from pydantic import BaseModel
from typing import Optional, ClassVar

logger = setup_logger('sensor_data_consumer.log')

class SensorDataModel(BaseModel):
    """Model for user input"""
    id: Optional[str] = None
    unit: Optional[str] = None
    
    TABLE_NAME: ClassVar[str] = "sensors"


class SensorDataConsumer(BaseConsumer):
    logger.info("Starting Sensor Data Consumer")
    def __init__(self, db_config: dict, kafka_config: dict):
        super().__init__(SensorDataModel, db_config['bronze_layer'], kafka_config['sensors'], logger)
    
# Example usage
if __name__ == "__main__":
    consumer = SensorDataConsumer(mysql, kafka)
    consumer.consume()