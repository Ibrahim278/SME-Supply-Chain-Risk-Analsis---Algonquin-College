# SME Supply Chain Risk Analysis - Product Requirements Document

**Author:** Master
**Date:** 2025-11-28
**Version:** 1.0

---

## Executive Summary

An AI-powered due diligence platform that enables a consultancy to help SME clients evaluate ESG (Environmental, Social, Governance) and modern slavery risks in their supply chains. The system uses agentic workflows to automate data collection from public sources, analyze evidence, assess risks, and generate actionable reports — transforming manual, time-intensive research into a scalable, consistent service.

### What Makes This Special

**"Verify First"** — Unlike traditional tools that rely on supplier self-assessment surveys, this platform investigates public data sources directly. It doesn't ask suppliers what they're doing; it finds evidence of what they're actually doing. Every risk rating comes with a full evidence trail of clickable sources, timestamps, and confidence scores.

This approach delivers:
- **Trust through transparency** — SMEs can see exactly why a supplier received a rating
- **Audit-ready documentation** — Every assessment is fully traceable
- **Consistency at scale** — AI agents apply the same rigor to every supplier

---

## Project Classification

**Technical Type:** B2B SaaS Platform
**Domain:** Compliance / ESG / Supply Chain Risk
**Complexity:** Medium-High

### Platform Architecture

Single-tenant, multi-user model:
- One consultancy owns and operates the platform
- Admin manages SME users directly (no organization/workspace layer)
- Each user sees only their own suppliers, assessments, and reports

| Role | Who | Capabilities |
|------|-----|--------------|
| **Admin** | Consultancy compliance experts | Configure risk frameworks, data sources, scoring rules, country parameters; manage users |
| **User** | SME client staff | Submit suppliers, view own assessments, access evidence, manage own reports |

### Geographic Scope

| Phase | Coverage |
|-------|----------|
| **MVP** | Canada |
| **Future** | International expansion (architecture supports multi-country) |

---

## Success Criteria

### Phase: MVP Validation

This is a "build and validate" phase. Success means proving the concept works with real users making real decisions — not achieving scale.

### The Core Validation Question

> **"Would an SME trust this assessment enough to make a supplier onboarding decision based on it?"**

If yes — concept validated, ready to scale.
If no — learn why, iterate, revalidate.

### Validation Criteria

| Criterion | What It Proves |
|-----------|----------------|
| **End-to-end workflow functional** | Agents collect data → analyze → score → generate reports without manual intervention |
| **Evidence is credible** | Sources are accurate, current, and relevant; confidence scores reflect data quality |
| **Consultancy can configure without dev help** | Risk frameworks, data sources, countries manageable through admin UI |
| **SMEs can self-serve** | Submit suppliers, understand results, act on recommendations without training |
| **Reports support decisions** | Clear enough for SMEs to approve/reject suppliers; defensible if audited |
| **First real clients onboarded** | At least one SME using it for actual supplier decisions |

### Business Metrics (Post-Validation)

Once validated, success metrics shift to:
- SME clients onboarded
- Supplier assessments completed per month
- Client retention rate
- Assessment completion time vs. manual baseline
- Countries/regions expanded

---

## Product Scope

### MVP - Minimum Viable Product

Everything required to validate the concept with real users in Canada.

#### Agentic Workflow Engine

| Capability | Description |
|------------|-------------|
| **Data Collection** | Agents query public sources: sanctions lists, corporate registries, ESG databases, debarment lists, Interpol notices, supplier websites, news/media, admin-uploaded files |
| **Evidence Analysis** | Process collected data; tag by quality, recency, relevance; generate evidence logs with source URLs, timestamps, reliability ratings, relevance scores, agent attribution |
| **Risk Assessment** | Apply admin-defined scoring criteria; produce risk ratings with confidence scores; identify red flags; flag data quality issues |
| **Report Generation** | Synthesize findings into structured reports: risk ratings, evidence logs, red flags, data quality issues, EDD recommendations, actionable next steps with full traceability |

#### Admin Dashboard (Consultancy)

| Capability | Description |
|------------|-------------|
| **Risk Framework Configuration** | CRUD for risk categories, classifications, scoring weights, thresholds, evaluation rules, red flag criteria |
| **Data Source Configuration** | CRUD for data sources (API endpoints, credentials, file uploads, URLs); designate as global or country-specific |
| **Country Configuration** | CRUD for countries with country-specific data sources and evaluation parameters |
| **AI-Assisted Data Source Discovery** | System suggests relevant data sources when adding new countries; admin reviews/approves/modifies |

#### User Dashboard (SME Clients)

| Capability | Description |
|------------|-------------|
| **Initiate Supplier Assessment** | Submit supplier info (name, country, sector, website, context) to trigger agentic assessment |
| **Assessment Status Tracking** | Real-time status display during background processing |
| **Risk Overview Display** | View risk ratings per category, confidence scores, traffic light indicators, evidence log with clickable sources, red flags, data quality warnings |
| **Actionable Recommendations** | AI-generated next steps; EDD recommendations when high-risk or insufficient data |
| **Supplier Questionnaire** | AI-generated questionnaire based on evidence gaps, using admin-provided templates |
| **Report Management** | View past assessments, access historical results, delete reports |

#### Technical Constraints (MVP)

| Aspect | Approach |
|--------|----------|
| **Processing Model** | Background processing with real-time status updates |
| **Agent Failure Handling** | Automatic retry; flag incomplete sections; show partial results |
| **Data Sources** | Discovered and configured with client during MVP delivery |
| **Notifications** | Nice-to-have; not required for launch |
| **Questionnaire Delivery** | Generate only; delivery mechanism deferred |

### Growth Features (Post-MVP)

Features to add once MVP is validated:

- **Email notifications** for assessment completion
- **Bulk supplier upload** (CSV import)
- **Assessment comparison** (compare suppliers side-by-side)
- **Trend tracking** (re-assess suppliers over time, track changes)
- **Custom report templates** (branded exports for SME clients)
- **API access** for third-party integrations
- **Advanced analytics dashboard** (assessment volume, risk distribution, data source performance)

### Vision Features (Future)

Long-term product evolution:

- **Multi-country expansion** (EU, UK, US, APAC) with localized data sources
- **Multi-consultancy support** (true multi-tenant SaaS)
- **Supplier portal** (suppliers respond to questionnaires directly in platform)
- **Continuous monitoring** (ongoing surveillance, not just point-in-time assessment)
- **Industry benchmarking** (anonymized risk comparisons across similar suppliers)
- **Mobile application** (native iOS/Android for on-the-go access)
- **Regulatory change tracking** (alert when compliance requirements change)

### Explicitly Out of Scope (MVP)

- Multi-consultancy (multi-tenant) architecture
- Countries beyond Canada (architecture ready, not populated)
- Mobile-native applications
- Advanced analytics/reporting dashboards
- Third-party API access
- Supplier self-service portal
- Continuous monitoring/alerting

---

## B2B SaaS Platform Requirements

### Tenant Model

**Architecture:** Single-tenant, multi-user (per-user data isolation)

```
┌─────────────────────────────────────────────────────────┐
│  Platform Instance (Single Tenant - Consultancy)        │
│                                                         │
│  ┌─────────────────┐                                    │
│  │  Admin          │  Global Config:                    │
│  │  (Consultancy)  │  - Risk frameworks                 │
│  │                 │  - Data sources                    │
│  │                 │  - Country settings                │
│  │                 │  - User management                 │
│  └─────────────────┘                                    │
│           │                                             │
│           ▼                                             │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐│
│  │User A  │ │User B  │ │User C  │ │User D  │ │User E  ││
│  │ (SME)  │ │ (SME)  │ │ (SME)  │ │ (SME)  │ │ (SME)  ││
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘│
│                                                         │
│  Each user isolated: own suppliers, assessments         │
└─────────────────────────────────────────────────────────┘
```

**Data Isolation:**
- Each user sees only their own data
- Suppliers, assessments, and reports are user-scoped
- Admin has visibility across all users' data
- No cross-user data leakage

### Permissions & Roles

| Role | Scope | Capabilities |
|------|-------|--------------|
| **Platform Admin** | Global | Full system configuration; manage all settings; view all users' data; manage user accounts |
| **User** | Own data | Submit assessments; view own assessments; manage own reports |

**Permission Matrix:**

| Action | Platform Admin | User |
|--------|----------------|------|
| Configure risk frameworks | ✓ | ✗ |
| Configure data sources | ✓ | ✗ |
| Manage countries | ✓ | ✗ |
| Create/manage user accounts | ✓ | ✗ |
| Submit supplier assessment | ✓ | ✓ |
| View assessments | All users' data | Own data only |
| Delete assessments | ✓ | ✓ (own only) |
| Export reports | ✓ | ✓ (own only) |

### Subscription Model

*To be determined with client — captured as open question*

Potential models:
- **Per-assessment pricing** — pay per supplier evaluated
- **Subscription tiers** — monthly/annual based on assessment volume
- **Bundled with advisory** — included in consultancy service packages

For MVP: Authentication and user-level data isolation required; billing/subscription logic deferred.

### Integration Requirements (MVP)

| Integration Type | MVP Approach |
|------------------|--------------|
| **Data Source APIs** | Direct integration with public APIs (sanctions lists, registries, etc.) |
| **File Uploads** | Admin can upload CSV/JSON data files as supplementary sources |
| **Authentication** | Username/password; SSO deferred to post-MVP |
| **Export** | PDF/CSV report export; API access deferred |

---

## Innovation: Agentic AI Architecture

This product's core innovation is the **agentic workflow** — autonomous AI agents that investigate, analyze, and report without human intervention per assessment.

### Agent Workflow Design

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│    Data      │     │   Evidence   │     │     Risk     │     │    Report    │
│  Collection  │ ──▶ │   Analysis   │ ──▶ │  Assessment  │ ──▶ │  Generation  │
│    Agent     │     │    Agent     │     │    Agent     │     │    Agent     │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
       │                    │                    │                    │
       ▼                    ▼                    ▼                    ▼
  Query multiple       Tag sources by       Apply scoring        Synthesize
  public sources       quality/recency      frameworks          findings into
  in parallel          and relevance        and red flags       structured report
```

### Agent Behavior Requirements

| Requirement | Description |
|-------------|-------------|
| **Autonomous execution** | Once triggered, agents complete full workflow without human intervention |
| **Parallel data collection** | Query multiple sources simultaneously for efficiency |
| **Graceful degradation** | If a source fails, continue with available sources; flag incomplete data |
| **Retry logic** | Automatic retries on transient failures (network, rate limits) |
| **Deterministic scoring** | Same inputs produce consistent risk scores (within acceptable variance) |
| **Full attribution** | Every piece of evidence tagged with source, timestamp, and collecting agent |
| **Configurable timeouts** | Prevent indefinite blocking; fail gracefully if timeout exceeded |

### Evidence Quality Framework

Agents must tag each piece of evidence with quality indicators:

| Dimension | Rating Scale | Criteria |
|-----------|--------------|----------|
| **Source Reliability** | High / Medium / Low | Official registry > news outlet > company website |
| **Recency** | Current / Recent / Dated / Stale | <30 days / <1 year / <3 years / >3 years |
| **Relevance** | Direct / Related / Peripheral | Exact match > industry match > general |
| **Confidence** | High / Medium / Low | Multiple corroborating sources > single source |

---

## User Experience Principles

### Design Philosophy

**"Clarity over complexity"** — Users are not compliance experts. The interface must translate complex risk data into clear, actionable insights without dumbing it down.

### UX Principles

| Principle | Application |
|-----------|-------------|
| **No training required** | A new SME user should be able to submit their first supplier assessment within 5 minutes of logging in |
| **Glanceable risk** | Traffic light indicators (red/amber/green) provide instant understanding; details available on drill-down |
| **Evidence transparency** | Every rating must be explainable with one click — "why did this supplier get this score?" |
| **Progressive disclosure** | Show summary first, details on demand; don't overwhelm with data |
| **Actionable outcomes** | Don't just show problems — tell users what to do next |
| **Status visibility** | Background processing must show clear progress; never leave users wondering "is it working?" |

### Visual Design Direction

| Aspect | Approach |
|--------|----------|
| **Tone** | Professional, trustworthy, clean — this is compliance tooling, not consumer app |
| **Color usage** | Semantic colors for risk (red/amber/green); neutral palette elsewhere |
| **Information density** | Medium — enough data to be useful, not so much it overwhelms |
| **Typography** | Highly readable; clear hierarchy between headings, body, and data |

### Key Interactions

#### SME User Dashboard

| Interaction | UX Goal |
|-------------|---------|
| **Submit supplier** | Simple form; minimal required fields; clear "what happens next" |
| **Track assessment** | Real-time status; estimated progress; no ambiguity |
| **View results** | Risk summary at top; evidence details expandable; recommendations prominent |
| **Explore evidence** | Click any rating to see sources; each source clickable to original |
| **Export report** | One-click PDF/CSV; professional format suitable for auditors |

#### Admin Dashboard

| Interaction | UX Goal |
|-------------|---------|
| **Configure risk framework** | Visual rule builder; no code required; preview impact |
| **Manage data sources** | Clear status indicators (active/error/disabled); test connection |
| **Add country** | AI suggestions displayed clearly; easy approve/reject/modify |
| **View all users' data** | At-a-glance overview; drill into any user's assessments |

### Error States

| Scenario | UX Response |
|----------|-------------|
| **Assessment partially complete** | Show what succeeded; clearly mark incomplete sections; explain why |
| **Data source unavailable** | Friendly message; no technical jargon; suggest alternatives if any |
| **No results found** | Explain what was searched; suggest different search terms or manual input |
| **System error** | Apologize; provide reference ID; never show stack traces |

---

## Functional Requirements

This section defines **WHAT capabilities** the product must have. It is the complete inventory of user-facing and system capabilities that deliver the product vision.

**How these will be used:**
- UX Designer reads FRs → designs interactions for each capability
- Architect reads FRs → designs systems to support each capability
- PM creates epics and stories to implement each capability
- Dev implements stories based on FRs

---

### User Account & Access

- **FR1:** Users can log in securely with email and password
- **FR2:** Users can reset passwords via email verification
- **FR3:** Users can update their profile information
- **FR4:** Platform Admin can create user accounts for SME clients
- **FR5:** Platform Admin can view and manage all user accounts
- **FR6:** Platform Admin can deactivate/reactivate user accounts
- **FR7:** System enforces role-based access (Platform Admin vs User)
- **FR8:** System automatically isolates data by user (each user only sees their own data)
- **FR9:** Platform Admin can view assessments across all users

### Supplier Assessment Submission

- **FR10:** SME Users can submit a new supplier for assessment
- **FR11:** Supplier submission captures: name, country of operation, sector/commodity, website URL, and additional context
- **FR12:** System validates supplier submission for required fields before processing
- **FR13:** System initiates agentic assessment workflow upon valid submission
- **FR14:** Users receive confirmation that assessment has started
- **FR15:** Users can view real-time status of in-progress assessments
- **FR16:** Users can see progress indicators for each stage of the assessment workflow

### Agentic Data Collection

- **FR17:** Data Collection Agent queries configured public data sources for supplier information
- **FR18:** Agent searches sanctions lists (global and country-specific) for supplier matches
- **FR19:** Agent searches corporate registries for company information
- **FR20:** Agent searches ESG databases for environmental, social, governance data
- **FR21:** Agent searches debarment lists for exclusion records
- **FR22:** Agent searches news and media sources for relevant coverage
- **FR23:** Agent crawls supplier website for self-reported information
- **FR24:** Agent processes admin-uploaded data files for matches
- **FR25:** Agent executes queries in parallel across multiple sources
- **FR26:** Agent implements retry logic for transient failures
- **FR27:** Agent respects ethical boundaries (robots.txt, no CAPTCHA bypass, no paywalled content)
- **FR28:** Agent records source URL, timestamp, and agent attribution for each data point collected

### Evidence Analysis

- **FR29:** Evidence Analysis Agent processes all collected data from Data Collection Agent
- **FR30:** Agent tags each piece of evidence with source reliability rating (High/Medium/Low)
- **FR31:** Agent tags each piece of evidence with recency rating (Current/Recent/Dated/Stale)
- **FR32:** Agent tags each piece of evidence with relevance score to risk categories
- **FR33:** Agent identifies corroborating evidence across multiple sources
- **FR34:** Agent generates confidence score based on evidence quality and quantity
- **FR35:** Agent creates structured evidence log with full attribution

### Risk Assessment

- **FR36:** Risk Assessment Agent applies admin-defined scoring criteria to analyzed evidence
- **FR37:** Agent calculates risk ratings for each configured risk category
- **FR38:** Agent produces overall risk score with confidence level
- **FR39:** Agent identifies and flags red flags based on admin-defined criteria
- **FR40:** Agent flags data quality issues where evidence is insufficient or conflicting
- **FR41:** Agent determines if Enhanced Due Diligence (EDD) is recommended
- **FR42:** Same inputs produce consistent risk scores within acceptable variance thresholds

### Report Generation

- **FR43:** Report Generation Agent synthesizes all findings into structured report
- **FR44:** Report includes risk ratings per category with traffic light indicators
- **FR45:** Report includes confidence scores for each rating
- **FR46:** Report includes complete evidence log with clickable source links
- **FR47:** Report includes identified red flags with supporting evidence
- **FR48:** Report includes data quality warnings where applicable
- **FR49:** Report includes EDD recommendations when triggered
- **FR50:** Report includes actionable next steps based on risk profile
- **FR51:** All report content maintains full traceability to source evidence

### Recommendations & Questionnaires

- **FR52:** System generates actionable recommendations based on assessment results
- **FR53:** System generates EDD recommendations when high-risk indicators detected
- **FR54:** System generates EDD recommendations when insufficient data detected
- **FR55:** System generates supplier questionnaire based on identified evidence gaps
- **FR56:** Questionnaire uses admin-provided templates as foundation
- **FR57:** AI tailors questionnaire questions to specific gaps identified for this supplier

### Assessment & Report Management

- **FR58:** Users can view list of all their past supplier assessments
- **FR59:** Users can access and review historical assessment results
- **FR60:** Users can search/filter assessments by supplier name, date, risk level
- **FR61:** Users can export assessment report as PDF
- **FR62:** Users can export assessment data as CSV
- **FR63:** Users can delete their own individual assessments

### Risk Framework Configuration (Admin)

- **FR64:** Platform Admin can create risk categories (e.g., ESG, Modern Slavery, Financial)
- **FR65:** Platform Admin can define risk classifications within categories
- **FR66:** Platform Admin can configure scoring weights for each risk factor
- **FR67:** Platform Admin can set risk thresholds (what constitutes high/medium/low)
- **FR68:** Platform Admin can define evaluation rules for scoring
- **FR69:** Platform Admin can define red flag criteria and triggers
- **FR70:** Platform Admin can update risk frameworks; changes apply to new assessments
- **FR71:** Platform Admin can preview impact of framework changes before applying

### Data Source Configuration (Admin)

- **FR72:** Platform Admin can add new data sources to the system
- **FR73:** Data source configuration supports: API endpoints, credentials, file uploads, URL sources
- **FR74:** Platform Admin can designate data sources as global (all countries) or country-specific
- **FR75:** Platform Admin can test data source connectivity
- **FR76:** Platform Admin can enable/disable data sources
- **FR77:** Platform Admin can view data source status (active, error, disabled)
- **FR78:** Platform Admin can upload CSV/JSON files as supplementary data sources
- **FR79:** Platform Admin can update data source credentials

### Country Configuration (Admin)

- **FR80:** Platform Admin can add new countries to the system
- **FR81:** Platform Admin can configure country-specific data sources
- **FR82:** Platform Admin can configure country-specific evaluation parameters
- **FR83:** Platform Admin can enable/disable countries for assessment availability
- **FR84:** Platform Admin can view which data sources are configured for each country

### AI-Assisted Data Source Discovery (Admin)

- **FR85:** When adding a new country, system suggests relevant data sources
- **FR86:** AI suggestions include: corporate registries, sanctions lists, local ESG databases
- **FR87:** Platform Admin can review each AI suggestion
- **FR88:** Platform Admin can approve suggestions (adds to country config)
- **FR89:** Platform Admin can reject suggestions (excludes from config)
- **FR90:** Platform Admin can modify suggestions before approving
- **FR91:** System learns from admin decisions to improve future suggestions

### System & Processing

- **FR92:** System processes assessments in background (non-blocking)
- **FR93:** System enforces configurable timeouts for agent tasks
- **FR94:** System continues processing when individual agents fail (graceful degradation)
- **FR95:** System marks assessment sections as incomplete when agent fails after retries
- **FR96:** System displays partial results with clear incomplete indicators

---

## Non-Functional Requirements

### Security

| ID | Requirement | Rationale |
|----|-------------|-----------|
| **NFR1** | Passwords must be hashed using industry-standard algorithms (bcrypt, Argon2) | Protect credentials if database compromised |
| **NFR2** | All data transmission must use TLS 1.2+ encryption | Protect data in transit |
| **NFR3** | User sessions must expire after configurable inactivity period | Limit exposure from abandoned sessions |
| **NFR4** | All user inputs must be validated and sanitized | Prevent injection attacks (SQL, XSS) |
| **NFR5** | API endpoints must enforce authentication and authorization | Prevent unauthorized access |
| **NFR6** | Data collection agents must respect robots.txt directives | Ethical web scraping |
| **NFR7** | System must not bypass CAPTCHAs or access paywalled content | Ethical data collection boundaries |
| **NFR8** | Sensitive credentials (API keys, passwords) must be encrypted at rest | Protect secrets in database |
| **NFR9** | System must log security-relevant events (login attempts, permission changes) | Audit trail for security incidents |

### Reliability

| ID | Requirement | Rationale |
|----|-------------|-----------|
| **NFR10** | System must continue operating when individual agents fail | Graceful degradation; partial results better than no results |
| **NFR11** | Agent workflows must produce consistent results for identical inputs | Deterministic scoring builds trust; variance within acceptable thresholds |
| **NFR12** | Failed agent tasks must retry automatically before marking incomplete | Transient failures shouldn't cause permanent gaps |
| **NFR13** | System must clearly indicate when assessment data is incomplete | Users must know what they're missing |
| **NFR14** | Database must be backed up regularly with point-in-time recovery capability | Protect against data loss |

### Performance

| ID | Requirement | Rationale |
|----|-------------|-----------|
| **NFR15** | Assessment processing must run in background without blocking UI | Users shouldn't wait for long-running agent tasks |
| **NFR16** | UI must show real-time progress updates during assessment | Status visibility; users know system is working |
| **NFR17** | Agent tasks must have configurable timeouts | Prevent indefinite blocking |
| **NFR18** | Data source queries should execute in parallel where possible | Minimize total assessment time |
| **NFR19** | Dashboard pages must load within 3 seconds under normal conditions | Responsive user experience |
| **NFR20** | System must handle concurrent assessments without degradation | Multiple SMEs may submit simultaneously |

### Usability

| ID | Requirement | Rationale |
|----|-------------|-----------|
| **NFR21** | Interface must be usable without training | SME users are not compliance experts |
| **NFR22** | Error messages must be user-friendly without technical jargon | Don't expose stack traces or technical details |
| **NFR23** | Risk ratings must be immediately understandable (traffic light indicators) | Glanceable risk assessment |
| **NFR24** | Every risk rating must be explainable with one click | Evidence transparency builds trust |
| **NFR25** | Admin configuration UI must not require coding knowledge | Consultancy is non-technical |
| **NFR26** | System must support English language | MVP target market is Canada |

### Maintainability

| ID | Requirement | Rationale |
|----|-------------|-----------|
| **NFR27** | Code must include inline documentation for key functions and agent workflows | Enable future maintenance |
| **NFR28** | System components must be modular and loosely coupled | Facilitate updates and modifications |
| **NFR29** | Agent workflows must be configurable without code changes | Admin can adjust behavior |
| **NFR30** | System must log agent actions for debugging and audit | Troubleshoot agent behavior |

### Data Integrity

| ID | Requirement | Rationale |
|----|-------------|-----------|
| **NFR31** | Assessment reports must be immutable once generated | Audit trail integrity |
| **NFR32** | All evidence must maintain traceability to original source | Verifiable claims |
| **NFR33** | Data isolation between users must be enforced at database level | Prevent cross-user data leakage |

---

## Open Questions

Items to clarify with client before or during implementation:

| # | Question | Impact |
|---|----------|--------|
| 1 | How does the consultancy deliver due diligence services today? | Informs migration/transition planning |
| 2 | What is the pricing model? (Per assessment, subscription, bundled) | Affects whether billing logic is needed |
| 3 | Does the consultancy review assessments before SMEs see them, or fully automated? | May require approval workflow |
| 4 | Which specific data sources should be configured for Canada MVP? | Drives initial data source integration work |
| 5 | What risk categories and scoring rules should be pre-configured? | Determines initial framework setup |
| 6 | Are there specific questionnaire templates the consultancy uses today? | Informs questionnaire generation feature |

---

## Document Summary

| Metric | Count |
|--------|-------|
| **Functional Requirements** | 96 |
| **Non-Functional Requirements** | 33 |
| **Total Requirements** | 129 |

### Capability Coverage

| Area | FRs |
|------|-----|
| User Account & Access | 9 |
| Supplier Assessment | 7 |
| Agentic Data Collection | 12 |
| Evidence Analysis | 7 |
| Risk Assessment | 7 |
| Report Generation | 9 |
| Recommendations & Questionnaires | 6 |
| Assessment Management | 6 |
| Admin: Risk Framework | 8 |
| Admin: Data Sources | 8 |
| Admin: Countries | 5 |
| Admin: AI Discovery | 7 |
| System & Processing | 5 |

---

## Tech Stack

| Category | Decision | Version | Affects FRs | Rationale |
| -------- | -------- | ------- | ----------- | --------- |
| Backend Framework | FastAPI | 0.115.x | All | Async-native, auto OpenAPI docs, Python ecosystem for AI |
| Frontend Framework | Next.js + React | 15.x (stable) | All UI | App Router, RSC, pairs with shadcn/ui |
| UI Components | shadcn/ui + Tailwind | 3.x / 3.4.x | All UI | Per UX spec, accessible, customizable |
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
| API Client | openapi-typescript | 7.x | All UI | Type-safe from OpenAPI spec |
| Deployment | Docker Compose on VPS | - | All | Self-contained, single server |

---

## Document History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0 | 2025-11-28 | Master | Initial PRD created through collaborative discovery |

---

_This PRD captures the complete requirements for SME Supply Chain Risk Analysis — an AI-powered "verify first" due diligence platform that investigates public data to deliver transparent, evidence-backed supplier risk assessments._

_Created through collaborative discovery between Master and AI facilitator._
