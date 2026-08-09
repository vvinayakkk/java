import logging
from typing import Dict, Any
from playwright.async_api import Page

logger = logging.getLogger(__name__)

class PerformanceExtractor:
    @staticmethod
    async def extract(page: Page) -> Dict[str, Any]:
        try:
            return await page.evaluate("""
                () => {
                    const res = {
                        ttfb_ms: 0,
                        dom_interactive_ms: 0,
                        dom_content_loaded_ms: 0,
                        load_time_ms: 0,
                        total_resources: 0
                    };

                    if (window.performance) {
                        const navEntries = performance.getEntriesByType('navigation');
                        if (navEntries && navEntries.length > 0) {
                            const nav = navEntries[0];
                            res.ttfb_ms = Math.round(nav.responseStart - nav.requestStart);
                            res.dom_interactive_ms = Math.round(nav.domInteractive);
                            res.dom_content_loaded_ms = Math.round(nav.domContentLoadedEventEnd);
                            res.load_time_ms = Math.round(nav.loadEventEnd);
                        } else if (performance.timing) {
                            const t = performance.timing;
                            res.ttfb_ms = Math.round(t.responseStart - t.requestStart);
                            res.dom_interactive_ms = Math.round(t.domInteractive - t.navigationStart);
                            res.dom_content_loaded_ms = Math.round(t.domContentLoadedEventEnd - t.navigationStart);
                            res.load_time_ms = Math.round(t.loadEventEnd - t.navigationStart);
                        }

                        const resources = performance.getEntriesByType('resource');
                        res.total_resources = resources.length;
                    }
                    return res;
                }
            """)
        except Exception as e:
            logger.error(f"Performance extraction error: {e}")
            return {"ttfb_ms": 0, "dom_interactive_ms": 0, "dom_content_loaded_ms": 0, "load_time_ms": 0, "total_resources": 0, "error": str(e)}
