package com.adtech.crawler;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;

@SpringBootApplication
@EnableAsync
public class AdtechCrawlerApplication {

    public static void main(String[] args) {
        SpringApplication.run(AdtechCrawlerApplication.class, args);
    }
}
