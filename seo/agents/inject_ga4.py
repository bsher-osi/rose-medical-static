#!/usr/bin/env python3
"""Inject ga4-init.js into all HTML pages that don't already have it."""
import os, re
from pathlib import Path

ROOT   = Path(__file__).resolve().parents[2]
SNIPPET = '<script src="/ga4-init.js" defer></script>'
MARKER  = 'ga4-init.js'

def process(path):
    text = path.read_text(encoding='utf-8', errors='ignore')
    if MARKER in text:
        return False
    # Insert before </head>
    if '</head>' not in text:
        return False
    new = text.replace('</head>', f'  {SNIPPET}\n</head>', 1)
    path.write_text(new, encoding='utf-8')
    return True

updated = 0
for html in ROOT.rglob('*.html'):
    parts = html.parts
    if any(p.startswith('.') for p in parts):
        continue
    if process(html):
        updated += 1

print(f"Injected ga4-init.js into {updated} pages")
