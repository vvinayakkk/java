import sys
import os
import argparse
import asyncio
import logging

from crawler import ForbesAdTechCrawler
from reporter import ReportGenerator
from batch_crawler import BatchAdTechCrawler, TEST_20_URLS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("AdTechCrawlerMain")

async def main_async():
    parser = argparse.ArgumentParser(description="Forbes AdTech Web Crawler & Quality Analytics Engine")
    parser.add_argument("--url", type=str, help="Single Target URL to crawl")
    parser.add_argument("--batch", type=str, help="Path to text file containing target URLs")
    parser.add_argument("--test-20", action="store_true", help="Run automated benchmark suite on 20 top publishers")
    parser.add_argument("--output-dir", type=str, default="./output", help="Directory to save JSON & HTML outputs")
    parser.add_argument("--concurrency", type=int, default=4, help="Parallel worker concurrency for batch crawl")
    parser.add_argument("--headful", action="store_true", help="Run browser in headful mode")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    headless = not args.headful

    if args.test_20:
        logger.info(f"Running Benchmark Crawl on 20 Top Publishers (Concurrency={args.concurrency})...")
        batch_runner = BatchAdTechCrawler(concurrency=args.concurrency, headless=headless, output_dir=args.output_dir)
        summary = await batch_runner.run_batch(TEST_20_URLS)
        print("\n" + "=" * 65)
        print("             20-SITE BENCHMARK TEST SUMMARY")
        print("=" * 65)
        print(f" Total URLs Crawled   : {summary['total_urls']}")
        print(f" Successful Crawls    : {summary['successful_crawls']}")
        print(f" Failed Crawls        : {summary['failed_crawls']}")
        print(f" Average Quality Score: {summary['average_quality_score']} / 100")
        print("=" * 65 + "\n")
        return

    if args.batch:
        if not os.path.exists(args.batch):
            logger.error(f"Batch URL file not found: {args.batch}")
            sys.exit(1)
        with open(args.batch, "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        logger.info(f"Loaded {len(urls)} URLs from {args.batch}")
        batch_runner = BatchAdTechCrawler(concurrency=args.concurrency, headless=headless, output_dir=args.output_dir)
        await batch_runner.run_batch(urls)
        return

    target_url = args.url if args.url else "https://www.forbes.com"
    logger.info(f"Starting Single URL Crawl for: {target_url}")

    crawler = ForbesAdTechCrawler(headless=headless, output_dir=args.output_dir)
    extraction_data = await crawler.crawl(target_url)

    reporter = ReportGenerator(output_dir=args.output_dir)
    json_path = reporter.save_json(extraction_data, filename_prefix="forbes_adtech")
    html_path = reporter.generate_html_report(extraction_data, filename_prefix="forbes_report")

    val = extraction_data.get("validation", {})
    print("\n" + "=" * 65)
    print("                 EXECUTIVE CRAWL SUMMARY")
    print("=" * 65)
    print(f" Quality Rating        : {val.get('quality_rating')} (Score: {val.get('quality_score')}/100)")
    print(f" GPT Ad Slots Found    : {len(extraction_data.get('ad_slots_summary', []))}")
    print(f" AdTech Calls Captured : {extraction_data.get('network_summary', {}).get('adtech_requests_count', 0)}")
    print(f" ads.txt Direct Partners: {extraction_data.get('ads_txt', {}).get('direct_count', 0)}")
    print(f" JSON Result File      : {json_path}")
    print(f" Interactive Dashboard : {html_path}")
    print("=" * 65 + "\n")

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()
