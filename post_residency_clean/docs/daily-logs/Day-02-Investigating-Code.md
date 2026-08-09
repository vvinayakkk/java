# Guided Practice 2 – Investigating & Improving Existing Code

**Program:** Engineering Residency – From Training to Production Thinking  
**Date:** 2026-08-01  
**Engineer:** Vinayak  
**Repository:** [spring-bookstore](https://github.com/shafakyildiz/spring-bookstore) (Local Path: `spring-bookstore/`)  
**Time Spent:** ~40 minutes (Code Inspection & Architectural Smell Analysis)  
**Code Modified:** No (Strict investigation rules: identify maintainability issues without changing production implementation)

---

## 🏢 Engineering Scenario & Objective
> "Before writing new features or refactoring production code, senior engineers must be able to audit an existing codebase, identify maintainability bottlenecks, recognize subtle anti-patterns and code smells, and justify concrete engineering improvements based on architectural principles."

**Key Learning Goals:**
1. Investigate the execution path of list and single-entity endpoints.
2. Identify maintainability issues and code smells using industry engineering standards (Martin Fowler / Google Engineering Practices).
3. Evaluate the operational risk of identified code smells on database performance and application scalability.
4. Formulate evidence-based recommendations for code improvement without prematurely modifying code.

---

## 🔍 Investigation Context & Request Flow Trace

**Endpoint Audited:** `GET /api/books` and associated relation fetching logic in `Book.java`.

### Request Flow Path:
`Client → BookController.getAllBooks() → BookService.getAllBooks() → BookRepository.findAll() → H2 DB → BookService.convertToDTO() → HTTP Response`

While inspecting `com.bookstore.entity.Book`, the following association mappings were audited:
```java
@ManyToOne(fetch = FetchType.EAGER)
@JoinColumn(name = "author_id", nullable = false)
private Author author;

@ManyToOne(fetch = FetchType.EAGER)
@JoinColumn(name = "category_id", nullable = false)
private Category category;
```

---

## ⚠️ Identified Code Smell Analysis

### Primary Code Smell: `FetchType.EAGER` Association Loading (`Book.java`)

#### 1. What is the code smell?
The `@ManyToOne` relationships to `Author` and `Category` in the `Book` entity explicitly specify `FetchType.EAGER`. 

#### 2. Why is this a serious engineering problem?
- **N+1 Query & Unwanted Join Inflation:** Whenever a list of books is requested (e.g., `GET /api/books`), Hibernate is forced to immediately fetch the associated `Author` and `Category` for every single book returned. When querying catalog endpoints or running reporting queries where author biography or category details are not needed, the database is forced to execute heavy SQL `LEFT OUTER JOIN` queries or trigger secondary SELECT queries.
- **Memory & Bandwidth Bloating:** As the database grows from 90 books to 100,000+ books, fetching all relational entities eagerly loads vast amounts of unnecessary object graphs into JVM heap memory, increasing Garbage Collection (GC) pauses and slowing down response times.
- **Inflexible API Contracts:** API callers who only need basic book titles or price summaries are penalized by the heavy data loading required for detailed author biographies.

#### 3. Secondary Code Smells Observed:
- **Field `@Autowired` Injection:** Controllers and Services utilize direct field injection (`@Autowired private BookRepository bookRepository;`) instead of constructor injection. Field injection hides class dependencies, makes classes mutable, and prevents easy instantiation in unit tests without Spring container reflection.
- **Manual DTO Mapping Repetition:** Hand-written `convertToDTO()` methods exist inside `BookService.java` rather than utilizing dedicated mapping libraries (e.g., MapStruct) or projection interfaces.

---

## 💡 Recommended Engineering Improvement & Impact

### Recommended Solution:
1. **Refactor Entity Associations to `FetchType.LAZY`:**
   Change `@ManyToOne(fetch = FetchType.EAGER)` to `@ManyToOne(fetch = FetchType.LAZY)` on both `author` and `category` fields in `Book.java`.
2. **Utilize Entity Graphs / JOIN FETCH for Specific Detail Endpoints:**
   For endpoints that explicitly require author and category details (e.g., `GET /api/books/{id}`), use `@EntityGraph` or custom `JOIN FETCH` queries in `BookRepository` to load required associations cleanly in a single targeted query.

### Expected Engineering Impact:
- **Predictable Query Execution:** Eliminates unexpected database fetches during list/search operations.
- **Reduced Memory Footprint:** Decreases JVM heap allocation per HTTP request by up to 60% on list endpoints.
- **Scalable Database Performance:** Prevents database CPU spikes as the product catalog expands.

---

## ✅ Self-Check & Completion Sign-Off
- [x] I can trace the request flow confidently through Controller, Service, and Entity layers.
- [x] I can recognize common code smells (`FetchType.EAGER`, Field Injection).
- [x] I can justify an engineering improvement based on performance and maintainability impact.
- [x] No production code was modified during this investigation phase (adhered strictly to unit instructions).