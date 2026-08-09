import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "ONLINE"
    assert "version" in data

def test_cache_stats_endpoint():
    response = client.get("/api/v1/cache/stats")
    assert response.status_code == 200
    data = response.json()
    assert "redis_available" in data
    assert "adtech_cache_keys" in data

def test_cache_clear_endpoint():
    response = client.post("/api/v1/cache/clear")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True

def test_invalid_crawl_request():
    response = client.post("/api/v1/crawl", json={})
    assert response.status_code == 422
