# SME Supply Chain Risk Analysis - Epic Breakdown

**Author:** Master
**Date:** 2025-11-28
**Project Level:** Medium-High Complexity
**Target Scale:** MVP (Canada) → International Expansion

---

## Overview

This document provides the complete epic and story breakdown for SME Supply Chain Risk Analysis, decomposing the requirements from the [PRD](./prd.md) into implementable stories.

**Living Document Notice:** This version incorporates full context from PRD, UX Design, and Architecture documents.

### Epic Summary

| # | Epic | Stories | Key Capability |
|---|------|---------|----------------|
| 1 | Foundation & Project Setup | 7 | Infrastructure, Docker, dev environment |
| 2 | User Authentication & Access | 9 | Login, roles, data isolation, E2E testing |
| 3 | Supplier Submission & Status | 7 | Submit suppliers, real-time SSE tracking |
| 4 | Admin Risk Framework Config | 6 | Categories, scoring rules, red flags |
| 5 | Admin Data Sources & Countries | 8 | Data sources, country setup, AI discovery |
| 6 | Agentic Assessment Pipeline | 7 | LangGraph agents: collect → analyze → score |
| 7 | Results & Reporting | 9 | Risk display, evidence, PDF/CSV export |

**Total: 53 stories across 7 epics covering all 96 FRs**

### Sequencing Rationale

```
Epic 1 (Foundation) → Epic 2 (Auth) ─┬─→ Epic 3 (Submission) ──────────────┐
                                     ├─→ Epic 4 (Risk Config) ─────────────┼─→ Epic 6 (Pipeline) → Epic 7 (Results)
                                     └─→ Epic 5 (Data Sources) ────────────┘
```

- **Epic 1-2:** Sequential foundation and authentication
- **Epics 3, 4, 5:** Parallel tracks after Epic 2 completes
  - Epic 3: SME user submission flow
  - Epics 4-5: Admin configuration (required by pipeline)
- **Epic 6-7:** Sequential after all parallel tracks complete

---

## Functional Requirements Inventory

### User Account & Access (FR1-FR9)
| FR | Description |
|----|-------------|
| FR1 | Users can log in securely with email and password |
| FR2 | Users can reset passwords via email verification |
| FR3 | Users can update their profile information |
| FR4 | Platform Admin can create user accounts for SME clients |
| FR5 | Platform Admin can view and manage all user accounts |
| FR6 | Platform Admin can deactivate/reactivate user accounts |
| FR7 | System enforces role-based access (Platform Admin vs User) |
| FR8 | System automatically isolates data by user (each user only sees their own data) |
| FR9 | Platform Admin can view assessments across all users |

### Supplier Assessment Submission (FR10-FR16)
| FR | Description |
|----|-------------|
| FR10 | SME Users can submit a new supplier for assessment |
| FR11 | Supplier submission captures: name, country of operation, sector/commodity, website URL, and additional context |
| FR12 | System validates supplier submission for required fields before processing |
| FR13 | System initiates agentic assessment workflow upon valid submission |
| FR14 | Users receive confirmation that assessment has started |
| FR15 | Users can view real-time status of in-progress assessments |
| FR16 | Users can see progress indicators for each stage of the assessment workflow |

### Agentic Data Collection (FR17-FR28)
| FR | Description |
|----|-------------|
| FR17 | Data Collection Agent queries configured public data sources for supplier information |
| FR18 | Agent searches sanctions lists (global and country-specific) for supplier matches |
| FR19 | Agent searches corporate registries for company information |
| FR20 | Agent searches ESG databases for environmental, social, governance data |
| FR21 | Agent searches debarment lists for exclusion records |
| FR22 | Agent searches news and media sources for relevant coverage |
| FR23 | Agent crawls supplier website for self-reported information |
| FR24 | Agent processes admin-uploaded data files for matches |
| FR25 | Agent executes queries in parallel across multiple sources |
| FR26 | Agent implements retry logic for transient failures |
| FR27 | Agent respects ethical boundaries (robots.txt, no CAPTCHA bypass, no paywalled content) |
| FR28 | Agent records source URL, timestamp, and agent attribution for each data point collected |

### Evidence Analysis (FR29-FR35)
| FR | Description |
|----|-------------|
| FR29 | Evidence Analysis Agent processes all collected data from Data Collection Agent |
| FR30 | Agent tags each piece of evidence with source reliability rating (High/Medium/Low) |
| FR31 | Agent tags each piece of evidence with recency rating (Current/Recent/Dated/Stale) |
| FR32 | Agent tags each piece of evidence with relevance score to risk categories |
| FR33 | Agent identifies corroborating evidence across multiple sources |
| FR34 | Agent generates confidence score based on evidence quality and quantity |
| FR35 | Agent creates structured evidence log with full attribution |

### Risk Assessment (FR36-FR42)
| FR | Description |
|----|-------------|
| FR36 | Risk Assessment Agent applies admin-defined scoring criteria to analyzed evidence |
| FR37 | Agent calculates risk ratings for each configured risk category |
| FR38 | Agent produces overall risk score with confidence level |
| FR39 | Agent identifies and flags red flags based on admin-defined criteria |
| FR40 | Agent flags data quality issues where evidence is insufficient or conflicting |
| FR41 | Agent determines if Enhanced Due Diligence (EDD) is recommended |
| FR42 | Same inputs produce consistent risk scores within acceptable variance thresholds |

### Report Generation (FR43-FR51)
| FR | Description |
|----|-------------|
| FR43 | Report Generation Agent synthesizes all findings into structured report |
| FR44 | Report includes risk ratings per category with traffic light indicators |
| FR45 | Report includes confidence scores for each rating |
| FR46 | Report includes complete evidence log with clickable source links |
| FR47 | Report includes identified red flags with supporting evidence |
| FR48 | Report includes data quality warnings where applicable |
| FR49 | Report includes EDD recommendations when triggered |
| FR50 | Report includes actionable next steps based on risk profile |
| FR51 | All report content maintains full traceability to source evidence |

### Recommendations & Questionnaires (FR52-FR57)
| FR | Description |
|----|-------------|
| FR52 | System generates actionable recommendations based on assessment results |
| FR53 | System generates EDD recommendations when high-risk indicators detected |
| FR54 | System generates EDD recommendations when insufficient data detected |
| FR55 | System generates supplier questionnaire based on identified evidence gaps |
| FR56 | Questionnaire uses admin-provided templates as foundation |
| FR57 | AI tailors questionnaire questions to specific gaps identified for this supplier |

### Assessment & Report Management (FR58-FR63)
| FR | Description |
|----|-------------|
| FR58 | Users can view list of all their past supplier assessments |
| FR59 | Users can access and review historical assessment results |
| FR60 | Users can search/filter assessments by supplier name, date, risk level |
| FR61 | Users can export assessment report as PDF |
| FR62 | Users can export assessment data as CSV |
| FR63 | Users can delete their own individual assessments |

### Risk Framework Configuration - Admin (FR64-FR71)
| FR | Description |
|----|-------------|
| FR64 | Platform Admin can create risk categories (e.g., ESG, Modern Slavery, Financial) |
| FR65 | Platform Admin can define risk classifications within categories |
| FR66 | Platform Admin can configure scoring weights for each risk factor |
| FR67 | Platform Admin can set risk thresholds (what constitutes high/medium/low) |
| FR68 | Platform Admin can define evaluation rules for scoring |
| FR69 | Platform Admin can define red flag criteria and triggers |
| FR70 | Platform Admin can update risk frameworks; changes apply to new assessments |
| FR71 | Platform Admin can preview impact of framework changes before applying |

### Data Source Configuration - Admin (FR72-FR79)
| FR | Description |
|----|-------------|
| FR72 | Platform Admin can add new data sources to the system |
| FR73 | Data source configuration supports: API endpoints, credentials, file uploads, URL sources |
| FR74 | Platform Admin can designate data sources as global (all countries) or country-specific |
| FR75 | Platform Admin can test data source connectivity |
| FR76 | Platform Admin can enable/disable data sources |
| FR77 | Platform Admin can view data source status (active, error, disabled) |
| FR78 | Platform Admin can upload CSV/JSON files as supplementary data sources |
| FR79 | Platform Admin can update data source credentials |

### Country Configuration - Admin (FR80-FR84)
| FR | Description |
|----|-------------|
| FR80 | Platform Admin can add new countries to the system |
| FR81 | Platform Admin can configure country-specific data sources |
| FR82 | Platform Admin can configure country-specific evaluation parameters |
| FR83 | Platform Admin can enable/disable countries for assessment availability |
| FR84 | Platform Admin can view which data sources are configured for each country |

### AI-Assisted Data Source Discovery - Admin (FR85-FR91)
| FR | Description |
|----|-------------|
| FR85 | When adding a new country, system suggests relevant data sources |
| FR86 | AI suggestions include: corporate registries, sanctions lists, local ESG databases |
| FR87 | Platform Admin can review each AI suggestion |
| FR88 | Platform Admin can approve suggestions (adds to country config) |
| FR89 | Platform Admin can reject suggestions (excludes from config) |
| FR90 | Platform Admin can modify suggestions before approving |
| FR91 | System learns from admin decisions to improve future suggestions |

### System & Processing (FR92-FR96)
| FR | Description |
|----|-------------|
| FR92 | System processes assessments in background (non-blocking) |
| FR93 | System enforces configurable timeouts for agent tasks |
| FR94 | System continues processing when individual agents fail (graceful degradation) |
| FR95 | System marks assessment sections as incomplete when agent fails after retries |
| FR96 | System displays partial results with clear incomplete indicators |

**Total: 96 Functional Requirements**

---

## FR Coverage Map

| Epic | Title | FRs Covered | User Value |
|------|-------|-------------|------------|
| **1** | Foundation & Project Setup | Infrastructure for all FRs | Deployment-ready platform (Foundation exception) |
| **2** | User Authentication & Access | FR1-FR9 | Users can log in; Admin manages accounts |
| **3** | Supplier Submission & Status | FR10-FR16, FR92-FR96 | SMEs submit suppliers and track progress |
| **4** | Admin Risk Framework Config | FR64-FR71 | Consultancy customizes risk assessment rules |
| **5** | Admin Data Sources & Countries | FR72-FR91 | Platform expands to new data sources/countries |
| **6** | Agentic Assessment Pipeline | FR17-FR42 | Suppliers assessed automatically by AI agents |
| **7** | Results & Reporting | FR43-FR63 | Users view results, evidence, export reports |

**FR Coverage Validation:** All 96 FRs mapped ✅

---

## Epic 1: Foundation & Project Setup

**Goal:** Establish the technical foundation enabling all subsequent development — project structure, infrastructure, deployment pipeline, and development environment.

**User Value:** Platform is deployable and development can proceed efficiently. (Foundation exception — required for greenfield projects)

**FRs Enabled:** Infrastructure supporting all 96 FRs

---

### Story 1.1: Initialize Monorepo Structure

As a **developer**,
I want a well-organized monorepo with frontend and backend directories,
So that I can navigate the codebase efficiently and both systems can evolve independently.

**Acceptance Criteria:**

**Given** a new project repository
**When** the project structure is initialized
**Then** the following structure exists:
- `/frontend` - Next.js application
- `/backend` - FastAPI application
- `/docker-compose.yml` - Full stack compose
- `/.env.example` - Environment template
- `/README.md` - Setup instructions

**And** `.gitignore` excludes: `node_modules/`, `venv/`, `.env`, `__pycache__/`, `.next/`

**Prerequisites:** None (first story)

**Technical Notes:**
- Follow structure from Architecture doc section "Project Structure"
- Use kebab-case for directories
- Include both `docker-compose.yml` (production) and `docker-compose.dev.yml` (development)

---

### Story 1.2: Setup Backend Foundation (FastAPI)

As a **developer**,
I want a configured FastAPI backend with core dependencies,
So that I can build API endpoints following established patterns.

**Acceptance Criteria:**

**Given** the `/backend` directory exists
**When** the backend is initialized
**Then** the following is configured:
- Python 3.11+ virtual environment
- FastAPI 0.115.x with uvicorn
- SQLAlchemy 2.x with asyncpg driver
- Alembic for migrations
- Pydantic-settings for configuration
- structlog for JSON logging
- Directory structure: `app/api/`, `app/models/`, `app/schemas/`, `app/services/`, `app/core/`

**And** running `uvicorn app.main:app --reload` starts the server on port 8000
**And** `/health` endpoint returns `{"status": "ok"}`
**And** `/docs` shows OpenAPI documentation

**Prerequisites:** Story 1.1

**Technical Notes:**
- Per Architecture: `pip install fastapi uvicorn sqlalchemy asyncpg alembic pydantic-settings python-jose passlib structlog playwright`
- Per Architecture ADR-007: Install Playwright browser binaries: `playwright install chromium`
- Config via environment variables with pydantic-settings
- Use async sessions for all database operations
- Response envelope pattern from Architecture doc

---

### Story 1.3: Setup Frontend Foundation (Next.js + shadcn/ui)

As a **developer**,
I want a configured Next.js frontend with shadcn/ui components,
So that I can build UI screens following the UX design system.

**Acceptance Criteria:**

**Given** the `/frontend` directory exists
**When** the frontend is initialized
**Then** the following is configured:
- Next.js 15.x with App Router
- TypeScript in strict mode
- Tailwind CSS with custom color tokens (Warm Indigo theme per UX spec)
- shadcn/ui initialized with core components
- Directory structure: `src/app/`, `src/components/`, `src/lib/`, `src/hooks/`, `src/stores/`

**And** running `npm run dev` starts the server on port 3000
**And** the home page renders with shadcn/ui styling
**And** Tailwind config includes UX color palette:
  - Primary: `#6366f1` (Indigo)
  - Success: `#22c55e` (Green)
  - Warning: `#f59e0b` (Amber)
  - Error: `#ef4444` (Red)

**Prerequisites:** Story 1.1

**Technical Notes:**
- Init: `npx create-next-app@15 frontend --typescript --tailwind --eslint --app --src-dir`
- shadcn: `npx shadcn@3 init`
- Install core shadcn components: Button, Card, Input, Form, Table, Dialog, Toast, Badge, Tabs
- UX spec: "Warm Indigo" theme, slate neutrals, system font stack

---

### Story 1.4: Setup Database Infrastructure

As a **developer**,
I want PostgreSQL with pgvector running in Docker,
So that I can persist application data and evidence embeddings.

**Acceptance Criteria:**

**Given** Docker is installed
**When** `docker compose up postgres` is run
**Then** PostgreSQL 16.x container starts with:
- Database name: `sme`
- pgvector extension enabled
- Persistent volume for data
- Port 5432 exposed

**And** Alembic can connect and run migrations
**And** initial migration creates base tables structure

**Prerequisites:** Story 1.2

**Technical Notes:**
- Image: `pgvector/pgvector:pg16`
- Per Architecture: indexes on user_id, status, timestamps
- Soft delete pattern: `deleted_at` column on all tables
- Base model includes: `id` (UUID), `created_at`, `updated_at`, `deleted_at`

---

### Story 1.5: Setup Supporting Infrastructure (Redis + MinIO)

As a **developer**,
I want Redis and MinIO running in Docker,
So that I have caching, job queue, and file storage available.

**Acceptance Criteria:**

**Given** Docker is installed
**When** `docker compose up redis minio` is run
**Then**:
- Redis 7.x container starts on port 6379
- MinIO container starts with:
  - API on port 9000
  - Console on port 9001
  - Persistent volume for data

**And** backend can connect to Redis
**And** backend can upload/download files from MinIO

**Prerequisites:** Story 1.2

**Technical Notes:**
- Redis for: session cache, rate limiting, ARQ job queue
- MinIO for: admin-uploaded files (FR24, FR78), generated reports
- S3-compatible API via boto3/aioboto3

---

### Story 1.6: Configure Development Environment

As a **developer**,
I want documented setup instructions and dev tooling,
So that new developers can onboard quickly and maintain code quality.

**Acceptance Criteria:**

**Given** all infrastructure components are configured
**When** a developer follows README instructions
**Then** they can:
- Start all services with `docker compose -f docker-compose.dev.yml up`
- Run backend with hot reload
- Run frontend with hot reload
- Run database migrations
- Execute tests

**And** the following dev tools are configured:
- Backend: pytest, black, ruff, mypy
- Frontend: ESLint, Prettier
- Pre-commit hooks for formatting

**And** `.env.example` contains all required environment variables with descriptions

**Prerequisites:** Stories 1.2, 1.3, 1.4, 1.5

**Technical Notes:**
- Per Architecture: Python 3.11+, Node.js 24 LTS
- Environment variables per Architecture "Environment Variables" section
- Document: DATABASE_URL, REDIS_URL, MINIO_URL, OPENAI_API_KEY, JWT_SECRET

---

### Story 1.7: Setup Fully Dockerized Development Environment

As a **non-technical team member** (QA, designer, new developer),
I want to run the entire development stack with a single Docker command,
So that I can work on the project without installing Python, Node.js, or managing dependencies locally.

**Acceptance Criteria:**

**Given** Docker and Docker Compose are installed on the developer's machine
**When** the developer runs `docker compose -f docker-compose.dev-full.yml up`
**Then** all services start successfully:
- Frontend accessible at `http://localhost:3000` with hot-reload
- Backend API accessible at `http://localhost:8000` with hot-reload
- API documentation accessible at `http://localhost:8000/docs`
- PostgreSQL, Redis, MinIO running and connected

**And** hot-reload works for both frontend and backend:
- Changes to `backend/app/**/*.py` trigger automatic reload
- Changes to `frontend/src/**/*` trigger Next.js HMR

**And** developers can run migrations via:
```bash
docker compose -f docker-compose.dev-full.yml exec backend alembic upgrade head
```

**And** developers can run tests via:
```bash
docker compose -f docker-compose.dev-full.yml exec backend pytest
docker compose -f docker-compose.dev-full.yml exec frontend npm test
```

**Prerequisites:** Stories 1.2, 1.3, 1.4, 1.5, 1.6

**Technical Notes:**
- Per Architecture ADR-006: Dual Development Environment Strategy
- Per Architecture ADR-007: Playwright + Chromium for web scraping (must be installed in Docker images)
- Backend: Volume mount `./backend/app` to `/app/app`, use `uvicorn --reload`
- Backend Dockerfile.dev must include: Playwright system deps + `playwright install chromium`
- Frontend: Volume mount `./frontend/src` to `/app/src`, anonymous volume for `node_modules`
- Create `docker-compose.dev-full.yml` with all services
- Document both dev environment options in README

**Deliverables:**
1. `docker-compose.dev-full.yml` - Full stack with hot-reload
2. `backend/Dockerfile.dev` - Development Dockerfile with Playwright + Chromium browser binaries
3. `frontend/Dockerfile.dev` - Development Dockerfile with dev dependencies
4. Updated README with Option B setup instructions

---

## Epic 2: User Authentication & Access

**Goal:** Enable secure user authentication, role-based access control, and per-user data isolation — the foundation for multi-user platform security.

**User Value:** Users can log in securely; Admin can manage user accounts; each user's data is protected from other users.

**FRs Covered:** FR1, FR2, FR3, FR4, FR5, FR6, FR7, FR8, FR9

---

### Story 2.0: Setup Playwright E2E Testing Infrastructure

As a **developer**,
I want Playwright configured for end-to-end testing,
So that I can write and run E2E tests for authentication flows and other critical user journeys.

**Acceptance Criteria:**

**Given** the frontend foundation exists
**When** the Playwright setup is complete
**Then** the following is configured:
- `@playwright/test` package installed as devDependency
- Playwright browsers installed (`npx playwright install`)
- `playwright.config.ts` with:
  - Base URL pointing to `http://localhost:3000`
  - Projects for chromium, firefox, webkit
  - Screenshots on failure
  - HTML reporter configured
- Directory structure: `e2e/` for test files

**And** npm scripts are available:
- `npm run test:e2e` - Run all E2E tests
- `npm run test:e2e:ui` - Run E2E tests with Playwright UI
- `npm run test:e2e:headed` - Run E2E tests in headed mode

**And** a sample smoke test exists:
- `e2e/smoke.spec.ts` that verifies the homepage loads
- Test passes when run against dev server

**Prerequisites:** Story 1.3 (Frontend Foundation)

**Technical Notes:**
- Per Architecture: E2E tests complement unit tests (Vitest) for integration coverage
- Per Epic 1 Retrospective recommendation: "Include test scripts in scaffolding stories"
- Configure `.gitignore` to exclude `playwright-report/`, `test-results/`
- This enables auth flow testing in subsequent Epic 2 stories

---

### Story 2.1: Implement User Data Model and Migrations

As a **developer**,
I want the User database model with role support,
So that I can persist user accounts and enforce access control.

**Acceptance Criteria:**

**Given** the database infrastructure exists
**When** the User model migration is applied
**Then** the `users` table exists with columns:
- `id` (UUID, primary key)
- `email` (string, unique, not null)
- `password_hash` (string, not null)
- `role` (enum: 'admin', 'user')
- `is_active` (boolean, default true)
- `last_login_at` (timestamp, nullable)
- `created_at`, `updated_at`, `deleted_at` (timestamps)

**And** index exists on `email` column
**And** soft delete is enforced (queries filter `deleted_at IS NULL`)

**Prerequisites:** Story 1.4 (Database Infrastructure)

**Technical Notes:**
- Per Architecture: SQLAlchemy model in `app/models/user.py`
- Pydantic schemas in `app/schemas/user.py`: `UserCreate`, `UserResponse`, `UserUpdate`
- Role enum: `Literal["admin", "user"]`

---

### Story 2.2: Implement Password Hashing and JWT Authentication

As a **developer**,
I want secure password handling and JWT token generation,
So that user credentials are protected and sessions are stateless.

**Acceptance Criteria:**

**Given** the User model exists
**When** a password is stored
**Then** it is hashed using Argon2id algorithm

**And** when a JWT token is generated, it contains:
- `sub` (user ID)
- `role` (admin/user)
- `exp` (expiration: 24 hours for access token)

**And** JWT tokens are signed with `JWT_SECRET` using HS256 algorithm
**And** password verification returns boolean without timing attacks

**Prerequisites:** Story 2.1

**Technical Notes:**
- Per Architecture NFR1: Argon2id via `passlib`
- JWT via `python-jose`
- Access token: 24h expiry; Refresh token: 7d expiry
- Store in `app/core/security.py`: `hash_password()`, `verify_password()`, `create_access_token()`

---

### Story 2.3: Implement Login Endpoint (FR1)

As an **SME user**,
I want to log in with my email and password,
So that I can access my supplier assessments securely.

**Acceptance Criteria:**

**Given** I have a valid user account
**When** I POST to `/api/v1/auth/login` with correct email and password
**Then** I receive a 200 response with:
- `access_token` (JWT)
- `token_type: "bearer"`
- `expires_in` (seconds)

**And** `last_login_at` is updated on my user record
**And** login attempt is logged (structlog)

**Given** I provide incorrect credentials
**When** I POST to `/api/v1/auth/login`
**Then** I receive 401 with error code `UNAUTHORIZED`
**And** no timing difference reveals whether email exists

**Prerequisites:** Story 2.2

**Technical Notes:**
- Endpoint: `POST /api/v1/auth/login`
- Request body: `{"email": string, "password": string}`
- Per Architecture NFR9: Log security events
- Rate limiting (future): 5 attempts/hour/IP

---

### Story 2.4: Implement Frontend Login Page (FR1)

As an **SME user**,
I want a clean login form,
So that I can authenticate and access my dashboard.

**Acceptance Criteria:**

**Given** I navigate to `/login`
**When** the page loads
**Then** I see a centered login form with:
- Email input field (required, email validation)
- Password input field (required, with visibility toggle)
- "Remember me" checkbox
- "Login" button (primary, Indigo)
- "Forgot password?" link

**And** when I submit valid credentials:
- Loading spinner appears on button
- On success: redirect to `/dashboard`
- On error: inline error message below form (red, 14px)

**And** form is responsive (full-width on mobile, centered card on desktop)
**And** keyboard navigation works (Tab order, Enter to submit)

**Prerequisites:** Stories 1.3, 2.3

**Technical Notes:**
- Per UX spec: Guided wizard feel, reassuring feedback
- Use shadcn/ui: Card, Input, Button, Form
- NextAuth.js for client-side auth state
- Store JWT in HTTP-only cookie (not localStorage)
- Error states: "Invalid email or password" (never reveal which)

---

### Story 2.5: Implement Password Reset Flow (FR2)

As an **SME user**,
I want to reset my password via email,
So that I can regain access if I forget my credentials.

**Acceptance Criteria:**

**Given** I click "Forgot password?" on login page
**When** I enter my email and submit
**Then** I see "If an account exists, you'll receive a reset link"
**And** if the email exists, a reset token is generated (expires in 1 hour)
**And** email is sent with reset link (MVP: log to console, email service deferred)

**Given** I have a valid reset token
**When** I navigate to `/reset-password?token=xxx`
**Then** I can enter a new password (with confirmation field)
**And** on submit, password is updated and token is invalidated
**And** I'm redirected to login with success message

**Prerequisites:** Story 2.4

**Technical Notes:**
- Endpoints: `POST /api/v1/auth/password-reset`, `POST /api/v1/auth/password-reset/confirm`
- Store reset tokens in DB with expiry (or use signed JWT with short expiry)
- Per UX: Gentle error handling, never reveal if email exists

---

### Story 2.6: Implement User Profile Management (FR3)

As an **SME user**,
I want to view and update my profile information,
So that I can keep my account details current.

**Acceptance Criteria:**

**Given** I am logged in
**When** I navigate to `/profile` or click my avatar
**Then** I see my profile with:
- Email (read-only display)
- Name fields (editable, if we add name columns)
- "Change Password" section
- "Save Changes" button

**And** when I update my password:
- Current password required
- New password + confirmation
- Password strength indicator (visual feedback)
- Success toast on save

**Prerequisites:** Story 2.4

**Technical Notes:**
- Endpoint: `PATCH /api/v1/users/me`
- Per Architecture: `GET /api/v1/users/me` returns current user
- Password change: validate current password before update
- UX: Toast notification (top-right, auto-dismiss 5s)

---

### Story 2.7: Implement Admin User Management (FR4, FR5, FR6)

As a **Platform Admin**,
I want to create and manage SME user accounts,
So that I can onboard new clients and control access.

**Acceptance Criteria:**

**Given** I am logged in as Admin
**When** I navigate to `/admin/users`
**Then** I see a data table with all users:
- Email, Role, Status (Active/Inactive), Created Date, Last Login
- Search/filter by email
- Pagination (20 per page)

**And** I can click "Add User" to open a modal:
- Email (required, validated)
- Temporary password (auto-generated or manual)
- Role selector (User is default)
- "Create" button

**And** I can click a user row to:
- View user details
- Deactivate/Reactivate account (toggle)
- Cannot delete (soft-delete only via deactivate)

**Given** I create a new user
**Then** they receive a welcome email with temporary password (MVP: log to console)

**Prerequisites:** Story 2.4

**Technical Notes:**
- Endpoints per Architecture:
  - `GET /api/v1/users` (admin only)
  - `POST /api/v1/users` (admin only)
  - `PATCH /api/v1/users/{id}` (admin only)
- Per UX: Admin uses sidebar navigation, data tables with filtering
- `is_active: false` = deactivated (cannot login)

---

### Story 2.8: Implement Role-Based Access Control (FR7, FR8, FR9)

As the **system**,
I want to enforce role-based permissions and data isolation,
So that users only access what they're authorized to see.

**Acceptance Criteria:**

**Given** a request with valid JWT
**When** the endpoint requires authentication
**Then** the `current_user` dependency extracts user from token
**And** the user is verified as `is_active: true`

**Given** an endpoint is admin-only (e.g., `/api/v1/users`)
**When** a regular user attempts access
**Then** they receive 403 `FORBIDDEN`

**Given** a user queries their assessments
**When** the service layer executes
**Then** queries automatically filter by `user_id = current_user.id`
**And** no other user's data is returned

**Given** an admin queries assessments
**When** they use `/api/v1/admin/assessments` (or view all flag)
**Then** they can see all users' assessments (FR9)

**Prerequisites:** Story 2.3

**Technical Notes:**
- Per Architecture "Data Isolation Pattern":
  - Service layer enforces `user_id` filter on all user-scoped queries
  - Admin endpoints use separate routes or explicit `view_all` flag
- Dependencies in `app/core/deps.py`:
  - `get_current_user` - extracts and validates JWT
  - `get_current_admin` - requires role == 'admin'
- Middleware logs authorization failures

---

## Epic 3: Supplier Submission & Status Tracking

**Goal:** Enable SME users to submit suppliers for assessment and track real-time progress — the core "gateway interaction" that defines the product experience.

**User Value:** SMEs can submit a supplier and watch the AI investigate in real-time, knowing exactly what's happening and when results will be ready.

**FRs Covered:** FR10, FR11, FR12, FR13, FR14, FR15, FR16, FR92, FR93, FR94, FR95, FR96

---

### Story 3.1: Implement Supplier and Assessment Data Models

As a **developer**,
I want Supplier and Assessment database models,
So that I can persist supplier information and track assessment state.

**Acceptance Criteria:**

**Given** the database infrastructure exists
**When** migrations are applied
**Then** the `suppliers` table exists with:
- `id` (UUID, primary key)
- `user_id` (UUID, FK → users.id, not null)
- `name` (string, not null)
- `country_code` (string, not null)
- `sector` (string, not null)
- `website_url` (string, nullable)
- `context` (text, nullable)
- `created_at`, `updated_at`, `deleted_at`

**And** the `assessments` table exists with:
- `id` (UUID, primary key)
- `user_id` (UUID, FK → users.id, not null)
- `supplier_id` (UUID, FK → suppliers.id, not null)
- `status` (enum: queued, collecting, analyzing, scoring, generating, complete, failed)
- `overall_risk_level` (enum: low, medium, high, nullable)
- `overall_confidence` (enum: low, medium, high, nullable)
- `progress_pct` (integer, 0-100)
- `started_at`, `completed_at` (timestamps, nullable)
- `error_message` (text, nullable)
- `created_at`, `updated_at`, `deleted_at`

**And** indexes exist on: `suppliers.user_id`, `assessments.user_id`, `assessments.status`

**Prerequisites:** Story 2.1

**Technical Notes:**
- Per Architecture: models in `app/models/supplier.py`, `app/models/assessment.py`
- Status enum matches workflow nodes: queued → collecting → analyzing → scoring → generating → complete
- `user_id` filter enforced in all queries (data isolation)

---

### Story 3.2: Implement Supplier Submission API (FR10, FR11, FR12, FR13, FR14)

As an **SME user**,
I want to submit a supplier for assessment via API,
So that the system can start investigating them.

**Acceptance Criteria:**

**Given** I am authenticated
**When** I POST to `/api/v1/assessments` with supplier data:
```json
{
  "supplier_name": "Acme Corp",
  "country_code": "CA",
  "sector": "Manufacturing",
  "website_url": "https://acme.com",
  "context": "Potential new vendor for raw materials"
}
```
**Then** the system:
1. Validates required fields (name, country_code, sector)
2. Creates a Supplier record (or links to existing)
3. Creates an Assessment record with status: `queued`
4. Enqueues assessment job to ARQ worker
5. Returns 201 with assessment ID and status

**And** response includes:
```json
{
  "data": {
    "id": "uuid",
    "supplier_id": "uuid",
    "status": "queued",
    "created_at": "timestamp"
  }
}
```

**Given** required fields are missing
**When** I POST to `/api/v1/assessments`
**Then** I receive 400 `VALIDATION_ERROR` with field-specific messages

**Prerequisites:** Story 3.1, Story 2.8

**Technical Notes:**
- Endpoint: `POST /api/v1/assessments`
- Per Architecture: ARQ task `run_assessment(assessment_id)`
- Supplier lookup: check if same user already has supplier with same name+country
- Per FR13: Assessment workflow triggered asynchronously

---

### Story 3.3: Implement ARQ Worker and Job Queue (FR92, FR93)

As the **system**,
I want background job processing for assessments,
So that users aren't blocked waiting for long-running AI tasks.

**Acceptance Criteria:**

**Given** an assessment is queued
**When** the ARQ worker picks up the job
**Then** it:
1. Updates assessment status to `collecting`
2. Executes the assessment workflow (stub for now)
3. Updates status through each stage
4. Sets `completed_at` on completion

**And** jobs have configurable timeout (default: 30 minutes)
**And** failed jobs are retried up to 3 times
**And** after max retries, status is set to `failed` with error message

**Given** the worker is running
**When** I check `arq` health
**Then** it shows connected workers and pending jobs

**Prerequisites:** Story 1.5 (Redis), Story 3.2

**Technical Notes:**
- Per Architecture: `app/workers/worker.py`, `app/workers/tasks.py`
- ARQ settings: 4 workers, max 10 concurrent jobs, 30min timeout
- Task: `async def run_assessment(ctx, assessment_id: str)`
- Status updates via direct DB writes (worker has DB access)

---

### Story 3.4: Implement Real-Time Status Updates via SSE (FR15, FR16)

As an **SME user**,
I want to see real-time progress updates,
So that I know the system is working and when results will be ready.

**Acceptance Criteria:**

**Given** I have a pending assessment
**When** I connect to `/api/v1/assessments/{id}/status` (SSE endpoint)
**Then** I receive server-sent events with:
```
event: status
data: {"status": "collecting", "progress_pct": 25, "current_stage": "Searching public sources..."}

event: status
data: {"status": "analyzing", "progress_pct": 50, "current_stage": "Analyzing evidence..."}

event: status
data: {"status": "complete", "progress_pct": 100, "current_stage": "Assessment complete"}
```

**And** connection stays open until assessment completes or fails
**And** heartbeat events sent every 30s to keep connection alive
**And** on completion, final event includes `result_available: true`

**Prerequisites:** Story 3.3

**Technical Notes:**
- Per Architecture ADR-004: SSE over WebSockets
- Endpoint: `GET /api/v1/assessments/{id}/status` with `text/event-stream`
- Worker publishes status to Redis pub/sub channel `assessment:{id}`
- SSE endpoint subscribes and forwards to client
- Auto-reconnect handled by browser EventSource API

---

### Story 3.5: Implement Supplier Submission Wizard UI (FR10, FR11, FR14)

As an **SME user**,
I want a guided wizard to submit a supplier,
So that I can easily provide the right information and feel confident about what happens next.

**Acceptance Criteria:**

**Given** I click "New Assessment" on my dashboard
**When** the wizard opens
**Then** I see a 4-step wizard:

**Step 1: Basic Info**
- Supplier Name* (text input, required)
- Country* (dropdown, Canada selected by default for MVP)
- Website URL (text input, optional, URL validation)
- "Continue" button (disabled until required fields filled)

**Step 2: Context**
- Sector/Commodity* (dropdown or combobox)
- Additional Context (textarea, optional, placeholder: "Any specific concerns or information...")
- "Back" and "Continue" buttons

**Step 3: Review**
- Summary card showing all entered information
- Checkbox: "I confirm this information is accurate"
- "Back" and "Start Assessment" buttons

**Step 4: Confirmation**
- Success animation/icon
- "Assessment started! We're now investigating [Supplier Name]"
- Progress indicator showing "Queued"
- "View Progress" button → navigates to assessment detail
- "Return to Dashboard" button

**And** wizard is centered on desktop, full-screen on mobile
**And** step indicator shows progress (1 → 2 → 3 → 4)
**And** keyboard navigation works throughout

**Prerequisites:** Stories 2.4, 3.2

**Technical Notes:**
- Per UX spec: "Core Experience" — must feel effortless and clear
- Use shadcn/ui: Card, Input, Select, Textarea, Button, Progress
- Per UX: WizardStepper component for progress indication
- Form state managed with React Hook Form + Zod validation
- On submit: POST to API, show confirmation, then offer navigation

---

### Story 3.6: Implement Assessment Status Tracking UI (FR15, FR16)

As an **SME user**,
I want to see my assessment's progress in real-time,
So that I know the system is working and can estimate when results are ready.

**Acceptance Criteria:**

**Given** I navigate to `/assessments/{id}` for a pending assessment
**When** the page loads
**Then** I see:
- Supplier name and submission date
- Current status with animated indicator
- Progress bar showing percentage complete
- Stage indicator: Collecting → Analyzing → Scoring → Generating → Complete
- Elapsed time since started

**And** the UI updates in real-time via SSE:
- Progress bar animates smoothly
- Current stage highlights change
- Stage descriptions update ("Searching sanctions lists...", "Analyzing evidence quality...")

**Given** assessment completes
**When** status changes to `complete`
**Then** I see:
- "Assessment Complete" with success icon
- "View Results" button (prominent)
- Time taken displayed

**Given** assessment fails
**When** status changes to `failed`
**Then** I see:
- "Assessment Incomplete" with warning icon
- Error message (user-friendly, no stack traces)
- "Retry Assessment" button
- "Contact Support" link

**Prerequisites:** Stories 3.4, 3.5

**Technical Notes:**
- Per UX: AssessmentStatusTracker component
- Per UX: "Status visibility — users know system is working"
- Use EventSource API for SSE connection
- Skeleton loader while initial status loads
- Per UX: "Collecting → Analyzing → Scoring → Complete" stages

---

### Story 3.7: Implement Graceful Degradation and Partial Results (FR94, FR95, FR96)

As the **system**,
I want to handle failures gracefully and show partial results,
So that users get value even when some data sources fail.

**Acceptance Criteria:**

**Given** a data source fails during collection
**When** the worker processes the assessment
**Then** it:
1. Logs the failure with source name and error
2. Continues with remaining sources
3. Marks the failed source in assessment metadata
4. Completes assessment with available data

**And** the assessment record includes:
- `incomplete_sources`: ["source_name_1", "source_name_2"]
- `warnings`: ["Could not access ESG Database - data may be incomplete"]

**Given** all sources fail
**When** no evidence is collected
**Then** assessment status is `failed` with message: "Unable to collect data from any sources. Please try again later."

**Given** assessment has partial results
**When** user views results
**Then** they see:
- Clear indicator: "⚠️ Some data sources were unavailable"
- List of unavailable sources
- Results based on available data
- Confidence scores reflect data quality

**Prerequisites:** Story 3.3

**Technical Notes:**
- Per Architecture: "Single source fails → Log error, continue with others"
- Per PRD NFR10: "Graceful degradation; partial results better than no results"
- Store incomplete sources in JSONB column on assessment
- UI shows warning banner when `incomplete_sources` is non-empty

---

## Epic 4: Admin Risk Framework Configuration

**Goal:** Enable the consultancy admin to configure risk assessment rules, categories, scoring weights, thresholds, and red flag criteria — embedding their domain expertise into the platform.

**User Value:** The consultancy can customize how suppliers are evaluated without developer help, ensuring assessments reflect their professional standards and client needs.

**FRs Covered:** FR64, FR65, FR66, FR67, FR68, FR69, FR70, FR71

---

### Story 4.1: Implement Risk Framework Data Model

As a **developer**,
I want the Risk Framework database model,
So that I can persist admin-configured assessment rules.

**Acceptance Criteria:**

**Given** the database infrastructure exists
**When** the migration is applied
**Then** the `risk_frameworks` table exists with:
- `id` (UUID, primary key)
- `name` (string, not null, e.g., "Default Framework")
- `description` (text, nullable)
- `categories` (JSONB) - list of risk category definitions
- `scoring_rules` (JSONB) - scoring configuration
- `thresholds` (JSONB) - low/medium/high boundaries
- `red_flag_criteria` (JSONB) - trigger definitions
- `questionnaire_templates` (JSONB) - base questions per category
- `is_active` (boolean, default false)
- `version` (integer, default 1)
- `created_at`, `updated_at`, `deleted_at`

**And** only one framework can be `is_active = true` at a time
**And** seed data includes a default framework with:
- Categories: ESG, Modern Slavery, Financial
- Default thresholds: Low (0-33), Medium (34-66), High (67-100)
- Basic red flag criteria

**Prerequisites:** Story 1.4

**Technical Notes:**
- Per Architecture: `app/models/risk_framework.py`
- JSONB allows flexible schema evolution
- Version column supports framework history tracking
- Categories schema example:
```json
{
  "categories": [
    {
      "code": "esg",
      "name": "ESG",
      "weight": 0.4,
      "classifications": ["environmental", "social", "governance"]
    }
  ]
}
```

---

### Story 4.2: Implement Risk Framework API (FR64, FR65, FR66, FR67, FR68, FR69, FR70)

As a **Platform Admin**,
I want API endpoints to manage risk frameworks,
So that I can configure assessment rules programmatically.

**Acceptance Criteria:**

**Given** I am authenticated as Admin
**When** I call risk framework endpoints
**Then**:

**GET `/api/v1/admin/risk-frameworks`:**
- Returns list of all frameworks with summary info
- Includes: id, name, is_active, version, updated_at

**GET `/api/v1/admin/risk-frameworks/{id}`:**
- Returns full framework configuration
- Includes all JSONB fields expanded

**POST `/api/v1/admin/risk-frameworks`:**
- Creates new framework (inactive by default)
- Validates required fields
- Returns created framework

**PATCH `/api/v1/admin/risk-frameworks/{id}`:**
- Updates framework configuration
- Increments version number
- Changes apply to new assessments only (FR70)
- Returns updated framework

**DELETE `/api/v1/admin/risk-frameworks/{id}`:**
- Soft-deletes framework
- Cannot delete active framework

**POST `/api/v1/admin/risk-frameworks/{id}/activate`:**
- Sets this framework as active
- Deactivates previously active framework

**And** non-admin users receive 403 FORBIDDEN

**Prerequisites:** Story 4.1, Story 2.8

**Technical Notes:**
- Per Architecture: Admin endpoints under `/api/v1/admin/`
- Validation: categories must have unique codes, weights must sum to 1.0
- Active framework loaded by assessment workflow

---

### Story 4.3: Implement Risk Categories Management UI (FR64, FR65)

As a **Platform Admin**,
I want to create and manage risk categories,
So that I can define what aspects of suppliers are evaluated.

**Acceptance Criteria:**

**Given** I navigate to `/admin/risk-frameworks`
**When** I select a framework and click "Edit Categories"
**Then** I see a configuration interface with:

**Category List:**
- Table showing: Name, Code, Weight, Classifications count, Actions
- Drag-to-reorder capability
- "Add Category" button

**Add/Edit Category Modal:**
- Name* (text input)
- Code* (auto-generated from name, editable)
- Description (textarea)
- Weight* (number input, 0-1)
- Classifications (tag input - add multiple)
  - e.g., for ESG: "environmental", "social", "governance"

**Validations:**
- Category codes must be unique
- Weights must be between 0 and 1
- At least one category required

**And** changes are saved to draft until "Save Framework" clicked
**And** total weight indicator shows if weights don't sum to 1.0

**Prerequisites:** Story 4.2, Story 2.7

**Technical Notes:**
- Per UX: Admin uses sidebar navigation, data tables
- Form validation with Zod
- Show warning if weights don't equal 1.0 (allow save with warning)
- Classifications used for evidence tagging in Epic 4

---

### Story 4.4: Implement Scoring Configuration UI (FR66, FR67, FR68)

As a **Platform Admin**,
I want to configure scoring weights and thresholds,
So that I can control how risk scores are calculated.

**Acceptance Criteria:**

**Given** I'm editing a risk framework
**When** I click "Scoring Configuration"
**Then** I see:

**Threshold Configuration (FR67):**
- Visual slider or input fields for boundaries:
  - Low Risk: 0 to [X]
  - Medium Risk: [X] to [Y]
  - High Risk: [Y] to 100
- Live preview showing color bands

**Scoring Rules (FR66, FR68):**
- Per category configuration:
  - Evidence weight multipliers by reliability (High: 1.0, Medium: 0.7, Low: 0.4)
  - Recency decay settings
  - Minimum evidence threshold (e.g., "need at least 2 sources")

**Evaluation Rules (FR68):**
- Rule builder interface:
  - IF [condition] THEN [action]
  - Example: "IF sanctions_match THEN score += 50"
  - Example: "IF no_evidence THEN confidence = low"
- Predefined rule templates available

**And** changes preview shows "Before/After" comparison
**And** validation prevents invalid configurations

**Prerequisites:** Story 4.3

**Technical Notes:**
- Per UX: Clean config UI, no JSON editing required
- Store as structured JSONB, not free-form
- Evaluation rules use simple DSL or structured format
- Consider: rule validation to prevent conflicts

---

### Story 4.5: Implement Red Flag Configuration UI (FR69)

As a **Platform Admin**,
I want to define red flag criteria and triggers,
So that serious risk indicators are automatically flagged.

**Acceptance Criteria:**

**Given** I'm editing a risk framework
**When** I click "Red Flag Criteria"
**Then** I see:

**Red Flag List:**
- Table: Name, Trigger Condition, Severity, Category, Actions
- "Add Red Flag" button

**Add/Edit Red Flag Modal:**
- Name* (e.g., "Sanctions Match")
- Description (what this flag means)
- Severity* (Critical / High / Medium)
- Category (which risk category, or "All")
- Trigger Condition*:
  - Dropdown: evidence_type_match, keyword_match, score_threshold, custom
  - Configuration based on type:
    - evidence_type_match: "sanctions" = true
    - keyword_match: ["forced labor", "child labor"]
    - score_threshold: category_score > 80

**And** red flags are evaluated during risk assessment (Epic 6)
**And** triggered flags appear in reports with supporting evidence

**Prerequisites:** Story 4.4

**Technical Notes:**
- Red flag schema:
```json
{
  "red_flags": [
    {
      "code": "sanctions_match",
      "name": "Sanctions List Match",
      "severity": "critical",
      "category": "all",
      "trigger": {
        "type": "evidence_type_match",
        "config": { "source_type": "sanctions", "match": true }
      }
    }
  ]
}
```
- Risk Assessment node loads these criteria (Story 4.6)

---

### Story 4.6: Implement Framework Preview and Activation (FR70, FR71)

As a **Platform Admin**,
I want to preview framework changes before applying them,
So that I can understand the impact on assessments.

**Acceptance Criteria:**

**Given** I have made changes to a risk framework
**When** I click "Preview Changes" (FR71)
**Then** I see:

**Change Summary:**
- List of what changed (categories, thresholds, rules, red flags)
- Side-by-side comparison with current active framework
- Highlight additions (green), removals (red), modifications (yellow)

**Impact Preview:**
- "Run sample assessment" option (optional enhancement)
- Warning if changes are significant:
  - "Threshold changes may affect 40% of risk classifications"
  - "New red flag criteria will flag additional evidence"

**Given** I click "Activate Framework" (FR70)
**When** activation completes
**Then**:
- This framework becomes `is_active = true`
- Previous active framework becomes `is_active = false`
- Version is incremented
- Success toast: "Framework activated. Changes apply to new assessments."
- Existing assessments are NOT affected

**And** I can revert to previous framework version

**Prerequisites:** Story 4.5

**Technical Notes:**
- Per FR70: Changes apply to NEW assessments only
- Store framework history (versions) for rollback
- Preview diff using JSON comparison
- Consider: "Test with sample supplier" feature for MVP+

---

## Epic 5: Admin Data Source & Country Management

**Goal:** Enable the consultancy admin to configure data sources, manage country availability, and leverage AI-assisted discovery to rapidly expand geographic coverage.

**User Value:** The consultancy can add new data sources and countries without developer help, and AI assists in discovering relevant sources for new markets — enabling rapid international expansion.

**FRs Covered:** FR72, FR73, FR74, FR75, FR76, FR77, FR78, FR79, FR80, FR81, FR82, FR83, FR84, FR85, FR86, FR87, FR88, FR89, FR90, FR91

---

### Story 5.1: Implement Data Source and Country Data Models

As a **developer**,
I want Data Source and Country database models,
So that I can persist configuration for evidence collection.

**Acceptance Criteria:**

**Given** the database infrastructure exists
**When** migrations are applied
**Then** the `data_sources` table exists with:
- `id` (UUID, primary key)
- `name` (string, not null, e.g., "OSFI Sanctions List")
- `description` (text, nullable)
- `source_type` (enum: api, file, url, scrape)
- `config` (JSONB) - connection details, credentials (encrypted)
- `country_code` (string, nullable - NULL means global)
- `is_enabled` (boolean, default true)
- `last_health_check` (timestamp, nullable)
- `health_status` (enum: healthy, degraded, failed, nullable)
- `created_at`, `updated_at`, `deleted_at`

**And** the `countries` table exists with:
- `code` (string, primary key - ISO 3166-1 alpha-2)
- `name` (string, not null)
- `is_enabled` (boolean, default false)
- `config` (JSONB) - country-specific parameters
- `created_at`, `updated_at`

**And** seed data includes:
- Canada (CA) enabled with basic config
- Global data sources (sanctions lists, etc.)

**Prerequisites:** Story 1.4

**Technical Notes:**
- Per Architecture: `app/models/data_source.py`, `app/models/country.py`
- Config JSONB for data sources:
```json
{
  "api": {
    "base_url": "https://api.example.com",
    "auth_type": "api_key",
    "credentials_ref": "encrypted_key_id"
  }
}
```
- Credentials stored encrypted, referenced by ID

---

### Story 5.2: Implement Data Source Management API (FR72, FR73, FR74, FR76, FR77, FR79)

As a **Platform Admin**,
I want API endpoints to manage data sources,
So that I can configure where evidence is collected from.

**Acceptance Criteria:**

**Given** I am authenticated as Admin
**When** I call data source endpoints
**Then**:

**GET `/api/v1/admin/data-sources`:**
- Returns list of all data sources
- Filterable by: country_code, source_type, is_enabled, health_status
- Includes: id, name, source_type, country_code, is_enabled, health_status

**GET `/api/v1/admin/data-sources/{id}`:**
- Returns full data source config
- Credentials masked (show `***` not actual values)

**POST `/api/v1/admin/data-sources`:**
- Creates new data source (FR72)
- Supports all source_types (FR73):
  - `api`: base_url, auth config
  - `file`: references uploaded file in MinIO
  - `url`: URL to fetch
  - `scrape`: URL + scraping rules
- `country_code` null = global (FR74)
- Returns created source

**PATCH `/api/v1/admin/data-sources/{id}`:**
- Updates configuration
- Can update credentials (FR79)
- Can enable/disable (FR76)

**DELETE `/api/v1/admin/data-sources/{id}`:**
- Soft-deletes data source

**And** health_status reflects last connectivity test (FR77)

**Prerequisites:** Story 5.1, Story 2.8

**Technical Notes:**
- Per Architecture: Admin endpoints
- Encrypt credentials before storage
- health_status updated by health check job or manual test

---

### Story 5.3: Implement Data Source Connectivity Test (FR75)

As a **Platform Admin**,
I want to test data source connectivity,
So that I can verify configurations work before using them.

**Acceptance Criteria:**

**Given** I have configured a data source
**When** I call `POST /api/v1/admin/data-sources/{id}/test`
**Then** the system:
1. Attempts to connect using stored configuration
2. For API: makes test request to health/ping endpoint
3. For URL/scrape: attempts to fetch and parse
4. For file: verifies file exists and is readable

**And** response includes:
```json
{
  "status": "success" | "failed",
  "latency_ms": 234,
  "message": "Connection successful" | "Error: Connection refused",
  "tested_at": "timestamp"
}
```

**And** `health_status` and `last_health_check` are updated on the data source
**And** UI shows real-time test results with loading indicator

**Prerequisites:** Story 5.2

**Technical Notes:**
- Timeout: 30 seconds
- For scrape sources: verify robots.txt allows access
- Don't store full response, just status
- Consider: scheduled health checks (cron job)

---

### Story 5.4: Implement File Upload for Data Sources (FR78)

As a **Platform Admin**,
I want to upload CSV/JSON files as data sources,
So that I can supplement automated sources with curated data.

**Acceptance Criteria:**

**Given** I'm creating a new data source with type "file"
**When** I upload a file
**Then**:
- Accepted formats: CSV, JSON
- Max file size: 50MB
- File is validated for structure
- File is stored in MinIO with unique key
- Data source config references the file

**And** when assessments run:
- File Parser tool (Story 4.4) searches this file
- Matches by supplier name, country, identifiers

**And** I can replace the file:
- Upload new version
- Previous version archived
- New version used for future assessments

**And** UI shows:
- File upload dropzone
- Upload progress bar
- Validation results (row count, columns detected)
- "Preview Data" button showing first 10 rows

**Prerequisites:** Story 5.2, Story 1.5

**Technical Notes:**
- Endpoint: `POST /api/v1/admin/data-sources/upload`
- Store in MinIO bucket: `data-sources/{source_id}/{timestamp}_{filename}`
- CSV parsing: detect headers, validate required columns
- JSON parsing: validate array of objects structure

---

### Story 5.5: Implement Data Source Management UI (FR72-FR79)

As a **Platform Admin**,
I want a UI to manage data sources,
So that I can configure evidence collection without technical help.

**Acceptance Criteria:**

**Given** I navigate to `/admin/data-sources`
**When** the page loads
**Then** I see:

**Data Source List:**
- Table with columns: Name, Type, Country (or "Global"), Status, Health, Actions
- Status badges: Enabled (green), Disabled (gray)
- Health badges: Healthy (green), Degraded (amber), Failed (red), Unknown (gray)
- Filter by: Country, Type, Status, Health
- Search by name

**Add Data Source:**
- "Add Source" button opens wizard:
  1. Select type (API, File, URL, Scrape)
  2. Configure based on type:
     - API: name, base_url, auth type, credentials
     - File: name, upload file, column mapping
     - URL: name, URL, parsing rules
     - Scrape: name, URL, selectors, schedule
  3. Assign to country or mark as global
  4. Test connection
  5. Save (enabled or disabled)

**Data Source Detail:**
- View/edit all configuration
- Test connection button with result display
- Enable/disable toggle
- Health check history
- Delete (with confirmation)

**Prerequisites:** Story 5.3, Story 5.4

**Technical Notes:**
- Per UX: Admin sidebar, data tables
- Credentials input: password fields, never display actual values
- Connection test: show spinner, then result badge

---

### Story 5.6: Implement Country Management API and UI (FR80, FR81, FR82, FR83, FR84)

As a **Platform Admin**,
I want to manage countries and their configurations,
So that I can control which geographies are available for assessments.

**Acceptance Criteria:**

**Given** I am authenticated as Admin
**When** I call country endpoints
**Then**:

**GET `/api/v1/admin/countries`:**
- Returns list of all countries
- Includes: code, name, is_enabled, data_source_count

**GET `/api/v1/admin/countries/{code}`:**
- Returns country detail with:
  - Country info
  - List of configured data sources (FR84)
  - Country-specific evaluation parameters (FR82)

**POST `/api/v1/admin/countries`:**
- Adds new country (FR80)
- Triggers AI discovery (Story 5.7)

**PATCH `/api/v1/admin/countries/{code}`:**
- Updates country config
- Can enable/disable (FR83)
- Can update evaluation parameters (FR82)

**And** the UI at `/admin/countries` shows:
- Country list with flags, names, status, source counts
- "Add Country" button
- Country detail view with:
  - Enable/disable toggle
  - Linked data sources list (FR84)
  - "Add Data Source" (links to 7.5 with country pre-selected)
  - Country-specific parameters editor

**Prerequisites:** Story 5.1, Story 5.5

**Technical Notes:**
- Use ISO 3166-1 for country codes
- Country flags via flag emoji or icon library
- Per FR81: Data sources linked via country_code foreign key
- Evaluation parameters: risk weight adjustments, required sources, etc.

---

### Story 5.7: Implement AI-Assisted Data Source Discovery (FR85, FR86, FR87, FR88, FR89, FR90)

As a **Platform Admin**,
I want AI to suggest relevant data sources when adding a new country,
So that I can quickly configure coverage without manual research.

**Acceptance Criteria:**

**Given** I add a new country (e.g., "United Kingdom")
**When** the country is created
**Then** the system automatically:
1. Triggers AI discovery agent
2. Researches relevant data sources for that country (FR85, FR86):
   - Corporate registries (e.g., "Companies House")
   - Sanctions lists (e.g., "UK Sanctions List")
   - ESG databases (e.g., "UK Modern Slavery Registry")
   - Government databases
   - News sources
3. Returns suggestions list

**And** GET `/api/v1/admin/countries/{code}/discover` returns:
```json
{
  "suggestions": [
    {
      "id": "temp-uuid",
      "name": "Companies House",
      "type": "api",
      "description": "UK official company registry",
      "url": "https://api.company-information.service.gov.uk",
      "category": "registry",
      "confidence": 0.95,
      "status": "pending"
    }
  ],
  "discovery_status": "complete"
}
```

**And** I can review each suggestion (FR87):
- View details, source URL, description
- Confidence score from AI

**And** I can take action on each suggestion:
- **Approve** (FR88): Creates data source with suggested config
- **Reject** (FR89): Marks as rejected, won't suggest again
- **Modify** (FR90): Edit before approving

**And** UI shows:
- Discovery progress indicator
- Suggestion cards with approve/reject/modify buttons
- Bulk actions: "Approve All", "Reject All"

**Prerequisites:** Story 5.6

**Technical Notes:**
- Discovery agent: separate LangGraph workflow or LLM call
- Use web search + LLM to find and evaluate sources
- Store suggestions in temp table or JSONB on country record
- Confidence based on source reliability, API availability

---

### Story 5.8: Implement Discovery Feedback Loop (FR91)

As the **system**,
I want to learn from admin decisions on suggestions,
So that future discoveries are more accurate.

**Acceptance Criteria:**

**Given** an admin approves or rejects a suggestion
**When** the decision is recorded
**Then** the system stores:
- Country code
- Suggestion details
- Decision (approved/rejected/modified)
- Modifications made (if any)
- Timestamp

**And** future discoveries for similar countries:
- Prioritize sources similar to approved ones
- Deprioritize sources similar to rejected ones
- Use modification patterns to improve initial suggestions

**And** admin can view discovery history:
- Past suggestions and decisions
- Accuracy metrics (suggestions approved vs rejected)

**Prerequisites:** Story 5.7

**Technical Notes:**
- Store decisions in `discovery_feedback` table
- Per FR91: "System learns" - can use:
  - Simple heuristics (similar country → similar sources)
  - Vector similarity of source descriptions
  - Fine-tuned prompts based on patterns
- MVP: basic pattern matching; ML enhancement post-MVP

---



## Epic 6: Agentic Assessment Pipeline

**Goal:** Implement the AI-powered assessment workflow that autonomously investigates suppliers — collecting evidence from public sources, analyzing data quality, and calculating risk scores.

**User Value:** Suppliers are automatically investigated by AI agents that search public data, analyze evidence quality, and produce risk assessments — the core innovation that replaces manual research.

**FRs Covered:** FR17, FR18, FR19, FR20, FR21, FR22, FR23, FR24, FR25, FR26, FR27, FR28, FR29, FR30, FR31, FR32, FR33, FR34, FR35, FR36, FR37, FR38, FR39, FR40, FR41, FR42

---

### Story 6.1: Implement LangGraph Workflow Foundation

As a **developer**,
I want the LangGraph workflow structure and state management,
So that I can orchestrate multi-node agent pipelines with checkpointing.

**Acceptance Criteria:**

**Given** the backend infrastructure exists
**When** the workflow module is initialized
**Then** the following structure exists:
- `app/agents/workflow.py` - Main assessment workflow graph
- `app/agents/state.py` - AssessmentState TypedDict definition
- `app/agents/nodes/` - Individual node implementations

**And** AssessmentState includes:
```python
class AssessmentState(TypedDict):
    assessment_id: str
    supplier_id: str
    user_id: str
    data_sources: List[dict]
    risk_framework: dict
    collected_evidence: List[Evidence]
    analyzed_evidence: List[TaggedEvidence]
    risk_scores: List[RiskScore]
    report: Optional[dict]
    status: str
    current_node: str
    progress_pct: int
    errors: List[dict]
```

**And** the workflow graph is: `data_collection → evidence_analysis → risk_assessment → report_generation`
**And** checkpointing is enabled for crash recovery

**Prerequisites:** Story 3.3

**Technical Notes:**
- Per Architecture: LangGraph 1.0.x
- `pip install langgraph langchain-core` + provider package (langchain-openai, langchain-anthropic, or langchain-google-genai)
- Per Architecture ADR-002: LangGraph for durable execution
- Per Architecture ADR-005: Provider-agnostic LLM via factory pattern
- Checkpoint storage in PostgreSQL (or Redis for MVP)

---

### Story 6.2: Implement Evidence Data Model

As a **developer**,
I want the Evidence database model with vector embeddings,
So that I can store collected evidence and enable similarity search.

**Acceptance Criteria:**

**Given** pgvector is enabled
**When** the Evidence migration is applied
**Then** the `evidence` table exists with:
- `id` (UUID, primary key)
- `assessment_id` (UUID, FK → assessments.id)
- `source_url` (string, not null)
- `source_type` (enum: sanctions, registry, esg, news, website, file)
- `content` (text, not null)
- `content_embedding` (vector(1536), nullable)
- `reliability` (enum: high, medium, low, nullable)
- `recency` (enum: current, recent, dated, stale, nullable)
- `relevance_score` (float, nullable)
- `collector_tool` (string, not null)
- `collected_at` (timestamp, not null)
- `created_at`, `updated_at`

**And** the `risk_scores` table exists with:
- `id` (UUID, primary key)
- `assessment_id` (UUID, FK → assessments.id)
- `category` (string, not null)
- `score` (float, 0-100)
- `level` (enum: low, medium, high)
- `confidence` (enum: low, medium, high)
- `red_flags` (JSONB)
- `evidence_ids` (JSONB - array of evidence UUIDs)

**And** ivfflat index exists on `content_embedding` for similarity search

**Prerequisites:** Story 1.4

**Technical Notes:**
- Per Architecture: Vector dimension depends on embedding model (1536 for OpenAI, 1024 for others)
- Index: `CREATE INDEX idx_evidence_embedding ON evidence USING ivfflat (content_embedding vector_cosine_ops)`
- Pydantic models: `Evidence`, `TaggedEvidence`, `RiskScore` per Architecture

---

### Story 6.3: Implement Data Collection Node - Core Framework (FR17, FR25, FR26, FR28)

As the **Data Collection Agent**,
I want to query multiple data sources in parallel,
So that I can gather comprehensive evidence about a supplier efficiently.

**Acceptance Criteria:**

**Given** an assessment is triggered with supplier info
**When** the data_collection node executes
**Then** it:
1. Loads configured data sources for supplier's country
2. Creates collection tasks for each source
3. Executes tasks in parallel (asyncio.gather)
4. Implements retry logic (3 attempts with exponential backoff)
5. Records each piece of evidence with:
   - `source_url`
   - `source_type`
   - `content`
   - `collector_tool` (which tool collected it)
   - `collected_at` timestamp

**And** progress updates are published: 0% → 25% during collection
**And** failures are logged but don't stop other sources
**And** state is updated with `collected_evidence` list

**Prerequisites:** Story 4.1, Story 4.2

**Technical Notes:**
- Per Architecture: `app/agents/nodes/data_collection.py`
- Tools in `app/agents/tools/`: `web_scraper.py`, `api_client.py`, `file_parser.py`
- Per FR25: Parallel execution via asyncio
- Per FR26: Retry with backoff (1s, 2s, 4s)
- Per FR28: Full attribution on every evidence item

---

### Story 6.4: Implement Data Collection Tools (FR18, FR19, FR20, FR21, FR22, FR23, FR24, FR27)

As the **Data Collection Agent**,
I want specialized tools for different data source types,
So that I can extract relevant information from each source appropriately.

**Acceptance Criteria:**

**Given** the data collection node runs
**When** it encounters different source types
**Then** appropriate tools are used:

**Sanctions List Tool (FR18):**
- Queries configured sanctions APIs
- Searches by company name, aliases, country
- Returns match/no-match with details

**Corporate Registry Tool (FR19):**
- Queries business registry APIs
- Extracts: registration status, directors, filings
- Handles country-specific formats

**ESG Database Tool (FR20):**
- Queries ESG rating APIs
- Extracts scores, reports, certifications

**Debarment List Tool (FR21):**
- Checks government exclusion lists
- Returns debarment status and details

**News/Media Tool (FR22):**
- Searches news APIs for company mentions
- Filters by relevance and recency
- Extracts headlines, summaries, dates

**Website Crawler Tool (FR23):**
- Uses Playwright headless Chromium to render JS-heavy supplier sites
- Fetches supplier website content (handles SPAs, dynamic content)
- Extracts: about page, sustainability info, certifications
- Can capture screenshots as visual evidence
- Respects robots.txt (FR27)
- No CAPTCHA bypass (FR27)

**File Parser Tool (FR24):**
- Searches admin-uploaded files for supplier matches
- Parses CSV/JSON formats
- Returns matching records

**And** all tools respect ethical boundaries:
- robots.txt compliance
- No CAPTCHA bypass attempts
- No paywalled content access
- Rate limiting per source

**Prerequisites:** Story 4.3

**Technical Notes:**
- Per Architecture: Tools in `app/agents/tools/`
- Per Architecture ADR-007: Use Playwright with headless Chromium for website scraping (handles JS-rendered content)
- Per NFR6, NFR7: Ethical web scraping (robots.txt compliance, rate limiting)
- Use httpx for API-based data sources; Playwright for website crawling
- Mock implementations for MVP; real integrations added during delivery

---

### Story 6.5: Implement Evidence Analysis Node (FR29, FR30, FR31, FR32, FR33, FR34, FR35)

As the **Evidence Analysis Agent**,
I want to process collected evidence and tag it with quality indicators,
So that risk assessment has reliable, scored inputs.

**Acceptance Criteria:**

**Given** evidence has been collected
**When** the evidence_analysis node executes
**Then** for each evidence item, it:

1. **Tags Source Reliability (FR30):**
   - High: Official registries, government databases
   - Medium: Established news outlets, industry databases
   - Low: Company self-reported, social media, unknown sources

2. **Tags Recency (FR31):**
   - Current: < 30 days old
   - Recent: < 1 year old
   - Dated: < 3 years old
   - Stale: > 3 years old

3. **Scores Relevance (FR32):**
   - 0.0 - 1.0 scale
   - Based on keyword matching, semantic similarity
   - Considers risk categories (ESG, Modern Slavery, etc.)

4. **Identifies Corroboration (FR33):**
   - Flags evidence confirmed by multiple sources
   - Links corroborating evidence items

5. **Generates Confidence Score (FR34):**
   - Based on evidence quantity and quality
   - High: Multiple reliable, current sources
   - Medium: Some reliable sources, or single strong source
   - Low: Limited or low-quality sources

6. **Creates Evidence Log (FR35):**
   - Structured log with full attribution
   - Grouped by risk category

**And** progress updates: 25% → 50% during analysis
**And** state is updated with `analyzed_evidence` list

**Prerequisites:** Story 4.3

**Technical Notes:**
- Per Architecture: `app/agents/nodes/evidence_analysis.py`
- Use LLM for semantic analysis and tagging
- Generate embeddings for relevance scoring (via configured LLM provider)
- Store embeddings in pgvector for future similarity search

---

### Story 6.6: Implement Risk Assessment Node (FR36, FR37, FR38, FR39, FR40, FR41, FR42)

As the **Risk Assessment Agent**,
I want to apply scoring rules to analyzed evidence,
So that suppliers receive accurate, explainable risk ratings.

**Acceptance Criteria:**

**Given** evidence has been analyzed
**When** the risk_assessment node executes
**Then** it:

1. **Applies Scoring Criteria (FR36):**
   - Loads active risk framework from config
   - Applies category-specific rules

2. **Calculates Category Scores (FR37):**
   - For each configured risk category (ESG, Modern Slavery, etc.)
   - Score 0-100 based on weighted evidence
   - Level: low (0-33), medium (34-66), high (67-100)

3. **Produces Overall Score (FR38):**
   - Weighted average of category scores
   - Overall confidence based on evidence confidence

4. **Identifies Red Flags (FR39):**
   - Checks evidence against red flag criteria
   - Examples: sanctions match, debarment record, negative news patterns
   - Links red flags to supporting evidence

5. **Flags Data Quality Issues (FR40):**
   - Insufficient evidence for category
   - Conflicting evidence
   - Stale data only

6. **Determines EDD Recommendation (FR41):**
   - If overall risk = high → EDD strongly recommended
   - If confidence = low → EDD recommended
   - If specific red flags triggered → EDD recommended

7. **Ensures Determinism (FR42):**
   - Same inputs produce consistent scores (within ±5%)
   - Use temperature=0 for LLM calls
   - Document any variance sources

**And** progress updates: 50% → 75% during scoring
**And** state is updated with `risk_scores` list

**Prerequisites:** Story 4.5

**Technical Notes:**
- Per Architecture: `app/agents/nodes/risk_assessment.py`
- Per NFR11: Deterministic scoring via temperature=0
- Red flag criteria loaded from risk_frameworks table
- Store risk_scores in database with evidence_ids for traceability

---

### Story 6.7: Integrate Workflow with ARQ Worker

As the **system**,
I want the LangGraph workflow invoked from ARQ jobs,
So that assessments run in the background with proper state management.

**Acceptance Criteria:**

**Given** an assessment job is picked up by ARQ
**When** `run_assessment(assessment_id)` executes
**Then** it:
1. Loads assessment and supplier from database
2. Loads risk framework and data sources config
3. Creates initial AssessmentState
4. Invokes LangGraph workflow
5. Publishes status updates to Redis pub/sub
6. Saves evidence and scores to database after each node
7. Updates assessment record on completion

**And** if workflow fails mid-execution:
- State is checkpointed
- Error is logged
- Assessment status set to `failed`
- ARQ retries if configured

**And** status updates include human-readable messages:
- "Searching sanctions lists..."
- "Checking corporate registries..."
- "Analyzing evidence quality..."
- "Calculating risk scores..."

**Prerequisites:** Stories 3.3, 4.6

**Technical Notes:**
- Per Architecture: Worker has full DB access
- Publish to Redis channel `assessment:{id}` for SSE
- Save after each node completion (not batched)
- Use LangGraph's built-in checkpointing

---

## Epic 7: Results & Reporting

**Goal:** Display assessment results with evidence transparency, generate actionable recommendations and questionnaires, and enable users to manage and export their assessment history.

**User Value:** Users see clear risk ratings with full evidence trails, understand exactly why a supplier received a score, get actionable next steps, and can export professional reports for auditors.

**FRs Covered:** FR43, FR44, FR45, FR46, FR47, FR48, FR49, FR50, FR51, FR52, FR53, FR54, FR55, FR56, FR57, FR58, FR59, FR60, FR61, FR62, FR63

---

### Story 7.1: Implement Report Generation Node (FR43, FR44, FR45, FR46, FR47, FR48, FR49, FR50, FR51)

As the **Report Generation Agent**,
I want to synthesize assessment findings into a structured report,
So that users receive comprehensive, traceable results.

**Acceptance Criteria:**

**Given** risk scores have been calculated
**When** the report_generation node executes
**Then** it creates a report structure containing:

1. **Executive Summary:**
   - Supplier name, country, sector
   - Overall risk level with traffic light (FR44)
   - Overall confidence score (FR45)
   - One-paragraph summary of findings

2. **Risk Ratings by Category (FR44, FR45):**
   - For each category: score, level (low/medium/high), confidence
   - Traffic light indicator (green/amber/red)
   - Brief explanation of score drivers

3. **Evidence Log (FR46, FR51):**
   - Complete list of evidence items
   - Each with: source URL (clickable), source type, reliability, recency
   - Grouped by risk category
   - Full traceability maintained

4. **Red Flags (FR47):**
   - List of triggered red flags
   - Supporting evidence for each flag
   - Severity indicator

5. **Data Quality Warnings (FR48):**
   - Incomplete data sources
   - Stale data warnings
   - Conflicting evidence notes

6. **Recommendations (FR49, FR50):**
   - EDD recommendation if triggered
   - Actionable next steps based on risk profile
   - Specific areas requiring attention

**And** report is saved to database as JSONB
**And** progress updates: 75% → 100% during generation
**And** assessment status set to `complete`

**Prerequisites:** Story 4.6

**Technical Notes:**
- Per Architecture: `app/agents/nodes/report_generation.py`
- Store report in `assessments.report` JSONB column
- LLM generates summaries and recommendations
- All evidence IDs linked for drill-down

---

### Story 7.2: Implement Assessment Results API

As an **SME user**,
I want to retrieve assessment results via API,
So that the frontend can display comprehensive risk information.

**Acceptance Criteria:**

**Given** an assessment is complete
**When** I GET `/api/v1/assessments/{id}`
**Then** I receive:
```json
{
  "data": {
    "id": "uuid",
    "supplier": { "name": "...", "country": "...", "sector": "..." },
    "status": "complete",
    "overall_risk_level": "medium",
    "overall_confidence": "high",
    "completed_at": "timestamp",
    "report": {
      "summary": "...",
      "risk_categories": [...],
      "red_flags": [...],
      "warnings": [...],
      "recommendations": [...]
    }
  }
}
```

**And** GET `/api/v1/assessments/{id}/evidence` returns:
```json
{
  "data": [
    {
      "id": "uuid",
      "source_url": "https://...",
      "source_type": "sanctions",
      "reliability": "high",
      "recency": "current",
      "relevance_score": 0.95,
      "risk_categories": ["Modern Slavery"],
      "collected_at": "timestamp"
    }
  ]
}
```

**Prerequisites:** Story 5.1, Story 2.8

**Technical Notes:**
- Endpoints per Architecture: `GET /api/v1/assessments/{id}`, `GET /api/v1/assessments/{id}/evidence`
- User can only access their own assessments (data isolation)
- Include pagination for evidence list

---

### Story 7.3: Implement Assessment Results UI (FR44, FR45, FR46, FR47, FR48)

As an **SME user**,
I want to view my assessment results with clear risk indicators,
So that I can quickly understand the supplier's risk profile and dig into evidence.

**Acceptance Criteria:**

**Given** I navigate to `/assessments/{id}` for a complete assessment
**When** the page loads
**Then** I see:

**Summary Section:**
- Supplier name, country, sector
- Large risk badge (green/amber/red) with level text
- Confidence indicator
- Assessment date
- One-line summary

**Risk Categories Section:**
- Card for each risk category (ESG, Modern Slavery, etc.)
- Traffic light indicator per category
- Score and confidence displayed
- "View Evidence" expand trigger

**Red Flags Section (if any):**
- Alert banner with count
- List of red flags with severity
- Each flag expandable to show supporting evidence

**Data Quality Warnings (if any):**
- Warning banner
- List of incomplete sources or issues

**Evidence Drill-Down:**
- Expandable accordion per category
- Each evidence item shows:
  - Source name and type icon
  - Reliability badge (High/Medium/Low)
  - Recency badge
  - "View Source" link (opens in new tab)

**And** page is responsive (cards stack on mobile)
**And** clicking any rating shows evidence that supports it

**Prerequisites:** Stories 5.2, 3.6

**Technical Notes:**
- Per UX: RiskBadge, RiskSummaryCard, RiskCategoryCard, EvidenceItem components
- Per UX: Progressive disclosure - summary first, details on demand
- Per UX: "Every rating explainable with one click"
- Use shadcn/ui: Card, Badge, Accordion, Tabs

---

### Story 7.4: Implement Recommendations Display (FR52, FR53, FR54)

As an **SME user**,
I want to see actionable recommendations based on assessment results,
So that I know exactly what to do next.

**Acceptance Criteria:**

**Given** assessment results are displayed
**When** I view the recommendations section
**Then** I see:

**Recommendation Banner:**
- **Low Risk (Green):** "Proceed with standard onboarding"
- **Medium Risk (Amber):** "Consider Enhanced Due Diligence"
- **High Risk (Red):** "Enhanced Due Diligence Strongly Recommended"
- **Insufficient Data (Gray):** "Enhanced Due Diligence Recommended - Data gaps identified"

**Actionable Next Steps:**
- Numbered list of specific actions
- Based on risk profile and red flags
- Examples:
  - "Request supplier's ESG certification documentation"
  - "Verify corporate registration with official registry"
  - "Review news coverage from last 12 months"

**EDD Recommendation (FR53, FR54):**
- If high risk: Prominent EDD recommendation with reasoning
- If insufficient data: EDD recommended to fill gaps
- Contact information or next steps for EDD services

**Prerequisites:** Story 5.3

**Technical Notes:**
- Per UX: RecommendationBanner component
- Per UX: Risk outcomes are screening/triage, not final judgment
- Recommendations generated by LLM in report_generation node

---

### Story 7.5: Implement Questionnaire Generation (FR55, FR56, FR57)

As an **SME user**,
I want an AI-generated questionnaire to send to suppliers,
So that I can fill evidence gaps identified in the assessment.

**Acceptance Criteria:**

**Given** an assessment has evidence gaps
**When** I click "Generate Questionnaire" or view the questionnaire tab
**Then** the system:
1. Loads admin-provided questionnaire templates (FR56)
2. Identifies specific gaps from assessment (missing evidence, low confidence areas)
3. Tailors questions to this supplier's gaps (FR57)
4. Generates questionnaire with:
   - Introduction explaining purpose
   - Questions organized by category
   - Space for supplier responses
   - Document request list (certifications, policies, etc.)

**And** GET `/api/v1/assessments/{id}/questionnaire` returns:
```json
{
  "data": {
    "generated_at": "timestamp",
    "gaps_identified": ["ESG certification", "Modern slavery policy"],
    "questions": [
      {
        "category": "ESG",
        "question": "Please provide your current ESG certification...",
        "required": true
      }
    ],
    "document_requests": [
      "ESG certification or audit report",
      "Modern slavery statement"
    ]
  }
}
```

**And** I can view questionnaire in UI
**And** I can copy questionnaire text or download as document

**Prerequisites:** Story 5.3

**Technical Notes:**
- Per PRD: MVP generates questionnaire; delivery mechanism deferred
- Store questionnaire templates in admin config (later epic)
- LLM tailors questions based on gap analysis
- Endpoint: `GET /api/v1/assessments/{id}/questionnaire`

---

### Story 7.6: Implement Assessment List and Search (FR58, FR59, FR60)

As an **SME user**,
I want to view and search my past assessments,
So that I can access historical results and track my supplier portfolio.

**Acceptance Criteria:**

**Given** I navigate to `/assessments` (my dashboard)
**When** the page loads
**Then** I see:

**Assessment List:**
- Card gallery view (per UX) showing:
  - Supplier name
  - Country flag/code
  - Risk level badge
  - Confidence indicator
  - Assessment date
  - Status (complete/in-progress/failed)
- Sorted by most recent first

**Filtering (FR60):**
- Tab filters: All | In Progress | Complete | Failed
- Search box: filter by supplier name
- Risk level filter: Low | Medium | High
- Date range picker (optional)

**Pagination:**
- 12 cards per page
- Load more or pagination controls

**And** clicking a card navigates to `/assessments/{id}`
**And** empty state shows friendly message with "New Assessment" CTA

**Prerequisites:** Story 5.2

**Technical Notes:**
- Per UX: Card Gallery layout for supplier list
- Endpoint: `GET /api/v1/assessments?status=...&search=...&risk_level=...`
- Per Architecture: offset/limit pagination
- Use React Query for data fetching and caching

---

### Story 7.7: Implement Report Export - PDF (FR61)

As an **SME user**,
I want to export my assessment as a PDF,
So that I can share it with stakeholders or keep for audit records.

**Acceptance Criteria:**

**Given** I'm viewing a complete assessment
**When** I click "Export PDF"
**Then** a PDF is generated containing:
- Professional header with date and assessment ID
- Executive summary section
- Risk ratings table with traffic light colors
- Evidence log (condensed format)
- Red flags and warnings
- Recommendations
- Footer with traceability notice

**And** PDF is downloaded to my browser
**And** filename format: `{supplier_name}_risk_assessment_{date}.pdf`
**And** loading indicator shown during generation

**Prerequisites:** Story 5.3

**Technical Notes:**
- Endpoint: `GET /api/v1/assessments/{id}/report?format=pdf`
- Use WeasyPrint or similar for PDF generation
- Per PRD: "Professional format suitable for auditors"
- Store generated PDF in MinIO, return download URL

---

### Story 7.8: Implement Report Export - CSV (FR62)

As an **SME user**,
I want to export assessment data as CSV,
So that I can analyze it in spreadsheets or import to other systems.

**Acceptance Criteria:**

**Given** I'm viewing a complete assessment
**When** I click "Export CSV"
**Then** a CSV is generated containing:
- Assessment metadata (ID, date, supplier info)
- Risk scores by category
- Evidence list with all attributes
- Red flags

**And** CSV is downloaded to my browser
**And** filename format: `{supplier_name}_assessment_data_{date}.csv`

**Prerequisites:** Story 5.3

**Technical Notes:**
- Endpoint: `GET /api/v1/assessments/{id}/report?format=csv`
- Use Python csv module
- Include header row with column names

---

### Story 7.9: Implement Assessment Deletion (FR63)

As an **SME user**,
I want to delete my own assessments,
So that I can remove outdated or unwanted records.

**Acceptance Criteria:**

**Given** I'm viewing my assessment list or an assessment detail
**When** I click "Delete" on an assessment
**Then** a confirmation modal appears:
- "Are you sure you want to delete this assessment for [Supplier Name]?"
- "This action cannot be undone."
- "Cancel" and "Delete" buttons

**Given** I confirm deletion
**When** the delete executes
**Then**:
- Assessment is soft-deleted (`deleted_at` set)
- Associated evidence is soft-deleted
- Assessment disappears from my list
- Success toast: "Assessment deleted"

**And** I cannot delete other users' assessments
**And** deleted assessments are not returned in queries

**Prerequisites:** Story 5.6

**Technical Notes:**
- Endpoint: `DELETE /api/v1/assessments/{id}`
- Per Architecture: Soft delete (set `deleted_at`)
- Per UX: Modal for destructive actions
- User-scoped: can only delete own assessments

---

## Final Summary

### Story Count by Epic

| Epic | Title | Stories |
|------|-------|---------|
| 1 | Foundation & Project Setup | 6 |
| 2 | User Authentication & Access | 9 |
| 3 | Supplier Submission & Status Tracking | 7 |
| 4 | Admin Risk Framework Configuration | 6 |
| 5 | Admin Data Source & Country Management | 8 |
| 6 | Agentic Assessment Pipeline | 7 |
| 7 | Results & Reporting | 9 |
| **Total** | | **52 stories** |

### FR Coverage Validation

| FR Range | Category | Epic | Status |
|----------|----------|------|--------|
| FR1-FR9 | User Account & Access | Epic 2 | ✅ Covered |
| FR10-FR16 | Supplier Assessment Submission | Epic 3 | ✅ Covered |
| FR64-FR71 | Risk Framework Configuration | Epic 4 | ✅ Covered |
| FR72-FR79 | Data Source Configuration | Epic 5 | ✅ Covered |
| FR80-FR84 | Country Configuration | Epic 5 | ✅ Covered |
| FR85-FR91 | AI-Assisted Data Source Discovery | Epic 5 | ✅ Covered |
| FR17-FR28 | Agentic Data Collection | Epic 6 | ✅ Covered |
| FR29-FR35 | Evidence Analysis | Epic 6 | ✅ Covered |
| FR36-FR42 | Risk Assessment | Epic 6 | ✅ Covered |
| FR43-FR51 | Report Generation | Epic 7 | ✅ Covered |
| FR52-FR57 | Recommendations & Questionnaires | Epic 7 | ✅ Covered |
| FR58-FR63 | Assessment & Report Management | Epic 7 | ✅ Covered |
| FR92-FR96 | System & Processing | Epic 3 | ✅ Covered |

**All 96 Functional Requirements are covered across 7 epics and 51 stories.**

### Dependency Graph

```
Epic 1 (Foundation)
    ├── 1.1 Monorepo
    ├── 1.2 Backend ────┬── 1.4 Database ──┬── Epic 2 → [3,4,5 parallel] → 6 → 7
    ├── 1.3 Frontend ───┤                  │
    └── 1.5 Redis/MinIO─┴── 1.6 Dev Env ───┘

Epic 2 (Auth) ─┬─→ Epic 3 (Submission) ──────────────┐
               ├─→ Epic 4 (Risk Config) ─────────────┼─→ Epic 6 (Pipeline) → Epic 7 (Results)
               └─→ Epic 5 (Data Sources) ────────────┘
```

### Implementation Recommendations

1. **Critical Path:** Epics 1 → 2 → 3 → 6 → 7 deliver end-to-end SME user value
2. **Parallel Track:** Epics 3, 4, 5 run in parallel after Epic 2; all must complete before Epic 6
3. **MVP Focus:** Prioritize core flow; admin config can use simpler UI initially
4. **Risk:** Epic 6 (Agentic Pipeline) is the most complex — allow buffer time

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-28 | PM Agent (John) | Initial epic breakdown with 51 stories covering all 96 FRs |
| 1.1 | 2025-11-30 | SM Agent (Bob) | Updated Story 4.4 to align with ADR-007 (Playwright for web scraping) |
| 1.2 | 2025-12-01 | SM Agent (Bob) | Updated Stories 1.2, 1.7 to include Playwright installation steps |
| 1.3 | 2025-12-01 | SM Agent (Bob) | Renumbered epics to match execution order (Epic 4↔6, Epic 5↔7) |
| 1.4 | 2025-12-01 | SM Agent (Bob) | Added Story 2.0: Playwright E2E Testing Infrastructure (tech debt from Epic 1) |

---

_This Epic Breakdown was created through the BMad Method create-epics-and-stories workflow._
_All stories include BDD acceptance criteria and technical implementation notes._
