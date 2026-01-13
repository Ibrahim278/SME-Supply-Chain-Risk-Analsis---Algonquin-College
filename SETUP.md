# SME Supply Chain Risk Analysis - Local Development Setup

Complete guide for setting up the SME Supply Chain Risk Analysis platform for local development.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Clone and Environment Setup](#initial-clone-and-environment-setup)
3. [Infrastructure Setup](#infrastructure-setup)
4. [Backend Setup](#backend-setup)
5. [Frontend Setup](#frontend-setup)
6. [Development Tools](#development-tools)
7. [Verification Steps](#verification-steps)
8. [Service URLs and Ports](#service-urls-and-ports)
9. [Common Issues and Troubleshooting](#common-issues-and-troubleshooting)

---

## Prerequisites

Ensure you have the following installed on your system:

| Tool | Version | Verification Command | Purpose |
|------|---------|---------------------|---------|
| Python | 3.11+ | `python --version` | Backend FastAPI application |
| Node.js | 24 LTS | `node --version` | Frontend Next.js application |
| npm | 10+ | `npm --version` | Frontend package management |
| Docker | 24+ | `docker --version` | Infrastructure services |
| Docker Compose | 2.20+ | `docker compose version` | Multi-container orchestration |
| Git | 2.30+ | `git --version` | Version control |

### Installation Links

- **Python 3.11+**: [python.org/downloads](https://www.python.org/downloads/)
- **Node.js 24 LTS**: [nodejs.org](https://nodejs.org/)
- **Docker Desktop**: [docker.com/get-started](https://www.docker.com/get-started)
- **Git**: [git-scm.com](https://git-scm.com/)

---

## Initial Clone and Environment Setup

### 1. Clone the Repository

```bash
git clone <repository-url> sme-platform
cd sme-platform
```

### 2. Create Environment File

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

### 3. Configure Environment Variables

Edit `.env` and set the following required values:

```bash
# Database (default values work for local development)
DATABASE_URL=postgresql+asyncpg://sme:password@localhost:5432/sme
DB_PASSWORD=password

# Redis (default works for local development)
REDIS_URL=redis://localhost:6379

# MinIO Object Storage (default works for local development)
MINIO_URL=http://localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_USER=minioadmin
MINIO_PASSWORD=minioadmin
MINIO_BUCKET_NAME=sme-files

# LLM Configuration (REQUIRED - add your API key)
LLM_PROVIDER=openai  # Options: openai | anthropic | google
LLM_MODEL=gpt-4o     # openai: gpt-4o, gpt-4o-mini
                     # anthropic: claude-sonnet-4-20250514, claude-3-5-haiku-20241022
                     # google: gemini-1.5-pro, gemini-1.5-flash
LLM_API_KEY=sk-...   # ⚠️ ADD YOUR API KEY HERE

# JWT Authentication (generate a secure random string for production)
JWT_SECRET=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-nextauth-secret-change-in-production

# Development Settings
DEBUG=true
LOG_LEVEL=DEBUG
```

**Important**: You must set `LLM_API_KEY` with a valid API key from your chosen provider (OpenAI, Anthropic, or Google).

---

## Infrastructure Setup

The platform uses Docker Compose to run PostgreSQL, Redis, and MinIO for local development.

### 1. Start Infrastructure Services

```bash
# Start PostgreSQL, Redis, and MinIO in detached mode
docker compose -f docker-compose.dev.yml up -d
```

Expected output:
```
✔ Container sme-postgres-dev  Started
✔ Container sme-redis-dev     Started
✔ Container sme-minio-dev     Started
```

### 2. Verify Service Health

```bash
docker compose -f docker-compose.dev.yml ps
```

All services should show status `Up (healthy)`:

```
NAME                 STATUS              PORTS
sme-postgres-dev     Up (healthy)        0.0.0.0:5432->5432/tcp
sme-redis-dev        Up (healthy)        0.0.0.0:6379->6379/tcp
sme-minio-dev        Up (healthy)        0.0.0.0:9000->9000/tcp, 0.0.0.0:9001->9001/tcp
```

### 3. Default Credentials

| Service | Username | Password | Notes |
|---------|----------|----------|-------|
| PostgreSQL | `sme` | `password` | Can be changed via `DB_PASSWORD` in `.env` |
| Redis | (none) | (none) | No authentication by default |
| MinIO | `minioadmin` | `minioadmin` | Access UI at http://localhost:9001 |

### 4. Infrastructure Architecture

- **PostgreSQL 16** with **pgvector** extension for vector embeddings
- **Redis 7** for caching and job queue (arq)
- **MinIO** (S3-compatible) for file storage

---

## Backend Setup

### 1. Create Python Virtual Environment

```bash
cd backend
python -m venv venv
```

### 2. Activate Virtual Environment

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

You should see `(venv)` prefix in your terminal prompt.

### 3. Install Dependencies

```bash
# Install all production and development dependencies
pip install -r requirements-dev.txt
```

This installs:
- **Production dependencies**: FastAPI, SQLAlchemy, Alembic, Redis, aioboto3, Playwright, etc.
- **Development tools**: pytest, black, ruff, mypy, pre-commit

### 4. Install Playwright Browser

Playwright is used for web scraping of JS-rendered supplier websites. Install Chromium browser:

```bash
# Install Chromium browser binaries (~160MB)
playwright install chromium
```

Expected output:
```
Downloading Chromium 131.0.6778.33 (playwright build v1148)
...
Chromium 131.0.6778.33 (playwright build v1148) downloaded
```

**Note**: If you see warnings about missing system dependencies, run:
```bash
# Linux only - install system dependencies
playwright install-deps chromium
# Or manually: sudo apt-get install libnss3 libatk1.0-0 libatk-bridge2.0-0 ...
```

### 5. Run Database Migrations

```bash
# Apply all database migrations
alembic upgrade head
```

Expected output:
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 78b576fc3930, initial_base_model
```

Verify migration status:
```bash
alembic current
```

Output should show:
```
78b576fc3930 (head)
```

### 6. Start Backend Server

```bash
uvicorn app.main:app --reload
```

Expected output:
```
INFO:     Will watch for changes in these directories: ['/path/to/backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 7. Verify Backend Health

Open in browser or use curl:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status":"ok"}
```

Visit API documentation at: http://localhost:8000/docs

---

## Frontend Setup

Open a **new terminal window** (keep backend running).

### 1. Navigate to Frontend Directory

```bash
cd frontend  # from project root
```

### 2. Install Node.js Dependencies

```bash
npm install
```

This installs:
- **Next.js 15** with React 19 RC
- **shadcn/ui** components (Radix UI primitives)
- **TanStack Query** for API data fetching
- **Zustand** for state management
- **Tailwind CSS** for styling
- **Development tools**: ESLint, Prettier, TypeScript

### 3. Create Frontend Environment File (Optional)

```bash
cp .env.example .env.local
```

Edit `.env.local` if you need to override defaults:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-nextauth-secret
```

### 4. Start Frontend Development Server

```bash
npm run dev
```

Expected output:
```
  ▲ Next.js 15.0.3
  - Local:        http://localhost:3000
  - Environments: .env.local

 ✓ Starting...
 ✓ Ready in 2.5s
```

### 5. Verify Frontend

Open http://localhost:3000 in your browser. You should see the application landing page.

---

## Development Tools

### Pre-commit Hooks Setup

Pre-commit hooks automatically format and lint code before each commit.

#### Install Hooks (One-time Setup)

```bash
# From project root, with backend venv activated
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
pre-commit install
```

Expected output:
```
pre-commit installed at .git/hooks/pre-commit
```

#### Run Hooks Manually

```bash
# From project root
pre-commit run --all-files
```

This runs:
- Trailing whitespace removal
- End-of-file fixer
- YAML/JSON validation
- Large file check
- Merge conflict detection
- Private key detection
- **Black** (Python formatting)
- **Ruff** (Python linting)
- **mypy** (Python type checking)
- **ESLint** (JavaScript/TypeScript linting)
- **Prettier** (JavaScript/TypeScript formatting)

### Backend Development Tools

All commands run from `backend/` directory with virtual environment activated.

#### pytest - Test Runner

```bash
# Run all tests
pytest

# Verbose output with short traceback
pytest -v --tb=short

# Run specific test file
pytest tests/test_health.py

# Run tests matching pattern
pytest -k "test_health"

# Show print statements
pytest -s

# Run with coverage
pytest --cov=app --cov-report=html
```

Configuration in `pyproject.toml`:
- Test discovery: `tests/test_*.py`
- Async support: auto-detected
- Python version: 3.12+

#### black - Code Formatter

```bash
# Check formatting (no changes)
black --check app/ tests/

# Format code
black app/ tests/

# Show diff of changes
black --diff app/ tests/
```

Configuration in `pyproject.toml`:
- Line length: 88 characters
- Target: Python 3.12

#### ruff - Linter

```bash
# Check for issues
ruff check app/ tests/

# Fix auto-fixable issues
ruff check --fix app/ tests/

# Show specific rule violations
ruff check --select E,F,I,W app/
```

Configuration in `pyproject.toml`:
- Rules: pycodestyle (E,W), pyflakes (F), isort (I)
- Line length: 88 (matches black)

#### mypy - Type Checker

```bash
# Type check application code
mypy app/

# Check specific file
mypy app/main.py

# Show error codes
mypy --show-error-codes app/
```

Configuration in `pyproject.toml`:
- Strict mode enabled
- Ignores: alembic/, venv/, tests/
- Relaxed typing for legacy modules: storage, logging, redis

### Frontend Development Tools

All commands run from `frontend/` directory.

#### ESLint - JavaScript/TypeScript Linter

```bash
# Run ESLint
npm run lint

# Fix auto-fixable issues
npm run lint -- --fix
```

Configuration in `.eslintrc.json`:
- Next.js recommended rules
- Prettier integration

#### Prettier - Code Formatter

```bash
# Check formatting
npm run format:check

# Format code
npm run format
```

Configuration in `.prettierrc`:
- Formats: TypeScript, JavaScript, JSON, CSS, Markdown
- Integrated with ESLint

#### Vitest - Test Runner

```bash
# Run all tests once
npm test

# Run tests in watch mode (re-runs on file changes)
npm run test:watch

# Run tests with coverage report
npm run test:coverage

# Run specific test file
npm test -- src/components/ui/__tests__/button.test.tsx
```

Configuration in `vitest.config.ts`:
- Environment: jsdom (simulates browser DOM)
- Test files: `src/**/*.{test,spec}.{ts,tsx}`
- Setup: `vitest.setup.ts` (jest-dom matchers)
- Path alias: `@/` maps to `src/`

#### Build Check

```bash
# Check production build
npm run build

# Start production server
npm run start
```

---

## Verification Steps

### Complete System Check

Run these commands to verify everything is working:

#### 1. Infrastructure Health

```bash
docker compose -f docker-compose.dev.yml ps
```
All services should show `Up (healthy)`.

#### 2. Backend Health

```bash
curl http://localhost:8000/health
```
Response: `{"status":"ok"}`

#### 3. Database Connection

```bash
cd backend
source venv/bin/activate
alembic current
```
Should show migration: `78b576fc3930 (head)`

#### 4. Redis Connection

```bash
docker compose -f docker-compose.dev.yml exec redis redis-cli ping
```
Response: `PONG`

#### 5. MinIO Access

Open http://localhost:9001 in browser.
Login: `minioadmin` / `minioadmin`

#### 6. Backend Tests

```bash
cd backend
source venv/bin/activate
pytest
```
All tests should pass.

#### 7. Frontend Tests

```bash
cd frontend
npm test
```
All tests should pass.

#### 8. Frontend Build

```bash
cd frontend
npm run lint
npm run format:check
```
No errors should be reported.

#### 9. Pre-commit Hooks

```bash
# From project root
pre-commit run --all-files
```
All hooks should pass.

---

## Service URLs and Ports

| Service | URL | Port | Description |
|---------|-----|------|-------------|
| **Frontend** | http://localhost:3000 | 3000 | Next.js web application |
| **Backend API** | http://localhost:8000 | 8000 | FastAPI REST API |
| **API Docs (Swagger)** | http://localhost:8000/docs | 8000 | Interactive API documentation |
| **API Docs (ReDoc)** | http://localhost:8000/redoc | 8000 | Alternative API docs |
| **PostgreSQL** | localhost:5432 | 5432 | Database (pgvector) |
| **Redis** | localhost:6379 | 6379 | Cache & job queue |
| **MinIO API** | http://localhost:9000 | 9000 | S3-compatible object storage |
| **MinIO Console** | http://localhost:9001 | 9001 | MinIO admin interface |

### Direct Database Access

Connect to PostgreSQL using any database client:

```bash
# Using psql command-line
docker compose -f docker-compose.dev.yml exec postgres psql -U sme -d sme

# Connection string for database clients (DBeaver, pgAdmin, etc.)
postgresql://sme:password@localhost:5432/sme
```

Common psql commands:
```sql
\l              -- List databases
\dt             -- List tables
\d table_name   -- Describe table
\q              -- Quit
```

### Direct Redis Access

```bash
# Redis CLI
docker compose -f docker-compose.dev.yml exec redis redis-cli

# Common commands
PING            # Test connection
KEYS *          # List all keys
GET key         # Get value
FLUSHDB         # Clear current database
```

---

## Common Issues and Troubleshooting

### Database Connection Issues

#### Symptom: "connection refused" or "could not connect to server"

**Solution 1: Check PostgreSQL is running**
```bash
docker compose -f docker-compose.dev.yml ps postgres
```
Should show `Up (healthy)`. If not:
```bash
docker compose -f docker-compose.dev.yml up -d postgres
docker compose -f docker-compose.dev.yml logs postgres
```

**Solution 2: Verify DATABASE_URL**
Ensure `.env` has correct connection string:
```
DATABASE_URL=postgresql+asyncpg://sme:password@localhost:5432/sme
```

**Solution 3: Wait for PostgreSQL to be ready**
PostgreSQL takes 5-10 seconds to start. Check health:
```bash
docker compose -f docker-compose.dev.yml exec postgres pg_isready -U sme -d sme
```

**Solution 4: Reset database container**
```bash
docker compose -f docker-compose.dev.yml down -v
docker compose -f docker-compose.dev.yml up -d postgres
```
⚠️ Warning: `-v` removes volumes and deletes all data.

#### Symptom: "relation does not exist" or missing tables

**Solution: Run migrations**
```bash
cd backend
source venv/bin/activate
alembic upgrade head
```

**Solution 2: Check migration status**
```bash
alembic current
alembic history
```

**Solution 3: Reset and re-run migrations**
```bash
alembic downgrade base
alembic upgrade head
```

---

### Redis Connection Issues

#### Symptom: "Connection refused" to Redis

**Solution 1: Check Redis is running**
```bash
docker compose -f docker-compose.dev.yml ps redis
```

**Solution 2: Test Redis connectivity**
```bash
docker compose -f docker-compose.dev.yml exec redis redis-cli ping
```
Expected: `PONG`

**Solution 3: Verify REDIS_URL**
Ensure `.env` has:
```
REDIS_URL=redis://localhost:6379
```

**Solution 4: Restart Redis**
```bash
docker compose -f docker-compose.dev.yml restart redis
docker compose -f docker-compose.dev.yml logs redis
```

---

### MinIO Connection Issues

#### Symptom: Cannot access MinIO console or API

**Solution 1: Check MinIO is running**
```bash
docker compose -f docker-compose.dev.yml ps minio
```

**Solution 2: Verify MinIO credentials**
Console login: http://localhost:9001
- Username: `minioadmin`
- Password: `minioadmin`

**Solution 3: Check MinIO logs**
```bash
docker compose -f docker-compose.dev.yml logs minio
```

**Solution 4: Test MinIO health**
```bash
curl http://localhost:9000/minio/health/live
```

#### Symptom: "Bucket does not exist" error

**Solution: Create bucket manually**
1. Open http://localhost:9001
2. Login with `minioadmin` / `minioadmin`
3. Click "Buckets" → "Create Bucket"
4. Name: `sme-files`
5. Click "Create"

---

### Port Conflicts

#### Symptom: "port is already allocated" or "address already in use"

**Solution 1: Check what's using the port**
```bash
# Linux/macOS
lsof -i :5432  # or :6379, :9000, :9001
sudo lsof -i :5432

# Windows (PowerShell)
netstat -ano | findstr :5432
```

**Solution 2: Stop conflicting service**
```bash
# Stop existing PostgreSQL service
sudo systemctl stop postgresql  # Linux
brew services stop postgresql   # macOS
```

**Solution 3: Change port in docker-compose.dev.yml**
Edit `docker-compose.dev.yml`:
```yaml
ports:
  - "5433:5432"  # Use host port 5433 instead
```
Update `.env`:
```
DATABASE_URL=postgresql+asyncpg://sme:password@localhost:5433/sme
```

---

### Backend Not Starting

#### Symptom: Import errors or module not found

**Solution 1: Ensure virtual environment is activated**
```bash
cd backend
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```
Check: `(venv)` should appear in prompt.

**Solution 2: Reinstall dependencies**
```bash
pip install --upgrade pip
pip install -r requirements-dev.txt
```

**Solution 3: Check Python version**
```bash
python --version  # Should be 3.11 or higher
```

#### Symptom: "No module named 'app'"

**Solution: Run uvicorn from backend directory**
```bash
cd backend
uvicorn app.main:app --reload
```

#### Symptom: Alembic migration errors

**Solution 1: Check database connection**
```bash
alembic current
```

**Solution 2: Review migration history**
```bash
alembic history
```

**Solution 3: Force migration to latest**
```bash
alembic stamp head
alembic upgrade head
```

---

### Playwright Browser Issues

#### Symptom: "Host system is missing dependencies to run browsers"

**Solution 1: Install system dependencies (Linux)**
```bash
playwright install-deps chromium
```

Or manually:
```bash
sudo apt-get install libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
  libdrm2 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libpango-1.0-0 \
  libcairo2 libasound2 libatspi2.0-0
```

**Solution 2: Reinstall browser**
```bash
playwright install chromium
```

#### Symptom: "Executable doesn't exist" or browser not found

**Solution: Reinstall Playwright and browsers**
```bash
pip install --force-reinstall playwright
playwright install chromium
```

---

### Frontend Build Errors

#### Symptom: "Module not found" or dependency errors

**Solution 1: Clear node_modules and reinstall**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Solution 2: Clear Next.js cache**
```bash
rm -rf .next
npm run dev
```

**Solution 3: Check Node.js version**
```bash
node --version  # Should be 20.x
```

**Solution 4: Use npm clean install**
```bash
npm ci  # Clean install from package-lock.json
```

#### Symptom: "Failed to compile" errors

**Solution 1: Check for TypeScript errors**
```bash
npm run lint
```

**Solution 2: Clear cache and rebuild**
```bash
rm -rf .next
npm run build
```

---

### Pre-commit Hook Failures

#### Symptom: Pre-commit hooks fail on commit

**Solution 1: Run hooks manually to see errors**
```bash
pre-commit run --all-files
```

**Solution 2: Format code before committing**
```bash
# Backend
cd backend
source venv/bin/activate
black app/ tests/
ruff check --fix app/ tests/

# Frontend
cd frontend
npm run format
npm run lint -- --fix
```

**Solution 3: Update pre-commit hooks**
```bash
pre-commit autoupdate
pre-commit install --install-hooks
```

**Solution 4: Skip hooks temporarily (not recommended)**
```bash
git commit -m "message" --no-verify
```

---

### Environment Variable Issues

#### Symptom: "LLM_API_KEY not found" or authentication errors

**Solution: Verify .env file**
```bash
# Check .env exists
ls -la .env

# Verify key is set
grep LLM_API_KEY .env
```

Ensure no extra spaces:
```bash
LLM_API_KEY=sk-abc123...  # ✓ Correct
LLM_API_KEY = sk-abc123... # ✗ Extra spaces
```

**Solution 2: Restart backend after changing .env**
Stop uvicorn (Ctrl+C) and start again:
```bash
uvicorn app.main:app --reload
```

---

### Docker Issues

#### Symptom: Permission denied errors

**Solution: Use sudo or add user to docker group**
```bash
# Linux - add user to docker group (logout/login required)
sudo usermod -aG docker $USER

# Or use sudo with docker commands
sudo docker compose -f docker-compose.dev.yml up -d
```

#### Symptom: "docker daemon not running"

**Solution: Start Docker Desktop**
- macOS/Windows: Open Docker Desktop application
- Linux: `sudo systemctl start docker`

#### Symptom: Out of disk space

**Solution: Clean up Docker resources**
```bash
# Remove unused containers, networks, images
docker system prune -a

# Remove volumes (⚠️ deletes data)
docker volume prune
```

---

### General Debugging Tips

#### Check All Services Status

```bash
# Infrastructure
docker compose -f docker-compose.dev.yml ps

# Backend
curl http://localhost:8000/health

# Frontend
curl http://localhost:3000
```

#### View Service Logs

```bash
# Docker services
docker compose -f docker-compose.dev.yml logs -f postgres
docker compose -f docker-compose.dev.yml logs -f redis
docker compose -f docker-compose.dev.yml logs -f minio

# Backend logs (in uvicorn terminal)
# Frontend logs (in npm terminal)
```

#### Reset Everything

```bash
# Stop all services
docker compose -f docker-compose.dev.yml down -v

# Clear caches
rm -rf backend/.venv backend/__pycache__ backend/.pytest_cache
rm -rf frontend/.next frontend/node_modules

# Restart from scratch
docker compose -f docker-compose.dev.yml up -d
# ... then follow backend and frontend setup again
```

---

## Next Steps

After completing setup:

1. Review [README.md](./README.md) for project overview
2. Check [docs/architecture.md](./docs/architecture.md) for architecture details
3. Read [docs/epics.md](./docs/epics.md) for feature roadmap
4. Explore API documentation at http://localhost:8000/docs
5. Review sprint artifacts in [docs/sprint-artifacts/](./docs/sprint-artifacts/)

---

## Getting Help

If you encounter issues not covered in this guide:

1. Check service logs: `docker compose -f docker-compose.dev.yml logs [service]`
2. Review story documentation in `docs/sprint-artifacts/`
3. Search for error messages in GitHub issues
4. Contact the development team

---

**Last Updated**: 2025-12-01
**Platform Version**: 0.1.0
