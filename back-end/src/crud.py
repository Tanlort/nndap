from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime, timedelta
from . import models, schemas


# Fetch a cow by ID
def get_cow(db: Session, cow_id: str) -> models.CowDB:
    return db.query(models.CowDB).filter(models.CowDB.id == cow_id).first()

# In your crud module
def get_latest_sensor_data(db: Session, cow_id: str):
    return db.query(models.DailyMeasurementAggregationResponseDB).filter(
        models.DailyMeasurementAggregationResponseDB.cow_id == cow_id
    ).order_by(desc(models.DailyMeasurementAggregationResponseDB.date)).first()

# Create a new cow
def create_cow(db: Session, cow: schemas.CowCreate) -> models.CowDB:
    # Extract the name and number part (e.g., 'Sandra #3')
    name_parts = cow.name.split(" #")
    base_name = name_parts[0]
    number = int(name_parts[1]) if len(name_parts) > 1 else None
    # If the number is not provided, find the last number and increment it
    if number is None:
        last_cow = db.query(models.CowDB).filter(models.CowDB.name.like(f"{base_name} #%")).order_by(models.CowDB.created_at.desc()).first()
        if last_cow:
            last_number = int(last_cow.name.split(" #")[1])
            number = last_number + 1
        else:
            number = 1  # Start from 1 if no cows exist

    new_cow = models.CowDB(
        name=f"{base_name} #{number}",
        birthdate=cow.birthdate,
    )
    
    return new_cow

def write_cow_to_db(db: Session, cow: models.CowDB):
    db.add(cow)
    db.commit()
    db.refresh(cow)

def close_connection(db: Session):
    db.close()

# Generate daily report (for milk production, weight, and illness detection)
def generate_report(db: Session, report_date: datetime):
    # Query for Milk Production Data (Filtered by 'unit = l' for liters)
    milk_data = db.execute("""
        SELECT c.name, SUM(m.average_value) AS daily_production
        FROM measurements_daily_aggregations m
        JOIN sensors s ON m.sensor_id = s.id
        JOIN cows c ON m.cow_id = c.id
        WHERE m.date = :report_date
        AND s.unit = 'l'  -- Only include milk data (unit 'l')
        GROUP BY c.name
    """, {'report_date': report_date}).fetchall()

    # Query for Cow Weight Data (last 30 days, filtered by 'unit = kg' for kilograms)
    weight_data = db.execute("""
        SELECT c.name, MAX(m.average_value) AS current_weight, AVG(m.average_value) AS avg_weight_last_30_days
        FROM measurements_daily_aggregations m
        JOIN sensors s ON m.sensor_id = s.id
        JOIN cows c ON m.cow_id = c.id
        WHERE m.date BETWEEN :start_date AND :end_date
        AND s.unit = 'kg'  -- Only include weight data (unit 'kg')
        GROUP BY c.name
    """, {'start_date': report_date - timedelta(days=30), 'end_date': report_date}).fetchall()

    # Heuristic for Illness Detection: Identify cows with low production or weight loss
    ill_cows = []
    
    for cow_id, daily_production in milk_data:
        if daily_production < 5:
            ill_cows.append(cow_id)

    # Convert milk data into list of MilkProduction models
    milk_production_list = [
        schemas.MilkProduction(cow_id=cow[0], milk_produced=cow[1]) for cow in milk_data
    ]

    # Convert weight data into list of CowWeight models
    cow_weights_list = [
        schemas.CowWeight(cow_id=cow[0], current_weight=cow[1], avg_weight_last_30_days=cow[2]) for cow in weight_data
    ]

    # Prepare the report
    report = schemas.Report(
        report_date=report_date.strftime('%Y-%m-%d'),
        milk_production=milk_production_list,
        cow_weights=cow_weights_list,
        ill_cows=ill_cows if ill_cows else "No cows identified as potentially ill."
    )

    return report
