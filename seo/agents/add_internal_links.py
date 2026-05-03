#!/usr/bin/env python3
"""
Add an "Areas We Serve" internal link grid to each main condition page.
Links to all localized city variants that exist on disk.
Injected just before the Schedule a Consultation box (fix-schedule-cta marker).
"""
import os, re, glob

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# Main condition page slug → condition prefix used in localized dirs
CONDITION_PAGES = {
    "pediatric-epilepsy-phoenix":               "pediatric-epilepsy",
    "pediatric-seizures-phoenix":               "pediatric-seizures",
    "developmental-delays-phoenix":             "developmental-delays",
    "pediatric-headaches-phoenix":              "pediatric-headaches",
    "cerebral-palsy-muscle-disease-phoenix":    "cerebral-palsy-muscle-disease",
    "movement-disorders-phoenix":               "movement-disorders",
    "tic-disorders-phoenix":                    "tic-disorders",
    "sleep-disorders-children-phoenix":         "sleep-disorders-children",
    "dizziness-vertigo-children-phoenix":       "dizziness-vertigo-children",
    "traumatic-brain-injury-phoenix":           "traumatic-brain-injury",
    "pediatric-concussion-phoenix":             "pediatric-concussion",
    "nerve-injury-phoenix":                     "nerve-injury",
    "insomnia-children-phoenix":                "insomnia-children",
    "syncope-loss-of-consciousness-phoenix":    "syncope-loss-of-consciousness",
    "visual-disturbances-children-phoenix":     "visual-disturbances-children",
    "brain-mri-children-phoenix":               "brain-mri-children",
    "pediatric-eeg-phoenix":                    "pediatric-eeg",
}


def city_display(slug, condition_prefix):
    """Strip condition prefix and convert city slug to title case."""
    city_slug = slug[len(condition_prefix)+1:]  # remove "condition-prefix-"
    specials = {
        "apache-junction": "Apache Junction",
        "bullhead-city": "Bullhead City",
        "camp-verde": "Camp Verde",
        "casa-grande": "Casa Grande",
        "cave-creek": "Cave Creek",
        "chino-valley": "Chino Valley",
        "colorado-city": "Colorado City",
        "fountain-hills": "Fountain Hills",
        "lake-havasu-city": "Lake Havasu City",
        "prescott-valley": "Prescott Valley",
        "queen-creek": "Queen Creek",
        "show-low": "Show Low",
        "sierra-vista": "Sierra Vista",
        "verde-valley": "Verde Valley",
        "san-tan-valley": "San Tan Valley",
        "sun-city": "Sun City",
        "sun-city-west": "Sun City West",
        "litchfield-park": "Litchfield Park",
        "el-mirage": "El Mirage",
        "paradise-valley": "Paradise Valley",
    }
    if city_slug in specials:
        return specials[city_slug]
    return city_slug.replace("-", " ").title()


def build_link_grid(condition_prefix, cities):
    """Build the HTML areas-we-serve grid."""
    items = ""
    for city_slug, city_dir in sorted(cities, key=lambda x: x[0]):
        name = city_display(city_dir, condition_prefix)
        items += f'    <a href="/{city_dir}/" style="display:inline-block;padding:6px 14px;margin:4px;background:#fff;border:1px solid #c8d8f0;border-radius:20px;color:#005da8;text-decoration:none;font-size:0.88rem;line-height:1.4;">{name}</a>\n'

    return f'''<div style="margin:2em 0;padding:1.5em 2em;background:#f0f6ff;border-radius:8px;">
  <h3 style="margin:0 0 0.8em;color:#005da8;font-size:1.05rem;">Areas We Serve Across Arizona</h3>
  <p style="margin:0 0 1em;font-size:0.92rem;color:#444;">We welcome patients from communities throughout Arizona. Click your city for local information.</p>
  <div style="line-height:2;">
{items}  </div>
</div>
'''


def main():
    all_dirs = set(os.listdir(REPO_ROOT))
    updated = skipped = 0

    for page_slug, condition_prefix in CONDITION_PAGES.items():
        path = os.path.join(REPO_ROOT, page_slug, "index.html")
        if not os.path.exists(path):
            continue

        with open(path, encoding='utf-8') as f:
            html = f.read()

        if 'areas-we-serve' in html or 'Areas We Serve' in html:
            skipped += 1
            continue

        # Find all localized dirs for this condition
        cities = []
        for d in all_dirs:
            if d.startswith(condition_prefix + "-") and d != page_slug:
                if os.path.exists(os.path.join(REPO_ROOT, d, "index.html")):
                    city_slug = d[len(condition_prefix)+1:]
                    cities.append((city_slug, d))

        if not cities:
            continue

        grid = build_link_grid(condition_prefix, cities)

        # Inject before the schedule CTA marker
        anchor = '<!-- fix-schedule-cta -->'
        if anchor in html:
            html = html.replace(anchor, grid + anchor, 1)
        else:
            # fallback: before </div>\n        </div>\n      </div>\n    </div> closing content
            anchor2 = '<h3>Schedule a Consultation</h3>'
            if anchor2 in html:
                html = html.replace(anchor2, grid + anchor2, 1)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        updated += 1
        print(f"  {page_slug}: {len(cities)} cities linked")

    print(f"\nDone. Updated: {updated}  Skipped: {skipped}")


if __name__ == "__main__":
    main()
