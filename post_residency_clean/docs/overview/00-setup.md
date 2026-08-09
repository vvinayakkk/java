# Day 0 — Setup & Bootstrap

**Time:** 30–45 minutes (once)  
**Goal:** Run `spring-bookstore` locally with seeded data and confirm the Day-6 hook is present but disabled.

---

## Prerequisites

| Tool | Version |
|------|---------|
| JDK | 17+ |
| Maven | 3.6+ |
| Postman (or Insomnia/curl) | any recent |
| IDE | IntelliJ / Cursor / VS Code |

Verify:

```bash
java -version
mvn -version
```

---

## 1. Project location

```bash
cd /Users/vinayak.b/Desktop/post_bootcamp/spring-bookstore
```

Upstream: https://github.com/shafakyildiz/spring-bookstore  
Local patches already applied for this residency:

| File | Why |
|------|-----|
| `config/DataLoader.java` | Seeds ~5 authors, ~5 categories, ~90 books |
| `service/CatalogSyncService.java` | Feature-flagged sync for Day 6 |
| `service/BookService.java` | Calls catalog sync after create |
| `application.properties` | `app.catalog-sync.*` defaults off |

---

## 2. Run the app

```bash
mvn clean spring-boot:run
```

Expect logs roughly like:

```text
Seeded 5 authors, 5 categories, 90 books
Started BookstoreApplication
```

Base URL: `http://localhost:8080`

| Surface | URL |
|---------|-----|
| Swagger UI | http://localhost:8080/swagger-ui.html |
| OpenAPI JSON | http://localhost:8080/api-docs |
| H2 console | http://localhost:8080/h2-console |

H2 console settings:

- JDBC URL: `jdbc:h2:mem:bookstore`
- User: `sa`
- Password: *(empty)*

---

## 3. Smoke tests

```bash
# Should return a large JSON array (~90 books)
curl -s http://localhost:8080/api/books | head -c 400

# Should return one book
curl -s http://localhost:8080/api/books/1

# Search
curl -s "http://localhost:8080/api/books/search?title=Patterns"

# Available only (stock > 0)
curl -s http://localhost:8080/api/books/available | head -c 200
```

Create author then book (needed later for POST flows):

```bash
curl -s -X POST http://localhost:8080/api/authors \
  -H 'Content-Type: application/json' \
  -d '{"name":"Test Author","biography":"Lab author"}'

curl -s -X POST http://localhost:8080/api/categories \
  -H 'Content-Type: application/json' \
  -d '{"name":"Lab Category","description":"For residency labs"}'
```

Use returned IDs in a book create (Day 6). For Days 1–5, GETs are enough.

---

## 4. Confirm Day-6 hook is OFF

In `application.properties`:

```properties
app.catalog-sync.enabled=false
app.catalog-sync.delay-ms=0
```

Do **not** enable until Day 6.

---

## 5. Postman collection (manual)

Create a collection `Bookstore Residency` with:

| Name | Method | URL |
|------|--------|-----|
| Get All Books | GET | `{{baseUrl}}/api/books` |
| Get Book By Id | GET | `{{baseUrl}}/api/books/1` |
| Search Books | GET | `{{baseUrl}}/api/books/search?title=Patterns` |
| Available Books | GET | `{{baseUrl}}/api/books/available` |
| Get Authors | GET | `{{baseUrl}}/api/authors` |
| Create Book | POST | `{{baseUrl}}/api/books` |

Collection variable: `baseUrl` = `http://localhost:8080`

In Postman, turn on **Save Response** timing (Time column) for Day 4.

---

## 6. Useful package map

```text
com.bookstore
├── BookstoreApplication
├── config/          DataLoader, OpenApiConfig
├── controller/      BookController, AuthorController, CategoryController
├── service/         BookService, AuthorService, CategoryService, CatalogSyncService
├── repository/      *Repository
├── entity/          Book, Author, Category
├── dto/             *DTO
└── exception/       GlobalExceptionHandler, ResourceNotFoundException
```

---

## Done checklist

- [ ] JDK 17+ and Maven available
- [ ] App starts without errors
- [ ] `GET /api/books` returns many seeded books
- [ ] Swagger UI loads
- [ ] Postman (or curl) smoke tests pass
- [ ] Catalog sync remains disabled

**Next:** [`day-01-reading-codebase.md`](day-01-reading-codebase.md)
