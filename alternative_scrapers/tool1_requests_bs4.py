import time
import json
import requests
from bs4 import BeautifulSoup

def scrape_with_requests_bs4(url: str) -> dict:
    start_time = time.time()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    result = {
        "tool": "Requests + BeautifulSoup4 (Static HTTP)",
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
        response = requests.get(url, headers=headers, timeout=15)
        result["http_status"] = response.status_code
        soup = BeautifulSoup(response.text, "html.parser")

        # Attempt to find iframes in static HTML
        iframes = soup.find_all("iframe")
        result["rendered_iframes_count"] = len(iframes)

        # Static HTML cannot execute window.googletag or window.pbjs
        result["gpt_slots_found"] = 0
        result["prebid_bids_captured"] = 0
        result["javascript_executed"] = False

        result["drawbacks"] = [
            "Cannot execute JavaScript engine (No V8 / JavaScript runtime).",
            "Fails to trigger Google Publisher Tag (googletag.defineSlot) ad slot declarations.",
            "Fails to capture Prebid.js client-side / S2S header bidding CPM responses.",
            "Cannot render dynamic ad creative iframes or pierce shadow DOM.",
            "Easily blocked by Cloudflare / Akamai / Imperva anti-bot WAFs (No browser TLS fingerprinting)."
        ]

    except Exception as e:
        result["error"] = str(e)
        result["drawbacks"].append(f"Network / Execution failure: {e}")

    result["execution_time_ms"] = int((time.time() - start_time) * 1000)
    return result

if __name__ == "__main__":
    res = scrape_with_requests_bs4("https://www.forbes.com")
    print(json.dumps(res, indent=2))
