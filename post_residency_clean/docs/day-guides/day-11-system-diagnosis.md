# Day 11 — Diagnose an Unfamiliar System

**Time:** ~2 hours · **Artefact:** [`artefacts/day-11-checkout-artefacts.md`](artefacts/day-11-checkout-artefacts.md)  
**Log:** Guided Practice 11

---

## Goal

Investigate an unfamiliar checkout failure with incomplete data. Recommend the **best next action** — not a certain root cause.

---

## Skip-video brief

### Troubleshooting under ambiguity

1. Build a timeline
2. Separate facts / assumptions / unknowns
3. Label signals vs noise vs red herrings
4. Rank competing hypotheses
5. Choose the action that **buys the most information or reduces blast radius fastest**

### Correlation ≠ causation

Payment Service deployed at 09:40; errors surge after **11:30 feature flag**. The deploy is suspicious but the flag timing may matter more.

**Optional deep links:** [Effective troubleshooting](https://sre.google/sre-book/effective-troubleshooting/) · [OpenTelemetry traces](https://opentelemetry.io/docs/concepts/signals/traces/)

---

## Phases

### 1. Timeline (15 min)

Merge Slack, deploys, dashboard inflection (~11:40–11:45), flag at 11:30, errors at 11:42.

### 2. Facts vs assumptions (15 min)

| Fact | Assumption |
|------|------------|
| Error% peaked 5.1% at 11:45 | “Android users” means mobile-only bug |
| Cache hit% dropped with errors | Cache is the root cause |
| Payment timeouts + retries in logs | Payment deploy at 09:40 is the cause |
| NPE appears once in excerpt | NPE is primary driver |

### 3. Signals / noise / red herring (15 min)

- **Signals:** flag enable → metric degradation; payment timeout; cache hit drop co-moving with errors
- **Noise:** auth success lines (normal path)
- **Red herring candidate:** DB CPU 32% “healthy” (doesn’t rule out lock/query issues); Recommendation Service 08:30 (early vs symptom start)

### 4. Three hypotheses (25 min)

Score High/Medium/Low confidence. For each, name evidence that would confirm/kill it.

Examples to refine:

1. Feature flag path triggers failing payment/cache interaction  
2. Payment service latent bug exposed by new traffic shape  
3. Cache stampedes → payment timeouts (secondary)

### 5. Single next action (20 min)

Good actions look like:

- Inspect flag configuration / percentage / targeting (Android?)
- Pull distributed traces for failed checkouts around 11:42
- Compare error rates flag-on vs flag-off cohort
- Prepare flag rollback **as mitigation**, while still investigating

Avoid: “rewrite payment service” as step one.

---

## What to record

All fields listed in practice-log GP11 — especially **Recommended Next Engineering Action** + rationale.

---

## Cursor prompts

```text
Act as Backend Engineer defending the Payment deploy. Attack my hypothesis ranking.
Act as EM: why is my next action the highest leverage?
```

---

## Done checklist

- [ ] Timeline reconstructed
- [ ] Facts vs assumptions listed
- [ ] 3 ranked hypotheses
- [ ] One next action justified
- [ ] No false certainty on root cause
- [ ] GP11 filled

**Next:** [`day-12-architecture-review.md`](day-12-architecture-review.md)
