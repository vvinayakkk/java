package com.adtech.crawler.model.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "crawl_payloads")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CrawlPayloadEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "crawl_job_id", nullable = false, unique = true)
    private CrawlJobEntity job;

    @Lob
    @Column(name = "raw_json", nullable = false, columnDefinition = "LONGTEXT")
    private String rawJson;
}
