package com.adtech.crawler.repository;

import com.adtech.crawler.model.entity.CrawlJobEntity;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;

@Repository
public interface CrawlJobRepository extends JpaRepository<CrawlJobEntity, Long> {
    Optional<CrawlJobEntity> findByJobId(String jobId);
    Page<CrawlJobEntity> findAllByOrderByCreatedAtDesc(Pageable pageable);
}
