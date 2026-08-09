import logging
from typing import Dict, Any
from playwright.async_api import Page

logger = logging.getLogger(__name__)

class PrebidExtractor:
    @staticmethod
    async def extract(page: Page) -> Dict[str, Any]:
        try:
            return await page.evaluate("""
                () => {
                    const res = {
                        detected: false,
                        version: null,
                        amazon_tam_detected: false,
                        ad_units_count: 0,
                        ad_units: [],
                        bid_responses: {},
                        winning_bids: [],
                        bidder_summary: []
                    };

                    if (typeof window.apstag !== 'undefined') {
                        res.amazon_tam_detected = true;
                    }

                    if (typeof window.pbjs !== 'undefined') {
                        res.detected = true;
                        res.version = window.pbjs.version || null;
                    }

                    const pb = window.pbjs || {};

                    let adUnitsList = [];
                    if (Array.isArray(pb.adUnits) && pb.adUnits.length > 0) {
                        adUnitsList = pb.adUnits.map(unit => ({
                            code: unit.code,
                            media_types: unit.mediaTypes || null,
                            bidders: Array.isArray(unit.bids) ? unit.bids.map(b => b.bidder) : []
                        }));
                    }

                    if (typeof pb.getHighestCpmBids === 'function') {
                        try {
                            const winners = pb.getHighestCpmBids() || [];
                            winners.forEach(w => {
                                res.winning_bids.push({
                                    ad_unit_code: w.adUnitCode || w.adUnit,
                                    bidder: w.bidder || w.bidderCode,
                                    cpm: w.cpm || 0,
                                    currency: w.currency || 'USD',
                                    width: w.width || 0,
                                    height: w.height || 0,
                                    creative_id: w.creativeId || null,
                                    source: 'prebid_client'
                                });
                            });
                        } catch(e){}
                    }

                    const summaryBidders = {};
                    const collectedResponses = {};

                    function addBidResponse(adUnitCode, bid) {
                        if (!adUnitCode || !bid) return;
                        const bidder = bid.bidder || bid.bidderCode || 'unknown';
                        const cpm = Number(bid.cpm || bid.hb_pb || 0);
                        const timeToRespond = bid.timeToRespond || bid.time_to_respond_ms || 0;

                        if (!collectedResponses[adUnitCode]) {
                            collectedResponses[adUnitCode] = [];
                        }

                        const existing = collectedResponses[adUnitCode].find(b => b.ad_id === bid.adId && b.bidder === bidder);
                        if (!existing) {
                            collectedResponses[adUnitCode].push({
                                bidder: bidder,
                                cpm: cpm,
                                currency: bid.currency || 'USD',
                                width: bid.width || 0,
                                height: bid.height || 0,
                                ad_id: bid.adId || null,
                                time_to_respond_ms: timeToRespond,
                                status: bid.status || 'rendered',
                                source: bid.source || 'prebid_client'
                            });
                        }

                        if (!summaryBidders[bidder]) {
                            summaryBidders[bidder] = {
                                bidder: bidder,
                                bids_count: 0,
                                max_cpm: 0,
                                total_cpm: 0,
                                total_latency: 0
                            };
                        }
                        summaryBidders[bidder].bids_count += 1;
                        summaryBidders[bidder].max_cpm = Math.max(summaryBidders[bidder].max_cpm, cpm);
                        summaryBidders[bidder].total_cpm += cpm;
                        summaryBidders[bidder].total_latency += timeToRespond;
                    }

                    if (typeof pb.getBidResponses === 'function') {
                        try {
                            const rawResponses = pb.getBidResponses() || {};
                            Object.keys(rawResponses).forEach(code => {
                                const val = rawResponses[code];
                                let bidsArr = [];
                                if (Array.isArray(val)) {
                                    bidsArr = val;
                                } else if (val && Array.isArray(val.bids)) {
                                    bidsArr = val.bids;
                                }
                                bidsArr.forEach(b => addBidResponse(code, b));
                            });
                        } catch(e){}
                    }

                    if (Array.isArray(pb._bidsReceived)) {
                        try {
                            pb._bidsReceived.forEach(bid => {
                                const code = bid.adUnitCode || bid.adUnit;
                                if (code) addBidResponse(code, bid);
                            });
                        } catch(e){}
                    }

                    if (typeof window.googletag !== 'undefined' && typeof window.googletag.pubads === 'function') {
                        try {
                            const slots = window.googletag.pubads().getSlots();
                            slots.forEach(slot => {
                                const code = slot.getSlotElementId();
                                
                                let slotWidth = 0;
                                let slotHeight = 0;
                                const el = document.getElementById(code);
                                if (el) {
                                    const rect = el.getBoundingClientRect();
                                    slotWidth = Math.round(rect.width);
                                    slotHeight = Math.round(rect.height);
                                }
                                if (slotWidth === 0 || slotHeight === 0) {
                                    try {
                                        const sizes = slot.getSizes();
                                        if (sizes && sizes.length > 0) {
                                            const s = sizes[0];
                                            if (typeof s === 'object' && typeof s.getWidth === 'function') {
                                                slotWidth = s.getWidth();
                                                slotHeight = s.getHeight();
                                            }
                                        }
                                    } catch(e){}
                                }
                                
                                const hbBidder = slot.getTargeting('hb_bidder')?.[0];
                                const hbPb = slot.getTargeting('hb_pb')?.[0];
                                const hbAdId = slot.getTargeting('hb_adid')?.[0];
                                const hbSize = slot.getTargeting('hb_size')?.[0];

                                if (hbBidder) {
                                    let w = slotWidth, h = slotHeight;
                                    if (hbSize && hbSize.includes('x')) {
                                        const parts = hbSize.split('x');
                                        w = parseInt(parts[0]);
                                        h = parseInt(parts[1]);
                                    }
                                    const cpmVal = hbPb ? parseFloat(hbPb) : 0;

                                    addBidResponse(code, {
                                        bidder: hbBidder,
                                        cpm: cpmVal,
                                        currency: 'USD',
                                        width: w,
                                        height: h,
                                        adId: hbAdId,
                                        status: 'gpt_key_value_winning_bid',
                                        source: 'gpt_targeting'
                                    });

                                    if (!res.winning_bids.some(wb => wb.ad_unit_code === code)) {
                                        res.winning_bids.push({
                                            ad_unit_code: code,
                                            bidder: hbBidder,
                                            cpm: cpmVal,
                                            currency: 'USD',
                                            width: w,
                                            height: h,
                                            creative_id: hbAdId,
                                            source: 'gpt_targeting'
                                        });
                                    }
                                }

                                const amzBid = slot.getTargeting('amznbid')?.[0];
                                const amzSz = slot.getTargeting('amznsz')?.[0];
                                if (amzBid) {
                                    let w = slotWidth, h = slotHeight;
                                    if (amzSz && amzSz.includes('x')) {
                                        const parts = amzSz.split('x');
                                        w = parseInt(parts[0]);
                                        h = parseInt(parts[1]);
                                    }
                                    addBidResponse(code, {
                                        bidder: 'amazon_tam',
                                        cpm: 0,
                                        currency: 'USD',
                                        width: w,
                                        height: h,
                                        adId: amzBid,
                                        status: 'amazon_tam_bid',
                                        source: 'amazon_tam'
                                    });
                                }

                                const respInfo = slot.getResponseInformation ? slot.getResponseInformation() : null;
                                if (respInfo && (!collectedResponses[code] || collectedResponses[code].length === 0)) {
                                    const creativeId = respInfo.creativeId ? String(respInfo.creativeId) : null;
                                    const lineItemId = respInfo.lineItemId ? String(respInfo.lineItemId) : null;
                                    const advertiserId = respInfo.advertiserId ? String(respInfo.advertiserId) : null;

                                    if (creativeId || lineItemId) {
                                        const bidderName = respInfo.serviceName === 'publisher_ads' ? 'gam_s2s_direct' : 'ad_server';
                                        
                                        addBidResponse(code, {
                                            bidder: bidderName,
                                            cpm: 0,
                                            currency: 'USD',
                                            width: slotWidth,
                                            height: slotHeight,
                                            adId: creativeId,
                                            status: 'gam_s2s_winner',
                                            source: 'gam_response_info'
                                        });

                                        if (!res.winning_bids.some(wb => wb.ad_unit_code === code)) {
                                            res.winning_bids.push({
                                                ad_unit_code: code,
                                                bidder: bidderName,
                                                cpm: 0,
                                                currency: 'USD',
                                                width: slotWidth,
                                                height: slotHeight,
                                                creative_id: creativeId,
                                                line_item_id: lineItemId,
                                                advertiser_id: advertiserId,
                                                source: 'gam_response_info'
                                            });
                                        }
                                    }
                                }
                            });
                        } catch(e){}
                    }

                    res.bid_responses = collectedResponses;

                    res.bidder_summary = Object.values(summaryBidders).map(b => ({
                        bidder: b.bidder,
                        bids_count: b.bids_count,
                        max_cpm: round(b.max_cpm, 2),
                        avg_cpm: b.bids_count ? round(b.total_cpm / b.bids_count, 2) : 0,
                        avg_latency_ms: b.bids_count ? Math.round(b.total_latency / b.bids_count) : 0
                    }));

                    if (adUnitsList.length === 0) {
                        const unitCodesMap = new Map();

                        if (typeof window.googletag !== 'undefined' && typeof window.googletag.pubads === 'function') {
                            try {
                                const slots = window.googletag.pubads().getSlots();
                                slots.forEach(s => {
                                    const code = s.getSlotElementId();
                                    const path = s.getAdUnitPath();
                                    if (code) {
                                        unitCodesMap.set(code, {
                                            code: code,
                                            ad_unit_path: path,
                                            source: 'gpt_slots_registry',
                                            bidders: (res.bid_responses[code] || []).map(b => b.bidder)
                                        });
                                    }
                                });
                            } catch(e){}
                        }

                        res.winning_bids.forEach(w => {
                            if (w.ad_unit_code && !unitCodesMap.has(w.ad_unit_code)) {
                                unitCodesMap.set(w.ad_unit_code, {
                                    code: w.ad_unit_code,
                                    source: 'reconstructed_from_auction_events',
                                    bidders: [w.bidder]
                                });
                            }
                        });

                        adUnitsList = Array.from(unitCodesMap.values());
                    }

                    res.ad_units = adUnitsList;
                    res.ad_units_count = adUnitsList.length;

                    function round(val, decimals) {
                        return Number(Math.round(val + 'e' + decimals) + 'e-' + decimals);
                    }

                    return res;
                }
            """)
        except Exception as e:
            logger.error(f"Prebid extraction error: {e}")
            return {"detected": False, "error": str(e), "ad_units_count": 0, "ad_units": [], "bid_responses": {}, "winning_bids": [], "bidder_summary": []}
