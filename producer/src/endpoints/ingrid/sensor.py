from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from src.producers.producer_manager import ProducerManager
import json

router = APIRouter(prefix="/sensor", tags=["sensor"])
producer = ProducerManager(bootstrap_servers='kafka:9092')

#TODO: Create Folder for Models and move this to the folder
class SensorInput(BaseModel):
    """Model for user input """
    id: Optional[str] = None
    unit: Optional[str] = None

@router.post("/")
async def record_sensor(reading: SensorInput):
    try:
        message = json.loads(reading.model_dump_json())
        
        result = producer.produce(
            topic='sensors',
            message=message,
            key=f"{message.get('id')}"
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
