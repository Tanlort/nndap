from sqlalchemy import Column, String, Integer, Float, Date, DateTime, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base
from uuid import uuid4
from datetime import datetime

Base = declarative_base()

class CowDB(Base):
    __tablename__ = "cows"
    
    id = Column(String, primary_key=True, default=str(uuid4()))
    name = Column(String, index=True)
    birthdate = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class DailyMeasurementAggregationResponseDB(Base):
    __tablename__ = "measurements_daily_aggregations"  # Table name in the database

    # Column definitions
    sensor_id = Column(String(255), nullable=False)
    cow_id = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)
    average_value = Column(Float, nullable=False)
    min_value = Column(Float, nullable=False)
    max_value = Column(Float, nullable=False)
    records_count = Column(Integer, nullable=False)

    # Define a composite primary key using PrimaryKeyConstraint
    __table_args__ = (
        PrimaryKeyConstraint('sensor_id', 'cow_id', 'date'),
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )