#!/usr/bin/env python3
"""
Enhance localized city pages with compelling "worth the trip" distance content.
Replaces the thin "Getting to Our Office" section with a richer block that:
 - States drive time (not just miles)
 - Explains why specialized care is worth traveling for
 - Uses warm, patient-facing language
"""
import os, re, glob

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# City → (miles, drive_time_str)
# Distances from 22044 N 44th St, Phoenix AZ 85050
CITY_DATA = {
    "ahwatukee":        (14,  "about 20 minutes"),
    "anthem":           (33,  "about 35 minutes"),
    "apache-junction":  (34,  "about 38 minutes"),
    "avondale":         (22,  "about 28 minutes"),
    "benson":           (155, "about 2 hours"),
    "bisbee":           (205, "about 2.5 hours"),
    "buckeye":          (38,  "about 45 minutes"),
    "bullhead-city":    (200, "about 2.5 hours"),
    "camp-verde":       (90,  "about 1 hour 25 minutes"),
    "carefree":         (28,  "about 32 minutes"),
    "casa-grande":      (52,  "about 52 minutes"),
    "cave-creek":       (24,  "about 28 minutes"),
    "chandler":         (22,  "about 28 minutes"),
    "chino-valley":     (95,  "about 1 hour 35 minutes"),
    "clarkdale":        (105, "about 1 hour 40 minutes"),
    "clifton":          (165, "about 2.5 hours"),
    "colorado-city":    (270, "about 4 hours"),
    "coolidge":         (62,  "about 1 hour 5 minutes"),
    "cottonwood":       (100, "about 1 hour 35 minutes"),
    "douglas":          (220, "about 3 hours"),
    "duncan":           (185, "about 2.5 hours"),
    "eagar":            (190, "about 2.5 hours"),
    "eloy":             (70,  "about 1 hour 10 minutes"),
    "flagstaff":        (145, "about 2 hours"),
    "florence":         (58,  "about 58 minutes"),
    "fountain-hills":   (22,  "about 26 minutes"),
    "fredonia":         (280, "about 4 hours"),
    "gilbert":          (24,  "about 28 minutes"),
    "glendale":         (20,  "about 26 minutes"),
    "globe":            (85,  "about 1 hour 20 minutes"),
    "goodyear":         (30,  "about 36 minutes"),
    "guadalupe":        (14,  "about 20 minutes"),
    "hayden":           (90,  "about 1 hour 25 minutes"),
    "holbrook":         (190, "about 2.5 hours"),
    "jerome":           (105, "about 1 hour 40 minutes"),
    "kingman":          (195, "about 2.5 hours"),
    "lake-havasu-city": (195, "about 2.5 hours"),
    "lakeside":         (175, "about 2.5 hours"),
    "laveen":           (18,  "about 24 minutes"),
    "mammoth":          (85,  "about 1 hour 20 minutes"),
    "marana":           (100, "about 1 hour 30 minutes"),
    "maricopa":         (38,  "about 44 minutes"),
    "mesa":             (16,  "about 22 minutes"),
    "miami":            (80,  "about 1 hour 15 minutes"),
    "nogales":          (185, "about 2.5 hours"),
    "page":             (270, "about 3.5 hours"),
    "parker":           (155, "about 2 hours"),
    "payson":           (95,  "about 1 hour 25 minutes"),
    "peoria":           (22,  "about 27 minutes"),
    "pima":             (165, "about 2.5 hours"),
    "prescott":         (95,  "about 1 hour 30 minutes"),
    "prescott-valley":  (90,  "about 1 hour 25 minutes"),
    "queen-creek":      (36,  "about 40 minutes"),
    "quartzsite":       (160, "about 2 hours"),
    "safford":          (165, "about 2.5 hours"),
    "sahuarita":        (125, "about 1 hour 45 minutes"),
    "scottsdale":       (10,  "about 18 minutes"),
    "sedona":           (115, "about 1 hour 45 minutes"),
    "show-low":         (175, "about 2.5 hours"),
    "sierra-vista":     (185, "about 2.5 hours"),
    "snowflake":        (185, "about 2.5 hours"),
    "somerton":         (185, "about 2.5 hours"),
    "springerville":    (195, "about 2.5 hours"),
    "superior":         (65,  "about 1 hour"),
    "surprise":         (28,  "about 34 minutes"),
    "taylor":           (185, "about 2.5 hours"),
    "tempe":            (12,  "about 18 minutes"),
    "thatcher":         (165, "about 2.5 hours"),
    "tolleson":         (16,  "about 22 minutes"),
    "tombstone":        (210, "about 2.5 hours"),
    "tucson":           (115, "about 1 hour 40 minutes"),
    "verde-valley":     (100, "about 1 hour 35 minutes"),
    "wickenburg":       (55,  "about 55 minutes"),
    "williams":         (155, "about 2 hours"),
    "winkelman":        (85,  "about 1 hour 15 minutes"),
    "winslow":          (155, "about 2 hours"),
    "yuma":             (185, "about 2.5 hours"),
}

GOOGLE_MAPS_BASE = "https://www.google.com/maps/dir/?api=1&destination=22044+N+44th+St+Suite+200+Phoenix+AZ+85050"


def worth_the_trip_block(city_display, miles, drive_time):
    """Generate the enhanced distance/worth-the-trip HTML block."""
    # Choose framing based on distance
    if miles <= 35:
        distance_framing = f"Just {drive_time} from {city_display}, our Phoenix office is a straightforward drive — easy to fit around school, work, or weekend schedules."
        urgency = "Most families from the area make the drive in a single appointment and leave with a clear care plan."
    elif miles <= 80:
        distance_framing = f"At {drive_time} from {city_display}, the drive to our Phoenix office is well within reach — and many families tell us the trip was absolutely worth it for the level of specialized care their child received."
        urgency = "We schedule thorough initial appointments so you get answers the same day, minimizing the need for return visits."
    else:
        distance_framing = f"We know {drive_time} from {city_display} is a meaningful commitment, and we take that seriously. That's why we structure appointments to be comprehensive — so families leave with a complete evaluation, clear diagnosis when possible, and a full care plan in a single visit."
        urgency = "We also coordinate closely with your local pediatrician so follow-up care can happen closer to home."

    return f'''
<div class="rose-distance-block" style="margin:2em 0;border-radius:10px;overflow:hidden;box-shadow:0 2px 16px rgba(0,0,0,0.08);">
  <div style="background:#005da8;color:#fff;padding:18px 24px;">
    <strong style="font-size:1.1rem;">Getting to Our Office from {city_display}</strong>
  </div>
  <div style="padding:20px 24px;background:#fff;border:1px solid #e5e9f0;border-top:none;">
    <p style="margin:0 0 12px;"><strong>📍 22044 N 44th St, Suite 200, Phoenix, AZ 85050</strong><br>
    Approximately {miles} miles &mdash; {drive_time} from {city_display}.</p>
    <p style="margin:0 0 12px;">{distance_framing}</p>
    <a href="{GOOGLE_MAPS_BASE}" target="_blank" rel="noopener"
       style="display:inline-block;background:#de7f68;color:#fff;padding:9px 20px;border-radius:4px;text-decoration:none;font-weight:600;font-size:0.9rem;">
      Get Directions &rarr;
    </a>
  </div>
</div>

<div class="rose-worth-block" style="margin:2em 0;padding:20px 24px;background:#f0f6ff;border-left:4px solid #005da8;border-radius:0 8px 8px 0;">
  <h3 style="margin:0 0 10px;color:#005da8;font-size:1.05rem;">Why Families from {city_display} Choose to Make the Drive</h3>
  <ul style="margin:0;padding-left:1.3em;line-height:1.8;">
    <li><strong>Fellowship-trained specialist</strong> — Dr. Tamara Zach MD completed specialized pediatric neurology training beyond general pediatrics, offering a level of expertise that isn't available at most local clinics.</li>
    <li><strong>Answers in one visit</strong> — {urgency}</li>
    <li><strong>In-office EEG testing</strong> — No need to coordinate separate testing facilities. EEG studies can often be completed the same day as your consultation.</li>
    <li><strong>Flexible scheduling</strong> — We work around school and work calendars, including early morning appointments.</li>
    <li><strong>Statewide reach</strong> — We proudly serve families from across Arizona. You are not too far.</li>
  </ul>
</div>'''


def get_city_slug(dirname):
    """Extract city slug from directory name like 'brain-mri-children-chandler'."""
    # Try to match known city slugs from the end of the directory name
    for city_slug in sorted(CITY_DATA.keys(), key=len, reverse=True):
        if dirname.endswith("-" + city_slug):
            return city_slug
    return None


def title_case_city(slug):
    """Convert city slug to display name."""
    special = {
        "apache-junction": "Apache Junction",
        "bullhead-city": "Bullhead City",
        "camp-verde": "Camp Verde",
        "casa-grande": "Casa Grande",
        "cave-creek": "Cave Creek",
        "chino-valley": "Chino Valley",
        "colorado-city": "Colorado City",
        "cottonwood": "Cottonwood",
        "fountain-hills": "Fountain Hills",
        "lake-havasu-city": "Lake Havasu City",
        "prescott-valley": "Prescott Valley",
        "queen-creek": "Queen Creek",
        "show-low": "Show Low",
        "sierra-vista": "Sierra Vista",
        "verde-valley": "Verde Valley",
    }
    if slug in special:
        return special[slug]
    return slug.replace("-", " ").title()


OLD_SECTION_PAT = re.compile(
    r'<h3>Getting to Our Office from [^<]+</h3>\s*<p>[^<]*<strong>22044[^<]*</strong>[^<]*</p>',
    re.DOTALL
)

# Also match the pattern with the distance block that may follow
FULL_SECTION_PAT = re.compile(
    r'<h3>Getting to Our Office from [^<]+</h3>.*?(?=<h3>|<div style="margin:1\.5em|<h3>Schedule|$)',
    re.DOTALL
)


def process_file(path, city_slug):
    with open(path, encoding="utf-8") as f:
        html = f.read()

    if "rose-distance-block" in html:
        return False  # already updated

    miles, drive_time = CITY_DATA[city_slug]
    city_display = title_case_city(city_slug)

    new_block = worth_the_trip_block(city_display, miles, drive_time)

    # Replace the old "Getting to Our Office" section
    m = OLD_SECTION_PAT.search(html)
    if m:
        html = html[:m.start()] + new_block + html[m.end():]
    else:
        # Inject before the "Other conditions we treat" box or the Schedule section
        for anchor in ['<div style="margin:1.5em 0;padding:1em;background:#f8f8f8', '<h3>Schedule a Consultation']:
            if anchor in html:
                html = html.replace(anchor, new_block + "\n" + anchor, 1)
                break

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return True


def main():
    dirs = [d for d in os.listdir(REPO_ROOT)
            if os.path.isdir(os.path.join(REPO_ROOT, d))
            and not d.startswith(".")]

    updated = skipped = unknown = 0
    for dirname in sorted(dirs):
        city_slug = get_city_slug(dirname)
        if not city_slug:
            continue
        path = os.path.join(REPO_ROOT, dirname, "index.html")
        if not os.path.exists(path):
            continue
        if process_file(path, city_slug):
            updated += 1
            print(f"  updated: {dirname}")
        else:
            skipped += 1

    print(f"\nDone. Updated: {updated}  Skipped (already done): {skipped}")


if __name__ == "__main__":
    main()
