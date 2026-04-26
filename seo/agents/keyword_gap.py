#!/usr/bin/env python3
"""
Keyword opportunity / gap analysis for Rose Medical Pavilion.

Finds queries with high impressions but low clicks (CTR gap) and
queries ranking 5-20 that are close to page 1.

Usage:
  python keyword_gap.py --days 90

Requires: seo/credentials/gsc-service-account.json
"""

import argparse
import os
from datetime import date, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(SCRIPT_DIR, "../reports")
CREDS_PATH = os.path.join(SCRIPT_DIR, "../credentials/gsc-service-account.json")
SITE_URL = "https://rosemedicalpavilion.com"


def fetch_all_queries(days):
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
        "dimensions": ["query"],
        "rowLimit": 500,
        "orderBy": [{"fieldName": "impressions", "sortOrder": "DESCENDING"}]
    }
    result = service.searchanalytics().query(siteUrl=SITE_URL, body=body).execute()
    return result.get("rows", []), start, end


def build_report(days, rows, start, end):
    # High impressions, low CTR (title/meta opportunity)
    low_ctr = sorted(
        [r for r in rows if r["impressions"] > 50 and r["ctr"] < 0.03],
        key=lambda r: r["impressions"],
        reverse=True
    )[:25]

    # Positions 5–20 (quick wins — just outside top 4)
    quick_wins = sorted(
        [r for r in rows if 4 < r["position"] <= 20 and r["impressions"] > 20],
        key=lambda r: r["position"]
    )[:25]

    lines = [
        f"# Keyword Gap Analysis — Rose Medical Pavilion",
        f"**Period:** {start} to {end} ({days} days)  ",
        f"**Generated:** {date.today()}",
        "",
        "## High-Impression / Low-CTR (title/meta optimization opportunities)",
        "| Query | Impressions | Clicks | CTR | Position |",
        "|-------|-------------|--------|-----|----------|",
    ]
    for r in low_ctr:
        q = r["keys"][0]
        lines.append(
            f"| {q} | {r['impressions']:.0f} | {r['clicks']:.0f} | "
            f"{r['ctr']:.1%} | {r['position']:.1f} |"
        )

    lines += [
        "",
        "## Quick Wins — Positions 5–20 (content improvement opportunities)",
        "| Query | Position | Impressions | Clicks |",
        "|-------|----------|-------------|--------|",
    ]
    for r in quick_wins:
        q = r["keys"][0]
        lines.append(
            f"| {q} | {r['position']:.1f} | {r['impressions']:.0f} | {r['clicks']:.0f} |"
        )

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=90)
    args = parser.parse_args()

    print(f"Fetching GSC data for last {args.days} days...")
    rows, start, end = fetch_all_queries(args.days)
    report = build_report(args.days, rows, start, end)

    os.makedirs(REPORTS_DIR, exist_ok=True)
    out_path = os.path.join(REPORTS_DIR, f"keyword-gap-{date.today()}.md")
    with open(out_path, "w") as f:
        f.write(report)
    print(f"Report written to {out_path}")
    print(report[:1000])


if __name__ == "__main__":
    main()
