from fastapi import FastAPI
from src.topics import Topics, TopicManager
from src.endpoints.ingrid.cow import router as cow_router
from src.endpoints.ingrid.sensor import router as sensor_router
from src.endpoints.ingrid.measurement import router as measurement_router

# -----------------------------GENERAL TOPICS-----------------------------

#TODO: Get from env
#TODO: Move to an API
KAFKA_BROKER_URL = "kafka_ingrid"


manager = TopicManager(bootstrap_servers=KAFKA_BROKER_URL)
    
# Get all topic names from enum
topic_names = [topic.value for topic in Topics]

for topic in topic_names:
    #TODO: ADD LOGS
    if not topic in manager.get_topics():
        # Create topics
        results = manager.create_topics(
            topics=topic_names,
            num_partitions=1,
            replication_factor=1
        )
    else:
        continue 
        ## print(f"Topic {topic} already exists")
        
# -----------------------------GENERAL TOPICS-----------------------------

# ---------------------------------API ------------------------------------

app = FastAPI()

app.include_router(cow_router)
app.include_router(sensor_router)
app.include_router(measurement_router)

# ---------------------------------API ------------------------------------
