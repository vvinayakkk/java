import logging
from typing import Dict, Any, List
from urllib.parse import urlparse
import requests

logger = logging.getLogger(__name__)

class AdsTxtParser:
    def __init__(self, timeout: int = 15):
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/plain, text/html, */*"
        }

    def fetch_and_parse(self, base_url: str, filename: str = "ads.txt") -> Dict[str, Any]:
        parsed_url = urlparse(base_url)
        domain = parsed_url.netloc or parsed_url.path.split('/')[0]
        scheme = parsed_url.scheme or "https"
        target_url = f"{scheme}://{domain}/{filename}"

        result = {
            "file_name": filename,
            "target_url": target_url,
            "status_code": None,
            "fetched": False,
            "error": None,
            "raw_line_count": 0,
            "valid_record_count": 0,
            "direct_count": 0,
            "reseller_count": 0,
            "unique_exchange_domains": 0,
            "top_exchanges": [],
            "records": []
        }

        try:
            resp = requests.get(target_url, headers=self.headers, timeout=self.timeout, allow_redirects=True)
            result["status_code"] = resp.status_code
            if resp.status_code == 200:
                result["fetched"] = True
                result.update(self.parse_content(resp.text))
            else:
                result["error"] = f"HTTP status {resp.status_code}"
        except Exception as e:
            result["error"] = str(e)

        return result

    def parse_content(self, text_content: str) -> Dict[str, Any]:
        lines = text_content.splitlines()
        records: List[Dict[str, Any]] = []
        direct_count = 0
        reseller_count = 0
        exchange_counts: Dict[str, int] = {}

        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if "#" in line:
                line = line.split("#")[0].strip()
            if not line:
                continue

            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 3:
                exchange_domain = parts[0].lower()
                seller_id = parts[1]
                supply_type = parts[2].upper()
                cert_id = parts[3] if len(parts) > 3 else ""

                if supply_type not in ("DIRECT", "RESELLER"):
                    supply_type = "UNKNOWN"

                if supply_type == "DIRECT":
                    direct_count += 1
                elif supply_type == "RESELLER":
                    reseller_count += 1

                exchange_counts[exchange_domain] = exchange_counts.get(exchange_domain, 0) + 1

                records.append({
                    "line_number": line_num,
                    "exchange_domain": exchange_domain,
                    "seller_account_id": seller_id,
                    "supply_type": supply_type,
                    "certification_authority_id": cert_id
                })

        top_exchanges = [
            {"domain": dom, "count": cnt}
            for dom, cnt in sorted(exchange_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        ]

        return {
            "raw_line_count": len(lines),
            "valid_record_count": len(records),
            "direct_count": direct_count,
            "reseller_count": reseller_count,
            "unique_exchange_domains": len(exchange_counts),
            "top_exchanges": top_exchanges,
            "records": records[:100]
        }
