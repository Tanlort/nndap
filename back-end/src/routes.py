from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal
from datetime import datetime

router = APIRouter()


# Fetch cow details and the latest sensor data
@router.get("/cows/{cow_id}", response_model=schemas.CowResponse)
def get_cow(cow_id: str):
    db: Session = SessionLocal()
    cow_id = cow_id.strip()

    # Fetch cow from the database using CRUD function
    cow = crud.get_cow(db, cow_id)
    if not cow:
        crud.close_connection(db)
        raise HTTPException(status_code=404, detail="Cow not found")

    latest_sensor_data = crud.get_latest_sensor_data(db, cow_id)

    if not latest_sensor_data:
        crud.close_connection(db)
        raise HTTPException(status_code=404, detail="Latest sensor data not found")
    crud.close_connection(db)

    # Prepare the response
    birthdate = None
    if cow.birthdate:
        if isinstance(cow.birthdate, str):  # Convert string to datetime
            birthdate = datetime.fromisoformat(cow.birthdate)
        else:
            birthdate = cow.birthdate

    if latest_sensor_data:
        latest_sensor_data_response = schemas.DailyMeasurementAggregationResponse(
            sensor_id=latest_sensor_data.sensor_id,
            cow_id=latest_sensor_data.cow_id,
            date=latest_sensor_data.date,  
            average_value=latest_sensor_data.average_value,
            min_value=latest_sensor_data.min_value,
            max_value=latest_sensor_data.max_value,
            records_count=latest_sensor_data.records_count
        )

    # Convert to Pydantic model before returning
    response = schemas.CowResponse(
        id=cow.id,
        name=cow.name,
        birthdate=birthdate,
        created_at=cow.created_at,
        latest_sensor_data=latest_sensor_data_response
    )

    return response


# Create a new cow
@router.post("/cows/", response_model=schemas.CowResponse)
def create_cow(cow: schemas.CowCreate):
    db: Session = SessionLocal()

    # Call the CRUD function to create a cow
    new_cow = crud.create_cow(db, cow)
    crud.write_cow_to_db(db, new_cow)
    crud.close_connection(db)

    return schemas.CowResponse(
        id=new_cow.id,
        name=new_cow.name,
        birthdate=new_cow.birthdate,
        created_at=new_cow.created_at
    )


# Generate daily report for milk production and cow weight
@router.get("/generate-report/{report_date}", response_model=schemas.Report)
def generate_daily_report(report_date: str):
    db: Session = SessionLocal()

    try:
        report_date = report_date.strip()
        report_date = datetime.strptime(report_date, "%Y-%m-%d")
    except ValueError:
        crud.close_connection(db)
        raise HTTPException(status_code=400, detail="Invalid date format. Please use 'YYYY-MM-DD'.")

    # Call the CRUD function to generate the report
    try:
        report = crud.generate_report(db, report_date)
    except ValueError as e:
        crud.close_connection(db)
        raise HTTPException(status_code=400, detail=str(e))

    crud.close_connection(db)

    return report
