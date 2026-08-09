package com.adtech.crawler.model.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "ad_slots")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class AdSlotEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "crawl_job_id", nullable = false)
    private CrawlJobEntity job;

    @Column(name = "slot_id", nullable = false, length = 255)
    private String slotId;

    @Column(name = "ad_unit_path", length = 512)
    private String adUnitPath;

    @Column(name = "width")
    private Integer width = 0;

    @Column(name = "height")
    private Integer height = 0;

    @Column(name = "declared_sizes", columnDefinition = "TEXT")
    private String declaredSizes;

    @Column(name = "is_visible")
    private Boolean isVisible = false;

    @Column(name = "monetization_type", length = 64)
    private String monetizationType = "UNKNOWN";

    @Column(name = "winning_bidder", length = 128)
    private String winningBidder = "None";

    @Column(name = "winning_cpm")
    private Double winningCpm = 0.0;

    @Column(name = "currency", length = 16)
    private String currency = "USD";

    @Column(name = "creative_asset_url", columnDefinition = "TEXT")
    private String creativeAssetUrl;

    @Column(name = "destination_click_url", columnDefinition = "TEXT")
    private String destinationClickUrl;
}
