package com.adtech.crawler.model.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CrawlJobListItemDto {
    private String jobId;
    private String targetUrl;
    private Integer httpStatus;
    private String status;
    private Integer qualityScore;
    private String qualityRating;
    private LocalDateTime createdAt;
}
