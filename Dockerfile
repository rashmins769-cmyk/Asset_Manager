# Use an official lightweight Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Python file into the container
COPY main.py .

# Run the Python script when the container launches
CMD ["python", "main.py"]
