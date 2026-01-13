# SME Supply Chain Risk Analysis UX Design Specification

_Created on 2025-11-28 by Master_
_Generated using BMad Method - Create UX Design Workflow v1.0_

---

## Executive Summary

An AI-powered due diligence platform enabling SME clients to evaluate ESG and modern slavery risks in their supply chains through a "verify first" approach that investigates public data sources directly.

**Core Emotional Goal:** *"Thank goodness — I don't have to figure this out alone. The system has my back."*

The platform serves as a screening/triage tool that surfaces risk signals and evidence, then guides users toward appropriate next steps — including when to invest in Enhanced Due Diligence (EDD) through paid services.

**Two Primary User Types:**
- **Admin (Consultancy):** Configure risk frameworks, data sources, country settings, manage users
- **User (SME Clients):** Submit suppliers, view risk assessments, access evidence, receive recommendations

---

## 1. Design System Foundation

### 1.1 Design System Choice

**Selected:** shadcn/ui

**Rationale:**
- Clean, professional aesthetic that builds trust
- Fully customizable for "reassuring" tone (not cold corporate)
- Tailwind-based for rapid iteration and consistent spacing/colors
- Accessible by default (WCAG compliance built-in)
- Lightweight — only import what you need

**What shadcn/ui Provides:**
- Buttons, forms, inputs, selects, checkboxes
- Cards, dialogs, modals, sheets
- Tables, data display components
- Navigation, tabs, breadcrumbs
- Toast notifications, alerts
- Progress indicators, skeletons

---

## 2. Core User Experience

### 2.1 Platform Requirements

- **Primary Platform:** Responsive web application
- **Supported Devices:** Desktop (PC/Mac), tablet, mobile browsers
- **Native Apps:** Out of scope for MVP

### 2.2 Defining Experience

**The Core Moment:** Submitting a new supplier for assessment

> "I need to vet this company before we work with them"

This is the gateway interaction — where trust begins. The supplier submission flow must feel effortless and clear, like sending a message: quick, confident, "I know exactly what happens next."

**All Critical User Actions (in priority order):**
1. **Submit a new supplier** — The entry point; must be frictionless
2. **View results and understand risk** — Clear verdict with evidence and recommendations
3. **Check on pending assessments** — Status visibility during background processing
4. **Dig into evidence** — Transparency for auditors and decision confidence

### 2.3 Desired Emotional Response

**Target Feeling:** Relieved and reassured

> "Thank goodness — I don't have to figure this out alone. The system has my back."

**Design Implications:**

| Principle | Implementation |
|-----------|----------------|
| Supportive tone | Language that guides, not intimidates |
| Clear next steps | Never leave users wondering "now what?" |
| Reassuring feedback | Progress indicators that calm, not stress |
| Conclusive results | Verdicts that resolve uncertainty with clear recommendations |
| Gentle error handling | Problems feel solvable, not scary |
| Expert backup | The system feels like a knowledgeable partner |

### 2.4 Core Experience Principles

| Principle | Definition |
|-----------|------------|
| **Speed** | Submission in under 2 minutes; results feel immediate even when processing |
| **Guidance** | High hand-holding; never leave users wondering what to do next |
| **Flexibility** | Low for SME users (guided paths); higher for Admin (configuration power) |
| **Feedback** | Reassuring, celebratory on success, gentle on errors |

### 2.5 Risk Assessment Outcomes

The app is a screening/triage tool — it informs and guides, not judges:

| Risk Level | Display | Recommendation |
|------------|---------|----------------|
| **Low Risk** | Green badge ✓ | "Proceed with standard onboarding" |
| **Medium Risk** | Amber badge ⚠ | "Consider Enhanced Due Diligence" |
| **High Risk** | Red badge ✕ | "Enhanced Due Diligence Strongly Recommended" |
| **Insufficient Data** | Gray badge ? | "Enhanced Due Diligence Recommended" |

---

## 3. Visual Foundation

### 3.1 Color System

**Theme:** Warm Indigo — Modern, AI-innovation feel while staying warm and trustworthy

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| **Primary** | Indigo | `#6366f1` | Main actions, key elements, active states |
| **Primary Dark** | Deep Indigo | `#4f46e5` | Hover states, emphasis |
| **Primary Light** | Light Indigo | `#818cf8` | Links, highlights |
| **Primary Subtle** | Indigo Wash | `#e0e7ff` | Backgrounds, selected states |
| **Success / Low Risk** | Green | `#22c55e` | Positive outcomes, low risk |
| **Success Background** | Light Green | `#dcfce7` | Low risk badge background |
| **Warning / Medium Risk** | Amber | `#f59e0b` | Caution, medium risk |
| **Warning Background** | Light Amber | `#fef3c7` | Medium risk badge background |
| **Error / High Risk** | Red | `#ef4444` | Problems, high risk |
| **Error Background** | Light Red | `#fee2e2` | High risk badge background |

**Neutral Scale (Slate):**

| Token | Hex | Usage |
|-------|-----|-------|
| `slate-50` | `#f8fafc` | Page backgrounds |
| `slate-100` | `#f1f5f9` | Card backgrounds, subtle fills |
| `slate-200` | `#e2e8f0` | Borders, dividers |
| `slate-300` | `#cbd5e1` | Disabled states |
| `slate-400` | `#94a3b8` | Placeholder text |
| `slate-500` | `#64748b` | Secondary text |
| `slate-600` | `#475569` | Body text |
| `slate-700` | `#334155` | Headings |
| `slate-800` | `#1e293b` | Primary text |
| `slate-900` | `#0f172a` | High emphasis, sidebar bg |

### 3.2 Typography

**Font Family:** System font stack (native feel, fast loading)
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
```

**Type Scale:**
| Element | Size | Weight | Line Height |
|---------|------|--------|-------------|
| H1 | 2rem (32px) | 700 | 1.2 |
| H2 | 1.5rem (24px) | 600 | 1.3 |
| H3 | 1.25rem (20px) | 600 | 1.4 |
| H4 | 1rem (16px) | 600 | 1.5 |
| Body | 1rem (16px) | 400 | 1.6 |
| Small | 0.875rem (14px) | 400 | 1.5 |
| Caption | 0.75rem (12px) | 400 | 1.4 |

### 3.3 Spacing System

**Base Unit:** 4px

| Token | Value | Usage |
|-------|-------|-------|
| `xs` | 4px | Tight spacing, icon gaps |
| `sm` | 8px | Compact elements |
| `md` | 16px | Standard spacing |
| `lg` | 24px | Section spacing |
| `xl` | 32px | Major sections |
| `2xl` | 48px | Page sections |

**Interactive Visualizations:**

- Color Theme Explorer: [ux-color-themes.html](./ux-color-themes.html)

---

## 4. Design Direction

### 4.1 Chosen Design Approach

**Hybrid approach combining multiple directions:**

| Screen | Direction | Rationale |
|--------|-----------|-----------|
| **SME Home/Dashboard** | Action-Oriented (#2) | Welcoming, shows "what needs attention", clear next steps |
| **Supplier List** | Card Gallery (#5) | Visual and scannable, less intimidating than dense tables |
| **Submission Flow** | Guided Wizard (#6) | Step-by-step hand-holding, maximum reassurance |
| **Results View** | Card-based progressive disclosure | Summary first, evidence on demand |
| **Admin Dashboard** | Sidebar Dashboard (#1) | Persistent navigation for frequent use |
| **Admin Config** | Data Table (#4) | Dense, filterable for managing many items |

### 4.2 Layout Patterns

**SME User Experience:**
- Top navigation bar
- Action-oriented home with card CTAs
- Card-based supplier gallery with tab filtering
- Centered wizard for submission flow
- Progressive disclosure for results

**Admin Experience:**
- Persistent sidebar navigation
- Stat cards for overview
- Data tables with filtering for configuration
- Wizard-style flow for country setup (AI-assisted)

**Interactive Mockups:**

- Design Direction Showcase: [ux-design-directions.html](./ux-design-directions.html)

---

## 5. User Journey Flows

### 5.1 Critical User Paths

#### Journey 1: Submit Supplier for Assessment (Core Experience)

**User:** SME Client
**Goal:** "I need to vet this company before we work with them"
**Flow:** Guided Wizard (4 steps)

| Step | Content | Actions |
|------|---------|---------|
| **1. Basic Info** | Supplier name*, Country*, Website (optional) | Continue |
| **2. Context** | Sector*, Description (optional), Concerns (optional) | Back, Continue |
| **3. Review** | Summary of entered info + confirmation checkbox | Back, Start Assessment |
| **4. Confirmation** | Success message + progress link | View Progress, Return to Dashboard |

#### Journey 2: View Results & Recommendations

**User:** SME Client
**Goal:** "What did the assessment find? What should I do?"
**Flow:** Card-based progressive disclosure

| Stage | Content |
|-------|---------|
| **Summary Card** | Supplier name, overall risk badge, one-line summary, recommendation banner |
| **Risk Categories** | Traffic light indicators for ESG, Modern Slavery, Financial |
| **Evidence Drill-down** | Expandable sections per category with source attribution |
| **Recommended Actions** | Clear next steps based on risk level (proceed / consider EDD / EDD recommended) |

#### Journey 3: Track Assessment Progress

**User:** SME Client
**Flow:** Dashboard card with inline status

| Stage | Display |
|-------|---------|
| **Collecting** | "Searching public sources..." with animated indicator |
| **Analyzing** | "Analyzing evidence..." |
| **Scoring** | "Calculating risk scores..." |
| **Complete** | "Assessment ready" with View Results CTA |

#### Journey 4: Admin - Configure Risk Framework

**User:** Consultancy Admin
**Flow:** Table view + modal editor

#### Journey 5: Admin - Add New Country

**User:** Consultancy Admin
**Flow:** Wizard with AI-assisted data source discovery

---

## 6. Component Library

### 6.1 From shadcn/ui (Standard)

| Component | Usage |
|-----------|-------|
| Button | Primary, secondary, ghost actions |
| Input, Select, Textarea | Form fields |
| Card | Supplier cards, stat cards, result cards |
| Table | Admin data views |
| Dialog/Modal | Confirmations, detail views |
| Tabs | Risk category switching, view modes |
| Progress | Assessment progress indicator |
| Badge | Status indicators |
| Toast | Success/error notifications |
| Skeleton | Loading states |
| Accordion | Evidence drill-down sections |

### 6.2 Custom Components

| Component | Purpose | Key States |
|-----------|---------|------------|
| **RiskBadge** | Traffic light risk indicator | Low (green), Medium (amber), High (red), Insufficient (gray) |
| **RiskSummaryCard** | Overall assessment result | Complete, Pending, Error |
| **RiskCategoryCard** | Individual risk score (ESG, etc.) | Score + drill-down trigger |
| **EvidenceItem** | Single source in evidence log | Source type, reliability, timestamp, link |
| **AssessmentStatusTracker** | Real-time progress during processing | Collecting → Analyzing → Scoring → Complete |
| **SupplierCard** | Supplier in list/gallery view | Risk level, confidence, last updated |
| **WizardStepper** | Progress indicator for submission | Steps completed/current/remaining |
| **RecommendationBanner** | EDD recommendation display | Proceed / Consider EDD / EDD Strongly Recommended |

---

## 7. UX Pattern Decisions

### 7.1 Consistency Rules

| Category | Decision | Rationale |
|----------|----------|-----------|
| **Button Hierarchy** | Primary (filled) → Secondary (outline) → Ghost (text) | Clear visual priority |
| **Feedback - Success** | Toast notification (top-right, auto-dismiss 5s) | Non-blocking, reassuring |
| **Feedback - Error** | Inline + toast for form errors; modal for critical failures | Gentle, actionable |
| **Feedback - Loading** | Skeleton loaders for content; spinner for actions | Feels faster, less anxious |
| **Forms - Labels** | Above input, always visible | Clear, accessible |
| **Forms - Validation** | On blur (field-level) + on submit (summary) | Immediate but not aggressive |
| **Forms - Required** | Asterisk (*) with "* Required" legend | Standard, understood |
| **Forms - Help Text** | Below input as caption; tooltip for complex fields | Progressive disclosure |
| **Modals - Dismiss** | Click outside to close; Escape key; explicit X button | Flexible, not trapped |
| **Empty States** | Friendly illustration + clear CTA | Guided, not dead-end |
| **Confirmations** | Modal for destructive actions (delete); inline for reversible | Protect from mistakes |
| **Notifications** | Top-right toast stack; max 3 visible; newest on top | Non-intrusive |
| **Navigation - Active** | Filled background (sidebar) or underline (top nav) | Clear "you are here" |
| **Back Button** | App-level back (not browser) within wizards | Controlled experience |
| **Dates** | Relative for recent ("2 hours ago"); absolute for older ("Nov 28, 2025") | Human-readable |
| **Risk Colors** | Green/Amber/Red only for risk; Indigo for actions/brand | No confusion |

---

## 8. Responsive Design & Accessibility

### 8.1 Responsive Strategy

**Breakpoints:**

| Breakpoint | Width | Layout |
|------------|-------|--------|
| **Mobile** | < 640px | Single column, hamburger menu, full-width cards |
| **Tablet** | 640px - 1024px | 2-column cards, collapsible sidebar |
| **Desktop** | > 1024px | Full layout, sidebar visible, multi-column |

**Adaptation Patterns:**

| Element | Desktop | Tablet | Mobile |
|---------|---------|--------|--------|
| SME Navigation | Top nav bar | Top nav bar | Hamburger menu |
| Admin Navigation | Sidebar (fixed) | Sidebar (collapsible) | Hamburger menu |
| Supplier Cards | 3-column grid | 2-column grid | Single column |
| Data Tables | Full table | Horizontal scroll | Card view |
| Wizards | Centered card | Centered card | Full-width |
| Modals | Centered overlay | Centered overlay | Full-screen sheet |

### 8.2 Accessibility Requirements

**Target:** WCAG 2.1 Level AA

| Requirement | Implementation |
|-------------|----------------|
| **Color Contrast** | 4.5:1 minimum for text; 3:1 for large text/UI |
| **Keyboard Navigation** | All interactive elements focusable; logical tab order |
| **Focus Indicators** | Visible focus ring (Indigo outline) on all elements |
| **Screen Readers** | Semantic HTML; ARIA labels on icons/buttons |
| **Touch Targets** | Minimum 44x44px on mobile |
| **Motion** | Respect `prefers-reduced-motion` |
| **Form Errors** | Announced to screen readers; not color-only |

---

## 9. Implementation Guidance

### 9.1 Design Decisions Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Design System | shadcn/ui | Modern, customizable, accessible |
| Color Theme | Warm Indigo | AI-innovation feel, distinctive, trustworthy |
| SME Layout | Action-oriented + Card gallery + Wizard | Guided, reassuring, visual |
| Admin Layout | Sidebar + Data tables | Power user efficiency |
| Emotional Target | "System has my back" | Drives all UX decisions |

### 9.2 Priority Screens for Development

1. **Supplier Submission Wizard** — The core experience
2. **Assessment Results View** — The payoff moment
3. **SME Dashboard/Home** — First impression
4. **Supplier List (Card Gallery)** — Daily use
5. **Admin Risk Framework Config** — Setup requirement

---

## Appendix

### Related Documents

- Product Requirements: `docs/prd.md`
- Product Brief: `docs/product-brief-SME-Supply-Chain-Risk-Analysis-2025-11-28.md`

### Interactive Deliverables

- **Color Theme Visualizer**: [ux-color-themes.html](./ux-color-themes.html)
- **Design Direction Mockups**: [ux-design-directions.html](./ux-design-directions.html)

### Inspiration References

| App | Pattern Borrowed |
|-----|-----------------|
| TurboTax | Guided wizard, reassuring progress |
| Gusto | Friendly dashboards, action cards |
| Stripe | Data hierarchy, status indicators |

### Version History

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-28 | 1.0 | Initial UX Design Specification | Master |

---

_This UX Design Specification was created through collaborative design facilitation. All decisions were made with user input and are documented with rationale._
