# Engineering Residency (12-Day Post-Bootcamp) — Design Spec

**Date:** 2026-08-01  
**Status:** Approved and implemented (docs pack + Day 0 bootstrap)  
**Source brief:** `ask.md`  
**Primary codebase:** `spring-bookstore/` (clone of https://github.com/shafakyildiz/spring-bookstore)

---

## 1. Purpose

Complete the 12 Guided Practices of the Engineering Residency program without watching videos. Deliverables are:

1. A runnable Spring Boot app used consistently for Units 1–6 (and as production context for 7–12).
2. Deep day-by-day markdown guides that replace video learning.
3. One continuous practice log matching program “How to Record” fields.
4. Artefacts for Units 7–12 where the brief assumes materials that are not shipped.

Success = every unit’s mandatory exercise is completable in ~2 hours with evidence recorded in a consistent format.

---

## 2. Repo choice

### Selected

| Item | Value |
|------|--------|
| Repo | `shafakyildiz/spring-bookstore` |
| Local path | `spring-bookstore/` |
| Stack | Java 17, Spring Boot 3.2, Spring Data JPA, H2, Validation, SpringDoc |
| Architecture | Package-by-layer: `controller`, `service`, `repository`, `entity`, `dto`, `exception` |

### Why this repo

- Clear Controller → Service → Repository → Entity layers (Unit 1).
- Zero external DB (H2) — Postman-friendly for Units 2–6.
- Many comparable GET endpoints for performance comparison (Unit 4) and caching (Unit 5).
- Existing maintainability issues useful for Unit 2 (field injection, EAGER fetches, manual DTO mapping, class-level `@Transactional`).
- Room for a small safe enhancement (pagination/sorting) without redoing existing validation (Unit 3).
- Units 7–12 are scenario/report exercises; this app is the narrative “production service.”

### Rejected alternatives

| Repo | Why not |
|------|---------|
| `RameshMF/springboot-blog-rest-api` | MySQL + JWT friction; pagination/validation already complete (weaker Unit 3). |
| `spring-projects/spring-petclinic` | Primarily MVC/Thymeleaf, not Postman REST-first. |
| Build from scratch | User chose a public repo. |

### Known gaps (must close)

1. **No seed data** — empty H2 on boot. Day 0 adds a seeder (~5 authors, ~5 categories, ~80–100 books).
2. **No user-blocking side work** for Unit 6. Day 0 adds a feature-flagged `CatalogSyncService` hook on `createBook`; Unit 6 enables sync delay then redesigns to async.
3. **Unit 12 artefacts missing** from brief — we author a fake design proposal under `docs/artefacts/`.

---

## 3. Workspace layout

```text
post_bootcamp/
├── ask.md
├── spring-bookstore/                 # cloned app + Day 0 patches only
└── docs/
    ├── 00-program-overview.md
    ├── 00-setup.md
    ├── 00-daily-template.md
    ├── practice-log.md               # single continuous log (Google Doc substitute)
    ├── day-01-reading-codebase.md
    ├── day-02-investigating-code.md
    ├── day-03-implementing-feature.md
    ├── day-04-measuring-performance.md
    ├── day-05-caching-strategy.md
    ├── day-06-workflow-redesign.md
    ├── day-07-incident-rca.md
    ├── day-08-readiness-review.md
    ├── day-09-sprint-prioritisation.md
    ├── day-10-pr-review.md
    ├── day-11-system-diagnosis.md
    ├── day-12-architecture-review.md
    ├── artefacts/
    │   ├── day-07-incident-context.md
    │   ├── day-08-release-evidence.md
    │   ├── day-09-backlog.md
    │   ├── day-10-pr-2481.md
    │   ├── day-11-checkout-artefacts.md
    │   └── day-12-design-proposal.md
    └── superpowers/
        ├── specs/2026-08-01-engineering-residency-design.md
        └── plans/                    # implementation plan for producing the pack
```

---

## 4. Daily workflow (consistency rules)

Every working day follows the same rhythm:

1. Open `docs/day-XX-*.md`.
2. Read the skip-video brief (mandatory concepts distilled).
3. Execute hands-on against `spring-bookstore/` or `docs/artefacts/`.
4. Fill the matching section in `docs/practice-log.md`.
5. Optionally run listed Cursor prompts; validate against code/evidence.
6. Tick the day’s done checklist.

### Day guide mandatory blocks

| Block | Purpose |
|--------|---------|
| Goal + skip-video brief | Concepts without watching program videos |
| Repo / artefact touchpoints | Exact classes, endpoints, or artefact files |
| Steps | Numbered, timeboxed |
| What to record | 1:1 with program “How to Record” |
| Cursor prompts | Optional AI companion |
| Done checklist | From `ask.md` self-check |
| Take further | Optional stretch |

### Practice log section shape (all 12 days)

```markdown
## Guided Practice N – <Title>
**Date:**
**Repo:** https://github.com/shafakyildiz/spring-bookstore (local: `spring-bookstore/`)

### Context
### Evidence / Work
### Engineering Judgment
### Outcome / Recommendation
### Self-check
- [ ] …
```

Days 1–6: Evidence = code paths, Postman timings, before/after.  
Days 7–12: Evidence = hypotheses, risk registers, review comments — same four headings.

---

## 5. Unit map (end-to-end)

### Day 0 — Bootstrap (prerequisite)

**Code changes (minimal):**

| File | Responsibility |
|------|----------------|
| `…/config/DataLoader.java` | Seed authors, categories, books on startup |
| `…/service/CatalogSyncService.java` | Feature-flagged sync hook (noop by default) |
| `…/service/BookService.java` | Call catalog sync after successful `createBook` |
| `application.properties` | `app.catalog-sync.enabled=false`, `app.catalog-sync.delay-ms=0` |

**Docs:** `docs/00-setup.md` (JDK 17, Maven, run, Swagger, Postman).

**Constraint:** Do not refactor smells away before Day 2.

---

### Day 1 — Reading an Existing Codebase

| Item | Spec |
|------|------|
| Trace endpoint | `GET /api/books/{id}` |
| Flow | `BookController.getBookById` → `BookService.getBookById` → `BookRepository.findById` → H2 `books` (+ EAGER author/category) |
| Business logic location | `BookService` (not found handling; ISBN uniqueness on create; author/category resolution) |
| Record | Repo link, package/file names, endpoint, request flow with real method names, 1–2 sentences on business logic |

---

### Day 2 — Investigating & Improving Existing Code

| Item | Spec |
|------|------|
| Same project | Yes |
| Execute | Chosen endpoint via Postman |
| Code change | **None** |
| Suggested smell (pick one) | EAGER `@ManyToOne` on `Book`; field `@Autowired`; duplicated manual DTO mapping; class-level `@Transactional` on read paths |
| Record | Repo, endpoint, flow, smell, why it matters, recommended improvement, engineering impact |

---

### Day 3 — Implementing a Small Feature

| Item | Spec |
|------|------|
| Enhancement | **Pagination + sorting** on `GET /api/books` (validation already exists — do not redo) |
| Likely files | `BookController`, `BookService`, `BookRepository` (use `Pageable` / `Page`) |
| Verify | Postman: new query params; existing `GET /api/books/{id}` still works |
| Record | Feature, classes modified, why, testing, issues, trade-offs, one future improvement |
| Discipline | Smallest safe change; YAGNI |

---

### Day 4 — Measuring API Performance

| Item | Spec |
|------|------|
| Endpoints (default trio) | `GET /api/books/{id}`, `GET /api/books`, `GET /api/books/search?title=` |
| Method | 5 runs each; record individual + average; identify slowest |
| Code change | **None** |
| Record | Times table, slowest, possible bottleneck, evidence, next investigation |
| Note | Warm vs cold JVM: discard first run or label it |

---

### Day 5 — Caching Strategy

| Item | Spec |
|------|------|
| Target | Slowest from Day 4 (likely `GET /api/books` or search) |
| Approach | Spring Cache abstraction; local cache (`ConcurrentMapCacheManager` or Caffeine) justified vs Redis for single-instance demo |
| Design | Cache name, key, TTL (or eviction), invalidation on create/update/delete |
| Measure | Before/after averages |
| Record | Decision, design, times, trade-offs, production recommendation |

---

### Day 6 — Workflow Redesign

| Item | Spec |
|------|------|
| Problem framing | `POST /api/books` blocks on catalog sync when `app.catalog-sync.enabled=true` and delay > 0 |
| Redesign | Keep create transactional; move sync to `@Async` or application event after commit |
| Implement | One improvement; measure create latency before/after |
| Record | Current vs redesigned diagrams, blocking work, decisions, alternatives, risks, production recommendation |

---

### Day 7 — Incident RCA

| Item | Spec |
|------|------|
| Code change | **None** (investigate only) |
| Narrative | Complaints after deploy of caching + async catalog sync |
| Artefact | `docs/artefacts/day-07-incident-context.md` (logs/metrics tied to bookstore) |
| Deliverable | Incident Investigation Report in practice log |

---

### Day 8 — Engineering Readiness Review

| Item | Spec |
|------|------|
| Evidence | Exact pass/fail/warning list from `ask.md` → `docs/artefacts/day-08-release-evidence.md` |
| Decision | Approve / Approve with Conditions / Reject |
| Deliverable | Engineering Readiness Review |

---

### Day 9 — Sprint Prioritisation

| Item | Spec |
|------|------|
| Capacity | 16 story points |
| Backlog | Exact 10 items from `ask.md` → `docs/artefacts/day-09-backlog.md` |
| Include | Mid-sprint incident on Day 4 of sprint — revise plan |
| Deliverable | Sprint Prioritisation Proposal |

---

### Day 10 — PR Review

| Item | Spec |
|------|------|
| PR | #2481 “Add request-level caching to Product Search” (program scenario; map mentally to bookstore search) |
| Artefact | Snippets A–G + reviewer comments → `docs/artefacts/day-10-pr-2481.md` |
| Severity | Blocker / Should Fix / Nice to Have / Not an Issue per snippet |
| Deliverable | Pull Request Review Report |

---

### Day 11 — Unfamiliar System Diagnosis

| Item | Spec |
|------|------|
| Artefact | Slack, dashboard, deploy timeline, logs, service flow from `ask.md` → `docs/artefacts/day-11-checkout-artefacts.md` |
| Rule | Do **not** guess root cause; recommend best next action |
| Deliverable | System Diagnosis Report |

---

### Day 12 — Architecture Review

| Item | Spec |
|------|------|
| Artefact | Authored design proposal for bookstore “Order + Notify” → `docs/artefacts/day-12-design-proposal.md` |
| Rule | Do **not** redesign; decide Approve / Approve with Required Changes / Reject Pending Rework |
| Deliverable | Architecture Review Recommendation |

---

## 6. Skip-video learning policy

Day guides must distill mandatory reading topics into short engineering notes (definitions, when to use, red flags). External URLs from `ask.md` remain listed as optional deep links, not blockers.

Mandatory concept coverage by day:

| Day | Concepts to distill |
|-----|---------------------|
| 1 | Layered architecture; request lifecycle |
| 2 | Code smells; maintainability |
| 3 | Reviewable changes; YAGNI |
| 4 | Measure before optimize |
| 5 | Spring Cache; cache-aside; TTL/invalidation |
| 6 | Sync vs async; event-driven trade-offs |
| 7 | Incident response; symptoms vs root cause |
| 8 | Release engineering; readiness vs feature-complete |
| 9 | Toil; error budgets; prioritisation trade-offs |
| 10 | Code review standards; blockers vs nits |
| 11 | Troubleshooting methodology; signals vs noise |
| 12 | Design docs; architectural trade-offs |

---

## 7. Day 0 implementation detail

### Seed data targets

- 5 authors with biographies
- 5 categories
- 80–100 books with varied titles, prices, stock (including some `stockQuantity = 0` for `/available` contrast), ISBNs unique

### Catalog sync hook

```properties
app.catalog-sync.enabled=false
app.catalog-sync.delay-ms=0
```

- When disabled: no-op (Days 1–5).
- Day 6 enables + sets delay (e.g. 2000ms) to create measurable blocking, then moves work off the request thread.

---

## 8. Out of scope

- Watching program videos
- Switching primary repo mid-program
- Kafka/microservices for Unit 6 (default: `@Async` / application events)
- Prefilling practice-log answers that replace the learner’s judgment
- Unrelated refactors of `spring-bookstore` beyond Day 0 bootstrap and day-specific exercise changes

---

## 9. Verification

| Check | How |
|-------|-----|
| App boots with seed | `mvn spring-boot:run`; `GET /api/books` returns many rows |
| Day 1 traceable | Named methods exist as documented |
| Day 3 feature | Query params work; id endpoint unchanged |
| Day 4 measurable | Three endpoints return 200 with data |
| Day 5 cache | Before/after times recordable |
| Day 6 async | Create latency drops with sync moved off-thread |
| Days 7–12 | Artefact files present; practice-log sections have required headings |
| Consistency | All day guides share the mandatory blocks; practice log uses shared section shape |

---

## 10. Implementation sequence (after this spec is approved)

1. Writing-plans: task list to produce docs + Day 0 code.
2. Execute: Day 0 code, overview/setup/template, practice-log skeleton, days 01–12, artefacts.
3. Spot-check one path (Day 1 + Day 4 endpoints) against real class names.

---

## Spec self-review (2026-08-01)

| Check | Result |
|-------|--------|
| Placeholders | None remaining (Unit 12 artefact explicitly authored) |
| Consistency | Day 3 = pagination/sorting; Day 5 target = Day 4 slowest; Day 6 uses Day 0 hook |
| Scope | Single program pack + one app; not a platform rewrite |
| Ambiguity | Day 3 enhancement fixed to pagination+sorting; Day 6 default async = `@Async`/events not Kafka |
