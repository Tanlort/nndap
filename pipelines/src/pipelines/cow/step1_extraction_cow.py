from config import mysql, kafka
from utils.base_consumer import BaseConsumer
from utils.base_log import setup_logger
from pydantic import BaseModel
from typing import Optional, ClassVar
import logging

logger = setup_logger('cow_data_consumer.log')

class CowDataModel(BaseModel):
    """Model for user input"""
    id: Optional[str] = None
    name: Optional[str] = None
    birthdate: Optional[str] = None

    TABLE_NAME: ClassVar[str] = "cows"

class CowsDataConsumer(BaseConsumer):
    
    def __init__(self, db_config: dict, kafka_config: dict, logger: logging.Logger):
        logger.info("Starting Cows Data Consumer")
        super().__init__(CowDataModel, db_config['bronze_layer'], kafka_config['cows'], logger)

    def start(self):
        self.consume()

if __name__ == "__main__":
    consumer = CowsDataConsumer(mysql, kafka, logger)
    consumer.start()