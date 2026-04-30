#!/usr/bin/env python3
"""
Regenerates blogs/index.html from all posts in blogs/*/index.html.
Run after any new post is added.
"""

import os
import re
import glob
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent
BLOGS_DIR = BASE / "blogs"
INDEX_PATH = BLOGS_DIR / "index.html"

FALLBACK_IMAGES = [
    "/wp-content/uploads/2023/11/AdobeStock_614753293-1024x683.jpeg",
    "/wp-content/uploads/2023/11/AdobeStock_622445982-1024x683.jpeg",
    "/wp-content/uploads/2023/12/AdobeStock_622356520-1024x683.jpeg",
    "/wp-content/uploads/2026/04/IMG_0045.jpg",
]


def extract_post_meta(post_dir):
    html_path = post_dir / "index.html"
    if not html_path.exists():
        return None
    html = html_path.read_text(encoding="utf-8", errors="ignore")

    slug = post_dir.name

    # Title
    title_m = re.search(r"<title>(.+?)\s*\|\s*Rose Medical", html)
    title = title_m.group(1).strip() if title_m else slug.replace("-", " ").title()

    # Description
    desc_m = re.search(r'<meta name="description" content="([^"]+)"', html)
    desc = desc_m.group(1).strip() if desc_m else ""
    # Truncate to ~20 words
    words = desc.split()
    excerpt = " ".join(words[:20]) + ("…" if len(words) > 20 else "")

    # Date
    date_m = re.search(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})', html)
    if date_m:
        pub_date = datetime.strptime(date_m.group(1), "%Y-%m-%d")
        date_display = pub_date.strftime("%B %d, %Y")
    else:
        date_display = ""

    # First img src in body (after <body tag)
    body_start = html.find("<body")
    img_m = re.search(r'<img[^>]+src="([^"]+\.(?:jpg|jpeg|png|webp))"', html[body_start:])
    image = img_m.group(1) if img_m else None

    return {
        "slug": slug,
        "title": title,
        "excerpt": excerpt,
        "date_display": date_display,
        "pub_date": date_m.group(1) if date_m else "2026-01-01",
        "image": image,
        "url": f"/blogs/{slug}/",
    }


def make_card(post, img_fallback):
    image = post["image"] or img_fallback
    return f"""<li class="mkdf-bl-item clearfix">
\t<div class="mkdf-bli-inner">
\t<div class="mkdf-post-image">
\t\t<a itemprop="url" href="{post['url']}" title="{post['title']}">
\t\t\t<img loading="lazy" width="1024" height="683" src="{image}" class="attachment-large size-large wp-post-image" alt="{post['title']}">
\t\t</a>
\t</div>
\t<div class="mkdf-bli-info-top">
\t\t<div class="mkdf-post-info-category"><a href="/blogs/" rel="category tag">Pediatric Neurology</a></div>
\t\t<div itemprop="dateCreated" class="mkdf-post-info-date entry-date published updated">
\t\t\t<span>{post['date_display']}</span>
\t\t</div>
\t</div>
\t<div class="mkdf-bli-content">
\t\t<h3 itemprop="name" class="entry-title mkdf-post-title">
\t\t\t<a itemprop="url" href="{post['url']}" title="{post['title']}">{post['title']}</a>
\t\t</h3>
\t\t<div class="mkdf-bli-excerpt">
\t\t\t<div class="mkdf-post-excerpt-holder">
\t\t\t\t<p itemprop="description" class="mkdf-post-excerpt">{post['excerpt']}</p>
\t\t\t</div>
\t\t</div>
\t\t<div class="mkdf-bli-info-bottom">
\t\t\t<div class="mkdf-post-read-more-button">
<a itemprop="url" href="{post['url']}" target="_self" class="mkdf-btn mkdf-btn-medium mkdf-btn-simple mkdf-blog-list-button">    <span class="mkdf-btn-text">Learn more</span>    <span class="mkdf-btn-icon-holder">        <span class="mkdf-btn-icon-normal"></span>        <span class="mkdf-btn-icon-flip"></span>    </span></a></div>
\t\t</div>
\t</div>
\t</div>
</li>"""


def rebuild():
    # Collect all posts
    posts = []
    for post_dir in BLOGS_DIR.iterdir():
        if not post_dir.is_dir():
            continue
        meta = extract_post_meta(post_dir)
        if meta:
            posts.append(meta)

    # Sort newest first
    posts.sort(key=lambda p: p["pub_date"], reverse=True)
    print(f"Found {len(posts)} blog posts")

    # Build card list HTML
    cards = []
    for i, post in enumerate(posts):
        fallback = FALLBACK_IMAGES[i % len(FALLBACK_IMAGES)]
        cards.append(make_card(post, fallback))
    cards_html = "\n".join(cards)

    # Read current index and replace the blog list section
    current = INDEX_PATH.read_text(encoding="utf-8", errors="ignore")

    new_list = (
        '<ul class="mkdf-blog-list">\n'
        + cards_html
        + '\n\t\t\t</ul>'
    )

    # Replace between <ul class="mkdf-blog-list"> and the closing </ul>
    updated = re.sub(
        r'<ul class="mkdf-blog-list">.*?</ul>',
        new_list,
        current,
        flags=re.DOTALL,
        count=1,
    )

    if updated == current:
        print("WARNING: blog list marker not found — index unchanged")
        return

    INDEX_PATH.write_text(updated, encoding="utf-8")
    print(f"blogs/index.html updated with {len(posts)} posts")


if __name__ == "__main__":
    rebuild()
