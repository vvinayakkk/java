import sys
import os
import json
import logging
from curl_cffi import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("TLSStealthTester")

def test_url_with_curl_cffi(url: str, impersonate: str = "chrome124"):
    logger.info(f"Testing {url} with curl_cffi (impersonate='{impersonate}')...")
    try:
        response = requests.get(
            url,
            impersonate=impersonate,
            headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Sec-Ch-Ua": '"Not=A?Brand";v="99", "Chromium";v="124", "Google Chrome";v="124"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"Windows"',
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1"
            },
            timeout=15
        )
        print("\n" + "=" * 70)
        print(f" Target URL        : {url}")
        print(f" HTTP Status Code  : {response.status_code}")
        print(f" TLS Impersonation : {impersonate}")
        print(f" Response Length   : {len(response.text)} bytes")
        print("-" * 70)
        print(" Response Snippet Preview:")
        print(response.text[:350].strip())
        print("=" * 70 + "\n")
        return response.status_code, response.text
    except Exception as e:
        logger.error(f"Error requesting {url}: {e}")
        return 0, str(e)

if __name__ == "__main__":
    urls_to_test = [
        "https://www.bloomberg.com",
        "https://nowsecure.nl",
        "https://httpbin.org/headers"
    ]
    for target in urls_to_test:
        test_url_with_curl_cffi(target)
