# SME Supply Chain Risk Analysis - Frontend Dockerfile
# Multi-stage build for development and production

# =============================================================================
# Base stage - shared dependencies
# =============================================================================
FROM node:24-slim AS base

# Set environment variables
ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1

WORKDIR /app

# =============================================================================
# Dependencies stage - install node modules
# =============================================================================
FROM base AS deps

# Install dependencies needed for node-gyp (native modules)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    make \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy package files
COPY package.json package-lock.json* .npmrc* ./

# Install dependencies
RUN npm ci --legacy-peer-deps

# =============================================================================
# Development stage
# =============================================================================
FROM base AS development

ENV NODE_ENV=development

WORKDIR /app

# Copy node_modules from deps stage
COPY --from=deps /app/node_modules ./node_modules

# Copy application code (will be overwritten by volume mount in dev)
COPY . .

# Expose port for app
EXPOSE 3000

# Default command for development with hot reload
CMD ["npm", "run", "dev"]

# =============================================================================
# Builder stage - build the application
# =============================================================================
FROM base AS builder

WORKDIR /app

# Copy node_modules from deps stage
COPY --from=deps /app/node_modules ./node_modules

# Copy application code
COPY . .

# Build the application
RUN npm run build

# =============================================================================
# Production stage
# =============================================================================
FROM base AS production

WORKDIR /app

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser

# Copy built application
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

# Set proper ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 3000

# Set hostname for Next.js standalone
ENV HOSTNAME="0.0.0.0"
ENV PORT=3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/ || exit 1

# Production command (standalone server)
CMD ["node", "server.js"]
