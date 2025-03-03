# Use an official Python image as the base
FROM python:3.7

# Set the working directory
WORKDIR /app

# Install system dependencies required for building some Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies individually to troubleshoot installation issues
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose the default FastAPI port
EXPOSE 8000

# Set the start command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
