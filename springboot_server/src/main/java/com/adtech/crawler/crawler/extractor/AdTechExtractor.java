package com.adtech.crawler.crawler.extractor;

import com.microsoft.playwright.Page;
import java.util.Map;

public interface AdTechExtractor {
    String getName();
    Map<String, Object> extract(Page page);
}
