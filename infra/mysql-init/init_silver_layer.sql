CREATE DATABASE IF NOT EXISTS silver_layer;

USE silver_layer;

CREATE TABLE measurements (
    sensor_id VARCHAR(255),
    cow_id VARCHAR(255),
    timestamp DATETIME,
    value FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (sensor_id, cow_id, timestamp)
);