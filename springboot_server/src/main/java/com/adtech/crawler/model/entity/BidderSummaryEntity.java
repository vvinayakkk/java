package com.adtech.crawler.model.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "bidder_summaries")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class BidderSummaryEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "crawl_job_id", nullable = false)
    private CrawlJobEntity job;

    @Column(name = "bidder_code", nullable = false, length = 128)
    private String bidderCode;

    @Column(name = "bids_count")
    private Integer bidsCount = 0;

    @Column(name = "max_cpm")
    private Double maxCpm = 0.0;

    @Column(name = "avg_cpm")
    private Double avgCpm = 0.0;

    @Column(name = "avg_latency_ms")
    private Integer avgLatencyMs = 0;

    @Column(name = "source", length = 64)
    private String source = "client_prebid";
}
