import json
import asyncio
import logging
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session

from app.config import settings
from app.db import get_db, init_db
from app.models import CrawlJob, CrawlPayloadModel
from app.redis_cache import cache_manager
from app.schemas import (
    CrawlRequest,
    BatchCrawlRequest,
    CrawlJobResponse,
    CrawlJobListItem,
    CacheStatsResponse
)
from app.services.crawl_service import CrawlService

logger = logging.getLogger(__name__)

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Enterprise-grade AdTech Web Crawler API powered by Playwright, MySQL & Redis",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    return {
        "title": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "ONLINE",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

@app.post("/api/v1/crawl", response_model=CrawlJobResponse)
async def trigger_single_crawl(req: CrawlRequest, db: Session = Depends(get_db)):
    service = CrawlService(db=db)
    try:
        data = await service.crawl_url(req.url, force_refresh=req.force_refresh)
        val = data.get("validation", {})
        return CrawlJobResponse(
            job_id=data.get("job_id", "unknown"),
            target_url=data.get("target_url", req.url),
            http_status=data.get("http_status", 200),
            status="SUCCESS",
            cached=data.get("cached", False),
            quality_score=val.get("quality_score", 0),
            quality_rating=val.get("quality_rating", "UNKNOWN"),
            ad_slots_summary=data.get("ad_slots_summary", []),
            data=data
        )
    except Exception as e:
        logger.error(f"Error during single crawl API execution: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/crawl/batch")
async def trigger_batch_crawl(req: BatchCrawlRequest, db: Session = Depends(get_db)):
    semaphore = asyncio.Semaphore(req.concurrency or settings.DEFAULT_CONCURRENCY)
    service = CrawlService(db=db)

    async def crawl_with_sem(url: str):
        async with semaphore:
            try:
                data = await service.crawl_url(url, force_refresh=req.force_refresh)
                val = data.get("validation", {})
                return {
                    "url": url,
                    "status": "SUCCESS",
                    "quality_score": val.get("quality_score", 0),
                    "quality_rating": val.get("quality_rating", "UNKNOWN"),
                    "job_id": data.get("job_id")
                }
            except Exception as e:
                return {"url": url, "status": "FAILED", "error": str(e)}

    tasks = [crawl_with_sem(u) for u in req.urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    successful = len([r for r in results if isinstance(r, dict) and r.get("status") == "SUCCESS"])
    return {
        "total_urls": len(req.urls),
        "successful_crawls": successful,
        "failed_crawls": len(req.urls) - successful,
        "results": results
    }

@app.get("/api/v1/crawls", response_model=List[CrawlJobListItem])
def list_crawl_jobs(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    if not db:
        raise HTTPException(status_code=503, detail="Database connection unavailable")
    jobs = db.query(CrawlJob).order_by(CrawlJob.created_at.desc()).offset(offset).limit(limit).all()
    return jobs

@app.get("/api/v1/crawls/{job_id}")
def get_crawl_job_detail(job_id: str, db: Session = Depends(get_db)):
    if not db:
        raise HTTPException(status_code=503, detail="Database connection unavailable")
    job = db.query(CrawlJob).filter(CrawlJob.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Crawl job not found")

    payload_record = db.query(CrawlPayloadModel).filter(CrawlPayloadModel.crawl_job_id == job.id).first()
    raw_payload = json.loads(payload_record.raw_json) if payload_record else {}

    return {
        "job_id": job.job_id,
        "target_url": job.target_url,
        "http_status": job.http_status,
        "status": job.status,
        "quality_score": job.quality_score,
        "quality_rating": job.quality_rating,
        "execution_time_ms": job.execution_time_ms,
        "created_at": job.created_at.isoformat() if hasattr(job.created_at, "isoformat") else str(job.created_at),
        "payload": raw_payload
    }

@app.get("/api/v1/crawls/{job_id}/report", response_class=HTMLResponse)
def get_crawl_html_report(job_id: str, db: Session = Depends(get_db)):
    if not db:
        raise HTTPException(status_code=503, detail="Database connection unavailable")
    job = db.query(CrawlJob).filter(CrawlJob.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Crawl job not found")

    payload_record = db.query(CrawlPayloadModel).filter(CrawlPayloadModel.crawl_job_id == job.id).first()
    if not payload_record:
        raise HTTPException(status_code=404, detail="Crawl payload missing")

    raw_payload = json.loads(payload_record.raw_json)
    from app.services.reporter import ReportGenerator, HTML_TEMPLATE
    from jinja2 import Template

    template = Template(HTML_TEMPLATE)
    html_content = template.render(**raw_payload)
    return HTMLResponse(content=html_content)

@app.get("/api/v1/cache/stats", response_model=CacheStatsResponse)
def get_cache_stats():
    return cache_manager.get_stats()

@app.post("/api/v1/cache/clear")
def clear_cache():
    success = cache_manager.flush()
    return {"success": success, "message": "Cache flushed successfully"}
