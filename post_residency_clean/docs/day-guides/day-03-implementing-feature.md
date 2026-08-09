# Day 3 — Implementing a Small Feature

**Unit:** Deliver Features Like an Engineer  
**Time:** ~2 hours  
**Feature:** Pagination + sorting on `GET /api/books`  
**Log section:** Guided Practice 3

---

## Goal

Ship the **smallest safe** enhancement in an existing codebase, verify with Postman, and record trade-offs.

---

## Skip-video brief

### Reviewable changes

- Small diffs beat giant rewrites.
- Change one behaviour; keep unrelated endpoints stable.
- Name commits/PRs by intent (“add pagination to list books”), not by files touched.

### YAGNI

Do **not** also add GraphQL, Elasticsearch, or a new microservice. Validation already exists on DTOs — **do not redo validation** as your enhancement.

### Safe delivery checklist

1. Understand requirement
2. Find affected classes
3. Implement minimal change
4. Test new behaviour
5. Regression-check old behaviour
6. Document trade-offs

**Optional deep links:** [Google code review](https://google.github.io/eng-practices/review/) · [YAGNI](https://martinfowler.com/bliki/Yagni.html)

---

## Requirement (locked)

Enhance:

```http
GET /api/books?page=0&size=10&sortBy=title&sortDir=asc
```

Behaviour:

| Param | Default | Meaning |
|-------|---------|---------|
| `page` | `0` | Zero-based page index |
| `size` | `10` | Page size (cap at e.g. 50 if you want a guard) |
| `sortBy` | `id` | Entity property name |
| `sortDir` | `asc` | `asc` or `desc` |

Response options (pick one; document why):

**A (recommended):** Return a small wrapper:

```json
{
  "content": [ /* BookDTO */ ],
  "page": 0,
  "size": 10,
  "totalElements": 90,
  "totalPages": 9,
  "sortBy": "title",
  "sortDir": "asc"
}
```

**B:** Keep `List<BookDTO>` and only add paging via headers (`X-Total-Count`) — thinner but less explicit.

This guide assumes **A**.

---

## Repo touchpoints

| File | Change |
|------|--------|
| `BookController.java` | Accept query params; return page response |
| `BookService.java` | Accept `Pageable` or explicit params; map page |
| `BookRepository.java` | Already extends `JpaRepository` — `findAll(Pageable)` free |
| New: `BookPageResponse.java` (or similar) in `dto` | Wrapper |

Do **not** change `GET /api/books/{id}` behaviour.

---

## Implementation sketch

### 1. DTO wrapper

```java
public class BookPageResponse {
    private List<BookDTO> content;
    private int page;
    private int size;
    private long totalElements;
    private int totalPages;
    private String sortBy;
    private String sortDir;
    // constructors + getters/setters
}
```

### 2. Service

```java
public BookPageResponse getAllBooks(int page, int size, String sortBy, String sortDir) {
    Sort sort = sortDir.equalsIgnoreCase("desc")
            ? Sort.by(sortBy).descending()
            : Sort.by(sortBy).ascending();
    Pageable pageable = PageRequest.of(page, size, sort);
    Page<Book> result = bookRepository.findAll(pageable);

    List<BookDTO> content = result.getContent().stream()
            .map(this::convertToDTO)
            .collect(Collectors.toList());

    BookPageResponse response = new BookPageResponse();
    response.setContent(content);
    response.setPage(result.getNumber());
    response.setSize(result.getSize());
    response.setTotalElements(result.getTotalElements());
    response.setTotalPages(result.getTotalPages());
    response.setSortBy(sortBy);
    response.setSortDir(sortDir);
    return response;
}
```

Keep the old `getAllBooks()` only if something else calls it; otherwise replace the list method carefully and update tests.

### 3. Controller

```java
@GetMapping
public ResponseEntity<BookPageResponse> getAllBooks(
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "10") int size,
        @RequestParam(defaultValue = "id") String sortBy,
        @RequestParam(defaultValue = "asc") String sortDir) {
    return ResponseEntity.ok(bookService.getAllBooks(page, size, sortBy, sortDir));
}
```

### 4. Tests to update

`BookControllerTest` / `BookServiceTest` likely expect `List<BookDTO>` — update mocks/assertions. Run:

```bash
mvn test -Dtest=BookControllerTest,BookServiceTest
```

---

## Verification (Postman)

```http
GET /api/books?page=0&size=5&sortBy=title&sortDir=asc
GET /api/books?page=1&size=5&sortBy=price&sortDir=desc
GET /api/books/1
```

Confirm:

- Page 0 size 5 → 5 items
- `totalElements` ≈ 90
- Invalid `sortBy` → decide: 500 vs 400 (handling unknown property is a nice stretch)
- By-id still 200

---

## Trade-offs to mention in the log

| Choice | Upside | Downside |
|--------|--------|----------|
| Response wrapper | Clear pagination metadata | Breaks old clients expecting a raw array |
| Spring `Pageable` | Idiomatic, little code | Sort property names leak entity fields |
| Cap `size` | Protects DB | Extra validation rule |

---

## What to record

- Feature implemented
- Classes modified + why
- Testing performed
- Issues encountered
- Engineering trade-offs
- One future improvement (e.g. filter by category + page)

---

## Cursor prompts

```text
Review my pagination change for backward compatibility risks.
Suggest edge cases for page/size/sortBy.
```

---

## Done checklist

- [ ] Pagination + sorting works
- [ ] Existing by-id verified
- [ ] Tests updated/pass (or failures explained)
- [ ] Practice log GP3 filled

**Take further:** Add a max page size guard (`size > 50 → 400`).

**Next:** [`day-04-measuring-performance.md`](day-04-measuring-performance.md)
