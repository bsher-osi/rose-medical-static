#!/usr/bin/env python3
"""
Core Web Vitals / PageSpeed monitor for Rose Medical Pavilion.

Tests key pages and reports LCP, FID/INP, CLS, Performance score.

Usage:
  python pagespeed_monitor.py
  python pagespeed_monitor.py --pages / /pediatric-epilepsy-phoenix/

Requires: PAGESPEED_API_KEY env var (optional — works without key at lower rate limit)
"""

import argparse
import os
import requests
from datetime import date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(SCRIPT_DIR, "../reports")
BASE_URL = "https://rosemedicalpavilion.com"
API_KEY = os.environ.get("PAGESPEED_API_KEY", "")

DEFAULT_PAGES = [
    "/",
    "/pediatric-epilepsy-phoenix/",
    "/pediatric-seizures-phoenix/",
    "/developmental-delays-phoenix/",
    "/pediatric-headaches-phoenix/",
    "/blogs/",
    "/about-us/",
    "/contact-us/",
]


def fetch_pagespeed(path, strategy="mobile"):
    url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    params = {
        "url": f"{BASE_URL}{path}",
        "strategy": strategy,
    }
    if API_KEY:
        params["key"] = API_KEY
    resp = requests.get(url, params=params, timeout=60)
    resp.raise_for_status()
    return resp.json()


def extract_metrics(data):
    cats = data.get("lighthouseResult", {}).get("categories", {})
    audits = data.get("lighthouseResult", {}).get("audits", {})
    score = cats.get("performance", {}).get("score", 0)

    def audit_display(key):
        a = audits.get(key, {})
        return a.get("displayValue", "n/a")

    return {
        "score": int((score or 0) * 100),
        "lcp": audit_display("largest-contentful-paint"),
        "fid": audit_display("max-potential-fid"),
        "cls": audit_display("cumulative-layout-shift"),
        "ttfb": audit_display("server-response-time"),
        "fcp": audit_display("first-contentful-paint"),
        "tbt": audit_display("total-blocking-time"),
    }


def score_emoji(score):
    if score >= 90:
        return "PASS"
    if score >= 50:
        return "WARN"
    return "FAIL"


def build_report(results):
    lines = [
        f"# PageSpeed Report — Rose Medical Pavilion",
        f"**Generated:** {date.today()}",
        "",
        "## Mobile Scores",
        "| Page | Score | LCP | CLS | FCP | TBT |",
        "|------|-------|-----|-----|-----|-----|",
    ]
    for path, m in results.items():
        lines.append(
            f"| `{path}` | {score_emoji(m['score'])} {m['score']} | "
            f"{m['lcp']} | {m['cls']} | {m['fcp']} | {m['tbt']} |"
        )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages", nargs="*", help="Pages to test (default: key pages)")
    args = parser.parse_args()

    pages = args.pages or DEFAULT_PAGES
    results = {}

    for path in pages:
        print(f"  testing: {path} ...", end=" ", flush=True)
        try:
            data = fetch_pagespeed(path, "mobile")
            m = extract_metrics(data)
            results[path] = m
            print(f"score={m['score']}")
        except Exception as e:
            print(f"ERROR: {e}")
            results[path] = {"score": 0, "lcp": "error", "fid": "error", "cls": "error",
                             "ttfb": "error", "fcp": "error", "tbt": "error"}

    report = build_report(results)
    os.makedirs(REPORTS_DIR, exist_ok=True)
    out_path = os.path.join(REPORTS_DIR, f"pagespeed-{date.today()}.md")
    with open(out_path, "w") as f:
        f.write(report)
    print(f"\nReport written to {out_path}")
    print(report)


if __name__ == "__main__":
    main()
