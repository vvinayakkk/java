import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class CrawlJob(Base):
    __tablename__ = "crawl_jobs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    job_id = Column(String(36), unique=True, index=True, default=lambda: str(uuid.uuid4()))
    target_url = Column(String(512), index=True, nullable=False)
    http_status = Column(Integer, nullable=True)
    status = Column(String(32), default="PENDING")
    quality_score = Column(Integer, default=0)
    quality_rating = Column(String(32), default="UNKNOWN")
    execution_time_ms = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    ad_slots = relationship("AdSlotModel", back_populates="job", cascade="all, delete-orphan")
    bidders = relationship("BidderSummaryModel", back_populates="job", cascade="all, delete-orphan")
    iframes = relationship("RenderedIframeModel", back_populates="job", cascade="all, delete-orphan")
    payload = relationship("CrawlPayloadModel", back_populates="job", uselist=False, cascade="all, delete-orphan")

class AdSlotModel(Base):
    __tablename__ = "ad_slots"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    crawl_job_id = Column(Integer, ForeignKey("crawl_jobs.id"), nullable=False)
    slot_id = Column(String(255), nullable=False)
    ad_unit_path = Column(String(512), nullable=True)
    width = Column(Integer, default=0)
    height = Column(Integer, default=0)
    declared_sizes = Column(Text, nullable=True)
    is_visible = Column(Boolean, default=False)
    monetization_type = Column(String(64), nullable=True)
    winning_bidder = Column(String(128), nullable=True)
    winning_cpm = Column(Float, default=0.0)
    currency = Column(String(16), default="USD")
    creative_asset_url = Column(Text, nullable=True)
    destination_click_url = Column(Text, nullable=True)

    job = relationship("CrawlJob", back_populates="ad_slots")

class BidderSummaryModel(Base):
    __tablename__ = "bidder_summaries"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    crawl_job_id = Column(Integer, ForeignKey("crawl_jobs.id"), nullable=False)
    bidder_code = Column(String(128), nullable=False)
    bids_count = Column(Integer, default=0)
    max_cpm = Column(Float, default=0.0)
    avg_cpm = Column(Float, default=0.0)
    avg_latency_ms = Column(Integer, default=0)
    source = Column(String(64), nullable=True)

    job = relationship("CrawlJob", back_populates="bidders")

class RenderedIframeModel(Base):
    __tablename__ = "rendered_iframes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    crawl_job_id = Column(Integer, ForeignKey("crawl_jobs.id"), nullable=False)
    frame_id = Column(String(255), nullable=False)
    frame_type = Column(String(128), nullable=True)
    width = Column(Integer, default=0)
    height = Column(Integer, default=0)
    is_visible = Column(Boolean, default=False)
    resolved_creative_url = Column(Text, nullable=True)
    ad_clickthrough_url = Column(Text, nullable=True)

    job = relationship("CrawlJob", back_populates="iframes")

from sqlalchemy.dialects.mysql import LONGTEXT

class CrawlPayloadModel(Base):
    __tablename__ = "crawl_payloads"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    crawl_job_id = Column(Integer, ForeignKey("crawl_jobs.id"), nullable=False)
    raw_json = Column(Text().with_variant(LONGTEXT, "mysql"), nullable=False)

    job = relationship("CrawlJob", back_populates="payload")
