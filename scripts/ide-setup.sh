#!/bin/bash
# SME Supply Chain Risk Analysis - IDE Setup Script
# Creates local dependencies for IDE intellisense without requiring local npm/pip
# Use this with Option B (Fully Dockerized Development)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "=========================================="
echo "SME Platform - IDE Setup for Docker Dev"
echo "=========================================="
echo ""

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed or not in PATH"
    exit 1
fi

echo "This script will create local dependencies for IDE support."
echo "Note: These are for IDE intellisense only - the Docker containers"
echo "use their own installed dependencies."
echo ""

# Frontend - create local node_modules
echo "[1/2] Installing frontend dependencies for IDE..."
echo "      This may take a few minutes..."
cd "$PROJECT_ROOT/frontend"

if [ -d "node_modules" ]; then
    echo "      node_modules already exists. Skipping."
else
    docker run --rm \
        -v "$(pwd):/app" \
        -w /app \
        node:24-slim \
        npm install --legacy-peer-deps
    echo "      Frontend dependencies installed."
fi

# Backend - create local venv
echo ""
echo "[2/2] Installing backend dependencies for IDE..."
cd "$PROJECT_ROOT/backend"

if [ -d "venv" ]; then
    echo "      venv already exists. Skipping."
else
    docker run --rm \
        -v "$(pwd):/app" \
        -w /app \
        python:3.11-slim \
        bash -c "python -m venv venv && venv/bin/pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt"
    echo "      Backend dependencies installed."
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Configure your IDE:"
echo ""
echo "VS Code:"
echo "  - Python: Set interpreter to backend/venv/bin/python"
echo "  - TypeScript: Should auto-detect frontend/node_modules"
echo ""
echo "PyCharm / WebStorm:"
echo "  - Python Interpreter: backend/venv/bin/python"
echo "  - Node.js: frontend/node_modules"
echo ""
echo "Note: To update dependencies after package.json or requirements.txt changes:"
echo "  1. Delete the local node_modules or venv directory"
echo "  2. Re-run this script"
echo ""
