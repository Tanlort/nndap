import argparse
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import List, ClassVar


# SQL Config
sql_config = {
    "host": "mysql",
    "port": "3306",
    "user": "root",
    "password": "secret",
}

# Pydantic model for validating daily aggregation
class DailyAggregationModel(BaseModel):
    sensor_id: str
    cow_id: str
    date: datetime
    average_value: float
    min_value: float
    max_value: float
    records_count: int

    TABLE_NAME: ClassVar[str] = "measurements_daily_aggregations"

    @field_validator("average_value")
    def validate_average_value(cls, v):
        if v < 0:
            raise ValueError("Average value must be a non-negative number.")
        return v

    @field_validator("min_value")
    def validate_min_value(cls, v):
        if v < 0:
            raise ValueError("Min value must be a non-negative number.")
        return v

    @field_validator("max_value")
    def validate_max_value(cls, v):
        if v < 0:
            raise ValueError("Max value must be a non-negative number.")
        return v

    @field_validator("records_count")
    def validate_records_count(cls, v):
        if v < 0:
            raise ValueError("Records count must be a non-negative integer.")
        return v

# Pydantic model for validating weekly aggregation
class WeeklyAggregationModel(BaseModel):
    sensor_id: str
    cow_id: str
    week: int
    month: int
    year: int
    average_value: float
    min_value: float
    max_value: float
    records_count: int

    TABLE_NAME: ClassVar[str] = "measurements_weekly_aggregations"

    @field_validator("average_value")
    def validate_average_value(cls, v):
        if v < 0:
            raise ValueError("Average value must be a non-negative number.")
        return v

    @field_validator("min_value")
    def validate_min_value(cls, v):
        if v < 0:
            raise ValueError("Min value must be a non-negative number.")
        return v

    @field_validator("max_value")
    def validate_max_value(cls, v):
        if v < 0:
            raise ValueError("Max value must be a non-negative number.")
        return v

    @field_validator("records_count")
    def validate_records_count(cls, v):
        if v < 0:
            raise ValueError("Records count must be a non-negative integer.")
        return v

# Pydantic model for validating monthly aggregation
class MonthlyAggregationModel(BaseModel):
    sensor_id: str
    cow_id: str
    month: int
    year: int
    average_value: float
    min_value: float
    max_value: float
    records_count: int

    TABLE_NAME: ClassVar[str] = "measurements_monthly_aggregations"

    @field_validator("average_value")
    def validate_average_value(cls, v):
        if v < 0:
            raise ValueError("Average value must be a non-negative number.")
        return v

    @field_validator("min_value")
    def validate_min_value(cls, v):
        if v < 0:
            raise ValueError("Min value must be a non-negative number.")
        return v

    @field_validator("max_value")
    def validate_max_value(cls, v):
        if v < 0:
            raise ValueError("Max value must be a non-negative number.")
        return v

    @field_validator("records_count")
    def validate_records_count(cls, v):
        if v < 0:
            raise ValueError("Records count must be a non-negative integer.")
        return v

# Pydantic model for validating yearly aggregation
class YearlyAggregationModel(BaseModel):
    sensor_id: str
    cow_id: str
    year: int
    average_value: float
    min_value: float
    max_value: float
    records_count: int

    TABLE_NAME: ClassVar[str] = "measurements_yearly_aggregations"

    @field_validator("average_value")
    def validate_average_value(cls, v):
        if v < 0:
            raise ValueError("Average value must be a non-negative number.")
        return v

    @field_validator("min_value")
    def validate_min_value(cls, v):
        if v < 0:
            raise ValueError("Min value must be a non-negative number.")
        return v

    @field_validator("max_value")
    def validate_max_value(cls, v):
        if v < 0:
            raise ValueError("Max value must be a non-negative number.")
        return v

    @field_validator("records_count")
    def validate_records_count(cls, v):
        if v < 0:
            raise ValueError("Records count must be a non-negative integer.")
        return v


def load_silver_data():
    engine = create_engine(f'mysql+pymysql://{sql_config["user"]}:{sql_config["password"]}@{sql_config["host"]}:{sql_config["port"]}/silver_layer')
    query = "SELECT * FROM measurements"  # Adjust the table name as needed
    return pd.read_sql(query, engine)

def aggregate_data(data: pd.DataFrame, aggregation_type: str) -> pd.DataFrame:
    # Determine the correct aggregation function based on the user input
    data['timestamp'] = pd.to_datetime(data['timestamp'], errors='coerce')
    data['value'] = pd.to_numeric(data['value'], errors='coerce')

    if aggregation_type == 'daily':
        data['date'] = data['timestamp'].dt.date
        group_cols = ['sensor_id', 'cow_id', 'date']
    elif aggregation_type == 'weekly':
        data['week'] = data['timestamp'].dt.isocalendar().week
        data['month'] = data['timestamp'].dt.month
        data['year'] = data['timestamp'].dt.year
        group_cols = ['sensor_id', 'cow_id', 'week', 'month', 'year']
    elif aggregation_type == 'monthly':
        data['month'] = data['timestamp'].dt.month
        data['year'] = data['timestamp'].dt.year
        group_cols = ['sensor_id', 'cow_id', 'month', 'year']
    elif aggregation_type == 'yearly':
        data['year'] = data['timestamp'].dt.year
        group_cols = ['sensor_id', 'cow_id', 'year']
    else:
        print("Invalid aggregation type.")
        return pd.DataFrame()  # Return an empty dataframe

    # Perform the aggregation
    aggregated_data = data.groupby(group_cols).agg(
        average_value=('value', 'mean'),
        min_value=('value', 'min'),
        max_value=('value', 'max'),
        records_count=('value', 'count')
    ).reset_index()

    return aggregated_data

def validate_aggregated_data(aggregated_data: pd.DataFrame, aggregation_type: str):
    if aggregation_type == 'daily':
        for row in aggregated_data.itertuples():
            DailyAggregationModel(
                sensor_id=row.sensor_id,
                cow_id=row.cow_id,
                date=row.date,
                average_value=row.average_value,
                min_value=row.min_value,
                max_value=row.max_value,
                records_count=row.records_count
            )
    elif aggregation_type == 'weekly':
        for row in aggregated_data.itertuples():
            WeeklyAggregationModel(
                sensor_id=row.sensor_id,
                cow_id=row.cow_id,
                week=row.week,
                month=row.month,
                year=row.year,
                average_value=row.average_value,
                min_value=row.min_value,
                max_value=row.max_value,
                records_count=row.records_count
            )
    elif aggregation_type == 'monthly':
        for row in aggregated_data.itertuples():
            MonthlyAggregationModel(
                sensor_id=row.sensor_id,
                cow_id=row.cow_id,
                month=row.month,
                year=row.year,
                average_value=row.average_value,
                min_value=row.min_value,
                max_value=row.max_value,
                records_count=row.records_count
            )
    elif aggregation_type == 'yearly':
        for row in aggregated_data.itertuples():
            YearlyAggregationModel(
                sensor_id=row.sensor_id,
                cow_id=row.cow_id,
                year=row.year,
                average_value=row.average_value,
                min_value=row.min_value,
                max_value=row.max_value,
                records_count=row.records_count
            )
def write_to_gold_layer(data: pd.DataFrame, aggregation_type: str):
    engine = create_engine(f'mysql+pymysql://{sql_config["user"]}:{sql_config["password"]}@{sql_config["host"]}:{sql_config["port"]}/gold_layer')
    
    # Determine the table name based on the aggregation type
    if aggregation_type == 'daily':
        table_name = DailyAggregationModel.TABLE_NAME
    elif aggregation_type == 'weekly':
        table_name = WeeklyAggregationModel.TABLE_NAME
    elif aggregation_type == 'monthly':
        table_name = MonthlyAggregationModel.TABLE_NAME
    elif aggregation_type == 'yearly':
        table_name = YearlyAggregationModel.TABLE_NAME
    else:
        raise ValueError("Invalid aggregation type.")

    # Write to the specified table
    data.to_sql(table_name, con=engine, if_exists='replace', index=False)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Aggregate measurement data.")
    parser.add_argument(
        "--aggregation_type", 
        type=str, 
        required=True,
        choices=["daily", "weekly", "monthly", "yearly"],
        help="Specify the aggregation type (daily, weekly, monthly, yearly)"
    )
    args = parser.parse_args()

    # Load data from the silver layer
    print("Loading data from the silver layer...")
    data = load_silver_data()

    if data.isnull().values.any():
        print("Warning: Null values found in the data. Filling missing values with forward fill.")
        data.fillna(method='ffill', inplace=True)

    # Perform the aggregation
    print(f"Performing {args.aggregation_type} aggregation...")
    aggregated_data = aggregate_data(data, args.aggregation_type)

    if not aggregated_data.empty:
        print(f"Validating the aggregated {args.aggregation_type} data...")
        validate_aggregated_data(aggregated_data, args.aggregation_type)

        write_to_gold_layer(aggregated_data, args.aggregation_type)

        print(f"Data successfully validated and saved to Gold Layer.")
    else:
        print("Aggregation failed or invalid aggregation type.")

if __name__ == "__main__":
    main()
