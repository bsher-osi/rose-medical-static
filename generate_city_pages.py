#!/usr/bin/env python3
"""
Generate localized pages for missing Arizona cities.
Copies from a chandler template and substitutes city name/slug.
"""

import os
import re
import shutil

BASE = r"D:\Downloads\rose-medical-static"

TOPICS = [
    "brain-mri-children",
    "cerebral-palsy-muscle-disease",
    "developmental-delays",
    "dizziness-vertigo-children",
    "insomnia-children",
    "movement-disorders",
    "nerve-injury",
    "pediatric-concussion",
    "pediatric-eeg",
    "pediatric-epilepsy",
    "pediatric-headaches",
    "pediatric-seizures",
    "sleep-disorders-children",
    "syncope-loss-of-consciousness",
    "tic-disorders",
    "traumatic-brain-injury",
    "visual-disturbances-children",
]

# (slug, display name, approx miles from Phoenix)
MISSING_CITIES = [
    ("clarkdale",    "Clarkdale",     95),
    ("colorado-city","Colorado City", 300),
    ("duncan",       "Duncan",        185),
    ("eagar",        "Eagar",         195),
    ("fredonia",     "Fredonia",      265),
    ("gila-bend",    "Gila Bend",     65),
    ("hayden",       "Hayden",        90),
    ("huachuca-city","Huachuca City", 90),
    ("jerome",       "Jerome",        100),
    ("kearny",       "Kearny",        70),
    ("mammoth",      "Mammoth",       65),
    ("miami",        "Miami",         80),
    ("pima",         "Pima",          160),
    ("south-tucson", "South Tucson",  110),
    ("springerville", "Springerville", 195),
    ("st-johns",     "St. Johns",     185),
    ("star-valley",  "Star Valley",   90),
    ("superior",     "Superior",      60),
    ("taylor",       "Taylor",        155),
    ("tombstone",    "Tombstone",     100),
    ("wellton",      "Wellton",       155),
    ("winkelman",    "Winkelman",     80),
]

created = 0
skipped = 0

for topic in TOPICS:
    template_dir = os.path.join(BASE, f"{topic}-chandler")
    template_file = os.path.join(template_dir, "index.html")
    if not os.path.exists(template_file):
        print(f"  SKIP (no template): {topic}-chandler")
        continue

    with open(template_file, "r", encoding="utf-8") as f:
        template = f.read()

    for slug, city_name, miles in MISSING_CITIES:
        dest_dir = os.path.join(BASE, f"{topic}-{slug}")
        dest_file = os.path.join(dest_dir, "index.html")

        if os.path.exists(dest_file):
            skipped += 1
            continue

        os.makedirs(dest_dir, exist_ok=True)

        html = template
        # Fix distance FIRST (before city name replacement changes "Chandler")
        html = re.sub(r"approximately \d+ miles from Chandler",
                      f"approximately {miles} miles from Phoenix",
                      html)

        # Replace slug references
        html = html.replace(f"{topic}-chandler/", f"{topic}-{slug}/")
        html = html.replace(f"{topic}-chandler\"", f"{topic}-{slug}\"")

        # Replace city name references
        html = html.replace("Chandler, AZ", f"{city_name}, AZ")
        html = html.replace("Chandler</span>", f"{city_name}</span>")
        html = html.replace("in Chandler", f"in {city_name}")
        html = html.replace("near Chandler", f"near {city_name}")
        html = html.replace("from Chandler", f"from {city_name}")
        html = html.replace(">Chandler, AZ<", f">{city_name}, AZ<")
        html = html.replace(">Chandler<", f">{city_name}<")
        html = html.replace("Chandler families", f"{city_name} families")
        html = html.replace("Chandler and", f"{city_name} and")
        html = html.replace("Chandler is", f"{city_name} is")

        # Fix doctor name
        html = html.replace("Dr. Zach Rose MD", "Dr. Tamara Zach MD")

        with open(dest_file, "w", encoding="utf-8") as f:
            f.write(html)
        created += 1

print(f"\nDone. Created: {created}, Skipped (already existed): {skipped}")
