import logging
from typing import Dict, Any, List
from urllib.parse import urlparse
from playwright.async_api import Page

logger = logging.getLogger(__name__)

class DOMExtractor:
    @staticmethod
    async def extract(page: Page) -> Dict[str, Any]:
        try:
            dom_data = await page.evaluate("""
                () => {
                    const currentHost = window.location.hostname;
                    const title = document.title || '';
                    const canonicalEl = document.querySelector('link[rel="canonical"]');
                    const canonicalUrl = canonicalEl ? canonicalEl.href : window.location.href;
                    const bodyTextSample = document.body ? document.body.innerText.substring(0, 500) : '';

                    const anchors = Array.from(document.querySelectorAll('a[href]'));
                    let internalLinks = 0;
                    let externalLinks = 0;
                    const sampleExternalLinks = [];

                    anchors.forEach(a => {
                        try {
                            const u = new URL(a.href, window.location.href);
                            if (u.hostname === currentHost || u.hostname.endsWith('.' + currentHost)) {
                                internalLinks++;
                            } else if (u.protocol.startsWith('http')) {
                                externalLinks++;
                                if (sampleExternalLinks.length < 15) {
                                    sampleExternalLinks.push(a.href);
                                }
                            }
                        } catch(e){}
                    });

                    const iframes = Array.from(document.querySelectorAll('iframe'));
                    const iframeDetails = iframes.map((f, index) => {
                        const rect = f.getBoundingClientRect();
                        let src = f.src || f.getAttribute('data-src') || 'about:blank';
                        const id = f.id || `iframe-${index}`;
                        const name = f.name || '';
                        
                        let isAdIframe = false;
                        let innerType = "Standard Frame";

                        const adSignatures = ['google_ads_iframe', 'googletag', 'doubleclick', 'rubicon', 'criteo', 'amazon', 'openx', 'pubmatic', 'taboola', 'outbrain', 'adnxs', 'gptm'];
                        if (adSignatures.some(sig => id.toLowerCase().includes(sig) || src.toLowerCase().includes(sig) || name.toLowerCase().includes(sig))) {
                            isAdIframe = true;
                        }

                        let isCrossOrigin = false;
                        try {
                            if (src !== 'about:blank' && !src.startsWith('javascript:')) {
                                isCrossOrigin = new URL(src).hostname !== currentHost;
                            }
                        } catch(e){}

                        return {
                            id: id,
                            name: name,
                            src: src,
                            frame_type: innerType,
                            resolved_creative_url: null,
                            ad_clickthrough_url: null,
                            width: Math.round(rect.width),
                            height: Math.round(rect.height),
                            is_visible: rect.width > 0 && rect.height > 0 && window.getComputedStyle(f).display !== 'none',
                            is_ad_iframe: isAdIframe,
                            is_cross_origin: isCrossOrigin
                        };
                    });

                    const scriptEls = Array.from(document.querySelectorAll('script'));
                    const scripts = scriptEls.map(s => ({
                        src: s.src || null,
                        async: s.async,
                        defer: s.defer,
                        type: s.type || 'text/javascript',
                        is_inline: !s.src,
                        inline_length: s.src ? 0 : (s.textContent || '').length
                    }));

                    return {
                        title: title,
                        canonical_url: canonicalUrl,
                        final_url: window.location.href,
                        body_sample: bodyTextSample,
                        links_summary: {
                            total_links: anchors.length,
                            internal_links: internalLinks,
                            external_links: externalLinks,
                            sample_external: sampleExternalLinks
                        },
                        rendered_iframes: iframeDetails,
                        scripts_raw: scripts
                    };
                }
            """)

            rendered_iframes = dom_data.get("rendered_iframes", [])
            for frame_info in rendered_iframes:
                frame_id = frame_info.get("id")
                frame_name = frame_info.get("name")

                matched_frame = None
                for fr in page.frames:
                    if fr.name == frame_name or (fr.name and frame_id and frame_id in fr.name):
                        matched_frame = fr
                        break

                if matched_frame:
                    try:
                        inner_assets = await matched_frame.evaluate("""
                            () => {
                                const images = Array.from(document.querySelectorAll('img[src]')).map(i => i.src);
                                const links = Array.from(document.querySelectorAll('a[href]')).map(a => a.href);
                                const scripts = Array.from(document.querySelectorAll('script[src]')).map(s => s.src);
                                const videoSources = Array.from(document.querySelectorAll('video[src], source[src]')).map(v => v.src);

                                return {
                                    creative_image_url: images.length > 0 ? images[0] : null,
                                    ad_clickthrough_url: links.length > 0 ? links[0] : null,
                                    video_url: videoSources.length > 0 ? videoSources[0] : null,
                                    scripts_count: scripts.length
                                };
                            }
                        """)
                        if inner_assets:
                            frame_info["resolved_creative_url"] = inner_assets.get("creative_image_url") or inner_assets.get("video_url")
                            frame_info["ad_clickthrough_url"] = inner_assets.get("ad_clickthrough_url")
                            if frame_info["resolved_creative_url"] or frame_info["ad_clickthrough_url"]:
                                frame_info["frame_type"] = "Friendly IFrame (Creative Rendered)"
                                frame_info["is_ad_iframe"] = True
                            elif inner_assets.get("scripts_count", 0) > 0:
                                frame_info["frame_type"] = "Friendly IFrame (Ad Script Running)"
                                frame_info["is_ad_iframe"] = True
                    except Exception:
                        pass

            categorized_scripts = DOMExtractor._categorize_scripts(dom_data.get("scripts_raw", []), page.url)
            dom_data["third_party_scripts"] = categorized_scripts
            del dom_data["scripts_raw"]

            return dom_data

        except Exception as e:
            logger.error(f"DOM extraction error: {e}")
            return {"title": "", "canonical_url": page.url, "final_url": page.url, "error": str(e), "rendered_iframes": [], "third_party_scripts": []}

    @staticmethod
    def _categorize_scripts(scripts: List[Dict[str, Any]], page_url: str) -> List[Dict[str, Any]]:
        page_domain = urlparse(page_url).netloc
        categorized = []

        vendor_rules = {
            "Google AdTech": ["googletagservices.com", "doubleclick.net", "pagead2.googlesyndication.com", "adservice.google.com"],
            "Google Analytics / GTM": ["google-analytics.com", "googletagmanager.com"],
            "Amazon AdTech": ["amazon-adsystem.com", "aaxads.com", "apstag"],
            "Prebid / Header Bidding": ["prebid.js", "pbjs"],
            "Rubicon / Magnite": ["rubiconproject.com", "magnite.com"],
            "Index Exchange": ["indexww.com", "casalemedia.com"],
            "Criteo": ["criteo.com", "criteo.net"],
            "AppNexus / Xandr": ["adnxs.com"],
            "PubMatic": ["pubmatic.com"],
            "OpenX": ["openx.net"],
            "Taboola / Outbrain": ["taboola.com", "outbrain.com"],
            "OneTrust / CMP": ["onetrust.com", "cookielaw.org", "cmp"],
            "Permutive / Analytics": ["permutive.com", "chartbeat.com", "comscore.com"]
        }

        for s in scripts:
            src = s.get("src")
            if not src:
                continue

            src_domain = urlparse(src).netloc.lower()
            if not src_domain or page_domain in src_domain:
                continue

            vendor = "Other Third Party"
            for v_name, keywords in vendor_rules.items():
                if any(kw in src.lower() for kw in keywords):
                    vendor = v_name
                    break

            categorized.append({
                "src": src,
                "domain": src_domain,
                "vendor_category": vendor,
                "async": s.get("async", False),
                "defer": s.get("defer", False)
            })

        return categorized
