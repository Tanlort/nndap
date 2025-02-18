from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List, Union

class CowCreate(BaseModel):
    name: str
    birthdate: Optional[datetime] = None

    class Config:
        orm_mode = True

class DailyMeasurementAggregationResponse(BaseModel):
    sensor_id: str
    cow_id: str
    date: date
    average_value: float
    min_value: float
    max_value: float
    records_count: int

    class Config:
        orm_mode = True
# Pydantic model for Cow response
class CowResponse(BaseModel):
    id: str
    name: str
    birthdate: Optional[datetime] = None
    created_at: datetime
    latest_sensor_data: Optional[DailyMeasurementAggregationResponse] = None

    class Config:
        orm_mode = True


class MilkProduction(BaseModel):
    cow_id: str
    milk_produced: float

class CowWeight(BaseModel):
    cow_id: str
    current_weight: float
    avg_weight_last_30_days: float

class Report(BaseModel):
    report_date: str
    milk_production: List[MilkProduction]
    cow_weights: List[CowWeight]
    ill_cows: Union[List[str], str]  # Either a list of cows or a message if no ill cows
