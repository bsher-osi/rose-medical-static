#!/usr/bin/env python3
"""Update blog post hero and blog_writer.py template to use the site's standard page background."""
import os, glob

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

OLD = 'background-image:url(/wp-content/uploads/2017/04/blog-parallax-1.jpg);'
NEW = 'background-image:url(/wp-content/uploads/2023/11/pagebackground-1-scaled.jpeg);'

# Blog post HTML files
files = glob.glob(os.path.join(REPO_ROOT, "blogs", "**", "index.html"), recursive=True)
changed = 0
for path in files:
    with open(path, encoding="utf-8") as f:
        html = f.read()
    if OLD in html:
        html = html.replace(OLD, NEW)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        changed += 1
        print(f"  updated: {os.path.basename(os.path.dirname(path))}")

# blog_writer.py template
bw = os.path.join(REPO_ROOT, "seo", "agents", "blog_writer.py")
with open(bw, encoding="utf-8") as f:
    src = f.read()
if OLD in src:
    src = src.replace(OLD, NEW)
    with open(bw, "w", encoding="utf-8") as f:
        f.write(src)
    print("  updated: blog_writer.py")
    changed += 1

print(f"Done. {changed} files updated.")
