# Product Brief: SME Supply Chain Risk Analysis

**Date:** 2025-11-28
**Author:** Master
**Context:** Client Project (B2B SaaS / Consultancy Tool)

---

## Executive Summary

An AI-powered due diligence platform that enables a consultancy to help SME clients evaluate ESG (Environmental, Social, Governance) and modern slavery risks in their supply chains. The system uses agentic workflows to automate data collection from public sources, analyze evidence, assess risks, and generate actionable reports — transforming what is currently a manual, time-intensive process into a scalable, consistent service offering.

---

## Core Vision

### The Origin

A consultancy that advises small and medium enterprises on supply chain compliance identified the need to scale their due diligence services. SMEs increasingly face pressure to demonstrate ethical supply chains — from regulations, customers, and investors — but lack the resources for comprehensive supplier vetting. This tool bridges that gap.

### Initial Vision

A platform where:
- **The consultancy** configures risk frameworks, data sources, and assessment criteria tailored to different industries and geographies
- **SME clients** submit suppliers for assessment and receive clear, evidence-backed risk ratings with actionable recommendations
- **AI agents** handle the heavy lifting — crawling public data sources, synthesizing evidence, and producing consistent, traceable reports

---

## Platform Model

**Single-tenant, multi-user architecture (per-user data isolation):**

- **One consultancy** owns and operates the platform
- **Admin manages SME users directly** (no organization/workspace layer)
- Each user sees only their own suppliers, assessments, and reports

| Role | Who | Capabilities |
|------|-----|--------------|
| **Admin** | Consultancy staff | Configure risk frameworks, data sources, scoring rules, country-specific parameters, red flag criteria; manage users |
| **User** | SME clients | Submit suppliers for assessment, view own risk ratings, access evidence logs, receive recommendations, manage own reports |

The consultancy's domain expertise is embedded in the configuration — risk frameworks, evaluation rules, data source curation. SME clients get a self-service tool that delivers consistent, professional-grade due diligence.

---

## Problem Statement

### The Core Challenge

SMEs are increasingly required to demonstrate ethical, compliant supply chains — but lack the resources, expertise, and tools to do it properly.

### Pain Points

| Pain | Impact |
|------|--------|
| **Manual research is slow** | Checking sanctions lists, ESG databases, corporate registries one by one consumes hours per supplier |
| **Inconsistent quality** | Different analysts apply different rigor — results vary, risk exposure is unpredictable |
| **No audit trail** | Hard to prove due diligence was performed; liability exposure if a supplier issue surfaces |
| **Regulatory pressure mounting** | UK Modern Slavery Act, EU Corporate Sustainability Due Diligence Directive, and similar regulations make this mandatory, not optional |
| **Resource mismatch** | SMEs face enterprise-level compliance expectations with startup-level budgets and no dedicated compliance teams |

### Why This Matters Now

Supply chain due diligence has shifted from "nice to have" to "legal requirement" in many jurisdictions. SMEs that can't demonstrate proper vetting face:
- Regulatory penalties
- Reputational damage
- Loss of contracts with larger partners who demand supply chain transparency
- Potential legal liability for modern slavery or ESG violations in their supply chain

The consultancy sees this pattern repeatedly — SME clients who know they need to do this, but don't have a scalable way to do it right.

---

## Proposed Solution

### The Approach

An AI-powered due diligence platform where intelligent agents automate the investigative work that currently consumes hours of manual research per supplier.

**How it works:**

1. **SME submits supplier** — name, country, sector, website, any additional context
2. **Agents investigate** — crawl public data sources (sanctions lists, corporate registries, ESG databases, news, company websites)
3. **Evidence synthesized** — sources tagged by quality, recency, relevance; full traceability maintained
4. **Risk assessed** — scored against consultancy-configured frameworks with confidence levels
5. **Report generated** — clear ratings, evidence logs, red flags, and actionable recommendations

### Key Differentiators

| Traditional Tools | This Solution |
|-------------------|---------------|
| Supplier self-assessment surveys | Public data investigation (verify first) |
| Opaque scoring algorithms | Full evidence trail with clickable sources |
| Enterprise pricing | SME-accessible via consultancy platform |
| Generic one-size-fits-all | Consultancy expertise embedded in configuration |
| Static data sources | AI-assisted data source discovery for new countries |

### Geographic Scalability

The platform is designed for multi-country expansion:

- **Country as first-class entity** — each country has its own data sources, regulatory context, risk parameters
- **AI-assisted country onboarding** — when adding a new country, the system researches and suggests relevant data sources (corporate registries, sanctions lists, local ESG databases)
- **Consultancy validates, not builds** — approve/reject/modify AI suggestions rather than manual research

This enables the consultancy to expand into new markets rapidly without hiring country-specific compliance specialists for each jurisdiction.

---

## Target Users

### Primary User: SME Client Staff

**Who they are:**
- Employees at small-to-medium enterprises across Canada
- Mixed industries (manufacturing, retail, services, etc.)
- Role varies: could be owner, procurement manager, operations lead, or office manager
- Not compliance experts — they use this tool because they *need* guidance

**What they need:**
- Simple, intuitive interface — no training required
- Clear risk ratings they can understand at a glance
- Actionable recommendations, not just scores
- Evidence they can reference if questioned by auditors or partners
- Confidence that they're meeting compliance obligations

**Technical comfort:** Varies widely. Design for the least technical user.

### Admin User: Consultancy Staff

**Who they are:**
- Compliance expert(s) at the consultancy
- Directly operates the platform — no IT intermediary
- Deep domain knowledge, but not highly technical

**What they need:**
- Clean UI for configuring risk frameworks, scoring rules, data sources
- Country management with AI-assisted data source discovery
- Visibility into SME client activity and assessment results
- Ability to customize without writing code

**Technical comfort:** Business user level. No JSON configs or API knowledge required.

### Geographic Scope

| Phase | Coverage |
|-------|----------|
| **MVP** | Canada |
| **Future** | International expansion (platform architecture supports multi-country) |

---

## Success Metrics

### Phase: MVP Validation

This is a "build and validate" phase — success is proving the concept works, not scaling.

### Validation Criteria

| Metric | What It Validates |
|--------|-------------------|
| **Platform functional** | Agents collect data, assess risk, generate reports end-to-end |
| **Consultancy can configure** | Risk frameworks, data sources, countries manageable without dev help |
| **SMEs can self-serve** | Submit suppliers, understand results, take action without hand-holding |
| **Reports are credible** | Evidence is accurate, sources valid, recommendations actionable |
| **First clients onboarded** | Real SMEs using it for real supplier decisions |

### The Core Validation Question

> "Would an SME trust this assessment enough to make a supplier onboarding decision based on it?"

**Yes** = Concept validated, ready to scale
**No** = Learn why, iterate, revalidate

### Post-MVP Metrics (Future)

Once validated, success metrics shift to:
- Number of SME clients onboarded
- Supplier assessments completed per month
- Client retention rate
- Time-to-assessment vs. manual baseline
- Geographic expansion (countries added)

---

## MVP Scope

### Core Features (All Required)

The client has defined these as must-haves for MVP launch.

#### Agentic Workflow

| Feature | Description |
|---------|-------------|
| **Data Collection** | Agents query public sources: sanctions lists, corporate registries, ESG databases, debarment lists, Interpol notices, supplier websites, news/media, admin-uploaded files |
| **Evidence Analysis** | Process collected data, tag by quality/recency, generate evidence logs with source URLs, timestamps, reliability ratings, relevance scores, agent attribution |
| **Risk Assessment** | Apply admin-defined scoring criteria, produce risk ratings with confidence scores, identify red flags, flag data quality issues |
| **Report Generation** | Synthesize findings into structured reports: risk ratings, evidence logs, red flags, data quality issues, EDD recommendations, actionable next steps with full traceability |

#### Admin Dashboard

| Feature | Description |
|---------|-------------|
| **Risk Framework Configuration** | CRUD for risk categories, classifications, scoring weights, thresholds, evaluation rules, best practices, red flag criteria |
| **Data Source Configuration** | CRUD for data sources (API endpoints, credentials, file uploads, URLs); designate as global or country-specific |
| **Country Configuration** | CRUD for countries with country-specific data sources and evaluation parameters |
| **AI-Assisted Data Source Discovery** | System suggests relevant data sources when adding new countries; admin reviews/approves/modifies |

#### User Dashboard

| Feature | Description |
|---------|-------------|
| **Initiate Supplier Assessment** | Submit supplier info (name, country, sector, website, context) to trigger agentic assessment |
| **Risk Overview Display** | View risk ratings per category, confidence scores, traffic light indicators, evidence log with clickable sources, red flags, data quality warnings |
| **Actionable Recommendations** | AI-generated next steps, EDD recommendations when high-risk or insufficient data |
| **Supplier Questionnaire** | AI-generated questionnaire based on gaps, using admin-provided templates |
| **Report Management** | View past assessments, access historical results, delete reports |

### Key Clarifications

| Aspect | Decision |
|--------|----------|
| **Data Sources** | Specific sources (sanctions lists, registries, ESG databases) will be discovered and configured as part of MVP delivery with client input |
| **Agent Failure Handling** | Automatic retry logic; if still failing, flag sections as incomplete and show partial results with clear indicators |
| **Processing Model** | Background processing — user submits assessment, UI shows real-time status, results available when complete |
| **Notifications** | Nice-to-have for MVP; not required for launch |
| **Supplier Questionnaire** | MVP generates the questionnaire; delivery mechanism (email, portal, export) deferred to later phase |

### Non-Functional Requirements (MVP)

| Category | Requirement |
|----------|-------------|
| **Reliability** | Graceful degradation when agents fail (retry + partial results); deterministic outputs within variance thresholds |
| **Performance** | Background processing with status tracking; configurable timeouts for agent tasks |
| **Security** | Username/password auth with hashed passwords; ethical data collection (respect robots.txt, no CAPTCHA bypass, no paywalled content); input validation |
| **Usability** | Intuitive interface for non-technical users; clear risk presentation; real-time assessment status; user-friendly error messages |
| **Maintainability** | Code documentation; modular, loosely-coupled design |

### Out of Scope for MVP

- Multi-consultancy (multi-tenant) architecture
- Countries beyond Canada (architecture ready, but not populated)
- Mobile-native applications
- Advanced analytics/reporting dashboards
- API access for third-party integrations

---

## Technical Direction

*Initial suggestions — tech stack is flexible and will be finalized during architecture phase*

| Category | Consideration | Notes |
|----------|---------------|-------|
| **AI/Agent Framework** | LangChain / LangGraph, CrewAI, or custom | Must support multi-agent orchestration, retries, partial failure handling |
| **Backend** | Python preferred | Strong AI/ML ecosystem; FastAPI or similar for async support |
| **Frontend** | React or modern alternative | Clean, intuitive UI is critical; component library TBD |
| **Database** | PostgreSQL or similar | Relational for structured data; may need document store for evidence logs |
| **Background Jobs** | Celery, Redis Queue, or similar | Assessment processing is async; needs status tracking |
| **Web Scraping** | Playwright, Puppeteer, or similar | Browser-based for dynamic content; must respect ethical boundaries |
| **Infrastructure** | TBD | Cloud deployment; scalability for future growth |

**Architecture phase will evaluate and finalize technology choices based on:**
- Performance requirements for agent workflows
- Scalability needs for multi-country expansion
- Cost considerations for MVP phase
- Team expertise and maintainability

---

## Open Questions (To Clarify with Client)

1. **Current Process:** How does the consultancy deliver due diligence services today? What's manual vs. tooled?
2. **Pricing Model:** Per assessment? Subscription? Bundled with advisory services?
3. **Consultancy Oversight:** Does the consultancy review assessments before SMEs see them, or is it fully automated?

---

## Document History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0 | 2025-11-28 | Master | Initial product brief created through collaborative discovery |

---

_This Product Brief captures the vision and requirements for SME Supply Chain Risk Analysis._

_It was created through collaborative discovery and reflects the unique needs of this client project._

_Next: PRD workflow will transform this brief into detailed product requirements with functional specifications._
