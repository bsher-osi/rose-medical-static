#!/usr/bin/env python3
"""
Appointment conversion tracking report for Rose Medical Pavilion.

Tracks phone_call, appointment_request, appointment_button_click events in GA4.

Usage:
  python conversion_tracker.py --days 7
  python conversion_tracker.py --days 30

Requires: seo/credentials/ga4-service-account.json
"""

import argparse
import os
from datetime import date, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(SCRIPT_DIR, "../reports")
CREDS_PATH = os.path.join(SCRIPT_DIR, "../credentials/ga4-service-account.json")
PROPERTY_ID = os.environ.get("GA4_PROPERTY_ID", "properties/XXXXXXXXX")

CONVERSION_EVENTS = [
    "phone_call",
    "appointment_request",
    "appointment_button_click",
    "schedule_online_click",
    "contact_form_submit",
]


def fetch_conversions(days):
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        DateRange, Dimension, Metric, RunReportRequest, FilterExpression,
        Filter, OrderBy
    )
    from google.oauth2.service_account import Credentials

    creds = Credentials.from_service_account_file(
        CREDS_PATH,
        scopes=["https://www.googleapis.com/auth/analytics.readonly"]
    )
    client = BetaAnalyticsDataClient(credentials=creds)

    end = date.today()
    start = end - timedelta(days=days)

    # Events by page
    by_page = client.run_report(RunReportRequest(
        property=PROPERTY_ID,
        date_ranges=[DateRange(start_date=str(start), end_date=str(end))],
        dimensions=[Dimension(name="pagePath"), Dimension(name="eventName")],
        metrics=[Metric(name="eventCount")],
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="eventCount"), desc=True)],
        limit=50,
    ))

    # Daily trend
    daily = client.run_report(RunReportRequest(
        property=PROPERTY_ID,
        date_ranges=[DateRange(start_date=str(start), end_date=str(end))],
        dimensions=[Dimension(name="date"), Dimension(name="eventName")],
        metrics=[Metric(name="eventCount")],
        order_bys=[OrderBy(dimension=OrderBy.DimensionOrderBy(dimension_name="date"))],
    ))

    return by_page, daily, start, end


def build_report(days, by_page, daily, start, end):
    conversion_rows = [
        r for r in by_page.rows
        if r.dimension_values[1].value in CONVERSION_EVENTS
    ]

    lines = [
        f"# Conversion Report — Rose Medical Pavilion",
        f"**Period:** {start} to {end} ({days} days)  ",
        f"**Generated:** {date.today()}",
        "",
        "## Conversion Events by Page",
        "| Page | Event | Count |",
        "|------|-------|-------|",
    ]
    for r in conversion_rows:
        page = r.dimension_values[0].value
        event = r.dimension_values[1].value
        count = r.metric_values[0].value
        lines.append(f"| `{page}` | {event} | {count} |")

    if not conversion_rows:
        lines.append("| — | No conversion events found | — |")

    lines += ["", "## All Events by Page (top 20)", "| Page | Event | Count |",
              "|------|-------|-------|"]
    for r in by_page.rows[:20]:
        page = r.dimension_values[0].value
        event = r.dimension_values[1].value
        count = r.metric_values[0].value
        lines.append(f"| `{page}` | {event} | {count} |")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=7)
    args = parser.parse_args()

    print(f"Fetching conversion data for last {args.days} days...")
    by_page, daily, start, end = fetch_conversions(args.days)
    report = build_report(args.days, by_page, daily, start, end)

    os.makedirs(REPORTS_DIR, exist_ok=True)
    out_path = os.path.join(REPORTS_DIR, f"conversions-{date.today()}.md")
    with open(out_path, "w") as f:
        f.write(report)
    print(f"Report written to {out_path}")
    print(report[:1000])


if __name__ == "__main__":
    main()
