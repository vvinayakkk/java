package com.adtech.crawler.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.TimeUnit;

@Service
@Slf4j
public class RedisCacheService {

    private final RedisTemplate<String, String> redisTemplate;
    private final ObjectMapper objectMapper;
    private final Map<String, String> inMemoryFallbackCache = new ConcurrentHashMap<>();

    @Value("${app.cache-ttl-seconds:3600}")
    private long ttlSeconds;

    public RedisCacheService(RedisTemplate<String, String> redisTemplate, ObjectMapper objectMapper) {
        this.redisTemplate = redisTemplate;
        this.objectMapper = objectMapper;
    }

    private String generateKey(String url) {
        try {
            MessageDigest md = MessageDigest.getInstance("MD5");
            byte[] hash = md.digest(url.toLowerCase().trim().getBytes());
            StringBuilder sb = new StringBuilder();
            for (byte b : hash) {
                sb.append(String.format("%02x", b));
            }
            return "adtech:crawl:" + sb.toString();
        } catch (NoSuchAlgorithmException e) {
            return "adtech:crawl:" + url.hashCode();
        }
    }

    public Map<String, Object> get(String url) {
        String key = generateKey(url);
        try {
            String jsonStr = redisTemplate.opsForValue().get(key);
            if (jsonStr != null) {
                log.info("Redis CACHE HIT for key: {}", key);
                return objectMapper.readValue(jsonStr, new TypeReference<Map<String, Object>>() {});
            }
        } catch (Exception e) {
            log.warn("Redis lookup failed, checking fallback memory cache: {}", e.getMessage());
            String fallbackStr = inMemoryFallbackCache.get(key);
            if (fallbackStr != null) {
                try {
                    return objectMapper.readValue(fallbackStr, new TypeReference<Map<String, Object>>() {});
                } catch (Exception ignored) {}
            }
        }
        log.info("Redis CACHE MISS for key: {}", key);
        return null;
    }

    public void set(String url, Map<String, Object> data) {
        String key = generateKey(url);
        try {
            String jsonStr = objectMapper.writeValueAsString(data);
            redisTemplate.opsForValue().set(key, jsonStr, ttlSeconds, TimeUnit.SECONDS);
            inMemoryFallbackCache.put(key, jsonStr);
            log.info("Cached result in Redis for key: {} (TTL: {}s)", key, ttlSeconds);
        } catch (Exception e) {
            log.warn("Failed to write to Redis, stored in memory cache: {}", e.getMessage());
            try {
                inMemoryFallbackCache.put(key, objectMapper.writeValueAsString(data));
            } catch (Exception ignored) {}
        }
    }

    public Map<String, Object> getStats() {
        Map<String, Object> stats = new HashMap<>();
        boolean isRedisAvailable = false;
        long totalKeys = 0;
        long adtechKeys = 0;

        try {
            Set<String> keys = redisTemplate.keys("adtech:crawl:*");
            adtechKeys = keys != null ? keys.size() : 0;
            Set<String> allKeys = redisTemplate.keys("*");
            totalKeys = allKeys != null ? allKeys.size() : 0;
            isRedisAvailable = true;
        } catch (Exception e) {
            log.warn("Redis ping failed: {}", e.getMessage());
            adtechKeys = inMemoryFallbackCache.size();
            totalKeys = inMemoryFallbackCache.size();
        }

        stats.put("redisAvailable", isRedisAvailable);
        stats.put("adtechCacheKeys", adtechKeys);
        stats.put("totalKeys", totalKeys);
        stats.put("mode", isRedisAvailable ? "REDIS_PERSISTENT" : "MEMORY_FALLBACK");
        return stats;
    }

    public void clearCache() {
        try {
            Set<String> keys = redisTemplate.keys("adtech:crawl:*");
            if (keys != null && !keys.isEmpty()) {
                redisTemplate.delete(keys);
            }
            log.info("Cleared all Redis adtech cache keys");
        } catch (Exception e) {
            log.warn("Failed to clear Redis keys: {}", e.getMessage());
        }
        inMemoryFallbackCache.clear();
    }
}
