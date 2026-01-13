# Epic Technical Specification: Foundation & Project Setup

Date: 2025-11-28
Author: Master
Epic ID: 1
Status: Draft

---

## Overview

Epic 1 establishes the technical foundation for the SME Supply Chain Risk Analysis platform. This foundational epic delivers a fully containerized development environment with a Next.js frontend, FastAPI backend, PostgreSQL database with pgvector, Redis cache, and MinIO file storage. All subsequent development depends on this infrastructure being correctly configured and operational.

This epic contains no user-facing features but enables all 96 functional requirements by providing the runtime environment, project structure, and development tooling.

## Objectives and Scope

### In Scope

- Monorepo structure with `/frontend` and `/backend` directories
- FastAPI backend with async support, health endpoints, and OpenAPI docs
- Next.js 15 frontend with App Router, TypeScript, Tailwind CSS, and shadcn/ui
- PostgreSQL 16 with pgvector extension in Docker
- Redis 7 for caching and job queue backing
- MinIO for S3-compatible file storage
- Docker Compose configurations (production and development)
- Alembic migrations infrastructure
- Development environment documentation
- Code quality tooling (pytest, black, ruff, mypy, ESLint, Prettier)

### Out of Scope

- User authentication implementation (Epic 2)
- Business logic or API endpoints beyond health checks
- Production deployment scripts
- CI/CD pipeline configuration
- Actual data models (beyond base model pattern)

## System Architecture Alignment

This epic implements the foundational layer of the architecture document:

| Architecture Component | Implementation in Epic 1 |
|----------------------|--------------------------|
| Backend Framework | FastAPI 0.115.x with uvicorn |
| Frontend Framework | Next.js 15.0.3 with App Router |
| Database | PostgreSQL 16 via pgvector Docker image |
| Vector Store | pgvector 0.7.x extension enabled |
| Cache | Redis 7.x container |
| File Storage | MinIO container with S3 API |
| ORM | SQLAlchemy 2.x with asyncpg driver |
| Migrations | Alembic with async support |

**Constraints:**
- All services must run in Docker for development parity
- Backend must use async patterns throughout (asyncpg, async sessions)
- Frontend must use strict TypeScript configuration
- Project structure must match Architecture doc layout exactly

## Detailed Design

### Services and Modules

| Service/Module | Responsibility | Inputs | Outputs | Owner |
|---------------|----------------|--------|---------|-------|
| `frontend/` | Next.js application container | HTTP requests | HTML/JS/CSS responses | Frontend dev |
| `backend/` | FastAPI application container | HTTP requests | JSON responses | Backend dev |
| `postgres` | Primary data store | SQL queries | Query results | Infrastructure |
| `redis` | Cache and queue backing | Key-value ops | Cached data | Infrastructure |
| `minio` | Object storage | S3 API calls | File data | Infrastructure |
| `worker` | ARQ background processor | Job queue | Task completion | Backend dev |

### Directory Structure

```
sme-platform/
├── frontend/
│   ├── src/
│   │   ├── app/              # App Router pages
│   │   ├── components/
│   │   │   └── ui/           # shadcn/ui components
│   │   ├── lib/              # Utilities
│   │   ├── hooks/            # Custom React hooks
│   │   └── stores/           # Zustand stores
│   ├── public/
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI entry point
│   │   ├── core/
│   │   │   ├── config.py     # pydantic-settings config
│   │   │   └── logging.py    # structlog configuration
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── router.py # API router stub
│   │   ├── models/
│   │   │   └── base.py       # Base SQLAlchemy model
│   │   ├── schemas/
│   │   │   └── base.py       # Response envelope schemas
│   │   ├── db/
│   │   │   ├── session.py    # Async session factory
│   │   │   └── init_db.py    # DB initialization
│   │   └── workers/
│   │       └── worker.py     # ARQ worker stub
│   ├── alembic/
│   │   ├── versions/
│   │   └── env.py
│   ├── tests/
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   └── Dockerfile
│
├── docker-compose.yml        # Production stack
├── docker-compose.dev.yml    # Development overrides
├── .env.example
├── .gitignore
└── README.md
```

### Data Models and Contracts

**Base Model Pattern (app/models/base.py):**

```python
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4
from datetime import datetime

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)  # Soft delete
```

**Response Envelope Schema (app/schemas/base.py):**

```python
from pydantic import BaseModel
from typing import TypeVar, Generic, Optional, List, Any

T = TypeVar('T')

class Meta(BaseModel):
    request_id: str
    total: Optional[int] = None
    limit: Optional[int] = None
    offset: Optional[int] = None

class SuccessResponse(BaseModel, Generic[T]):
    data: T
    meta: Meta

class ErrorDetail(BaseModel):
    field: Optional[str] = None
    message: str

class ErrorResponse(BaseModel):
    error: dict  # code, message, details
```

### APIs and Interfaces

**Health Check Endpoint:**

| Method | Path | Request | Response | Status Codes |
|--------|------|---------|----------|--------------|
| GET | `/health` | None | `{"status": "ok"}` | 200 |
| GET | `/docs` | None | OpenAPI UI | 200 |
| GET | `/openapi.json` | None | OpenAPI spec | 200 |

**FastAPI App Entry (app/main.py):**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="SME Supply Chain Risk Analysis API",
    version="0.1.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
```

### Workflows and Sequencing

**Development Environment Setup Sequence:**

```
1. Clone repository
2. Copy .env.example → .env (configure values)
3. docker compose -f docker-compose.dev.yml up -d postgres redis minio
4. cd backend && python -m venv venv && source venv/bin/activate
5. pip install -r requirements-dev.txt
6. alembic upgrade head
7. uvicorn app.main:app --reload (port 8000)
8. cd frontend && npm install
9. npm run dev (port 3000)
```

**Docker Compose Startup Order:**
```
postgres → redis → minio → backend → frontend → worker
```

## Non-Functional Requirements

### Performance

| Metric | Target | Measurement |
|--------|--------|-------------|
| Backend cold start | < 5s | Time from `docker compose up` to healthy |
| Frontend dev server start | < 10s | Time to first page render |
| Database connection pool | 20 connections | asyncpg pool size |
| Health endpoint latency | < 50ms | Response time under load |

### Security

| Requirement | Implementation |
|-------------|----------------|
| No secrets in code | All secrets via environment variables |
| .env in .gitignore | Prevent accidental secret commits |
| CORS configured | Restrict to known origins |
| Strict TypeScript | Catch type errors at compile time |

**Environment Variables (NFR8 - encrypted at rest in production):**

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db

# Redis
REDIS_URL=redis://host:6379

# MinIO
MINIO_URL=http://host:9000
MINIO_ACCESS_KEY=key
MINIO_SECRET_KEY=secret

# LLM Configuration (placeholder for future epics)
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o
LLM_API_KEY=sk-...

# JWT (placeholder for Epic 2)
JWT_SECRET=secret
JWT_ALGORITHM=HS256
```

### Reliability/Availability

| Requirement | Implementation |
|-------------|----------------|
| Container restart policy | `restart: unless-stopped` |
| Database persistence | Named volume `postgres_data` |
| Redis persistence | Named volume `redis_data` |
| MinIO persistence | Named volume `minio_data` |

### Observability

| Signal | Implementation |
|--------|----------------|
| Application logs | structlog with JSON format |
| Request logging | FastAPI middleware with request_id |
| Container logs | Docker stdout/stderr |

**Logging Configuration (app/core/logging.py):**

```python
import structlog

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.BoundLogger,
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
)
```

## Dependencies and Integrations

### Backend Dependencies (requirements.txt)

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.115.x | Web framework |
| uvicorn | 0.32.x | ASGI server |
| sqlalchemy | 2.0.x | ORM |
| asyncpg | 0.30.x | PostgreSQL async driver |
| alembic | 1.14.x | Database migrations |
| pydantic-settings | 2.6.x | Configuration management |
| structlog | 24.x | Structured logging |
| redis | 5.x | Redis client |
| arq | 0.26.x | Async job queue |

### Backend Dev Dependencies (requirements-dev.txt)

| Package | Version | Purpose |
|---------|---------|---------|
| pytest | 8.x | Testing |
| pytest-asyncio | 0.24.x | Async test support |
| black | 24.x | Code formatting |
| ruff | 0.8.x | Linting |
| mypy | 1.13.x | Type checking |

### Frontend Dependencies (package.json)

| Package | Version | Purpose |
|---------|---------|---------|
| next | 15.0.3 | React framework |
| react | 19.x | UI library |
| typescript | 5.x | Type safety |
| tailwindcss | 3.4.x | CSS framework |
| @radix-ui/* | latest | shadcn/ui primitives |

### Docker Images

| Image | Version | Purpose |
|-------|---------|---------|
| pgvector/pgvector | pg16 | PostgreSQL with vector support |
| redis | 7-alpine | Cache and queue |
| minio/minio | RELEASE.2024-11 | Object storage |
| python | 3.12-slim | Backend runtime |
| node | 20-alpine | Frontend runtime |

## Acceptance Criteria (Authoritative)

| # | Criterion | Testable Statement |
|---|-----------|-------------------|
| AC1 | Monorepo structure exists | `/frontend` and `/backend` directories present with correct structure |
| AC2 | Backend starts successfully | `uvicorn app.main:app --reload` starts on port 8000 |
| AC3 | Health endpoint responds | `GET /health` returns `{"status": "ok"}` with 200 |
| AC4 | OpenAPI docs available | `GET /docs` renders Swagger UI |
| AC5 | Frontend starts successfully | `npm run dev` starts on port 3000 |
| AC6 | Frontend renders | Home page shows shadcn/ui styled content |
| AC7 | PostgreSQL container runs | `docker compose up postgres` succeeds, accepts connections |
| AC8 | pgvector enabled | `CREATE EXTENSION vector;` succeeds |
| AC9 | Redis container runs | `docker compose up redis` succeeds, accepts connections |
| AC10 | MinIO container runs | Console accessible on port 9001 |
| AC11 | Alembic configured | `alembic upgrade head` runs without error |
| AC12 | Base model migration | Initial migration creates base table structure pattern |
| AC13 | Dev tools configured | `black`, `ruff`, `mypy` run on backend; `eslint`, `prettier` on frontend |
| AC14 | .env.example complete | All required environment variables documented |
| AC15 | README setup works | Following README instructions results in running system |
| AC16 | .gitignore complete | Excludes `node_modules/`, `venv/`, `.env`, `__pycache__/`, `.next/` |

## Traceability Mapping

| AC | Spec Section | Component/File | Test Approach |
|----|--------------|----------------|---------------|
| AC1 | Detailed Design | Directory structure | Manual inspection |
| AC2 | APIs/Interfaces | `app/main.py` | Run command, check stdout |
| AC3 | APIs/Interfaces | `app/main.py` | HTTP GET request |
| AC4 | APIs/Interfaces | FastAPI auto-docs | Browser navigation |
| AC5 | Workflows | `frontend/package.json` | Run command, check stdout |
| AC6 | Dependencies | `src/app/page.tsx` | Visual inspection |
| AC7 | Services/Modules | `docker-compose.yml` | Docker logs, psql connect |
| AC8 | Architecture Alignment | pgvector image | SQL command |
| AC9 | Services/Modules | `docker-compose.yml` | Docker logs, redis-cli |
| AC10 | Services/Modules | `docker-compose.yml` | Browser to port 9001 |
| AC11 | Workflows | `alembic/` | Run migration command |
| AC12 | Data Models | `app/models/base.py` | Inspect generated SQL |
| AC13 | NFRs | Config files | Run lint/format commands |
| AC14 | Security | `.env.example` | Compare to required vars list |
| AC15 | Workflows | `README.md` | Fresh clone test |
| AC16 | Security | `.gitignore` | git status after install |

## Risks, Assumptions, Open Questions

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Version incompatibilities between dependencies | Medium | High | Pin exact versions in requirements.txt and package.json |
| Docker networking issues on different OSes | Low | Medium | Document platform-specific workarounds in README |
| pgvector extension not loading | Low | High | Use official pgvector image; test extension create on startup |

### Assumptions

| Assumption | Rationale |
|------------|-----------|
| Developers have Docker installed | Standard development prerequisite |
| Python 3.12+ available | Required for modern async features |
| Node.js 20 LTS available | Required for Next.js 15 |
| Unix-like environment for shell commands | Windows users can use WSL2 |

### Open Questions

| Question | Impact | Proposed Resolution |
|----------|--------|---------------------|
| Should we include pre-commit hooks in Epic 1? | Code quality automation | Yes, add pre-commit config with black/ruff |
| Docker Compose version requirements? | Compatibility | Document minimum Docker Compose v2.20+ |

## Test Strategy Summary

### Test Levels

| Level | Scope | Framework |
|-------|-------|-----------|
| Unit | Individual functions | pytest (backend), Jest (frontend) |
| Integration | Container connectivity | Docker Compose health checks |
| Smoke | End-to-end startup | Manual verification script |

### Test Coverage

| AC | Test Type | Description |
|----|-----------|-------------|
| AC1-AC3 | Smoke | Backend startup and health check |
| AC4 | Smoke | OpenAPI docs render |
| AC5-AC6 | Smoke | Frontend startup and render |
| AC7-AC10 | Integration | Docker containers start and accept connections |
| AC11-AC12 | Integration | Alembic migrations run successfully |
| AC13 | Unit | Lint/format commands exit 0 on clean code |

### Edge Cases

- Backend starts without database (should fail gracefully with clear error)
- Frontend starts without backend (should show connection error, not crash)
- Docker Compose partial startup (dependency ordering verified)
