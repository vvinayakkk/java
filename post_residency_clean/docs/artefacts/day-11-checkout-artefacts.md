# Day 11 Artefact — Unfamiliar System (Checkout)

**Monday 11:53 AM** — Customer Support: *14 complaints in 20 minutes. Some customers cannot complete checkout. Others succeed after refreshing. Intermittent.*

**Tech Lead:** Perform initial investigation. **Don’t fix anything yet.** Recommend the best next action.

---

## Artifact 1 — Slack

- Customer Support: “Checkout failures increasing.”
- Backend Engineer: “We deployed Payment Service this morning.”
- SRE: “Infrastructure appears healthy.”
- Database Engineer: “Database CPU is only 32%.”
- Product Manager: “Most complaints are from Android users.”

## Artifact 2 — Dashboard

| Time | Error% | p95(ms) | Cache Hit% |
|------|--------|---------|------------|
| 11:30 | 0.3 | 190 | 91 |
| 11:35 | 0.4 | 195 | 90 |
| 11:40 | 1.2 | 260 | 84 |
| 11:45 | 5.1 | 490 | 62 |
| 11:50 | 2.6 | 330 | 74 |
| 11:55 | 0.4 | 220 | 91 |

## Artifact 3 — Deployment timeline

| Time | Event |
|------|-------|
| 08:30 | Recommendation Service deploy |
| 09:40 | Payment Service deploy |
| 11:30 | Feature Flag enabled |
| 11:42 | Customer errors begin |

## Artifact 4 — Log excerpts

```text
11:42:03 Payment timeout. Retry initiated.
11:42:05 Cache miss.
11:42:07 Authentication successful.
11:42:10 NullPointerException.
11:42:11 Retry succeeded.
11:42:14 Cache miss.
11:42:18 Payment timeout.
11:42:21 Inventory lookup completed.
11:42:23 Authentication successful.
11:42:27 Retry succeeded.
11:42:29 Cache miss.
11:42:31 Order completed.
```

## Artifact 5 — Service flow

```text
Gateway → Checkout → Payment → Inventory → Database
```

## Rules

- Reconstruct timeline; separate facts vs assumptions
- Identify signals, noise, one red herring
- Produce **three ranked hypotheses** with confidence
- State evidence that would raise/lower confidence
- Recommend **one** next engineering action
- **Do not claim certain root cause**
