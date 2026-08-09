# Day 1 — Reading an Existing Codebase

**Unit:** Think Like an Engineer  
**Time:** ~2 hours  
**Code changes:** None  
**Log section:** Guided Practice 1 in [`practice-log.md`](practice-log.md)

---

## Goal

Trace one real HTTP request through this bookstore app and explain where each layer’s responsibility ends.

---

## Skip-video brief (mandatory concepts)

### Layered Spring Boot backend

| Layer | Owns | Must not own |
|-------|------|----------------|
| **Controller** | HTTP mapping, status codes, request/response types | Business rules, SQL |
| **Service** | Business rules, orchestration, transactions (usually) | HTTP status details |
| **Repository** | Persistence API (Spring Data / JPA) | Domain policy |
| **Entity / Model** | Table mapping + invariants at persistence edge | Transport concerns |
| **DTO** | API shape | DB schema leakage (ideal) |

### Package-by-layer vs package-by-feature

This repo is **package-by-layer** (`controller`, `service`, `repository`, …). Fine for small services. Feature packages scale better when many domains share a deployable.

### Request lifecycle (simplified)

```text
HTTP request
  → DispatcherServlet
    → @RestController method
      → @Service method
        → JpaRepository method
          → SQL via Hibernate
            → H2
```

### Dependency injection

Spring wires `BookService` into `BookController`. This codebase uses **field `@Autowired`** (a smell you’ll revisit on Day 2). Constructor injection is the modern default.

**Optional deep links:** [Spring REST guide](https://spring.io/guides/gs/rest-service) · [Package by layer vs feature (video)](https://www.youtube.com/watch?v=B1d95I7-zsw)

---

## Repo touchpoints

| Role | Path |
|------|------|
| Controller | `…/controller/BookController.java` |
| Service | `…/service/BookService.java` |
| Repository | `…/repository/BookRepository.java` |
| Entity | `…/entity/Book.java` (+ `Author`, `Category`) |
| DTO | `…/dto/BookDTO.java` |
| Exceptions | `…/exception/GlobalExceptionHandler.java` |
| Seed | `…/config/DataLoader.java` |

---

## Steps (~60 min build)

### 1. Orient (10 min)

Open the project. Skim packages. Confirm seed ran (`GET /api/books` returns many rows).

### 2. Locate layers (10 min)

Find and note the exact file names for controller, service, repository, entity.

### 3. Pick the GET endpoint (5 min)

Use:

```http
GET http://localhost:8080/api/books/1
```

Controller method:

```java
@GetMapping("/{id}")
public ResponseEntity<BookDTO> getBookById(@PathVariable Long id)
```

### 4. Trace end-to-end (25 min)

Walk this path with the debugger or by reading:

1. `BookController.getBookById(Long id)` — returns `ResponseEntity.ok(book)`
2. `BookService.getBookById(Long id)` — `findById` or throw `ResourceNotFoundException`
3. `BookRepository` extends `JpaRepository<Book, Long>` — `findById` inherited
4. Hibernate loads `books` row; `author` and `category` are **`FetchType.EAGER`**
5. `convertToDTO(Book)` maps entity → `BookDTO` (includes `authorName`, `categoryName`)
6. JSON serialized to client

Write the flow using **actual names**:

```text
Client
  → BookController.getBookById
    → BookService.getBookById
      → BookRepository.findById
        → H2 (books + eager author/category)
          → BookService.convertToDTO
            → HTTP 200 BookDTO
```

### 5. Locate business logic (10 min)

In `BookService`, note rules that are not “just CRUD”:

- Missing book → `ResourceNotFoundException`
- On create: ISBN uniqueness check
- On create/update: author/category must exist

Controllers stay thin: they call services and wrap HTTP status.

---

## What to record (practice log)

Copy into GP1:

- GitHub repo URL
- Controller / Service / Repository / Entity file names
- GET endpoint traced
- Request flow with class.method names
- 1–2 sentences: where business logic lives and what it does

---

## Cursor prompts (optional)

```text
Explain this project architecture using the package structure.
Trace GET /api/books/{id} from controller to database with method names.
Which design pattern is BookController → BookService → BookRepository?
```

Validate every answer against the files above.

---

## Done checklist

- [ ] Mandatory concepts in the brief understood
- [ ] Layers located with real file names
- [ ] One GET traced end-to-end
- [ ] Business logic location explained
- [ ] Practice log GP1 filled

### Self-check

- [ ] I can explain the project structure
- [ ] I can identify Controller, Service, Repository
- [ ] I can trace one API request
- [ ] I know where business logic lives

**Take further:** Trace `POST /api/books` and compare where validation runs (`@Valid` on DTO vs service ISBN check).

**Next:** [`day-02-investigating-code.md`](day-02-investigating-code.md)
