#!/usr/bin/env python3
"""
Weekly GA4 traffic digest for Rose Medical Pavilion.

Outputs a Markdown report to seo/reports/ga4-digest-YYYY-MM-DD.md

Usage:
  python ga4_digest.py --days 7
  python ga4_digest.py --days 28

Requires:
  seo/credentials/ga4-service-account.json
  GA4_PROPERTY_ID env var or update PROPERTY_ID below
"""

import argparse
import os
from datetime import date, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))
CREDS_PATH = os.path.join(SCRIPT_DIR, "../credentials/ga4-service-account.json")
REPORTS_DIR = os.path.join(SCRIPT_DIR, "../reports")

PROPERTY_ID = os.environ.get("GA4_PROPERTY_ID", "properties/XXXXXXXXX")


def run_report(days):
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        DateRange, Dimension, Metric, RunReportRequest, OrderBy
    )
    from google.oauth2.service_account import Credentials

    creds = Credentials.from_service_account_file(
        CREDS_PATH,
        scopes=["https://www.googleapis.com/auth/analytics.readonly"]
    )
    client = BetaAnalyticsDataClient(credentials=creds)

    end = date.today()
    start = end - timedelta(days=days)

    def req(**kwargs):
        return RunReportRequest(
            property=PROPERTY_ID,
            date_ranges=[DateRange(start_date=str(start), end_date=str(end))],
            **kwargs
        )

    # Overview
    overview = client.run_report(req(
        metrics=[
            Metric(name="sessions"),
            Metric(name="totalUsers"),
            Metric(name="newUsers"),
            Metric(name="bounceRate"),
            Metric(name="averageSessionDuration"),
        ]
    ))

    # Top pages
    top_pages = client.run_report(req(
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="sessions"), Metric(name="totalUsers")],
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
        limit=20,
    ))

    # Traffic sources
    sources = client.run_report(req(
        dimensions=[Dimension(name="sessionDefaultChannelGroup")],
        metrics=[Metric(name="sessions")],
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
    ))

    # Conversions (phone clicks, appointments)
    conversions = client.run_report(req(
        dimensions=[Dimension(name="eventName")],
        metrics=[Metric(name="eventCount")],
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="eventCount"), desc=True)],
    ))

    return overview, top_pages, sources, conversions, start, end


def build_report(days, overview, top_pages, sources, conversions, start, end):
    ov = overview.rows[0].metric_values if overview.rows else ["0"] * 5

    def mv(row, i):
        return row.metric_values[i].value

    lines = [
        f"# GA4 Traffic Digest — Rose Medical Pavilion",
        f"**Period:** {start} to {end} ({days} days)  ",
        f"**Generated:** {date.today()}",
        "",
        "## Overview",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Sessions | {mv(overview.rows[0], 0)} |",
        f"| Total Users | {mv(overview.rows[0], 1)} |",
        f"| New Users | {mv(overview.rows[0], 2)} |",
        f"| Bounce Rate | {float(mv(overview.rows[0], 3)):.1%} |",
        f"| Avg Session Duration | {float(mv(overview.rows[0], 4)):.0f}s |",
        "",
        "## Top Pages",
        "| Page | Sessions | Users |",
        "|------|----------|-------|",
    ]
    for row in top_pages.rows[:20]:
        path = row.dimension_values[0].value
        sess = row.metric_values[0].value
        users = row.metric_values[1].value
        lines.append(f"| `{path}` | {sess} | {users} |")

    lines += ["", "## Traffic Sources", "| Channel | Sessions |", "|---------|----------|"]
    for row in sources.rows:
        ch = row.dimension_values[0].value
        sess = row.metric_values[0].value
        lines.append(f"| {ch} | {sess} |")

    lines += ["", "## Events / Conversions", "| Event | Count |", "|-------|-------|"]
    for row in conversions.rows:
        ev = row.dimension_values[0].value
        ct = row.metric_values[0].value
        lines.append(f"| {ev} | {ct} |")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=7)
    args = parser.parse_args()

    print(f"Fetching GA4 data for last {args.days} days...")
    overview, top_pages, sources, conversions, start, end = run_report(args.days)
    report = build_report(args.days, overview, top_pages, sources, conversions, start, end)

    os.makedirs(REPORTS_DIR, exist_ok=True)
    out_path = os.path.join(REPORTS_DIR, f"ga4-digest-{date.today()}.md")
    with open(out_path, "w") as f:
        f.write(report)
    print(f"Report written to {out_path}")
    print(report[:500])


if __name__ == "__main__":
    main()
