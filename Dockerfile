# Use a lightweight Python base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
# This caches the pip install layer if requirements.txt doesn't change
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

# Copy the rest of your application code
COPY . .

# Expose the port your Flask app runs on
EXPOSE 5000

# Command to run your application (using Gunicorn for production readiness)
# Install gunicorn: pip install gunicorn
# For development, you can use: CMD ["python", "run.py"]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]