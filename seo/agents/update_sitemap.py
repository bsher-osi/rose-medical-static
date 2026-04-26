#!/usr/bin/env python3
"""
Auto-regenerate sitemap.xml for Rose Medical Pavilion static site.

Crawls all .html files, assigns priority/changefreq by URL pattern,
and writes sitemap.xml to the repo root.

Usage:
  python update_sitemap.py
  python update_sitemap.py --dry-run
"""

import argparse
import os
from datetime import date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))
BASE_URL = "https://rosemedicalpavilion.com"

EXCLUDE_DIRS = {"wp-content", "wp-includes", "wp-admin", "seo", ".github", ".git"}
EXCLUDE_PREFIXES = ("wp-", "_")


def get_priority_and_freq(rel_path):
    parts = rel_path.strip("/").split("/")
    slug = parts[0] if parts else ""

    if rel_path in ("", "index.html"):
        return "1.0", "weekly"
    if slug in ("about-us", "contact-us", "schedule-online", "refer-a-patient"):
        return "0.9", "monthly"
    if slug in ("blogs",) and len(parts) == 1:
        return "0.8", "weekly"
    if slug == "blogs" and len(parts) >= 2:
        return "0.65", "monthly"
    # Service phoenix pages (original)
    if slug.endswith("-phoenix") and len(parts) == 1:
        return "0.85", "monthly"
    # City landing pages — service-city combos
    if len(parts) == 1 and "-" in slug and not slug.endswith("-phoenix"):
        return "0.70", "monthly"
    return "0.5", "monthly"


def crawl_html_files(root):
    urls = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Prune excluded directories
        dirnames[:] = [
            d for d in dirnames
            if d not in EXCLUDE_DIRS and not d.startswith(".")
        ]
        for fname in filenames:
            if not fname.endswith(".html"):
                continue
            if any(fname.startswith(p) for p in EXCLUDE_PREFIXES):
                continue
            full_path = os.path.join(dirpath, fname)
            rel = os.path.relpath(full_path, root).replace("\\", "/")
            if any(part in EXCLUDE_DIRS for part in rel.split("/")):
                continue
            urls.append(rel)
    return sorted(urls)


def rel_to_url(rel_path):
    if rel_path == "index.html":
        return f"{BASE_URL}/"
    if rel_path.endswith("/index.html"):
        return f"{BASE_URL}/{rel_path[:-len('/index.html')]}/"
    return f"{BASE_URL}/{rel_path}"


def build_sitemap(urls, today):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for rel in urls:
        url = rel_to_url(rel)
        priority, freq = get_priority_and_freq(rel)
        lines.append(f"""  <url>
    <loc>{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>""")
    lines.append("</urlset>")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Regenerate sitemap.xml")
    parser.add_argument("--dry-run", action="store_true", help="Print URL count without writing")
    args = parser.parse_args()

    urls = crawl_html_files(REPO_ROOT)
    today = date.today().isoformat()
    sitemap = build_sitemap(urls, today)

    print(f"Found {len(urls)} HTML files")

    if args.dry_run:
        print(sitemap[:2000])
        return

    out_path = os.path.join(REPO_ROOT, "sitemap.xml")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(sitemap)
    print(f"Wrote {out_path} ({len(urls)} URLs)")


if __name__ == "__main__":
    main()
