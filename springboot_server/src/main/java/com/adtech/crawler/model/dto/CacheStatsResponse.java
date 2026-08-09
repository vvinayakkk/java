package com.adtech.crawler.model.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CacheStatsResponse {
    private boolean redisAvailable;
    private long adtechCacheKeys;
    private long totalKeys;
    private String mode;
}
