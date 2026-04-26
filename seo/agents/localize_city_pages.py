#!/usr/bin/env python3
"""
Generate city-specific landing pages for Rose Medical Pavilion.

URL pattern: /{service-base}-{city-slug}/index.html
where service-base is the service slug with '-phoenix' stripped.

Usage:
  python localize_city_pages.py --all                    # all services × all cities
  python localize_city_pages.py --all --primary-only     # primary AZ cities only
  python localize_city_pages.py --service pediatric-epilepsy-phoenix --all-cities
  python localize_city_pages.py --service pediatric-epilepsy-phoenix --city scottsdale
  python localize_city_pages.py --all --use-ai           # AI-generated content
"""

import argparse
import os
import re
import sys
import yaml

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "../config.yml")
TEMPLATE_PATH = os.path.join(SCRIPT_DIR, "../templates/city-page-template.html")

SERVICE_CONTENT = {
    "pediatric-epilepsy-phoenix": """
<h3>What Is Pediatric Epilepsy?</h3>
<p>Epilepsy is a neurological disorder characterized by recurrent, unprovoked seizures. It affects approximately 1 in 150 children. At Rose Medical Pavilion, Dr. Zach Rose MD provides comprehensive epilepsy diagnosis and management, including EEG monitoring and individualized medication plans.</p>
<h3>Signs &amp; Symptoms</h3>
<p>Common signs include recurrent seizures, staring spells, sudden stiffening or jerking, temporary confusion, loss of awareness, and unusual sensations. Some children experience absence seizures that can be mistaken for daydreaming.</p>
""",
    "pediatric-seizures-phoenix": """
<h3>Pediatric Seizures Overview</h3>
<p>Seizures occur when abnormal electrical activity disrupts normal brain function. Dr. Zach Rose MD specializes in identifying the underlying cause — whether epilepsy, febrile illness, or other neurological conditions — and creating a targeted treatment plan for your child.</p>
<h3>Types of Seizures in Children</h3>
<p>Seizure types include focal seizures, generalized tonic-clonic seizures, absence seizures, and febrile seizures. Accurate diagnosis through EEG and clinical evaluation is essential for effective management.</p>
""",
    "developmental-delays-phoenix": """
<h3>Understanding Developmental Delays</h3>
<p>Developmental delays occur when a child does not reach expected milestones in areas such as speech, motor skills, social skills, or cognition. Early neurological evaluation can identify treatable causes and guide intervention.</p>
<h3>When to See a Neurologist</h3>
<p>Consider a pediatric neurology evaluation if your child is significantly behind on milestones, has regression in previously acquired skills, or if your pediatrician recommends further workup.</p>
""",
    "pediatric-headaches-phoenix": """
<h3>Headaches and Migraines in Children</h3>
<p>Pediatric migraines are more common than many parents realize, affecting up to 10% of school-age children. Dr. Zach Rose MD offers comprehensive headache evaluation and management, including preventive strategies and acute treatment plans tailored to your child.</p>
<h3>Headache Red Flags</h3>
<p>Seek prompt evaluation for headaches that are sudden and severe ("thunderclap"), worsen with position changes, awaken your child from sleep, or are accompanied by fever, stiff neck, vision changes, or neurological symptoms.</p>
""",
    "cerebral-palsy-muscle-disease-phoenix": """
<h3>Cerebral Palsy and Muscle Disease</h3>
<p>Cerebral palsy (CP) is a group of disorders affecting movement and muscle tone caused by injury to the developing brain. Muscle diseases (myopathies) affect the muscles directly. Dr. Zach Rose MD provides expert evaluation, coordination of therapies, and long-term management for children with these conditions.</p>
<h3>Treatment Approach</h3>
<p>Management is individualized and may include physical therapy, occupational therapy, medications for spasticity, and coordination with orthopedic specialists. Early intervention improves functional outcomes.</p>
""",
    "movement-disorders-phoenix": """
<h3>Movement Disorders in Children</h3>
<p>Pediatric movement disorders include tremors, dystonia, chorea, ataxia, and stereotypies. These conditions can significantly impact a child's daily functioning and quality of life. Accurate diagnosis is the first step toward effective treatment.</p>
<h3>Diagnosis and Management</h3>
<p>Dr. Zach Rose MD evaluates movement disorders through detailed neurological examination, video analysis, and targeted testing. Treatment options vary by condition and may include medication, physical therapy, and other interventions.</p>
""",
    "tic-disorders-phoenix": """
<h3>Tic Disorders and Tourette Syndrome</h3>
<p>Tics are sudden, repetitive movements or sounds. Tourette syndrome is diagnosed when a child has both motor and vocal tics lasting more than one year. Most tic disorders are manageable, and many improve with age.</p>
<h3>Treatment Options</h3>
<p>Treatment depends on severity and impact on daily life. Options include behavioral therapy (CBIT), medication management, and supportive education for the child and family. Dr. Zach Rose MD creates individualized plans for each patient.</p>
""",
    "sleep-disorders-children-phoenix": """
<h3>Sleep Disorders in Children</h3>
<p>Poor sleep affects a child's brain development, behavior, learning, and emotional health. Neurological causes of sleep problems include restless leg syndrome, parasomnias (sleepwalking, night terrors), narcolepsy, and sleep-related epilepsy.</p>
<h3>Evaluation and Treatment</h3>
<p>Dr. Zach Rose MD conducts thorough sleep evaluations, including review of sleep logs, targeted testing, and when necessary, referral for polysomnography. Effective treatment restores healthy sleep and improves daytime function.</p>
""",
    "dizziness-vertigo-children-phoenix": """
<h3>Dizziness and Vertigo in Children</h3>
<p>Children can experience dizziness from vestibular migraines, benign paroxysmal vertigo, inner ear disorders, or central nervous system causes. Identifying the underlying cause is essential for appropriate treatment.</p>
<h3>What to Expect</h3>
<p>Evaluation includes detailed history, neurological examination, and targeted testing. Most causes of childhood dizziness respond well to treatment once identified.</p>
""",
    "traumatic-brain-injury-phoenix": """
<h3>Traumatic Brain Injury in Children</h3>
<p>Traumatic brain injury (TBI) ranges from mild concussion to severe injury requiring intensive care. Neurological follow-up is essential for monitoring recovery, identifying complications, and guiding return-to-school and return-to-activity decisions.</p>
<h3>Long-Term Management</h3>
<p>Dr. Zach Rose MD provides ongoing TBI management including cognitive rehabilitation, headache management, mood support, and coordination with school staff for accommodations.</p>
""",
    "pediatric-concussion-phoenix": """
<h3>Pediatric Concussion Management</h3>
<p>Concussion is a mild traumatic brain injury caused by a bump, blow, or jolt to the head. Symptoms include headache, dizziness, confusion, memory problems, and emotional changes. Most children recover fully with proper management.</p>
<h3>Return-to-Learn and Return-to-Play</h3>
<p>Dr. Zach Rose MD follows evidence-based protocols for safe return to school and sports. Early evaluation and proper guidance reduce the risk of prolonged symptoms and second-impact syndrome.</p>
""",
    "nerve-injury-phoenix": """
<h3>Nerve Injury in Children</h3>
<p>Peripheral nerve injuries in children can result from birth trauma, accidents, compression, or underlying medical conditions. Symptoms include weakness, numbness, tingling, and pain in the affected area.</p>
<h3>Diagnosis and Recovery</h3>
<p>Evaluation includes electromyography (EMG) and nerve conduction studies. Treatment depends on injury type and severity and may include physical therapy, splinting, or surgical consultation.</p>
""",
    "insomnia-children-phoenix": """
<h3>Insomnia in Children</h3>
<p>Childhood insomnia affects sleep initiation and maintenance, leading to daytime fatigue, behavioral problems, and academic difficulties. Neurological and behavioral factors both contribute to insomnia in children.</p>
<h3>Treatment</h3>
<p>Dr. Zach Rose MD evaluates contributing neurological factors and coordinates with behavioral sleep medicine when needed. Effective treatment improves sleep, mood, attention, and overall well-being.</p>
""",
    "syncope-loss-of-consciousness-phoenix": """
<h3>Syncope and Loss of Consciousness</h3>
<p>Syncope (fainting) in children is usually benign and related to dehydration or standing up quickly, but it can sometimes signal a cardiac or neurological condition. A thorough evaluation helps distinguish benign from concerning causes.</p>
<h3>Evaluation</h3>
<p>Dr. Zach Rose MD evaluates syncope through detailed history, EEG when seizure is suspected, and coordination with cardiology as needed. Proper diagnosis guides management and reassures families.</p>
""",
    "visual-disturbances-children-phoenix": """
<h3>Visual Disturbances in Children</h3>
<p>Visual symptoms in children can arise from migraines, seizures, increased intracranial pressure, or other neurological conditions. Timely evaluation helps identify the cause and initiate appropriate treatment.</p>
<h3>When to Seek Evaluation</h3>
<p>Seek prompt neurological evaluation for sudden vision loss, visual field defects, double vision, or visual symptoms accompanied by headache, weakness, or altered consciousness.</p>
""",
    "brain-mri-children-phoenix": """
<h3>Pediatric Brain MRI</h3>
<p>Brain MRI is the gold-standard imaging study for evaluating neurological conditions in children. It provides detailed images of brain structure without radiation exposure. Dr. Zach Rose MD interprets MRI results in the context of each child's clinical presentation.</p>
<h3>What to Expect</h3>
<p>MRI is painless but requires the child to remain still. For young children or those with anxiety, sedation may be arranged. Dr. Zach Rose MD discusses results with families in detail and explains the next steps clearly.</p>
""",
    "pediatric-eeg-phoenix": """
<h3>Pediatric EEG Testing</h3>
<p>An EEG (electroencephalogram) measures electrical activity in the brain. It is essential for diagnosing epilepsy, evaluating seizure type, and guiding treatment. The test is painless and non-invasive.</p>
<h3>How It Works</h3>
<p>Small electrodes are placed on the scalp to record brain waves. The test typically takes 30–60 minutes. Results are interpreted by Dr. Zach Rose MD in the context of the child's full clinical picture.</p>
""",
}

OTHER_CONDITIONS_BY_SERVICE = {
    s: ", ".join(
        f'<a href="/{o}/">{o.replace("-phoenix","").replace("-"," ").title()}</a>'
        for o in [
            "pediatric-epilepsy-phoenix", "pediatric-seizures-phoenix",
            "developmental-delays-phoenix", "pediatric-headaches-phoenix",
            "cerebral-palsy-muscle-disease-phoenix", "movement-disorders-phoenix",
            "tic-disorders-phoenix", "sleep-disorders-children-phoenix",
            "traumatic-brain-injury-phoenix", "pediatric-concussion-phoenix",
        ]
        if o != s
    )[:600] + "..."
    for s in SERVICE_CONTENT
}


def load_config():
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def load_template():
    with open(TEMPLATE_PATH) as f:
        return f.read()


def service_base(service_slug):
    """Strip '-phoenix' to get the base slug."""
    if service_slug.endswith("-phoenix"):
        return service_slug[:-len("-phoenix")]
    return service_slug


def page_slug(service_slug, city_slug):
    return f"{service_base(service_slug)}-{city_slug}"


def get_nearby_cities(city, all_cities):
    if "neighbors" in city:
        return ", ".join(city["neighbors"][:5])
    county = city.get("county", "")
    same_county = [c["name"] for c in all_cities if c.get("county") == county and c["name"] != city["name"]]
    return ", ".join(same_county[:5]) or "the Phoenix metro area"


def generate_city_page(template, service, city, all_cities):
    service_slug = service["slug"]
    city_slug = city["slug"]
    city_name = city["name"]
    service_name = service["name"]
    service_name_lower = service.get("short", service_name.lower())
    slug = page_slug(service_slug, city_slug)
    distance = city.get("distance_miles", "")
    county = city.get("county", "Maricopa")
    nearby = get_nearby_cities(city, all_cities)

    service_content = SERVICE_CONTENT.get(service_slug, f"""
<h3>About {service_name}</h3>
<p>Dr. Zach Rose MD provides expert diagnosis and treatment of {service_name_lower} for children near {city_name}, AZ. Early evaluation leads to better outcomes.</p>
""")

    other_cond = OTHER_CONDITIONS_BY_SERVICE.get(service_slug, "")

    html = template
    html = html.replace("{{SERVICE_NAME}}", service_name)
    html = html.replace("{{SERVICE_NAME_LOWER}}", service_name_lower)
    html = html.replace("{{CITY_NAME}}", city_name)
    html = html.replace("{{CITY_SLUG}}", city_slug)
    html = html.replace("{{PAGE_SLUG}}", slug)
    html = html.replace("{{SERVICE_PHOENIX_SLUG}}", service_slug)
    html = html.replace("{{DISTANCE_MILES}}", str(distance))
    html = html.replace("{{COUNTY}}", county)
    html = html.replace("{{NEARBY_CITIES}}", nearby)
    html = html.replace("{{SERVICE_CONTENT}}", service_content)
    html = html.replace("{{OTHER_CONDITIONS}}", other_cond)
    return html


def generate_city_page_ai(service, city, config):
    """Generate content using Claude AI (requires ANTHROPIC_API_KEY)."""
    import anthropic
    practice = config["practice"]
    city_name = city["name"]
    service_name = service["name"]
    distance = city.get("distance_miles", "")
    county = city.get("county", "Maricopa")

    client = anthropic.Anthropic()
    prompt = f"""Write the main content section (HTML only, no full page wrapper) for a pediatric neurology city landing page.

Practice: {practice['name']}
Doctor: {practice['doctor']}
Phone: {practice['phone']}
Address: {practice['address']}
City served: {city_name}, AZ ({distance} miles from Phoenix, {county} County)
Service: {service_name}

Write 4-5 paragraphs of HTML with h3 headings. Include:
1. Overview of the condition in children
2. Signs and symptoms
3. Diagnostic approach
4. Treatment at {practice['name']}
5. Why families from {city_name} choose {practice['name']}

Use Arizona-specific context where appropriate. Mention {city_name} naturally 3-4 times.
Return only HTML (h3/p tags). No wrapper divs."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


def get_all_cities(config):
    primary = config["cities"]["primary"]
    secondary = config["cities"].get("secondary", [])
    return primary + secondary


def main():
    parser = argparse.ArgumentParser(description="Generate Rose Medical city landing pages")
    parser.add_argument("--all", action="store_true", help="All services")
    parser.add_argument("--service", help="Single service slug")
    parser.add_argument("--city", help="Single city slug")
    parser.add_argument("--all-cities", action="store_true", help="All cities for given service")
    parser.add_argument("--primary-only", action="store_true", help="Primary cities only")
    parser.add_argument("--use-ai", action="store_true", help="Use Claude AI for content")
    parser.add_argument("--dry-run", action="store_true", help="Print paths without writing")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    config = load_config()
    template = load_template()

    primary_cities = config["cities"]["primary"]
    secondary_cities = config["cities"].get("secondary", [])
    all_cities = primary_cities + secondary_cities

    if args.primary_only:
        target_cities = primary_cities
    else:
        target_cities = all_cities

    services = config["services"]
    if args.service:
        services = [s for s in services if s["slug"] == args.service]
        if not services:
            print(f"Service not found: {args.service}")
            sys.exit(1)

    if args.city:
        target_cities = [c for c in all_cities if c["slug"] == args.city]
        if not target_cities:
            print(f"City not found: {args.city}")
            sys.exit(1)
    elif args.all_cities:
        pass  # already set above

    generated = 0
    skipped = 0

    for service in services:
        for city in target_cities:
            slug = page_slug(service["slug"], city["slug"])
            out_dir = os.path.join(REPO_ROOT, slug)
            out_path = os.path.join(out_dir, "index.html")

            if os.path.exists(out_path) and not args.force:
                skipped += 1
                continue

            if args.dry_run:
                print(f"  [dry-run] Would write: /{slug}/index.html")
                generated += 1
                continue

            if args.use_ai:
                try:
                    service_content = generate_city_page_ai(service, city, config)
                    html = generate_city_page(template, service, city, all_cities)
                    html = html.replace(
                        SERVICE_CONTENT.get(service["slug"], ""),
                        service_content
                    )
                except Exception as e:
                    print(f"  AI failed for {slug}: {e}, using template")
                    html = generate_city_page(template, service, city, all_cities)
            else:
                html = generate_city_page(template, service, city, all_cities)

            os.makedirs(out_dir, exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"  wrote: /{slug}/index.html")
            generated += 1

    print(f"\nDone. Generated: {generated}, Skipped (already exist): {skipped}")
    print(f"Run with --force to overwrite existing pages.")


if __name__ == "__main__":
    main()
