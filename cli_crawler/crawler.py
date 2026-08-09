import os
import sys
import asyncio
import logging
from typing import Dict, Any, List
from urllib.parse import urlparse
from datetime import datetime
from playwright.async_api import async_playwright, Page, BrowserContext

from extractors import (
    GPTExtractor,
    PrebidExtractor,
    DOMExtractor,
    NetworkInterceptor,
    PerformanceExtractor
)
from ads_txt import AdsTxtParser
from validator import QualityValidator

logger = logging.getLogger(__name__)

class ForbesAdTechCrawler:
    def __init__(self, headless: bool = True, output_dir: str = "./output", timeout_ms: int = 45000):
        self.headless = headless
        self.output_dir = output_dir
        self.timeout_ms = timeout_ms
        self.ads_txt_parser = AdsTxtParser(timeout=15)
        self.validator = QualityValidator()
        os.makedirs(os.path.join(output_dir, "screenshots"), exist_ok=True)

    async def crawl(self, target_url: str) -> Dict[str, Any]:
        if not target_url.startswith("http"):
            target_url = "https://" + target_url

        parsed_domain = urlparse(target_url).netloc.replace("www.", "")
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=self.headless,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-popup-blocking",
                    "--no-sandbox",
                    "--disable-setuid-sandbox"
                ]
            )
            context: BrowserContext = await browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                locale="en-US",
                timezone_id="America/New_York",
                device_scale_factor=1,
                has_touch=False
            )

            page: Page = await context.new_page()
            await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")

            network_interceptor = NetworkInterceptor()
            network_interceptor.attach(page)

            console_logs: List[Dict[str, Any]] = []
            page_errors: List[str] = []
            page.on("console", lambda msg: console_logs.append({"type": msg.type, "text": msg.text[:300]}))
            page.on("pageerror", lambda exc: page_errors.append(str(exc)[:300]))

            logger.info(f"Navigating to {target_url}...")
            response = await page.goto(target_url, wait_until="domcontentloaded", timeout=self.timeout_ms)
            http_status = response.status if response else 0

            await self._handle_cmp_consent(page)
            await self._smooth_scroll(page)
            await page.wait_for_timeout(3000)

            viewport_shot_path = os.path.join(self.output_dir, "screenshots", f"{parsed_domain}_viewport_{timestamp_str}.png")
            fullpage_shot_path = os.path.join(self.output_dir, "screenshots", f"{parsed_domain}_fullpage_{timestamp_str}.png")
            await page.screenshot(path=viewport_shot_path, full_page=False)
            await page.screenshot(path=fullpage_shot_path, full_page=True)

            logger.info("Extracting AdTech parameters...")
            gpt_data = await GPTExtractor.extract(page)
            prebid_data = await PrebidExtractor.extract(page)
            dom_data = await DOMExtractor.extract(page)
            performance_data = await PerformanceExtractor.extract(page)
            raw_cookies = await context.cookies()
            cookies_data = self._format_cookies(raw_cookies, target_url)
            net_summary = network_interceptor.get_summary()
            net_bidders = net_summary.get("network_bidders", [])

            if not prebid_data.get("bidder_summary") and net_bidders:
                prebid_data["detected"] = True
                prebid_data["s2s_network_bidding_detected"] = True
                prebid_data["bidder_summary"] = [
                    {
                        "bidder": b["bidder"],
                        "bids_count": b["call_count"],
                        "max_cpm": 0,
                        "avg_cpm": 0,
                        "avg_latency_ms": 0,
                        "source": "network_interception"
                    }
                    for b in net_bidders
                ]

            ads_txt_data = self.ads_txt_parser.fetch_and_parse(target_url, "ads.txt")
            app_ads_txt_data = self.ads_txt_parser.fetch_and_parse(target_url, "app-ads.txt")

            await browser.close()

            ad_slots_summary = self._build_unified_ad_slots_summary(gpt_data, prebid_data, dom_data)

            extraction_data = {
                "target_url": target_url,
                "http_status": http_status,
                "ad_slots_summary": ad_slots_summary,
                "screenshots": {
                    "viewport": viewport_shot_path,
                    "full_page": fullpage_shot_path
                },
                "page_metadata": {
                    "title": dom_data.get("title", ""),
                    "canonical_url": dom_data.get("canonical_url", target_url),
                    "final_url": dom_data.get("final_url", target_url),
                    "body_sample": dom_data.get("body_sample", ""),
                    "links_summary": dom_data.get("links_summary", {})
                },
                "gpt_status": gpt_data,
                "header_bidding": prebid_data,
                "rendered_iframes": dom_data.get("rendered_iframes", []),
                "third_party_scripts": dom_data.get("third_party_scripts", []),
                "network_summary": net_summary,
                "cookies": cookies_data,
                "console_messages": {
                    "logs": console_logs[:200],
                    "page_errors": page_errors[:50]
                },
                "performance": performance_data,
                "ads_txt": ads_txt_data,
                "app_ads_txt": app_ads_txt_data
            }

            validation_result = self.validator.evaluate(extraction_data)
            extraction_data["validation"] = validation_result

            logger.info(f"Extraction Completed. Quality Score: {validation_result['quality_score']}/100 ({validation_result['quality_rating']})")
            return extraction_data

    async def _handle_cmp_consent(self, page: Page):
        consent_selectors = [
            "#onetrust-accept-btn-handler",
            "button[id*='accept']",
            "button[class*='accept']",
            ".truste-button1",
            "button:has-text('Accept')",
            "button:has-text('Agree')",
            "button:has-text('I Accept')"
        ]
        for sel in consent_selectors:
            try:
                el = page.locator(sel).first
                if await el.is_visible(timeout=1500):
                    await el.click(force=True)
                    await asyncio.sleep(1.5)
                    break
            except Exception:
                continue

    async def _smooth_scroll(self, page: Page):
        try:
            await page.evaluate("""
                async () => {
                    await new Promise((resolve) => {
                        let totalHeight = 0;
                        const distance = 400;
                        const timer = setInterval(() => {
                            const scrollHeight = document.body.scrollHeight;
                            window.scrollBy(0, distance);
                            totalHeight += distance;

                            if(totalHeight >= scrollHeight || totalHeight >= 4000){
                                clearInterval(timer);
                                window.scrollTo(0, 0);
                                resolve();
                            }
                        }, 250);
                    });
                }
            """)
        except Exception:
            pass

    def _format_cookies(self, raw_cookies: List[Dict[str, Any]], target_url: str) -> List[Dict[str, Any]]:
        page_domain = urlparse(target_url).netloc
        formatted = []
        for c in raw_cookies:
            domain = c.get("domain", "").lstrip(".")
            is_first_party = page_domain in domain or domain in page_domain
            formatted.append({
                "name": c.get("name"),
                "value": c.get("value")[:50] + "..." if len(c.get("value", "")) > 50 else c.get("value"),
                "domain": c.get("domain"),
                "path": c.get("path"),
                "expires": c.get("expires"),
                "http_only": c.get("httpOnly"),
                "secure": c.get("secure"),
                "same_site": c.get("sameSite"),
                "party": "1st Party" if is_first_party else "3rd Party"
            })
        return formatted

    def _build_unified_ad_slots_summary(self, gpt_data: Dict[str, Any], prebid_data: Dict[str, Any], dom_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        slots = gpt_data.get("slots", [])
        winning_bids = prebid_data.get("winning_bids", [])
        iframes = dom_data.get("rendered_iframes", [])
        
        summary = []
        for s in slots:
            code = s.get("element_id")
            path = s.get("ad_unit_path")
            
            wb = next((w for w in winning_bids if w.get("ad_unit_code") == code), {})
            frame = next((f for f in iframes if code and code in f.get("id", "")), {})
            
            creative_url = frame.get("resolved_creative_url")
            click_url = frame.get("ad_clickthrough_url")
            
            w = s.get("rendered_size", {}).get("width", 0) if s.get("rendered_size") else 0
            h = s.get("rendered_size", {}).get("height", 0) if s.get("rendered_size") else 0

            bidder = wb.get("bidder") or "None"
            monetization = "AD_SERVER_DIRECT"

            if bidder != "None" and bidder != "ad_server" and bidder != "gam_s2s_direct":
                monetization = "HEADER_BIDDING"
            elif bidder == "ad_server":
                monetization = "AD_SERVER_DIRECT"
            elif not s.get("is_visible", False) or (w == 0 and h == 0):
                monetization = "UNFILLED_OR_HIDDEN"
            elif prebid_data.get("amazon_tam_detected"):
                monetization = "AMAZON_TAM"
            elif prebid_data.get("s2s_network_bidding_detected"):
                monetization = "S2S_HEADER_BIDDING"

            summary.append({
                "slot_id": code,
                "ad_unit_path": path,
                "dimensions": {"width": w, "height": h},
                "declared_sizes": s.get("declared_sizes", []),
                "is_visible": s.get("is_visible", False),
                "monetization_type": monetization,
                "winning_bidder": bidder,
                "winning_cpm": wb.get("cpm", 0.0),
                "currency": wb.get("currency", "USD"),
                "creative_asset_url": creative_url,
                "destination_click_url": click_url
            })
        return summary
