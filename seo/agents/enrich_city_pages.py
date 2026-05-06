#!/usr/bin/env python3
"""
Use Claude API to enrich city pages for top AZ cities with deeper, city-specific content.
Targets cities where competition is higher (Flagstaff, Glendale, Tucson, etc.)

Usage:
  python enrich_city_pages.py
  python enrich_city_pages.py --cities flagstaff glendale tucson
  python enrich_city_pages.py --dry-run
"""
import argparse, os, re, sys
from pathlib import Path

import anthropic

ROOT = Path(__file__).resolve().parents[2]

TOP_CITIES = [
    ("flagstaff", "Flagstaff", "Coconino County", "147 miles", "Northern Arizona University and the Colorado Plateau"),
    ("glendale", "Glendale", "Maricopa County", "18 miles", "one of the largest cities in the Phoenix metro area"),
    ("tucson", "Tucson", "Pima County", "115 miles", "Arizona's second-largest city and home to the University of Arizona"),
    ("chandler", "Chandler", "Maricopa County", "22 miles", "a fast-growing tech hub in the East Valley"),
    ("mesa", "Mesa", "Maricopa County", "18 miles", "the third-largest city in Arizona"),
    ("scottsdale", "Scottsdale", "Maricopa County", "12 miles", "a premier healthcare destination in the Phoenix metro"),
    ("tempe", "Tempe", "Maricopa County", "15 miles", "home to Arizona State University"),
    ("gilbert", "Gilbert", "Maricopa County", "20 miles", "one of Arizona's fastest-growing communities"),
    ("peoria", "Peoria", "Maricopa County", "15 miles", "a growing family community in the Northwest Valley"),
    ("surprise", "Surprise", "Maricopa County", "22 miles", "a rapidly expanding West Valley suburb"),
]

SERVICES = [
    ("pediatric-epilepsy", "pediatric epilepsy", "epilepsy"),
    ("pediatric-seizures", "pediatric seizures", "seizures"),
    ("developmental-delays", "developmental delays", "developmental delays"),
    ("pediatric-headaches", "pediatric headaches and migraines", "headaches"),
    ("adhd-specialist", "ADHD in children", "ADHD"),
    ("autism-evaluation", "autism spectrum disorder evaluation", "autism"),
    ("brain-mri-children", "pediatric brain MRI", "brain MRI"),
    ("pediatric-eeg", "pediatric EEG testing", "EEG testing"),
]

ENRICH_MARKER = "<!-- enriched-v1 -->"

def generate_enrichment(client, city_name, county, distance, city_context, condition, condition_short):
    prompt = f"""You are writing a section for a pediatric neurology clinic website page targeting families in {city_name}, AZ ({distance} from Phoenix, {city_context}).

The page is about {condition} at Rose Medical Pavilion with Dr. Tamara Zach MD, a board-certified pediatric neurologist in Phoenix.

Write 4-5 paragraphs (approximately 400-500 words) of genuinely helpful, city-specific content that:
1. Opens with something specific and true about {city_name} families seeking {condition_short} care (mention the drive distance, county, or region naturally)
2. Addresses the real concern: "is it worth driving to Phoenix for this?"
3. Explains what makes pediatric neurology different from a general pediatrician for this condition
4. Mentions telehealth/follow-up options so not every visit requires the drive
5. Closes with a natural call to action to schedule

Use plain HTML paragraphs only (<p>, <h3>, <ul>/<li>). No markdown. No em-dashes. Write in a warm, reassuring tone for parents. Do not fabricate facts. Do not mention specific local doctors by name. Keep Dr. Tamara Zach MD's full name on first mention, then just "Dr. Zach"."""

    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return msg.content[0].text

def enrich_page(path, city_slug, city_name, county, distance, city_context, condition, condition_short, client, dry_run):
    text = path.read_text(encoding="utf-8", errors="ignore")
    if ENRICH_MARKER in text:
        return False  # already enriched

    enrichment = generate_enrichment(client, city_name, county, distance, city_context, condition, condition_short)
    # Insert enrichment before the schedule CTA
    insert_point = text.find("<!-- fix-schedule-cta -->")
    if insert_point == -1:
        return False
    new_text = text[:insert_point] + ENRICH_MARKER + "\n" + enrichment + "\n\n" + text[insert_point:]
    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cities", nargs="+")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("ANTHROPIC_API_KEY not set"); sys.exit(1)
    client = anthropic.Anthropic(api_key=api_key)

    cities = TOP_CITIES
    if args.cities:
        cities = [c for c in TOP_CITIES if c[0] in args.cities]

    enriched = 0
    for city_slug, city_name, county, distance, city_context in cities:
        for svc_slug, condition, condition_short in SERVICES:
            page = ROOT / f"{svc_slug}-{city_slug}" / "index.html"
            if not page.exists():
                continue
            print(f"  enriching {svc_slug}-{city_slug}...", end=" ", flush=True)
            if enrich_page(page, city_slug, city_name, county, distance, city_context,
                           condition, condition_short, client, args.dry_run):
                print("done")
                enriched += 1
            else:
                print("skipped")

    print(f"\n{'Would enrich' if args.dry_run else 'Enriched'} {enriched} pages")

if __name__ == "__main__":
    main()
