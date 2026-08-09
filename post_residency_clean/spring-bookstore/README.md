# 📚 Spring Bookstore REST API (Post-Residency Clean Build)

> **Complete 12-Day Engineering Residency Master Implementation**  
> A production-grade REST API built with **Spring Boot 3**, **Java 17/21**, **Spring Data JPA**, **H2 In-Memory Database**, **SpringDoc OpenAPI / Swagger UI**, **Async Execution**, **Spring Caching**, and **JUnit 5 / Mockito Test Suite**.

---

## 📌 Executive Directory & Execution Summary

To run or test this project on any machine (including company laptops without AI tools), execute all commands from the **`spring-bookstore`** project directory:

```bash
# 1. Navigate to the project directory from repo root
cd post_residency_clean/spring-bookstore

# 2. Build the application & run unit tests
mvn clean install

# 3. Start the application
mvn spring-boot:run
```

---

## ⚙️ System Prerequisites

Ensure the following tools are installed and available on your system PATH:

* **Java Development Kit (JDK)**: Version 17 or higher (Java 17 / 21 recommended). Verify with:
  ```bash
  java -version
  ```
* **Apache Maven**: Version 3.8+ (or use wrapper). Verify with:
  ```bash
  mvn -version
  ```
* **Web Browser / cURL / Postman**: For testing API endpoints and viewing Swagger UI dashboards.

---

## 🚀 Quick Setup & Execution Guide (Step-by-Step)

### Step 1: Navigate to Project Directory
Always ensure your current working directory is `post_residency_clean/spring-bookstore`:

```bash
# From workspace / repository root:
cd post_residency_clean/spring-bookstore
```

---

### Step 2: Build the Application
Clean the target folder, compile source files, execute all unit tests, and build the executable JAR:

```bash
mvn clean install
```

*To build quickly without running tests:*
```bash
mvn clean install -DskipTests
```

---

### Step 3: Run the Application
Start the embedded Tomcat web server on port `8080`:

```bash
mvn spring-boot:run
```

*Alternatively, run using the compiled JAR file:*
```bash
java -jar target/spring-bookstore-1.0.0.jar
```

Upon successful startup, the terminal will log:
```text
[INFO] Started BookstoreApplication in X.XXX seconds (process running)
[INFO] Seeded 5 authors, 5 categories, 90 books
```

---

## 🌐 Interactive Dashboards & Documentation

Once the server is running on `http://localhost:8080`, open the following URLs in your web browser:

| Interface / Dashboard | Access URL | Description & Credentials |
| :--- | :--- | :--- |
| **Swagger UI (Primary)** | `http://localhost:8080/swagger-ui.html` | Interactive API documentation to browse and test all REST endpoints. |
| **Swagger UI (Alternative)**| `http://localhost:8080/swagger-ui/index.html` | Fallback URL path for Swagger UI. |
| **OpenAPI 3.0 JSON Spec** | `http://localhost:8080/api-docs` | Raw OpenAPI JSON schema definition. |
| **H2 Database Console** | `http://localhost:8080/h2-console` | Database administration console.<br/>• **JDBC URL**: `jdbc:h2:mem:bookstore`<br/>• **User**: `sa`<br/>• **Password**: *(Leave empty)* |

---

## 🗄️ Pre-Seeded Demo Data (`DataLoader.java`)

To ensure all listing, filtering, search, and availability endpoints are testable immediately upon startup without manual data entry, `DataLoader.java` automatically seeds the database:

* **5 Authors**: Ada Lovelace, Grace Hopper, Alan Turing, Donald Knuth, Barbara Liskov.
* **5 Categories**: Software Engineering, Algorithms, Distributed Systems, Security, Career.
* **90 Books**: Complete book catalog pre-populated with titles, ISBNs, prices, stock quantities, and publication dates (including out-of-stock items for testing `/api/books/available`).

---

## 📡 REST API Endpoint Reference & cURL Commands

### 1. Book Management Endpoints (`/api/books`)

| Method | Endpoint Path | Description | Example cURL Command |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/books` | Get all books (Supports pagination & sorting) | `curl -X GET "http://localhost:8080/api/books"` |
| `GET` | `/api/books/{id}` | Get book details by ID | `curl -X GET "http://localhost:8080/api/books/1"` |
| `GET` | `/api/books/isbn/{isbn}` | Get book by ISBN string | `curl -X GET "http://localhost:8080/api/books/isbn/978-0-0001-1001-1"` |
| `GET` | `/api/books/search?title={t}`| Search books by title keyword | `curl -X GET "http://localhost:8080/api/books/search?title=Patterns"` |
| `GET` | `/api/books/author/{authorId}`| Get books by Author ID | `curl -X GET "http://localhost:8080/api/books/author/1"` |
| `GET` | `/api/books/category/{catId}` | Get books by Category ID | `curl -X GET "http://localhost:8080/api/books/category/1"` |
| `GET` | `/api/books/price-range` | Filter by price range (`?minPrice=10&maxPrice=30`)| `curl -X GET "http://localhost:8080/api/books/price-range?minPrice=10&maxPrice=30"` |
| `GET` | `/api/books/available` | Filter available books in stock (`stockQuantity > 0`) | `curl -X GET "http://localhost:8080/api/books/available"` |
| `POST` | `/api/books` | Create a new book entry | *(See JSON Payload sample below)* |
| `PUT` | `/api/books/{id}` | Update an existing book | *(See JSON Payload sample below)* |
| `DELETE`| `/api/books/{id}` | Delete a book by ID | `curl -X DELETE "http://localhost:8080/api/books/1"` |

#### Sample Create Book Request (`POST /api/books`)
```bash
curl -X POST "http://localhost:8080/api/books" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Clean Code Architecture Handbook",
    "isbn": "978-0132350884",
    "price": 39.99,
    "stockQuantity": 25,
    "description": "Comprehensive guide to software craftsmanship and system design.",
    "publicationDate": "2024-01-15",
    "authorId": 1,
    "categoryId": 1
  }'
```

---

### 2. Author Management Endpoints (`/api/authors`)

| Method | Endpoint Path | Description | Example cURL Command |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/authors` | Get list of all authors | `curl -X GET "http://localhost:8080/api/authors"` |
| `GET` | `/api/authors/{id}` | Get author by ID | `curl -X GET "http://localhost:8080/api/authors/1"` |
| `POST` | `/api/authors` | Create a new author | *(See JSON Payload sample below)* |
| `PUT` | `/api/authors/{id}` | Update an existing author | `curl -X PUT "http://localhost:8080/api/authors/1" -H "Content-Type: application/json" -d '{"name":"Ada Lovelace Updated","biography":"Pioneer of computer algorithms"}'` |
| `DELETE`| `/api/authors/{id}` | Delete author by ID | `curl -X DELETE "http://localhost:8080/api/authors/1"` |

#### Sample Create Author Request (`POST /api/authors`)
```bash
curl -X POST "http://localhost:8080/api/authors" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Martin Fowler",
    "biography": "Software developer, author, and international speaker on software architecture."
  }'
```

---

### 3. Category Management Endpoints (`/api/categories`)

| Method | Endpoint Path | Description | Example cURL Command |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/categories` | Get list of all categories | `curl -X GET "http://localhost:8080/api/categories"` |
| `GET` | `/api/categories/{id}`| Get category by ID | `curl -X GET "http://localhost:8080/api/categories/1"` |
| `POST` | `/api/categories` | Create a new category | `curl -X POST "http://localhost:8080/api/categories" -H "Content-Type: application/json" -d '{"name":"DevOps","description":"CI/CD and infrastructure automation"}'` |
| `PUT` | `/api/categories/{id}`| Update an existing category | `curl -X PUT "http://localhost:8080/api/categories/1" -H "Content-Type: application/json" -d '{"name":"Core Software Engineering","description":"Updated description"}'` |
| `DELETE`| `/api/categories/{id}`| Delete category by ID | `curl -X DELETE "http://localhost:8080/api/categories/1"` |

---

## 🧪 Comprehensive Unit & Integration Testing Guide

All unit tests are written using **JUnit 5**, **Mockito**, **MockMvc**, and **AssertJ**.

### 1. Run the Entire Test Suite
From `post_residency_clean/spring-bookstore`:

```bash
mvn test
```

### 2. Run Specific Test Classes
* **Service Layer Tests**:
  ```bash
  mvn test -Dtest=BookServiceTest
  mvn test -Dtest=AuthorServiceTest
  mvn test -Dtest=CategoryServiceTest
  ```
* **Controller Layer Tests**:
  ```bash
  mvn test -Dtest=BookControllerTest
  mvn test -Dtest=AuthorControllerTest
  mvn test -Dtest=CategoryControllerTest
  ```
* **Exception Handler Tests**:
  ```bash
  mvn test -Dtest=GlobalExceptionHandlerTest
  ```

### 3. Run a Single Test Method
```bash
mvn test -Dtest=BookControllerTest#testGetAllBooks
```

### Expected Output Format
```text
[INFO] -------------------------------------------------------
[INFO]  T E S T S
[INFO] -------------------------------------------------------
[INFO] Running com.bookstore.service.BookServiceTest
[INFO] Tests run: 15, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.284 s
[INFO] Running com.bookstore.controller.BookControllerTest
[INFO] Tests run: 12, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.412 s
[INFO] 
[INFO] Results:
[INFO] Tests run: 45, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS
```

---

## 🛠️ Architecture & 12-Day Residency Milestones

```text
src/main/java/com/bookstore/
├── BookstoreApplication.java      # Main Spring Boot Entry Point & EnableAsync / EnableCaching
├── config/
│   ├── AsyncConfig.java           # ThreadPoolTaskExecutor for background sync jobs
│   ├── CacheConfig.java           # ConcurrentMapCacheManager configuration
│   ├── DataLoader.java            # Automatic startup DB seeding (90 books, 5 authors, 5 categories)
│   └── OpenApiConfig.java         # Swagger UI & OpenAPI 3.0 metadata customization
├── controller/                    # REST Controllers handling HTTP contracts & validation
│   ├── AuthorController.java
│   ├── BookController.java
│   └── CategoryController.java
├── dto/                           # Data Transfer Objects decoupled from JPA entities
│   ├── AuthorDTO.java
│   ├── BookDTO.java
│   ├── BookPageResponse.java      # Pagination metadata wrapper DTO
│   └── CategoryDTO.java
├── entity/                        # JPA Entities with Jakarta Validation & Relationships
│   ├── Author.java
│   ├── Book.java
│   └── Category.java
├── exception/                     # Centralized Global Exception Handling
│   ├── GlobalExceptionHandler.java # Custom error payload response builder (@ControllerAdvice)
│   └── ResourceNotFoundException.java # HTTP 404 Exception mapping
├── repository/                    # Spring Data JPA Repositories with custom queries
│   ├── AuthorRepository.java
│   ├── BookRepository.java        # Custom Derived Queries (findByTitleContainingIgnoreCase, etc.)
│   └── CategoryRepository.java
└── service/                       # Business Logic Layer & Async Services
    ├── AuthorService.java
    ├── BookService.java           # Spring Caching (@Cacheable, @CacheEvict)
    ├── CatalogSyncService.java    # Asynchronous task execution (@Async)
    └── CategoryService.java
```

### Summary of Residency Accomplishments
1. **Days 1–3: Domain Modeling & REST Architecture**: Built JPA Entities (`Author`, `Book`, `Category`), established foreign key relationships (`@ManyToOne`), and defined clean DTO abstractions.
2. **Days 4–6: Service Layer & Database Access**: Implemented Spring Data JPA Repositories with custom derived query methods, pagination (`Pageable`), and service-layer validation rules.
3. **Days 7–9: Robust Web Layer & OpenAPI Documentation**: Configured Jakarta Bean Validation (`@Valid`, `@NotNull`, `@Min`, `@Size`), crafted a `@ControllerAdvice` global exception handler, and integrated OpenAPI / Swagger UI.
4. **Days 10–12: Advanced Features & Testing**: Implemented Spring `@Cacheable` response caching, `@Async` background execution task pools, and achieved 100% pass rate across Mockito and MockMvc unit tests.
