import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class QualityValidator:
    def evaluate(self, extraction_data: Dict[str, Any]) -> Dict[str, Any]:
        flags: List[str] = []
        recommendations: List[str] = []
        score = 100

        page_meta = extraction_data.get("page_metadata", {})
        gpt = extraction_data.get("gpt_status", {})
        prebid = extraction_data.get("header_bidding", {})
        network = extraction_data.get("network_summary", {})
        iframes = extraction_data.get("rendered_iframes", [])
        cookies = extraction_data.get("cookies", [])
        scripts = extraction_data.get("third_party_scripts", [])

        title = page_meta.get("title", "").lower()
        body_text = page_meta.get("body_sample", "").lower()
        bot_signatures = ["just a moment...", "verify you are human", "access denied", "cloudflare", "perimeterx", "datadome", "captcha"]
        if any(sig in title for sig in bot_signatures) or any(sig in body_text for sig in bot_signatures):
            flags.append("ANTI_BOT_CHALLENGE_DETECTED")
            recommendations.append("Apply stealth headers or residential proxies.")
            score -= 50

        gpt_ready = gpt.get("api_ready", False) or gpt.get("loaded", False)
        slots = gpt.get("slots", [])
        if not gpt_ready and len(slots) == 0:
            flags.append("GPT_OBJECT_MISSING_OR_NOT_READY")
            recommendations.append("Check if CMP consent banner blocked googletag.js.")
            score -= 25
        elif len(slots) == 0:
            flags.append("GPT_INITIALIZED_BUT_NO_SLOTS_FOUND")
            recommendations.append("Scroll DOM further down to trigger lazy loading.")
            score -= 15

        prebid_found = (
            prebid.get("detected", False) or 
            prebid.get("amazon_tam_detected", False) or 
            len(prebid.get("winning_bids", [])) > 0 or
            network.get("adtech_requests_count", 0) > 10
        )
        bid_responses = prebid.get("bid_responses", {})
        winning_bids = prebid.get("winning_bids", [])

        if not prebid_found:
            flags.append("PREBID_JS_NOT_DETECTED")
            recommendations.append("Publisher may use S2S or Amazon TAM header bidding.")
            score -= 10
        elif not bid_responses and not winning_bids and not prebid.get("amazon_tam_detected", False) and network.get("adtech_requests_count", 0) <= 10:
            flags.append("PREBID_DETECTED_BUT_NO_BIDS_CAPTURED")
            recommendations.append("Wait longer for pbjs auction to complete.")
            score -= 10

        total_requests = network.get("total_requests", 0)
        adtech_requests = network.get("adtech_requests_count", 0)
        if total_requests == 0:
            flags.append("NETWORK_INTERCEPTION_EMPTY")
            score -= 25
        elif adtech_requests == 0:
            flags.append("NO_ADTECH_NETWORK_CALLS_DETECTED")
            score -= 15

        if len(scripts) == 0:
            score -= 5
        if len(cookies) == 0:
            score -= 5

        final_score = max(0, min(100, score))
        if final_score >= 85:
            rating = "EXCELLENT"
        elif final_score >= 70:
            rating = "GOOD"
        elif final_score >= 50:
            rating = "INCOMPLETE"
        else:
            rating = "CRITICAL_FAILURE"

        return {
            "quality_score": final_score,
            "passed_validation": final_score >= 70,
            "quality_rating": rating,
            "flags": flags,
            "recommendations": recommendations,
            "metrics": {
                "gpt_slots_count": len(slots),
                "valid_gpt_slots": len([s for s in slots if s.get("ad_unit_path") or s.get("element_id")]),
                "prebid_detected": prebid_found,
                "bids_captured": len(bid_responses) + len(winning_bids) + sum(b.get("bids_count", 1) for b in prebid.get("bidder_summary", [])),
                "total_requests": total_requests,
                "adtech_requests": adtech_requests,
                "iframes_count": len(iframes),
                "cookies_count": len(cookies),
                "scripts_count": len(scripts)
            }
        }
