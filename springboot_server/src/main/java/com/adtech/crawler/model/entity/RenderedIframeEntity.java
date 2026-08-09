package com.adtech.crawler.model.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "rendered_iframes")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class RenderedIframeEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "crawl_job_id", nullable = false)
    private CrawlJobEntity job;

    @Column(name = "frame_id", nullable = false, length = 255)
    private String frameId;

    @Column(name = "frame_type", length = 128)
    private String frameType;

    @Column(name = "width")
    private Integer width = 0;

    @Column(name = "height")
    private Integer height = 0;

    @Column(name = "is_visible")
    private Boolean isVisible = false;

    @Column(name = "resolved_creative_url", columnDefinition = "TEXT")
    private String resolvedCreativeUrl;

    @Column(name = "ad_clickthrough_url", columnDefinition = "TEXT")
    private String adClickthroughUrl;
}
