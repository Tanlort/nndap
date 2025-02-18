from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#TODO: Add the database config to the .env file
sql_config = {
    "host": "mysql",
    "port": "3306",
    "user": "root",
    "password": "secret",
}

# Database setup
DATABASE_URL = (f'mysql+pymysql://{sql_config["user"]}:{sql_config["password"]}@{sql_config["host"]}:{sql_config["port"]}/gold_layer')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()