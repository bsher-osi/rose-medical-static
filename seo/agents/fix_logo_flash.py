#!/usr/bin/env python3
"""Inject inline logo-constraint style into all HTML pages to prevent flash on load."""
import os, glob

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

INJECT = '<style>.mkdf-logo-wrapper img{height:56px!important;width:auto!important;max-width:160px!important;object-fit:contain!important}</style>'
ANCHOR = '<meta charset="UTF-8">'

files = glob.glob(os.path.join(REPO_ROOT, "**/*.html"), recursive=True)
changed = 0
for path in files:
    with open(path, encoding="utf-8") as f:
        html = f.read()
    if INJECT in html:
        continue
    if ANCHOR not in html:
        continue
    html = html.replace(ANCHOR, ANCHOR + "\n" + INJECT, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    changed += 1

print(f"Updated {changed} files")
