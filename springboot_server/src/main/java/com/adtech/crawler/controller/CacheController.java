package com.adtech.crawler.controller;

import com.adtech.crawler.service.RedisCacheService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/cache")
@RequiredArgsConstructor
public class CacheController {

    private final RedisCacheService cacheService;

    @GetMapping("/stats")
    public ResponseEntity<Map<String, Object>> getCacheStats() {
        return ResponseEntity.ok(cacheService.getStats());
    }

    @PostMapping("/clear")
    public ResponseEntity<Map<String, String>> clearCache() {
        cacheService.clearCache();
        Map<String, String> response = new HashMap<>();
        response.put("status", "SUCCESS");
        response.put("message", "Cache cleared successfully");
        return ResponseEntity.ok(response);
    }
}
