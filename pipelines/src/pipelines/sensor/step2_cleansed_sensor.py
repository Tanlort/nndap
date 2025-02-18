import pandas as pd
from sqlalchemy import create_engine
from pydantic import BaseModel, ValidationError, field_validator
from typing import List

# SQL Config
sql_config = {
    "host": "mysql",
    "port": "3306",
    "user": "root",
    "password": "secret",
}

# Define the Pydantic model
class SensorDataModel(BaseModel):
    id: str
    unit: str

    @field_validator("unit")
    def validate_unit(cls, value):
        if len(value) > 10:  # Example rule: unit should be less than or equal to 10 characters
            raise ValueError("unit must be 10 characters or less")
        return value

def run_step2_sensor():
    raw_data = load_raw_data()

    if raw_data.isnull().values.any():
        print("Warning: Null values found in the raw data.")
        raw_data.fillna(method='ffill', inplace=True)

    # Check for duplicates
    if raw_data.duplicated().any():
        print("Warning: Duplicates found in the raw data.")
        raw_data.drop_duplicates(inplace=True)

    # Validate and fix data types
    valid_rows = []
    invalid_rows = []

    for index, row in raw_data.iterrows():
        try:
            # Create a SensorDataModel instance to validate the row
            sensor_data = SensorDataModel(id=row['id'], unit=row['unit'])
            valid_rows.append(row)  # Append row if valid
        except ValidationError as e:
            print(f"Validation error at index {index}: {e}")
            invalid_rows.append(index)  # Log or handle invalid rows if needed

    # TODO: Handle invalid rows (e.g., by dropping them or fixing)
    raw_data.drop(index=invalid_rows, inplace=True)

    # Write to the gold layer after validation
    write_to_gold_layer(raw_data)

def load_raw_data():
    engine = create_engine(f'mysql+pymysql://{sql_config["user"]}:{sql_config["password"]}@{sql_config["host"]}:{sql_config["port"]}/bronze_layer')
    query = "SELECT * FROM sensors"  # Adjust the table name as needed
    return pd.read_sql(query, engine)

def write_to_gold_layer(data):
    engine = create_engine(f'mysql+pymysql://{sql_config["user"]}:{sql_config["password"]}@{sql_config["host"]}:{sql_config["port"]}/gold_layer')
    data.to_sql('sensors', con=engine, if_exists='replace', index=False)  # Adjust the table name as needed

# Automatically run the function when the script is executed
if __name__ == "__main__":
    run_step2_sensor()
