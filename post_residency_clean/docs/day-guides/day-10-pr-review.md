# Day 10 — Conduct an Effective Code Review

**Time:** ~2 hours · **Artefact:** [`artefacts/day-10-pr-2481.md`](artefacts/day-10-pr-2481.md)  
**Log:** Guided Practice 10

---

## Goal

Review beyond “tests pass”: severity-rate findings, write constructive comments, recommend merge decision.

---

## Skip-video brief

### Severity model

| Level | Meaning |
|-------|---------|
| **Blocker** | Must fix before merge (security, data corruption, severe prod risk) |
| **Should Fix** | Important; fix in this PR if reasonable |
| **Nice to Have** | Improve later; don’t block |
| **Not an Issue** | Preference or already acceptable |

### Reviewer pitfalls

- “LGTM” without reading (Reviewer A)
- Architecture bike-shedding without threat (“just use Redis”) when local cache may be fine with eviction
- Personal style nits disguised as blockers

**Optional deep links:** [Google code review](https://google.github.io/eng-practices/review/) · [Writing good CLs](https://google.github.io/eng-practices/review/developer/) · [OWASP secure coding](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)

---

## Snippet scoring guide (starting point — decide yourself)

| Snippet | Likely severity | Why |
|---------|-----------------|-----|
| A `cache.put(query, result)` | Should Fix / Blocker* | Unbounded cache? key collisions? |
| B log user + query | Should Fix | PII / sensitive query leakage |
| C SQL string concat | **Blocker** | SQL injection |
| D duplicated validation | Nice to Have | Maintainability |
| E no eviction documented | Should Fix | Stale/OOM risk (aligns with Reviewer C) |
| F missing edge tests | Should Fix | Confidence gap |
| G nested loop per search | Should Fix | Complexity / latency |

\*Depends on bounds and eviction.

### Existing reviewers

- **A:** Disagree — insufficient review.
- **B:** Partially disagree — Redis not mandatory; ask for requirements (multi-instance?).
- **C:** Agree in spirit — demand eviction/TTL/invalidation story.

---

## Comment formula

```text
[Severity] What’s wrong → Why it matters in prod → Concrete suggestion
```

Example:

> **Blocker:** SQL is concatenated from `id`. This is SQL injection. Use a parameterized query / repository method. Please add a test with a malicious id payload.

---

## Decision

Given snippet C alone, **Request Changes** is the usual professional call. Argue if you choose otherwise.

---

## What to record

Executive summary · findings by severity · review comments · responses to A/B/C · questions · recommendation · merge risks · follow-ups

---

## Cursor prompts

```text
Act as PR author defending snippet C. I must still justify blocking.
Act as Security Engineer — what else would you scan for?
```

---

## Done checklist

- [ ] All snippets rated
- [ ] Reviewers A/B/C addressed
- [ ] Constructive comments written
- [ ] GP10 filled

**Next:** [`day-11-system-diagnosis.md`](day-11-system-diagnosis.md)
