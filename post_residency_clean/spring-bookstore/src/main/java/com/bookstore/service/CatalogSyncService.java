package com.bookstore.service;

import com.bookstore.entity.Book;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

/**
 * Simulates a downstream catalog / search-index sync after a book is created.
 * Disabled by default. Use app.catalog-sync.async=false to measure blocking latency (Day 6 baseline),
 * then async=true for the redesigned non-blocking path.
 */
@Service
public class CatalogSyncService {

    private static final Logger log = LoggerFactory.getLogger(CatalogSyncService.class);

    @Value("${app.catalog-sync.enabled:false}")
    private boolean enabled;

    @Value("${app.catalog-sync.delay-ms:0}")
    private long delayMs;

    /** Blocking sync — used when app.catalog-sync.async=false */
    public void syncAfterCreate(Book book) {
        doSync(book);
    }

    /** Non-blocking sync — used when app.catalog-sync.async=true */
    @Async("taskExecutor")
    public void syncAfterCreateAsync(Book book) {
        doSync(book);
    }

    private void doSync(Book book) {
        if (!enabled) {
            return;
        }

        log.info("Starting catalog sync for book id={} isbn={} (delayMs={}) thread={}",
                book.getId(), book.getIsbn(), delayMs, Thread.currentThread().getName());

        if (delayMs > 0) {
            try {
                Thread.sleep(delayMs);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                log.warn("Catalog sync interrupted for book id={}", book.getId());
                return;
            }
        }

        log.info("Completed catalog sync for book id={}", book.getId());
    }
}