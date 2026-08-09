import sys
import os
import json
import asyncio
import logging
from playwright.async_api import async_playwright

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("StealthDemoCrawler")

async def run_stealth_demo(target_url: str = "https://httpbin.org/headers", output_dir: str = "./output"):
    os.makedirs(output_dir, exist_ok=True)
    logger.info(f"Initializing Stealth Browser Architecture for: {target_url}")

    async with async_playwright() as p:
        # 1. Launch Chromium with Chrome DevTools Protocol (CDP) stealth arguments
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
                "--no-zygote"
            ]
        )

        # 2. Create isolated Browser Context with normalized desktop hardware signatures
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            locale="en-US",
            timezone_id="America/New_York",
            geolocation={"latitude": 40.7128, "longitude": -74.0060},
            permissions=["geolocation"],
            device_scale_factor=1.0,
            has_touch=False,
            is_mobile=False
        )

        page = await context.new_page()

        # 3. Inject init scripts to mask automated browser flags (navigator.webdriver)
        await page.add_init_script("""
            // Mask navigator.webdriver flag
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });

            // Mock languages and plugins array
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });

            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });

            // Mock WebGL vendor string
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) return 'Intel Inc.';
                if (parameter === 37446) return 'Intel Iris OpenGL Engine';
                return getParameter.apply(this, [parameter]);
            };
        """)

        # Data collection buckets
        captured_requests = []
        captured_responses = []

        # 4. Asynchronous Network Interception Listener
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

        # 5. Navigate to Target URL
        logger.info(f"Navigating to {target_url}...")
        response = await page.goto(target_url, wait_until="domcontentloaded", timeout=60000)
        http_status = response.status if response else 0

        # 6. Behavioral Interaction (Natural Scrolling & Micro-Delays)
        logger.info("Executing behavioral interaction simulation (smooth scrolling & delays)...")
        for _ in range(3):
            await page.evaluate("window.scrollBy(0, 400)")
            await asyncio.sleep(0.5)

        # 7. Extract Page Metadata & Text Snippet
        page_title = await page.title()
        body_text = await page.locator("body").inner_text()

        # Save Execution Summary JSON
        output_data = {
            "target_url": target_url,
            "http_status": http_status,
            "page_title": page_title,
            "total_responses_captured": len(captured_responses),
            "sample_body_preview": body_text[:500] if body_text else "",
            "stealth_flags_applied": [
                "disable-blink-features=AutomationControlled",
                "navigator.webdriver = undefined",
                "WebGL vendor normalization",
                "Normalized desktop User-Agent & Viewport"
            ]
        }

        output_file = os.path.join(output_dir, "stealth_crawl_result.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2)

        logger.info(f"Crawl Completed! Status: {http_status} | Results saved to {output_file}")
        print("\n" + "=" * 65)
        print("            STEALTH BROWSER CRAWL SUMMARY")
        print("=" * 65)
        print(f" Target URL             : {target_url}")
        print(f" HTTP Status Code       : {http_status}")
        print(f" Page Title             : {page_title}")
        print(f" Network Calls Intercepted: {len(captured_responses)}")
        print(f" Output JSON Result Path: {output_file}")
        print("=" * 65 + "\n")

        await context.close()
        await browser.close()

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "https://httpbin.org/headers"
    asyncio.run(run_stealth_demo(target))
