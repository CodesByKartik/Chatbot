# Use an official Python image as the base
FROM python:3.10

# Install build dependencies
RUN apt-get update && apt-get install -y build-essential python3-dev

# Set the working directory
WORKDIR /app

# Copy all files to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the default FastAPI port
EXPOSE 8000

# Set the start command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
