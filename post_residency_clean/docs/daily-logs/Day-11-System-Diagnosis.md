# Guided Practice 11 – System Diagnosis

**Program:** Engineering Residency – From Training to Production Thinking  
**Date:** 2026-08-01  
**Engineer:** Vinayak  
**Artefact Reference:** [`docs/artefacts/day-11-checkout-artefacts.md`](../artefacts/day-11-checkout-artefacts.md)  
**Time Spent:** ~80 minutes (System Diagnosis & Incident Signal Analysis)

---

## 🏢 Engineering Scenario & Investigation Brief
> "Monday 11:53 AM - Customer Support reports: '14 complaints received in the last 20 minutes. Some customers cannot complete checkout; others succeed after refreshing.' Your Tech Lead messages: 'Please perform the initial investigation. Don't fix anything yet. Determine what signals, noise, and red herrings exist, rank potential hypotheses, and recommend the single next engineering action.'"

---

## ⏱️ Incident Timeline Reconstruction

```text
08:30 — Recommendation Service Deployed (No immediate error rate changes observed)
09:40 — Payment Service Deployed (No immediate error rate changes observed)
11:30 — Feature Flag Enabled (Triggers new execution path)
11:40 — Error rate begins rising (0.4% -> 1.2%)
11:42 — Customer checkout error complaints begin surfacing in logs
11:45 — Error rate PEAKS at 5.1%, p95 latency spikes to 490ms, Cache Hit rate drops to 62%
11:50 — Error rate decays to 2.6%, Cache Hit rate recovers to 74%
11:55 — Error rate settles to 0.4%, Cache Hit rate recovers to 91%
```

---

## 📊 Signals vs. Noise vs. Red Herrings Matrix

| Item / Metric | Classification | Engineering Rationale |
|---|---|---|
| **11:30 Feature Flag Toggle vs 11:42 Errors** | **PRIMARY SIGNAL** | Strong chronological alignment. Errors began exactly 12 minutes after the 11:30 Feature Flag activation. |
| **Cache Hit Rate Drop (91% -> 62% -> 91%)** | **SECONDARY SIGNAL** | Cache hit rate co-moved inversely with the error rate peak at 11:45, indicating cache stampedes or invalidation loops. |
| **Payment Timeout & Retry Success Logs** | **SIGNAL** | Log excerpts show repeated `Payment timeout. Retry initiated` followed by `Retry succeeded`, explaining intermittent user behavior. |
| **Database CPU at 32%** | **RED HERRING** | DB Engineer claimed healthy DB based on 32% CPU, but low CPU does not rule out application-level lock contention, thread pool starvation, or bad query plans. |
| **"Most complaints are from Android users"** | **POSSIBLE NOISE / CORRELATION** | PM assumption. May simply reflect Android market share majority rather than an Android-specific app bug. |
| **Routine Authentication Success Logs** | **NOISE** | Baseline operational traffic logs unrelated to checkout failure paths. |

---

## 🔬 Ranked Hypotheses Matrix

| Rank | Hypothesis Description | Confidence | Evidence Supporting | Evidence Required to Prove/Disprove |
|---|---|---|---|---|
| **H1** | **Feature Flag Interaction Bug:** The 11:30 feature flag activated a new checkout/payment path that causes cache stampedes and intermittent payment service timeouts. | **HIGH** | Error onset (11:42) aligns directly with 11:30 flag enable. Logs show timeouts and cache hit drops. | Pull feature flag evaluation logs; compare error rate of `Flag=ON` users vs `Flag=OFF` users. |
| **H2** | **Payment Service Retries / Connection Pool Saturation:** 09:40 Payment Service deploy contained a latent connection timeout bug exposed under peak traffic. | **MEDIUM** | Log excerpts show `Payment timeout. Retry initiated.` | Trace connection pool metrics (`HikariPool`) and payment downstream latency. |
| **H3** | **Cache Stampede / Cache Eviction Loop:** Heavy cache misses (62% hit rate) flooded backend services, cascading into downstream payment timeouts. | **MEDIUM** | Cache hit rate dropped from 91% down to 62% at peak error window (11:45). | Check cache key TTLs and eviction rate metrics during 11:40-11:50. |

---

## 🎯 Recommended Next Engineering Action

### Single Recommended Next Action:
**Inspect Feature Flag Rollout Configuration (User Cohort %, Target Rules) and Compare Error Rates Between `Flag=ON` and `Flag=OFF` Users; Prepare Immediate Flag Rollback as Mitigation.**

### Rationale:
The highest-leverage engineering action is confirming or disproving the 11:30 feature flag correlation before committing engineering resources to refactoring Payment Service code. Toggling the feature flag OFF provides instant risk mitigation if H1 is confirmed.

---

## ✅ Self-Check & Completion Sign-Off
- [x] Reconstructed chronological timeline from multi-source telemetry artefacts.
- [x] Separated verified facts from assumptions, signals from noise, and identified red herrings.
- [x] Ranked 3 distinct hypotheses with confidence ratings and specified required evidence.
- [x] Recommended a data-driven next engineering action without prematurely declaring unproven root cause.