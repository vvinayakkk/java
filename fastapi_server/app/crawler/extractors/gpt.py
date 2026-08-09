import logging
from typing import Dict, Any
from playwright.async_api import Page

logger = logging.getLogger(__name__)

class GPTExtractor:
    @staticmethod
    async def extract(page: Page) -> Dict[str, Any]:
        try:
            return await page.evaluate("""
                () => {
                    const res = {
                        detected: false,
                        api_ready: false,
                        version: null,
                        page_targeting: {},
                        slots_count: 0,
                        slots: []
                    };

                    if (typeof window.googletag === 'undefined') return res;

                    res.detected = true;
                    const gt = window.googletag;
                    res.api_ready = Boolean(gt.apiReady);
                    
                    if (typeof gt.getVersion === 'function') {
                        try { res.version = gt.getVersion(); } catch(e){}
                    }

                    if (typeof gt.pubads === 'function') {
                        try {
                            const pubads = gt.pubads();
                            if (typeof pubads.getTargetingKeys === 'function') {
                                pubads.getTargetingKeys().forEach(key => {
                                    res.page_targeting[key] = pubads.getTargeting(key);
                                });
                            }

                            if (typeof pubads.getSlots === 'function') {
                                const rawSlots = pubads.getSlots();
                                res.slots_count = rawSlots.length;
                                res.slots = rawSlots.map(slot => {
                                    const slotData = {
                                        element_id: null,
                                        ad_unit_path: null,
                                        targeting: {},
                                        declared_sizes: [],
                                        rendered_size: null,
                                        response_info: null,
                                        is_visible: false
                                    };

                                    try { slotData.element_id = slot.getSlotElementId(); } catch(e){}
                                    try { slotData.ad_unit_path = slot.getAdUnitPath(); } catch(e){}

                                    try {
                                        slot.getTargetingKeys().forEach(k => {
                                            slotData.targeting[k] = slot.getTargeting(k);
                                        });
                                    } catch(e){}

                                    try {
                                        const sizes = slot.getSizes();
                                        slotData.declared_sizes = sizes.map(s => {
                                            if (typeof s === 'object' && s !== null && typeof s.getWidth === 'function') {
                                                return `${s.getWidth()}x${s.getHeight()}`;
                                            }
                                            return String(s);
                                        });
                                    } catch(e){}

                                    try {
                                        const resp = slot.getResponseInformation();
                                        if (resp) {
                                            slotData.response_info = {
                                                advertiser_id: resp.advertiserId || null,
                                                campaign_id: resp.campaignId || null,
                                                line_item_id: resp.lineItemId || null,
                                                creative_id: resp.creativeId || null,
                                                label_ids: resp.labelIds || []
                                            };
                                        }
                                    } catch(e){}

                                    if (slotData.element_id) {
                                        const el = document.getElementById(slotData.element_id);
                                        if (el) {
                                            const rect = el.getBoundingClientRect();
                                            slotData.rendered_size = {
                                                width: Math.round(rect.width),
                                                height: Math.round(rect.height)
                                            };
                                            slotData.is_visible = rect.width > 0 && rect.height > 0 && window.getComputedStyle(el).display !== 'none';
                                        }
                                    }
                                    return slotData;
                                });
                            }
                        } catch(e) {
                            res.error = e.toString();
                        }
                    }
                    return res;
                }
            """)
        except Exception as e:
            logger.error(f"GPT extraction error: {e}")
            return {"detected": False, "api_ready": False, "error": str(e), "slots_count": 0, "slots": []}
