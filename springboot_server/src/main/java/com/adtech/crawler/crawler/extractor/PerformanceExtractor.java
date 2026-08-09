package com.adtech.crawler.crawler.extractor;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.microsoft.playwright.Page;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import java.util.*;

@Component
@Slf4j
public class PerformanceExtractor implements AdTechExtractor {

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public String getName() {
        return "performance";
    }

    @Override
    public Map<String, Object> extract(Page page) {
        try {
            Object evalResult = page.evaluate("""
                () => {
                    const perf = window.performance ? window.performance.timing : null;
                    if (!perf) return { ttfb: 0, dom_interactive: 0, page_load_time: 0 };
                    
                    const navigationStart = perf.navigationStart || 0;
                    return {
                        ttfb: perf.responseStart ? (perf.responseStart - navigationStart) : 0,
                        dom_interactive: perf.domInteractive ? (perf.domInteractive - navigationStart) : 0,
                        page_load_time: perf.loadEventEnd ? (perf.loadEventEnd - navigationStart) : 0
                    };
                }
            """);

            if (evalResult != null) {
                String jsonStr = objectMapper.writeValueAsString(evalResult);
                return objectMapper.readValue(jsonStr, new TypeReference<Map<String, Object>>() {});
            }
        } catch (Exception e) {
            log.error("Performance Extraction error: {}", e.getMessage());
        }
        Map<String, Object> fallback = new HashMap<>();
        fallback.put("ttfb", 0);
        fallback.put("dom_interactive", 0);
        fallback.put("page_load_time", 0);
        return fallback;
    }
}
