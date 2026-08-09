# How to Run the Project and Access Swagger

## Running the Application

1. **Build the project** (if needed):
   ```bash
   mvn clean install
   ```

2. **Run the Spring Boot application**:
   ```bash
   mvn spring-boot:run
   ```
   
   Or if you have the JAR file:
   ```bash
   java -jar target/spring-bookstore-1.0.0.jar
   ```

3. **Wait for the application to start**. You should see:
   ```
   Started BookstoreApplication in X.XXX seconds
   ```

## Accessing Swagger UI

Once the application is running, you can access Swagger UI in several ways:

### Option 1: Swagger UI (Recommended)
Open your browser and navigate to:
```
http://localhost:8080/swagger-ui.html
```

### Option 2: Swagger UI (Alternative path)
```
http://localhost:8080/swagger-ui/index.html
```

### Option 3: OpenAPI JSON Documentation
```
http://localhost:8080/api-docs
```

## What You'll See in Swagger UI

Swagger UI provides an interactive interface where you can:

1. **Browse all API endpoints** organized by tags:
   - **Books** - All book-related endpoints
   - **Authors** - All author-related endpoints
   - **Categories** - All category-related endpoints

2. **View endpoint details**:
   - HTTP method (GET, POST, PUT, DELETE)
   - Endpoint path
   - Request parameters
   - Request body schema
   - Response schemas
   - Example values

3. **Test endpoints directly**:
   - Click "Try it out" on any endpoint
   - Fill in the parameters/request body
   - Click "Execute" to send the request
   - See the response immediately

## Other Useful URLs

- **API Base URL**: `http://localhost:8080/api`
- **H2 Database Console**: `http://localhost:8080/h2-console`
  - JDBC URL: `jdbc:h2:mem:bookstore`
  - Username: `sa`
  - Password: (leave empty)

## Quick Test Example

1. Start the application
2. Open Swagger UI at `http://localhost:8080/swagger-ui.html`
3. Navigate to **Authors** section
4. Click on `POST /api/authors` → Click "Try it out"
5. Enter this JSON in the request body:
   ```json
   {
     "name": "J.K. Rowling",
     "biography": "British author, best known for the Harry Potter series"
   }
   ```
6. Click "Execute"
7. You should see a 201 response with the created author

## Troubleshooting

- **Port 8080 already in use?** Change the port in `application.properties`:
  ```
  server.port=8081
  ```
  Then access Swagger at `http://localhost:8081/swagger-ui.html`

- **Swagger UI not loading?** Make sure:
  - The application started successfully
  - No errors in the console
  - You're using the correct URL

- **404 on Swagger endpoints?** Check that SpringDoc dependency is properly included in `pom.xml`

