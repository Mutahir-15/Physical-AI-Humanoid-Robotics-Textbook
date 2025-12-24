# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the working directory
COPY backend/requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Set environment variables for FastAPI
ENV PYTHONPATH=/app
ENV DOCS_DIRECTORY=docs
ENV PORT=8000

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the Uvicorn server when the container launches
# Use 0.0.0.0 to bind to all available network interfaces
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
