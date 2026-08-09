package com.adtech.crawler.crawler.extractor;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.microsoft.playwright.Frame;
import com.microsoft.playwright.Page;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import java.util.*;

@Component
@Slf4j
public class DomExtractor implements AdTechExtractor {

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public String getName() {
        return "dom";
    }

    @Override
    @SuppressWarnings("unchecked")
    public Map<String, Object> extract(Page page) {
        Map<String, Object> domData = new HashMap<>();
        try {
            Object evalResult = page.evaluate("""
                () => {
                    const title = document.title || '';
                    const canonicalEl = document.querySelector('link[rel="canonical"]');
                    const canonicalUrl = canonicalEl ? canonicalEl.href : window.location.href;
                    const bodyTextSample = document.body ? document.body.innerText.substring(0, 500) : '';

                    const iframes = Array.from(document.querySelectorAll('iframe'));
                    const iframeDetails = iframes.map((f, index) => {
                        const rect = f.getBoundingClientRect();
                        let src = f.src || f.getAttribute('data-src') || 'about:blank';
                        const id = f.id || `iframe-${index}`;
                        const name = f.name || '';
                        
                        return {
                            id: id,
                            name: name,
                            src: src,
                            frame_type: 'Standard Frame',
                            resolved_creative_url: null,
                            ad_clickthrough_url: null,
                            width: Math.round(rect.width),
                            height: Math.round(rect.height),
                            is_visible: rect.width > 0 && rect.height > 0 && window.getComputedStyle(f).display !== 'none'
                        };
                    });

                    return {
                        title: title,
                        canonical_url: canonicalUrl,
                        final_url: window.location.href,
                        body_sample: bodyTextSample,
                        rendered_iframes: iframeDetails
                    };
                }
            """);

            if (evalResult != null) {
                String jsonStr = objectMapper.writeValueAsString(evalResult);
                domData = objectMapper.readValue(jsonStr, new TypeReference<Map<String, Object>>() {});
            }

            List<Map<String, Object>> iframes = (List<Map<String, Object>>) domData.getOrDefault("rendered_iframes", new ArrayList<>());
            for (Map<String, Object> iframeInfo : iframes) {
                String frameId = (String) iframeInfo.get("id");
                String frameName = (String) iframeInfo.get("name");

                Frame matchedFrame = null;
                for (Frame fr : page.frames()) {
                    if ((frameName != null && frameName.equals(fr.name())) || 
                        (fr.name() != null && frameId != null && fr.name().contains(frameId))) {
                        matchedFrame = fr;
                        break;
                    }
                }

                if (matchedFrame != null) {
                    try {
                        Object innerAssetsObj = matchedFrame.evaluate("""
                            () => {
                                const images = Array.from(document.querySelectorAll('img[src]')).map(i => i.src);
                                const links = Array.from(document.querySelectorAll('a[href]')).map(a => a.href);
                                return {
                                    creative_image_url: images.length > 0 ? images[0] : null,
                                    ad_clickthrough_url: links.length > 0 ? links[0] : null
                                };
                            }
                        """);
                        if (innerAssetsObj != null) {
                            String innerStr = objectMapper.writeValueAsString(innerAssetsObj);
                            Map<String, Object> assets = objectMapper.readValue(innerStr, new TypeReference<Map<String, Object>>() {});
                            if (assets.get("creative_image_url") != null || assets.get("ad_clickthrough_url") != null) {
                                iframeInfo.put("resolved_creative_url", assets.get("creative_image_url"));
                                iframeInfo.put("ad_clickthrough_url", assets.get("ad_clickthrough_url"));
                                iframeInfo.put("frame_type", "Friendly IFrame (Creative Rendered)");
                            }
                        }
                    } catch (Exception ignored) {}
                }
            }
            return domData;
        } catch (Exception e) {
            log.error("DOM Extraction error: {}", e.getMessage());
        }
        return domData;
    }
}
