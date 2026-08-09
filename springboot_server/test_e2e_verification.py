import time
import requests
import json

BASE_URL = "http://127.0.0.1:8080"

def run_e2e_verification():
    print("=" * 65)
    print("  SPRING BOOT 3 END-TO-END FASTAPI-PARITY VERIFICATION SUITE")
    print("=" * 65)

    # 1. Health Check Test
    resp = requests.get(f"{BASE_URL}/")
    assert resp.status_code == 200, f"Health check failed: {resp.text}"
    print(f"[PASSED] Health Check Endpoint (Status: {resp.json().get('status')}, Framework: {resp.json().get('framework')})")

    # 2. Test 1: Single URL Crawl & Database Persistence (Cache Miss)
    print("\n--- Test 1: Executing Live Crawl Request (Cache Miss) ---")
    start_t = time.time()
    payload = {"url": "https://www.forbes.com", "forceRefresh": True}
    resp1 = requests.post(f"{BASE_URL}/api/v1/crawl", json=payload)
    t1 = time.time() - start_t
    assert resp1.status_code == 200, f"Crawl failed: {resp1.text}"
    data1 = resp1.json()
    job_id = data1.get("jobId")
    
    assert data1.get("cached") is False, "Expected cached=False on fresh crawl"
    assert data1.get("qualityScore") == 100, f"Expected qualityScore 100, got {data1.get('qualityScore')}"
    assert len(data1.get("adSlotsSummary", [])) > 0, "Ad slots summary should not be empty"
    print(f"[PASSED] Live Crawl Success! Job ID: {job_id}")
    print(f"         Time Taken: {t1:.2f}s | Quality Score: {data1.get('qualityScore')}/100 | Ad Slots: {len(data1.get('adSlotsSummary'))} | Cached: {data1.get('cached')}")

    # 3. Test 2: Cache Hit Verification
    print("\n--- Test 2: Executing Repeat Crawl Request (Cache Hit) ---")
    start_t = time.time()
    payload_cache = {"url": "https://www.forbes.com", "forceRefresh": False}
    resp2 = requests.post(f"{BASE_URL}/api/v1/crawl", json=payload_cache)
    t2 = time.time() - start_t
    assert resp2.status_code == 200, f"Repeat crawl failed: {resp2.text}"
    data2 = resp2.json()

    assert data2.get("cached") is True, "Expected cached=True on repeat request"
    assert t2 < 0.2, f"Expected instant cache response (<0.2s), got {t2:.2f}s"
    print(f"[PASSED] Cache Hit Verified!")
    print(f"         Time Taken: {t2:.4f}s (<0.2s) | Cached: {data2.get('cached')} | Ad Slots: {len(data2.get('adSlotsSummary'))}")

    # 4. Test 3: Force Refresh Verification
    print("\n--- Test 3: Executing Force Refresh Request ---")
    start_t = time.time()
    payload_force = {"url": "https://www.forbes.com", "forceRefresh": True}
    resp3 = requests.post(f"{BASE_URL}/api/v1/crawl", json=payload_force)
    t3 = time.time() - start_t
    assert resp3.status_code == 200, f"Force refresh failed: {resp3.text}"
    data3 = resp3.json()

    assert data3.get("cached") is False, "Expected cached=False on forceRefresh=True"
    print(f"[PASSED] Force Refresh Verified! Bypassed cache in {t3:.2f}s")

    # 5. Test 4: Database Persistence & History Retrieval
    print("\n--- Test 4: Database Persistence & History Retrieval ---")
    resp_list = requests.get(f"{BASE_URL}/api/v1/crawls?limit=10")
    assert resp_list.status_code == 200, f"List crawls failed: {resp_list.text}"
    history = resp_list.json()
    assert len(history) > 0, "Database history should contain saved jobs"
    print(f"[PASSED] MySQL DB History Verified! Found {len(history)} persisted crawl jobs.")

    resp_detail = requests.get(f"{BASE_URL}/api/v1/crawls/{job_id}")
    assert resp_detail.status_code == 200, f"Get detail failed: {resp_detail.text}"
    detail = resp_detail.json()
    assert detail.get("job_id") == job_id, "Job ID mismatch in DB detail query"
    print(f"[PASSED] MySQL DB Job Detail & Payload Blob Verified for Job ID {job_id}")

    # 6. Test 5: Redis Cache Stats & Clear Operations
    print("\n--- Test 5: Redis Cache Stats & Clear Operations ---")
    resp_stats = requests.get(f"{BASE_URL}/api/v1/cache/stats")
    assert resp_stats.status_code == 200
    stats = resp_stats.json()
    print(f"[PASSED] Cache Stats Endpoint: Total Keys: {stats.get('totalKeys')}, Mode: {stats.get('mode')}")

    resp_clear = requests.post(f"{BASE_URL}/api/v1/cache/clear")
    assert resp_clear.status_code == 200
    print(f"[PASSED] Cache Clear Endpoint Success: {resp_clear.json().get('message')}")

    print("\n" + "=" * 65)
    print("    SPRING BOOT 3 VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    run_e2e_verification()
