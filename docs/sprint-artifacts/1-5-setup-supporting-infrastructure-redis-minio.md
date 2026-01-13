# Story 1.5: Setup Supporting Infrastructure (Redis + MinIO)

Status: done

## Story

As a **developer**,
I want Redis and MinIO running in Docker,
so that I have caching, job queue, and file storage available.

## Acceptance Criteria

1. **AC1:** Redis 7.x container starts via `docker compose up redis`
2. **AC2:** Redis accepts connections on port 6379
3. **AC3:** Redis persistent volume configured for data
4. **AC4:** MinIO container starts via `docker compose up minio`
5. **AC5:** MinIO API accessible on port 9000
6. **AC6:** MinIO Console accessible on port 9001
7. **AC7:** MinIO persistent volume configured for data
8. **AC8:** Backend can connect to Redis and perform basic operations (set/get)
9. **AC9:** Backend can upload and download files from MinIO
10. **AC10:** Health checks configured for both containers

## Tasks / Subtasks

- [x] **Task 1: Add Redis service to docker-compose.yml** (AC: 1, 2, 3, 10)
  - [x] Add redis service using `redis:7-alpine` image
  - [x] Configure port mapping 6379:6379
  - [x] Add persistent volume `redis_data:/data`
  - [x] Configure health check: `redis-cli ping`
  - [x] Test: `sudo docker compose up redis -d` starts successfully
  - [x] Test: `redis-cli ping` returns PONG

- [x] **Task 2: Add MinIO service to docker-compose.yml** (AC: 4, 5, 6, 7, 10)
  - [x] Add minio service using `minio/minio:RELEASE.2024-11-07T00-52-20Z` image
  - [x] Configure command: `server /data --console-address ":9001"`
  - [x] Configure port mappings: 9000:9000 (API), 9001:9001 (Console)
  - [x] Add persistent volume `minio_data:/data`
  - [x] Configure environment: MINIO_ROOT_USER, MINIO_ROOT_PASSWORD from env
  - [x] Configure health check: `mc ready local`
  - [x] Test: `sudo docker compose up minio -d` starts successfully
  - [x] Test: MinIO console accessible at http://localhost:9001

- [x] **Task 3: Install Redis dependencies in backend** (AC: 8)
  - [x] Add to backend requirements.txt:
    - `redis>=5.0.0`
  - [x] Install dependencies in virtual environment
  - [x] Verify: `python -c "import redis; print(redis.__version__)"`

- [x] **Task 4: Create Redis configuration module** (AC: 8)
  - [x] Add REDIS_URL to `backend/app/core/config.py`
  - [x] Create `backend/app/core/redis.py` with:
    - Async Redis client factory
    - Connection pool management
    - get_redis dependency for FastAPI
  - [x] Test: Backend can connect and perform set/get operations

- [x] **Task 5: Install MinIO/S3 dependencies in backend** (AC: 9)
  - [x] Add to backend requirements.txt:
    - `aioboto3>=13.0.0`
    - `boto3>=1.35.0` (installed as aioboto3 dependency)
  - [x] Install dependencies in virtual environment
  - [x] Verify: `python -c "import aioboto3; print(aioboto3.__version__)"`

- [x] **Task 6: Create MinIO/S3 configuration module** (AC: 9)
  - [x] Add MinIO settings to `backend/app/core/config.py`:
    - MINIO_URL
    - MINIO_ACCESS_KEY
    - MINIO_SECRET_KEY
    - MINIO_BUCKET_NAME (default: "sme-files")
  - [x] Create `backend/app/core/storage.py` with:
    - Async S3 client factory using aioboto3
    - upload_file() function
    - download_file() function
    - delete_file() function
    - get_presigned_url() function
  - [x] Test: Backend can upload and download files

- [x] **Task 7: Update environment configuration** (AC: 8, 9)
  - [x] Update `.env.example` with:
    - REDIS_URL=redis://localhost:6379
    - MINIO_URL=http://localhost:9000
    - MINIO_ACCESS_KEY=minioadmin
    - MINIO_SECRET_KEY=minioadmin
    - MINIO_BUCKET_NAME=sme-files
  - [x] Update `.env` with local development values

- [x] **Task 8: Verification testing** (AC: 1-10)
  - [x] Start all services: `sudo docker compose up redis minio -d`
  - [x] Verify Redis healthy: `docker ps` shows healthy status
  - [x] Verify MinIO healthy: `docker ps` shows healthy status
  - [x] Test Redis connection from backend
  - [x] Test MinIO file upload/download from backend
  - [x] Verify MinIO console accessible at http://localhost:9001

## Dev Notes

### Architecture Patterns and Constraints

- **Cache:** Redis 7.x for session cache, rate limiting, ARQ job queue [Source: docs/architecture.md#Decision-Summary]
- **File Storage:** MinIO (S3-compatible) for admin-uploaded files, generated reports [Source: docs/architecture.md#Decision-Summary]
- **Task Queue:** ARQ 0.26.x backed by Redis [Source: docs/architecture.md#Decision-Summary]

### Redis Configuration Pattern

Per Architecture specification:
```python
# backend/app/core/redis.py
import redis.asyncio as redis
from app.core.config import settings

async def get_redis_pool():
    return redis.ConnectionPool.from_url(
        settings.REDIS_URL,
        decode_responses=True
    )

async def get_redis():
    pool = await get_redis_pool()
    return redis.Redis(connection_pool=pool)
```

### MinIO S3 Client Pattern

Per Architecture specification:
```python
# backend/app/core/storage.py
import aioboto3
from app.core.config import settings

async def get_s3_client():
    session = aioboto3.Session()
    async with session.client(
        's3',
        endpoint_url=settings.MINIO_URL,
        aws_access_key_id=settings.MINIO_ACCESS_KEY,
        aws_secret_access_key=settings.MINIO_SECRET_KEY
    ) as client:
        yield client
```

### Docker Compose Services

Redis service (to add):
```yaml
redis:
  image: redis:7-alpine
  container_name: sme-redis
  volumes:
    - redis_data:/data
  ports:
    - "6379:6379"
  healthcheck:
    test: ["CMD", "redis-cli", "ping"]
    interval: 10s
    timeout: 5s
    retries: 5
  restart: unless-stopped
```

MinIO service (to add):
```yaml
minio:
  image: minio/minio:RELEASE.2024-11-07T00-52-20Z
  container_name: sme-minio
  command: server /data --console-address ":9001"
  environment:
    MINIO_ROOT_USER: ${MINIO_ACCESS_KEY:-minioadmin}
    MINIO_ROOT_PASSWORD: ${MINIO_SECRET_KEY:-minioadmin}
  volumes:
    - minio_data:/data
  ports:
    - "9000:9000"
    - "9001:9001"
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
    interval: 30s
    timeout: 20s
    retries: 3
  restart: unless-stopped
```

### Environment Variables

```bash
# Redis
REDIS_URL=redis://localhost:6379

# MinIO
MINIO_URL=http://localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=sme-files
```

### Prerequisites

- Story 1.2 (Backend Foundation) - DONE
- Story 1.4 (Database Infrastructure) - DONE
- Docker available with sudo access

### Learnings from Previous Story

**From Story 1-4 (Status: done)**

- **Infrastructure Pattern**: docker-compose.yml already exists with postgres service - follow same pattern for redis and minio
- **Configuration Pattern**: Settings loaded via pydantic-settings in `app/core/config.py` - add Redis and MinIO settings there
- **Volume Pattern**: Named volumes used for persistence (postgres_data) - use same pattern for redis_data and minio_data
- **Health Check Pattern**: Health checks configured on postgres - follow same pattern for redis and minio
- **Async Pattern**: All database code uses async patterns - Redis and MinIO code should also be async

[Source: docs/sprint-artifacts/1-4-setup-database-infrastructure.md#Dev-Agent-Record]

### References

- [Source: docs/architecture.md#Technology-Stack-Details]
- [Source: docs/architecture.md#Docker-Compose-Stack]
- [Source: docs/epics.md#Story-1.5]
- [Source: docs/sprint-artifacts/tech-spec-epic-1.md#AC9-AC10]

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2025-11-30 | Story drafted from epics and tech spec | SM Agent (Bob) |
| 2025-11-30 | All tasks implemented and verified | Dev Agent (Amelia) |
| 2025-11-30 | Senior Developer Review - Approved | Code Reviewer (AI) |

## Dev Agent Record

### Context Reference

- docs/sprint-artifacts/1-5-setup-supporting-infrastructure-redis-minio.context.xml

### Agent Model Used

Claude Opus 4.5 (claude-opus-4-5-20251101)

### Debug Log References

- Redis and MinIO services pre-configured in docker-compose.yml from prior story
- Config.py already had REDIS_URL, MINIO_URL, MINIO_ACCESS_KEY, MINIO_SECRET_KEY
- Added MINIO_BUCKET_NAME setting
- Dependency conflict between boto3 and aiobotocore resolved by installing aioboto3 alone

### Completion Notes List

- Redis 7-alpine container starts healthy, accepts connections on 6379
- MinIO RELEASE.2024-11-07T00-52-20Z container starts healthy, API on 9000, Console on 9001
- Backend redis.py: async client with connection pool, get_redis() dependency, check_redis_health()
- Backend storage.py: async S3 client, upload_file, download_file, delete_file, get_presigned_url, ensure_bucket_exists, check_storage_health
- Verified Redis set/get operations from Python
- Verified MinIO upload/download operations from Python, bucket auto-created
- All 10 acceptance criteria satisfied

### File List

- backend/app/core/redis.py (created)
- backend/app/core/storage.py (created)
- backend/app/core/config.py (modified - added MINIO_BUCKET_NAME)
- backend/requirements.txt (modified - added aioboto3)
- .env.example (modified - added MINIO_BUCKET_NAME)

---

## Senior Developer Review (AI)

### Review Details

- **Reviewer:** Master
- **Date:** 2025-11-30
- **Outcome:** ✅ **APPROVED**

### Summary

All 10 acceptance criteria verified as implemented. All 8 tasks verified as correctly completed with file-level evidence. Infrastructure modules follow async patterns per architecture specification. No HIGH or MEDIUM severity issues found.

### Key Findings

No blocking or critical issues identified.

**LOW Severity (Advisory):**
- Note: `redis.py` could add connection error handling in `get_redis()` for resilience
- Note: `storage.py` `ensure_bucket_exists()` catches generic `ClientError` - could be more specific

### Acceptance Criteria Coverage

| AC# | Description | Status | Evidence |
|-----|-------------|--------|----------|
| AC1 | Redis 7.x container starts via docker compose up redis | ✅ IMPLEMENTED | docker-compose.yml:24 `image: redis:7-alpine` |
| AC2 | Redis accepts connections on port 6379 | ✅ IMPLEMENTED | docker-compose.yml:29-30 `ports: - "6379:6379"` |
| AC3 | Redis persistent volume configured for data | ✅ IMPLEMENTED | docker-compose.yml:27-28, 122 `volumes: redis_data` |
| AC4 | MinIO container starts via docker compose up minio | ✅ IMPLEMENTED | docker-compose.yml:38 `image: minio/minio:RELEASE.2024-11-07T00-52-20Z` |
| AC5 | MinIO API accessible on port 9000 | ✅ IMPLEMENTED | docker-compose.yml:47 `ports: - "9000:9000"` |
| AC6 | MinIO Console accessible on port 9001 | ✅ IMPLEMENTED | docker-compose.yml:48 `ports: - "9001:9001"` |
| AC7 | MinIO persistent volume configured for data | ✅ IMPLEMENTED | docker-compose.yml:45-46, 123 `volumes: minio_data` |
| AC8 | Backend can connect to Redis and perform set/get | ✅ IMPLEMENTED | backend/app/core/redis.py:1-42 (async client, get_redis dependency) |
| AC9 | Backend can upload and download files from MinIO | ✅ IMPLEMENTED | backend/app/core/storage.py:44-89 (upload_file, download_file) |
| AC10 | Health checks configured for both containers | ✅ IMPLEMENTED | docker-compose.yml:31-35, 50-54 (healthcheck blocks) |

**Summary:** 10 of 10 acceptance criteria fully implemented

### Task Completion Validation

| Task | Marked | Verified | Evidence |
|------|--------|----------|----------|
| Task 1: Add Redis service to docker-compose.yml | [x] | ✅ VERIFIED | docker-compose.yml:23-35 |
| Task 2: Add MinIO service to docker-compose.yml | [x] | ✅ VERIFIED | docker-compose.yml:37-54 |
| Task 3: Install Redis dependencies in backend | [x] | ✅ VERIFIED | requirements.txt:20 redis==5.2.0 |
| Task 4: Create Redis configuration module | [x] | ✅ VERIFIED | backend/app/core/redis.py (42 lines) |
| Task 5: Install MinIO/S3 dependencies in backend | [x] | ✅ VERIFIED | requirements.txt:24 aioboto3==13.2.0 |
| Task 6: Create MinIO/S3 configuration module | [x] | ✅ VERIFIED | backend/app/core/storage.py (143 lines) |
| Task 7: Update environment configuration | [x] | ✅ VERIFIED | config.py:28, .env.example |
| Task 8: Verification testing | [x] | ✅ VERIFIED | Containers healthy, Python tests passed |

**Summary:** 8 of 8 completed tasks verified, 0 questionable, 0 falsely marked complete

### Test Coverage and Gaps

- Manual verification via Python scripts confirmed Redis set/get and MinIO upload/download
- No automated unit tests yet (test framework not installed per Epic 1 scope)
- Container health checks provide operational validation

### Architectural Alignment

- ✅ Follows async patterns per architecture.md
- ✅ Uses pydantic-settings for configuration
- ✅ Matches docker-compose stack specification
- ✅ Uses correct package versions

### Security Notes

- ✅ No hardcoded secrets in code
- ✅ All credentials via environment variables
- ✅ Defaults are local development values only

### Best-Practices and References

- Redis async client: [redis-py docs](https://redis-py.readthedocs.io/en/stable/examples/asyncio_examples.html)
- aioboto3 S3 client: [aioboto3 GitHub](https://github.com/terrycain/aioboto3)
- MinIO health checks: Uses `mc ready local` (recommended by MinIO)

### Action Items

**Advisory Notes:**
- Note: Consider adding connection retry logic to redis.py for production resilience (no action required now)
- Note: Consider using more specific exception handling in storage.py (no action required now)
