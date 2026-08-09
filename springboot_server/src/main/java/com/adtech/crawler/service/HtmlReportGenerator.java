package com.adtech.crawler.service;

import org.springframework.stereotype.Service;
import java.util.*;

@Service
public class HtmlReportGenerator {

    @SuppressWarnings("unchecked")
    public String generateHtmlReport(Map<String, Object> data) {
        String targetUrl = (String) data.getOrDefault("target_url", "N/A");
        String jobId = (String) data.getOrDefault("job_id", "N/A");
        
        Map<String, Object> val = (Map<String, Object>) data.getOrDefault("validation", Collections.emptyMap());
        int qualityScore = (int) val.getOrDefault("quality_score", 0);
        String qualityRating = (String) val.getOrDefault("quality_rating", "UNKNOWN");
        
        List<Map<String, Object>> slots = (List<Map<String, Object>>) data.getOrDefault("ad_slots_summary", Collections.emptyList());

        StringBuilder slotsHtml = new StringBuilder();
        for (Map<String, Object> s : slots) {
            Map<String, Integer> dims = (Map<String, Integer>) s.getOrDefault("dimensions", Collections.emptyMap());
            slotsHtml.append(String.format("""
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #333; font-weight: bold; color: #40a9ff;">%s</td>
                    <td style="padding: 10px; border-bottom: 1px solid #333;">%s</td>
                    <td style="padding: 10px; border-bottom: 1px solid #333;">%dx%d</td>
                    <td style="padding: 10px; border-bottom: 1px solid #333;"><span style="background: %s; padding: 3px 8px; border-radius: 4px; font-size: 12px;">%s</span></td>
                    <td style="padding: 10px; border-bottom: 1px solid #333; color: #52c41a; font-weight: bold;">%s</td>
                    <td style="padding: 10px; border-bottom: 1px solid #333;">$%s</td>
                </tr>
            """,
                    s.get("slot_id"),
                    s.get("ad_unit_path"),
                    dims.getOrDefault("width", 0), dims.getOrDefault("height", 0),
                    Boolean.TRUE.equals(s.get("is_visible")) ? "#135200" : "#5c0011",
                    Boolean.TRUE.equals(s.get("is_visible")) ? "VISIBLE" : "HIDDEN",
                    s.get("winning_bidder"),
                    s.get("winning_cpm")
            ));
        }

        return String.format("""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>AdTech Audit Dashboard - %s</title>
                <style>
                    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }
                    .card { background-color: #1e293b; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
                    h1, h2 { margin-top: 0; color: #38bdf8; }
                    .badge { font-size: 24px; font-weight: bold; color: #4ade80; }
                    table { width: 100%%; border-collapse: collapse; margin-top: 10px; }
                    th { text-align: left; background-color: #334155; padding: 12px; color: #94a3b8; }
                </style>
            </head>
            <body>
                <div class="card">
                    <h1>⚡ Forbes AdTech Executive Dashboard (Spring Boot)</h1>
                    <p><strong>Target URL:</strong> <a href="%s" style="color: #38bdf8;" target="_blank">%s</a></p>
                    <p><strong>Crawl Job UUID:</strong> %s</p>
                    <p><strong>Quality Score:</strong> <span class="badge">%d/100 (%s)</span></p>
                </div>

                <div class="card">
                    <h2>🎯 Normalized Ad Slots Summary (%d Slots)</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Slot ID</th>
                                <th>Ad Unit Path</th>
                                <th>Dimensions</th>
                                <th>Visibility</th>
                                <th>Winning Bidder</th>
                                <th>Winning CPM</th>
                            </tr>
                        </thead>
                        <tbody>
                            %s
                        </tbody>
                    </table>
                </div>
            </body>
            </html>
        """, targetUrl, targetUrl, targetUrl, jobId, qualityScore, qualityRating, slots.size(), slotsHtml.toString());
    }
}
