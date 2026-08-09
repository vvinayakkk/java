import sys
import os
import json
import asyncio
import logging
from typing import List, Dict, Any
from datetime import datetime

from crawler import ForbesAdTechCrawler
from reporter import ReportGenerator

logger = logging.getLogger("BatchAdTechCrawler")

TEST_20_URLS = [
    "https://www.forbes.com",
    "https://edition.cnn.com",
    "https://techcrunch.com",
    "https://www.businessinsider.com",
    "https://www.theverge.com",
    "https://www.wired.com",
    "https://www.engadget.com",
    "https://mashable.com",
    "https://www.bloomberg.com",
    "https://www.reuters.com",
    "https://www.nytimes.com",
    "https://www.wsj.com",
    "https://www.usatoday.com",
    "https://www.bbc.com",
    "https://www.foxnews.com",
    "https://www.cnbc.com",
    "https://finance.yahoo.com",
    "https://pitchfork.com",
    "https://www.vox.com",
    "https://www.polygon.com"
]

class BatchAdTechCrawler:
    def __init__(self, concurrency: int = 4, headless: bool = True, output_dir: str = "./output"):
        self.concurrency = concurrency
        self.headless = headless
        self.output_dir = output_dir
        self.semaphore = asyncio.Semaphore(concurrency)
        self.reporter = ReportGenerator(output_dir=output_dir)

    async def crawl_single(self, crawler: ForbesAdTechCrawler, url: str) -> Dict[str, Any]:
        async with self.semaphore:
            logger.info(f"[BATCH] Starting crawl for: {url}")
            try:
                data = await crawler.crawl(url)
                domain_prefix = url.replace("https://", "").replace("http://", "").replace("/", "_")[:30]
                json_path = self.reporter.save_json(data, filename_prefix=f"result_{domain_prefix}")
                html_path = self.reporter.generate_html_report(data, filename_prefix=f"report_{domain_prefix}")

                val = data.get("validation", {})
                return {
                    "url": url,
                    "status": "SUCCESS",
                    "quality_score": val.get("quality_score", 0),
                    "quality_rating": val.get("quality_rating", "UNKNOWN"),
                    "gpt_slots": len(data.get("ad_slots_summary", [])),
                    "adtech_calls": data.get("network_summary", {}).get("adtech_requests_count", 0),
                    "json_file": json_path,
                    "html_file": html_path
                }
            except Exception as e:
                logger.error(f"[BATCH] Failed to crawl {url}: {e}")
                return {
                    "url": url,
                    "status": "FAILED",
                    "error": str(e),
                    "quality_score": 0,
                    "quality_rating": "CRITICAL_FAILURE"
                }

    async def run_batch(self, url_list: List[str]) -> Dict[str, Any]:
        logger.info(f"Starting Batch Crawl for {len(url_list)} URLs with Concurrency={self.concurrency}...")
        crawler = ForbesAdTechCrawler(headless=self.headless, output_dir=self.output_dir)
        
        tasks = [self.crawl_single(crawler, url) for url in url_list]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        batch_summary = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_urls": len(url_list),
            "successful_crawls": len([r for r in results if isinstance(r, dict) and r.get("status") == "SUCCESS"]),
            "failed_crawls": len([r for r in results if isinstance(r, dict) and r.get("status") == "FAILED"]),
            "average_quality_score": round(
                sum(r.get("quality_score", 0) for r in results if isinstance(r, dict)) / max(1, len(results)), 1
            ),
            "results": results
        }

        batch_summary_path = os.path.join(self.output_dir, f"batch_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(batch_summary_path, "w", encoding="utf-8") as f:
            json.dump(batch_summary, f, indent=2)

        logger.info(f"Batch Crawl Completed! Summary saved to {batch_summary_path}")
        return batch_summary
