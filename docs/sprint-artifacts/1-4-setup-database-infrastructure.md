# Story 1.4: Setup Database Infrastructure

Status: done

## Story

As a **developer**,
I want PostgreSQL with pgvector running in Docker,
so that I can persist application data and evidence embeddings.

## Acceptance Criteria

1. **AC1:** PostgreSQL 16.x container starts via `docker compose up postgres`
2. **AC2:** Database name is `sme` with user `sme`
3. **AC3:** pgvector extension is enabled and functional
4. **AC4:** Persistent volume configured for data
5. **AC5:** Port 5432 exposed to host
6. **AC6:** Alembic is configured with async support
7. **AC7:** Alembic can connect to database and run migrations
8. **AC8:** Initial migration creates base model pattern (id, created_at, updated_at, deleted_at)
9. **AC9:** Health check configured on postgres container

## Tasks / Subtasks

- [x] **Task 1: Verify PostgreSQL container configuration** (AC: 1, 2, 4, 5, 9)
  - [x] Verify docker-compose.yml uses `pgvector/pgvector:pg16` image
  - [x] Verify environment variables: POSTGRES_DB=sme, POSTGRES_USER=sme
  - [x] Verify volume mount for persistence
  - [x] Verify port 5432 mapping
  - [x] Verify health check configuration
  - [x] Test: `sudo docker compose up postgres -d` starts successfully

- [x] **Task 2: Verify pgvector extension** (AC: 3)
  - [x] Connect to database and run `CREATE EXTENSION IF NOT EXISTS vector;`
  - [x] Verify: `SELECT * FROM pg_extension WHERE extname = 'vector';` returns row
  - [x] Test vector operations work (create table with vector column)

- [x] **Task 3: Install Alembic and asyncpg** (AC: 6)
  - [x] Add to backend requirements.txt:
    - `alembic>=1.14.0`
    - `asyncpg>=0.30.0`
  - [x] Install dependencies in virtual environment
  - [x] Verify: `alembic --version` returns version

- [x] **Task 4: Configure Alembic for async SQLAlchemy** (AC: 6, 7)
  - [x] Initialize Alembic: `alembic init alembic`
  - [x] Configure `alembic.ini`:
    - Set `script_location = alembic`
    - Configure sqlalchemy.url placeholder
  - [x] Configure `alembic/env.py` for async:
    - Import asyncpg and async engine
    - Use `run_async_migrations()` pattern
    - Load DATABASE_URL from environment
  - [x] Verify: Alembic can connect to database

- [x] **Task 5: Create base model and initial migration** (AC: 8)
  - [x] Create `backend/app/models/base.py` with:
    - `id: UUID` (primary key, default uuid4)
    - `created_at: datetime` (default utcnow)
    - `updated_at: datetime` (onupdate utcnow)
    - `deleted_at: Optional[datetime]` (soft delete)
  - [x] Create `backend/app/models/__init__.py` exporting Base
  - [x] Generate initial migration: `alembic revision --autogenerate -m "initial_base_model"`
  - [x] Review generated migration for correctness
  - [x] Run migration: `alembic upgrade head`
  - [x] Verify: alembic_version table exists in database

- [x] **Task 6: Add database configuration to backend** (AC: 7)
  - [x] Create `backend/app/core/database.py` with:
    - Async engine creation
    - Session factory with async_sessionmaker
    - get_db dependency for FastAPI
  - [x] Update `backend/app/core/config.py` with DATABASE_URL setting
  - [x] Update `.env.example` with DATABASE_URL template

- [x] **Task 7: Verification testing** (AC: 1-9)
  - [x] Start postgres: `sudo docker compose up postgres -d`
  - [x] Verify container healthy: `docker ps` - "Up (healthy)"
  - [x] Connect via docker exec psql
  - [x] Verify pgvector: version 0.8.1 installed
  - [x] Run migrations: `alembic upgrade head`
  - [x] Verify alembic_version table created

## Dev Notes

### Architecture Patterns and Constraints

- **Database:** PostgreSQL 16 via pgvector Docker image [Source: docs/architecture.md]
- **ORM:** SQLAlchemy 2.x with asyncpg driver [Source: docs/architecture.md]
- **Migrations:** Alembic with async support [Source: docs/architecture.md]
- **Soft Delete:** All tables use `deleted_at` column pattern [Source: docs/epics.md]
- **Base Model:** UUID id, created_at, updated_at, deleted_at [Source: docs/epics.md]

### Database Connection

Per Architecture specification:
```
DATABASE_URL=postgresql+asyncpg://sme:${DB_PASSWORD}@localhost:5432/sme
```

### Base Model Pattern

```python
from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase
import uuid

class Base(DeclarativeBase):
    pass

class BaseModel(Base):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
```

### Alembic Async Configuration

Per SQLAlchemy 2.0 async pattern:
```python
# alembic/env.py
from sqlalchemy.ext.asyncio import async_engine_from_config
import asyncio

def run_async_migrations():
    connectable = async_engine_from_config(...)
    async def do_run_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)
    asyncio.run(do_run_migrations())
```

### Docker Compose postgres service

Already defined in docker-compose.yml:
```yaml
postgres:
  image: pgvector/pgvector:pg16
  container_name: sme-postgres
  environment:
    POSTGRES_DB: sme
    POSTGRES_USER: sme
    POSTGRES_PASSWORD: ${DB_PASSWORD}
  volumes:
    - postgres_data:/var/lib/postgresql/data
  ports:
    - "5432:5432"
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U sme -d sme"]
```

### Prerequisites

- Story 1.2 (Backend Foundation) - DONE
- Docker available with sudo access

### References

- [Source: docs/architecture.md#Database]
- [Source: docs/epics.md#Story-1.4]
- [Source: docs/sprint-artifacts/tech-spec-epic-1.md]

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2025-11-30 | Story drafted from epics and tech spec | Dev Agent (Amelia) |
| 2025-11-30 | Story implementation complete - all tasks verified | Dev Agent (Amelia) |

## Dev Agent Record

### Completion Notes

- PostgreSQL 16.11 container running via pgvector/pgvector:pg16 image
- pgvector 0.8.1 extension enabled and functional
- Container healthy with port 5432 exposed
- Alembic 1.14.0 configured for async SQLAlchemy 2.x
- Base model with UUID, created_at, updated_at, deleted_at pattern exists in `app/models/base.py`
- Initial migration `78b576fc3930_initial_base_model` generated and applied
- database.py created with async engine, session factory, and get_db dependency
- .env file created from .env.example for local development

### Files Created/Modified

**Created:**
- `backend/app/core/database.py` - Async database session management
- `backend/alembic/versions/78b576fc3930_initial_base_model.py` - Initial migration
- `backend/alembic/versions/.gitkeep` - Keep versions directory in git
- `.env` - Local environment configuration

**Pre-existing (from Story 1.2):**
- `backend/app/models/base.py` - Base model with UUID and timestamps
- `backend/app/models/__init__.py` - Model exports
- `backend/alembic/env.py` - Async Alembic configuration
- `backend/alembic.ini` - Alembic settings
- `backend/requirements.txt` - Already included alembic and asyncpg
