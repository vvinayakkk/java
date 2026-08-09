# Engineering Residency Pack Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce Day 0 bootstrap code plus the full docs pack so all 12 Guided Practices are completable without videos.

**Architecture:** Single H2 Spring Boot app (`spring-bookstore/`) for Units 1–6; markdown guides + one practice log + artefacts for Units 7–12.

**Tech Stack:** Java 17, Spring Boot 3.2, Spring Data JPA, H2, Markdown docs under `docs/`.

## Global Constraints

- Spec: `docs/superpowers/specs/2026-08-01-engineering-residency-design.md`
- Do not remove existing code smells before Day 2 exercises.
- Day 3 enhancement is pagination + sorting only.
- Day 6 default async approach is `@Async` / application events (not Kafka).
- Practice log uses shared section headings for all 12 days.
- Do not prefill learner judgment answers in `practice-log.md`.

---

### Task 1: Day 0 bootstrap code

**Files:**
- Create: `spring-bookstore/src/main/java/com/bookstore/config/DataLoader.java`
- Create: `spring-bookstore/src/main/java/com/bookstore/service/CatalogSyncService.java`
- Modify: `spring-bookstore/src/main/java/com/bookstore/service/BookService.java`
- Modify: `spring-bookstore/src/main/resources/application.properties`

**Interfaces:**
- Produces: `CatalogSyncService.syncAfterCreate(Book book)` — no-op when `app.catalog-sync.enabled=false`
- Produces: seed of ~5 authors, ~5 categories, ~90 books on startup when DB empty

- [x] **Step 1:** Add catalog-sync properties to `application.properties`
- [x] **Step 2:** Implement `CatalogSyncService` with configurable delay via `Thread.sleep`
- [x] **Step 3:** Call sync from `BookService.createBook` after save
- [x] **Step 4:** Implement `DataLoader` `CommandLineRunner` seeding data
- [x] **Step 5:** Commit note — only if user requests git commit

---

### Task 2: Core program docs

**Files:**
- Create: `docs/00-program-overview.md`
- Create: `docs/00-setup.md`
- Create: `docs/00-daily-template.md`
- Create: `docs/practice-log.md`

- [x] **Step 1:** Write overview mapping all 12 days to repo/artefacts
- [x] **Step 2:** Write setup (JDK 17, Maven, run, Swagger, Postman, seed verification)
- [x] **Step 3:** Write daily template matching practice-log shape
- [x] **Step 4:** Write practice-log with empty sections for GP 1–12

---

### Task 3: Day guides 01–06

**Files:**
- Create: `docs/day-01-reading-codebase.md` … `docs/day-06-workflow-redesign.md`

- [x] **Step 1:** Day 1 — trace `GET /api/books/{id}` with real class/method names
- [x] **Step 2:** Day 2 — smell investigation, no code changes
- [x] **Step 3:** Day 3 — pagination + sorting implementation guide with code sketches
- [x] **Step 4:** Day 4 — three-endpoint measurement protocol
- [x] **Step 5:** Day 5 — Spring Cache design + implementation guide
- [x] **Step 6:** Day 6 — enable sync delay, redesign async, measure

---

### Task 4: Artefacts + Day guides 07–12

**Files:**
- Create: `docs/artefacts/day-07-incident-context.md` … `day-12-design-proposal.md`
- Create: `docs/day-07-incident-rca.md` … `docs/day-12-architecture-review.md`

- [x] **Step 1:** Author artefacts from `ask.md` (+ Day 12 design proposal)
- [x] **Step 2:** Write Days 7–12 guides with analysis method + record fields
- [x] **Step 3:** Spec coverage check — every unit in ask.md has a guide + log section

---

### Task 5: Verification

- [x] **Step 1:** Confirm Day 0 files exist and properties present
- [x] **Step 2:** Confirm all `docs/day-*.md` and artefacts exist
- [x] **Step 3:** Grep practice-log for 12 Guided Practice headings
- [x] **Step 4:** Update spec status to Implemented
