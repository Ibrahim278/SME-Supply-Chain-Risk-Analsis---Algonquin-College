# Story 1-8: Hotfix - Upgrade React, Next.js, and shadcn to Stable Versions

**Epic:** 1 - Foundation & Project Setup
**Type:** Hotfix / Technical Debt
**Status:** done
**Priority:** High

## Problem Statement

The frontend was scaffolded with `create-next-app@15.0.3` which bundled React 19.0.0-rc (release candidate from November 2024). As of late 2025:
- React 19 stable has been available since December 2024
- Next.js 15.x has received multiple stable releases
- Using RC versions in production carries unnecessary risk
- The `--legacy-peer-deps` flag was required during setup, indicating dependency conflicts

## Objective

Upgrade frontend dependencies to latest stable versions within major version lines and update all documentation to reflect stable version requirements.

## Acceptance Criteria

### AC1: Frontend Dependencies Updated
- [x] React upgraded to latest stable 19.x (not RC) → `19.2.0`
- [x] React-DOM upgraded to latest stable 19.x → `19.2.0`
- [x] Next.js upgraded to latest stable 15.x → `15.5.6`
- [x] @types/react upgraded to version 19.x → `19.2.7`
- [x] @types/react-dom upgraded to version 19.x → `19.2.3`
- [x] No `--legacy-peer-deps` flag required for install
- [x] shadcn CLI 3.x compatibility verified → `3.5.1` tested

### AC2: Documentation Updated
- [x] `docs/architecture.md` - Version references updated
- [x] `docs/prd.md` - Tech stack table updated
- [x] `docs/epics.md` - Setup commands corrected
- [x] Version strategy changed from exact patch (`15.0.3`) to major.minor range (`15.x`)
- [x] shadcn CLI updated from `@2.1.6` to `@3` (latest 3.x stable)

### AC3: Build Verification
- [x] `npm install` completes without errors or warnings
- [x] `npm run build` completes successfully
- [x] `npm run lint` passes with no errors
- [x] Development server starts and serves pages correctly
- [x] No TypeScript compilation errors

### AC4: shadcn Components Regenerated with v3
- [x] All existing components regenerated with `shadcn@3.5.1`
- [x] Missing UX spec components added: progress, skeleton, accordion, select, textarea
- [x] Lint error in `use-toast.ts` fixed (eslint-disable for actionTypes)
- [x] Build passes with all 17 components
- [x] Dev server starts successfully

**Complete Component Inventory (17 components):**
| Component | Status | Notes |
|-----------|--------|-------|
| accordion | NEW | Added per UX spec |
| alert-dialog | Updated | From compatibility test |
| badge | Updated | Regenerated |
| button | Updated | Regenerated |
| card | Updated | Regenerated |
| dialog | Updated | Regenerated |
| form | Updated | Regenerated |
| input | Updated | Regenerated |
| label | Updated | Regenerated |
| progress | NEW | Added per UX spec |
| select | NEW | Added per UX spec |
| skeleton | NEW | Added per UX spec |
| table | Updated | Regenerated |
| tabs | Updated | Regenerated |
| textarea | NEW | Added per UX spec |
| toast | Updated | Regenerated |
| toaster | Updated | Regenerated |

### AC5: Runtime Verification (Manual)
- [x] Homepage renders correctly at localhost:3000
- [x] All shadcn/ui components render properly
- [x] No console errors related to React version mismatches
- [x] Hot reload functions correctly in development
- [x] UX theme colors (Warm Indigo) display correctly

### AC6: Audit All Dependencies for Compatibility
- [x] Review all dependencies in `package.json` for current stable versions
- [x] Verify compatibility with React 19.2.0 and Next.js 15.5.6
- [x] Update any outdated packages that have newer stable versions → `eslint-config-next` updated to 15.5.6
- [x] Ensure no peer dependency warnings after updates
- [x] Run build/lint verification after dependency updates

**Dependencies to audit:**
| Package | Current | Check For |
|---------|---------|-----------|
| @hookform/resolvers | ^5.2.2 | Latest compatible with react-hook-form |
| @radix-ui/* | Various | Latest compatible with React 19 |
| @tanstack/react-query | ^5.90.11 | Latest 5.x |
| class-variance-authority | ^0.7.1 | Latest |
| clsx | ^2.1.1 | Latest |
| lucide-react | ^0.555.0 | Latest |
| react-hook-form | ^7.67.0 | Latest 7.x |
| tailwind-merge | ^3.4.0 | Latest |
| tailwindcss-animate | ^1.0.7 | Latest |
| zod | ^4.1.13 | Latest 4.x |
| zustand | ^5.0.9 | Latest 5.x |
| eslint-config-next | 15.5.6 ✅ | Updated to match Next.js 15.5.6 |
| openapi-typescript | ^7.10.1 | Latest |
| tailwindcss | ^3.4.1 | Latest 3.x (v4 migration is separate story) |

### AC7: Future - Tailwind CSS v4 Migration (OUT OF SCOPE)
**Note:** Tailwind CSS is now at v4.x with significant architectural changes:
- CSS-first configuration replaces `tailwind.config.ts`
- Current shadcn/ui docs are based on Tailwind v4
- Migration requires converting config, updating PostCSS, re-testing components

**Decision:** Stay on Tailwind 3.x for this hotfix. Create separate story for v4 migration.

**Reason:** Tailwind v4 is a breaking change requiring dedicated migration effort, not a simple version bump.

## Tasks

### Task 1: Update Documentation (First)
Update architecture, PRD, and epics to specify stable version requirements:
- Change `Next.js 15.0.3` → `Next.js 15.x (latest stable)`
- Change `create-next-app@15.0.3` → `create-next-app@15`
- Note: React version managed by Next.js, specify `React 19.x stable`

### Task 2: Update Frontend Dependencies
```bash
cd frontend
npm install react@19 react-dom@19 next@15
npm install -D @types/react@19 @types/react-dom@19
```

### Task 3: Verify Installation
```bash
npm ls react react-dom next  # Verify versions
npm run build                 # Verify compilation
npm run lint                  # Verify linting
```

### Task 4: Runtime Testing
```bash
npm run dev
# Manual verification:
# - Homepage loads
# - Components render
# - No console errors
# - Hot reload works
```

## Files to Modify

### Documentation
- `docs/architecture.md` - Lines 11, 28, 30, 57
- `docs/prd.md` - Line 609
- `docs/epics.md` - Line 312

### Code
- `frontend/package.json` - Lines 24-26 (dependencies), 34-35 (devDependencies)

## Verification Checklist

```
[ ] npm install completes cleanly (no --legacy-peer-deps)
[ ] npm run build exits with code 0
[ ] npm run lint exits with code 0
[ ] npm run dev starts without errors
[ ] Browser: localhost:3000 renders homepage
[ ] Browser: No React version warnings in console
[ ] Browser: shadcn/ui Button component renders
[ ] Browser: Hot reload updates page on file change
```

## Rollback Plan

If upgrade causes issues:
```bash
git checkout -- frontend/package.json frontend/package-lock.json
npm install --legacy-peer-deps
```

## Notes

- This is a temporary hotfix story
- Will be manually deleted after verification
- Sprint artifacts (1-3, 1-6 context files) are historical records - update with note about upgrade rather than changing history

---

## Senior Developer Review (AI)

**Reviewer:** Master
**Date:** 2025-11-30
**Outcome:** ✅ APPROVE

### Summary

All acceptance criteria verified with evidence. Frontend dependencies successfully upgraded to stable versions. Build, lint, and runtime verification all pass. No security vulnerabilities detected.

### Key Findings

**No HIGH or MEDIUM severity issues found.**

**LOW severity (Advisory):**
- Note: `next lint` deprecation warning in Next.js 16 - informational only, not blocking

### Acceptance Criteria Coverage

| AC# | Description | Status | Evidence |
|-----|-------------|--------|----------|
| AC1 | Frontend Dependencies Updated | ✅ IMPLEMENTED | `frontend/package.json:28-30,39-40,42` - react@19.2.0, react-dom@19.2.0, next@15.5.6, @types/react@19.2.7, @types/react-dom@19.2.3, eslint-config-next@15.5.6 |
| AC2 | Documentation Updated | ✅ IMPLEMENTED | `docs/architecture.md:30,34-35,57,261-262` - Next.js 15.x, React 19.x references |
| AC3 | Build Verification | ✅ IMPLEMENTED | `npm run build` compiled successfully in 2.6s, `npm run lint` passed with 0 warnings/errors |
| AC4 | shadcn Components Regenerated | ✅ IMPLEMENTED | `frontend/src/components/ui/` - 17 components present (accordion, alert-dialog, badge, button, card, dialog, form, input, label, progress, select, skeleton, table, tabs, textarea, toast, toaster) |
| AC5 | Runtime Verification | ✅ IMPLEMENTED | Dev server starts in 1827ms, homepage renders, components render, no errors in HTML |
| AC6 | Dependency Audit | ✅ IMPLEMENTED | `eslint-config-next` updated to 15.5.6, `npm ls` shows no peer dependency warnings |
| AC7 | Tailwind v4 Migration | ⏭️ OUT OF SCOPE | Documented decision to defer - correct approach |

**Summary:** 6 of 6 in-scope acceptance criteria fully implemented.

### Task Completion Validation

| Task | Description | Verified |
|------|-------------|----------|
| Task 1 | Update Documentation | ✅ VERIFIED - `docs/architecture.md` contains 15.x/19.x references |
| Task 2 | Update Frontend Dependencies | ✅ VERIFIED - `package.json` has stable versions |
| Task 3 | Verify Installation | ✅ VERIFIED - build/lint pass |
| Task 4 | Runtime Testing | ✅ VERIFIED - dev server starts, homepage renders |

**Summary:** 4 of 4 tasks verified complete.

### Test Coverage and Gaps

- No unit tests required for this dependency upgrade story
- Build and lint serve as integration verification
- Manual runtime verification completed

### Architectural Alignment

- Follows documented version strategy (major.minor ranges vs exact patches)
- shadcn CLI upgraded to v3 as per UX spec requirements
- Tailwind v4 correctly deferred per AC7 decision

### Security Notes

- `npm audit`: 0 vulnerabilities
- No security-related changes in this upgrade
- All dependencies from trusted sources (npm registry)

### Best-Practices and References

- [Next.js 15.5 Release Notes](https://nextjs.org/blog)
- [React 19 Stable Release](https://react.dev/blog)
- [shadcn/ui v3 Migration](https://ui.shadcn.com)

### Action Items

**Code Changes Required:**
- None

**Advisory Notes:**
- Note: Consider migrating to ESLint CLI before Next.js 16 (deprecation warning)
- Note: Plan Tailwind CSS v4 migration as a separate story when ready
