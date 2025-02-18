import pandas as pd
from sqlalchemy import create_engine
from pydantic import BaseModel, ValidationError, field_validator
from typing import Optional
from datetime import datetime

# SQL Config
sql_config = {
    "host": "mysql",
    "port": "3306",
    "user": "root",
    "password": "secret",
}

# Define the Pydantic model
class CowInput(BaseModel):
    """Model for cow input validation (no timestamp field)"""
    id: str
    name: str
    birthdate: datetime

    # Validator for birthdate to ensure it is a valid datetime
    @field_validator("birthdate")
    def validate_birthdate(cls, value):
        if isinstance(value, datetime):
            return value
        raise ValueError("Birthdate must be a valid datetime object")

def run_step2_cow():
    raw_data = load_raw_data()

    if raw_data.isnull().values.any():
        print("Warning: Null values found in the raw data.")
        raw_data.fillna(method='ffill', inplace=True)

    # Validate and fix data types (birthdate)
    valid_rows = []
    invalid_rows = []

    for index, row in raw_data.iterrows():
        try:
            # Convert 'birthdate' column to datetime
            row['birthdate'] = pd.to_datetime(row['birthdate'], errors='coerce')

            # Create a CowInput instance to validate the row
            cow_data = CowInput(
                id=row['id'],
                name=row['name'],
                birthdate=row['birthdate']
            )
            valid_rows.append(row)  # Append the row if valid
        except (ValidationError, ValueError) as e:
            print(f"Validation error at index {index}: {e}")
            invalid_rows.append(index)  # Log or handle invalid rows if needed

    # Optionally: Handle invalid rows (e.g., by dropping them or fixing)
    raw_data.drop(index=invalid_rows, inplace=True)

    # Write to the gold layer after validation
    write_to_gold_layer(raw_data)

def load_raw_data():
    engine = create_engine(f'mysql+pymysql://{sql_config["user"]}:{sql_config["password"]}@{sql_config["host"]}:{sql_config["port"]}/bronze_layer')
    query = "SELECT * FROM cows"  # Adjust the table name as needed
    return pd.read_sql(query, engine)

def write_to_gold_layer(data):
    engine = create_engine(f'mysql+pymysql://{sql_config["user"]}:{sql_config["password"]}@{sql_config["host"]}:{sql_config["port"]}/gold_layer')
    data.to_sql('cows', con=engine, if_exists='replace', index=False)  # Adjust the table name as needed

# Automatically run the function when the script is executed
if __name__ == "__main__":
    run_step2_cow()
