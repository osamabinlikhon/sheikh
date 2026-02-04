# Use a Python 3.11 base image
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install system dependencies if any (e.g., for certain Python packages)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the FastAPI application runs on
EXPOSE 8000

# Command to run the application
# Use Uvicorn with Gunicorn for production or just Uvicorn for development
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
