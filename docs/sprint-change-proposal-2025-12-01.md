# Sprint Change Proposal: Epic Renumbering

**Date:** 2025-12-01
**Author:** Bob (Scrum Master Agent)
**Status:** Approved
**Scope:** Minor (Documentation Only)

---

## Section 1: Issue Summary

### Problem Statement
Epic numbering in project documentation does not align with actual execution order. Epics 6 and 7 (Admin Risk Framework Configuration, Admin Data Sources & Countries) are numbered as if they come after Epic 5, but per documented dependencies they execute in parallel with Epic 3 and must complete before the current Epic 4.

### Discovery Context
Identified during sprint planning review when analyzing the dependency graph in `docs/epics.md`. The sequencing rationale explicitly states "Epics 6-7 can begin after Epic 2 (Admin exists) and complete before Epic 4 needs config."

### Evidence
From `docs/epics.md` lines 30-39:
```
Epic 1 (Foundation) → Epic 2 (Auth) → Epic 3 (Submission) → Epic 4 (Assessment) → Epic 5 (Results)
                                                                    ↓
                                          Epic 6 (Risk Config) ← Epic 7 (Data Sources)

- **Epics 6-7** can begin after Epic 2 (Admin exists) and complete before Epic 4 needs config
```

This creates cognitive friction: the instruction "start 6 & 7 after 2, complete before 4" is counterintuitive given the numbering.

---

## Section 2: Impact Analysis

### Epic Impact
| Current # | New # | Epic Name | Impact |
|-----------|-------|-----------|--------|
| 1 | 1 | Foundation & Project Setup | No change |
| 2 | 2 | User Authentication & Access | No change |
| 3 | 3 | Supplier Submission & Status | No change |
| 4 | **6** | Agentic Assessment Pipeline | Renumbered |
| 5 | **7** | Results & Reporting | Renumbered |
| 6 | **4** | Admin Risk Framework Config | Renumbered |
| 7 | **5** | Admin Data Sources & Countries | Renumbered |

### Story Impact
- Story numbers within each epic will be updated (e.g., Story 4.1 → 6.1 for Pipeline stories)
- No story content changes required
- No acceptance criteria changes

### Artifact Conflicts
| Artifact | References Found | Action |
|----------|------------------|--------|
| `docs/epics.md` | 30+ | Full renumber |
| `docs/implementation-readiness-report-2025-11-28.md` | 8 | Update diagrams |
| `docs/sprint-artifacts/sprint-status.yaml` | 5 sections | Renumber |
| `docs/sprint-artifacts/1-2-*.md` | 2 | Update comments |
| `docs/sprint-artifacts/1-3-*.md` | 4 | Update comments |
| `docs/sprint-artifacts/1-6-*.md` | 1 | Update comment |
| `docs/prd.md` | 0 | No change |
| `docs/architecture.md` | 0 | No change |

### Technical Impact
- **Code:** None — no code references epic numbers
- **Infrastructure:** None
- **Deployment:** None

---

## Section 3: Recommended Approach

### Selected Path: Direct Adjustment

**Rationale:**
1. Pure documentation change with no code impact
2. Low effort (~1-2 hours)
3. Low risk — only text/number replacements
4. High value — eliminates ongoing confusion during sprint planning

**Effort Estimate:** Low
**Risk Level:** Low
**Timeline Impact:** None

**Alternatives Considered:**
- Keep current numbering with explanatory notes → Rejected (cognitive overhead persists)
- Use sub-numbers like 3a, 3b → Rejected (adds complexity, doesn't solve root issue)

---

## Section 4: Detailed Change Proposals

### Proposal 1: Epic Summary Table
**File:** `docs/epics.md` (lines 18-27)

Reorder table rows:
```
| 4 | Admin Risk Framework Config | 6 | ... |
| 5 | Admin Data Sources & Countries | 8 | ... |
| 6 | Agentic Assessment Pipeline | 7 | ... |
| 7 | Results & Reporting | 9 | ... |
```

### Proposal 2: Sequencing Diagram
**File:** `docs/epics.md` (lines 30-39)

Replace with parallel execution diagram:
```
Epic 1 → Epic 2 ─┬─→ Epic 3 ──────────────┐
                 ├─→ Epic 4 (Risk Config) ─┼─→ Epic 6 (Pipeline) → Epic 7 (Results)
                 └─→ Epic 5 (Data Sources) ┘
```

### Proposal 3: Epic Section Headers
**File:** `docs/epics.md`

Renumber all `## Epic X:` headers and corresponding story numbers.

### Proposal 4: FR Coverage Tables
**File:** `docs/epics.md`

Update all FR-to-Epic mappings in coverage tables.

### Proposal 5: Dependency Graph
**File:** `docs/epics.md` (Final Summary section)

Update ASCII diagram and implementation recommendations.

### Proposal 6: Sprint Status
**File:** `docs/sprint-artifacts/sprint-status.yaml`

Renumber epic sections and story IDs.

### Proposal 7: Supporting Docs
**Files:** Implementation readiness report, story file comments

Update all epic number references.

---

## Section 5: Implementation Handoff

### Scope Classification: Minor

This change can be implemented directly by the development team or documentation maintainer.

### Handoff Recipients
- **Primary:** SM Agent (Bob) or Dev Agent — execute documentation updates
- **Notification:** PM Agent (John) — awareness of numbering change

### Responsibilities
1. Execute all 7 approved edit proposals
2. Verify no broken cross-references after renumbering
3. Update Document History in `docs/epics.md`
4. Commit with message: "docs: renumber epics to match execution order"

### Success Criteria
- [x] All epic numbers in docs align with execution sequence
- [x] Dependency diagrams show correct parallel/sequential flow
- [x] Sprint status file reflects new numbering
- [x] No orphaned references to old epic numbers

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-01 | SM Agent (Bob) | Initial Sprint Change Proposal |

---

*Generated via BMad Method correct-course workflow*
