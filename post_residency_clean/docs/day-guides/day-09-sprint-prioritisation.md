# Day 9 — Prioritise Engineering Work

**Time:** ~2 hours · **Artefact:** [`artefacts/day-09-backlog.md`](artefacts/day-09-backlog.md)  
**Log:** Guided Practice 9 · **Capacity:** 16 SP

---

## Goal

Build a sprint ≤16 SP that balances customer pain, security, reliability, and delivery — then revise after a mid-sprint incident.

---

## Skip-video brief

### Toil & limited capacity

Engineering time is finite. **Toil** is repetitive operational work that doesn’t create lasting value. Prioritisation is choosing what *not* to do this sprint.

### Useful lenses

| Lens | Question |
|------|----------|
| Customer impact | Who is hurting now? |
| Error budget | Are we allowed to ship features? |
| Security | What’s the exploit window? |
| Leverage | Does this reduce future toil? |
| Dependencies | Does A unblock B? |

**Optional deep links:** [Eliminating Toil (workbook)](https://sre.google/workbook/eliminating-toil/) · [Eliminating Toil (book)](https://sre.google/sre-book/eliminating-toil/) · [Error budgets](https://sre.google/workbook/error-budget-policy/) · [Tech debt quadrant](https://martinfowler.com/bliki/TechnicalDebtQuadrant.html)

---

## Phases

### 1. Understand backlog (15 min)

Mark urgent vs important; note Feature A = 8 SP alone.

### 2. Score each item (25 min)

Use a simple table: customer / business / risk reduction / effort.

### 3. Build the sprint (25 min)

Select items summing to **≤16**. Example *shape* (not mandatory):

- Checkout timeout (5) + payment retry (5) + vuln (2) + alerts (3) = 15  
  Defers Feature A — product will push back; document why error budget / tickets win.

Your mix can differ; justify every include **and** every deferral.

### 4. Defend trade-offs (15 min)

Who hates this plan? Product? Security? SRE?

### 5. Mid-sprint incident (20 min)

Assume Day-4 major incident. What slips? What gets pulled in? Update the proposal.

---

## What to record

Executive summary · criteria · assessment · selected work · deferred · trade-offs · stakeholder impact · risks accepted · success measures · mid-sprint revision

---

## Cursor prompts

```text
Act as Engineering Manager. Attack my 16 SP plan.
Identify a hidden dependency between backlog items.
```

---

## Done checklist

- [ ] Entire backlog evaluated
- [ ] Sprint ≤ 16 SP
- [ ] Mid-sprint change addressed
- [ ] GP9 filled

**Next:** [`day-10-pr-review.md`](day-10-pr-review.md)
