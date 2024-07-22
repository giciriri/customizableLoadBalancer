# Use an official Python image as a base
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the application code
COPY app.py .
COPY load_balancer.py .
COPY consistent_hashing.py .

# Expose the port the Load Balancer will listen on
EXPOSE 4001

# Run the command to start the Load Balancer when the container starts
CMD ["python", "app.py"]
