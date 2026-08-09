package com.adtech.crawler.service;

import com.adtech.crawler.crawler.PlaywrightCrawlerEngine;
import com.adtech.crawler.model.dto.AdSlotSummaryDto;
import com.adtech.crawler.model.dto.CrawlJobResponse;
import com.adtech.crawler.model.entity.*;
import com.adtech.crawler.repository.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.*;

@Service
@RequiredArgsConstructor
@Slf4j
public class CrawlService {

    private final PlaywrightCrawlerEngine crawlerEngine;
    private final RedisCacheService cacheService;
    private final CrawlJobRepository crawlJobRepository;
    private final CrawlPayloadRepository crawlPayloadRepository;
    private final ObjectMapper objectMapper;

    public CrawlJobResponse executeCrawl(String url, boolean forceRefresh) {
        String cleanUrl = url.trim();

        if (!forceRefresh) {
            Map<String, Object> cachedData = cacheService.get(cleanUrl);
            if (cachedData != null) {
                cachedData.put("cached", true);
                return mapToResponse(cachedData);
            }
        }

        long startTime = System.currentTimeMillis();
        String jobId = UUID.randomUUID().toString();

        Map<String, Object> extractionData = crawlerEngine.crawl(cleanUrl);
        int executionTimeMs = (int) (System.currentTimeMillis() - startTime);

        extractionData.put("job_id", jobId);
        extractionData.put("cached", false);

        cacheService.set(cleanUrl, extractionData);

        try {
            persistToDatabase(jobId, cleanUrl, extractionData, executionTimeMs);
        } catch (Exception e) {
            log.error("Failed to persist crawl job to database: {}", e.getMessage(), e);
        }

        return mapToResponse(extractionData);
    }

    @Transactional
    protected void persistToDatabase(String jobId, String targetUrl, Map<String, Object> data, int executionTimeMs) {
        @SuppressWarnings("unchecked")
        Map<String, Object> val = (Map<String, Object>) data.getOrDefault("validation", Collections.emptyMap());

        CrawlJobEntity job = CrawlJobEntity.builder()
                .jobId(jobId)
                .targetUrl(targetUrl)
                .httpStatus((Integer) data.getOrDefault("http_status", 200))
                .status("SUCCESS")
                .qualityScore((Integer) val.getOrDefault("quality_score", 0))
                .qualityRating((String) val.getOrDefault("quality_rating", "UNKNOWN"))
                .executionTimeMs(executionTimeMs)
                .build();

        @SuppressWarnings("unchecked")
        List<Map<String, Object>> slots = (List<Map<String, Object>>) data.getOrDefault("ad_slots_summary", Collections.emptyList());
        for (Map<String, Object> s : slots) {
            @SuppressWarnings("unchecked")
            Map<String, Integer> dims = (Map<String, Integer>) s.getOrDefault("dimensions", Collections.emptyMap());
            
            AdSlotEntity slotEntity = AdSlotEntity.builder()
                    .job(job)
                    .slotId((String) s.getOrDefault("slot_id", "unknown"))
                    .adUnitPath((String) s.get("ad_unit_path"))
                    .width(dims.getOrDefault("width", 0))
                    .height(dims.getOrDefault("height", 0))
                    .declaredSizes(s.get("declared_sizes") != null ? s.get("declared_sizes").toString() : "[]")
                    .isVisible((Boolean) s.getOrDefault("is_visible", false))
                    .monetizationType((String) s.getOrDefault("monetization_type", "UNKNOWN"))
                    .winningBidder((String) s.getOrDefault("winning_bidder", "None"))
                    .winningCpm(s.get("winning_cpm") != null ? ((Number) s.get("winning_cpm")).doubleValue() : 0.0)
                    .currency((String) s.getOrDefault("currency", "USD"))
                    .creativeAssetUrl((String) s.get("creative_asset_url"))
                    .destinationClickUrl((String) s.get("destination_click_url"))
                    .build();
            job.getAdSlots().add(slotEntity);
        }

        try {
            CrawlPayloadEntity payloadEntity = CrawlPayloadEntity.builder()
                    .job(job)
                    .rawJson(objectMapper.writeValueAsString(data))
                    .build();
            job.setPayload(payloadEntity);
        } catch (Exception e) {
            log.error("JSON payload serialization error: {}", e.getMessage());
        }

        crawlJobRepository.save(job);
        log.info("Successfully persisted crawl job {} to MySQL", jobId);
    }

    @SuppressWarnings("unchecked")
    private CrawlJobResponse mapToResponse(Map<String, Object> data) {
        Map<String, Object> val = (Map<String, Object>) data.getOrDefault("validation", Collections.emptyMap());
        List<Map<String, Object>> slotsRaw = (List<Map<String, Object>>) data.getOrDefault("ad_slots_summary", Collections.emptyList());
        
        List<AdSlotSummaryDto> slotDtos = new ArrayList<>();
        for (Map<String, Object> s : slotsRaw) {
            slotDtos.add(AdSlotSummaryDto.builder()
                    .slotId((String) s.get("slot_id"))
                    .adUnitPath((String) s.get("ad_unit_path"))
                    .dimensions((Map<String, Integer>) s.get("dimensions"))
                    .declaredSizes((List<String>) s.get("declared_sizes"))
                    .isVisible(Boolean.TRUE.equals(s.get("is_visible")))
                    .monetizationType((String) s.get("monetization_type"))
                    .winningBidder((String) s.get("winning_bidder"))
                    .winningCpm(s.get("winning_cpm") != null ? ((Number) s.get("winning_cpm")).doubleValue() : 0.0)
                    .currency((String) s.getOrDefault("currency", "USD"))
                    .creativeAssetUrl((String) s.get("creative_asset_url"))
                    .destinationClickUrl((String) s.get("destination_click_url"))
                    .build());
        }

        return CrawlJobResponse.builder()
                .jobId((String) data.get("job_id"))
                .targetUrl((String) data.get("target_url"))
                .httpStatus((Integer) data.getOrDefault("http_status", 200))
                .status("SUCCESS")
                .cached(Boolean.TRUE.equals(data.get("cached")))
                .qualityScore((Integer) val.getOrDefault("quality_score", 0))
                .qualityRating((String) val.getOrDefault("quality_rating", "UNKNOWN"))
                .adSlotsSummary(slotDtos)
                .data(data)
                .build();
    }
}
