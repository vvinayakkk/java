# Guided Practice 7 – Incident Investigation (RCA)

**Program:** Engineering Residency – From Training to Production Thinking  
**Date:** 2026-08-01  
**Engineer:** Vinayak  
**Artefact Reference:** [`docs/artefacts/day-07-incident-context.md`](../artefacts/day-07-incident-context.md)  
**Time Spent:** ~90 minutes (Incident Evidence Gathering & Root Cause Analysis)

---

## 🏢 Engineering Scenario & Incident Overview
> "24 hours following the deployment of local Caffeine caching and `@Async` catalog synchronization across a dual-instance production cluster (Instance A and Instance B), customer support complaints surged. Customers report seeing outdated book prices after price updates, while admin users experience periodic `500 Internal Server Error` failures during book creation under peak load."

---

## ⏱️ Incident Investigation Timeline

| Time Marker | Event / Symptom | Evidence Collected |
|---|---|---|
| **D-1 16:40** | Deployment of local Caffeine cache & `@Async` catalog sync to dual-instance cluster. | Release tag `v1.4.0` deployed to Instance A and Instance B. |
| **D-0 09:10** | First customer complaints: updated book prices reverted on page refresh. | Support ticket #4029: Price updated to $29.99, but checkout showed $39.99. |
| **D-0 10:15** | Cache hit rate variance detected between cluster nodes. | Metrics dashboard: Instance A cache hit 88%, Instance B cache hit 41%. |
| **D-0 11:20** | `RejectedExecutionException` logged during book creation peak. | Log snippet: `ThreadPoolExecutor rejected task on catalog-sync pool`. Create success dropped from 99.9% to 97.2%. |
| **D-0 12:00** | Incident Investigation Initiated. | Tech Lead instructs team to perform full evidence-based RCA before proposing code fixes. |

---

## 🔍 Evidence vs Hypotheses Evaluation Matrix

### Evaluated Hypotheses:

| Hypothesis # | Proposed Failure Mechanism | Evidence Supporting | Evidence Contradicting | Confidence Rating |
|---|---|---|---|---|
| **H1 (Primary)** | **In-Process Cache Incoherence across Cluster Nodes:** Updating a book on Instance A invalidates Instance A's local Caffeine cache, but leaves Instance B's local cache intact with stale price data. | Logs show `PUT /api/books/2` evicting cache on Instance A, followed by `GET /api/books/2` on Instance B returning HTTP 200 with cache **HIT** and old price ($39.99). | None. Fully supported by cluster trace logs. | **HIGH (Root Cause)** |
| **H2 (Contributing)** | **Async Thread Pool Saturation:** Heavy create load saturates `taskExecutor` bounded queue (size 25), triggering task rejection that leaks to API callers as HTTP 500 errors. | Log excerpts show `RejectedExecutionException` on `catalog-sync-` thread pool during peak traffic. | None. Fully supported by error trace logs. | **HIGH (Contributing Cause)** |
| **H3** | **Database Performance Degradation:** Database CPU/IOPS saturation causing read/write timeouts. | None. | DB CPU metrics remained flat at **22% to 25%** throughout the incident window. | **LOW (Rejected)** |
| **H4** | **Sync Hook still executing synchronously:** Sync logic blocking HTTP threads. | None. | Thread logs clearly show execution on `catalog-sync-*` worker threads. | **LOW (Rejected)** |

---

## 🎯 Root Cause Analysis (RCA) Summary

### 1. Primary Root Cause (Stale Read Anomalies):
The application utilizes an in-process local Caffeine cache (`spring.cache.type=caffeine`) deployed across a multi-instance load-balanced cluster without a cross-instance cache invalidation mechanism (pub-sub bus or distributed cache). Updating data on Node A clears Node A's memory, but leaves Node B serving stale cached data to clients whose requests land on Node B.

### 2. Secondary Contributing Cause (Write Path Errors):
The `@Async` thread pool (`taskExecutor`) was configured with a fixed max pool size of 10 and a queue capacity of 25 without a fail-safe fallback policy. When write volume exceeded processing capacity, rejected execution exceptions broke the HTTP `POST /api/books` request execution.

---

## 💡 Evidence-Based Remediation & Prevention Plan

### Immediate Remediation:
1. **Cache Flush / Temporary Bypass:** Flush Caffeine cache across all instances and enable sticky session routing (or temporarily disable caching via feature toggle) to prevent stale price displays during checkout.
2. **Fail-Open Async Error Handling:** Wrap `CatalogSyncService` invocation in a `try-catch` block inside `BookService` to prevent background pool rejections from failing the primary HTTP 201 response.

### Long-Term Architectural Fix:
1. **Migrate to Distributed Redis Cache:** Replace local Caffeine cache with Redis (`spring-boot-starter-data-redis`) so all cluster nodes share a single source of truth for cached records.
2. **Transactional Outbox for Catalog Sync:** Replace Spring `@Async` with a persistent Transactional Outbox pattern or Message Queue (Kafka/RabbitMQ) to ensure guaranteed event processing and decouple background tasks from HTTP thread pool limits.

---

## ✅ Self-Check & Completion Sign-Off
- [x] Distinguished symptoms (stale prices, 500 errors) from root causes (cache incoherence, thread saturation).
- [x] Evaluated multiple hypotheses against concrete metrics and log evidence before proposing remedies.
- [x] Delivered a complete Incident Investigation Report suitable for post-incident review.