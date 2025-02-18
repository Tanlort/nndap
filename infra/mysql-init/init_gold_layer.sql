CREATE DATABASE IF NOT EXISTS gold_layer CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE gold_layer;

CREATE TABLE cows (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    birthdate DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE sensors (
    id VARCHAR(255) PRIMARY KEY,
    unit VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE measurements_daily_aggregations (
    sensor_id VARCHAR(255),
    cow_id VARCHAR(255),
    date DATE,
    average_value FLOAT,
    min_value FLOAT,
    max_value FLOAT,
    records_count INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (sensor_id, cow_id, date)
);

CREATE TABLE measurements_weekly_aggregations (
    sensor_id VARCHAR(255),
    cow_id VARCHAR(255),
    `week` INT,
    `month` INT,
    `year` INT,
    average_value FLOAT,
    min_value FLOAT,
    max_value FLOAT,
    records_count INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (sensor_id, cow_id, `year`, `week`)
);

CREATE TABLE measurements_monthly_aggregations (
    sensor_id VARCHAR(255),
    cow_id VARCHAR(255),
    `month` INT,
    `year` INT,
    average_value FLOAT,
    min_value FLOAT,
    max_value FLOAT,
    records_count INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (sensor_id, cow_id, `year`, `month`)
);

CREATE TABLE measurements_yearly_aggregations (
    sensor_id VARCHAR(255),
    cow_id VARCHAR(255),
    `year` INT,
    average_value FLOAT,
    min_value FLOAT,
    max_value FLOAT,
    records_count INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (sensor_id, cow_id, `year`)
);
