# Day 4 — Measuring API Performance

**Unit:** Measure Performance Like an Engineer  
**Time:** ~2 hours  
**Code changes:** **None**  
**Log section:** Guided Practice 4

---

## Goal

Measure three endpoints with a repeatable method, compare averages, and recommend what to investigate next — **without optimising yet**.

---

## Skip-video brief

### Measure before optimise

Optimising without numbers wastes time and can make the wrong thing faster. Performance work starts with:

1. **What** are we measuring? (latency of specific endpoints)
2. **How** (tool, warmups, sample size)
3. **Compared to what** (other endpoints / baseline)
4. **Hypothesis** for the slowest (not a fix yet)

### Latency basics

| Term | Meaning |
|------|---------|
| Response time | Client-observed duration (Postman Time) |
| Warm vs cold | First calls pay JVM/JIT/cache costs |
| Average | Simple mean of N samples (good enough here) |
| p95 | 95th percentile — not required today, good future metric |

### Fair measurement protocol

1. App running, seed loaded, no debugger breakpoints.
2. Discard or label run #1 as warmup.
3. Five measured runs per endpoint.
4. Same machine, same network (localhost).
5. Do not change code between runs.

**Optional deep links:** [web.dev performance](https://web.dev/performance/) · [Postman responses](https://learning.postman.com/docs/sending-requests/responses/)

---

## Default endpoint trio

| # | Endpoint | Why |
|---|----------|-----|
| A | `GET /api/books/1` | Single entity + EAGER relations |
| B | `GET /api/books` or `GET /api/books?page=0&size=10` | List path (use whatever Day 3 left as default list) |
| C | `GET /api/books/search?title=Patterns` | Query + list mapping |

If Day 3 changed list to paged, use the paged URL and note it.

---

## Steps (~60 min)

### 1. Prepare sheet (5 min)

| Endpoint | R1 | R2 | R3 | R4 | R5 | Avg |
|----------|----|----|----|----|----|-----|
| A | | | | | | |
| B | | | | | | |
| C | | | | | | |

### 2. Warmup (5 min)

Hit each endpoint once; do not record (or record separately as “warmup”).

### 3. Measure (30 min)

Five runs each. In Postman, read **Time** (ms). With curl:

```bash
curl -o /dev/null -s -w '%{time_total}\n' http://localhost:8080/api/books/1
```

(`time_total` is seconds — multiply by 1000 for ms.)

### 4. Analyse (15 min)

- Compute averages
- Name the slowest
- Hypothesise **one** reason tied to code you already read, e.g.:
  - Full table load + EAGER author/category on list
  - `show-sql=true` logging overhead
  - Search `LIKE` across titles
- State what evidence you’d need before changing code (query plans, row counts, allocation profiles)

### 5. Log (5 min)

Fill GP4. Explicitly: **no code modified**.

---

## Example reasoning (illustrative — replace with your numbers)

> Slowest was `GET /api/books` at ~X ms avg vs ~Y ms for by-id. Likely because `findAll` loads all seeded books with EAGER associations and maps each to DTO. Next: count SQL statements (hibernate statistics) or compare paged vs unpaged if Day 3 shipped.

---

## What to record

- Endpoints tested
- Individual times
- Averages
- Slowest endpoint
- Possible bottleneck
- Evidence
- What to investigate next

---

## Cursor prompts

```text
Review these timings and challenge my bottleneck hypothesis.
What additional measurements would strengthen the case before caching?
```

---

## Done checklist

- [ ] Three endpoints × five runs recorded
- [ ] Averages calculated
- [ ] Slowest identified with a hypothesis
- [ ] No optimisation implemented
- [ ] Practice log GP4 filled

**Take further:** Re-measure with `spring.jpa.show-sql=false` and compare.

**Next:** [`day-05-caching-strategy.md`](day-05-caching-strategy.md)
