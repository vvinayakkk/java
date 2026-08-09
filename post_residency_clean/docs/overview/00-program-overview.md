# Engineering Residency — Program Overview

**Duration:** 12 working days · **Daily time:** ~1.5–2 hours  
**Primary app:** `spring-bookstore/` ([GitHub](https://github.com/shafakyildiz/spring-bookstore))  
**Practice log:** [`practice-log.md`](practice-log.md) (use this instead of a Google Doc)  
**Source brief:** [`ask.md`](../ask.md)  
**Design spec:** [`superpowers/specs/2026-08-01-engineering-residency-design.md`](superpowers/specs/2026-08-01-engineering-residency-design.md)

---

## How to use this pack

You already know Java/Spring Boot. **Skip the program videos.** Each `day-XX-*.md` file distills the mandatory concepts and gives exact repo steps.

**Current status:** All code, unit tests, live performance measurements, and reports for Days 1 through 12 are COMPLETE and verified.  
**Execution:** All steps from [`READY-FOR-JAVA.md`](READY-FOR-JAVA.md) are finished.

1. Complete [`00-setup.md`](00-setup.md) once when JDK is installed.
2. Use [`practice-log.md`](practice-log.md) as the submission log (all timing data and analysis recorded).
3. Same section shape every day ([`00-daily-template.md`](00-daily-template.md)).

---

## 12-day map

| Day | Guide | Type | Touchpoint |
|-----|--------|------|------------|
| 0 | [`00-setup.md`](00-setup.md) | Bootstrap | Seed data + catalog-sync hook |
| 1 | [`day-01-reading-codebase.md`](day-01-reading-codebase.md) | Read | Trace `GET /api/books/{id}` |
| 2 | [`day-02-investigating-code.md`](day-02-investigating-code.md) | Investigate | One smell, **no code change** |
| 3 | [`day-03-implementing-feature.md`](day-03-implementing-feature.md) | Build | Pagination + sorting on `GET /api/books` |
| 4 | [`day-04-measuring-performance.md`](day-04-measuring-performance.md) | Measure | 3 endpoints × 5 runs |
| 5 | [`day-05-caching-strategy.md`](day-05-caching-strategy.md) | Build | Spring Cache on Day-4 slowest |
| 6 | [`day-06-workflow-redesign.md`](day-06-workflow-redesign.md) | Build | Sync catalog sync → async |
| 7 | [`day-07-incident-rca.md`](day-07-incident-rca.md) | Report | [`artefacts/day-07-incident-context.md`](artefacts/day-07-incident-context.md) |
| 8 | [`day-08-readiness-review.md`](day-08-readiness-review.md) | Report | [`artefacts/day-08-release-evidence.md`](artefacts/day-08-release-evidence.md) |
| 9 | [`day-09-sprint-prioritisation.md`](day-09-sprint-prioritisation.md) | Report | [`artefacts/day-09-backlog.md`](artefacts/day-09-backlog.md) |
| 10 | [`day-10-pr-review.md`](day-10-pr-review.md) | Report | [`artefacts/day-10-pr-2481.md`](artefacts/day-10-pr-2481.md) |
| 11 | [`day-11-system-diagnosis.md`](day-11-system-diagnosis.md) | Report | [`artefacts/day-11-checkout-artefacts.md`](artefacts/day-11-checkout-artefacts.md) |
| 12 | [`day-12-architecture-review.md`](day-12-architecture-review.md) | Report | [`artefacts/day-12-design-proposal.md`](artefacts/day-12-design-proposal.md) |

---

## Repo mental model

```text
Client (Postman)
  → controller  (HTTP only)
    → service   (business rules)
      → repository (Spring Data JPA)
        → entity → H2
```

Key packages under `spring-bookstore/src/main/java/com/bookstore/`:

| Package | Role |
|---------|------|
| `controller` | REST endpoints |
| `service` | Business logic (+ `CatalogSyncService` for Day 6) |
| `repository` | Data access |
| `entity` | JPA models |
| `dto` | API payloads |
| `exception` | Global error handling |
| `config` | OpenAPI + `DataLoader` seed |

---

## Rules that keep days consistent

- **Same repo** for Days 1–6 (and as production context for 7–12).
- **Smallest safe change** on build days (3, 5, 6).
- **Measure before optimize** (Day 4 before Day 5).
- **Evidence before opinion** on report days (7–12).
- **Validate AI** against code/artefacts before accepting suggestions.

---

## Suggested calendar

| Block | Days | Theme |
|-------|------|--------|
| Week 1 | 0–5 | Understand → improve → measure → cache |
| Week 2 | 6–11 | Async redesign → ops judgment |
| Capstone | 12 | Architecture review |

---

## Done definition for the whole program

- [x] App runs with seeded books
- [x] Practice log has completed sections for GP 1–12
- [x] Day 3/5/6 code changes exist and are verified live
- [x] Days 7–12 reports include evidence, not vibes
