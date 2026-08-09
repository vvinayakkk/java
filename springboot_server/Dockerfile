# Multi-Stage Build for Spring Boot + Playwright Java SDK
FROM maven:3.9.6-eclipse-temurin-17 AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn package -DskipTests

FROM mcr.microsoft.com/playwright/java:v1.42.0-jammy
WORKDIR /app
COPY --from=builder /app/target/crawler-2.0.0.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
