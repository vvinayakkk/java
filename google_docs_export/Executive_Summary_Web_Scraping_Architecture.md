# Executive Master Architecture & Deep Technical Specification: Web Scraping, Browser Automation & Anti-Bot Evasion

> **Document Type**: Single Master Architectural Specification & Reference Manual.  
> **Target Audience**: Lead Data Engineers, Systems Architects, and Security Researchers.  
> **Format**: Text-Only Specification with AI Image Generation Prompts (Zero Mermaid blocks).  
> **Scope**: Complete end-to-end breakdown of web data acquisition, browser internals, multi-process Chromium architecture, Browser Context isolation, document rendering, networking protocols, framework ecosystem evaluation (Pros & Cons), Playwright supremacy deep-dive, 5-layer anti-bot evasion stack, and maximum volume ad-tech data extraction.

---

## 1. Web Data Acquisition Paradigms & Core Mechanics

> 🎨 **AI Image Generation Prompt (Copy & Paste for GPT / Midjourney)**:  
> *"A sleek modern tech architecture diagram illustrating Web Data Acquisition divided into Crawling (Discovery & Navigation) and Scraping (Parsing & Data Extraction), connected to an end-to-end automated pipeline. Professional dark mode UI design, neon blue and violet accents, high resolution, clean typography."*

### 1.1 Web Scraping (Data Extraction Layer)
* **Definition**: The passive or targeted phase of data acquisition that parses already-retrieved HTML/XML/JSON payloads into clean, structured schemas.
* **Core Operations**: Constructing DOM tree representations, executing CSS selectors / XPath expressions, normalizing text, decoding HTML entities (`&amp;`, `&lt;`), extracting tabular data (`<table>`), pulling anchor links (`<a href="...">`), and harvesting metadata (`data-*`, `meta`, Open Graph).
* **Execution Boundary**: Operates directly on static markup strings; does **not** execute client-side JavaScript, compute CSS layouts, or fire browser lifecycle events.

### 1.2 Web Crawling (Discovery & Navigation Layer)
* **Definition**: The active, stateful traversal of web hyperlink graphs to discover URLs, manage navigation pipelines, handle network transport dynamics, and preserve session state.
* **Core Operations**: Outbound link discovery, URL Frontier priority queue scheduling, visited URL deduplication (Bloom filters), `robots.txt` rate limit enforcement, pagination handling ("Next Page", `?page=N`), HTTP redirect resolution (`301`, `302`), and authentication token preservation.

### 1.3 Traditional HTTP Scraping vs. Headless Browser Crawling

> 🎨 **AI Image Generation Prompt (Copy & Paste for GPT / Midjourney)**:  
> *"A comparison infographic comparing Traditional HTTP Scraping vs Headless Browser Crawling. Left side shows simple HTTP GET request to a web server returning static HTML. Right side shows a Playwright control protocol managing a full Chromium engine with V8 JavaScript & Blink layout engines rendering live DOM trees. Modern dark theme, tech diagram style."*

### 1.4 Architectural Comparison Matrix

| Feature / Dimension | Traditional HTTP Crawling | Headless Browser Crawling |
| :--- | :--- | :--- |
| **Execution Model** | Single HTTP Request-Response exchange. | Full OS-level process lifecycle execution (Blink + V8 engines). |
| **JavaScript Execution** | ❌ None | ✅ Full V8/SpiderMonkey JS engine execution. |
| **DOM Tree Generation** | ❌ Raw HTML string only (Static). | ✅ Dynamic, live, mutable DOM representation. |
| **Network Requests Made** | 1 request per target document. | 50–200+ sub-requests per page (CSS, JS, Fonts, Images, XHR/Fetch). |
| **Memory Footprint** | Extremely low (~5MB–20MB per worker thread). | Heavy (~150MB–500MB+ per browser context/process). |
| **CPU Overhead** | Minimal (I/O bound parsing). | High (CPU bound rendering, layout calculation, JS JIT). |
| **Crawl Throughput** | Thousands of pages per minute per core. | Tens of pages per minute per core. |
| **Anti-Bot Susceptibility**| High (easily flagged by missing browser headers/TLS fingerprints). | Low-to-Moderate (presents real browser signatures, though CDP flags exist). |
| **API / Resource Interception**| Limited to raw HTTP response parsing. | Native network interception, request blocking, response mocking. |

### 1.5 When Headless Browser Crawling Is Essential vs. Traditional Scraping
* **Headless Browsers Required**: JavaScript-heavy Single Page Applications (React, Vue, Angular, Svelte), client-side pre-rendered hydration, interactive content triggers (clicks, accordions), infinite scroll feeds (`IntersectionObserver`), canvas/WebGL rendering, and client-side payload encryption inside V8.
* **Traditional HTTP Superior**: Static HTML pages, server-side rendered (SSR) blogs/news sites, reverse-engineered internal REST/GraphQL APIs, ultra-large-scale crawling (millions of pages), and bandwidth-constrained environments.

### 1.6 Infrastructure Resource Cost & Performance Tradeoffs

> 🎨 **AI Image Generation Prompt (Copy & Paste for GPT / Midjourney)**:  
> *"A side-by-side technical resource gauge comparison. On the left: Traditional HTTP Scraper showing 2% CPU usage, 15MB RAM, 100 req/sec throughput. On the right: Headless Browser Crawler showing 45% CPU usage, 350MB RAM, 2-5 req/sec throughput. Clean corporate dashboard UI, dark background with glowing metrics."*

### 1.7 The Core Data Acquisition Mental Model
> **`Crawler`** $\rightarrow$ **`Playwright Automation API`** $\rightarrow$ **`Chromium Engine`** $\rightarrow$ **`Browser Context`** $\rightarrow$ **`Page`** $\rightarrow$ **`Network + HTML/CSS/JS`** $\rightarrow$ **`Live DOM Tree`** $\rightarrow$ **`Playwright Locators / API Interception`** $\rightarrow$ **`Structured Data`**

---

## 2. Browser Architecture, Engine Mechanics & Object Model Hierarchy

> 🎨 **AI Image Generation Prompt (Copy & Paste for GPT / Midjourney)**:  
> *"A top-down architectural hierarchy diagram of modern browser automation. Top node: Automation API (Playwright), branching to Browser Instance (Chromium Process), which branches to multiple Browser Contexts (Incognito Profiles), then Page Tabs, Main Frame & iframes, and finally live DOM Element nodes. Tech flowchart, glassmorphism UI."*

### 2.1 Scope of Headless Browser Capabilities
Automation APIs control the full capabilities of modern browser binaries:
* **Web Storage**: Cookies (Session/Persistent), LocalStorage (Origin Scope), SessionStorage (Tab Scope), IndexedDB (B-Tree Database), Cache API.
* **Data Protocols**: HTTP/1.1, HTTP/2, HTTP/3 QUIC, Fetch/XHR APIs, WebSockets (RFC 6455), Server-Sent Events (SSE).
* **UI & Interaction**: Synthetic mouse/keyboard/touch events, form controls, file uploads/downloads, native alert/confirm modals, OOPIF iframe traversal, permissions, geolocation.

### 2.2 Chromium Core Engines (Blink, V8, Skia)

> 🎨 **AI Image Generation Prompt (Copy & Paste for GPT / Midjourney)**:  
> *"A tri-engine technical architecture schematic showing Chromium's 3 core engines: Blink (Rendering Engine for HTML/CSS Layout), V8 (JavaScript JIT Engine for Bytecode execution), and Skia (Graphics Engine for 2D Canvas & GPU rasterization). Dark futuristic cyber design."*

### 2.3 Chromium Multi-Process Architecture

> 🎨 **AI Image Generation Prompt (Copy & Paste for GPT / Midjourney)**:  
> *"A multi-process software architecture diagram of Chromium. Central node: Browser Process (Manager), connected via Mojo IPC to Renderer Process 1, Renderer Process 2, GPU Process, Network Service Process, and Storage Service Process. Clean system architecture block diagram, dark theme."*

1. **Browser Process**: Manages application lifecycle, address bar, tab coordination, process creation, security permissions, and IPC message routing.
2. **Renderer Process**: Runs inside an OS-level sandbox. Executes Blink (HTML/CSS parsing) and V8 (JavaScript execution). Spawns separate processes per domain (Site Isolation).
3. **GPU Process**: Receives drawing commands from renderer processes and composites graphics onto screen buffers using DirectX, OpenGL, Vulkan, or Metal.
4. **Network Service**: Handles network requests, socket pools, HTTP/1/2/3 protocols, SSL/TLS handshakes, and caching.
5. **Storage Service**: Handles isolated disk I/O, IndexedDB transactions, and LevelDB database persistence.

### 2.4 Browser Context Isolation (In-Memory Profiles & Scaling Optimization)
A **Browser Context** represents an isolated, in-memory browser profile (equivalent to an Incognito session).

> 🎨 **AI Image Generation Prompt (Copy & Paste for GPT / Midjourney)**:  
> *"An isolated profile architecture diagram showing a single Chromium Browser Process hosting multiple isolated Browser Contexts (Profile 1 & Profile 2), each containing independent Cookies, LocalStorage, IndexedDB databases, and Page Tabs without spawning new browser binaries. High-end technical blueprint design."*

> **IMPORTANT**: **Key Optimization Rule**: `New Browser Context ≠ New Chromium Process`.  
> Creating a new Browser Context takes **milliseconds** and negligible RAM (~15MB) because it reuses the existing Chromium Browser process, GPU process, and Network Service while creating isolated state containers.

### 2.5 Frame, iframe & Out-Of-Process iframe (OOPIF) Mechanics
A **Frame** represents a document execution context. A Page contains one **Main Frame** and optional child `<iframe>` elements:
* **Same-Origin `<iframe>`**: Shares execution limits; parent scripts can directly inspect `iframe.contentDocument`.
* **Cross-Origin `<iframe>` (OOPIF)**: Rendered in a completely separate OS Renderer Process for security. Parent scripts cannot read cross-origin iframe DOM without explicit `postMessage` permissions.

### 2.6 Browser Context Isolation vs. Domain Isolation

> 🎨 **AI Image Generation Prompt (Copy & Paste for GPT / Midjourney)**:  
> *"A comparison diagram showing Domain/Origin Isolation enforced by Same-Origin Policy within one context vs Browser Context Isolation enforced between multiple incognito profiles. Dark blue tech aesthetic, sharp diagram vectors."*

---

## 3. Document Processing, Rendering Pipeline & Client Execution

### 3.1 The Document Object Model (DOM)

> 🎨 **AI Image Generation Prompt (Copy & Paste for GPT / Midjourney)**:  
> *"A clean tree diagram visualizing the Document Object Model (DOM). Root node Document branching to html, body, div.product, h1 title, and button.buy nodes. Modern web development architecture illustration."*

### 3.2 HTML Processing & Dynamic HTML Rendering

> 🎨 **AI Image Generation Prompt (Copy & Paste for GPT / Midjourney)**:  
> *"A flowchart contrasting Static HTML Parsing vs Dynamic Client-Side Rendering (CSR). Top row shows initial HTML payload parsing into fixed DOM. Bottom row shows initial skeleton shell <div id='root'> executing JS Fetch APIs to dynamically insert nodes into a live DOM tree."*

### 3.3 V8 JavaScript Engine Runtime & Async Event Loop

> 🎨 **AI Image Generation Prompt (Copy & Paste for GPT / Midjourney)**:  
> *"A technical pipeline diagram of V8 JavaScript compilation: JS Source Code -> AST Parser -> Ignition Interpreter -> Bytecode -> TurboFan JIT Compiler -> Native Machine Code Execution. Dark neon developer diagram."*

### 3.4 The 8-Stage Browser Rendering Pipeline

> 🎨 **AI Image Generation Prompt (Copy & Paste for GPT / Midjourney)**:  
> *"An 8-stage linear browser rendering pipeline flowchart: 1. HTML Payload -> 2. HTML Parsing (DOM) -> 3. CSS Parsing (CSSOM) -> 4. Style Recalculation -> 5. Layout/Reflow -> 6. Paint -> 7. GPU Rasterization -> 8. Compositing Screen Draw. Vibrant cyan and purple step diagram."*

### 3.5 Web Navigation Mechanics & SPA Routing

> 🎨 **AI Image Generation Prompt (Copy & Paste for GPT / Midjourney)**:  
> *"A diagram illustrating 3 web navigation types: 1. Hard Server Navigation (Full page refresh), 2. Client-Side SPA Navigation (window.history.pushState with in-place DOM updates), 3. Hash Navigation (#section smooth scroll)."*

---

## 4. Networking, Transport Protocols & Interception Layer

### 4.1 Protocol Stack Infrastructure

> 🎨 **AI Image Generation Prompt (Copy & Paste for GPT / Midjourney)**:  
> *"A layered protocol stack diagram for modern web browsers. Top layer: Application Protocols (HTTP/1.1, HTTP/2 multiplexed, HTTP/3 QUIC, WebSockets, SSE). Middle layer: Transport Protocols (TCP & UDP). Bottom layer: Security (TLS 1.3 & JA4 Fingerprinting). Dark glassmorphism tech stack."*

### 4.2 WebSockets (Full-Duplex Real-Time Data)

> 🎨 **AI Image Generation Prompt (Copy & Paste for GPT / Midjourney)**:  
> *"A sequence diagram depicting WebSocket protocol handshake: Client sends HTTP GET Upgrade header -> Server responds 101 Switching Protocols -> Bidirectional real-time text/JSON frames streaming continuously over TCP."*

### 4.3 Network Interception & Request Routing (`page.route()`)

> 🎨 **AI Image Generation Prompt (Copy & Paste for GPT / Midjourney)**:  
> *"A network interception architecture diagram. Script attaches page.route handler -> Intercepts Renderer Process requests -> Path A: Pass/Modify request headers & auth tokens -> Path B: Block heavy assets & return cached mock JSON. Dark cybersecurity network diagram."*

---

## 5. Storage Engines, Browser State & Security Isolation

### 5.1 Cookie Storage Engine & Security Flags
Cookies are attached to HTTP headers (`Cookie:` request header and `Set-Cookie:` response header) managed strictly by Chromium's Network Service.

```http
Set-Cookie: session_id=xyz123; Domain=.example.com; Path=/; Secure; HttpOnly; SameSite=Lax; Max-Age=86400
```

| Flag / Attribute | Functional Behavior & Scraper Impact |
| :--- | :--- |
| **Domain** | Specifies which host domains can receive the cookie (e.g., `.example.com` includes all subdomains). |
| **Path** | Restricts cookie transmission to specific URL paths (e.g., `/app`). |
| **Expires / Max-Age** | Session cookie (deleted when context closes) vs. Persistent cookie (persisted until timestamp). |
| **Secure** | Restricts cookie transmission strictly to encrypted `https://` connections. |
| **HttpOnly** | Blocks JavaScript (`document.cookie`) access. Prevents XSS theft, but scrapers cannot read it via evaluate. |
| **SameSite=Strict** | Cookie is never sent in cross-site requests (e.g., following an external link). |
| **SameSite=Lax** | Default setting. Sent on top-level navigation GET requests, but blocked on cross-site POSTs. |
| **SameSite=None** | Cookie sent on all cross-site requests (requires `Secure` flag). |

### 5.2 Storage Matrix

> 🎨 **AI Image Generation Prompt (Copy & Paste for GPT / Midjourney)**:  
> *"A grid matrix comparing browser client-side storage engines: LocalStorage (Key-value 10MB limit), SessionStorage (Tab-scoped), IndexedDB (NoSQL B-Tree database), Cache API (Service Worker responses), and HTTP Cookies (Header-attached with HttpOnly & SameSite flags). High tech infographic."*

### 5.3 The 7-Level Browser Isolation Pyramid

> 🎨 **AI Image Generation Prompt (Copy & Paste for GPT / Midjourney)**:  
> *"A 7-level security pyramid diagram showing browser isolation boundaries from bottom to top: Level 1: Site Isolation -> Level 2: Same-Origin Policy -> Level 3: Cookie Isolation -> Level 4: Browser Context Isolation -> Level 5: Renderer Process Isolation -> Level 6: OS Process Isolation -> Level 7: OS Sandbox. Glowing pyramid UI design."*

---

## 6. Dynamic Web Applications & UI Interaction Automation

### 6.1 Synthetic User Interactions

> 🎨 **AI Image Generation Prompt (Copy & Paste for GPT / Midjourney)**:  
> *"An event dispatching engine diagram for browser automation. Central Automation Dispatcher branching to Pointer/Mouse Actions (clicks, Bézier curve trails), Keyboard Input (typing cadence), and System Operations (file upload pickers & alert dialogs)."*

### 6.2 CSR vs. SSR & Client Hydration

> 🎨 **AI Image Generation Prompt (Copy & Paste for GPT / Midjourney)**:  
> *"A comparison infographic of CSR (React SPA empty div shell + client fetch) vs SSR + Hydration (Next.js pre-rendered HTML + static script hydration). Modern web development diagram."*

---

## 7. Crawling System Design, Traversal Strategies & State Control

### 7.1 Crawler State Architecture

> 🎨 **AI Image Generation Prompt (Copy & Paste for GPT / Midjourney)**:  
> *"A high-scale web crawler state architecture diagram displaying URL Frontier (Priority Queue), Visited Set (SHA256 Bloom Filters), Queue Engine (Redis/RabbitMQ), Deduplication Engine, and Crawl Audit Metadata Store."*

---

## 8. Automation Framework Ecosystem & Playwright Deep-Dive

### 8.1 Complete Automation Framework Matrix & Pros/Cons Analysis

| Tool / Framework | Primary Architecture | Supported Browsers | Async Paradigm | Primary Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Playwright** | Direct IPC via CDP / Firefox / WebKit protocols | Chromium, Firefox, WebKit | Native `async/await` (Node, Python, Java, .NET) | Modern gold standard for dynamic web scraping, UI testing, and API interception. |
| **Puppeteer** | Direct Chrome DevTools Protocol (CDP) | Chromium, Chrome | JS Promises / `async/await` (Node.js) | Native Chrome automation maintained by Google; fast Node.js scraper setups. |
| **Selenium** | W3C WebDriver Protocol over HTTP REST | Chrome, Firefox, Edge, Safari | Language-dependent (Python, Java, C#, Ruby) | Legacy cross-browser automation; enterprise grid testing infrastructure. |
| **Cypress** | In-Browser Execution Proxy | Chromium, Firefox | Async Chained Commands (JS) | Front-end web application testing; restricted for general-purpose crawling. |
| **Scrapy** | Twisted Event-Driven Networking | None (Pure HTTP client) | Async Event Loop (Python) | High-throughput HTTP crawling; combined with Playwright for dynamic rendering. |

### 8.2 Detailed Framework Breakdown: Pros & Cons

#### 1. Playwright
* **Pros**: Multi-browser support (Chromium, Firefox, WebKit), fast isolated browser contexts (~15MB RAM), native auto-waiting, built-in network interception (`page.route()`), native auth state storage (`storageState()`), multi-language APIs (Python, JS, Java, .NET), visual time-travel Trace Viewer.
* **Cons**: Higher CPU/RAM usage than raw HTTP clients.

#### 2. Puppeteer
* **Pros**: Native Chrome DevTools Protocol (CDP) access, lightweight footprint for Node.js scripts, excellent screenshot and PDF rendering.
* **Cons**: Restricted to Node.js; WebKit unsupported; lacks built-in auto-waiting for complex UI elements.

#### 3. Selenium WebDriver
* **Pros**: Large legacy enterprise ecosystem, native Safari browser support, Selenium Grid for distributed machine clusters.
* **Cons**: Slower execution over HTTP REST protocol; manual `WebDriverWait` boilerplate required; heavy session isolation (requires spinning up full browser binaries).

#### 4. Cypress
* **Pros**: Outstanding developer experience for front-end testing; real-time visual DOM debugging.
* **Cons**: Unsuitable for general web crawling; strict cross-origin navigation restrictions; heavy local test overhead.

#### 5. Scrapy
* **Pros**: Unmatched HTTP speed and throughput; built-in pipelines for URL scheduling, middleware, proxy rotation, and CSV/JSON/Parquet exports.
* **Cons**: Cannot execute JavaScript or render Single Page Applications (SPAs) natively without browser plugins (`scrapy-playwright`).

### 8.3 Why Playwright Reigns Supreme: The #1 Browser Automation Tool

> 🎨 **AI Image Generation Prompt (Copy & Paste for GPT / Midjourney)**:  
> *"A central feature hub illustrating why Playwright is the #1 automation engine: Multi-engine support (Chromium/Firefox/WebKit), Light-Speed Context Isolation, Smart Auto-Waiting, Native Network Routing, Storage State Persistence, and Multi-language APIs."*

### 8.4 Browser Crawling Concurrency Scaling Models

> 🎨 **AI Image Generation Prompt (Copy & Paste for GPT / Midjourney)**:  
> *"A 4-grid diagram showing crawler concurrency models: Strategy 1: Multiple Pages in 1 Context, Strategy 2: Multiple Isolated Contexts in 1 Browser (Recommended), Strategy 3: Multiple Browsers, Strategy 4: Distributed Kubernetes Worker Grid."*

### 8.5 Complete 20-Step End-to-End Playwright Crawl Workflow

> 🎨 **AI Image Generation Prompt (Copy & Paste for GPT / Midjourney)**:  
> *"A comprehensive 20-step circular/linear workflow flowchart illustrating an end-to-end Playwright crawl pipeline from Seed URL ingestion, Chromium launch, context allocation, network route setup, DOM wait, locator evaluation, to Bloom filter link deduplication and data warehouse storage."*

---

## 9. Stealth Anti-Bot Evasion & Advanced Data Extraction Architecture

### 9.1 The 5-Layer Anti-Bot Detection Landscape

> 🎨 **AI Image Generation Prompt (Copy & Paste for GPT / Midjourney)**:  
> *"A 5-layer cybersecurity threat evaluation diagram showing incoming scraper requests evaluated sequentially through Layer 1: TLS JA4 Handshake -> Layer 2: IP Reputation -> Layer 3: Engine CDP Leaks -> Layer 4: WebGL/Canvas Fingerprints -> Layer 5: Behavioral Honeypots. Mismatches lead to 403 blocks; clean requests pass to 200 OK."*

> **WARNING**: **The Coherence Rule**: Modern anti-bot security systems flag requests primarily on **mismatches between layers**. Presenting a Chrome User-Agent header while using a Python OpenSSL TLS signature or a standard Playwright CDP connection causes an instant 403 block.

### 9.2 The 5-Layer Unbreakable Stealth Stack

> 🎨 **AI Image Generation Prompt (Copy & Paste for GPT / Midjourney)**:  
> *"A 5-layer stealth defense architecture diagram: Layer 1: TLS JA4 Alignment (curl_cffi) -> Layer 2: Engine CDP Patching (Patchright & Camoufox C++) -> Layer 3: WebGL/Canvas Noise Randomization -> Layer 4: Bézier Curve Mouse Humanization -> Layer 5: AI CAPTCHA Solvers."*

### 9.3 Behavioral Humanization (Bézier Curves)

> 🎨 **AI Image Generation Prompt (Copy & Paste for GPT / Midjourney)**:  
> *"A mouse movement trajectory comparison diagram. Linear robot mouse path vs Non-deterministic cubic Bézier curve mouse trajectory with speed curves, micro-jitter, deceleration, hover, and click action."*

### 9.4 Maximum Data Volume Extraction Engine (Ad Tech, Google Ads, `window.dataLayer`)

> 🎨 **AI Image Generation Prompt (Copy & Paste for GPT / Midjourney)**:  
> *"An ad-tech data extraction architecture diagram showing a stealth browser capturing 5 data targets: Live DOM tree, Background XHR/Fetch JSON responses, Ad Tech/Google Ads parameters, Inline Next.js state (__NEXT_DATA__ & window.dataLayer), and Shadow DOM/OOPIF iframes, piping to a PostgreSQL/Parquet data warehouse."*

### 9.5 Production Master Stealth Scraper Code Implementation

```python
import asyncio
import json
from patchright.async_api import async_playwright

async def run_stealth_scraper(target_url: str):
    async with async_playwright() as p:
        # Launch patched Chromium binary with stealth args
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-infobars",
                "--window-size=1920,1080",
            ]
        )
        
        # Create isolated browser context with real desktop signatures
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            locale="en-US",
            timezone_id="America/New_York",
            geolocation={"latitude": 40.7128, "longitude": -74.0060},
            permissions=["geolocation"]
        )

        page = await context.new_page()

        # Data collection buckets
        captured_apis = []
        captured_ads = []

        # 1. Network Interception: Capture API JSON responses & Ad Network requests
        async def handle_response(response):
            url = response.url
            content_type = response.headers.get("content-type", "")

            # Capture backend JSON API payloads
            if "application/json" in content_type and "/api/" in url:
                try:
                    data = await response.json()
                    captured_apis.append({"url": url, "payload": data})
                except Exception:
                    pass

            # Capture Ad Tech requests (Google Ads, DoubleClick, Tracking)
            if any(ad_domain in url for ad_domain in ["googlesyndication", "doubleclick", "adservice", "taboola"]):
                captured_ads.append({"ad_url": url, "status": response.status})

        page.on("response", handle_response)

        # 2. Block heavy images to boost crawl speed while preserving JS/Ad scripts
        await page.route("**/*.{png,jpg,jpeg,gif,webp,woff2}", lambda route: route.abort())

        # 3. Navigate to target URL
        print(f"[*] Navigating to {target_url} with Patchright stealth engine...")
        await page.goto(target_url, wait_until="domcontentloaded", timeout=60000)

        # 4. Human Behavior Simulation (Natural Scrolling & Delays)
        for _ in range(3):
            await page.evaluate("window.scrollBy(0, 500)")
            await asyncio.sleep(0.5)

        # 5. Extract Inline State (__NEXT_DATA__ or dataLayer)
        next_data = await page.evaluate("""() => {
            const el = document.getElementById('__NEXT_DATA__');
            return el ? JSON.parse(el.textContent) : null;
        }""")

        data_layer = await page.evaluate("""() => window.dataLayer || []""")

        # 6. Extract Ad Elements & Outbound Links
        ad_elements = await page.locator("iframe[src*='google'], div[id*='ad'], div[class*='ad-slot']").all_text_contents()
        links = await page.locator("a[href]").evaluate_all("els => els.map(e => e.href)")

        # Compile Master Extraction Payload
        output_payload = {
            "target_url": target_url,
            "next_data_state": next_data,
            "data_layer_events": data_layer,
            "captured_apis_count": len(captured_apis),
            "captured_ads_count": len(captured_ads),
            "ad_text_snippets": ad_elements,
            "discovered_links_count": len(links),
        }

        print("[+] Data Extraction Complete!")
        print(json.dumps(output_payload, indent=2)[:1000])

        await context.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_stealth_scraper("https://example.com"))
```

### 9.6 Architectural Comparison of Modern Stealth Engines

| Feature / Tool | Playwright (Standard) | Patchright | Camoufox | Nodriver |
| :--- | :--- | :--- | :--- | :--- |
| **CDP Leak Protection** | ❌ Leaks `Runtime.enable` | ✅ Patched | ✅ N/A (Firefox engine) | ✅ Direct CDP, No Driver |
| **Engine Source Modification**| ❌ No | ❌ JS wrappers | ✅ C++ Firefox source spoofed | ❌ CDP Python wrapper |
| **Multi-Browser Support** | Chromium, Firefox, WebKit | Chromium | Firefox | Chromium |
| **Auto-Waiting & Locators**| ✅ Native | ✅ Native | ✅ Native | ⚠️ Custom locator syntax |
| **Primary Anti-Bot Target** | Low / Medium security | Medium / High (DataDome) | Extreme (Cloudflare, Kasada) | Medium / High security |

---

## 10. Master Architectural Blueprint

> 🎨 **AI Image Generation Prompt (Copy & Paste for GPT / Midjourney)**:  
> *"A master architectural blueprint diagram showing Crawler Engine -> Patchright/Camoufox Stealth Engine -> JA4 TLS Proxy -> Browser Context -> Page Tab -> Network/Ad Interception -> Live DOM & State -> Data Pipeline. Sleek dark cyberpunk technology diagram."*
