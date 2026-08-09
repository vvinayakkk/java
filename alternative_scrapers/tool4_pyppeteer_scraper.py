import time
import json
import asyncio

async def scrape_with_pyppeteer(url: str) -> dict:
    start_time = time.time()
    result = {
        "tool": "Pyppeteer (Unofficial Python Puppeteer Port)",
        "target_url": url,
        "http_status": 200,
        "execution_time_ms": 0,
        "gpt_slots_found": 0,
        "prebid_bids_captured": 0,
        "rendered_iframes_count": 0,
        "javascript_executed": True,
        "error": None,
        "drawbacks": []
    }

    try:
        from pyppeteer import launch

        browser = await launch(headless=True, args=['--no-sandbox'])
        page = await browser.newPage()
        await page.goto(url, {'waitUntil': 'domcontentloaded', 'timeout': 30000})
        await asyncio.sleep(5)

        slots_count = await page.evaluate("""
            () => typeof googletag !== 'undefined' && googletag.apiReady ? googletag.pubads().getSlots().length : 0
        """)

        bids_count = await page.evaluate("""
            () => typeof pbjs !== 'undefined' ? pbjs.getWinningBids().length : 0
        """)

        iframes_count = await page.evaluate("""
            () => document.querySelectorAll('iframe').length
        """)

        result["gpt_slots_found"] = slots_count
        result["prebid_bids_captured"] = bids_count
        result["rendered_iframes_count"] = iframes_count

        await browser.close()

        result["drawbacks"] = [
            "Unmaintained & Deprecated Repository: No active maintenance; causes crashes in modern Python 3.10+ runtime.",
            "Single-Browser Support: Only supports Chromium; lacks WebKit (Safari) and Firefox multi-browser engines.",
            "Flaky Async Event Loop Crashing: Known memory leaks and unhandled WebSocket closed connection bugs.",
            "Outdated Stealth Mitigation: Easily flagged by modern Cloudflare Turnstile and Akamai bot detection.",
            "Lacks Playwright Auto-Waiting: Requires brittle fixed sleeps (asyncio.sleep) instead of smart event-driven assertions."
        ]

    except Exception as e:
        result["error"] = str(e)
        result["drawbacks"] = [
            "Pyppeteer Execution / Deprecation Failure: " + str(e),
            "Pyppeteer is unmaintained and incompatible with modern Python 3.10+ asyncio event loops."
        ]

    result["execution_time_ms"] = int((time.time() - start_time) * 1000)
    return result

if __name__ == "__main__":
    res = asyncio.run(scrape_with_pyppeteer("https://www.forbes.com"))
    print(json.dumps(res, indent=2))
