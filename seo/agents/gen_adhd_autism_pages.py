#!/usr/bin/env python3
"""
Generate ADHD specialist and autism evaluation city pages for all AZ cities.
Uses the same structure as existing city pages (pediatric-epilepsy pattern).

Usage:
  python gen_adhd_autism_pages.py
  python gen_adhd_autism_pages.py --dry-run
"""
import argparse, os, re, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_SOURCE = ROOT / "pediatric-epilepsy-flagstaff" / "index.html"

ADHD_CONTENT = """
<h2>ADHD Specialist Near {city_name}, AZ</h2>
<p>Families in <strong>{city_name}, AZ</strong> looking for a pediatric ADHD specialist can find expert care at <strong>Rose Medical Pavilion</strong> with <strong>Dr. Tamara Zach MD, FAAN</strong>. Our Phoenix practice serves children and adolescents throughout Arizona, including those traveling from {city_name} and surrounding {county} communities.</p>

<h3>What Is ADHD?</h3>
<p>Attention-Deficit/Hyperactivity Disorder (ADHD) is one of the most common neurodevelopmental conditions in children, affecting approximately 1 in 10 school-age kids. ADHD is characterized by persistent patterns of inattention, hyperactivity, and impulsivity that interfere with daily functioning and development. Many children with ADHD also experience learning differences, anxiety, or sleep difficulties.</p>

<h3>Signs of ADHD in Children</h3>
<ul>
  <li>Difficulty sustaining attention in tasks or play activities</li>
  <li>Frequently losing items needed for school or activities</li>
  <li>Easily distracted by external stimuli</li>
  <li>Fidgeting, squirming, or inability to stay seated</li>
  <li>Talking excessively or interrupting others</li>
  <li>Acting without thinking — impulsive decisions</li>
  <li>Difficulty organizing tasks and managing time</li>
  <li>Forgetfulness in daily activities</li>
</ul>

<h3>ADHD Evaluation at Rose Medical Pavilion</h3>
<p>A comprehensive ADHD evaluation with Dr. Tamara Zach MD includes detailed developmental and medical history, review of school records and teacher input, standardized behavioral rating scales, neurological examination, and ruling out other conditions that can mimic ADHD (such as sleep disorders, anxiety, or seizure activity). We take the time to understand your child as a whole person — not just a checklist of symptoms.</p>

<h3>ADHD Treatment Options</h3>
<p>Treatment at Rose Medical Pavilion is individualized and evidence-based. Options include behavioral therapy recommendations, school accommodation planning (IEP / 504 plans), medication management when appropriate, and coordination with your child's teachers and other providers. Dr. Zach takes a collaborative approach with families to find what works best for your child.</p>

<h3>Why Families from {city_name} Choose Rose Medical Pavilion</h3>
<p>While there may be general pediatricians closer to {city_name} who can screen for ADHD, a pediatric neurologist offers a deeper level of evaluation — particularly important when symptoms are complex, a previous diagnosis doesn't seem to fit, or your child has not responded to standard treatments. Dr. Tamara Zach MD brings fellowship-trained expertise in child neurology to every evaluation.</p>
"""

AUTISM_CONTENT = """
<h2>Autism Evaluation Near {city_name}, AZ</h2>
<p>Families in <strong>{city_name}, AZ</strong> seeking an autism spectrum disorder (ASD) evaluation for their child can access expert care at <strong>Rose Medical Pavilion</strong>. <strong>Dr. Tamara Zach MD, FAAN</strong> provides comprehensive neurological evaluation for children with suspected autism, serving families from {city_name} and across {county}.</p>

<h3>What Is Autism Spectrum Disorder?</h3>
<p>Autism spectrum disorder (ASD) is a complex neurodevelopmental condition that affects social communication, behavior, and sensory processing. It is called a "spectrum" because it manifests differently in every child — from those who are minimally verbal to highly verbal children who struggle with social nuance. Early identification and intervention significantly improve long-term outcomes.</p>

<h3>Early Signs of Autism</h3>
<ul>
  <li>Limited or no eye contact</li>
  <li>Not responding to their name by 12 months</li>
  <li>Not pointing at objects to show interest by 14 months</li>
  <li>Lack of pretend play by 18 months</li>
  <li>Losing previously acquired speech or social skills</li>
  <li>Repetitive movements (hand flapping, rocking, spinning)</li>
  <li>Strong insistence on routines; distress at small changes</li>
  <li>Unusual sensory responses (over- or under-sensitivity to sounds, textures, lights)</li>
</ul>

<h3>Neurological Evaluation for Autism at Rose Medical Pavilion</h3>
<p>Dr. Tamara Zach MD conducts neurological evaluations that complement the broader diagnostic process for autism. The neurological component helps identify co-occurring conditions that are common in children with ASD — including epilepsy (present in up to 30% of children with autism), sleep disorders, attention difficulties, and movement differences. Understanding the full neurological picture helps guide targeted interventions and ensures nothing is missed.</p>

<h3>Working with Your Child's Team</h3>
<p>An autism diagnosis and care plan typically involves multiple specialists. Dr. Zach works collaboratively with your child's developmental pediatrician, psychologist, speech-language pathologist, occupational therapist, and school team. Families from {city_name} appreciate having a neurologist who communicates clearly with all providers and keeps the focus on your child's overall wellbeing and development.</p>

<h3>Schedule an Evaluation</h3>
<p>If you have concerns about your child's development, early evaluation is always the right move. Contact Rose Medical Pavilion to schedule a consultation. Serving {city_name} and all of Arizona.</p>
"""

CITY_DATA = {
    "ahwatukee": ("Ahwatukee", "Maricopa County", "180 miles"),
    "anthem": ("Anthem", "Maricopa County", "35 miles"),
    "apache-junction": ("Apache Junction", "Pinal County", "35 miles"),
    "avondale": ("Avondale", "Maricopa County", "25 miles"),
    "benson": ("Benson", "Cochise County", "180 miles"),
    "bisbee": ("Bisbee", "Cochise County", "220 miles"),
    "buckeye": ("Buckeye", "Maricopa County", "45 miles"),
    "bullhead-city": ("Bullhead City", "Mohave County", "195 miles"),
    "camp-verde": ("Camp Verde", "Yavapai County", "95 miles"),
    "carefree": ("Carefree", "Maricopa County", "30 miles"),
    "casa-grande": ("Casa Grande", "Pinal County", "60 miles"),
    "cave-creek": ("Cave Creek", "Maricopa County", "28 miles"),
    "chandler": ("Chandler", "Maricopa County", "22 miles"),
    "chino-valley": ("Chino Valley", "Yavapai County", "100 miles"),
    "clarkdale": ("Clarkdale", "Yavapai County", "110 miles"),
    "clifton": ("Clifton", "Greenlee County", "175 miles"),
    "colorado-city": ("Colorado City", "Mohave County", "300 miles"),
    "coolidge": ("Coolidge", "Pinal County", "70 miles"),
    "cottonwood": ("Cottonwood", "Yavapai County", "110 miles"),
    "douglas": ("Douglas", "Cochise County", "235 miles"),
    "duncan": ("Duncan", "Greenlee County", "200 miles"),
    "eagar": ("Eagar", "Apache County", "200 miles"),
    "el-mirage": ("El Mirage", "Maricopa County", "20 miles"),
    "eloy": ("Eloy", "Pinal County", "75 miles"),
    "flagstaff": ("Flagstaff", "Coconino County", "147 miles"),
    "florence": ("Florence", "Pinal County", "65 miles"),
    "fountain-hills": ("Fountain Hills", "Maricopa County", "25 miles"),
    "fredonia": ("Fredonia", "Coconino County", "330 miles"),
    "gila-bend": ("Gila Bend", "Maricopa County", "75 miles"),
    "gilbert": ("Gilbert", "Maricopa County", "20 miles"),
    "glendale": ("Glendale", "Maricopa County", "18 miles"),
    "globe": ("Globe", "Gila County", "90 miles"),
    "goodyear": ("Goodyear", "Maricopa County", "28 miles"),
    "guadalupe": ("Guadalupe", "Maricopa County", "15 miles"),
    "hayden": ("Hayden", "Gila County", "80 miles"),
    "holbrook": ("Holbrook", "Navajo County", "180 miles"),
    "huachuca-city": ("Huachuca City", "Cochise County", "195 miles"),
    "jerome": ("Jerome", "Yavapai County", "115 miles"),
    "kearny": ("Kearny", "Pinal County", "75 miles"),
    "kingman": ("Kingman", "Mohave County", "185 miles"),
    "lake-havasu-city": ("Lake Havasu City", "Mohave County", "195 miles"),
    "laveen": ("Laveen", "Maricopa County", "20 miles"),
    "litchfield-park": ("Litchfield Park", "Maricopa County", "25 miles"),
    "mammoth": ("Mammoth", "Pinal County", "80 miles"),
    "marana": ("Marana", "Pima County", "120 miles"),
    "maricopa": ("Maricopa", "Pinal County", "40 miles"),
    "mesa": ("Mesa", "Maricopa County", "18 miles"),
    "miami": ("Miami", "Gila County", "90 miles"),
    "nogales": ("Nogales", "Santa Cruz County", "185 miles"),
    "oro-valley": ("Oro Valley", "Pima County", "115 miles"),
    "page": ("Page", "Coconino County", "270 miles"),
    "paradise-valley": ("Paradise Valley", "Maricopa County", "15 miles"),
    "parker": ("Parker", "La Paz County", "190 miles"),
    "payson": ("Payson", "Gila County", "85 miles"),
    "peoria": ("Peoria", "Maricopa County", "15 miles"),
    "phoenix": ("Phoenix", "Maricopa County", "12 miles"),
    "pima": ("Pima", "Graham County", "165 miles"),
    "pinetop-lakeside": ("Pinetop-Lakeside", "Navajo County", "185 miles"),
    "prescott": ("Prescott", "Yavapai County", "100 miles"),
    "prescott-valley": ("Prescott Valley", "Yavapai County", "98 miles"),
    "quartzsite": ("Quartzsite", "La Paz County", "150 miles"),
    "queen-creek": ("Queen Creek", "Maricopa County", "30 miles"),
    "safford": ("Safford", "Graham County", "165 miles"),
    "sahuarita": ("Sahuarita", "Pima County", "130 miles"),
    "san-luis": ("San Luis", "Yuma County", "185 miles"),
    "san-tan-valley": ("San Tan Valley", "Pinal County", "32 miles"),
    "scottsdale": ("Scottsdale", "Maricopa County", "12 miles"),
    "sedona": ("Sedona", "Yavapai County", "120 miles"),
    "show-low": ("Show Low", "Navajo County", "175 miles"),
    "sierra-vista": ("Sierra Vista", "Cochise County", "195 miles"),
    "snowflake": ("Snowflake", "Navajo County", "175 miles"),
    "somerton": ("Somerton", "Yuma County", "190 miles"),
    "south-tucson": ("South Tucson", "Pima County", "120 miles"),
    "springerville": ("Springerville", "Apache County", "210 miles"),
    "st-johns": ("St. Johns", "Apache County", "200 miles"),
    "star-valley": ("Star Valley", "Gila County", "85 miles"),
    "sun-city": ("Sun City", "Maricopa County", "20 miles"),
    "sun-city-west": ("Sun City West", "Maricopa County", "22 miles"),
    "superior": ("Superior", "Pinal County", "55 miles"),
    "surprise": ("Surprise", "Maricopa County", "22 miles"),
    "taylor": ("Taylor", "Navajo County", "175 miles"),
    "tempe": ("Tempe", "Maricopa County", "15 miles"),
    "thatcher": ("Thatcher", "Graham County", "160 miles"),
    "tolleson": ("Tolleson", "Maricopa County", "18 miles"),
    "tombstone": ("Tombstone", "Cochise County", "210 miles"),
    "tucson": ("Tucson", "Pima County", "115 miles"),
    "wellton": ("Wellton", "Yuma County", "185 miles"),
    "wickenburg": ("Wickenburg", "Maricopa County", "60 miles"),
    "willcox": ("Willcox", "Cochise County", "195 miles"),
    "williams": ("Williams", "Coconino County", "155 miles"),
    "winkelman": ("Winkelman", "Gila County", "85 miles"),
    "winslow": ("Winslow", "Navajo County", "165 miles"),
    "youngtown": ("Youngtown", "Maricopa County", "20 miles"),
    "yuma": ("Yuma", "Yuma County", "185 miles"),
}

SERVICES = {
    "adhd-specialist": {
        "title": "ADHD Specialist",
        "slug_prefix": "adhd-specialist",
        "content_template": ADHD_CONTENT,
        "meta_desc": "Expert ADHD evaluation and treatment for children near {city_name}, AZ. Dr. Tamara Zach MD, board-certified pediatric neurologist at Rose Medical Pavilion Phoenix. Call (623) 257-ROSE.",
        "h1": "ADHD Specialist Near {city_name}, AZ",
        "breadcrumb_parent": "ADHD Specialist",
        "breadcrumb_parent_url": "/adhd-specialist-phoenix/",
    },
    "autism-evaluation": {
        "title": "Autism Evaluation",
        "slug_prefix": "autism-evaluation",
        "content_template": AUTISM_CONTENT,
        "meta_desc": "Comprehensive autism spectrum disorder (ASD) neurological evaluation near {city_name}, AZ. Dr. Tamara Zach MD, pediatric neurologist, Rose Medical Pavilion Phoenix. Call (623) 257-ROSE.",
        "h1": "Autism Evaluation Near {city_name}, AZ",
        "breadcrumb_parent": "Autism Evaluation",
        "breadcrumb_parent_url": "/autism-evaluation-phoenix/",
    },
}

PAGE_TEMPLATE = open(ROOT / "pediatric-epilepsy-flagstaff" / "index.html", encoding="utf-8").read()

OTHER_CONDITIONS = [
    ("pediatric-epilepsy", "Pediatric Epilepsy"),
    ("pediatric-seizures", "Seizures"),
    ("developmental-delays", "Developmental Delays"),
    ("pediatric-headaches", "Headaches & Migraines"),
    ("adhd-specialist", "ADHD"),
    ("autism-evaluation", "Autism Evaluation"),
    ("pediatric-eeg", "EEG Testing"),
    ("brain-mri-children", "Brain MRI"),
]

def build_page(svc_key, city_slug, dry_run=False):
    if city_slug not in CITY_DATA:
        return False
    city_name, county, distance = CITY_DATA[city_slug]
    svc = SERVICES[svc_key]
    slug = f"{svc['slug_prefix']}-{city_slug}"
    out_dir = ROOT / slug
    out_file = out_dir / "index.html"
    if out_file.exists():
        return False
    if dry_run:
        print(f"  would create: /{slug}/")
        return True

    content = svc["content_template"].format(
        city_name=city_name, county=county, distance=distance
    )
    other_links = " &bull; ".join(
        f'<a href="/{s}-{city_slug}/">{label}</a>'
        for s, label in OTHER_CONDITIONS if s != svc_key
    )

    # Build from template by substituting key sections
    page = PAGE_TEMPLATE
    # Title
    page = re.sub(r'<title>[^<]+</title>',
        f'<title>{svc["title"]} Near {city_name}, AZ | Rose Medical Pavilion</title>', page, count=1)
    # Meta description
    page = re.sub(r'<meta name="description" content="[^"]*"',
        f'<meta name="description" content="{svc["meta_desc"].format(city_name=city_name)}"', page, count=1)
    # Canonical
    page = re.sub(r'<link rel="canonical" href="[^"]*"',
        f'<link rel="canonical" href="https://rosemedicalpavilion.com/{slug}/"', page, count=1)
    # OG title
    page = re.sub(r'<meta property="og:title" content="[^"]*"',
        f'<meta property="og:title" content="{svc["title"]} Near {city_name}, AZ | Rose Medical Pavilion"', page, count=1)
    # OG description
    page = re.sub(r'<meta property="og:description" content="[^"]*"',
        f'<meta property="og:description" content="{svc["meta_desc"].format(city_name=city_name)}"', page, count=1)
    # OG url
    page = re.sub(r'<meta property="og:url" content="[^"]*"',
        f'<meta property="og:url" content="https://rosemedicalpavilion.com/{slug}/"', page, count=1)
    # H1
    page = re.sub(r'<h1 class="mkdf-page-title entry-title"><span>[^<]+</span></h1>',
        f'<h1 class="mkdf-page-title entry-title"><span>{svc["h1"].format(city_name=city_name)}</span></h1>', page, count=1)
    # Breadcrumb
    page = re.sub(
        r'<nav aria-label="Breadcrumb"[^>]*>.*?</nav>',
        f'<nav aria-label="Breadcrumb" style="margin-bottom:1em;font-size:0.9em;">'
        f'<a href="/">Home</a> &rsaquo; <a href="{svc["breadcrumb_parent_url"]}">{svc["breadcrumb_parent"]}</a> &rsaquo; {city_name}, AZ</nav>',
        page, count=1, flags=re.DOTALL
    )
    # Replace main content block (between breadcrumb nav and the schedule CTA)
    schedule_cta_pattern = r'<!-- fix-schedule-cta -->.*?</div>\s*</div>\s*</div>\s*</div>\s*</div>'
    schedule_cta = re.search(schedule_cta_pattern, page, re.DOTALL)
    if schedule_cta:
        content_start = page.find('</nav>', page.find('aria-label="Breadcrumb"')) + 6
        content_end = schedule_cta.start()
        page = page[:content_start] + "\n" + content + "\n" + page[content_end:]

    # Fix other conditions section
    page = re.sub(
        r'<strong>Other conditions we treat near [^<]+:</strong>.*?</div>',
        f'<strong>Other conditions we treat near {city_name}:</strong><p style="margin-top:0.5em;">{other_links}</p></div>',
        page, count=1, flags=re.DOTALL
    )

    # Fix schedule CTA city name
    page = page.replace("showing signs of epilepsy", f"showing signs that need evaluation")
    page = re.sub(r'If your child in \w[\w\s-]* is showing', f'If your child in {city_name} is showing', page)

    out_dir.mkdir(parents=True, exist_ok=True)
    out_file.write_text(page, encoding="utf-8")
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    created = 0
    for svc_key in SERVICES:
        for city_slug in CITY_DATA:
            if build_page(svc_key, city_slug, dry_run=args.dry_run):
                if not args.dry_run:
                    print(f"  created: /{svc_key}-{city_slug}/")
                created += 1

    action = "would create" if args.dry_run else "created"
    print(f"\n{action} {created} pages ({len(SERVICES)} services × cities)")

if __name__ == "__main__":
    main()
