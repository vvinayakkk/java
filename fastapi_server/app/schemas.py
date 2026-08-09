from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime

class CrawlRequest(BaseModel):
    url: str = Field(..., json_schema_extra={"example": "https://www.forbes.com"})
    force_refresh: bool = Field(default=False, description="Bypass Redis cache if True")

class BatchCrawlRequest(BaseModel):
    urls: List[str] = Field(..., json_schema_extra={"example": ["https://www.forbes.com", "https://techcrunch.com"]})
    concurrency: Optional[int] = Field(default=4, ge=1, le=20)
    force_refresh: Optional[bool] = Field(default=False)

class DimensionsSchema(BaseModel):
    width: int
    height: int

class AdSlotSummarySchema(BaseModel):
    slot_id: str
    ad_unit_path: Optional[str] = None
    dimensions: DimensionsSchema
    declared_sizes: List[str] = []
    is_visible: bool
    monetization_type: Optional[str] = "UNKNOWN"
    winning_bidder: Optional[str] = "None"
    winning_cpm: float = 0.0
    currency: str = "USD"
    creative_asset_url: Optional[str] = None
    destination_click_url: Optional[str] = None

class ValidationMetricsSchema(BaseModel):
    gpt_slots_count: int
    valid_gpt_slots: int
    prebid_detected: bool
    bids_captured: int
    total_requests: int
    adtech_requests: int
    iframes_count: int
    cookies_count: int
    scripts_count: int

class ValidationResultSchema(BaseModel):
    quality_score: int
    passed_validation: bool
    quality_rating: str
    flags: List[str] = []
    recommendations: List[str] = []
    metrics: ValidationMetricsSchema

class CrawlJobResponse(BaseModel):
    job_id: str
    target_url: str
    http_status: Optional[int] = 200
    status: str
    cached: bool = False
    quality_score: int
    quality_rating: str
    ad_slots_summary: List[AdSlotSummarySchema] = []
    data: Optional[Dict[str, Any]] = None

class CrawlJobListItem(BaseModel):
    job_id: str
    target_url: str
    http_status: Optional[int] = 200
    status: str = "SUCCESS"
    quality_score: int = 0
    quality_rating: str = "UNKNOWN"
    created_at: Optional[Any] = None

    model_config = {"from_attributes": True}

class CacheStatsResponse(BaseModel):
    redis_available: bool
    connected_clients: int = 0
    used_memory_human: str = "0B"
    total_keys: int = 0
    adtech_cache_keys: int = 0
