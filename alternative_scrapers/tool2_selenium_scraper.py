import time
import json

def scrape_with_selenium(url: str) -> dict:
    start_time = time.time()
    result = {
        "tool": "Selenium WebDriver (Legacy Automation)",
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
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30)
        driver.get(url)
        time.sleep(5)  # Wait for JS execution

        # Try evaluating JS
        slots_count = driver.execute_script("""
            try {
                return typeof googletag !== 'undefined' && googletag.apiReady ? googletag.pubads().getSlots().length : 0;
            } catch(e) { return 0; }
        """)

        bids_count = driver.execute_script("""
            try {
                return typeof pbjs !== 'undefined' ? pbjs.getWinningBids().length : 0;
            } catch(e) { return 0; }
        """)

        iframes = driver.find_elements("tag name", "iframe")
        
        result["gpt_slots_found"] = slots_count
        result["prebid_bids_captured"] = bids_count
        result["rendered_iframes_count"] = len(iframes)

        driver.quit()

        result["drawbacks"] = [
            "Synchronous & Blocking Architecture: Cannot run concurrent async tasks effectively.",
            "Easily Detected Bot Fingerprint: Exposes 'navigator.webdriver = true' and 'cdc_' variables by default.",
            "No Native Network Interception: Cannot capture background Server-to-Server (S2S) HTTP requests natively without proxy servers.",
            "Heavier Resource Usage & Flaky Page Timeouts: High memory footprint and fragile wait conditions.",
            "Driver Binary Dependency Hell: Requires managing matching ChromeDriver binary versions manually."
        ]

    except Exception as e:
        result["error"] = str(e)
        result["drawbacks"] = [
            "Selenium Execution / Driver Error: " + str(e),
            "Selenium requires ChromeDriver installed on host system."
        ]

    result["execution_time_ms"] = int((time.time() - start_time) * 1000)
    return result

if __name__ == "__main__":
    res = scrape_with_selenium("https://www.forbes.com")
    print(json.dumps(res, indent=2))
