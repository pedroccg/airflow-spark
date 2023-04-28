# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the monitoring script into the container
COPY monitor.py /app

# Install any required dependencies (if needed)
RUN pip install requests

# Run the monitoring script when the container launches
CMD ["python", "monitor.py"]
