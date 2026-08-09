package com.adtech.crawler.repository;

import com.adtech.crawler.model.entity.CrawlPayloadEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;

@Repository
public interface CrawlPayloadRepository extends JpaRepository<CrawlPayloadEntity, Long> {
    Optional<CrawlPayloadEntity> findByJobId(Long jobId);
}
