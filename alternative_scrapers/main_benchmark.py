import os
import sys
import time
import json
import asyncio

# Import alternative scrapers
from tool1_requests_bs4 import scrape_with_requests_bs4
from tool2_selenium_scraper import scrape_with_selenium
from tool3_httpx_async import scrape_with_httpx
from tool4_pyppeteer_scraper import scrape_with_pyppeteer
from tool5_urllib_basic import scrape_with_urllib

def run_alternative_scrapers_benchmark(url: str = "https://www.forbes.com"):
    print("=" * 70)
    print(f"    RUNNING SCRAPER BENCHMARK & COMPARISON FOR: {url}")
    print("=" * 70)

    results = []

    # 1. Requests + BS4
    print("\n[1/5] Running Requests + BeautifulSoup4 Scraper...")
    res_bs4 = scrape_with_requests_bs4(url)
    results.append(res_bs4)
    print(f"      Status: {res_bs4['http_status']} | Time: {res_bs4['execution_time_ms']}ms | GPT Slots: {res_bs4['gpt_slots_found']}")

    # 2. HTTPX Async
    print("\n[2/5] Running HTTPX Async Scraper...")
    res_httpx = asyncio.run(scrape_with_httpx(url))
    results.append(res_httpx)
    print(f"      Status: {res_httpx['http_status']} | Time: {res_httpx['execution_time_ms']}ms | GPT Slots: {res_httpx['gpt_slots_found']}")

    # 3. Urllib Basic
    print("\n[3/5] Running Urllib Standard Library Scraper...")
    res_urllib = scrape_with_urllib(url)
    results.append(res_urllib)
    print(f"      Status: {res_urllib['http_status']} | Time: {res_urllib['execution_time_ms']}ms | GPT Slots: {res_urllib['gpt_slots_found']}")

    # 4. Selenium
    print("\n[4/5] Running Selenium WebDriver Scraper...")
    res_selenium = scrape_with_selenium(url)
    results.append(res_selenium)
    print(f"      Status: {res_selenium['http_status']} | Time: {res_selenium['execution_time_ms']}ms | GPT Slots: {res_selenium['gpt_slots_found']}")

    # 5. Pyppeteer
    print("\n[5/5] Running Pyppeteer Scraper...")
    res_pyppeteer = asyncio.run(scrape_with_pyppeteer(url))
    results.append(res_pyppeteer)
    print(f"      Status: {res_pyppeteer['http_status']} | Time: {res_pyppeteer['execution_time_ms']}ms | GPT Slots: {res_pyppeteer['gpt_slots_found']}")

    # Save outputs to JSON
    output_path = os.path.join("output", "alternative_scrapers_results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 70)
    print("                   BENCHMARK SUMMARY RESULTS")
    print("=" * 70)
    print(f"{'Tool Name':<35} | {'JS Support':<10} | {'GPT Slots':<10} | {'Prebid Bids':<10} | {'Time (ms)':<10}")
    print("-" * 85)
    for r in results:
        tool_name = r["tool"][:34]
        js_sup = "YES" if r["javascript_executed"] else "NO"
        slots = str(r["gpt_slots_found"])
        bids = str(r["prebid_bids_captured"])
        exec_t = str(r["execution_time_ms"])
        print(f"{tool_name:<35} | {js_sup:<10} | {slots:<10} | {bids:<10} | {exec_t:<10}")

    print("\nSaved detailed benchmark JSON to:", output_path)

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "https://www.forbes.com"
    run_alternative_scrapers_benchmark(target)
