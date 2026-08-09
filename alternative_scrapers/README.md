# Alternative Scrapers Comparison & Playwright Technical Deep-Dive

This directory contains benchmark implementations of **5 alternative web scraping tools/libraries** in Python, evaluating their execution capabilities, missing features, anti-bot failures, and architectural drawbacks when auditing modern AdTech websites compared to **Playwright**.

---

## 📚 Web Scraping Fundamentals for Beginners

### 1. What is Web Scraping?
Web scraping is the automated process of fetching web pages, extracting structured data (such as prices, metadata, ad slots, CPM bids, or images), and storing the extracted information into databases or JSON files.

### 2. Static HTTP Requests vs. Real Browser Automation

```
+-----------------------------------------------------------------------------------+
|                            STATIC HTTP SCRAPERS                                   |
| (requests, httpx, urllib, curl, axios)                                            |
|                                                                                   |
|  Python Code  ==== [ HTTP GET ] ====>  Target Server                             |
|  Python Code  <=== [ Raw HTML Text ] = Target Server                              |
|                                                                                   |
|  ⚠️ NO JavaScript Execution | NO DOM | NO GPT Ad Slots | NO Prebid Bids             |
+-----------------------------------------------------------------------------------+

                                        vs.

+-----------------------------------------------------------------------------------+
|                        PLAYWRIGHT REAL BROWSER ENGINE                             |
| (Chromium V8 Engine + WebKit + Firefox)                                           |
|                                                                                   |
|  Python Code ==[ CDP Commands ]==> Browser Engine (Chromium)                      |
|                                         |                                         |
|                                   Executes JavaScript (googletag, pbjs)            |
|                                   Renders CSS Layout & Viewport Bounds            |
|                                   Intercepts Network Traffic (S2S Bids)           |
|                                   Pierces Creative IFrames & Shadow DOM           |
+-----------------------------------------------------------------------------------+
```

- **Static HTTP Requests** (`requests`, `httpx`, `urllib`):
  Sends an HTTP `GET` request to a URL and receives the raw HTML string sent by the server. **It does NOT execute JavaScript.**
- **Real Browser Automation** (`Playwright`, `Selenium`):
  Launches an actual browser instance (Chromium / Firefox / WebKit), executes all JavaScript scripts on the page (`googletag.defineSlot`, `pbjs.getWinningBids`), calculates CSS layout dimensions, and renders creative iframes.

---

## 🛠️ Analysis of 5 Alternative Scrapers & Technical Drawbacks

### 1. `tool1_requests_bs4.py` (Requests + BeautifulSoup4)
- **How It Works**: Sends a synchronous HTTP GET request and parses the static HTML string using BeautifulSoup.
- **Drawbacks**:
  - **Zero JavaScript Execution**: Missing 100% of client-side AdTech scripts (`googletag`, `pbjs`).
  - **0 Ad Slots Extracted**: Cannot evaluate dynamic ad unit paths or CPM bids.
  - **High WAF Block Rate**: Blocked by Cloudflare / Akamai because requests lack browser TLS fingerprinting (JA3/Akamai H2 fingerprints).

---

### 2. `tool2_selenium_scraper.py` (Selenium WebDriver)
- **How It Works**: Controls a desktop browser using the legacy WebDriver HTTP protocol and driver binaries (ChromeDriver).
- **Drawbacks**:
  - **Synchronous & Extremely Slow**: Blocks the Python thread on page loads; lacks native `async/await` event loops.
  - **Immediate Bot Detection**: Exposes `navigator.webdriver = true` and `cdc_` ChromeDriver variables by default, causing Cloudflare and Imperva to block requests.
  - **No Native Network Interception**: Cannot asynchronously capture background Server-to-Server (S2S) HTTP bidding requests without running heavy proxy servers (Browsermob Proxy).
  - **Driver Versioning Frustration**: Requires constantly updating ChromeDriver binaries to match host Chrome versions.

---

### 3. `tool3_httpx_async.py` (Async HTTPX Client)
- **How It Works**: An asynchronous HTTP/2 client for Python.
- **Drawbacks**:
  - **Still a Static HTTP Client**: Fast network performance, but still cannot execute V8 JavaScript or render the DOM.
  - **No Window / Document Context**: Missing browser APIs (`window.googletag`, `window.pbjs`, `localStorage`, cookie lifecycle).

---

### 4. `tool4_pyppeteer_scraper.py` (Pyppeteer)
- **How It Works**: An unofficial Python port of the Node.js Puppeteer library.
- **Drawbacks**:
  - **Abandoned & Deprecated**: The project is unmaintained and contains unpatched bugs with modern Python 3.10+ event loops (`asyncio.get_event_loop()` crashes).
  - **Single-Browser Only**: Only supports Chromium; cannot test WebKit (Safari) or Firefox.
  - **Flaky & Memory Leaks**: Known WebSocket connection drop issues under concurrent workloads.

---

### 5. `tool5_urllib_basic.py` (Urllib Standard Library)
- **How It Works**: Python's standard library `urllib.request` module.
- **Drawbacks**:
  - **Primitive Capabilities**: No built-in connection pooling, HTTP/2, or session management.
  - **Blocked Instantly**: Default `Python-urllib` User-Agent header is blocked with `403 Forbidden` by almost every major publisher WAF.

---

## 🏆 Comparative Benchmark Results Matrix

| Tool / Scraper Name | JS Execution | GPT Slots | Prebid Bids | WAF Anti-Bot Bypass | Native Network Interception | IFrame Piercing | Speed / Concurrency |
| :--- | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| **Urllib + HTMLParser** | ❌ NO | 0 | 0 | ❌ Fails (403) | ❌ NO | ❌ NO | ⚡ Fast (Raw) |
| **Requests + BeautifulSoup4** | ❌ NO | 0 | 0 | ❌ Fails | ❌ NO | ❌ NO | ⚡ Fast (Raw) |
| **HTTPX Async** | ❌ NO | 0 | 0 | ❌ Fails | ❌ NO | ❌ NO | ⚡ Ultra-Fast |
| **Selenium WebDriver** | ✅ YES | 0 (Blocked) | 0 | ❌ Fails (`navigator.webdriver`) | ❌ NO (Requires Proxy) | ⚠️ Partial | 🐢 Slow (Blocking) |
| **Pyppeteer (Unmaintained)** | ⚠️ Unstable | 0 (Flaky) | 0 | ⚠️ Moderate | ⚠️ Partial | ⚠️ Limited | 🐢 Flaky |
| 🥇 **Playwright (Chosen)** | ✅ **YES** | **7/7 (100%)** | **Captured** | ✅ **PASSED (Stealth)** | ✅ **Native Async** | ✅ **Full Piercing** | ⚡ **Ultra-Fast Async** |

---

## 💎 Top-Notch Technical Justification: Why We Chose Playwright

### 1. Direct Chrome DevTools Protocol (CDP) WebSocket Architecture
Unlike Selenium (which uses a slow HTTP-based WebDriver protocol), Playwright connects directly to browser engines via high-speed binary WebSocket Chrome DevTools Protocol (CDP) channels. This enables instant command execution and zero driver version mismatch issues.

### 2. Native Asynchronous Network Interception
Playwright provides built-in, non-blocking asynchronous event listeners (`page.onRequest` and `page.onResponse`). This allows our crawler to intercept background Server-to-Server (S2S) header bidding calls, Google Publisher Tag requests, and ad network network traffic in real-time without external proxy servers.

### 3. Anti-Bot WAF Stealth Evasion
Playwright allows injecting initialization scripts (`page.addInitScript`) before any site JavaScript executes. We mask bot signals by overriding `navigator.webdriver = undefined`, randomizing TLS fingerprints, user agents, and viewport dimensions, bypassing Cloudflare, Akamai, and Imperva protections.

### 4. Cross-Origin Creative IFrame & Shadow DOM Piercing
Ad creatives render inside nested `about:blank`, friendly, or cross-origin `<iframe>` elements. Playwright exposes a unified `page.frames` API and selector engine (`iframe >> img`) that pierces cross-origin boundaries to extract ad image URLs and destination clickthrough URLs.

### 5. Auto-Waiting & Event-Driven Reliability
Playwright automatically waits for elements to be visible, actionable, and stable before interacting, eliminating brittle `sleep()` calls and preventing race conditions during ad loading.
