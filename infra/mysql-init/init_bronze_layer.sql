CREATE DATABASE IF NOT EXISTS bronze_layer;

USE bronze_layer;

CREATE TABLE cows (
    id VARCHAR(255), 
    name VARCHAR(255),
    birthdate VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sensors (
    id VARCHAR(255),
    unit VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE measurements (
    sensor_id VARCHAR(255),
    cow_id VARCHAR(255),
    timestamp VARCHAR(255),
    value VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);