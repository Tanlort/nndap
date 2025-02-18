from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from src.producers.producer_manager import ProducerManager
import json

router = APIRouter(prefix="/cow", tags=["cow"])
producer = ProducerManager(bootstrap_servers='kafka:9092')

#TODO: Create Folder for Models and move this to the folder
class CowInput(BaseModel):
    """Model for user input - no timestamp"""
    id: Optional[str] = None
    name: Optional[str] = None
    birthdate: Optional[str] = None

@router.post("/")
async def record_cow(reading: CowInput):
    try:
        message = json.loads(reading.model_dump_json())

        result = producer.produce(
            topic='cows',
            message=message,
            key=f"{message.get('id')}"
        )
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))