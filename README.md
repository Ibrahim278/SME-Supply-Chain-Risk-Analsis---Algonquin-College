# SME Supply Chain Risk Analysis Platform

AI-powered ESG and modern slavery due diligence platform for SME supplier risk assessment.

## Prerequisites

- Python 3.11+
- Node.js 24 LTS
- Docker & Docker Compose
- Git

## Development Environment Options

Choose the setup that matches your workflow:

| Option | Best For | Prerequisites |
|--------|----------|---------------|
| **Option A: Hybrid** | Active development with IDE features | Python 3.11+, Node.js 24 LTS, Docker |
| **Option B: Fully Dockerized** | Quick start, CI/CD, non-developers | Docker only |

### Option A: Hybrid Development (Recommended for Developers)

Infrastructure runs in Docker, backend/frontend run locally for best hot-reload and IDE integration.

#### 1. Clone and Configure

```bash
git clone <repo-url> sme-platform
cd sme-platform
cp .env.example .env
# Edit .env with your values (especially LLM_API_KEY)
```

#### 2. Start Infrastructure

```bash
docker compose -f docker-compose.dev.yml up -d
docker compose -f docker-compose.dev.yml ps  # Verify healthy
```

#### 3. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt

# Install Playwright browser (for web scraping features)
playwright install chromium

alembic upgrade head
uvicorn app.main:app --reload
```

#### 4. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

#### 5. Worker Setup (optional)

```bash
cd backend && source venv/bin/activate
arq app.workers.worker.WorkerSettings
```

### Option B: Fully Dockerized Development

Entire stack runs in Docker. No local Python/Node.js required.

#### Prerequisites

- Docker & Docker Compose only

#### Quick Start

```bash
git clone <repo-url> sme-platform
cd sme-platform
cp .env.example .env
# Edit .env with your values

# Start everything
docker compose -f docker-compose.dev-full.yml up -d

# Run migrations
docker compose -f docker-compose.dev-full.yml exec backend alembic upgrade head
```

#### Common Commands (Option B)

```bash
# Start all services
docker compose -f docker-compose.dev-full.yml up -d

# Stop all services
docker compose -f docker-compose.dev-full.yml down

# View logs
docker compose -f docker-compose.dev-full.yml logs -f
docker compose -f docker-compose.dev-full.yml logs -f backend  # specific service

# Run backend tests
docker compose -f docker-compose.dev-full.yml exec backend pytest tests/ -v

# Run frontend tests
docker compose -f docker-compose.dev-full.yml exec frontend npm test

# Run migrations
docker compose -f docker-compose.dev-full.yml exec backend alembic upgrade head

# Access backend shell
docker compose -f docker-compose.dev-full.yml exec backend bash

# Start with worker (for background jobs)
docker compose -f docker-compose.dev-full.yml --profile worker up -d
```

#### IDE Support for Option B

For IDE intellisense without local Python/Node.js:

```bash
./scripts/ide-setup.sh
```

This creates local `node_modules` and `venv` directories for your IDE to use.

## Project Structure

```
sme-platform/
├── frontend/                    # Next.js application
│   ├── Dockerfile.dev           # Development container
│   └── src/                     # Application source
├── backend/                     # FastAPI application
│   ├── Dockerfile.dev           # Development container
│   ├── app/                     # Application source
│   └── alembic/                 # Database migrations
├── scripts/                     # Utility scripts
│   └── ide-setup.sh             # IDE support for Option B
├── docker-compose.yml           # Production stack
├── docker-compose.dev.yml       # Development infrastructure (Option A)
├── docker-compose.dev-full.yml  # Fully dockerized dev (Option B)
├── .pre-commit-config.yaml      # Pre-commit hooks configuration
├── .env.example                 # Environment template
└── README.md                    # This file
```

## Development Tooling

### Pre-commit Hooks

Pre-commit hooks are configured to run automatically on `git commit`:

```bash
# Install hooks (run once after cloning)
cd backend && source venv/bin/activate
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

### Backend Code Quality

```bash
cd backend && source venv/bin/activate

# Formatting with Black
black app/ tests/

# Linting with Ruff
ruff check app/ tests/
ruff check --fix app/ tests/  # Auto-fix issues

# Type checking with mypy
mypy app/

# Run tests with pytest
pytest tests/
pytest tests/ -v --tb=short  # Verbose output
```

### Frontend Code Quality

```bash
cd frontend

# ESLint
npm run lint

# Prettier formatting
npm run format:check  # Check only
npm run format        # Fix issues

# Testing with Vitest
npm test              # Run tests once
npm run test:watch    # Run tests in watch mode
npm run test:coverage # Run tests with coverage report

# Build check
npm run build
```

## Services

| Service   | Port  | Description           |
|-----------|-------|-----------------------|
| Frontend  | 3000  | Next.js web app       |
| Backend   | 8000  | FastAPI REST API      |
| PostgreSQL| 5432  | Database (pgvector)   |
| Redis     | 6379  | Cache & job queue     |
| MinIO     | 9000  | Object storage (S3)   |
| MinIO UI  | 9001  | MinIO console         |

## Full Stack (Docker)

```bash
# Development: Infrastructure only (backend/frontend run locally for hot reload)
docker compose -f docker-compose.dev.yml up -d

# Development: Everything in docker
docker compose -f docker-compose.dev-full.yml up -d

# Production mode (full containerized stack)
docker compose up -d
```

## Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
docker compose ps postgres

# View PostgreSQL logs
docker compose logs postgres
```

### Redis Connection Issues

```bash
# Test Redis connectivity
docker compose exec redis redis-cli ping
```

### MinIO Access Issues

```bash
# Access MinIO console at http://localhost:9001
# Default credentials: minioadmin / minioadmin
```

### Backend Not Starting

```bash
# Ensure virtual environment is activated
source backend/venv/bin/activate

# Check dependencies
pip install -r backend/requirements-dev.txt

# Verify database migrations
cd backend && alembic current
```

### Frontend Build Errors

```bash
# Clear Next.js cache
rm -rf frontend/.next
npm run dev
```

### Playwright Browser Issues

```bash
# Missing system dependencies (Linux)
sudo apt-get install libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
  libdrm2 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libpango-1.0-0 \
  libcairo2 libasound2 libatspi2.0-0

# Or use Playwright's installer
playwright install-deps chromium

# Reinstall browser binaries
playwright install chromium
```

### Docker Development (Option B) Issues

```bash
# Container not starting
docker compose -f docker-compose.dev-full.yml logs backend
docker compose -f docker-compose.dev-full.yml logs frontend

# Rebuild containers after Dockerfile changes
docker compose -f docker-compose.dev-full.yml build --no-cache
docker compose -f docker-compose.dev-full.yml up -d

# Hot-reload not working
# Ensure volumes are mounted correctly
docker compose -f docker-compose.dev-full.yml exec backend ls -la /app/app
docker compose -f docker-compose.dev-full.yml exec frontend ls -la /app/src

# Reset everything
docker compose -f docker-compose.dev-full.yml down -v
docker compose -f docker-compose.dev-full.yml up -d --build

# Port already in use
docker ps  # Check for conflicting containers
docker stop <container_id>
```

### Performance on macOS/Windows

Docker volume mounts can be slow on macOS/Windows. For best performance:
- Use Option A (Hybrid) for active development
- Use Option B for testing or running the full stack

## Environment Variables

See `.env.example` for all required environment variables with descriptions.

## License

Proprietary - All rights reserved.
