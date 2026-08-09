# Guided Practice 3 – Implementing a Small Feature

**Program:** Engineering Residency – From Training to Production Thinking  
**Date:** 2026-08-01  
**Engineer:** Vinayak  
**Repository:** [spring-bookstore](https://github.com/shafakyildiz/spring-bookstore) (Local Path: `spring-bookstore/`)  
**Time Spent:** ~60 minutes (Implementation, Unit Testing, and Live HTTP Verification)

---

## 🏢 Engineering Scenario & Objective
> "Your product team has requested an enhancement to the catalog API: `GET /api/books` currently returns all books in a single flat list, which risks crashing client browsers and causing severe latency as the catalog grows. You must implement server-side pagination and dynamic sorting following production engineering discipline—delivering the smallest safe change while preserving existing system stability."

**Key Learning Goals:**
1. Interpret feature requirements and identify affected components across layers.
2. Implement safe, incremental pagination and dynamic sorting on `GET /api/books`.
3. Create dedicated response DTOs (`BookPageResponse`) to encapsulate pagination metadata cleanly.
4. Execute automated unit test suites (`mvn clean test`) and verify backward compatibility live.

---

## 💻 Feature Implementation Details

### 1. Enhancement Delivered:
- **Server-Side Pagination:** Added `page` (0-indexed, default 0) and `size` (default 10, capped at max 50) parameters.
- **Dynamic Multi-Field Sorting:** Added `sortBy` (default `id`) and `sortDir` (`asc` / `desc`, default `asc`) parameters.
- **Structured Response DTO:** Wrapped page content inside `BookPageResponse` containing page metadata (`totalPages`, `totalElements`, `pageNumber`, `pageSize`, `first`, `last`).

### 2. Classes Modified / Created:

| File Modified / Created | Changes Implemented | Engineering Rationale |
|---|---|---|
| **[MODIFY]** `BookController.java` | Updated `getAllBooks()` method signature to accept `@RequestParam` for `page`, `size`, `sortBy`, and `sortDir`. | Controller owns HTTP query parameter parsing and default values. |
| **[MODIFY]** `BookService.java` | Implemented `Pageable` creation via `PageRequest.of()`, applied safety cap (`size = Math.min(size, 50)`), mapped `Page<Book>` to `BookPageResponse`. | Service layer owns business rules (safety caps, page size enforcement, entity-to-DTO page mapping). |
| **[NEW]** `BookPageResponse.java` | Created wrapper DTO containing `List<BookDTO> content`, `int pageNumber`, `int pageSize`, `long totalElements`, `int totalPages`, `boolean last`. | Encapsulates pagination metadata cleanly without exposing raw Spring Data `PageImpl` internal structures. |
| **[MODIFY]** `BookControllerTest.java` & `BookServiceTest.java` | Updated existing unit test assertions to validate paginated response payloads and new signatures. | Ensures 100% regression safety across test suites. |

---

## 🔬 Code Snippet Highlights

### `BookController.java`
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

### `BookService.java`
```java
public BookPageResponse getAllBooks(int page, int size, String sortBy, String sortDir) {
    int cappedSize = Math.min(size, MAX_PAGE_SIZE); // MAX_PAGE_SIZE = 50
    Sort sort = sortDir.equalsIgnoreCase("desc") ? Sort.by(sortBy).descending() : Sort.by(sortBy).ascending();
    Pageable pageable = PageRequest.of(page, cappedSize, sort);
    
    Page<Book> bookPage = bookRepository.findAll(pageable);
    List<BookDTO> dtos = bookPage.getContent().stream()
            .map(this::convertToDTO)
            .collect(Collectors.toList());
            
    return new BookPageResponse(dtos, bookPage.getNumber(), bookPage.getSize(), 
                                bookPage.getTotalElements(), bookPage.getTotalPages(), bookPage.isLast());
}
```

---

## 🧪 Verification & Automated Test Results

### 1. Automated Test Verification:
Executed Maven build & test command:
```bash
cmd /c "tools\run_env.cmd mvn clean test"
```
**Output:** `Tests run: 58, Failures: 0, Errors: 0, Skipped: 0` (**BUILD SUCCESS**).

### 2. Live HTTP Verification:
Executed live request:
```http
GET http://localhost:8080/api/books?page=0&size=5&sortBy=title&sortDir=asc
```
**Response Status:** `200 OK`  
**JSON Body Sample:**
```json
{
  "content": [
    { "id": 1, "title": "Design Patterns", "price": 44.99 },
    { "id": 4, "title": "Effective Java", "price": 45.00 },
    { "id": 2, "title": "Clean Code", "price": 40.00 },
    { "id": 5, "title": "Refactoring", "price": 48.00 },
    { "id": 3, "title": "Domain-Driven Design", "price": 55.00 }
  ],
  "pageNumber": 0,
  "pageSize": 5,
  "totalElements": 90,
  "totalPages": 18,
  "last": false
}
```

---

## 💡 Engineering Trade-Offs & Future Improvements
- **Trade-Off Accepted:** Returning a structured `BookPageResponse` payload breaks legacy clients that expected a raw JSON array (`List<BookDTO>`). This was accepted as a necessary API contract update to support multi-thousand catalog scalability.
- **Future Improvement:** Add validation to reject invalid `sortBy` property names with HTTP 400 Bad Request instead of allowing Spring Data JPA to throw property exception 500.

---

## ✅ Self-Check & Completion Sign-Off
- [x] I can justify every code change across Controller, Service, and DTO layers.
- [x] I delivered the smallest safe implementation without over-engineering (YAGNI).
- [x] Existing functionality verified live against the running server.
- [x] Tested with Postman / live HTTP client and verified automated unit tests pass 100%.