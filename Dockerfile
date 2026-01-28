FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update --fix-missing && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    netcat-traditional \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose port (will be overridden by docker-compose)
EXPOSE 8000

# Set only essential environment variables
ENV PYTHONUNBUFFERED=1

# Run entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
