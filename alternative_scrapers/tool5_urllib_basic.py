import time
import json
import urllib.request
from html.parser import HTMLParser

class SimpleIframeParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.iframe_count = 0

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'iframe':
            self.iframe_count += 1

def scrape_with_urllib(url: str) -> dict:
    start_time = time.time()
    result = {
        "tool": "Urllib + HTMLParser (Python Standard Library)",
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
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0"}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            result["http_status"] = response.getcode()
            html_content = response.read().decode('utf-8', errors='ignore')

            parser = SimpleIframeParser()
            parser.feed(html_content)
            result["rendered_iframes_count"] = parser.iframe_count

            result["drawbacks"] = [
                "Primitive Standard Library: Lacks automatic cookie handling, connection pooling, and HTTP/2.",
                "Zero JavaScript Support: Returns raw unrendered server text; misses all client-side AdTech scripts.",
                "High WAF Block Rate: Frequently blocked with 403 Forbidden by Akamai, Cloudflare, and CloudFront.",
                "No DOM Representation: Cannot inspect computed CSS layout, dimensions, or iframe sub-documents.",
                "No Stealth Capabilities: Completely transparent bot headers."
            ]

    except Exception as e:
        result["error"] = str(e)
        result["drawbacks"].append(f"Urllib Network Error: {e}")

    result["execution_time_ms"] = int((time.time() - start_time) * 1000)
    return result

if __name__ == "__main__":
    res = scrape_with_urllib("https://www.forbes.com")
    print(json.dumps(res, indent=2))
