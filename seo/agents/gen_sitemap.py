#!/usr/bin/env python3
"""Generate sitemap.xml for all pages in the static site."""
import os, glob
from datetime import date

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
BASE_URL = "https://rosemedicalpavilion.com"
TODAY = date.today().isoformat()

# Priority rules
HIGH_PRIORITY = {"", "about-us", "conditions-we-treat", "blog", "contact-us", "schedule-online"}
MEDIUM_PRIORITY_PREFIXES = [
    "pediatric-epilepsy", "pediatric-seizures", "developmental-delays",
    "pediatric-headaches", "cerebral-palsy", "movement-disorders",
    "tic-disorders", "sleep-disorders", "dizziness-vertigo",
    "traumatic-brain-injury", "pediatric-concussion", "nerve-injury",
    "insomnia-children", "syncope", "visual-disturbances",
    "brain-mri-children", "pediatric-eeg",
]

def get_priority(slug):
    if slug in HIGH_PRIORITY:
        return "1.0"
    for prefix in MEDIUM_PRIORITY_PREFIXES:
        if slug.startswith(prefix):
            # Main condition page (e.g. pediatric-epilepsy-phoenix) = 0.8
            # Localized (e.g. pediatric-epilepsy-chandler) = 0.6
            if slug.endswith("-phoenix") and slug.count("-") <= 3:
                return "0.8"
            return "0.6"
    if slug.startswith("blogs/"):
        return "0.7"
    return "0.5"

def get_changefreq(slug):
    if slug in HIGH_PRIORITY:
        return "weekly"
    if slug.startswith("blogs/"):
        return "monthly"
    return "monthly"

def main():
    urls = []

    # Root pages
    for path in glob.glob(os.path.join(REPO_ROOT, "*/index.html")):
        slug = os.path.basename(os.path.dirname(path))
        if slug.startswith(".") or slug == "seo":
            continue
        urls.append((f"/{slug}/", get_priority(slug), get_changefreq(slug)))

    # Homepage
    if os.path.exists(os.path.join(REPO_ROOT, "index.html")):
        urls.append(("/", "1.0", "weekly"))

    # Blog posts
    for path in glob.glob(os.path.join(REPO_ROOT, "blogs/*/index.html")):
        slug = "blogs/" + os.path.basename(os.path.dirname(path))
        urls.append((f"/{slug}/", get_priority(slug), get_changefreq(slug)))

    # Sort: homepage first, then by priority desc, then alpha
    urls.sort(key=lambda x: (-float(x[1]), x[0]))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for loc, priority, changefreq in urls:
        lines.append(f"""  <url>
    <loc>{BASE_URL}{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>""")
    lines.append('</urlset>')

    out = os.path.join(REPO_ROOT, "sitemap.xml")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Written {len(urls)} URLs to sitemap.xml")

if __name__ == "__main__":
    main()
