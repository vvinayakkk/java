package com.adtech.crawler.model.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class CrawlRequest {

    @NotBlank(message = "URL cannot be blank")
    private String url;

    private boolean forceRefresh = false;
}
