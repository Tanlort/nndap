#TODO: Add key to the message to improve performance and processing
from confluent_kafka import Producer
from typing import Dict, Any, Optional, Callable
import json

class ProducerManager:
    def __init__(self, bootstrap_servers: str = 'kafka:9092', client_id: str = 'producer_ingrid'):
        """Initialize Kafka producer.
        
        Args:
            bootstrap_servers: Kafka broker address
            client_id: Unique identifier for this producer
        """
        self.producer = Producer({
            'bootstrap.servers': bootstrap_servers,
            'client.id': client_id
        })

    def produce(self, 
                topic: str, 
                message: Dict[str, Any],
                key: Optional[str] = None) -> Dict[str, str]:
        """Produce message to Kafka topic.
        
        Args:
            topic: Topic name
            message: Message to send
            
        Returns:
            Dict with status
        """
        try:
            # Convert message to bytes if needed
            if isinstance(message, dict):
                message = json.dumps(message).encode('utf-8')
            

            # Produce message
            self.producer.produce(
                topic=topic,
                value=message,
                key=key
            )
            
            return {"status": "success", "message": f"Sent to {topic} kafka topic"}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}