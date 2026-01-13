# SME Supply Chain Risk Analysis - Backend Dockerfile
# Multi-stage build for development and production

# =============================================================================
# Base stage - shared dependencies
# =============================================================================
FROM python:3.11-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies including Playwright/Chromium requirements (ADR-007)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    # Playwright/Chromium dependencies
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxcb1 \
    libxkbcommon0 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libatspi2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# =============================================================================
# Development stage
# =============================================================================
FROM base AS development

# Install development dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

# Install Playwright browser binaries (Chromium only)
RUN playwright install chromium

# Copy application code (will be overwritten by volume mount in dev)
COPY . .

# Expose ports for app and debugger
EXPOSE 8000 5678

# Default command for development
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# =============================================================================
# Production build stage
# =============================================================================
FROM base AS builder

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browser binaries (Chromium only)
# Set PLAYWRIGHT_BROWSERS_PATH for consistent location
ENV PLAYWRIGHT_BROWSERS_PATH=/opt/playwright
RUN playwright install chromium

# =============================================================================
# Production stage
# =============================================================================
FROM base AS production

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser

# Set Playwright browsers path
ENV PLAYWRIGHT_BROWSERS_PATH=/opt/playwright

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy Playwright browsers from builder
COPY --from=builder /opt/playwright /opt/playwright

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Production command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
