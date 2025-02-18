#!/bin/bash

# Run the data_seeder.py script with different types
docker exec -d producer_ingrid python3 data/data_seeder.py --type sensors
docker exec -d producer_ingrid python3 data/data_seeder.py --type cows
docker exec -d producer_ingrid python3 data/data_seeder.py --type measurements

echo "All seeders currently running!"
