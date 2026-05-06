#!/usr/bin/env python3
"""Add 'Serving Arizona Families' city link sections to blog posts."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BLOGS_DIR = ROOT / "blogs"

MARKER = "<!-- city-links-v1 -->"

TOP_CITIES = [
    ("flagstaff", "Flagstaff"),
    ("glendale", "Glendale"),
    ("tucson", "Tucson"),
    ("chandler", "Chandler"),
    ("mesa", "Mesa"),
    ("scottsdale", "Scottsdale"),
    ("tempe", "Tempe"),
    ("gilbert", "Gilbert"),
    ("peoria", "Peoria"),
    ("surprise", "Surprise"),
    ("prescott", "Prescott"),
    ("yuma", "Yuma"),
]

# Map blog slug keywords to relevant service pages
BLOG_SERVICE_MAP = {
    "epilepsy": "pediatric-epilepsy",
    "seizure": "pediatric-seizures",
    "febrile": "pediatric-seizures",
    "developmental": "developmental-delays",
    "headache": "pediatric-headaches",
    "migraine": "pediatric-headaches",
    "adhd": "adhd-specialist",
    "autism": "autism-evaluation",
    "eeg": "pediatric-eeg",
    "mri": "brain-mri-children",
    "concussion": "pediatric-concussion",
    "brain-injury": "traumatic-brain-injury",
    "traumatic": "traumatic-brain-injury",
    "sleep": "sleep-disorders-children",
    "insomnia": "sleep-disorders-children",
    "movement": "movement-disorders",
    "tic": "tic-disorders",
    "tourette": "tic-disorders",
    "cerebral": "cerebral-palsy-muscle-disease",
    "palsy": "cerebral-palsy-muscle-disease",
    "vertigo": "dizziness-vertigo-children",
    "dizziness": "dizziness-vertigo-children",
    "syncope": "syncope-loss-of-consciousness",
    "visual": "visual-disturbances-children",
    "nerve": "nerve-injury",
}

def get_service_for_blog(slug):
    for keyword, service in BLOG_SERVICE_MAP.items():
        if keyword in slug:
            return service
    return "pediatric-epilepsy"  # default

def build_city_links_section(service, blog_label):
    links = " &bull; ".join(
        f'<a href="/{service}-{city_slug}/">{city_name}</a>'
        for city_slug, city_name in TOP_CITIES
    )
    return f"""
{MARKER}
<div style="margin:2.5em 0;padding:1.5em 2em;background:#f0f6ff;border-left:4px solid #005da8;border-radius:0 8px 8px 0;">
  <h3 style="margin:0 0 0.7em;color:#005da8;font-size:1.05rem;">Serving Arizona Families Statewide</h3>
  <p style="margin:0 0 0.8em;">Dr. Tamara Zach MD sees patients from across Arizona at Rose Medical Pavilion in Phoenix. Families traveling for {blog_label} care:</p>
  <p style="margin:0;line-height:2;">{links}</p>
</div>
"""

def process_blog(path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    if MARKER in text:
        return False

    slug = path.parent.name
    service = get_service_for_blog(slug)
    # Derive a readable label from the slug
    label = slug.replace("-arizona", "").replace("-guide", "").replace("-children", "").replace("-", " ")

    section = build_city_links_section(service, label)

    # Insert before closing article content — find last </div> before footer
    insert_before = '<footer class="rose-footer">'
    if insert_before not in text:
        return False

    new_text = text.replace(insert_before, section + "\n" + insert_before, 1)
    path.write_text(new_text, encoding="utf-8")
    return True

updated = 0
for blog_dir in sorted(BLOGS_DIR.iterdir()):
    if not blog_dir.is_dir():
        continue
    idx = blog_dir / "index.html"
    if idx.exists() and process_blog(idx):
        print(f"  added city links: /blogs/{blog_dir.name}/")
        updated += 1

print(f"\nAdded city links to {updated} blog posts")
