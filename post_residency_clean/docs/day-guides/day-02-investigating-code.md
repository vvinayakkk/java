# Day 2 — Investigating & Improving Existing Code

**Unit:** Debug Like an Engineer  
**Time:** ~2 hours  
**Code changes:** **None** (recommend only)  
**Log section:** Guided Practice 2

---

## Goal

Execute one endpoint, re-trace the flow, identify **one** maintainability issue, and recommend a practical fix with engineering benefit — without changing code.

---

## Skip-video brief

### Code smells (what they are)

A **code smell** is a surface signal that often correlates with deeper design problems. Smells are not compiler errors; they are maintainability risks.

Common families (Refactoring Guru / Fowler):

| Family | Examples relevant here |
|--------|-------------------------|
| Bloaters | Long methods, duplicated mapping blocks |
| Object-orientation abusers | Anemic vs over-coupled models |
| Change preventers | Shotgun surgery when DTO mapping copied in 3 services |
| Dispensables | Dead code, speculative generality |
| Couplers | Feature envy, inappropriate intimacy |

### Production engineer stance

1. Reproduce behaviour (Postman).
2. Trace with evidence.
3. Name the smell precisely.
4. Explain **customer/engineer impact**.
5. Propose the smallest improvement that pays rent.
6. Do **not** “drive-by refactor” without a goal.

**Optional deep links:** [Fowler – Code Smell](https://martinfowler.com/bliki/CodeSmell.html) · [Refactoring Guru – Smells](https://refactoring.guru/refactoring/smells) · [Google eng practices](https://google.github.io/eng-practices/)

---

## Repo touchpoints

Re-use Day 1 endpoint or pick another:

| Endpoint | Why interesting |
|----------|-----------------|
| `GET /api/books/1` | EAGER joins + DTO mapping |
| `GET /api/books` | Loads all books + EAGER relations |
| `POST /api/books` | Validation + ISBN rule + catalog sync hook |

Smell candidates already present:

1. **Field injection** — `@Autowired` on fields in controllers/services (harder to test, hides dependencies).
2. **EAGER `@ManyToOne`** on `Book.author` / `Book.category` — always loads relations; costly on list endpoints.
3. **Duplicated manual mapping** — `convertToDTO` / `convertToEntity` repeated patterns across services.
4. **Class-level `@Transactional`** on `BookService` — read methods participate in transactions unnecessarily.
5. **Inconsistent OpenAPI annotations** — some Book endpoints documented, others not (API usability smell).

Pick **ONE**.

---

## Steps (~60 min)

### 1. Execute (10 min)

```http
GET http://localhost:8080/api/books
```

Note status, body shape, Postman time (baseline curiosity only — measuring is Day 4).

### 2. Trace (15 min)

Document:

```text
Client → BookController.getAllBooks
      → BookService.getAllBooks
      → BookRepository.findAll
      → H2 + EAGER author/category per row
      → stream map convertToDTO
```

### 3. Identify one smell (15 min)

Example write-up (EAGER fetch):

- **Smell:** Inappropriate fetch strategy / performance-prone association loading
- **Where:** `Book.java` — `@ManyToOne(fetch = FetchType.EAGER)` on `author` and `category`
- **Why it matters:** `getAllBooks` becomes N association loads (or fat joins) even when callers need a subset of fields; gets worse as catalog grows; surprises future endpoints
- **Improvement:** Default to `LAZY`; fetch joins or entity graphs only where needed; consider projection DTOs for list views
- **Benefit:** Predictable query cost, safer scaling of list APIs, clearer intent

### 4. Sanity-check with AI (optional, 10 min)

Ask AI for smells, then **reject** anything you cannot point to in a file/line.

### 5. Log (10 min)

Fill GP2. Explicitly state: **no code modified**.

---

## What to record

- Repository
- Endpoint investigated
- Request flow
- Code smell identified
- Why it matters
- Recommended improvement
- Expected engineering impact

---

## Cursor prompts

```text
Trace GET /api/books and list possible code smells with file references.
Challenge this smell analysis: is EAGER actually a problem at 90 rows? When does it become one?
```

---

## Done checklist

- [ ] Mandatory concepts understood
- [ ] Endpoint executed in Postman
- [ ] One smell documented with impact
- [ ] Improvement recommended (not implemented)
- [ ] Practice log GP2 filled

**Take further:** Check whether the same smell appears in `AuthorService` / `CategoryService`.

**Next:** [`day-03-implementing-feature.md`](day-03-implementing-feature.md)
