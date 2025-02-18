from kafka import KafkaConsumer
from kafka.errors import KafkaError
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
from typing import Type
from datetime import datetime
import logging

class BaseConsumer:
    def __init__(self, model: Type[BaseModel], db_config: dict, kafka_config: dict, logger: logging.Logger):
        self.logger = logger
        self.db_config = db_config
        self.kafka_config = kafka_config
        self.model = model
        self.connection = self.create_sql_connection()
        self.consumer = self.create_kafka_consumer()


    def create_sql_connection(self, ):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=self.db_config['host'],
                user=self.db_config['user'],
                password=self.db_config['password'],
                database=self.db_config['database']
            )
            self.logger.info("MySQL connection successful")
        except Error as e:
            self.logger.error(f"The error '{e}' occurred")
        return connection
        
    def create_kafka_consumer(self):
        consumer = None
        try:
            consumer =  KafkaConsumer(
                self.kafka_config['topic'],
                auto_offset_reset='earliest',
                bootstrap_servers=[self.kafka_config['server']],
                enable_auto_commit=True,
                group_id=self.kafka_config['group_id'],
                value_deserializer=lambda x: x.decode('utf-8')
            )
            self.logger.info(f"Kafka consumer created successfully for topic: {self.kafka_config['topic']}")
        except KafkaError as e:
            self.logger.error(f"Kafka connection error: {e}")
        return consumer
    
    def reconnect_db(self):
        """Reconnect if MySQL connection is lost"""
        if not self.connection or not self.connection.is_connected():
            self.logger.info("Reconnecting to MySQL...")
            self.connection = self.create_sql_connection()

    def insert_message(self, message: BaseModel):
        if not self.connection or not self.connection.is_connected():
            self.reconnect_db()
        
        #TOD: Develop a class to handle data types before inserting
        try:
            if message.timestamp:
                timestamp = datetime.fromtimestamp(float(message.timestamp)).strftime('%Y-%m-%d %H:%M:%S')
                message.timestamp = timestamp 
        except AttributeError:
            pass
        for key in message.dict().keys():
            if message.dict()[key] == "None":
                setattr(message, key, None)


        cursor = self.connection.cursor()
        table_name = self.model.TABLE_NAME
        columns = ', '.join(self.model.__fields__.keys())
        values_placeholders = ', '.join(['%s'] * len(self.model.__fields__))

        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values_placeholders})"
        
        cursor.execute(query, tuple(message.dict().values()))
        self.connection.commit()

        cursor.close()
            
    def consume(self):
        try:
            for message in self.consumer:
                self.logger.info(f"Received message: {message.value}")
                message_data = self.model.parse_raw(message.value)
                self.insert_message(message_data)
        except KeyboardInterrupt:
            self.logger.info("Kafka consumer interrupted")
        finally:
            self.consumer.close()
            if self.connection:
                self.connection.close()