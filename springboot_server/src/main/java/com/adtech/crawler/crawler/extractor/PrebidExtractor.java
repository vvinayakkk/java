package com.adtech.crawler.crawler.extractor;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.microsoft.playwright.Page;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import java.util.*;

@Component
@Slf4j
public class PrebidExtractor implements AdTechExtractor {

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public String getName() {
        return "prebid";
    }

    @Override
    @SuppressWarnings("unchecked")
    public Map<String, Object> extract(Page page) {
        Map<String, Object> prebidData = new HashMap<>();
        try {
            Object evalResult = page.evaluate("""
                () => {
                    const detected = typeof pbjs !== 'undefined';
                    const version = detected && pbjs.version ? pbjs.version : null;
                    const winningBids = [];
                    const bidderSummary = [];

                    if (detected) {
                        try {
                            const wins = pbjs.getWinningBids();
                            wins.forEach(w => {
                                winningBids.push({
                                    ad_unit_code: w.adUnitCode,
                                    bidder: w.bidder,
                                    cpm: w.cpm,
                                    currency: w.currency || 'USD',
                                    time_to_respond: w.timeToRespond || 0,
                                    source: 'prebid_client'
                                });
                            });
                        } catch(e){}

                        try {
                            const responses = pbjs.getBidResponses();
                            const summaryMap = {};
                            Object.keys(responses).forEach(code => {
                                const res = responses[code];
                                if (res.bids) {
                                    res.bids.forEach(b => {
                                        const bidder = b.bidder;
                                        if (!summaryMap[bidder]) {
                                            summaryMap[bidder] = { bidder: bidder, bids_count: 0, total_cpm: 0, max_cpm: 0, total_latency: 0 };
                                        }
                                        summaryMap[bidder].bids_count++;
                                        summaryMap[bidder].total_cpm += (b.cpm || 0);
                                        summaryMap[bidder].max_cpm = Math.max(summaryMap[bidder].max_cpm, b.cpm || 0);
                                        summaryMap[bidder].total_latency += (b.timeToRespond || 0);
                                    });
                                }
                            });

                            Object.keys(summaryMap).forEach(k => {
                                const item = summaryMap[k];
                                bidderSummary.push({
                                    bidder: item.bidder,
                                    bids_count: item.bids_count,
                                    max_cpm: item.max_cpm,
                                    avg_cpm: item.bids_count > 0 ? (item.total_cpm / item.bids_count) : 0,
                                    avg_latency_ms: item.bids_count > 0 ? Math.round(item.total_latency / item.bids_count) : 0,
                                    source: 'client_prebid'
                                });
                            });
                        } catch(e){}
                    }

                    return {
                        detected: detected,
                        version: version,
                        winning_bids: winningBids,
                        bidder_summary: bidderSummary
                    };
                }
            """);

            if (evalResult != null) {
                String jsonStr = objectMapper.writeValueAsString(evalResult);
                return objectMapper.readValue(jsonStr, new TypeReference<Map<String, Object>>() {});
            }
        } catch (Exception e) {
            log.error("Prebid Extraction error: {}", e.getMessage());
        }

        prebidData.put("detected", false);
        prebidData.put("version", null);
        prebidData.put("winning_bids", Collections.emptyList());
        prebidData.put("bidder_summary", Collections.emptyList());
        return prebidData;
    }
}
