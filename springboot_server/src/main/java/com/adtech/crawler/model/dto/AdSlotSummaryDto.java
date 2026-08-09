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
public class AdSlotSummaryDto {
    private String slotId;
    private String adUnitPath;
    private Map<String, Integer> dimensions;
    private List<String> declaredSizes;
    private boolean isVisible;
    private String monetizationType;
    private String winningBidder;
    private double winningCpm;
    private String currency;
    private String creativeAssetUrl;
    private String destinationClickUrl;
}
