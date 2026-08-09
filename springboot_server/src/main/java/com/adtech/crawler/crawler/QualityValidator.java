package com.adtech.crawler.crawler;

import org.springframework.stereotype.Component;
import java.util.*;

@Component
public class QualityValidator {

    @SuppressWarnings("unchecked")
    public Map<String, Object> evaluate(Map<String, Object> extractionData) {
        int score = 0;
        List<String> flags = new ArrayList<>();
        List<String> recommendations = new ArrayList<>();

        int httpStatus = (int) extractionData.getOrDefault("http_status", 500);
        if (httpStatus == 200) {
            score += 20;
        } else {
            flags.add("Non-200 HTTP response code: " + httpStatus);
        }

        Map<String, Object> gptStatus = (Map<String, Object>) extractionData.getOrDefault("gpt_status", Collections.emptyMap());
        List<Map<String, Object>> slots = (List<Map<String, Object>>) gptStatus.getOrDefault("slots", Collections.emptyList());
        if (Boolean.TRUE.equals(gptStatus.get("loaded"))) {
            score += 20;
        }
        if (!slots.isEmpty()) {
            score += 20;
        } else {
            flags.add("No GPT ad slots detected");
            recommendations.add("Verify Google Publisher Tag integration");
        }

        Map<String, Object> headerBidding = (Map<String, Object>) extractionData.getOrDefault("header_bidding", Collections.emptyMap());
        List<Map<String, Object>> bidderSummary = (List<Map<String, Object>>) headerBidding.getOrDefault("bidder_summary", Collections.emptyList());
        if (Boolean.TRUE.equals(headerBidding.get("detected")) || !bidderSummary.isEmpty()) {
            score += 20;
        } else {
            recommendations.add("Consider implementing Prebid.js or Amazon TAM header bidding");
        }

        Map<String, Object> adsTxt = (Map<String, Object>) extractionData.getOrDefault("ads_txt", Collections.emptyMap());
        if (Boolean.TRUE.equals(adsTxt.get("exists"))) {
            score += 20;
        } else {
            flags.add("ads.txt not found");
            recommendations.add("Publish an IAB compliant ads.txt file");
        }

        String rating = "POOR";
        if (score >= 90) rating = "EXCELLENT";
        else if (score >= 70) rating = "GOOD";
        else if (score >= 50) rating = "FAIR";

        Map<String, Object> metrics = new HashMap<>();
        metrics.put("gpt_slots_count", slots.size());
        metrics.put("valid_gpt_slots", slots.size());
        metrics.put("prebid_detected", headerBidding.getOrDefault("detected", false));
        metrics.put("bids_captured", bidderSummary.size());
        metrics.put("iframes_count", ((List<?>) extractionData.getOrDefault("rendered_iframes", Collections.emptyList())).size());

        Map<String, Object> result = new HashMap<>();
        result.put("quality_score", score);
        result.put("passed_validation", score >= 70);
        result.put("quality_rating", rating);
        result.put("flags", flags);
        result.put("recommendations", recommendations);
        result.put("metrics", metrics);
        return result;
    }
}
