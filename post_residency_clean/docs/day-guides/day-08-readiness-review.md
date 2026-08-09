# Day 8 — Engineering Readiness Review

**Time:** ~2 hours · **Artefact:** [`artefacts/day-08-release-evidence.md`](artefacts/day-08-release-evidence.md)  
**Log:** Guided Practice 8

---

## Goal

Decide **Approve / Approve with Conditions / Reject** using evidence — not feature enthusiasm.

---

## Skip-video brief

### Feature-complete ≠ production-ready

QA sign-off answers “does it work?” Readiness asks “can we operate, detect, and recover?”

### Release engineering levers

- Automated deploy + config as code
- Tested rollback / canaries / feature flags
- Alerts on **user-true** symptoms (errors, latency, business KPIs)
- Known vulns tracked with owners

**Optional deep links:** [Reliable Product Launches](https://sre.google/resources/book-update/reliable-product-launches-at-scale/) · [Release Engineering](https://sre.google/sre-book/release-engineering/) · [Feature Toggles](https://martinfowler.com/articles/feature-toggles.html)

---

## Phases

### Phase 1 — Facts vs assumptions vs unknowns

| Type | Examples from artefact |
|------|------------------------|
| Fact | 98% tests pass; rollback untested; manual config step exists |
| Assumption | “Logging means we can debug fast” |
| Unknown | Alert noise level; vuln exploitability window; blast radius of recommendations |

### Phase 2 — Risk register

Score each risk: likelihood × impact → priority.

Suggested rows: missing business alerts, untested rollback, manual config, medium vuln, cache/async coupling from prior days.

### Phase 3 — Mitigations

For Medium/High: concrete actions (test rollback in staging today; add error-rate alert; freeze manual config; flag-only rollout).

### Phase 4 — Decision

Most defensible default for this pack: **Approve with Conditions** — but you must argue your own call.

### Phase 5 — Meeting summary

3–5 bullets: decision, top evidence, conditions, what would flip you to Reject.

---

## What to record

Executive summary · evidence · facts vs assumptions · risk register · mitigations · conditions · rollback readiness · recommendation · follow-ups

---

## Cursor prompts

```text
Argue the opposite deployment decision from mine using only the artefact.
What operational risk did I underweight?
```

---

## Done checklist

- [ ] Risks prioritised
- [ ] One clear recommendation
- [ ] GP8 filled

**Next:** [`day-09-sprint-prioritisation.md`](day-09-sprint-prioritisation.md)
