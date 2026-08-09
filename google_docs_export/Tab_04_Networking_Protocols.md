# 04 - Networking, Protocols & Interception Layer

> **NOTE**: Google Docs Export Version (Formatted for pasting as document tabs).

## Overview
Web crawlers depend heavily on understanding browser networking infrastructure. Modern web applications do not just fetch flat HTML; they initiate complex transport connections over HTTP/1.1, HTTP/2, and HTTP/3 QUIC, negotiate TLS handshakes, stream persistent data via WebSockets and Server-Sent Events, and load dozens of subresources. Headless browsers provide powerful APIs to intercept, modify, block, and log these network exchanges.

---

## 16. The Network Layer Infrastructure

Browser network communication relies on a layered protocol stack managed by Chromium's Network Service process:

```mermaid
flowchart TD
    A["NETWORK PROTOCOL STACK"] --> B["APPLICATION LAYER"]
    A --> C["TRANSPORT LAYER"]
    A --> D["SECURITY LAYER"]

    subgraph AppLayer["Application Layer Protocols"]
        B1["HTTP/1.1 (Text Header, Pipelining)"]
        B2["HTTP/2 (Binary, Multiplexed Streams)"]
        B3["HTTP/3 (QUIC over UDP)"]
        B4["WebSockets (RFC 6455)"]
        B5["Server-Sent Events (SSE)"]
    end

    subgraph TransportLayer["Transport Layer Protocols"]
        C1["TCP (Three-Way Handshake)"]
        C2["UDP (Datagrams for QUIC)"]
    end

    subgraph SecurityLayer["Security Layer Protocols"]
        D1["TLS 1.2 / TLS 1.3"]
        D2["Certificate Validation"]
        D3["JA3 / TLS Fingerprinting (Client Hello)"]
    end

    B --- AppLayer
    C --- TransportLayer
    D --- SecurityLayer
```

### HTTP Protocol Evolution Matrix

| Protocol Version | Underlying Transport | Multiplexing Model | Header Compression | Head-of-Line Blocking |
| :--- | :--- | :--- | :--- | :--- |
| **HTTP/1.1** | TCP | Sequential (Keep-Alive) | ❌ Plaintext headers | ⚠️ Yes (At HTTP level) |
| **HTTP/2** | TCP | Binary Stream Multiplexing | ✅ HPACK | ⚠️ Yes (At TCP packet level) |
| **HTTP/3** | UDP (QUIC) | Independent QUIC Streams | ✅ QPACK | ✅ Eliminated completely |

---

## 17. The Browser Network Request Spectrum

When a single page load occurs, Chromium generates a spectrum of subresource network requests:

```mermaid
flowchart TD
    PageInit["PAGE INITIALIZATION"] --> HTML["HTML Request (Root Document)"]
    PageInit --> CSS["CSS Stylesheets (Style Recalculation)"]
    PageInit --> JS["JS Scripts (V8 Engine Execution)"]
    PageInit --> Media["Fonts & Images (Paint & Layout Assets)"]
    PageInit --> XHR["XHR / Fetch APIs (Dynamic JSON Payloads)"]
    PageInit --> Stream["Media Streams (HLS / DASH Segments)"]
    PageInit --> WS["WebSockets (Full-Duplex Real-Time Data)"]
    PageInit --> SSE["SSE Streams (Unidirectional Event Streams)"]
```

---

## 25. WebSockets (Full-Duplex Real-Time Data)

WebSockets provide persistent, bidirectional, low-latency TCP communication between client and server (`ws://` or `wss://`).

```mermaid
sequenceDiagram
    autonumber
    actor Client as Browser Client
    participant Server as Remote Server

    Client->>Server: HTTP GET /chat (Headers: Upgrade: websocket)
    Server-->>Client: HTTP 101 Switching Protocols
    Note over Client,Server: ESTABLISHED FULL-DUPLEX WEBSOCKET CONNECTION
    Client->>Server: Text Frame (JSON Payload)
    Server-->>Client: Text Frame (Real-Time Broadcast Data)
```

### Relevance for Crawlers
* Financial portals, crypto exchanges, betting platforms, and live chats broadcast data strictly over WebSockets.
* Automation engines (Playwright/Puppeteer) intercept WebSocket frame events (`page.on('websocket')`) to record real-time data frames directly without parsing HTML.

---

## 26. Server-Sent Events (SSE / EventSource)

Server-Sent Events (SSE) provide a lightweight, unidirectional stream from server to client over standard HTTP (`text/event-stream`).

```mermaid
sequenceDiagram
    autonumber
    actor Client as Browser Client
    participant Server as Remote Server

    Client->>Server: HTTP GET /api/stream
    Server-->>Client: HTTP 200 OK (Content-Type: text/event-stream)
    Note over Client,Server: PERSISTENT UNIDIRECTIONAL HTTP STREAM
    Server-->>Client: event: price_update | data: {"symbol": "AAPL", "price": 185.50}
    Server-->>Client: event: price_update | data: {"symbol": "AAPL", "price": 186.10}
```

---

## 47. Subresource Loading Lifecycle

Browser engines prioritize subresource loads based on resource type and viewport position:

| Priority Level | Resource Types | Loading Behavior |
| :--- | :--- | :--- |
| **Priority 1 (Highest)** | Main HTML Document, Synchronous `<script>`, CSS Stylesheets | Blocks rendering until downloaded and parsed. |
| **Priority 2 (High)** | Visible Viewport Images, Fonts, Active XHR/Fetch requests | Scheduled immediately for painting and data injection. |
| **Priority 3 (Medium)** | Async / Defer JavaScript files | Downloaded in background without blocking DOM parsing. |
| **Priority 4 (Low)** | Offscreen Below-the-Fold Images, Analytics scripts | Delayed until main network idle or scroll trigger. |

---

## 49. Network Interception & Request Routing

Network Interception allows automation tools to sit directly inside Chromium's network layer to observe, modify, block, or mock network requests.

```mermaid
flowchart TD
    Script["Automation Script<br/>(Playwright / CDP)"] --> Listen["Listens to Network.requestIntercepted"]

    Renderer["Renderer Process Request"] --> Interceptor["Network Interceptor"]

    Interceptor --> OptionA["PASS / MODIFY<br/>- Alter Request Headers<br/>- Inject Bearer Auth Token<br/>- Modify POST Payload data"]
    Interceptor --> OptionB["BLOCK / MOCK<br/>- Block heavy images/fonts<br/>- Return cached JSON mock payload<br/>- Prevent analytics tracking"]

    OptionA --> Server["Remote Server"]
    OptionB --> LocalReturn["Immediate Local Response"]
```

### Strategic Use Cases for Scrapers
1. **Performance & Speed Optimization**: Blocking media assets (`.png`, `.jpg`, `.mp4`, `.woff2`) reduces bandwidth by 80% and increases page crawl speed by 3x–5x.
2. **API Data Extraction**: Capturing background XHR/Fetch JSON responses directly (`response.json()`) eliminates the need to scrape HTML altogether.
3. **Authentication Injection**: Automatically appending custom authorization headers (`Authorization: Bearer <token>`) or custom cookies to outgoing requests.
4. **Bypassing Bot Blockers**: Filtering or modifying headers (`User-Agent`, `Sec-Ch-Ua`) to ensure browser request signatures match expected profiles.
