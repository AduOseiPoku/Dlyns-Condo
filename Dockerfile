FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system libraries needed for psycopg2, image processing & health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev libjpeg-dev zlib1g-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . /app/

# Ensure media and staticfiles directories exist, normalize line endings and set permissions
RUN mkdir -p /app/media /app/staticfiles && \
    sed -i 's/\r$//' /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

# Collect static files for WhiteNoise production serving
RUN python manage.py collectstatic --noinput

# Dokploy listens on port 8000 by default
EXPOSE 8000

# Container healthcheck for Dokploy / Traefik
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Launch using entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
