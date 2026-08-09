package com.adtech.crawler.model.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.util.List;
import java.util.Map;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CrawlJobResponse {
    private String jobId;
    private String targetUrl;
    private Integer httpStatus;
    private String status;
    private boolean cached;
    private Integer qualityScore;
    private String qualityRating;
    private List<AdSlotSummaryDto> adSlotsSummary;
    private Map<String, Object> data;
}
