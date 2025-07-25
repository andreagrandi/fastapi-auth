FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install the application in development mode
RUN pip install -e .

# Expose port
EXPOSE 7000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7000"]