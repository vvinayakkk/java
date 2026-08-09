package com.adtech.crawler.model.dto;

import jakarta.validation.constraints.NotEmpty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class BatchCrawlRequest {

    @NotEmpty(message = "URLs list cannot be empty")
    private List<String> urls;

    private int concurrency = 5;
    private boolean forceRefresh = false;
}
