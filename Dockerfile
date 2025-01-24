# Use an official Python runtime as a parent image
FROM python:3.13.1-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variables (you can specify custom ones if needed)
COPY .env .env

# Expose the port the app will run on (for FastAPI, default is 8000)
EXPOSE 80

# Command to run the application with Uvicorn (FastAPI server)
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "80"]
