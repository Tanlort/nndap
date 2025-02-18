mysql = {
    "bronze_layer":{
        "host": "mysql",
        "port": "3306",
        "user": "root",
        "password": "secret",
        "database": "bronze_layer",
    },
    "silver_layer":{
        "host": "mysql",
        "port": "3306",
        "user": "root",
        "password": "secret",
        "database": "silver_layer",
    },
    "gold_layer":{
        "host": "mysql",
        "port": "3306",
        "user": "root",
        "password": "secret",
        "database": "gold_layer",
    }
}

kafka = {
    "cows":{
        "topic": "cows",
        "group_id": "cows",
        "server": "kafka:9092",
    },
    "measurements":{
        "topic": "measurements",
        "group_id": "measurements",
        "server": "kafka:9092",
    },
    "sensors":{
        "topic": "sensors",
        "group_id": "sensors_consumer",
        "server": "kafka:9092",
    }
}