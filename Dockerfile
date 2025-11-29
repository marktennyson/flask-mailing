# Flask-Mailing v3.0.0 - 2026-Ready Dockerfile
# Python 3.12 base image for modern performance
FROM python:3.12-slim

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create non-root user for security
RUN groupadd -r flaskmail && useradd -r -g flaskmail flaskmail

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt pyproject.toml setup.py ./
COPY flask_mailing/__init__.py flask_mailing/__init__.py

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install -e .[dev,email-checking]

# Copy the rest of the application
COPY . .

# Change ownership to non-root user
RUN chown -R flaskmail:flaskmail /app

# Switch to non-root user
USER flaskmail

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import flask_mailing; print('Flask-Mailing v3.0.0 - Health OK')"

# Default command
CMD ["python", "-c", "import flask_mailing; print('Flask-Mailing v3.0.0 - 2026 Ready!')"]
