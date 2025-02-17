# Use an official Python image as the base
FROM python:3.10

# Set the working directory
WORKDIR /app

# Install system dependencies (optional but might be necessary for some packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip to ensure the latest version is used
RUN pip install --upgrade pip

# Copy all files to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the default FastAPI port
EXPOSE 8000

# Set the start command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
