#!/usr/bin/env python3
import glob, os
from datetime import date

today = date.today().isoformat()
base = "https://rosemedicalpavilion.com"

dirs = sorted([
    d.replace("\\", "/").replace("/index.html", "")
    for d in glob.glob("*/index.html")
    if ".git" not in d and "seo/" not in d and "contact_form/" not in d
])

TOP_PAGES = {"about-us", "contact-us", "refer-a-patient", "schedule-online", "blogs", "blog"}

urls = [("/", "1.0", "weekly")]
for slug in dirs:
    priority = "0.8" if slug in TOP_PAGES else "0.6"
    urls.append((f"/{slug}/", priority, "monthly"))

lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
]
for path, priority, freq in urls:
    lines += [
        "  <url>",
        f"    <loc>{base}{path}</loc>",
        f"    <lastmod>{today}</lastmod>",
        f"    <changefreq>{freq}</changefreq>",
        f"    <priority>{priority}</priority>",
        "  </url>",
    ]
lines.append("</urlset>")

with open("sitemap.xml", "w", newline="\n") as f:
    f.write("\n".join(lines) + "\n")

print(f"Sitemap written: {len(urls)} URLs")
