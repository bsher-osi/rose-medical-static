#!/usr/bin/env python3
"""Fix 'other conditions' links in city pages to point to city-specific URLs."""
import os, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

SERVICES = [
    "pediatric-epilepsy", "pediatric-seizures", "developmental-delays",
    "pediatric-headaches", "cerebral-palsy-muscle-disease", "movement-disorders",
    "tic-disorders", "sleep-disorders-children", "traumatic-brain-injury",
    "pediatric-concussion", "nerve-injury", "brain-mri-children",
    "pediatric-eeg", "visual-disturbances-children", "dizziness-vertigo-children",
    "syncope-loss-of-consciousness", "insomnia-children",
]

def fix_page(path, city):
    text = path.read_text(encoding="utf-8", errors="ignore")
    changed = False
    for svc in SERVICES:
        # Replace href="/svc-phoenix/" with href="/svc-city/"
        old = f'href="/{svc}-phoenix/"'
        new = f'href="/{svc}-{city}/"'
        if old in text:
            text = text.replace(old, new)
            changed = True
    if changed:
        path.write_text(text, encoding="utf-8")
    return changed

updated = 0
for svc in SERVICES:
    svc_dir = ROOT / f"{svc}-phoenix"
    # Find all city pages for this service
    pattern = f"{svc}-*"
    for page_dir in ROOT.glob(pattern):
        if not page_dir.is_dir():
            continue
        city = page_dir.name.replace(f"{svc}-", "")
        if city == "phoenix":
            continue
        idx = page_dir / "index.html"
        if idx.exists() and fix_page(idx, city):
            updated += 1

print(f"Fixed cross-links in {updated} city pages")
