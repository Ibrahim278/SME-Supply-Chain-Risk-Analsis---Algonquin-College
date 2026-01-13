# System-Level Test Design

**Project:** SME Supply Chain Risk Analysis
**Date:** 2025-11-28
**Author:** Master (via TEA Agent)
**Status:** Draft

---

## Executive Summary

This document provides the system-level testability assessment for the SME Supply Chain Risk Analysis platform before the implementation-readiness gate check. The architecture is **testable with mitigations** - no blockers identified, but 3 high-risk areas require attention.

**Overall Assessment: PASS (with CONCERNS)**

---

## Testability Assessment

### Controllability: PASS

| Factor | Status | Evidence |
|--------|--------|----------|
| State Control | ✅ | API-first design enables test data seeding via REST endpoints |
| External Dependencies | ✅ | Interfaces for LLM (LangGraph), database (SQLAlchemy), cache (Redis) - all mockable |
| Error Injection | ⚠️ | No explicit chaos engineering hooks - recommend failure injection points |
| Data Reset | ✅ | Soft delete pattern + transaction rollback capability |

**Recommendation:** Add failure injection endpoints for agent nodes (data_collection, evidence_analysis, risk_assessment, report_generation) to enable resilience testing.

### Observability: PASS (with concerns)

| Factor | Status | Evidence |
|--------|--------|----------|
| Logging | ✅ | structlog JSON logging with request_id correlation |
| Metrics | ⚠️ | No APM/metrics layer defined - performance testing harder |
| Traces | ✅ | request_id for request tracing, assessment:{id} Redis channel |
| Agent Status | ✅ | SSE status updates with progress percentage |

**Recommendation:** Add Prometheus metrics endpoint for:
- Request latency (p50, p95, p99)
- Assessment processing time per node
- LLM token usage and latency
- Error rates by endpoint

### Reliability: PASS (with concerns)

| Factor | Status | Evidence |
|--------|--------|----------|
| Test Isolation | ✅ | user_id filter enforced at service layer |
| Determinism | ⚠️ | LLM calls non-deterministic; needs temperature=0 enforcement |
| Parallel Safety | ✅ | Stateless API design; LangGraph checkpointing |
| Cleanup | ✅ | Soft delete + fixture teardown patterns |

**Recommendation:** Enforce `temperature=0` for all LLM calls in risk_assessment and evidence_analysis nodes. Add variance threshold validation (±5%) to test suite.

---

## Architecturally Significant Requirements (ASRs)

### High-Priority Risks (Score ≥6)

| Risk ID | ASR | Category | P | I | Score | Mitigation | Owner |
|---------|-----|----------|---|---|-------|------------|-------|
| ASR-001 | NFR11: Deterministic Scoring | TECH | 2 | 3 | **6** | Enforce temperature=0; snapshot tests for agent outputs; variance threshold validation | Backend Lead |
| ASR-002 | NFR5: RBAC Enforcement | SEC | 2 | 3 | **6** | Comprehensive auth matrix tests (96 FRs × 2 roles); negative permission tests | Security Lead |
| ASR-003 | NFR33: Data Isolation | SEC | 2 | 3 | **6** | Assert user_id filter in every query; cross-user access tests | Backend Lead |

### Medium-Priority Risks (Score 3-5)

| Risk ID | ASR | Category | P | I | Score | Mitigation | Owner |
|---------|-----|----------|---|---|-------|------------|-------|
| ASR-004 | NFR15: Background Processing | PERF | 2 | 2 | 4 | ARQ worker integration tests with Redis | Backend Lead |
| ASR-005 | NFR16: Real-time Updates | TECH | 2 | 2 | 4 | SSE testing with EventSource mocking | Frontend Lead |
| ASR-006 | NFR10: Graceful Degradation | TECH | 2 | 2 | 4 | Failure injection tests for partial results | QA Lead |

### Low-Priority Risks (Score 1-2)

| Risk ID | ASR | Category | P | I | Score | Mitigation |
|---------|-----|----------|---|---|-------|------------|
| ASR-007 | NFR6/7: Ethical Scraping | BUS | 1 | 2 | 2 | robots.txt compliance tests |
| ASR-008 | MinIO Integration | OPS | 1 | 1 | 1 | Test containers for S3-compatible storage |

---

## Test Levels Strategy

### Recommended Distribution

| Level | Target % | Rationale |
|-------|----------|-----------|
| **Unit** | 50% | Agent nodes, business logic, pure functions |
| **Integration** | 30% | Database, Redis, ARQ, LangGraph workflows |
| **E2E** | 20% | Critical user journeys, admin config flows |

### Level-to-Component Mapping

| Component | Unit | Integration | E2E |
|-----------|------|-------------|-----|
| Agent Nodes (FR17-42) | ✅ Primary | ⚠️ Workflow | - |
| Services (business logic) | ✅ Primary | - | - |
| API Endpoints | - | ✅ Primary | ⚠️ Critical paths |
| Database Operations | - | ✅ Primary | - |
| LangGraph Workflow | ⚠️ Node logic | ✅ Primary | - |
| User Journeys (FR10-16) | - | - | ✅ Primary |
| Admin Config (FR64-91) | - | ⚠️ API | ✅ Primary |
| Real-time Status (FR15-16) | - | ✅ SSE | ⚠️ Visual |

### Anti-Patterns to Avoid

- ❌ E2E testing for risk scoring logic (use unit tests)
- ❌ Unit testing LangGraph state transitions (use integration)
- ❌ Integration testing shadcn/ui components (use E2E or component)
- ❌ Duplicate coverage at multiple levels

---

## NFR Testing Approach

### Security (NFR1-9)

| NFR | Test Type | Tool | Validation |
|-----|-----------|------|------------|
| NFR1: Password Hashing | Unit | pytest | Argon2id algorithm verification |
| NFR2: TLS 1.2+ | E2E | Playwright + security headers | SSL/TLS handshake validation |
| NFR3: Session Expiry | E2E | Playwright | JWT expiration (24h access, 7d refresh) |
| NFR4: Input Validation | Integration | pytest | Pydantic schema rejection tests |
| NFR5: Auth/Authz | E2E + API | Playwright + pytest | Permission matrix coverage |
| NFR6/7: Ethical Scraping | Unit | pytest | robots.txt parser tests |
| NFR8: Encrypted Secrets | Unit | pytest | Credential encryption validation |
| NFR9: Audit Logging | Integration | pytest | Security event log assertions |

**Test Files:**
- `tests/nfr/security/test_authentication.py`
- `tests/nfr/security/test_authorization.py`
- `tests/nfr/security/test_input_validation.py`
- `tests/e2e/security/auth-flows.spec.ts`

### Performance (NFR15-20)

| NFR | Test Type | Tool | Threshold |
|-----|-----------|------|-----------|
| NFR15: Background Processing | Load | k6 | 10 concurrent assessments, no degradation |
| NFR17: Configurable Timeouts | Integration | pytest | Agent task timeout (5 min per node) |
| NFR18: Parallel Execution | Load | k6 | Data source queries execute in parallel |
| NFR19: Page Load | E2E | Lighthouse | <3s for dashboard pages |
| NFR20: Concurrent Assessments | Stress | k6 | 50+ concurrent users, <500ms p95 |

**Test Files:**
- `tests/nfr/performance/load-test.k6.js`
- `tests/nfr/performance/stress-test.k6.js`
- `tests/nfr/performance/lighthouse.spec.ts`

**SLO Thresholds (k6):**
```javascript
thresholds: {
  http_req_duration: ['p(95)<500'],  // 95% of requests under 500ms
  errors: ['rate<0.01'],              // Error rate under 1%
  api_duration: ['p(99)<1000'],       // 99% of API calls under 1s
}
```

### Reliability (NFR10-14)

| NFR | Test Type | Tool | Validation |
|-----|-----------|------|------------|
| NFR10: Graceful Degradation | E2E | Playwright | API failure → partial results shown |
| NFR11: Deterministic Scoring | Unit | pytest | Same inputs → ±5% variance |
| NFR12: Automatic Retries | Integration | pytest | 3 retries on transient failures |
| NFR13: Incomplete Indicators | E2E | Playwright | Warning UI for missing data |
| NFR14: Backups | OPS | Infrastructure | Point-in-time recovery validation |

**Test Files:**
- `tests/nfr/reliability/test_graceful_degradation.py`
- `tests/nfr/reliability/test_retry_logic.py`
- `tests/e2e/reliability/error-states.spec.ts`

### Maintainability (NFR27-30)

| NFR | Test Type | Tool | Threshold |
|-----|-----------|------|-----------|
| NFR27: Documentation | CI | - | Inline docs required for key functions |
| NFR28: Modularity | Static Analysis | ruff, mypy | Type coverage >90% |
| NFR29: Config Without Code | Integration | pytest | Admin config changes apply correctly |
| NFR30: Agent Logging | Integration | pytest | structlog output validated |

**CI Jobs:**
```yaml
- test-coverage:    # pytest-cov ≥80%
- code-duplication: # jscpd <5%
- type-checking:    # mypy strict
- linting:          # ruff + eslint
```

---

## Test Environment Requirements

### Local Development

| Component | Implementation |
|-----------|----------------|
| PostgreSQL 16 | Docker container with pgvector |
| Redis 7 | Docker container |
| MinIO | Docker container (S3-compatible) |
| LLM | Mock (langchain-mock or fixture responses) |

**Docker Compose (dev):**
```yaml
services:
  postgres-test:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: sme_test
      POSTGRES_PASSWORD: test
  redis-test:
    image: redis:7-alpine
  minio-test:
    image: minio/minio
    command: server /data
```

### CI Environment

| Component | Implementation |
|-----------|----------------|
| PostgreSQL | Test container (ephemeral per run) |
| Redis | Test container |
| MinIO | Test container or mock |
| LLM | Mocked responses (no API calls) |

### Staging Environment

| Component | Implementation |
|-----------|----------------|
| Full Stack | Docker Compose replica |
| LLM | Real LLM API via configured provider (rate-limited test account) |
| Data Sources | Sandbox/mock endpoints |

---

## Testability Concerns

### Concern 1: LLM Determinism (Score: 6)

**Problem:** LLM outputs are inherently non-deterministic. NFR11 requires consistent risk scores within ±5% variance.

**Mitigation:**
1. Enforce `temperature=0` for all LLM calls
2. Use snapshot testing for agent outputs (golden file comparison)
3. Add variance threshold validation in CI
4. Seed random number generators in test environment

**Implementation:**
```python
# app/agents/config.py
LLM_CONFIG = {
    "temperature": 0,  # Enforce determinism
    "seed": 42,        # If supported by provider
}

# tests/agents/test_risk_assessment.py
def test_risk_score_determinism():
    evidence = create_test_evidence()
    scores = [calculate_risk_score(evidence) for _ in range(10)]
    variance = max(scores) - min(scores)
    assert variance <= 5, f"Score variance {variance}% exceeds 5% threshold"
```

### Concern 2: External API Mocking (Score: 4)

**Problem:** Data collection agents query external APIs (sanctions lists, registries, ESG databases). Tests must not depend on external services.

**Mitigation:**
1. Create abstraction layer for all external data sources
2. Use HAR capture for realistic mock responses
3. Implement fixture factories for each source type

**Implementation:**
```python
# app/agents/tools/base.py
class DataSourceClient(Protocol):
    async def fetch(self, query: str) -> dict: ...

# tests/fixtures/data_sources.py
class MockSanctionsClient:
    def __init__(self, responses: dict):
        self.responses = responses

    async def fetch(self, query: str) -> dict:
        return self.responses.get(query, {"matches": []})
```

### Concern 3: SSE Testing (Score: 2)

**Problem:** Real-time assessment status updates use Server-Sent Events. Testing SSE connections requires special handling.

**Mitigation:**
1. Use Playwright's native EventSource support
2. Mock Redis pub/sub in integration tests
3. Validate SSE message format in unit tests

**Implementation:**
```typescript
// tests/e2e/assessment/status-tracking.spec.ts
test('receives real-time status updates', async ({ page }) => {
  const assessmentId = await createAssessment(page);

  const statusUpdates: string[] = [];
  page.on('response', async (response) => {
    if (response.url().includes('/status')) {
      const reader = response.body()?.getReader();
      // Collect SSE events
    }
  });

  await page.goto(`/assessments/${assessmentId}`);
  await expect(page.getByTestId('status')).toHaveText(/collecting|analyzing|complete/);
});
```

---

## Recommendations for Sprint 0

### 1. Test Framework Setup (`*framework` workflow)

**Backend (Python):**
- pytest + pytest-asyncio
- pytest-cov (coverage ≥80%)
- factory_boy + faker (test data)
- httpx (async API testing)
- pytest-docker (containers)

**Frontend (TypeScript):**
- Playwright (E2E + API)
- Vitest (unit tests)
- MSW (API mocking)
- Testing Library (component tests)

**Performance:**
- k6 (load/stress/spike testing)
- Lighthouse CI (Core Web Vitals)

### 2. CI Pipeline Structure (`*ci` workflow)

```yaml
name: CI Pipeline

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Backend linting
        run: ruff check && mypy app/
      - name: Frontend linting
        run: npm run lint

  unit:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - name: Run unit tests
        run: pytest tests/unit -n auto --cov=app --cov-report=xml
      - name: Check coverage threshold
        run: coverage report --fail-under=80

  integration:
    runs-on: ubuntu-latest
    needs: lint
    services:
      postgres:
        image: pgvector/pgvector:pg16
      redis:
        image: redis:7-alpine
    steps:
      - name: Run integration tests
        run: pytest tests/integration

  e2e:
    runs-on: ubuntu-latest
    needs: [unit, integration]
    steps:
      - name: Start services
        run: docker compose -f docker-compose.test.yml up -d
      - name: Run E2E tests
        run: npx playwright test --shard=${{ matrix.shard }}/4
    strategy:
      matrix:
        shard: [1, 2, 3, 4]

  performance:
    runs-on: ubuntu-latest
    if: github.event_name == 'schedule' || contains(github.event.head_commit.message, '[perf]')
    steps:
      - name: Run k6 load tests
        run: k6 run tests/nfr/performance/load-test.k6.js
```

### 3. Test Data Strategy

**Factory Pattern:**
```python
# tests/factories/user.py
from factory import Factory, Faker, LazyAttribute

class UserFactory(Factory):
    class Meta:
        model = dict

    email = Faker('email')
    password_hash = LazyAttribute(lambda _: hash_password('password123'))
    role = 'user'
    is_active = True
```

**Fixture with Auto-Cleanup:**
```python
# tests/conftest.py
@pytest.fixture
async def user(db_session):
    user = UserFactory()
    db_session.add(User(**user))
    await db_session.commit()
    yield user
    await db_session.delete(user)
    await db_session.commit()
```

### 4. LLM Testing Strategy

**Unit Tests (Mocked):**
```python
# tests/agents/test_evidence_analysis.py
@pytest.fixture
def mock_llm():
    return MockLLM(responses={
        "tag_evidence": {"reliability": "high", "recency": "current"}
    })

def test_evidence_tagging(mock_llm):
    node = EvidenceAnalysisNode(llm=mock_llm)
    result = node.process(test_evidence)
    assert result.reliability == "high"
```

**Integration Tests (Snapshot):**
```python
# tests/agents/test_risk_assessment_integration.py
def test_risk_score_snapshot(snapshot):
    evidence = load_test_evidence("supplier_acme.json")
    result = risk_assessment_node.process(evidence)
    snapshot.assert_match(result.model_dump(), "acme_risk_score")
```

---

## Quality Gate Criteria

### Pre-Implementation Readiness

- [x] Testability assessment complete (this document)
- [ ] Test framework initialized (Sprint 0)
- [ ] CI pipeline configured (Sprint 0)
- [ ] Test data factories created (Sprint 0)
- [ ] Mock infrastructure ready (Sprint 0)

### Per-Epic Release Criteria

- [ ] P0 tests pass: 100%
- [ ] P1 tests pass: ≥95%
- [ ] Test coverage: ≥80% for new code
- [ ] No high-risk (≥6) items unmitigated
- [ ] NFR validation complete (security, performance, reliability)

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-28 | TEA Agent (Murat) | Initial system-level testability review |

---

_Generated by BMad TEA Agent - Test Architect Module_
_Workflow: `.bmad/bmm/testarch/test-design` (System-Level Mode)_
_Version: 4.0 (BMad v6)_
