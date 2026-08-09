import logging
from typing import Dict, Any, List
from urllib.parse import urlparse
from playwright.async_api import Page, Response

logger = logging.getLogger(__name__)

class NetworkInterceptor:
    def __init__(self):
        self.requests: List[Dict[str, Any]] = []
        self.domain_counter: Dict[str, Dict[str, int]] = {}
        self.bidder_network_counter: Dict[str, int] = {}

        self.categories_summary: Dict[str, Dict[str, int]] = {
            "AdTech / Bidding": {"count": 0, "bytes": 0},
            "Analytics": {"count": 0, "bytes": 0},
            "Script": {"count": 0, "bytes": 0},
            "Media": {"count": 0, "bytes": 0},
            "XHR / Fetch": {"count": 0, "bytes": 0},
            "Stylesheet": {"count": 0, "bytes": 0},
            "Document": {"count": 0, "bytes": 0},
            "Other": {"count": 0, "bytes": 0}
        }

        self.adtech_vendor_map = {
            "rubicon": "rubiconproject.com",
            "magnite": "magnite.com",
            "appnexus": "adnxs.com",
            "index_exchange": "indexww.com",
            "openx": "openx.net",
            "criteo": "criteo.com",
            "pubmatic": "pubmatic.com",
            "amazon_tam": "amazon-adsystem.com",
            "triplelift": "triplelift.com",
            "unruly": "unrulymedia.com",
            "yieldmo": "yieldmo.com",
            "smartadserver": "smartadserver.com"
        }

        self.adtech_keywords = [
            "doubleclick", "googlesyndication", "googleadservices", "rubiconproject",
            "magnite", "indexww", "casalemedia", "criteo", "adnxs", "appnexus",
            "amazon-adsystem", "aaxads", "pubmatic", "openx", "taboola", "outbrain",
            "yieldmo", "triplelift", "360yield", "smartadserver", "prebid", "bidder", "unrulymedia"
        ]

        self.analytics_keywords = [
            "google-analytics", "analytics.google", "googletagmanager", "permutive",
            "chartbeat", "comscore", "scorecardresearch", "omtrdc", "hotjar", "segment"
        ]

    def attach(self, page: Page):
        page.on("response", self._handle_response)

    async def _handle_response(self, response: Response):
        try:
            req = response.request
            url = req.url
            method = req.method
            resource_type = req.resource_type
            status = response.status
            headers = response.headers
            content_type = headers.get("content-type", "")

            content_length = headers.get("content-length")
            body_bytes = int(content_length) if (content_length and content_length.isdigit()) else 0

            domain = urlparse(url).netloc.lower()
            category = self._classify(url, resource_type, content_type)

            self.categories_summary[category]["count"] += 1
            self.categories_summary[category]["bytes"] += body_bytes

            if domain not in self.domain_counter:
                self.domain_counter[domain] = {"count": 0, "bytes": 0}
            self.domain_counter[domain]["count"] += 1
            self.domain_counter[domain]["bytes"] += body_bytes

            for bidder_name, kw in self.adtech_vendor_map.items():
                if kw in domain or kw in url.lower():
                    self.bidder_network_counter[bidder_name] = self.bidder_network_counter.get(bidder_name, 0) + 1

            if len(self.requests) < 500:
                self.requests.append({
                    "url": url[:300],
                    "domain": domain,
                    "method": method,
                    "status": status,
                    "resource_type": resource_type,
                    "content_type": content_type,
                    "category": category,
                    "size_bytes": body_bytes
                })
        except Exception:
            pass

    def _classify(self, url: str, resource_type: str, content_type: str) -> str:
        url_lower = url.lower()
        if any(kw in url_lower for kw in self.adtech_keywords):
            return "AdTech / Bidding"
        if any(kw in url_lower for kw in self.analytics_keywords):
            return "Analytics"
        if resource_type == "script" or "javascript" in content_type:
            return "Script"
        if resource_type in ("image", "media", "font"):
            return "Media"
        if resource_type in ("xhr", "fetch"):
            return "XHR / Fetch"
        if resource_type == "stylesheet" or "css" in content_type:
            return "Stylesheet"
        if resource_type == "document" or "text/html" in content_type:
            return "Document"
        return "Other"

    def get_summary(self) -> Dict[str, Any]:
        total_requests = len(self.requests)
        total_bytes = sum(c["bytes"] for c in self.categories_summary.values())
        adtech_requests_count = self.categories_summary["AdTech / Bidding"]["count"]

        top_domains = [
            {"domain": dom, "count": info["count"], "bytes_mb": round(info["bytes"] / (1024 * 1024), 2)}
            for dom, info in sorted(self.domain_counter.items(), key=lambda x: x[1]["count"], reverse=True)[:15]
        ]

        network_bidders = [
            {"bidder": b, "call_count": cnt}
            for b, cnt in sorted(self.bidder_network_counter.items(), key=lambda x: x[1], reverse=True)
        ]

        return {
            "total_requests": total_requests,
            "total_transferred_bytes": total_bytes,
            "total_transferred_mb": round(total_bytes / (1024 * 1024), 2),
            "adtech_requests_count": adtech_requests_count,
            "categories": self.categories_summary,
            "top_domains": top_domains,
            "network_bidders": network_bidders,
            "sample_requests": self.requests[:100]
        }
