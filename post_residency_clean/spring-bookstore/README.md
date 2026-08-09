# Spring Bookstore REST API

A comprehensive REST API for managing a bookstore built with Spring Boot.

## Features

- **Book Management**: CRUD operations for books
- **Author Management**: CRUD operations for authors
- **Category Management**: CRUD operations for categories
- **Search & Filter**: Search books by title, filter by author, category, price range
- **Stock Management**: Track book inventory
- **Validation**: Input validation using Jakarta Bean Validation
- **Error Handling**: Global exception handling with meaningful error messages

## Technology Stack

- **Java 17**
- **Spring Boot 3.2.0**
- **Spring Data JPA**
- **H2 Database** (in-memory, for development)
- **Lombok** (for reducing boilerplate code)
- **Maven** (build tool)


## Project Structure

<img width="1889" height="958" alt="spring-bookstore" src="https://github.com/user-attachments/assets/90e539d5-1f44-4482-9021-b1c56464d5e0" />

```
src/
├── main/
│   ├── java/com/bookstore/
│   │   ├── controller/     # REST Controllers
│   │   ├── service/         # Business Logic Layer
│   │   ├── repository/      # Data Access Layer
│   │   ├── entity/          # JPA Entities
│   │   ├── dto/             # Data Transfer Objects
│   │   ├── exception/       # Exception Handling
│   │   └── BookstoreApplication.java
│   └── resources/
│       └── application.properties
```

## Getting Started

### Prerequisites

- Java 17 or higher
- Maven 3.6 or higher

### Running the Application

1. Clone the repository
2. Navigate to the project directory
3. Build the project:
   ```bash
   mvn clean install
   ```
4. Run the application:
   ```bash
   mvn spring-boot:run
   ```

The API will be available at `http://localhost:8080`

## API Endpoints

### Books

- `GET /api/books` - Get all books
- `GET /api/books/{id}` - Get book by ID
- `GET /api/books/isbn/{isbn}` - Get book by ISBN
- `GET /api/books/search?title={title}` - Search books by title
- `GET /api/books/author/{authorId}` - Get books by author
- `GET /api/books/category/{categoryId}` - Get books by category
- `GET /api/books/price-range?minPrice={min}&maxPrice={max}` - Get books by price range
- `GET /api/books/available` - Get available books (stock > 0)
- `POST /api/books` - Create a new book
- `PUT /api/books/{id}` - Update a book
- `DELETE /api/books/{id}` - Delete a book

### Authors

- `GET /api/authors` - Get all authors
- `GET /api/authors/{id}` - Get author by ID
- `POST /api/authors` - Create a new author
- `PUT /api/authors/{id}` - Update an author
- `DELETE /api/authors/{id}` - Delete an author

### Categories

- `GET /api/categories` - Get all categories
- `GET /api/categories/{id}` - Get category by ID
- `POST /api/categories` - Create a new category
- `PUT /api/categories/{id}` - Update a category
- `DELETE /api/categories/{id}` - Delete a category

## Example Requests

### Create an Author
```json
POST /api/authors
{
  "name": "J.K. Rowling",
  "biography": "British author, best known for the Harry Potter series"
}
```

### Create a Category
```json
POST /api/categories
{
  "name": "Fantasy",
  "description": "Fantasy fiction books"
}
```

### Create a Book
```json
POST /api/books
{
  "title": "Harry Potter and the Philosopher's Stone",
  "isbn": "978-0747532699",
  "price": 29.99,
  "stockQuantity": 50,
  "description": "The first book in the Harry Potter series",
  "publicationDate": "1997-06-26",
  "authorId": 1,
  "categoryId": 1
}
```

## Database

The application uses H2 in-memory database by default. You can access the H2 console at:
- URL: `http://localhost:8080/h2-console`
- JDBC URL: `jdbc:h2:mem:bookstore`
- Username: `sa`
- Password: (empty)

## Notes

- The database is recreated on each application restart (using `create-drop` strategy)
- For production, update `application.properties` to use a persistent database (PostgreSQL, MySQL, etc.)
- All endpoints support CORS (Cross-Origin Resource Sharing)

