# Unit Testing Guide

This guide explains how to run unit tests for the Spring Bookstore REST API.

## Test Structure

The project includes comprehensive unit tests for:

- **Service Layer Tests** (`BookServiceTest`, `AuthorServiceTest`, `CategoryServiceTest`)
  - Test business logic
  - Mock repository dependencies
  - Test success and error scenarios

- **Controller Layer Tests** (`BookControllerTest`, `AuthorControllerTest`, `CategoryControllerTest`)
  - Test REST endpoints
  - Verify HTTP status codes
  - Test request/response handling
  - Test validation

- **Exception Handler Tests** (`GlobalExceptionHandlerTest`)
  - Test error handling
  - Verify error response format

## Running Unit Tests

### Option 1: Run All Tests (Recommended)

Run all tests using Maven:

```bash
mvn test
```

This will:
- Compile the test code
- Run all unit tests
- Display test results
- Show a summary at the end

### Option 2: Run Tests with Verbose Output

For more detailed output:

```bash
mvn test -X
```

Or with standard output:

```bash
mvn test -s
```

### Option 3: Run Specific Test Class

Run a single test class:

```bash
mvn test -Dtest=BookServiceTest
```

Or multiple specific classes:

```bash
mvn test -Dtest=BookServiceTest,AuthorServiceTest
```

### Option 4: Run Specific Test Method

Run a single test method:

```bash
mvn test -Dtest=BookServiceTest#testGetAllBooks
```

### Option 5: Skip Tests During Build

If you want to build without running tests:

```bash
mvn clean install -DskipTests
```

Or skip tests and compilation:

```bash
mvn clean install -Dmaven.test.skip=true
```

## Test Output

After running tests, you'll see output like:

```
[INFO] -------------------------------------------------------
[INFO]  T E S T S
[INFO] -------------------------------------------------------
[INFO] Running com.bookstore.service.BookServiceTest
[INFO] Tests run: 15, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.234 s
[INFO] Running com.bookstore.controller.BookControllerTest
[INFO] Tests run: 10, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.456 s
...
[INFO] Results:
[INFO] 
[INFO] Tests run: 45, Failures: 0, Errors: 0, Skipped: 0
[INFO] 
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
```

## Test Coverage

### View Test Reports

After running tests, Maven generates test reports in:

```
target/surefire-reports/
```

You can open the HTML reports in your browser to see detailed test results.

### Generate Test Coverage Report (Optional)

To generate a code coverage report, you can add JaCoCo plugin to `pom.xml`:

```xml
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.10</version>
    <executions>
        <execution>
            <goals>
                <goal>prepare-agent</goal>
            </goals>
        </execution>
        <execution>
            <id>report</id>
            <phase>test</phase>
            <goals>
                <goal>report</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

Then run:

```bash
mvn clean test
```

Coverage reports will be in `target/site/jacoco/index.html`

## Running Tests in IDE

### IntelliJ IDEA

1. Right-click on the test class or method
2. Select "Run 'TestName'"
3. Or use keyboard shortcut: `Ctrl+Shift+F10` (Windows/Linux) or `Cmd+Shift+R` (Mac)

To run all tests:
1. Right-click on `src/test/java`
2. Select "Run 'All Tests'"

### Eclipse

1. Right-click on the test class
2. Select "Run As" → "JUnit Test"
3. Or use keyboard shortcut: `Alt+Shift+X, T`

### VS Code

1. Install the "Java Test Runner" extension
2. Click the "Run Test" link above test methods
3. Or use the Test Explorer panel

## Test Naming Conventions

Tests follow these naming patterns:

- **Service Tests**: `testMethodName_Success`, `testMethodName_NotFound`, etc.
- **Controller Tests**: `testEndpointName`, `testEndpointName_InvalidInput`, etc.

## Understanding Test Results

### Success Indicators

- ✅ All tests pass: `Tests run: 45, Failures: 0, Errors: 0`
- ✅ BUILD SUCCESS message

### Failure Indicators

- ❌ Test failures: `Failures: 2`
- ❌ Compilation errors: Check error messages
- ❌ BUILD FAILURE message

### Common Issues

1. **Tests not found**: Make sure test files are in `src/test/java`
2. **Compilation errors**: Run `mvn clean compile` first
3. **Mockito errors**: Check that `@ExtendWith(MockitoExtension.class)` is present
4. **Missing dependencies**: Run `mvn clean install` to download dependencies

## Continuous Integration

For CI/CD pipelines, use:

```bash
mvn clean test
```

This ensures:
- Clean build environment
- All tests are executed
- Build fails if any test fails

## Best Practices

1. **Run tests before committing**: `mvn test`
2. **Fix failing tests immediately**: Don't commit broken tests
3. **Write tests for new features**: Maintain test coverage
4. **Keep tests independent**: Each test should be able to run alone
5. **Use descriptive test names**: Makes it clear what's being tested

## Quick Reference

| Command | Description |
|---------|-------------|
| `mvn test` | Run all tests |
| `mvn test -Dtest=ClassName` | Run specific test class |
| `mvn test -Dtest=ClassName#methodName` | Run specific test method |
| `mvn clean test` | Clean and run all tests |
| `mvn test -DskipTests` | Skip tests (not recommended) |

## Test Statistics

Current test coverage:
- **Service Tests**: 3 test classes, ~45 test methods
- **Controller Tests**: 3 test classes, ~30 test methods
- **Exception Tests**: 1 test class, ~3 test methods
- **Total**: ~78 unit tests

All tests use:
- **JUnit 5** for test framework
- **Mockito** for mocking dependencies
- **MockMvc** for controller testing
- **AssertJ** (via Spring Boot Test) for assertions

