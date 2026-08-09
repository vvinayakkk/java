package com.adtech.crawler.controller;

import com.adtech.crawler.model.dto.*;
import com.adtech.crawler.model.entity.CrawlJobEntity;
import com.adtech.crawler.model.entity.CrawlPayloadEntity;
import com.adtech.crawler.repository.CrawlJobRepository;
import com.adtech.crawler.repository.CrawlPayloadRepository;
import com.adtech.crawler.service.CrawlService;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.*;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/v1")
@RequiredArgsConstructor
@Slf4j
public class CrawlController {

    private final CrawlService crawlService;
    private final CrawlJobRepository crawlJobRepository;
    private final CrawlPayloadRepository crawlPayloadRepository;
    private final ObjectMapper objectMapper;

    @PostMapping("/crawl")
    public ResponseEntity<CrawlJobResponse> triggerCrawl(@Valid @RequestBody CrawlRequest request) {
        log.info("Received Crawl Request for URL: {} (forceRefresh: {})", request.getUrl(), request.isForceRefresh());
        CrawlJobResponse response = crawlService.executeCrawl(request.getUrl(), request.isForceRefresh());
        return ResponseEntity.ok(response);
    }

    @PostMapping("/crawl/batch")
    public ResponseEntity<Map<String, Object>> triggerBatchCrawl(@Valid @RequestBody BatchCrawlRequest request) {
        log.info("Received Batch Crawl Request for {} URLs (Concurrency: {})", request.getUrls().size(), request.getConcurrency());
        
        ExecutorService executor = Executors.newFixedThreadPool(Math.min(request.getConcurrency(), 10));
        List<CompletableFuture<Map<String, Object>>> futures = request.getUrls().stream()
                .map(url -> CompletableFuture.supplyAsync(() -> {
                    Map<String, Object> item = new HashMap<>();
                    item.put("url", url);
                    try {
                        CrawlJobResponse resp = crawlService.executeCrawl(url, request.isForceRefresh());
                        item.put("status", "SUCCESS");
                        item.put("quality_score", resp.getQualityScore());
                        item.put("quality_rating", resp.getQualityRating());
                        item.put("job_id", resp.getJobId());
                    } catch (Exception e) {
                        item.put("status", "FAILED");
                        item.put("error", e.getMessage());
                    }
                    return item;
                }, executor))
                .collect(Collectors.toList());

        List<Map<String, Object>> results = futures.stream().map(CompletableFuture::join).collect(Collectors.toList());
        executor.shutdown();

        long successful = results.stream().filter(r -> "SUCCESS".equals(r.get("status"))).count();
        Map<String, Object> response = new HashMap<>();
        response.put("total_urls", request.getUrls().size());
        response.put("successful_crawls", successful);
        response.put("failed_crawls", request.getUrls().size() - successful);
        response.put("results", results);

        return ResponseEntity.ok(response);
    }

    @GetMapping("/crawls")
    public ResponseEntity<List<CrawlJobListItemDto>> listCrawlJobs(
            @RequestParam(defaultValue = "20") int limit,
            @RequestParam(defaultValue = "0") int offset) {
        
        int pageNumber = offset / Math.max(limit, 1);
        Page<CrawlJobEntity> page = crawlJobRepository.findAllByOrderByCreatedAtDesc(PageRequest.of(pageNumber, limit));

        List<CrawlJobListItemDto> items = page.getContent().stream()
                .map(job -> CrawlJobListItemDto.builder()
                        .jobId(job.getJobId())
                        .targetUrl(job.getTargetUrl())
                        .httpStatus(job.getHttpStatus())
                        .status(job.getStatus())
                        .qualityScore(job.getQualityScore())
                        .qualityRating(job.getQualityRating())
                        .createdAt(job.getCreatedAt())
                        .build())
                .collect(Collectors.toList());

        return ResponseEntity.ok(items);
    }

    @GetMapping("/crawls/{jobId}")
    public ResponseEntity<Map<String, Object>> getCrawlJobDetail(@PathVariable String jobId) {
        CrawlJobEntity job = crawlJobRepository.findByJobId(jobId)
                .orElseThrow(() -> new RuntimeException("Crawl job not found: " + jobId));

        Map<String, Object> response = new HashMap<>();
        response.put("job_id", job.getJobId());
        response.put("target_url", job.getTargetUrl());
        response.put("http_status", job.getHttpStatus());
        response.put("status", job.getStatus());
        response.put("quality_score", job.getQualityScore());
        response.put("quality_rating", job.getQualityRating());
        response.put("execution_time_ms", job.getExecutionTimeMs());
        response.put("created_at", job.getCreatedAt() != null ? job.getCreatedAt().toString() : null);

        Optional<CrawlPayloadEntity> payloadOpt = crawlPayloadRepository.findByJobId(job.getId());
        if (payloadOpt.isPresent()) {
            try {
                Map<String, Object> payloadMap = objectMapper.readValue(
                        payloadOpt.get().getRawJson(), new TypeReference<Map<String, Object>>() {});
                response.put("payload", payloadMap);
            } catch (Exception e) {
                response.put("payload", Collections.emptyMap());
            }
        }

        return ResponseEntity.ok(response);
    }

    private final com.adtech.crawler.service.HtmlReportGenerator htmlReportGenerator;

    @GetMapping(value = "/crawls/{jobId}/report", produces = "text/html")
    public ResponseEntity<String> getCrawlHtmlReport(@PathVariable String jobId) {
        CrawlJobEntity job = crawlJobRepository.findByJobId(jobId)
                .orElseThrow(() -> new RuntimeException("Crawl job not found: " + jobId));

        Optional<CrawlPayloadEntity> payloadOpt = crawlPayloadRepository.findByJobId(job.getId());
        Map<String, Object> payloadMap = new HashMap<>();
        if (payloadOpt.isPresent()) {
            try {
                payloadMap = objectMapper.readValue(payloadOpt.get().getRawJson(), new TypeReference<Map<String, Object>>() {});
            } catch (Exception ignored) {}
        }

        payloadMap.put("job_id", job.getJobId());
        payloadMap.put("target_url", job.getTargetUrl());

        String html = htmlReportGenerator.generateHtmlReport(payloadMap);
        return ResponseEntity.ok(html);
    }
}
