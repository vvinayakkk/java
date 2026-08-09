import os
import json
import logging
from typing import Dict, Any
from datetime import datetime
from jinja2 import Template

logger = logging.getLogger(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AdTech Crawl Dashboard - {{ page_metadata.title }}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #0f172a;
            --card-bg: #1e293b;
            --card-border: #334155;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent-blue: #38bdf8;
            --accent-green: #4ade80;
            --accent-yellow: #facc15;
            --accent-red: #f87171;
            --accent-purple: #c084fc;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-dark);
            color: var(--text-main);
            padding: 2rem;
            line-height: 1.5;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid var(--card-border);
            margin-bottom: 2rem;
        }
        .header h1 { font-size: 1.8rem; color: var(--accent-blue); }
        .header .subtitle { color: var(--text-muted); font-size: 0.9rem; margin-top: 0.2rem; }
        .score-badge {
            background-color: rgba(74, 222, 128, 0.1);
            border: 1px solid var(--accent-green);
            color: var(--accent-green);
            padding: 0.5rem 1.2rem;
            border-radius: 8px;
            font-weight: 700;
            font-size: 1.2rem;
            text-align: center;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.2rem;
            margin-bottom: 2rem;
        }
        .metric-card {
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            padding: 1.2rem;
            border-radius: 10px;
        }
        .metric-card .title { color: var(--text-muted); font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; }
        .metric-card .value { font-size: 1.6rem; font-weight: 700; color: var(--accent-blue); margin-top: 0.4rem; }
        .section {
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 2rem;
        }
        .section-title {
            font-size: 1.2rem;
            color: var(--accent-purple);
            margin-bottom: 1rem;
            border-bottom: 1px solid var(--card-border);
            padding-bottom: 0.5rem;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.88rem;
        }
        th, td {
            text-align: left;
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--card-border);
        }
        th { color: var(--text-muted); font-weight: 600; background-color: rgba(15, 23, 42, 0.5); }
        tr:hover { background-color: rgba(255, 255, 255, 0.02); }
        .badge {
            display: inline-block;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .badge-green { background: rgba(74, 222, 128, 0.2); color: var(--accent-green); }
        .badge-blue { background: rgba(56, 189, 248, 0.2); color: var(--accent-blue); }
        .badge-yellow { background: rgba(250, 204, 21, 0.2); color: var(--accent-yellow); }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>AdTech Analytics Dashboard</h1>
            <div class="subtitle">Target: <a href="{{ target_url }}" target="_blank" style="color: var(--accent-blue);">{{ target_url }}</a> | Status: {{ http_status }}</div>
        </div>
        <div class="score-badge">
            Score: {{ validation.quality_score }}/100 ({{ validation.quality_rating }})
        </div>
    </div>

    <div class="metrics-grid">
        <div class="metric-card">
            <div class="title">Ad Slots Summary</div>
            <div class="value">{{ ad_slots_summary|length }}</div>
        </div>
        <div class="metric-card">
            <div class="title">AdTech Network Calls</div>
            <div class="value">{{ network_summary.adtech_requests_count }}</div>
        </div>
        <div class="metric-card">
            <div class="title">Prebid / S2S Bidders</div>
            <div class="value">{{ header_bidding.bidder_summary|length }}</div>
        </div>
        <div class="metric-card">
            <div class="title">ads.txt Direct Sellers</div>
            <div class="value">{{ ads_txt.direct_count }}</div>
        </div>
    </div>

    <div class="section">
        <div class="section-title">Ad Slots & Monetization Summary</div>
        <table>
            <thead>
                <tr>
                    <th>Slot ID</th>
                    <th>Ad Unit Path</th>
                    <th>Rendered Size</th>
                    <th>Monetization</th>
                    <th>Winning Bidder</th>
                    <th>Winning CPM</th>
                    <th>Creative Asset URL</th>
                </tr>
            </thead>
            <tbody>
                {% for slot in ad_slots_summary %}
                <tr>
                    <td><strong>{{ slot.slot_id }}</strong></td>
                    <td style="color: var(--text-muted);">{{ slot.ad_unit_path }}</td>
                    <td>{{ slot.dimensions.width }}x{{ slot.dimensions.height }}</td>
                    <td><span class="badge badge-blue">{{ slot.monetization_type }}</span></td>
                    <td><span class="badge badge-green">{{ slot.winning_bidder }}</span></td>
                    <td>${{ "%.4f"|format(slot.winning_cpm) }}</td>
                    <td style="max-width: 250px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                        {% if slot.creative_asset_url %}
                        <a href="{{ slot.creative_asset_url }}" target="_blank" style="color: var(--accent-blue);">View Asset</a>
                        {% else %}
                        <span style="color: var(--text-muted);">N/A</span>
                        {% endif %}
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <div class="section">
        <div class="section-title">Rendered IFrames & Creative Piercing</div>
        <table>
            <thead>
                <tr>
                    <th>Frame ID</th>
                    <th>Dimensions</th>
                    <th>Frame Type</th>
                    <th>Resolved Creative URL</th>
                    <th>Clickthrough Landing URL</th>
                </tr>
            </thead>
            <tbody>
                {% for iframe in rendered_iframes %}
                <tr>
                    <td>{{ iframe.id }}</td>
                    <td>{{ iframe.width }}x{{ iframe.height }}</td>
                    <td><span class="badge badge-yellow">{{ iframe.frame_type }}</span></td>
                    <td style="max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                        {% if iframe.resolved_creative_url %}
                        <a href="{{ iframe.resolved_creative_url }}" target="_blank" style="color: var(--accent-green);">{{ iframe.resolved_creative_url }}</a>
                        {% else %}
                        <span style="color: var(--text-muted);">N/A</span>
                        {% endif %}
                    </td>
                    <td style="max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                        {% if iframe.ad_clickthrough_url %}
                        <a href="{{ iframe.ad_clickthrough_url }}" target="_blank" style="color: var(--accent-blue);">{{ iframe.ad_clickthrough_url }}</a>
                        {% else %}
                        <span style="color: var(--text-muted);">N/A</span>
                        {% endif %}
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <div class="section">
        <div class="section-title">Demand Partner Bidders Summary</div>
        <table>
            <thead>
                <tr>
                    <th>Bidder Code</th>
                    <th>Bids / Calls Count</th>
                    <th>Max CPM</th>
                    <th>Avg CPM</th>
                    <th>Avg Latency (ms)</th>
                </tr>
            </thead>
            <tbody>
                {% for bidder in header_bidding.bidder_summary %}
                <tr>
                    <td><strong>{{ bidder.bidder }}</strong></td>
                    <td>{{ bidder.bids_count }}</td>
                    <td>${{ bidder.max_cpm }}</td>
                    <td>${{ bidder.avg_cpm }}</td>
                    <td>{{ bidder.avg_latency_ms }} ms</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
"""

class ReportGenerator:
    def __init__(self, output_dir: str = "./output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def save_json(self, extraction_data: Dict[str, Any], filename_prefix: str = "forbes_adtech") -> str:
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp_str}.json"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(extraction_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Saved JSON result to {filepath}")
        return filepath

    def generate_html_report(self, extraction_data: Dict[str, Any], filename_prefix: str = "forbes_report") -> str:
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp_str}.html"
        filepath = os.path.join(self.output_dir, filename)

        template = Template(HTML_TEMPLATE)
        html_content = template.render(**extraction_data)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)

        logger.info(f"Generated HTML report at {filepath}")
        return filepath
