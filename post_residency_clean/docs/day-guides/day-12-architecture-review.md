# Day 12 — Conduct an Architecture Review

**Time:** ~2 hours · **Artefact:** [`artefacts/day-12-design-proposal.md`](artefacts/day-12-design-proposal.md)  
**Log:** Guided Practice 12

---

## Goal

Review a design **before** implementation. Surface assumptions, risks, and trade-offs. Recommend Approve / Approve with Required Changes / Reject Pending Rework — **without redesigning**.

---

## Skip-video brief

### What architecture review is for

- Catch irreversible coupling early (shared DB, sync payment in request path)
- Force explicit assumptions
- Align product speed with operational reality
- Leave authors with **required changes**, not a competing design essay

### Lenses

| Lens | Questions |
|------|-----------|
| Reliability | Failure modes? Retries? Idempotency? |
| Security / compliance | PCI, PII in logs, tokens |
| Operability | Metrics, rollback, flag strategy |
| Evolution | Shared DB escape cost? |
| Product | Goals/non-goals respected? |

**Optional deep links:** [Google eng practices / design docs](https://google.github.io/eng-practices/) · [AWS Well-Architected](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) · [Evolutionary architecture](https://martinfowler.com/articles/evo-arch-forward.html)

---

## Phases

### 1. Assumptions (20 min)

Mine the draft. Examples:

- Shared DB is acceptable short-term
- Sync payment can meet 500ms p95
- Kafka consumers won’t need exactly-once for email
- “Add saga later” is safe
- Two regions can wait

### 2. Risks & trade-offs (25 min)

| Decision | Benefit | Risk |
|----------|---------|------|
| Shared DB | Speed | Coupling, contested migrations, blast radius |
| Sync payment | Simple status=PAID | Latency, timeouts, partial failure |
| No outbox | Less infra | Lost events on crash after commit |
| Feature flag 10% | Safe rollout | Needs cohort metrics |

Identify **one** decision with long-term operational pain (often shared DB or missing outbox).

### 3. Review questions (15 min)

Write 5–8 questions for the authors (idempotency keys, payment timeout behaviour, stock oversell, PII, DLQ for email, ownership of schema).

### 4. Recommendation (30 min)

Most designs like this land on **Approve with Required Changes** or **Reject Pending Rework**. Pick one and list **required** changes (not wishlist).

Example required changes (illustrative):

1. Document payment timeout/compensation path  
2. Outbox or transactional messaging for `order-placed`  
3. Clarify PCI boundary (no card data in Order Service logs)  
4. Define stock concurrency test plan  

Positives to acknowledge: clear goals/non-goals, flag rollout, reuse of catalog.

---

## What to record

Executive summary · assumptions · major risks · trade-offs · questions · blockers · positives · recommendation · required changes · evidence

---

## Cursor prompts

```text
Act as proposal author defending shared database. I must still decide if it's blocking.
Act as SRE: what is the single worst production night this design creates?
```

---

## Done checklist

- [ ] Assumptions listed
- [ ] Risks linked to trade-offs
- [ ] Questions prepared
- [ ] One clear recommendation
- [ ] Did not redesign the system
- [ ] GP12 filled

---

## Program complete

Return to [`00-program-overview.md`](00-program-overview.md) and tick the program-level done definition. Ensure [`practice-log.md`](practice-log.md) has all 12 sections filled with evidence.
