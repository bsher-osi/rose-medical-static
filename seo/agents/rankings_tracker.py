#!/usr/bin/env python3
"""
Google Search Console keyword rankings report for Rose Medical Pavilion.

Usage:
  python rankings_tracker.py --days 28
  python rankings_tracker.py --days 90 --top 50

Requires: seo/credentials/gsc-service-account.json
"""

import argparse
import os
from datetime import date, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(SCRIPT_DIR, "../reports")
CREDS_PATH = os.path.join(SCRIPT_DIR, "../credentials/gsc-service-account.json")
SITE_URL = "https://rosemedicalpavilion.com"


def fetch_rankings(days, top):
    from googleapiclient.discovery import build
    from google.oauth2.service_account import Credentials

    creds = Credentials.from_service_account_file(
        CREDS_PATH,
        scopes=["https://www.googleapis.com/auth/webmasters.readonly"]
    )
    service = build("searchconsole", "v1", credentials=creds)

    end = date.today() - timedelta(days=3)  # GSC has ~3 day lag
    start = end - timedelta(days=days)

    body = {
        "startDate": str(start),
        "endDate": str(end),
        "dimensions": ["query"],
        "rowLimit": top,
        "orderBy": [{"fieldName": "clicks", "sortOrder": "DESCENDING"}]
    }
    result = service.searchanalytics().query(siteUrl=SITE_URL, body=body).execute()
    return result.get("rows", []), start, end


def fetch_page_rankings(days, top):
    from googleapiclient.discovery import build
    from google.oauth2.service_account import Credentials

    creds = Credentials.from_service_account_file(
        CREDS_PATH,
        scopes=["https://www.googleapis.com/auth/webmasters.readonly"]
    )
    service = build("searchconsole", "v1", credentials=creds)

    end = date.today() - timedelta(days=3)
    start = end - timedelta(days=days)

    body = {
        "startDate": str(start),
        "endDate": str(end),
        "dimensions": ["page"],
        "rowLimit": top,
        "orderBy": [{"fieldName": "clicks", "sortOrder": "DESCENDING"}]
    }
    result = service.searchanalytics().query(siteUrl=SITE_URL, body=body).execute()
    return result.get("rows", [])


def build_report(days, rows, page_rows, start, end):
    lines = [
        f"# GSC Rankings Report — Rose Medical Pavilion",
        f"**Period:** {start} to {end} ({days} days)  ",
        f"**Generated:** {date.today()}",
        "",
        "## Top Keywords",
        "| Query | Clicks | Impressions | CTR | Avg Position |",
        "|-------|--------|-------------|-----|--------------|",
    ]
    for r in rows:
        q = r["keys"][0]
        lines.append(
            f"| {q} | {r['clicks']:.0f} | {r['impressions']:.0f} | "
            f"{r['ctr']:.1%} | {r['position']:.1f} |"
        )

    lines += [
        "",
        "## Top Pages by Clicks",
        "| Page | Clicks | Impressions | CTR | Avg Position |",
        "|------|--------|-------------|-----|--------------|",
    ]
    for r in page_rows:
        page = r["keys"][0].replace(SITE_URL, "")
        lines.append(
            f"| `{page}` | {r['clicks']:.0f} | {r['impressions']:.0f} | "
            f"{r['ctr']:.1%} | {r['position']:.1f} |"
        )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=28)
    parser.add_argument("--top", type=int, default=50)
    args = parser.parse_args()

    print(f"Fetching GSC data for last {args.days} days...")
    rows, start, end = fetch_rankings(args.days, args.top)
    page_rows = fetch_page_rankings(args.days, args.top)
    report = build_report(args.days, rows, page_rows, start, end)

    os.makedirs(REPORTS_DIR, exist_ok=True)
    out_path = os.path.join(REPORTS_DIR, f"rankings-{date.today()}.md")
    with open(out_path, "w") as f:
        f.write(report)
    print(f"Report written to {out_path}")


if __name__ == "__main__":
    main()
