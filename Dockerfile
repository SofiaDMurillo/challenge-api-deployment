# Start from the official Ubuntu base image
FROM ubuntu:22.04

# Install system dependencies and Python
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set Python3.11 as default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

# Set work directory inside the container
WORKDIR /app

# Copy requirements file into container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project into the container
COPY . .

# Expose the port Uvicorn will run on
EXPOSE 8000

# Run the API using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]