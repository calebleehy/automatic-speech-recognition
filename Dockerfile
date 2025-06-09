# Base Python image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your code folder into the container
COPY asr/ ./asr

# Expose the port used by Flask
EXPOSE 8001

# Run the API
CMD ["python", "asr/asr_api.py"]
