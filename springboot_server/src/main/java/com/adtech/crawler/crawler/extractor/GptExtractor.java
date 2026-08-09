package com.adtech.crawler.crawler.extractor;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.microsoft.playwright.Page;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import java.util.*;

@Component
@Slf4j
public class GptExtractor implements AdTechExtractor {

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public String getName() {
        return "gpt";
    }

    @Override
    @SuppressWarnings("unchecked")
    public Map<String, Object> extract(Page page) {
        Map<String, Object> gptData = new HashMap<>();
        try {
            Object evalResult = page.evaluate("""
                () => {
                    if (typeof googletag === 'undefined' || !googletag.apiReady) {
                        return { loaded: false, slots: [], publisher_ids: [] };
                    }
                    const pubIds = new Set();
                    const slotsInfo = [];
                    try {
                        const slots = googletag.pubads().getSlots();
                        slots.forEach(slot => {
                            const path = slot.getAdUnitPath();
                            const elementId = slot.getSlotElementId();
                            
                            const match = path.match(/\\/(\\d+)\\//);
                            if (match) pubIds.add(match[1]);

                            const declared = [];
                            try {
                                const sizes = slot.getSizes();
                                sizes.forEach(s => {
                                    if (typeof s === 'object' && s.getWidth) {
                                        declared.push(s.getWidth() + 'x' + s.getHeight());
                                    }
                                });
                            } catch(e){}

                            let isVisible = false;
                            let renderedSize = { width: 0, height: 0 };
                            const el = document.getElementById(elementId);
                            if (el) {
                                const rect = el.getBoundingClientRect();
                                isVisible = rect.width > 0 && rect.height > 0 && window.getComputedStyle(el).display !== 'none';
                                renderedSize = { width: Math.round(rect.width), height: Math.round(rect.height) };
                            }

                            slotsInfo.push({
                                element_id: elementId,
                                ad_unit_path: path,
                                declared_sizes: declared,
                                rendered_size: renderedSize,
                                is_visible: isVisible
                            });
                        });
                    } catch(e){}

                    return {
                        loaded: true,
                        slots: slotsInfo,
                        publisher_ids: Array.from(pubIds)
                    };
                }
            """);

            if (evalResult != null) {
                String jsonStr = objectMapper.writeValueAsString(evalResult);
                return objectMapper.readValue(jsonStr, new TypeReference<Map<String, Object>>() {});
            }
        } catch (Exception e) {
            log.error("GPT Extraction error: {}", e.getMessage());
        }

        gptData.put("loaded", false);
        gptData.put("slots", Collections.emptyList());
        gptData.put("publisher_ids", Collections.emptyList());
        return gptData;
    }
}
