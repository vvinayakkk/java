package com.adtech.crawler.controller;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

@RestController
public class HealthController {

    @Value("${spring.application.name:Forbes AdTech Crawler API (Spring Boot)}")
    private String appName;

    @Value("${app.version:2.0.0}")
    private String appVersion;

    @GetMapping("/")
    public ResponseEntity<Map<String, String>> healthCheck() {
        Map<String, String> response = new HashMap<>();
        response.put("title", appName);
        response.put("version", appVersion);
        response.put("status", "ONLINE");
        response.put("framework", "Spring Boot 3 + Playwright Java SDK");
        return ResponseEntity.ok(response);
    }
}
