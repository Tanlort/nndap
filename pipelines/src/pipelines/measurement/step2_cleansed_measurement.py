import pandas as pd
from sqlalchemy import create_engine
from pydantic import BaseModel, ValidationError, field_validator
from datetime import datetime

# SQL Config
sql_config = {
    "host": "mysql",
    "port": "3306",
    "user": "root",
    "password": "secret",
}

# Define the Pydantic model
class MeasurementsDataModel(BaseModel):
    """Model for measurement data validation"""
    cow_id: str
    sensor_id: str
    timestamp: datetime
    value: float

    # Custom validation for timestamp to ensure correct format
    @field_validator("timestamp")
    def validate_timestamp(cls, value):
        if isinstance(value, datetime):
            return value
        raise ValueError("Timestamp must be a valid datetime object")

    # Custom validation for value to ensure it's a valid float and non-negative
    @field_validator("value")
    def validate_value(cls, value):
        if not isinstance(value, (float, int)):  # Allow integers but treat as floats
            raise ValueError("Value must be a float")
        if value < 0:
            raise ValueError("Value must be 0 or greater")
        return float(value)

def run_step2_measurement():
    raw_data = load_raw_data()

    if raw_data.isnull().values.any():
        print("Warning: Null values found in the raw data.")
        raw_data.fillna(method='ffill', inplace=True)

    # Validate and fix data types
    valid_rows = []
    invalid_rows = []

    for index, row in raw_data.iterrows():
        try:
            # Attempt to convert 'timestamp' column to datetime
            row['timestamp'] = pd.to_datetime(row['timestamp'], errors='coerce')

            # Create a MeasurementsDataModel instance to validate the row
            measurement_data = MeasurementsDataModel(
                cow_id=row['cow_id'],
                sensor_id=row['sensor_id'],
                timestamp=row['timestamp'],
                value=row['value']
            )
            valid_rows.append(row)  # Append the row if valid
        except (ValidationError, ValueError) as e:
            print(f"Validation error at index {index}: {e}")
            invalid_rows.append(index)  # Log or handle invalid rows if needed

    # Optionally: Handle invalid rows (e.g., by dropping them or fixing)
    raw_data.drop(index=invalid_rows, inplace=True)

    # Write to the silver layer after validation
    write_to_silver_layer(raw_data)

def load_raw_data():
    engine = create_engine(f'mysql+pymysql://{sql_config["user"]}:{sql_config["password"]}@{sql_config["host"]}:{sql_config["port"]}/bronze_layer')
    query = "SELECT * FROM measurements"  # Adjust the table name as needed
    return pd.read_sql(query, engine)

def write_to_silver_layer(data):
    engine = create_engine(f'mysql+pymysql://{sql_config["user"]}:{sql_config["password"]}@{sql_config["host"]}:{sql_config["port"]}/silver_layer')
    #TODO: Check if the row exists in the table, if not, insert the row, if yes, update the row
    data.to_sql('measurements', con=engine, if_exists='replace', index=False) 

# Automatically run the function when the script is executed
if __name__ == "__main__":
    run_step2_measurement()
