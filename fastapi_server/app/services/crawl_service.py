import json
import time
import uuid
import logging
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session

from app.config import settings
from app.redis_cache import cache_manager
from app.crawler.engine import ForbesAdTechCrawler
from app.services.reporter import ReportGenerator
from app.models import CrawlJob, AdSlotModel, BidderSummaryModel, RenderedIframeModel, CrawlPayloadModel

logger = logging.getLogger(__name__)

class CrawlService:
    def __init__(self, db: Optional[Session] = None):
        self.db = db
        self.crawler = ForbesAdTechCrawler(headless=True, output_dir=settings.OUTPUT_DIR)
        self.reporter = ReportGenerator(output_dir=settings.OUTPUT_DIR)

    async def crawl_url(self, url: str, force_refresh: bool = False) -> Dict[str, Any]:
        url_clean = url.strip()
        if not force_refresh:
            cached_data = cache_manager.get(url_clean)
            if cached_data:
                cached_data["cached"] = True
                return cached_data

        start_time = time.time()
        job_uuid = str(uuid.uuid4())

        extraction_data = await self.crawler.crawl(url_clean)
        execution_time_ms = int((time.time() - start_time) * 1000)
        extraction_data["job_id"] = job_uuid
        extraction_data["cached"] = False

        domain_prefix = url_clean.replace("https://", "").replace("http://", "").replace("/", "_")[:30]
        json_path = self.reporter.save_json(extraction_data, filename_prefix=f"result_{domain_prefix}")
        html_path = self.reporter.generate_html_report(extraction_data, filename_prefix=f"report_{domain_prefix}")
        extraction_data["json_file"] = json_path
        extraction_data["html_file"] = html_path

        cache_manager.set(url_clean, extraction_data)

        if self.db:
            try:
                self._persist_to_mysql(job_uuid, url_clean, extraction_data, execution_time_ms)
            except Exception as e:
                logger.error(f"Error persisting crawl job to MySQL: {e}")

        return extraction_data

    def _persist_to_mysql(self, job_uuid: str, url: str, data: Dict[str, Any], execution_time_ms: int):
        val = data.get("validation", {})
        job = CrawlJob(
            job_id=job_uuid,
            target_url=url,
            http_status=data.get("http_status", 200),
            status="SUCCESS",
            quality_score=val.get("quality_score", 0),
            quality_rating=val.get("quality_rating", "UNKNOWN"),
            execution_time_ms=execution_time_ms
        )
        self.db.add(job)
        self.db.flush()

        slots_summary = data.get("ad_slots_summary", [])
        for s in slots_summary:
            dims = s.get("dimensions", {})
            slot_record = AdSlotModel(
                crawl_job_id=job.id,
                slot_id=s.get("slot_id", "unknown"),
                ad_unit_path=s.get("ad_unit_path"),
                width=dims.get("width", 0),
                height=dims.get("height", 0),
                declared_sizes=json.dumps(s.get("declared_sizes", [])),
                is_visible=s.get("is_visible", False),
                monetization_type=s.get("monetization_type", "UNKNOWN"),
                winning_bidder=s.get("winning_bidder", "None"),
                winning_cpm=s.get("winning_cpm", 0.0),
                currency=s.get("currency", "USD"),
                creative_asset_url=s.get("creative_asset_url"),
                destination_click_url=s.get("destination_click_url")
            )
            self.db.add(slot_record)

        bidders = data.get("header_bidding", {}).get("bidder_summary", [])
        for b in bidders:
            bidder_record = BidderSummaryModel(
                crawl_job_id=job.id,
                bidder_code=b.get("bidder", "unknown"),
                bids_count=b.get("bids_count", 0),
                max_cpm=b.get("max_cpm", 0.0),
                avg_cpm=b.get("avg_cpm", 0.0),
                avg_latency_ms=b.get("avg_latency_ms", 0),
                source=b.get("source", "client_prebid")
            )
            self.db.add(bidder_record)

        iframes = data.get("rendered_iframes", [])
        for f in iframes:
            iframe_record = RenderedIframeModel(
                crawl_job_id=job.id,
                frame_id=f.get("id", "iframe-unknown"),
                frame_type=f.get("frame_type"),
                width=f.get("width", 0),
                height=f.get("height", 0),
                is_visible=f.get("is_visible", False),
                resolved_creative_url=f.get("resolved_creative_url"),
                ad_clickthrough_url=f.get("ad_clickthrough_url")
            )
            self.db.add(iframe_record)

        payload_record = CrawlPayloadModel(
            crawl_job_id=job.id,
            raw_json=json.dumps(data, ensure_ascii=False)
        )
        self.db.add(payload_record)
        self.db.commit()
        logger.info(f"Persisted crawl job {job_uuid} into MySQL successfully.")
