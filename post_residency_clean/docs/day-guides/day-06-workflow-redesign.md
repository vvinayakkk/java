# Day 6 — Redesign a Production Workflow

**Unit:** Improving UX Through Workflow Redesign  
**Time:** ~2 hours  
**Log section:** Guided Practice 6

---

## Goal

Find work that blocks the user on `POST /api/books`, redesign so non-critical work happens after the response, implement one improvement, measure, and judge production readiness.

---

## Skip-video brief

### Sync vs async in request paths

| Must be sync (before response) | Often safe to defer |
|--------------------------------|---------------------|
| AuthZ / validation | Email / notifications |
| Persisting the source of truth | Search index updates |
| Returning IDs the client needs | Analytics, audit fan-out |
| Invariants that affect the response | Secondary cache warming |

### Event-driven idea (lightweight)

You do **not** need Kafka for this lab. Patterns that count:

1. **`@Async` method** after save
2. **ApplicationEvent** published after commit (`@TransactionalEventListener`)
3. Later: message broker for multi-service fan-out

Trade-offs: faster responses vs eventual consistency, harder failure handling, need retries/idempotency in real systems.

**Optional deep links:** [Fowler – Event-driven](https://martinfowler.com/articles/201701-event-driven.html) · [Spring Kafka ref](https://docs.spring.io/spring-kafka/reference/) (reference only)

---

## Built-in hook (Day 0)

`CatalogSyncService.syncAfterCreate(Book)` is called from `BookService.createBook` after save.

Properties:

```properties
app.catalog-sync.enabled=false
app.catalog-sync.delay-ms=0
```

---

## Steps

### Phase A — Map current lifecycle (20 min)

Enable blocking sync:

```properties
app.catalog-sync.enabled=true
app.catalog-sync.delay-ms=2000
```

Restart app.

Current flow:

```text
Client POST /api/books
  → BookController.createBook
    → BookService.createBook
      → validate ISBN / load author & category
      → bookRepository.save
      → CatalogSyncService.syncAfterCreate  // sleeps 2000ms when enabled
      → convertToDTO
  → HTTP 201
```

**User-blocking:** HTTP validation, DB write, **catalog sync sleep**, DTO mapping.

Measure create latency (5 runs) with a unique ISBN each time:

```bash
curl -o /dev/null -s -w '%{time_total}\n' -X POST http://localhost:8080/api/books \
  -H 'Content-Type: application/json' \
  -d '{"title":"Async Lab 1","isbn":"978-LAB-0001","price":12.5,"stockQuantity":3,"authorId":1,"categoryId":1}'
```

Expect ~2s+ per call.

### Phase B — Redesign (15 min)

Target flow:

```text
Client POST /api/books
  → validate + save (sync)
  → return 201 quickly
  → catalog sync runs asynchronously afterward
```

**Stays sync:** validation, ISBN check, persist book, return DTO.  
**Becomes async:** catalog sync delay/work.

### Phase C — Implement ONE improvement (40 min)

#### 1. Enable async

```java
@SpringBootApplication
@EnableAsync
public class BookstoreApplication { ... }
```

Optional config:

```java
@Configuration
@EnableAsync
public class AsyncConfig {
    @Bean
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor exec = new ThreadPoolTaskExecutor();
        exec.setCorePoolSize(2);
        exec.setMaxPoolSize(4);
        exec.setThreadNamePrefix("catalog-sync-");
        exec.initialize();
        return exec;
    }
}
```

#### 2. Make sync async

```java
@Async
public void syncAfterCreate(Book book) {
    // existing enabled/delay logic
}
```

**Important:** `@Async` on same-class self-invocation won’t work. Keep `@Async` on `CatalogSyncService` (separate bean) — already true.

#### 3. Re-measure

Create latency should drop toward pre-sleep levels while logs still show sync completing on `catalog-sync-*` threads.

### Phase D — Risks (15 min)

| Risk | Why it matters | Mitigation |
|------|----------------|------------|
| Sync fails after 201 | Catalog missing book | Retry + outbox later |
| Process crashes mid-async | Lost sync | Persistent queue |
| No backpressure | Thread pool saturation | Bounded queue + metrics |
| Client assumes catalog is searchable immediately | UX lie | Document eventual consistency |

Production recommendation: **Approve with conditions** (retries, metrics, not fire-and-forget `Thread.sleep` in prod).

---

## Alternatives considered (mention in log)

| Alternative | Why not today |
|-------------|----------------|
| Kafka | Overkill for single service lab |
| Keep sync | Hurts UX for non-critical work |
| Batch nightly sync | Higher lag than needed |

---

## What to record

Current vs redesigned diagrams, blocking activities, decisions, alternatives, before/after ms, risks, production recommendation.

---

## Cursor prompts

```text
Critique this async catalog sync for failure scenarios after HTTP 201.
What would an SRE ask before approving?
```

---

## Done checklist

- [ ] Workflow mapped
- [ ] Blocking vs deferred decided
- [ ] One improvement implemented
- [ ] Before/after measured
- [ ] Risks evaluated
- [ ] Practice log GP6 filled

**Take further:** Switch to `@TransactionalEventListener(phase = AFTER_COMMIT)` so sync doesn’t run if the transaction rolls back.

**Next:** [`day-07-incident-rca.md`](day-07-incident-rca.md)
