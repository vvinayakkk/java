# Guided Practice 1 – Reading an Existing Codebase

**Program:** Engineering Residency – From Training to Production Thinking  
**Date:** 2026-08-01  
**Engineer:** Vinayak  
**Repository:** [spring-bookstore](https://github.com/shafakyildiz/spring-bookstore) (Local Path: `spring-bookstore/`)  
**Time Spent:** ~45 minutes (Static Architecture Trace & Live HTTP Endpoint Verification)

---

## 🏢 Engineering Scenario & Objective
> "You've just joined a new engineering team responsible for maintaining a core e-commerce REST API backend (`spring-bookstore`). Before making any code modifications, your first responsibility is to understand how the existing application is structured, how components interact, and how HTTP requests traverse through each architectural layer to the database."

**Key Learning Goals:**
1. Identify the package-by-layer structure of a Spring Boot enterprise application.
2. Locate Controller, Service, Repository, DTO, and Entity/Model components.
3. Trace an HTTP `GET` request end-to-end: `Client → Controller → Service → Repository → H2 Database → Client`.
4. Understand where business logic belongs and justify why it resides in the Service layer rather than the Controller.

---

## 🎯 Mandatory Architecture Identification

| Architectural Layer | Identified Package / Class Name | Responsibility & Functionality |
|---|---|---|
| **Controller Layer** | `com.bookstore.controller.BookController` | Handles HTTP requests, maps URLs (`/api/books`), validates path variables/query parameters, calls the Service layer, and returns `ResponseEntity<T>` HTTP responses. |
| **Service Layer** | `com.bookstore.service.BookService` | Contains core business logic, transaction management (`@Transactional`), entity lookup validation, error throwing (`ResourceNotFoundException`), ISBN uniqueness checks, and DTO conversion. |
| **Repository Layer** | `com.bookstore.repository.BookRepository` | Data Access Object (DAO) interface extending Spring Data JPA's `JpaRepository<Book, Long>`. Executes SQL/HQL queries against the H2 database. |
| **Model / Entity Layer** | `com.bookstore.entity.Book` (and related `Author`, `Category`) | JPA Entities mapped to relational database tables (`books`, `authors`, `categories`) using Hibernate annotations (`@Entity`, `@Table`, `@ManyToOne`). |
| **DTO Layer** | `com.bookstore.dto.BookDTO` | Data Transfer Objects used to decouple internal JPA database entities from external REST API representations. |

---

## 🔄 End-to-End Request Flow Trace

**Endpoint Traced:** `GET /api/books/{id}` (Specifically tested with ID = `1`)

### Detailed Step-by-Step Execution Sequence:
1. **Client / Postman Request:**  
   Client issues an HTTP GET request to `http://localhost:8080/api/books/1`.
2. **Controller Routing (`BookController`):**  
   Spring MVC routes the request to `@GetMapping("/{id}") public ResponseEntity<BookDTO> getBookById(@PathVariable Long id)`. Controller invokes `bookService.getBookById(id)`.
3. **Service Processing (`BookService`):**  
   `BookService.getBookById(1)` is executed within a read-only transaction. It calls `bookRepository.findById(1)`.
4. **Repository Execution (`BookRepository`):**  
   Spring Data JPA translates `findById(1)` into an H2 SQL query:  
   `SELECT b.*, a.*, c.* FROM books b LEFT JOIN authors a ON b.author_id = a.id LEFT JOIN categories c ON b.category_id = c.id WHERE b.id = 1`.
5. **Database Interaction (H2 In-Memory DB):**  
   H2 fetches the record for Book ID 1 along with associated Author (ID 1) and Category (ID 1) data.
6. **Domain Entity to DTO Conversion:**  
   If found, `BookService` calls `convertToDTO(Book book)` to map entity fields into a clean `BookDTO` instance. If not found, it throws `ResourceNotFoundException("Book not found with id: 1")`.
7. **HTTP Response:**  
   The controller wraps the `BookDTO` inside `ResponseEntity.ok()` and returns HTTP 200 OK with JSON payload to the client:
   ```json
   {
     "id": 1,
     "title": "Design Patterns",
     "isbn": "978-0201633610",
     "price": 44.99,
     "stockQuantity": 15,
     "authorName": "Erich Gamma",
     "categoryName": "Software Engineering"
   }
   ```

---

## 💡 Business Logic Analysis & Engineering Defense

### 1. Where does the business logic live?
The business logic lives strictly inside **`com.bookstore.service.BookService`**.

### 2. What specific business rules does it enforce?
- **Resource Existence Validation:** Ensures an entity exists before processing; throws `ResourceNotFoundException` if missing.
- **Data Integrity & Constraints:** Validates ISBN uniqueness during book creation to prevent duplicate catalog entries.
- **Entity Association Resolution:** Resolves foreign key relationships (e.g., verifying `authorId` and `categoryId` exist before attaching them to a new `Book`).
- **DTO Mapping Safety:** Converts internal JPA relational entities into external DTO representations to avoid leaking database schemas or private entity state.

### 3. Why does business logic belong in the Service layer instead of the Controller?
- **Separation of Concerns:** Controllers are responsible ONLY for HTTP protocol orchestration (parsing headers, URL parameters, status codes, content-types).
- **Reusability & DRY Principles:** Service methods can be reused across different entry points (e.g., REST Controllers, gRPC handlers, scheduled background jobs, CLI commands) without duplicating business validation logic.
- **Transactional Integrity (`@Transactional`):** Database transactions are scoped at the service level so all database modifications commit or rollback atomically.
- **Testability:** Service classes can be unit-tested in isolation using standard mocks (e.g., Mockito) without spinning up a heavy HTTP servlet environment.

---

## 🔬 Live Environment Verification
- **Test Command Executed:** `curl -s http://localhost:8080/api/books/1`
- **Result:** Successfully returned HTTP 200 OK with seeded book entity payload (`Design Patterns`, ISBN `978-0201633610`).
- **Automated Tests:** All 58 unit tests passed (`mvn clean test`).

---

## ✅ Self-Check & Completion Sign-Off
- [x] I can explain the Spring Boot project structure (Package-by-Layer).
- [x] I can locate and distinguish Controller, Service, Repository, DTO, and Entity layers.
- [x] I can trace an HTTP GET request end-to-end with class and method names.
- [x] I can explain where business logic lives and defend its placement in the Service layer.