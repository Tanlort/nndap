FROM python:3.11-slim

WORKDIR /workspace
ENV PYTHONPATH=/workspace/src

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY requirements.txt .
# Install Python packages
RUN pip install -r requirements.txt

# Changed the path to directly point to src/__main__.py
CMD ["uvicorn", "src.__main__:app", "--host", "0.0.0.0", "--port", "5001", "--reload"]