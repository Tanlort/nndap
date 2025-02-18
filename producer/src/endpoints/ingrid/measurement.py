from fastapi import APIRouter, HTTPException
from pydantic import BaseModel 
from typing import Optional
from src.producers.producer_manager import ProducerManager
import json

router = APIRouter(prefix="/measurement", tags=["measurement"])
producer = ProducerManager(bootstrap_servers='kafka:9092')

#TODO: Create Folder for Models and move this to the folder
class MeasurementInput(BaseModel):
    """Model for user input """
    sensor_id: Optional[str] = None
    cow_id: Optional[str] = None
    value: Optional[str] = None
    timestamp: Optional[str] = None

@router.post("/")
async def record_measurement(reading: MeasurementInput):
    try:
        message = json.loads(reading.model_dump_json())

        result = producer.produce(
            topic='measurements',
            message=message,
            key=f"{message.get('sensor_id')}_{message.get('cow_id')}"
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
