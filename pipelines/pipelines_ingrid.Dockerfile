# Use the official Python image as a base
FROM python:3.11-slim

COPY requirements.txt /workspace/

# Set the working directory in the container
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y pkg-config libmariadb-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Command to run your application (modify as needed)
CMD ["sleep", "infinity"]