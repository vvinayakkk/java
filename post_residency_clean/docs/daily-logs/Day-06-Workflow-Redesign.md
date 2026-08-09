# Guided Practice 6 – Workflow Redesign

**Program:** Engineering Residency – From Training to Production Thinking  
**Date:** 2026-08-01  
**Engineer:** Vinayak  
**Repository:** [spring-bookstore](https://github.com/shafakyildiz/spring-bookstore) (Local Path: `spring-bookstore/`)  
**Time Spent:** ~60 minutes (Workflow Lifecycle Mapping, `@Async` Implementation, A/B Performance Testing)

---

## 🏢 Engineering Scenario & Objective
> "Users creating new books via `POST /api/books` report severe latency delays (~2+ seconds per request). Investigation reveals that after saving the book entity to the database, the server synchronously executes a downstream catalog search-index synchronization task (`CatalogSyncService`) directly on the HTTP request thread before returning a response to the user. You must redesign the workflow to decouple non-blocking tasks using asynchronous processing while preserving data consistency."

**Key Learning Goals:**
1. Map an existing request lifecycle and separate user-blocking tasks from deferrable work.
2. Redesign the workflow using asynchronous execution (`@Async`).
3. Configure dedicated bounded thread pools (`AsyncConfig.java`) to protect system memory.
4. Perform A/B benchmarking comparing synchronous blocking latency against asynchronous non-blocking latency.

---

## 🔄 Workflow Mapping & Decoupling Analysis

### 1. Current Workflow (Blocking Synchronous Path):
```text
Client POST /api/books
  └─► BookController.createBook()
        └─► BookService.createBook()
              ├─► Validate input & check ISBN uniqueness (User Blocking)
              ├─► Save to DB via BookRepository (User Blocking)
              └─► CatalogSyncService.syncAfterCreate() (User Blocking — Thread.sleep 2000ms delay)
                    └─► Return HTTP 201 Created to Client (Delayed by 2000ms+)
```

### 2. Activity Classification:
- **User-Blocking (Must complete before HTTP 201):** Input validation, database constraint checks (ISBN uniqueness), entity persistence (`bookRepository.save()`), database ID assignment.
- **Deferrable / Non-Blocking (Can safely happen in background):** Downstream catalog search index update, audit logging, email/webhook notifications.

### 3. Redesigned Workflow (Asynchronous Path):
```text
Client POST /api/books
  └─► BookController.createBook()
        └─► BookService.createBook()
              ├─► Validate input & check ISBN uniqueness (User Blocking)
              ├─► Save to DB via BookRepository (User Blocking)
              ├─► Return HTTP 201 Created IMMEDIATELY to Client (~35ms response)
              └─► CatalogSyncService.syncAfterCreateAsync() (@Async on 'taskExecutor' pool)
                    └─► Background thread 'catalog-sync-1' handles 2000ms sync out-of-band
```

---

## 💻 Asynchronous Implementation Details

### 1. Bounded Thread Pool Configuration (`AsyncConfig.java`):
```java
@Configuration
@EnableAsync
public class AsyncConfig {
    @Bean(name = "taskExecutor")
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(5);
        executor.setMaxPoolSize(10);
        executor.setQueueCapacity(25);
        executor.setThreadNamePrefix("catalog-sync-");
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        executor.initialize();
        return executor;
    }
}
```

### 2. Async Service Method (`CatalogSyncService.java`):
```java
@Service
public class CatalogSyncService {
    private static final Logger log = LoggerFactory.getLogger(CatalogSyncService.class);

    @Async("taskExecutor")
    public void syncAfterCreateAsync(Book book) {
        log.info("Starting catalog sync for book id={} on thread={}", 
                 book.getId(), Thread.currentThread().getName());
        doSync(book);
    }
}
```

---

## 📊 Empirical A/B Benchmark Results

Tested `POST /api/books` latency under both configurations:

| Mode / Configuration | Properties Setting | Measured `POST /api/books` Latency | Client Experience & Behavior |
|---|---|---|---|
| **Baseline (Blocking Sync)** | `app.catalog-sync.enabled=true`<br>`app.catalog-sync.delay-ms=2000`<br>`app.catalog-sync.async=false` | **~2,035 ms** | HTTP thread blocked waiting 2+ seconds for downstream sync to sleep and complete. High latency. |
| **Redesigned (`@Async` Path)** | `app.catalog-sync.enabled=true`<br>`app.catalog-sync.delay-ms=2000`<br>`app.catalog-sync.async=true` | **35 ms** | HTTP 201 Created returned immediately. Server logs show `catalog-sync-1` thread executing sync in background. |

### Performance Impact:
- **Client Latency Reduction:** **98.3% speedup** (reduced client wait time from 2035 ms to 35 ms).
- **Throughput:** Web server worker threads are freed immediately to serve concurrent incoming HTTP requests.

---

## 💡 Risks, Failure Modes & Production Recommendation

### Risks & Failure Scenarios Identified:
1. **Async Failure After HTTP 201:** If the background thread crashes during catalog sync, the HTTP client has already received `201 Created`, leaving the search index out of sync with the database.
2. **Thread Pool Saturation:** Under heavy burst traffic, if the queue fills beyond 25 tasks, `CallerRunsPolicy` falls back to running tasks on the HTTP thread, temporarily reintroducing latency spikes.

### Production Recommendation: **Approve with Conditions**
- **Condition 1:** Replace `@Async` with a Transactional Outbox pattern or messaging broker (e.g., RabbitMQ / Kafka) for production environments to guarantee at-least-once delivery.
- **Condition 2:** Add dead-letter queues (DLQ) and retry policies for downstream sync failures.

---

## ✅ Self-Check & Completion Sign-Off
- [x] Request lifecycle mapped and user-blocking tasks separated from deferrable work.
- [x] Workflow redesigned using Spring `@Async` with dedicated bounded thread pool (`taskExecutor`).
- [x] Empirical before/after A/B measurements recorded live (2035 ms down to 35 ms).
- [x] Production risks, failure modes, and architectural recommendations documented.