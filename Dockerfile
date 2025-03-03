# Use an official Python runtime as a parent image
FROM python:3.13.2-slim

# Install system dependencies
RUN apt update && \
    apt install -y --no-install-recommends default-mysql-client && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app will run on
EXPOSE 8000

# Run migrations, seed data, and start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
