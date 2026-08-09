package com.adtech.crawler.crawler;

import lombok.extern.slf4j.Slf4j;
import org.jsoup.Jsoup;
import org.springframework.stereotype.Component;

import java.net.URI;
import java.util.*;

@Component
@Slf4j
public class AdsTxtParser {

    public Map<String, Object> fetchAndParse(String targetUrl, String filename) {
        Map<String, Object> result = new HashMap<>();
        try {
            URI uri = new URI(targetUrl);
            String baseUrl = uri.getScheme() + "://" + uri.getHost();
            String fullUrl = baseUrl + "/" + filename;

            log.info("Fetching {} from: {}", filename, fullUrl);
            String content = Jsoup.connect(fullUrl)
                    .timeout(10000)
                    .ignoreContentType(true)
                    .execute()
                    .body();

            if (content != null && !content.isEmpty()) {
                int directCount = 0;
                int resellerCount = 0;
                String[] lines = content.split("\n");
                for (String line : lines) {
                    String trimmed = line.trim();
                    if (trimmed.isEmpty() || trimmed.startsWith("#")) continue;
                    String upper = trimmed.toUpperCase();
                    if (upper.contains("DIRECT")) directCount++;
                    else if (upper.contains("RESELLER")) resellerCount++;
                }

                result.put("exists", true);
                result.put("url", fullUrl);
                result.put("total_records", directCount + resellerCount);
                result.put("direct_partners", directCount);
                result.put("reseller_partners", resellerCount);
                return result;
            }
        } catch (Exception e) {
            log.warn("Could not fetch {}: {}", filename, e.getMessage());
        }

        result.put("exists", false);
        result.put("url", null);
        result.put("total_records", 0);
        result.put("direct_partners", 0);
        result.put("reseller_partners", 0);
        return result;
    }
}
