import sys
import os
import json
import asyncio
import logging
import time
import random
from typing import List, Dict, Any
from playwright.async_api import async_playwright, Browser

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("StealthDemoCrawler")

ADVANCED_STEALTH_JS = """
    // 1. Mask navigator.webdriver
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined,
        configurable: true
    });

    // 2. Add window.chrome runtime mock
    if (!window.chrome) {
        window.chrome = {
            runtime: {
                OnInstalledReason: {
                    CHROME_UPDATE: "chrome_update",
                    INSTALL: "install",
                    SHARED_MODULE_UPDATE: "shared_module_update",
                    UPDATE: "update"
                },
                OnRestartRequiredReason: {
                    APP_UPDATE: "app_update",
                    OS_UPDATE: "os_update",
                    PERIODIC: "periodic"
                },
                PlatformArch: {
                    ARM: "arm",
                    ARM64: "arm64",
                    MIPS: "mips",
                    MIPS64: "mips64",
                    X86_32: "x86-32",
                    X86_64: "x86-64"
                },
                PlatformNaclArch: {
                    ARM: "arm",
                    MIPS: "mips",
                    MIPS64: "mips64",
                    X86_32: "x86-32",
                    X86_64: "x86-64"
                },
                PlatformOs: {
                    ANDROID: "android",
                    CROS: "cros",
                    LINUX: "linux",
                    MAC: "mac",
                    OPENBSD: "openbsd",
                    WIN: "win"
                }
            },
            loadTimes: function() {},
            csi: function() {},
            app: {}
        };
    }

    // 3. Mock navigator.permissions.query
    const originalQuery = window.navigator.permissions.query;
    window.navigator.permissions.query = (parameters) => (
        parameters.name === 'notifications' ?
            Promise.resolve({ state: Notification.permission || 'granted' }) :
            originalQuery(parameters)
    );

    // 4. Mock Plugins & MimeTypes
    const makePlugin = (name, filename, description) => {
        const plugin = [
            { type: "application/pdf", suffixes: "pdf", description: "Portable Document Format" }
        ];
        plugin.name = name;
        plugin.filename = filename;
        plugin.description = description;
        return plugin;
    };
    const pluginList = [
        makePlugin('PDF Viewer', 'pdf-viewer.plugin', 'Portable Document Format'),
        makePlugin('Chrome PDF Viewer', 'mhjfbheakiddpjooeepmodchbnpobgfc', 'Portable Document Format'),
        makePlugin('Chromium PDF Viewer', 'internal-pdf-viewer', 'Portable Document Format')
    ];
    Object.defineProperty(navigator, 'plugins', {
        get: () => pluginList,
        configurable: true
    });

    Object.defineProperty(navigator, 'languages', {
        get: () => ['en-US', 'en'],
        configurable: true
    });

    // 5. Normalize WebGL Vendor / Renderer (NVIDIA Signature)
    const getParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(parameter) {
        if (parameter === 37445) return 'Google Inc. (NVIDIA)';
        if (parameter === 37446) return 'ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0 ps_5_0, D3D11)';
        return getParameter.apply(this, [parameter]);
    };

    if (typeof WebGL2RenderingContext !== 'undefined') {
        const getParameter2 = WebGL2RenderingContext.prototype.getParameter;
        WebGL2RenderingContext.prototype.getParameter = function(parameter) {
            if (parameter === 37445) return 'Google Inc. (NVIDIA)';
            if (parameter === 37446) return 'ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0 ps_5_0, D3D11)';
            return getParameter2.apply(this, [parameter]);
        };
    }
"""

TOUGH_TEST_URLS = [
    "https://bot.sannysoft.com/",
    "https://nowsecure.nl",
    "https://browserleaks.com/canvas",
    "https://www.scrapingcourse.com/ecommerce/",
    "https://news.ycombinator.com/",
    "https://httpbin.org/anything"
]

async def simulate_human_interaction(page):
    """Simulate realistic human interactions (mouse curves, micro scrolls, delays)."""
    try:
        # Random mouse movements
        for _ in range(3):
            x = random.randint(100, 800)
            y = random.randint(100, 600)
            await page.mouse.move(x, y, steps=5)
            await asyncio.sleep(random.uniform(0.1, 0.3))

        # Smooth natural scroll
        for _ in range(2):
            scroll_y = random.randint(200, 500)
            await page.evaluate(f"window.scrollBy({{top: {scroll_y}, behavior: 'smooth'}});")
            await asyncio.sleep(random.uniform(0.3, 0.6))
    except Exception:
        pass

async def handle_interactive_challenges(page):
    """Detect and attempt to solve interactive challenges (Cloudflare Turnstile, PerimeterX Press & Hold, CAPTCHA checkboxes)."""
    try:
        # 1. Cloudflare Turnstile iframe button clicker
        turnstile_frame = page.frame_locator("iframe[src*='challenges.cloudflare.com'], iframe[src*='turnstile']")
        if await turnstile_frame.locator("input[type='checkbox'], .mark, #challenge-stage").count() > 0:
            logger.info("Detected Cloudflare Turnstile iframe. Attempting human-like click...")
            target = turnstile_frame.locator("input[type='checkbox'], .mark, #challenge-stage").first
            box = await target.bounding_box()
            if box:
                await page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=10)
                await asyncio.sleep(0.2)
                await page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                await asyncio.sleep(3.0)

        # 2. PerimeterX / Press & Hold button
        px_captcha = page.locator("#px-captcha, #px-captcha-container, div[id*='px-captcha']")
        if await px_captcha.count() > 0:
            logger.info("Detected PerimeterX CAPTCHA element. Attempting human Press & Hold simulation...")
            box = await px_captcha.first.bounding_box()
            if box:
                target_x = box["x"] + box["width"] / 2
                target_y = box["y"] + box["height"] / 2
                await page.mouse.move(target_x, target_y, steps=15)
                await asyncio.sleep(0.3)
                # Press down and hold mouse button for 3.5 seconds
                await page.mouse.down()
                await asyncio.sleep(3.5)
                await page.mouse.up()
                await asyncio.sleep(3.0)

        # 3. Generic Verification Button Clicker
        human_btn = page.locator("button:has-text('Verify you are human'), input[value*='Verify'], button:has-text('I am human')")
        if await human_btn.count() > 0:
            logger.info("Detected human verification button. Clicking...")
            await human_btn.first.click(delay=150)
            await asyncio.sleep(2.5)

    except Exception as e:
        logger.warning(f"Error handling interactive challenge clicker: {e}")

async def extract_tough_site_data(page, url: str) -> Dict[str, Any]:
    """Extract clean structured data from tough targets and anti-bot verification suites."""
    extracted = {}
    try:
        if "bot.sannysoft.com" in url:
            # Parse bot detection test table results
            rows = await page.locator("table tr").all()
            results_summary = []
            passed_count = 0
            failed_count = 0

            for row in rows:
                text = await row.inner_text()
                if text.strip():
                    parts = [p.strip() for p in text.split("\t") if p.strip()]
                    if len(parts) >= 2:
                        test_name = parts[0]
                        status = parts[1]
                        is_failed = "failed" in status.lower() or "warn" in status.lower()
                        if is_failed:
                            failed_count += 1
                        else:
                            passed_count += 1
                        results_summary.append({
                            "test": test_name,
                            "result": status,
                            "passed": not is_failed
                        })
            extracted["bot_sannysoft_summary"] = {
                "total_tests": len(results_summary),
                "passed_tests": passed_count,
                "failed_tests": failed_count,
                "stealth_rating": f"{(passed_count / len(results_summary) * 100):.1f}%" if results_summary else "N/A",
                "test_details": results_summary[:10] # Top 10 key tests
            }

        elif "nowsecure.nl" in url:
            # Cloudflare challenge test page
            heading = await page.locator("h1").inner_text() if await page.locator("h1").count() > 0 else ""
            body_snippet = await page.locator("body").inner_text()
            extracted["cloudflare_bypass_check"] = {
                "heading": heading.strip(),
                "bypassed": "OH YEAH" in body_snippet.upper() or "NOWSECURE" in body_snippet.upper(),
                "snippet": body_snippet[:300].strip()
            }

        elif "browserleaks.com" in url:
            # Canvas fingerprinting detector
            page_title = await page.title()
            canvas_status = await page.locator("#canvas-fp").inner_text() if await page.locator("#canvas-fp").count() > 0 else "N/A"
            extracted["canvas_fingerprint_check"] = {
                "title": page_title,
                "canvas_fingerprint_id": canvas_status.strip(),
                "page_verified": True
            }

        elif "scrapingcourse.com" in url:
            # E-commerce challenge site
            product_elements = await page.locator(".product").all()
            products = []
            for p in product_elements[:5]:
                name = await p.locator(".product-name, h2, h3").first.inner_text() if await p.locator(".product-name, h2, h3").count() > 0 else "Product"
                price = await p.locator(".price, .amount").first.inner_text() if await p.locator(".price, .amount").count() > 0 else "N/A"
                products.append({"name": name.strip(), "price": price.strip()})
            extracted["ecommerce_products"] = products
            extracted["total_products_found"] = len(product_elements)

        elif "news.ycombinator.com" in url:
            # Hacker News frontpage top stories
            story_elements = await page.locator(".athing").all()
            stories = []
            for s in story_elements[:5]:
                title = await s.locator(".titleline > a").first.inner_text()
                link = await s.locator(".titleline > a").first.get_attribute("href")
                stories.append({"title": title, "link": link})
            extracted["hacker_news_top_stories"] = stories
            extracted["total_stories"] = len(story_elements)

        elif "bloomberg.com" in url:
            page_title = await page.title()
            body_snippet = await page.locator("body").inner_text()
            
            # Check if PerimeterX / Kasada bot challenge block page is triggered
            is_blocked = "PERIMETERX" in body_snippet.upper() or "PRESS & HOLD" in body_snippet.upper() or "ARE YOU A HUMAN" in body_snippet.upper() or "CAPTCHA" in body_snippet.upper()
            
            headlines = []
            if not is_blocked:
                # Attempt to extract headline links
                headline_elements = await page.locator("a[href*='/news/articles/'], h1, h2, h3").all()
                for h in headline_elements[:5]:
                    txt = await h.inner_text()
                    if txt.strip() and len(txt.strip()) > 15:
                        headlines.append(txt.strip())
            
            extracted["bloomberg_crawl_check"] = {
                "page_title": page_title,
                "is_blocked_by_antibot": is_blocked,
                "bypassed": not is_blocked,
                "top_headlines_extracted": headlines,
                "sample_snippet": body_snippet[:300].strip()
            }

        else: # httpbin / anything
            body_text = await page.locator("body").inner_text()
            try:
                extracted["parsed_json"] = json.loads(body_text)
            except Exception:
                extracted["raw_snippet"] = body_text[:300]

    except Exception as e:
        extracted["extraction_error"] = str(e)

    return extracted

async def crawl_single_url(
    browser: Browser,
    target_url: str,
    index: int,
    output_dir: str,
    semaphore: asyncio.Semaphore
) -> Dict[str, Any]:
    async with semaphore:
        start_time = time.time()
        logger.info(f"[{index}] Starting advanced stealth crawl for TOUGH URL: {target_url}")

        result_data = {
            "index": index,
            "target_url": target_url,
            "http_status": 0,
            "page_title": "",
            "total_responses_captured": 0,
            "extracted_data": {},
            "sample_body_preview": "",
            "duration_seconds": 0.0,
            "status": "FAILED",
            "error": None,
            "stealth_flags_applied": [
                "disable-blink-features=AutomationControlled",
                "window.chrome runtime injection",
                "navigator.permissions.query override",
                "NVIDIA WebGL vendor normalization",
                "Realistic PDF plugin signatures",
                "Human mouse bezier movement & smooth scrolling"
            ]
        }

        context = None
        try:
            # Create isolated stealth browser context with realistic hardware flags
            context = await browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                locale="en-US",
                timezone_id="America/New_York",
                geolocation={"latitude": 40.7128, "longitude": -74.0060},
                permissions=["geolocation", "notifications"],
                device_scale_factor=1.0,
                has_touch=False,
                is_mobile=False
            )

            page = await context.new_page()
            await page.add_init_script(ADVANCED_STEALTH_JS)

            captured_responses = []

            async def handle_response(response):
                try:
                    captured_responses.append({
                        "url": response.url,
                        "status": response.status,
                        "content_type": response.headers.get("content-type", "")
                    })
                except Exception:
                    pass

            page.on("response", handle_response)

            logger.info(f"[{index}] Navigating to tough target: {target_url}...")
            response = await page.goto(target_url, wait_until="domcontentloaded", timeout=60000)
            http_status = response.status if response else 0
            result_data["http_status"] = http_status

            # Dynamic wait & interactive challenge detection (Cloudflare Turnstile / PerimeterX Press & Hold)
            logger.info(f"[{index}] Simulating human interactions & checking interactive CAPTCHA/Turnstile challenges...")
            await simulate_human_interaction(page)
            await handle_interactive_challenges(page)
            await asyncio.sleep(2.0) # Grace delay for dynamic JS challenge evaluation

            page_title = await page.title()
            body_text = await page.locator("body").inner_text()

            # Structured Data Extraction
            extracted_data = await extract_tough_site_data(page, target_url)

            elapsed = round(time.time() - start_time, 2)
            result_data.update({
                "page_title": page_title,
                "total_responses_captured": len(captured_responses),
                "extracted_data": extracted_data,
                "sample_body_preview": body_text[:300].strip() if body_text else "",
                "duration_seconds": elapsed,
                "status": "SUCCESS" if http_status in [200, 304] else f"HTTP_{http_status}"
            })

            single_output_file = os.path.join(output_dir, f"stealth_crawl_result_{index}.json")
            with open(single_output_file, "w", encoding="utf-8") as f:
                json.dump(result_data, f, indent=2)

            logger.info(f"[{index}] Advanced crawl completed for {target_url} in {elapsed}s (Status: {http_status})")

        except Exception as e:
            elapsed = round(time.time() - start_time, 2)
            result_data["error"] = str(e)
            result_data["duration_seconds"] = elapsed
            logger.error(f"[{index}] Error crawling {target_url}: {e}")
        finally:
            if context:
                await context.close()

        return result_data

async def run_stealth_batch(urls: List[str], output_dir: str = "./output", max_concurrency: int = 3):
    os.makedirs(output_dir, exist_ok=True)
    logger.info(f"Initializing Async Stealth Batch Crawler for {len(urls)} TOUGH URLs (Concurrency limit: {max_concurrency})")

    start_batch_time = time.time()

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-infobars",
                "--window-size=1920,1080",
                "--disable-dev-shm-usage",
                "--disable-accelerated-2d-canvas",
                "--no-first-run",
                "--no-zygote",
                "--disable-features=IsolateOrigins,site-per-process"
            ]
        )

        semaphore = asyncio.Semaphore(max_concurrency)
        tasks = [
            crawl_single_url(browser, url, idx + 1, output_dir, semaphore)
            for idx, url in enumerate(urls)
        ]

        results = await asyncio.gather(*tasks)
        await browser.close()

    total_batch_duration = round(time.time() - start_batch_time, 2)

    summary_data = {
        "total_urls": len(urls),
        "successful_crawls": sum(1 for r in results if r["status"] == "SUCCESS"),
        "total_duration_seconds": total_batch_duration,
        "concurrency_limit": max_concurrency,
        "results": results
    }

    summary_file = os.path.join(output_dir, "stealth_batch_summary.json")
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2)

    # Console Summary Table & Data Inspection
    print("\n" + "=" * 90)
    print("                      ASYNC STEALTH CRAWLER BATCH SUMMARY (TOUGH SITES)")
    print("=" * 90)
    print(f" Total URLs Crawled   : {len(urls)}")
    print(f" Concurrency Limit    : {max_concurrency} parallel instances")
    print(f" Total Batch Time     : {total_batch_duration}s")
    print(f" Summary Output Path  : {summary_file}")
    print("-" * 90)
    print(f"{'#':<3} | {'Status':<8} | {'HTTP':<5} | {'Time (s)':<8} | {'Calls':<6} | {'Target URL'}")
    print("-" * 90)
    for r in results:
        status_str = r["status"][:8]
        http_code = str(r["http_status"])
        duration = f"{r['duration_seconds']}s"
        calls = str(r["total_responses_captured"])
        url = r["target_url"]
        print(f"{r['index']:<3} | {status_str:<8} | {http_code:<5} | {duration:<8} | {calls:<6} | {url}")
    print("=" * 90 + "\n")

    # Detailed Scraped Data Inspection Output
    print("=" * 90)
    print("                   MANUAL DATA INSPECTION OF SCRAPED CONTENT (TOUGH SITES)")
    print("=" * 90)
    for r in results:
        print(f"\n--- [URL #{r['index']}] {r['target_url']} ---")
        print(f"Page Title: {r['page_title']}")
        print("Extracted Data Preview:")
        print(json.dumps(r['extracted_data'], indent=2))
        print("-" * 60)

    return results

if __name__ == "__main__":
    urls_to_crawl = sys.argv[1:] if len(sys.argv) > 1 else TOUGH_TEST_URLS
    asyncio.run(run_stealth_batch(urls_to_crawl))



