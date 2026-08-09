# Day 7 — Investigate a Production Incident (RCA)

**Time:** ~2 hours · **Code changes:** None  
**Artefact:** [`artefacts/day-07-incident-context.md`](artefacts/day-07-incident-context.md)  
**Log:** Guided Practice 7

---

## Goal

Investigate with structure: symptoms ≠ root cause, ≥3 hypotheses, evidence-based remediation recommendation.

---

## Skip-video brief

### Incident response habits

1. **Declare & communicate** — what’s broken, impact, who’s investigating
2. **Stabilize** before perfect root cause (today you’re asked to investigate, not patch)
3. **Timeline** from symptoms, deploys, and metric breaks
4. **Hypotheses** that are falsifiable
5. **Remediation** with validation steps and risks

### Symptoms vs causes

| Symptom | Possible deeper cause |
|---------|----------------------|
| Slow reads | Cache asymmetry, N+1, noisy neighbor |
| Stale price | Local cache not evicted on all instances |
| Create failures | Async executor rejection surfaced to client |

**Optional deep links:** [SRE Workbook – Incident Response](https://sre.google/workbook/incident-response/) · [SRE Book – Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/)

---

## Method (follow in order)

### 1. Understand impact (10 min)

Who hurts? Reads? Writes? Both? Since when?

### 2. Gather evidence (25 min)

From the artefact: timeline, metrics, logs, deploy diff (cache + async). Map to bookstore components you built on Days 5–6.

### 3. Hypotheses (≥3) (20 min)

Example seeds (replace/refine with your reasoning):

| # | Hypothesis | Supports | Contradicts |
|---|------------|----------|-------------|
| H1 | Per-instance local cache → stale reads after update on other instance | Log price mismatch A vs B; hit% skew | DB CPU still low |
| H2 | Async catalog pool saturation → create errors | RejectedExecutionException; success rate drop | Unrelated to stale GET |
| H3 | DB regression from deploy | — | DB CPU only +3% |
| H4 | Delay still on request thread somehow | — | Logs show async thread names |

Rank by likelihood after scoring evidence.

### 4. Root cause statement (15 min)

One primary cause + contributing factors. Example shape:

> Primary: in-process cache without cross-instance invalidation caused stale reads.  
> Contributing: undersized async executor caused create failures under load.

### 5. Remediation plan (20 min)

Include: immediate mitigation, durable fix, validation, rollback, follow-ups. **Do not implement today.**

---

## Report fields (practice log)

Incident summary · impact · timeline · evidence · hypotheses · RCA · remediation · risks · follow-ups

---

## Cursor prompts

```text
Act as Tech Lead. Challenge my RCA: what evidence is missing?
Suggest a third hypothesis I ignored.
```

---

## Done checklist

- [ ] ≥3 hypotheses evaluated
- [ ] Root cause supported by evidence
- [ ] Remediation + risks documented
- [ ] GP7 filled

**Next:** [`day-08-readiness-review.md`](day-08-readiness-review.md)
