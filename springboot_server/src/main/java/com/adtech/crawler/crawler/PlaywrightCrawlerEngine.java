package com.adtech.crawler.crawler;

import com.adtech.crawler.crawler.extractor.AdTechExtractor;
import com.microsoft.playwright.*;
import com.microsoft.playwright.options.WaitUntilState;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

@Component
@Slf4j
public class PlaywrightCrawlerEngine {

    private final List<AdTechExtractor> extractors;
    private final AdsTxtParser adsTxtParser;
    private final QualityValidator validator;

    public PlaywrightCrawlerEngine(List<AdTechExtractor> extractors, AdsTxtParser adsTxtParser, QualityValidator validator) {
        this.extractors = extractors;
        this.adsTxtParser = adsTxtParser;
        this.validator = validator;
    }

    @SuppressWarnings("unchecked")
    public Map<String, Object> crawl(String targetUrl) {
        log.info("Starting Playwright Java Crawl for URL: {}", targetUrl);
        Map<String, Object> result = new ConcurrentHashMap<>();
        long startTime = System.currentTimeMillis();

        AtomicInteger totalNetworkRequests = new AtomicInteger(0);
        AtomicInteger adTechRequests = new AtomicInteger(0);
        List<String> consoleLogs = Collections.synchronizedList(new ArrayList<>());
        List<String> pageErrors = Collections.synchronizedList(new ArrayList<>());
        Map<String, Integer> networkBiddersCount = new ConcurrentHashMap<>();

        List<String> adTechSignatures = List.of(
                "googletagservices.com", "doubleclick.net", "pagead2.googlesyndication.com",
                "rubiconproject.com", "criteo.com", "amazon-adsystem.com", "adnxs.com",
                "pubmatic.com", "openx.net", "taboola.com", "outbrain.com", "indexww.com"
        );

        try (Playwright playwright = Playwright.create()) {
            Browser browser = playwright.chromium().launch(new BrowserType.LaunchOptions()
                    .setHeadless(true)
                    .setArgs(List.of(
                            "--disable-blink-features=AutomationControlled",
                            "--no-sandbox",
                            "--disable-setuid-sandbox"
                    )));

            BrowserContext context = browser.newContext(new Browser.NewContextOptions()
                    .setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
                    .setViewportSize(1920, 1080)
                    .setJavaScriptEnabled(true));

            Page page = context.newPage();
            page.addInitScript("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});");

            page.onRequest(request -> {
                totalNetworkRequests.incrementAndGet();
                String reqUrl = request.url().toLowerCase();
                for (String sig : adTechSignatures) {
                    if (reqUrl.contains(sig)) {
                        adTechRequests.incrementAndGet();
                        networkBiddersCount.merge(sig, 1, Integer::sum);
                        break;
                    }
                }
            });

            page.onConsoleMessage(msg -> {
                if (consoleLogs.size() < 200) {
                    consoleLogs.add("[" + msg.type() + "] " + msg.text());
                }
            });

            page.onPageError(err -> {
                if (pageErrors.size() < 50) {
                    pageErrors.add(err);
                }
            });

            int httpStatus = 200;
            try {
                Response response = page.navigate(targetUrl, new Page.NavigateOptions()
                        .setWaitUntil(WaitUntilState.DOMCONTENTLOADED)
                        .setTimeout(45000));
                if (response != null) {
                    httpStatus = response.status();
                }
            } catch (Exception e) {
                log.warn("Navigation timeout/warning for {}: {}", targetUrl, e.getMessage());
            }

            handleCmpConsent(page);
            smoothScroll(page);

            Map<String, Object> gptData = Collections.emptyMap();
            Map<String, Object> prebidData = Collections.emptyMap();
            Map<String, Object> domData = Collections.emptyMap();
            Map<String, Object> perfData = Collections.emptyMap();

            for (AdTechExtractor extractor : extractors) {
                Map<String, Object> extracted = extractor.extract(page);
                if ("gpt".equals(extractor.getName())) gptData = extracted;
                else if ("prebid".equals(extractor.getName())) prebidData = extracted;
                else if ("dom".equals(extractor.getName())) domData = extracted;
                else if ("performance".equals(extractor.getName())) perfData = extracted;
            }

            List<Map<String, Object>> adSlotsSummary = buildAdSlotsSummary(gptData, prebidData, domData);
            Map<String, Object> adsTxt = adsTxtParser.fetchAndParse(targetUrl, "ads.txt");
            Map<String, Object> appAdsTxt = adsTxtParser.fetchAndParse(targetUrl, "app-ads.txt");

            browser.close();

            Map<String, Object> networkSummary = new HashMap<>();
            networkSummary.put("total_requests", totalNetworkRequests.get());
            networkSummary.put("adtech_requests", adTechRequests.get());

            List<Map<String, Object>> biddersList = new ArrayList<>();
            networkBiddersCount.forEach((bidder, count) -> {
                Map<String, Object> bItem = new HashMap<>();
                bItem.put("bidder", bidder);
                bItem.put("call_count", count);
                biddersList.add(bItem);
            });
            networkSummary.put("network_bidders", biddersList);

            result.put("target_url", targetUrl);
            result.put("http_status", httpStatus);
            result.put("ad_slots_summary", adSlotsSummary);
            result.put("gpt_status", gptData);
            result.put("header_bidding", prebidData);
            result.put("rendered_iframes", domData.getOrDefault("rendered_iframes", Collections.emptyList()));
            result.put("performance", perfData);
            result.put("network_summary", networkSummary);
            result.put("console_messages", Map.of("logs", consoleLogs, "page_errors", pageErrors));
            result.put("ads_txt", adsTxt);
            result.put("app_ads_txt", appAdsTxt);
            result.put("execution_time_ms", (int) (System.currentTimeMillis() - startTime));

            Map<String, Object> validation = validator.evaluate(result);
            result.put("validation", validation);

            log.info("Crawl Completed for {}. Quality Score: {}/100 ({})",
                    targetUrl, validation.get("quality_score"), validation.get("quality_rating"));

        } catch (Exception e) {
            log.error("Fatal Playwright Crawl exception for {}: {}", targetUrl, e.getMessage(), e);
            result.put("target_url", targetUrl);
            result.put("http_status", 500);
            result.put("error", e.getMessage());
            result.put("ad_slots_summary", Collections.emptyList());
            Map<String, Object> validation = validator.evaluate(result);
            result.put("validation", validation);
        }

        return result;
    }

    private void handleCmpConsent(Page page) {
        String[] selectors = new String[]{
                "#onetrust-accept-btn-handler",
                "button[id*='accept']",
                "button:has-text('Accept')"
        };
        for (String sel : selectors) {
            try {
                Locator loc = page.locator(sel).first();
                if (loc.isVisible()) {
                    loc.click();
                    page.waitForTimeout(1000);
                    break;
                }
            } catch (Exception ignored) {}
        }
    }

    private void smoothScroll(Page page) {
        try {
            page.evaluate("""
                async () => {
                    await new Promise((resolve) => {
                        let totalHeight = 0;
                        const distance = 400;
                        const timer = setInterval(() => {
                            const scrollHeight = document.body.scrollHeight;
                            window.scrollBy(0, distance);
                            totalHeight += distance;
                            if (totalHeight >= scrollHeight || totalHeight >= 4000) {
                                clearInterval(timer);
                                window.scrollTo(0, 0);
                                resolve();
                            }
                        }, 200);
                    });
                }
            """);
        } catch (Exception ignored) {}
    }

    @SuppressWarnings("unchecked")
    private List<Map<String, Object>> buildAdSlotsSummary(Map<String, Object> gptData, Map<String, Object> prebidData, Map<String, Object> domData) {
        List<Map<String, Object>> slots = (List<Map<String, Object>>) gptData.getOrDefault("slots", Collections.emptyList());
        List<Map<String, Object>> winningBids = (List<Map<String, Object>>) prebidData.getOrDefault("winning_bids", Collections.emptyList());
        List<Map<String, Object>> iframes = (List<Map<String, Object>>) domData.getOrDefault("rendered_iframes", Collections.emptyList());

        List<Map<String, Object>> summary = new ArrayList<>();
        for (Map<String, Object> s : slots) {
            String elementId = (String) s.get("element_id");
            String path = (String) s.get("ad_unit_path");
            Boolean isVisible = (Boolean) s.getOrDefault("is_visible", false);

            Map<String, Object> renderedSize = (Map<String, Object>) s.getOrDefault("rendered_size", Collections.emptyMap());
            int width = renderedSize.get("width") != null ? ((Number) renderedSize.get("width")).intValue() : 0;
            int height = renderedSize.get("height") != null ? ((Number) renderedSize.get("height")).intValue() : 0;

            Map<String, Object> winBid = winningBids.stream()
                    .filter(w -> elementId != null && elementId.equals(w.get("ad_unit_code")))
                    .findFirst()
                    .orElse(Collections.emptyMap());

            Map<String, Object> matchedFrame = iframes.stream()
                    .filter(f -> elementId != null && ((String) f.getOrDefault("id", "")).contains(elementId))
                    .findFirst()
                    .orElse(Collections.emptyMap());

            String bidder = (String) winBid.getOrDefault("bidder", "None");
            String monetization = "AD_SERVER_DIRECT";

            if (!"None".equals(bidder) && !"ad_server".equals(bidder)) {
                monetization = "HEADER_BIDDING";
            } else if ("ad_server".equals(bidder)) {
                monetization = "AD_SERVER_DIRECT";
            } else if (!isVisible || (width == 0 && height == 0)) {
                monetization = "UNFILLED_OR_HIDDEN";
            }

            Map<String, Object> slotItem = new HashMap<>();
            slotItem.put("slot_id", elementId);
            slotItem.put("ad_unit_path", path);
            Map<String, Integer> dims = new HashMap<>();
            dims.put("width", width);
            dims.put("height", height);
            slotItem.put("dimensions", dims);
            slotItem.put("declared_sizes", s.getOrDefault("declared_sizes", Collections.emptyList()));
            slotItem.put("is_visible", isVisible);
            slotItem.put("monetization_type", monetization);
            slotItem.put("winning_bidder", bidder);
            slotItem.put("winning_cpm", winBid.getOrDefault("cpm", 0.0));
            slotItem.put("currency", winBid.getOrDefault("currency", "USD"));
            slotItem.put("creative_asset_url", matchedFrame.get("resolved_creative_url"));
            slotItem.put("destination_click_url", matchedFrame.get("ad_clickthrough_url"));

            summary.add(slotItem);
        }
        return summary;
    }
}
