# Architecture

## Executive Summary

A decoupled architecture for an AI-powered ESG/modern slavery due diligence platform. Python/FastAPI backend handles business logic and orchestrates LangGraph-based agentic workflows. Next.js/React frontend provides SME and Admin dashboards. PostgreSQL persists all data with pgvector for embeddings. Redis provides caching and job queue backing. Self-hosted on VPS via Docker Compose.

## Project Initialization

### Frontend Setup
```bash
npx create-next-app@15 frontend --typescript --tailwind --eslint --app --src-dir
cd frontend
npx shadcn@3 init
```

### Backend Setup
```bash
mkdir backend && cd backend
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy asyncpg alembic langgraph langchain-core arq redis pydantic-settings python-jose passlib playwright
playwright install chromium  # Install browser binaries
# Install LLM provider package(s) as needed:
# pip install langchain-openai      # OpenAI (GPT-4o, etc.)
# pip install langchain-anthropic   # Anthropic (Claude)
# pip install langchain-google-genai # Google (Gemini)
```

### Provided by Starter Template (create-next-app)

The following are configured automatically by `create-next-app@15` (latest Next.js 15.x stable):

| Component | Provided | Notes |
|-----------|----------|-------|
| Next.js 15.x | ✓ | App Router enabled via `--app` flag |
| React 19.x | ✓ | Bundled with Next.js 15 |
| TypeScript 5.x | ✓ | Via `--typescript` flag |
| Tailwind CSS 4.x | ✓ | Via `--tailwind` flag (migrated to v4 CSS-first config) |
| ESLint | ✓ | Via `--eslint` flag |
| `src/` directory | ✓ | Via `--src-dir` flag |
| App Router structure | ✓ | `src/app/` with layout.tsx, page.tsx |
| PostCSS config | ✓ | For Tailwind processing |
| TypeScript config | ✓ | tsconfig.json with strict mode |
| Next.js config | ✓ | next.config.ts |

**Additional setup required (not from starter):**
- shadcn/ui components (`npx shadcn init`)
- API client generation (openapi-typescript)
- State management (Zustand, React Query)
- Authentication (NextAuth.js)
- Testing framework (Vitest + React Testing Library)
- Custom components in `src/components/`

## Decision Summary

| Category | Decision | Version | Affects FRs | Rationale |
| -------- | -------- | ------- | ----------- | --------- |
| Backend Framework | FastAPI | 0.115.x | All | Async-native, auto OpenAPI docs, Python ecosystem for AI |
| Frontend Framework | Next.js + React | 15.x (stable) | All UI | App Router, RSC, pairs with shadcn/ui |
| UI Components | shadcn/ui + Tailwind | 4.x | All UI | Per UX spec, accessible, customizable |
| Agent Orchestration | LangGraph | 1.0.x | FR17-51 | Stateful graphs, durable execution, multi-agent |
| LLM Provider | Configurable | - | FR17-57 | Provider-agnostic via LangChain (OpenAI, Anthropic, Google, etc.) |
| ORM | SQLAlchemy | 2.0.x | All data | Mature, async support, Alembic migrations |
| Database | PostgreSQL | 16.x | All data | Relational, pgvector, RLS capable |
| Vector Store | pgvector | 0.7.x | FR29-35 | Evidence embeddings, single DB |
| Cache | Redis | 7.x | Performance | Session cache, rate limiting |
| Task Queue | ARQ | 0.26.x | FR17-51 | Async job queue, Redis-backed |
| Real-time | SSE | - | FR15-16 | Assessment status updates |
| File Storage | MinIO | RELEASE.2024-11 | FR24, FR78 | S3-compatible, self-hosted |
| Auth | JWT + NextAuth.js | 5.x | FR1-9 | Stateless, HTTP-only cookies |
| API Style | REST + OpenAPI | 3.1 | All | FastAPI auto-docs, standard |
| API Versioning | URL-based | /api/v1/ | All | Clear, explicit |
| Frontend State | React Query + Zustand | 5.x / 5.x | All UI | Server state + client state |
| Frontend Testing | Vitest + React Testing Library | 4.x / 16.x | All UI | Fast unit/integration tests |
| API Client | openapi-typescript | 7.x | All UI | Type-safe from OpenAPI spec |
| Deployment | Docker Compose on VPS | - | All | Self-contained, single server |
| Web Browser Automation | Playwright | 1.49.x | FR17-28 | Headless browser for JS-heavy supplier sites |

*Version verification date: 2025-11-28*

## Project Structure

```
sme-platform/
├── frontend/                    # Next.js application
│   ├── src/
│   │   ├── app/                 # App Router pages
│   │   │   ├── (auth)/          # Auth routes (login, register)
│   │   │   ├── (dashboard)/     # Protected SME routes
│   │   │   │   ├── assessments/
│   │   │   │   ├── suppliers/
│   │   │   │   └── reports/
│   │   │   ├── admin/           # Admin routes
│   │   │   │   ├── users/
│   │   │   │   ├── risk-frameworks/
│   │   │   │   ├── data-sources/
│   │   │   │   └── countries/
│   │   │   ├── api/             # API routes (NextAuth, proxies)
│   │   │   └── layout.tsx
│   │   ├── components/
│   │   │   ├── ui/              # shadcn/ui components
│   │   │   ├── forms/           # Form components
│   │   │   ├── assessment/      # Assessment-specific
│   │   │   └── admin/           # Admin-specific
│   │   ├── lib/
│   │   │   ├── api-client.ts    # Generated OpenAPI client
│   │   │   ├── auth.ts          # NextAuth config
│   │   │   └── utils.ts
│   │   ├── hooks/               # Custom React hooks
│   │   └── stores/              # Zustand stores
│   ├── public/
│   └── package.json
│   # Note: Tailwind CSS v4 uses CSS-first configuration in globals.css
│
├── backend/                     # FastAPI application
│   ├── app/
│   │   ├── main.py              # FastAPI app entry
│   │   ├── core/
│   │   │   ├── config.py        # Settings (pydantic-settings)
│   │   │   ├── security.py      # JWT, password hashing
│   │   │   ├── deps.py          # Dependency injection
│   │   │   └── logging.py       # structlog config
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── router.py    # Main API router
│   │   │       └── endpoints/
│   │   │           ├── auth.py
│   │   │           ├── users.py
│   │   │           ├── assessments.py
│   │   │           ├── suppliers.py
│   │   │           ├── reports.py
│   │   │           ├── risk_frameworks.py
│   │   │           ├── data_sources.py
│   │   │           └── countries.py
│   │   ├── models/              # SQLAlchemy models
│   │   │   ├── base.py          # Base model with common fields
│   │   │   ├── user.py
│   │   │   ├── supplier.py
│   │   │   ├── assessment.py
│   │   │   ├── evidence.py
│   │   │   ├── risk_framework.py
│   │   │   ├── data_source.py
│   │   │   └── country.py
│   │   ├── schemas/             # Pydantic schemas
│   │   │   ├── base.py          # Response envelope schemas
│   │   │   ├── user.py
│   │   │   ├── assessment.py
│   │   │   └── ...
│   │   ├── services/            # Business logic
│   │   │   ├── user_service.py
│   │   │   ├── assessment_service.py
│   │   │   └── report_service.py
│   │   ├── agents/              # LangGraph workflows
│   │   │   ├── workflow.py      # Main assessment workflow
│   │   │   ├── nodes/
│   │   │   │   ├── data_collection.py
│   │   │   │   ├── evidence_analysis.py
│   │   │   │   ├── risk_assessment.py
│   │   │   │   └── report_generation.py
│   │   │   ├── tools/           # Agent tools
│   │   │   │   ├── web_scraper.py
│   │   │   │   ├── api_client.py
│   │   │   │   └── file_parser.py
│   │   │   └── state.py         # Graph state definition
│   │   ├── workers/             # ARQ workers
│   │   │   ├── worker.py        # Worker entry
│   │   │   └── tasks.py         # Task definitions
│   │   └── db/
│   │       ├── session.py       # Async session factory
│   │       └── init_db.py       # DB initialization
│   ├── alembic/                 # DB migrations
│   │   ├── versions/
│   │   └── env.py
│   ├── tests/
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   └── Dockerfile
│
├── docker-compose.yml           # Full stack compose (production)
├── docker-compose.dev.yml       # Dev infra only (hybrid setup)
├── docker-compose.dev-full.yml  # Full stack dev with hot-reload
├── .env.example
└── README.md
```

## FR Category to Architecture Mapping

| FR Category | FRs | Backend Module | Frontend Route | Agent Involvement |
|-------------|-----|----------------|----------------|-------------------|
| User Account & Access | FR1-9 | `api/v1/endpoints/auth.py`, `users.py` | `(auth)/`, `(dashboard)/` | None |
| Supplier Assessment | FR10-16 | `api/v1/endpoints/assessments.py` | `assessments/new`, `assessments/[id]` | Triggers workflow |
| Agentic Data Collection | FR17-28 | `agents/nodes/data_collection.py` | Status via SSE | `data_collection` node |
| Evidence Analysis | FR29-35 | `agents/nodes/evidence_analysis.py` | Evidence display | `evidence_analysis` node |
| Risk Assessment | FR36-42 | `agents/nodes/risk_assessment.py` | Risk ratings display | `risk_assessment` node |
| Report Generation | FR43-51 | `agents/nodes/report_generation.py` | Report view/export | `report_generation` node |
| Recommendations | FR52-57 | `agents/nodes/report_generation.py` | Recommendations panel | Part of report node |
| Assessment Management | FR58-63 | `api/v1/endpoints/assessments.py` | `assessments/` list | None |
| Admin: Risk Framework | FR64-71 | `api/v1/endpoints/risk_frameworks.py` | `admin/risk-frameworks/` | None |
| Admin: Data Sources | FR72-79 | `api/v1/endpoints/data_sources.py` | `admin/data-sources/` | None |
| Admin: Countries | FR80-84 | `api/v1/endpoints/countries.py` | `admin/countries/` | None |
| Admin: AI Discovery | FR85-91 | `services/discovery_service.py` | `admin/countries/[id]/discover` | Separate discovery agent |
| System & Processing | FR92-96 | `workers/`, `agents/workflow.py` | Status indicators | Workflow orchestration |

## Technology Stack Details

### Core Technologies

| Technology | Version | Purpose | Configuration |
|------------|---------|---------|---------------|
| Python | 3.11+ | Backend runtime | Type hints, async/await |
| FastAPI | 0.115.x | API framework | Async routes, OpenAPI |
| SQLAlchemy | 2.x | ORM | Async sessions, declarative |
| Alembic | Latest | Migrations | Async support |
| LangGraph | 1.0.x | Agent orchestration | Checkpointing enabled |
| LangChain | 1.1.x | LLM abstractions | Provider-agnostic via factory pattern |
| Playwright | 1.49.x | Web browser automation | Headless Chromium for JS-rendered sites |

### LLM Configuration (NFR11: Determinism)

LLM provider is configurable via environment variables. All providers use `temperature=0` for deterministic output.

```python
# app/agents/llm.py
from langchain_core.language_models.chat_models import BaseChatModel
from app.core.config import settings

def get_llm() -> BaseChatModel:
    """Factory function returning configured LLM based on settings."""
    common = {"temperature": 0, "max_tokens": 4096}

    match settings.LLM_PROVIDER:
        case "openai":
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(model=settings.LLM_MODEL, **common)
        case "anthropic":
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(model=settings.LLM_MODEL, **common)
        case "google":
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(model=settings.LLM_MODEL, **common)
        case _:
            raise ValueError(f"Unknown LLM provider: {settings.LLM_PROVIDER}")

# Usage in agent nodes
from app.agents.llm import get_llm

llm = get_llm()
result = llm.invoke(prompt)
```

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| temperature | 0 | Required for NFR11 - deterministic scoring within ±5% variance |
| max_tokens | 4096 | Sufficient for analysis responses |

| Provider | Package | Example Models |
|----------|---------|----------------|
| OpenAI | `langchain-openai` | gpt-4o, gpt-4o-mini |
| Anthropic | `langchain-anthropic` | claude-sonnet-4-20250514, claude-3-5-haiku-20241022 |
| Google | `langchain-google-genai` | gemini-1.5-pro, gemini-1.5-flash |

| Technology | Version | Purpose | Configuration |
|------------|---------|---------|---------------|
| ARQ | Latest | Task queue | Redis backend |
| Node.js | 24 LTS | Frontend runtime | - |
| Next.js | 15.x | React framework | App Router, RSC |
| React | 19.x | UI library | Server Components |
| TypeScript | 5.x | Type safety | Strict mode |

### Integration Points

| Integration | Protocol | Purpose |
|-------------|----------|---------|
| Frontend ↔ Backend | REST/JSON over HTTPS | All API calls |
| Frontend ↔ Backend | SSE | Real-time assessment status |
| Backend ↔ PostgreSQL | asyncpg | Data persistence |
| Backend ↔ Redis | aioredis | Cache + job queue |
| Backend ↔ MinIO | S3 API (boto3) | File storage |
| Backend ↔ LLM Provider | HTTPS | LLM inference (OpenAI, Anthropic, Google, etc.) |
| Agents ↔ External APIs | HTTPS | Data source queries |
| Agents ↔ Websites | Playwright (headless Chromium) | Web scraping, JS-rendered content |

## Novel Pattern: Assessment Workflow

The core innovation — a 4-node LangGraph pipeline for autonomous supplier assessment.

### Workflow Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            AssessmentState                                  │
│  supplier_info | collected_evidence | analyzed_evidence | risk_scores      │
│  report | status | current_node | errors | timestamps                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
    ┌────────────────────────────────┼────────────────────────────────────────┐
    │                                │                                        │
    ▼                                ▼                                        ▼
┌────────────────┐  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│ DATA COLLECTION│─▶│EVIDENCE ANALYSIS│─▶│ RISK ASSESSMENT│─▶│REPORT GENERATION│
│                │  │                │  │                │  │                │
│ • Sanctions    │  │ • Tag quality  │  │ • Apply scoring│  │ • Synthesize   │
│ • Registries   │  │ • Rate recency │  │ • Calc confidence│ │ • Format       │
│ • ESG databases│  │ • Score relevance│ │ • Flag red flags│ │ • Recommend    │
│ • News/media   │  │ • Correlate    │  │ • Determine EDD│  │ • Generate PDF │
│ • Website crawl│  │                │  │                │  │                │
└────────────────┘  └────────────────┘  └────────────────┘  └────────────────┘
     [Parallel]         [Sequential]        [Sequential]        [Sequential]
```

### State Definition

```python
from typing import TypedDict, Literal, Optional, List
from datetime import datetime
from pydantic import BaseModel

class Evidence(BaseModel):
    id: str  # UUID
    source_url: str
    source_type: Literal["sanctions", "registry", "esg", "news", "website", "file"]
    content: str
    collected_at: datetime
    collector_tool: str

class TaggedEvidence(Evidence):
    reliability: Literal["high", "medium", "low"]
    recency: Literal["current", "recent", "dated", "stale"]
    relevance_score: float  # 0.0 - 1.0
    risk_categories: List[str]
    confidence: float

class RiskScore(BaseModel):
    category: str
    score: float  # 0-100
    level: Literal["low", "medium", "high"]
    confidence: Literal["high", "medium", "low"]
    red_flags: List[str]
    supporting_evidence_ids: List[str]

class AssessmentState(TypedDict):
    # Identity
    assessment_id: str
    supplier_id: str
    user_id: str

    # Input configuration (from admin settings)
    data_sources: List[dict]
    risk_framework: dict
    country_config: dict

    # Progressive results
    collected_evidence: List[Evidence]
    analyzed_evidence: List[TaggedEvidence]
    risk_scores: List[RiskScore]
    report: Optional[dict]

    # Workflow state
    status: Literal["queued", "collecting", "analyzing", "scoring", "generating", "complete", "failed"]
    current_node: str
    progress_pct: int  # 0-100
    errors: List[dict]

    # Timestamps
    queued_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
```

### Node Responsibilities

| Node | Input | Output | Tools Used | FR Coverage |
|------|-------|--------|------------|-------------|
| `data_collection` | supplier_info, data_sources | collected_evidence[] | Playwright (web_scraper), api_client, file_parser | FR17-28 |
| `evidence_analysis` | collected_evidence[] | analyzed_evidence[] | LLM (tagging, correlation) | FR29-35 |
| `risk_assessment` | analyzed_evidence[], risk_framework | risk_scores[] | LLM (scoring), rule engine | FR36-42 |
| `report_generation` | risk_scores[], analyzed_evidence[] | report | LLM (synthesis), PDF generator | FR43-57 |

### Failure Handling

| Scenario | Behavior | User Impact |
|----------|----------|-------------|
| Single source fails | Log error, continue with others | Partial results with warning |
| Node timeout | Checkpoint state, mark incomplete | Can retry from checkpoint |
| LLM rate limit | Exponential backoff, retry | Delayed completion |
| All sources fail | Mark assessment failed | Error message, suggest retry |
| Worker crash | ARQ re-queues job, LangGraph resumes from checkpoint | Transparent recovery |

## Implementation Patterns

These patterns ensure consistent implementation across all AI agents:

### Naming Conventions

| Category | Convention | Example |
|----------|------------|---------|
| Python files | snake_case | `risk_assessment.py` |
| Python classes | PascalCase | `RiskFramework` |
| Python functions | snake_case | `calculate_score()` |
| Python constants | UPPER_SNAKE | `MAX_RETRY_COUNT` |
| DB tables | snake_case, plural | `risk_frameworks` |
| DB columns | snake_case | `created_at` |
| Foreign keys | `{table}_id` | `user_id`, `assessment_id` |
| API endpoints | kebab-case, plural | `/api/v1/risk-frameworks` |
| TS/React files | kebab-case | `risk-badge.tsx` |
| React components | PascalCase | `RiskBadge` |
| TS functions | camelCase | `fetchAssessment()` |
| TS types/interfaces | PascalCase | `Assessment`, `RiskScore` |
| Environment vars | UPPER_SNAKE | `DATABASE_URL` |

### API Patterns

| Pattern | Decision | Example |
|---------|----------|---------|
| Resource naming | Plural nouns | `/assessments`, `/suppliers` |
| Nested resources | Max 2 levels | `/assessments/{id}/evidence` |
| Actions | POST to verb endpoint | `POST /assessments/{id}/retry` |
| Filtering | Query params | `?status=complete&user_id=uuid` |
| Sorting | `-` prefix for desc | `?sort=-created_at` |
| Pagination | offset/limit | `?offset=0&limit=20` |
| Field selection | `fields` param | `?fields=id,name,status` |

### Response Envelope

```python
# Success - Single resource
{
    "data": {
        "id": "uuid",
        "type": "assessment",
        ...
    },
    "meta": {
        "request_id": "uuid"
    }
}

# Success - List
{
    "data": [...],
    "meta": {
        "total": 100,
        "limit": 20,
        "offset": 0,
        "request_id": "uuid"
    }
}

# Error
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Human readable message",
        "details": [
            {"field": "email", "message": "Invalid email format"}
        ]
    }
}
```

### Error Codes

| Code | HTTP | Usage |
|------|------|-------|
| `VALIDATION_ERROR` | 400 | Request body/params invalid |
| `UNAUTHORIZED` | 401 | Missing or invalid auth token |
| `FORBIDDEN` | 403 | Valid token, insufficient permissions |
| `NOT_FOUND` | 404 | Resource does not exist |
| `CONFLICT` | 409 | Duplicate entry or state conflict |
| `RATE_LIMITED` | 429 | Too many requests |
| `ASSESSMENT_IN_PROGRESS` | 409 | Cannot modify active assessment |
| `DATA_SOURCE_ERROR` | 502 | External data source failed |
| `INTERNAL_ERROR` | 500 | Unexpected server error |

## Consistency Rules

### Code Organization

**Backend (Python/FastAPI):**
```
endpoints/   → HTTP route handlers only (thin, delegate to services)
services/    → Business logic (validation, orchestration)
models/      → SQLAlchemy ORM models
schemas/     → Pydantic request/response schemas
agents/      → LangGraph workflows and nodes
workers/     → ARQ task definitions
core/        → Shared utilities (config, security, logging)
```

**Frontend (Next.js/React):**
```
app/         → Pages and layouts (App Router)
components/  → Reusable UI components
  ui/        → shadcn/ui primitives
  forms/     → Form-specific components
  {feature}/ → Feature-specific components
lib/         → Utilities, API client, auth
hooks/       → Custom React hooks
stores/      → Zustand state stores
```

### Error Handling

**Backend:**
```python
# All endpoints use dependency injection for error handling
from fastapi import HTTPException
from app.schemas.base import ErrorResponse

# Service layer raises domain exceptions
class AssessmentNotFoundError(Exception):
    pass

class InsufficientPermissionError(Exception):
    pass

# Endpoint layer catches and converts to HTTP
@router.get("/assessments/{id}")
async def get_assessment(id: str, current_user: User = Depends(get_current_user)):
    try:
        return await assessment_service.get(id, current_user)
    except AssessmentNotFoundError:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Assessment not found"})
    except InsufficientPermissionError:
        raise HTTPException(status_code=403, detail={"code": "FORBIDDEN", "message": "Access denied"})
```

**Frontend:**
```typescript
// React Query handles errors consistently
const { data, error, isLoading } = useQuery({
  queryKey: ['assessment', id],
  queryFn: () => api.assessments.get(id),
});

// Error boundary catches unhandled errors
// Toast notifications for user-facing errors
```

### Logging Strategy

**Format:** Structured JSON via `structlog`

```python
import structlog

logger = structlog.get_logger()

# All logs include context
logger.info(
    "assessment_started",
    assessment_id=assessment.id,
    user_id=user.id,
    supplier_name=supplier.name
)

# Agent logs include node context
logger.info(
    "evidence_collected",
    assessment_id=state["assessment_id"],
    node="data_collection",
    source_type="sanctions",
    evidence_count=len(evidence)
)
```

**Log Levels:**
| Level | Usage |
|-------|-------|
| `DEBUG` | Detailed diagnostic info (dev only) |
| `INFO` | Normal operations, state transitions |
| `WARNING` | Recoverable issues, degraded operation |
| `ERROR` | Failures requiring attention |
| `CRITICAL` | System-level failures |

**Required Context Fields:**
- `request_id` - Correlation ID for request tracing
- `user_id` - When user context available
- `assessment_id` - For assessment-related logs
- `node` - For agent workflow logs

## Data Architecture

### Core Entities

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    User     │────<│ Assessment  │>────│  Supplier   │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │
       │            ┌──────┴──────┐
       │            ▼             ▼
       │     ┌─────────────┐ ┌─────────────┐
       │     │  Evidence   │ │ RiskScore   │
       │     └─────────────┘ └─────────────┘
       │
       ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│RiskFramework│     │ DataSource  │     │  Country    │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Entity Schemas

```python
# Base model with common fields
class BaseModel(SQLAlchemyBase):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow, onupdate=utcnow)
    deleted_at: Optional[datetime] = None  # Soft delete

# User (FR1-9)
class User(BaseModel):
    __tablename__ = "users"
    email: str  # unique
    password_hash: str
    role: Literal["admin", "user"]
    is_active: bool = True
    last_login_at: Optional[datetime]

# Supplier (FR10-11)
class Supplier(BaseModel):
    __tablename__ = "suppliers"
    user_id: UUID  # FK -> users.id (owner)
    name: str
    country_code: str  # FK -> countries.code
    sector: str
    website_url: Optional[str]
    context: Optional[str]

# Assessment (FR10-16, FR58-63)
class Assessment(BaseModel):
    __tablename__ = "assessments"
    user_id: UUID  # FK -> users.id
    supplier_id: UUID  # FK -> suppliers.id
    status: Literal["queued", "collecting", "analyzing", "scoring", "generating", "complete", "failed"]
    overall_risk_level: Optional[Literal["low", "medium", "high"]]
    overall_confidence: Optional[Literal["low", "medium", "high"]]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    report_url: Optional[str]  # MinIO path

# Evidence (FR17-35)
class Evidence(BaseModel):
    __tablename__ = "evidence"
    assessment_id: UUID  # FK -> assessments.id
    source_url: str
    source_type: str
    content: Text
    content_embedding: Vector(1536)  # pgvector for similarity search
    reliability: Optional[Literal["high", "medium", "low"]]
    recency: Optional[Literal["current", "recent", "dated", "stale"]]
    relevance_score: Optional[float]
    collector_tool: str
    collected_at: datetime

# RiskScore (FR36-42)
class RiskScore(BaseModel):
    __tablename__ = "risk_scores"
    assessment_id: UUID  # FK -> assessments.id
    category: str  # FK -> risk_categories.code
    score: float  # 0-100
    level: Literal["low", "medium", "high"]
    confidence: Literal["low", "medium", "high"]
    red_flags: JSONB  # List of flag strings
    evidence_ids: JSONB  # List of evidence UUIDs

# RiskFramework (FR64-71)
class RiskFramework(BaseModel):
    __tablename__ = "risk_frameworks"
    name: str
    categories: JSONB  # List of category definitions
    scoring_rules: JSONB  # Scoring configuration
    thresholds: JSONB  # low/medium/high thresholds
    red_flag_criteria: JSONB
    is_active: bool = True

# DataSource (FR72-79)
class DataSource(BaseModel):
    __tablename__ = "data_sources"
    name: str
    source_type: Literal["api", "file", "url", "scrape"]
    config: JSONB  # Connection details (encrypted credentials)
    country_code: Optional[str]  # NULL = global
    is_enabled: bool = True
    last_health_check: Optional[datetime]
    health_status: Optional[Literal["healthy", "degraded", "failed"]]

# Country (FR80-84)
class Country(BaseModel):
    __tablename__ = "countries"
    code: str  # ISO 3166-1 alpha-2, primary key
    name: str
    is_enabled: bool = True
    config: JSONB  # Country-specific parameters
```

### Indexes

```sql
-- Performance indexes
CREATE INDEX idx_assessments_user_id ON assessments(user_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_assessments_status ON assessments(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_evidence_assessment_id ON evidence(assessment_id);
CREATE INDEX idx_suppliers_user_id ON suppliers(user_id) WHERE deleted_at IS NULL;

-- Vector similarity search
CREATE INDEX idx_evidence_embedding ON evidence USING ivfflat (content_embedding vector_cosine_ops);
```

## API Contracts

### Authentication Endpoints

```
POST   /api/v1/auth/login          # Email/password login, returns JWT
POST   /api/v1/auth/logout         # Invalidate session
POST   /api/v1/auth/refresh        # Refresh access token
POST   /api/v1/auth/password-reset # Request password reset
```

### User Endpoints

```
GET    /api/v1/users               # List users (admin only)
POST   /api/v1/users               # Create user (admin only)
GET    /api/v1/users/me            # Current user profile
PATCH  /api/v1/users/me            # Update profile
GET    /api/v1/users/{id}          # Get user (admin only)
PATCH  /api/v1/users/{id}          # Update user (admin only)
DELETE /api/v1/users/{id}          # Deactivate user (admin only)
```

### Assessment Endpoints

```
GET    /api/v1/assessments                    # List user's assessments
POST   /api/v1/assessments                    # Create new assessment
GET    /api/v1/assessments/{id}               # Get assessment details
DELETE /api/v1/assessments/{id}               # Delete assessment
POST   /api/v1/assessments/{id}/retry         # Retry failed assessment
GET    /api/v1/assessments/{id}/evidence      # Get evidence list
GET    /api/v1/assessments/{id}/status        # SSE stream for status updates
GET    /api/v1/assessments/{id}/report        # Get/download report
GET    /api/v1/assessments/{id}/questionnaire # Get generated questionnaire
```

### Admin Endpoints

```
# Risk Frameworks
GET    /api/v1/admin/risk-frameworks
POST   /api/v1/admin/risk-frameworks
GET    /api/v1/admin/risk-frameworks/{id}
PATCH  /api/v1/admin/risk-frameworks/{id}
DELETE /api/v1/admin/risk-frameworks/{id}

# Data Sources
GET    /api/v1/admin/data-sources
POST   /api/v1/admin/data-sources
GET    /api/v1/admin/data-sources/{id}
PATCH  /api/v1/admin/data-sources/{id}
DELETE /api/v1/admin/data-sources/{id}
POST   /api/v1/admin/data-sources/{id}/test   # Test connection

# Countries
GET    /api/v1/admin/countries
POST   /api/v1/admin/countries
GET    /api/v1/admin/countries/{code}
PATCH  /api/v1/admin/countries/{code}
POST   /api/v1/admin/countries/{code}/discover # AI suggest data sources
```

## Security Architecture

### Authentication Flow

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ Browser │────>│ Next.js │────>│ FastAPI │────>│   DB    │
└─────────┘     └─────────┘     └─────────┘     └─────────┘
     │               │               │
     │  1. Login     │               │
     │──────────────>│  2. Proxy     │
     │               │──────────────>│  3. Verify
     │               │               │     credentials
     │               │  4. JWT       │<─────────────
     │  5. Set       │<──────────────│
     │     cookie    │               │
     │<──────────────│               │
     │               │               │
     │  6. API call  │               │
     │  (with cookie)│  7. Forward   │
     │──────────────>│     JWT       │  8. Validate
     │               │──────────────>│     & authorize
```

### Security Controls

| Control | Implementation | NFR |
|---------|----------------|-----|
| Password hashing | Argon2id | NFR1 |
| Transport security | TLS 1.3 | NFR2 |
| Session expiry | 24h access, 7d refresh | NFR3 |
| Input validation | Pydantic schemas | NFR4 |
| Authorization | Role-based (admin/user) + ownership | NFR5 |
| Ethical scraping | Respect robots.txt | NFR6 |
| Secret storage | Environment variables + encrypted DB fields | NFR8 |
| Audit logging | All auth events logged | NFR9 |
| Data isolation | User-scoped queries enforced at service layer | NFR33 |

### Data Isolation Pattern

```python
# All user-scoped queries include user filter
async def get_assessments(user: User, filters: AssessmentFilter) -> List[Assessment]:
    query = select(Assessment).where(
        Assessment.user_id == user.id,  # ALWAYS filter by user
        Assessment.deleted_at.is_(None)
    )
    if filters.status:
        query = query.where(Assessment.status == filters.status)
    return await db.execute(query)

# Admin can access all with explicit flag
async def get_all_assessments(admin: User, filters: AssessmentFilter) -> List[Assessment]:
    assert admin.role == "admin"  # Double-check
    query = select(Assessment).where(Assessment.deleted_at.is_(None))
    # No user filter for admin
    return await db.execute(query)
```

## Performance Considerations

### Caching Strategy

| Data | Cache Location | TTL | Invalidation |
|------|----------------|-----|--------------|
| User session | Redis | 24h | On logout |
| Risk framework config | Redis | 1h | On update |
| Data source config | Redis | 1h | On update |
| Assessment status | Redis | 30s | On status change |
| Static assets | CDN/Browser | 1y | Versioned URLs |

### Database Optimization

- **Connection pooling:** asyncpg with pool size 20
- **Indexes:** On foreign keys, status fields, timestamps
- **Pagination:** Offset/limit with max 100 per page
- **Soft deletes:** Filter `deleted_at IS NULL` in all queries

### Background Processing

- **ARQ workers:** 4 workers per container
- **Concurrency:** Max 10 concurrent assessments per worker
- **LLM rate limiting:** Token bucket per API key
- **Timeouts:** 5 min per node, 30 min per assessment

### Metrics & Observability

**Endpoint:** `GET /metrics` (Prometheus format)

```python
# app/core/metrics.py
from prometheus_client import Counter, Histogram, Gauge

# Request metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'Request latency', ['endpoint'])

# Assessment metrics
ASSESSMENT_DURATION = Histogram('assessment_duration_seconds', 'Assessment processing time', ['node'])
ASSESSMENT_STATUS = Gauge('assessments_by_status', 'Current assessments by status', ['status'])

# LLM metrics
LLM_TOKEN_USAGE = Counter('llm_tokens_total', 'Total LLM tokens used', ['provider', 'model', 'type'])
LLM_LATENCY = Histogram('llm_request_duration_seconds', 'LLM request latency', ['provider', 'model'])
LLM_ERRORS = Counter('llm_errors_total', 'LLM API errors', ['provider', 'model', 'error_type'])
```

| Metric | Type | Labels | Purpose |
|--------|------|--------|---------|
| `http_requests_total` | Counter | method, endpoint, status | Request volume |
| `http_request_duration_seconds` | Histogram | endpoint | p50/p95/p99 latency |
| `assessment_duration_seconds` | Histogram | node | Per-node processing time |
| `llm_tokens_total` | Counter | provider, model, type | Token usage tracking |
| `llm_request_duration_seconds` | Histogram | provider, model | LLM API latency |
| `llm_errors_total` | Counter | provider, model, error_type | Error rate monitoring |

**SLO Thresholds:**
- p95 API latency: <500ms
- p99 API latency: <1000ms
- Error rate: <1%
- Assessment completion: <30 min

## Deployment Architecture

### Docker Compose Stack

```yaml
services:
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on: [backend]

  backend:
    build: ./backend
    ports: ["8000:8000"]
    environment:
      - DATABASE_URL=postgresql+asyncpg://...
      - REDIS_URL=redis://redis:6379
      - MINIO_URL=http://minio:9000
    depends_on: [postgres, redis, minio]

  worker:
    build: ./backend
    command: arq app.workers.worker.WorkerSettings
    environment: # Same as backend
    depends_on: [postgres, redis, backend]

  postgres:
    image: pgvector/pgvector:pg16
    volumes: [postgres_data:/var/lib/postgresql/data]
    environment:
      - POSTGRES_DB=sme
      - POSTGRES_USER=sme
      - POSTGRES_PASSWORD=${DB_PASSWORD}

  redis:
    image: redis:7-alpine
    volumes: [redis_data:/data]

  minio:
    image: minio/minio
    command: server /data --console-address ":9001"
    volumes: [minio_data:/data]
    environment:
      - MINIO_ROOT_USER=${MINIO_USER}
      - MINIO_ROOT_PASSWORD=${MINIO_PASSWORD}

volumes:
  postgres_data:
  redis_data:
  minio_data:
```

### VPS Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| CPU | 4 cores | 8 cores |
| RAM | 8 GB | 16 GB |
| Storage | 50 GB SSD | 100 GB SSD |
| OS | Ubuntu 22.04 LTS | Ubuntu 24.04 LTS |

### Reverse Proxy (Nginx/Caddy)

```
example.com        → frontend:3000
api.example.com    → backend:8000
minio.example.com  → minio:9001 (console)
```

## Development Environment

Two development setups are available to accommodate different developer preferences and technical skill levels.

### Option A: Hybrid Setup (Recommended for Technical Developers)

Infrastructure runs in Docker; application code runs locally for fastest hot-reload and debugging.

**Prerequisites:**
- Python 3.11+
- Node.js 24 LTS
- Docker & Docker Compose
- Git

**Setup Commands:**

```bash
# Clone repository
git clone <repo-url> sme-platform
cd sme-platform

# Start infrastructure
docker compose -f docker-compose.dev.yml up -d postgres redis minio

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env  # Edit with local values
alembic upgrade head  # Run migrations
uvicorn app.main:app --reload

# Frontend setup (new terminal)
cd frontend
npm install
cp .env.example .env.local  # Edit with local values
npm run dev

# Worker (new terminal)
cd backend
source venv/bin/activate
arq app.workers.worker.WorkerSettings
```

### Option B: Fully Dockerized Setup (Recommended for Non-Technical Developers)

Everything runs in Docker with hot-reload support. Only requires Docker installed.

**Prerequisites:**
- Docker & Docker Compose
- Git

**Setup Commands:**

```bash
# Clone repository
git clone <repo-url> sme-platform
cd sme-platform

# Copy environment files
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local

# Start entire stack with hot-reload
docker compose -f docker-compose.dev-full.yml up

# Run migrations (first time only, in separate terminal)
docker compose -f docker-compose.dev-full.yml exec backend alembic upgrade head
```

**Services available:**
| Service | URL | Hot-Reload |
|---------|-----|------------|
| Frontend | http://localhost:3000 | Yes (Next.js HMR) |
| Backend API | http://localhost:8000 | Yes (uvicorn --reload) |
| API Docs | http://localhost:8000/docs | - |
| MinIO Console | http://localhost:9001 | - |

**How hot-reload works:**
- Source code is volume-mounted into containers
- Backend uses `uvicorn --reload` watching `/app` directory
- Frontend uses Next.js built-in HMR via volume mount
- `node_modules` uses anonymous volume to prevent host/container conflicts

**Comparison of Development Setups:**

| Aspect | Hybrid (Option A) | Fully Dockerized (Option B) |
|--------|-------------------|------------------------------|
| Prerequisites | Python, Node.js, Docker | Docker only |
| Setup complexity | Higher | Lower |
| Hot-reload speed | Fastest | Fast (slight overhead) |
| IDE integration | Native (breakpoints, etc.) | Requires remote debugging |
| Resource usage | Lower | Higher (containers overhead) |
| Best for | Backend/frontend developers | QA, designers, new team members |

### Environment Variables

```bash
# Backend (.env)
DATABASE_URL=postgresql+asyncpg://sme:password@localhost:5432/sme
REDIS_URL=redis://localhost:6379
MINIO_URL=http://localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin

# LLM Configuration
LLM_PROVIDER=openai                 # openai | anthropic | google
LLM_MODEL=gpt-4o                    # Model name for chosen provider
LLM_API_KEY=sk-...                  # API key for chosen provider

JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-nextauth-secret
```

## Architecture Decision Records (ADRs)

### ADR-001: Decoupled Frontend/Backend

**Context:** Need flexible architecture for B2B SaaS platform with complex AI workflows.

**Decision:** Separate Next.js frontend from FastAPI backend.

**Rationale:**
- Python ecosystem superior for AI/LLM workloads
- Independent scaling of API and workers
- Team can parallelize frontend/backend development
- Clear API contract via OpenAPI

**Consequences:**
- CORS configuration required
- Auth token coordination between systems
- Two deployments to manage

---

### ADR-002: LangGraph for Agent Orchestration

**Context:** Need to orchestrate 4-stage assessment pipeline with parallel execution, failure handling, and checkpointing.

**Decision:** Use LangGraph over raw LangChain or custom implementation.

**Rationale:**
- Built-in state management and checkpointing
- Graph-based workflow matches our pipeline model
- Durable execution survives failures
- Active development by LangChain team

**Consequences:**
- Learning curve for graph-based programming
- Dependency on LangGraph release cycle

---

### ADR-003: ARQ over Celery for Task Queue

**Context:** Need background job processing for assessment workflows.

**Decision:** Use ARQ instead of Celery.

**Rationale:**
- Async-native (matches FastAPI's async model)
- Lighter weight than Celery
- Redis-only dependency (already in stack)
- Simpler configuration

**Consequences:**
- Less ecosystem tooling than Celery
- No built-in task monitoring UI (use Redis inspection)

---

### ADR-004: SSE over WebSockets for Status Updates

**Context:** Need real-time assessment status updates in frontend.

**Decision:** Use Server-Sent Events instead of WebSockets.

**Rationale:**
- Simpler implementation (HTTP-native)
- One-way data flow matches our use case
- Better proxy/firewall compatibility
- Automatic reconnection built into EventSource API

**Consequences:**
- Cannot send client→server messages (not needed)
- Limited to text data (JSON strings)

---

### ADR-005: Provider-Agnostic LLM Integration

**Context:** Initial architecture specified OpenAI as the sole LLM provider. Need flexibility to use different providers based on cost, performance, or capability requirements.

**Decision:** Use LangChain's provider abstraction with a factory pattern instead of hardcoding OpenAI.

**Rationale:**
- Avoids vendor lock-in
- Enables cost optimization (different models for different tasks)
- Allows switching providers without code changes
- All major providers implement compatible `BaseChatModel` interface
- `temperature=0` provides determinism across all providers

**Consequences:**
- Must install provider-specific packages (langchain-openai, langchain-anthropic, etc.)
- Model names differ between providers (configuration concern)
- Some provider-specific features (like `seed`) not universally available
- Slightly more complex initialization via factory function

---

### ADR-006: Dual Development Environment Strategy

**Context:** The development team includes both technical developers (comfortable with Python, Node.js, IDE debugging) and less technical team members (QA, designers) who struggle with local environment setup.

**Decision:** Provide two parallel development environment options:
1. **Hybrid setup:** Infrastructure in Docker, app code runs locally (existing approach)
2. **Fully dockerized setup:** Entire stack in Docker with hot-reload via volume mounts

**Rationale:**
- Reduces onboarding friction for non-technical team members
- Single `docker compose up` command vs. multi-step local setup
- Hot-reload preserved in both setups via volume mounts and `--reload` flags
- Technical developers retain native IDE debugging when preferred
- Same Docker images can be tested locally before production

**Implementation:**
- `docker-compose.dev.yml` - Infrastructure only (existing)
- `docker-compose.dev-full.yml` - Full stack with volume mounts for hot-reload
- Backend: `uvicorn --reload` watching mounted `/app` directory
- Frontend: Next.js HMR with source mounted, `node_modules` in anonymous volume

**Consequences:**
- Two development paths to document and maintain
- Volume mount performance varies by OS (native on Linux, slower on macOS/Windows)
- IDE remote debugging requires additional configuration in fully-dockerized mode
- Team members can choose setup that matches their comfort level

---

### ADR-007: Playwright for Web Browser Automation

**Context:** The data collection agent needs to crawl supplier websites to gather ESG disclosures, modern slavery statements, and corporate information. Many supplier websites use JavaScript frameworks (React, Vue, Angular) that render content client-side.

**Decision:** Use Playwright with headless Chromium for all web scraping operations instead of simple HTTP requests.

**Rationale:**
- Modern supplier websites are often SPAs that require JavaScript execution
- Full browser engine handles dynamic content, AJAX calls, and lazy loading
- Async-native Python API (`playwright.async_api`) integrates cleanly with FastAPI
- Can capture screenshots as visual evidence of findings
- Handles cookies, sessions, and authentication flows for supplier portals
- Respects robots.txt when configured (NFR6: Ethical scraping)
- Single browser context can be reused across multiple page visits (performance)

**Alternatives Considered:**
| Option | Why Not |
|--------|---------|
| requests + BeautifulSoup | Cannot execute JavaScript, misses dynamic content |
| Selenium | Heavier, less performant, older API design |
| httpx + trafilatura | Good for article extraction, not general web scraping |
| Puppeteer | Node.js only, would require separate service |

**Implementation:**
```python
# app/agents/tools/web_scraper.py
from playwright.async_api import async_playwright

async def scrape_supplier_website(url: str) -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="SME-DueDiligence-Bot/1.0 (+https://example.com/bot)"
        )
        page = await context.new_page()
        await page.goto(url, wait_until="networkidle")

        content = await page.content()
        screenshot = await page.screenshot(full_page=True)

        await browser.close()
        return {"html": content, "screenshot": screenshot}
```

**Docker Configuration:**
```dockerfile
# backend/Dockerfile
RUN pip install playwright && playwright install chromium --with-deps
```

**Consequences:**
- Larger Docker image (~400MB for Chromium)
- Higher memory usage per scrape operation (~100-200MB)
- Slower than simple HTTP requests (acceptable for our throughput needs)
- Must manage browser lifecycle carefully to avoid resource leaks

---

_Generated by BMAD Decision Architecture Workflow v1.0_
_Date: 2025-11-28_
_Updated: 2025-11-30_
_For: Master_
