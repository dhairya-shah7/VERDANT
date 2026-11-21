# ==============================================================================
# V.E.R.D.A.N.T. — Google Cloud Run Production Multi-Stage Container
# Built for Google Cloud & DeepMind Startup Buildathon 2026
# ==============================================================================

FROM python:3.11-slim AS base

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PORT=8000

WORKDIR /app

# Install system dependencies for Playwright headless browser & imaging
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    fonts-liberation \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir \
        google-cloud-aiplatform \
        google-cloud-storage \
        google-cloud-secret-manager \
        cloud-sql-python-connector[asyncpg] \
        asyncpg

# Install Playwright Chromium headless engine for Sentinel crawler
RUN python -m playwright install --with-deps chromium

# Copy application source code
COPY . .

# Ensure storage directories exist with write permissions and copy assets
RUN mkdir -p uploads/assets uploads/captures tests static/assets && \
    cp -r static/assets/* uploads/assets/ 2>/dev/null || true && \
    chmod -R 777 uploads static

# Create non-root system user for security compliance (SOC2 / GCP best practices)
RUN useradd -m -u 1001 verdantuser && \
    chown -R verdantuser:verdantuser /app

USER verdantuser

# Expose Cloud Run dynamic port (default 8000)
EXPOSE 8000

# Healthcheck probe for Cloud Run service vitality
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Launch production server with Uvicorn worker
CMD ["sh", "-c", "uvicorn server:app --host 0.0.0.0 --port ${PORT} --workers 2 --timeout-keep-alive 65"]
