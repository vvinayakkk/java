import time
import json
import asyncio
import httpx

async def scrape_with_httpx(url: str) -> dict:
    start_time = time.time()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    result = {
        "tool": "HTTPX Async Client (High-Speed Static HTTP/2)",
        "target_url": url,
        "http_status": None,
        "execution_time_ms": 0,
        "gpt_slots_found": 0,
        "prebid_bids_captured": 0,
        "rendered_iframes_count": 0,
        "javascript_executed": False,
        "error": None,
        "drawbacks": []
    }

    try:
        async with httpx.AsyncClient(follow_redirects=True, http2=True, timeout=15.0) as client:
            response = await client.get(url, headers=headers)
            result["http_status"] = response.status_code

            # Count static iframe tags in raw HTML
            html_text = response.text
            static_iframes = html_text.count("<iframe")

            result["rendered_iframes_count"] = static_iframes
            result["gpt_slots_found"] = 0
            result["prebid_bids_captured"] = 0

            result["drawbacks"] = [
                "No JavaScript Engine: Cannot execute client-side scripts, Google Publisher Tag, or Prebid.js.",
                "Static Content Only: Only sees initial server HTML, missing 90%+ of dynamically injected ad slots.",
                "Cannot Pierce Creative IFrames: Cannot inspect inside cross-origin or friendly creative iframes.",
                "No DOM Layout Information: Cannot calculate element width, height, or computed CSS visibility.",
                "Lacks Browser API Surface: Missing window, document, localStorage, and cookie jar lifecycle handling."
            ]

    except Exception as e:
        result["error"] = str(e)
        result["drawbacks"].append(f"HTTPX Execution Error: {e}")

    result["execution_time_ms"] = int((time.time() - start_time) * 1000)
    return result

if __name__ == "__main__":
    res = asyncio.run(scrape_with_httpx("https://www.forbes.com"))
    print(json.dumps(res, indent=2))
