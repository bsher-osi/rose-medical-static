#!/usr/bin/env python3
"""
Regenerates blogs/index.html from all posts — both /blogs/{slug}/ and legacy top-level posts.
Run after any new post is added.
"""

import os
import re
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent
BLOGS_DIR = BASE / "blogs"
INDEX_PATH = BLOGS_DIR / "index.html"

# Stock images to rotate through (never show the Rose Medical logo)
STOCK_IMAGES = [
    "/wp-content/uploads/2023/11/AdobeStock_614753293-1024x683.jpeg",
    "/wp-content/uploads/2023/11/AdobeStock_622445982-1024x683.jpeg",
    "/wp-content/uploads/2023/12/AdobeStock_622356520-1024x683.jpeg",
    "/wp-content/uploads/2023/12/AdobeStock_536256155-1024x683.jpeg",
    "/wp-content/uploads/2023/12/AdobeStock_80235139-1024x683.jpeg",
    "/wp-content/uploads/2023/11/AdobeStock_309189896-1024x683.jpeg",
    "/wp-content/uploads/2023/11/AdobeStock_309189896-1-1024x683.jpeg",
]

# Logo path — never use this as a blog card image
LOGO_PATHS = ["Rose-Logo", "IMG_0045", "favicon"]

# Legacy top-level blog posts to include
LEGACY_POSTS = [
    {"slug": "febrile-seizures",           "url": "/febrile-seizures/",           "title": "Febrile Seizures in a Child: Causes, Signs & Treatment",    "date_display": "November 26, 2023", "pub_date": "2023-11-26"},
    {"slug": "febrile-seizures-2",         "url": "/febrile-seizures-2/",         "title": "Headache Management Tips & Headache Prevention",            "date_display": "November 26, 2023", "pub_date": "2023-11-26"},
    {"slug": "febrile-seizures-2-2",       "url": "/febrile-seizures-2-2/",       "title": "Nurturing Resilience: Anxiety in Children",                 "date_display": "November 26, 2023", "pub_date": "2023-11-26"},
    {"slug": "generalized-seizure-dos-donts", "url": "/generalized-seizure-dos-donts/", "title": "What to Do During a Seizure: First Aid Steps Guide", "date_display": "June 1, 2025",      "pub_date": "2025-06-01"},
    {"slug": "generalized-seizure-dos-donts-2", "url": "/generalized-seizure-dos-donts-2/", "title": "What is POTS?",                                   "date_display": "June 1, 2025",      "pub_date": "2025-06-01"},
    {"slug": "psychogenic-non-epileptic-seizure", "url": "/psychogenic-non-epileptic-seizure/", "title": "Psychogenic Non-Epileptic Seizures (PNES)",   "date_display": "June 1, 2025",      "pub_date": "2025-06-01"},
]


def is_logo(src):
    return any(p in src for p in LOGO_PATHS)


def extract_post_meta(post_dir):
    html_path = post_dir / "index.html"
    if not html_path.exists():
        return None
    html = html_path.read_text(encoding="utf-8", errors="ignore")

    slug = post_dir.name

    title_m = re.search(r"<title>(.+?)\s*\|\s*Rose Medical", html)
    title = title_m.group(1).strip() if title_m else slug.replace("-", " ").title()

    desc_m = re.search(r'<meta name="description" content="([^"]+)"', html)
    desc = desc_m.group(1).strip() if desc_m else ""
    words = desc.split()
    excerpt = " ".join(words[:20]) + ("…" if len(words) > 20 else "")

    date_m = re.search(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})', html)
    if date_m:
        pub_date = datetime.strptime(date_m.group(1), "%Y-%m-%d")
        date_display = pub_date.strftime("%B %d, %Y")
        pub_date_str = date_m.group(1)
    else:
        date_display = ""
        pub_date_str = "2026-01-01"

    # Find first non-logo image in body
    body_start = html.find("<body")
    image = None
    for m in re.finditer(r'<img[^>]+src="([^"]+\.(?:jpg|jpeg|png|webp))"', html[body_start:]):
        src = m.group(1)
        if not is_logo(src):
            image = src
            break

    return {
        "slug": slug,
        "title": title,
        "excerpt": excerpt,
        "date_display": date_display,
        "pub_date": pub_date_str,
        "image": image,
        "url": f"/blogs/{slug}/",
    }


def make_card(post, stock_img):
    image = post.get("image") or stock_img
    if is_logo(image):
        image = stock_img
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
\t\t\t\t<p itemprop="description" class="mkdf-post-excerpt">{post.get('excerpt', '')}</p>
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
    # Collect new-style posts from blogs/*/
    posts = []
    for post_dir in BLOGS_DIR.iterdir():
        if not post_dir.is_dir():
            continue
        meta = extract_post_meta(post_dir)
        if meta:
            posts.append(meta)

    # Add legacy top-level posts
    for lp in LEGACY_POSTS:
        # Add excerpt from actual file if available
        html_path = BASE / lp["slug"] / "index.html"
        if html_path.exists():
            html = html_path.read_text(encoding="utf-8", errors="ignore")
            desc_m = re.search(r'<meta name="description" content="([^"]+)"', html)
            if desc_m:
                words = desc_m.group(1).split()
                lp["excerpt"] = " ".join(words[:20]) + ("…" if len(words) > 20 else "")
        posts.append(lp)

    # Sort newest first
    posts.sort(key=lambda p: p["pub_date"], reverse=True)
    print(f"Found {len(posts)} blog posts total")

    # Build cards
    cards = []
    for i, post in enumerate(posts):
        stock = STOCK_IMAGES[i % len(STOCK_IMAGES)]
        cards.append(make_card(post, stock))
    cards_html = "\n".join(cards)

    new_list = (
        '<ul class="mkdf-blog-list">\n'
        + cards_html
        + '\n\t\t\t</ul>'
    )

    current = INDEX_PATH.read_text(encoding="utf-8", errors="ignore")
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
