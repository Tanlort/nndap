from confluent_kafka.admin import AdminClient, NewTopic
from typing import List, Optional

class TopicManager:
    def __init__(self, bootstrap_servers: str = 'kafka'):
        """Initialize the Topic Manager.
        
        Args:
            bootstrap_servers (str): Kafka bootstrap servers
        """
        self.admin_client = AdminClient({
            'bootstrap.servers': bootstrap_servers,
        })
    
    def get_topics(self) -> List[str]:
        """Get all topics from Kafka.
        
        Returns:
            List[str]: List of topic names
        """
        return self.admin_client.list_topics().topics.keys()
        
    def create_topics(self, topics: List[str], 
                     num_partitions: int = 1, 
                     replication_factor: int = 1) -> dict:
        """Create multiple Kafka topics.
        
        Args:
            topics (List[str]): List of topic names
            num_partitions (int): Number of partitions per topic
            replication_factor (int): Replication factor per topic
            
        Returns:
            dict: Results of topic creation attempts
        """
        new_topics = [
            NewTopic(
                topic, 
                num_partitions=num_partitions, 
                replication_factor=replication_factor
            ) for topic in topics if topic not in self.get_topics()
        ]
        
        results = {}
        kafka_topics = self.admin_client.create_topics(new_topics)
        
        for topic, future in kafka_topics.items():
            try:
                future.result()
                results[topic] = "Created successfully"
                print(f"Topic {topic} created")
            except Exception as e:
                results[topic] = f"Failed: {str(e)}"
                print(f"Failed to create topic {topic}: {e}")
                
        return results
    
    #TODO: Add delete topics method
