#!/usr/bin/env python3
"""Add missing jQuery plugin dependencies before modules.min.js on blog/CWT pages."""
import os, glob

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

PLUGINS = '''\
<script src="/wp-includes/js/jquery/jquery-migrate.min.js?ver=3.4.1"></script>
<script src="/wp-content/themes/mediclinic/assets/js/modules/plugins/jquery.hoverIntent.min.js?ver=6.9.4"></script>
<script src="/wp-content/themes/mediclinic/assets/js/modules/plugins/fluidvids.min.js?ver=6.9.4"></script>
<script src="/wp-content/themes/mediclinic/assets/js/modules/plugins/perfect-scrollbar.jquery.min.js?ver=6.9.4"></script>
<script src="/wp-includes/js/mediaelement/mediaelement-and-player.min.js?ver=4.2.17"></script>'''

ANCHOR = '<script src="/wp-content/themes/mediclinic/assets/js/modules.min.js'

TARGETS = []
for slug in os.listdir(os.path.join(REPO_ROOT, "blogs")):
    path = os.path.join(REPO_ROOT, "blogs", slug, "index.html")
    if os.path.exists(path):
        TARGETS.append(path)
TARGETS.append(os.path.join(REPO_ROOT, "conditions-we-treat", "index.html"))

for path in TARGETS:
    with open(path, encoding="utf-8") as f:
        html = f.read()
    if "hoverIntent" in html:
        print(f"  skip: {path}")
        continue
    if ANCHOR not in html:
        print(f"  no anchor: {path}")
        continue
    html = html.replace(ANCHOR, PLUGINS + "\n" + ANCHOR)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  updated: {path}")

print("Done.")
