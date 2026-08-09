# 07 - Crawling Architecture, Strategies & State Control

> **NOTE**: Google Docs Export Version (Formatted for pasting as document tabs).

## Overview
Large-scale web crawling requires robust state management, URL deduplication, crawl tree traversal algorithms, and strict depth control. Without well-designed state engines and crawling strategies, a web crawler will fall into infinite loop traps, crawl duplicate pages, violate host rate limits, or consume excessive system storage.

---

## 33. Crawling State Architecture & Components

A production crawler relies on five fundamental state components:

```mermaid
flowchart TD
    A["CRAWLER STATE ARCHITECTURE"] --> B["URL FRONTIER"]
    A --> C["VISITED SET"]
    A --> D["QUEUE ENGINE"]
    A --> E["DEDUPLICATION ENGINE"]
    A --> F["METADATA STORE"]

    subgraph Frontier["URL Frontier"]
        B1["Discovered URLs"]
        B2["Pending Fetch List"]
        B3["Priority Scoring"]
    end

    subgraph Visited["Visited Set"]
        C1["Hashes of Crawled URLs (SHA256)"]
        C2["Bloom Filters for Fast Lookup"]
    end

    subgraph QueueEng["Queue Engine"]
        D1["Priority Queue (Redis / RabbitMQ)"]
        D2["FIFO / LIFO Task Scheduling"]
    end

    subgraph Dedup["Deduplication Engine"]
        E1["URL Normalization"]
        E2["Canonical Tag Verification"]
        E3["Tracking Parameter Stripping"]
    end

    subgraph Metadata["Metadata Store"]
        F1["HTTP Status Codes & Headers"]
        F2["Depth Level & Parent Source"]
        F3["Response Execution Time"]
    end

    B --- Frontier
    C --- Visited
    D --- QueueEng
    E --- Dedup
    F --- Metadata
```

### Detailed Sub-system Operations
* **URL Frontier**: The centralized repository holding all discovered URLs waiting to be scheduled for fetching.
* **Visited Set & Deduplication**:
  * **Bloom Filters**: High-performance probabilistic data structures used to test set membership in memory with minimal RAM footprint.
  * **URL Normalization**: Standardizing raw URLs before hashing (`HTTP://Example.COM:80/foo/` $\rightarrow$ `http://example.com/foo`).
  * **Canonicalization**: Inspecting HTML `<link rel="canonical" href="...">` tags to collapse multiple URL aliases into a single primary URL.
  * **Tracking Parameter Removal**: Stripping marketing queries (`?utm_source=...`, `?gclid=...`, `?ref=...`) to avoid crawling duplicate pages.
* **Crawl Metadata Tracking**: Recording audit trails for every request (Timestamp, Response Time, Content-Type, Depth Level, Parent Source URL, Error Stack).

---

## 34 & 36. Crawling Hierarchy & Depth Traversal

Web crawlers view the internet as a directed graph where web pages are nodes and hyperlinks are edges.

```mermaid
flowchart TD
    Depth0["Depth 0 (Seed URL)<br/>https://example.com"] --> Depth1_A["Depth 1: /products"]
    Depth0 --> Depth1_B["Depth 1: /about"]
    Depth0 --> Depth1_C["Depth 1: /contact"]

    Depth1_A --> Depth2_A1["Depth 2: /prod/1"]
    Depth1_A --> Depth2_A2["Depth 2: /prod/2"]
    Depth1_A --> Depth2_A3["Depth 2: /prod/3"]

    Depth2_A1 --> Depth3_Rev["Depth 3: /prod/1/reviews"]
    Depth2_A1 --> Depth3_Spec["Depth 3: /prod/1/specs"]
```

---

## 35. Crawl Traversal Strategies

Depending on the business requirements, crawlers deploy different graph traversal strategies:

```mermaid
flowchart TD
    subgraph BFS["BREADTH-FIRST SEARCH (BFS - Level by Level)"]
        Seed1["Seed URL"] --> Level1_A["Page A"]
        Seed1 --> Level1_B["Page B"]
        Level1_A --> Level2_A1["Page A1"]
        Level1_B --> Level2_B1["Page B1"]
    end

    subgraph DFS["DEPTH-FIRST SEARCH (DFS - Deep Traversal)"]
        Seed2["Seed URL"] --> DeepA["Page A"]
        DeepA --> DeepA1["Page A1"]
        DeepA1 --> DeepA1a["Page A1a (Deep Target)"]
    end
```

### Strategy Matrix

| Strategy | Algorithmic Traversal | Primary Operational Benefit |
| :--- | :--- | :--- |
| **Breadth-First Search (BFS)**| Level-by-level queue (FIFO). | Discovers high-level category pages fast; avoids getting stuck in deep URL traps. |
| **Depth-First Search (DFS)**| Stack-based queue (LIFO). | Useful when searching for specific deep nested documents or completing single items fast. |
| **Priority Crawling** | Weighted Priority Queue. | Ranks URLs by importance (e.g., domain authority, update frequency, page rank). |
| **Depth-Limited Crawling**| Max Depth Guard Condition. | Prevents crawlers from going deeper than $N$ levels from the seed URL. |
| **Domain-Restricted** | Domain Regex Whitelist. | Enforces strict host bounds (`allowed_domains = ['example.com']`). |
| **Sitemap Crawling** | Parses `sitemap.xml`. | Direct discovery of structured URLs without relying solely on HTML link parsing. |
| **API-Assisted / Hybrid**| XHR Discovery + HTML Crawl.| Combines backend API endpoint extraction with traditional HTML link following. |
