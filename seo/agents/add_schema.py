#!/usr/bin/env python3
"""
Add JSON-LD structured data to key pages:
- Homepage: MedicalBusiness + Physician
- Main condition pages: MedicalCondition + Physician
- Blog posts: BlogPosting + Physician
"""
import os, re, glob, json

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

PRACTICE = {
    "@context": "https://schema.org",
    "@type": "MedicalBusiness",
    "name": "Rose Medical Pavilion",
    "description": "Pediatric neurology practice serving families across Arizona. Dr. Tamara Zach MD specializes in epilepsy, seizures, developmental delays, headaches, and more.",
    "url": "https://rosemedicalpavilion.com",
    "telephone": "+16232577673",
    "email": "info@rosemedicalpavilion.com",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "22044 N 44th St, Suite 200",
        "addressLocality": "Phoenix",
        "addressRegion": "AZ",
        "postalCode": "85050",
        "addressCountry": "US"
    },
    "geo": {
        "@type": "GeoCoordinates",
        "latitude": 33.6832,
        "longitude": -111.9782
    },
    "openingHoursSpecification": [{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
        "opens": "08:00",
        "closes": "16:00"
    }],
    "medicalSpecialty": "Neurology",
    "hasMap": "https://www.google.com/maps/dir/?api=1&destination=22044+N+44th+St+Suite+200+Phoenix+AZ+85050",
    "image": "https://rosemedicalpavilion.com/wp-content/uploads/2023/11/Rose-Logo_ROSE-2.png",
    "priceRange": "$$",
    "currenciesAccepted": "USD",
    "paymentAccepted": "Insurance, Credit Card"
}

PHYSICIAN = {
    "@context": "https://schema.org",
    "@type": "Physician",
    "name": "Dr. Tamara Zach MD",
    "medicalSpecialty": "Neurology",
    "description": "Fellowship-trained pediatric neurologist at Rose Medical Pavilion in Phoenix, AZ.",
    "worksFor": {"@type": "MedicalBusiness", "name": "Rose Medical Pavilion"},
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "22044 N 44th St, Suite 200",
        "addressLocality": "Phoenix",
        "addressRegion": "AZ",
        "postalCode": "85050",
        "addressCountry": "US"
    },
    "telephone": "+16232577673",
    "url": "https://rosemedicalpavilion.com/about-us/"
}

CONDITION_NAMES = {
    "pediatric-epilepsy-phoenix": ("Epilepsy", "https://rosemedicalpavilion.com/pediatric-epilepsy-phoenix/"),
    "pediatric-seizures-phoenix": ("Seizure Disorder", "https://rosemedicalpavilion.com/pediatric-seizures-phoenix/"),
    "developmental-delays-phoenix": ("Developmental Delay", "https://rosemedicalpavilion.com/developmental-delays-phoenix/"),
    "pediatric-headaches-phoenix": ("Headache", "https://rosemedicalpavilion.com/pediatric-headaches-phoenix/"),
    "cerebral-palsy-muscle-disease-phoenix": ("Cerebral Palsy", "https://rosemedicalpavilion.com/cerebral-palsy-muscle-disease-phoenix/"),
    "movement-disorders-phoenix": ("Movement Disorder", "https://rosemedicalpavilion.com/movement-disorders-phoenix/"),
    "tic-disorders-phoenix": ("Tic Disorder", "https://rosemedicalpavilion.com/tic-disorders-phoenix/"),
    "sleep-disorders-children-phoenix": ("Sleep Disorder", "https://rosemedicalpavilion.com/sleep-disorders-children-phoenix/"),
    "dizziness-vertigo-children-phoenix": ("Vertigo", "https://rosemedicalpavilion.com/dizziness-vertigo-children-phoenix/"),
    "traumatic-brain-injury-phoenix": ("Traumatic Brain Injury", "https://rosemedicalpavilion.com/traumatic-brain-injury-phoenix/"),
    "pediatric-concussion-phoenix": ("Concussion", "https://rosemedicalpavilion.com/pediatric-concussion-phoenix/"),
    "nerve-injury-phoenix": ("Peripheral Neuropathy", "https://rosemedicalpavilion.com/nerve-injury-phoenix/"),
    "insomnia-children-phoenix": ("Insomnia", "https://rosemedicalpavilion.com/insomnia-children-phoenix/"),
    "syncope-loss-of-consciousness-phoenix": ("Syncope", "https://rosemedicalpavilion.com/syncope-loss-of-consciousness-phoenix/"),
    "visual-disturbances-children-phoenix": ("Visual Disturbance", "https://rosemedicalpavilion.com/visual-disturbances-children-phoenix/"),
    "brain-mri-children-phoenix": ("Brain MRI", "https://rosemedicalpavilion.com/brain-mri-children-phoenix/"),
    "pediatric-eeg-phoenix": ("Electroencephalography", "https://rosemedicalpavilion.com/pediatric-eeg-phoenix/"),
}


def schema_tag(data):
    return f'<script type="application/ld+json">\n{json.dumps(data, indent=2)}\n</script>'


def inject_schema(html, schemas):
    marker = '</head>'
    if marker not in html:
        return html, False
    tags = "\n".join(schema_tag(s) for s in schemas)
    return html.replace(marker, tags + "\n" + marker, 1), True


def process_homepage():
    path = os.path.join(REPO_ROOT, "index.html")
    if not os.path.exists(path):
        return False
    with open(path, encoding='utf-8') as f:
        html = f.read()
    if 'application/ld+json' in html:
        return False
    html, ok = inject_schema(html, [PRACTICE, PHYSICIAN])
    if ok:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
    return ok


def process_condition_pages():
    updated = 0
    for slug, (condition_name, page_url) in CONDITION_NAMES.items():
        path = os.path.join(REPO_ROOT, slug, "index.html")
        if not os.path.exists(path):
            continue
        with open(path, encoding='utf-8') as f:
            html = f.read()
        if 'application/ld+json' in html:
            continue
        schema = {
            "@context": "https://schema.org",
            "@type": "MedicalWebPage",
            "name": f"Pediatric {condition_name} Treatment | Rose Medical Pavilion",
            "url": page_url,
            "about": {
                "@type": "MedicalCondition",
                "name": condition_name
            },
            "author": {
                "@type": "Physician",
                "name": "Dr. Tamara Zach MD",
                "medicalSpecialty": "Neurology"
            },
            "publisher": {
                "@type": "MedicalBusiness",
                "name": "Rose Medical Pavilion",
                "telephone": "+16232577673",
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "22044 N 44th St, Suite 200",
                    "addressLocality": "Phoenix",
                    "addressRegion": "AZ",
                    "postalCode": "85050"
                }
            }
        }
        html, ok = inject_schema(html, [schema, PHYSICIAN])
        if ok:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html)
            updated += 1
            print(f"  schema: {slug}")
    return updated


def process_blog_posts():
    updated = 0
    for path in glob.glob(os.path.join(REPO_ROOT, "blogs/*/index.html")):
        with open(path, encoding='utf-8') as f:
            html = f.read()
        if 'application/ld+json' in html:
            continue
        # Extract title from <title> tag
        m = re.search(r'<title>([^<]+)</title>', html)
        title = m.group(1).split('|')[0].strip() if m else "Blog Post"
        slug_dir = os.path.basename(os.path.dirname(path))
        schema = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": title,
            "url": f"https://rosemedicalpavilion.com/blogs/{slug_dir}/",
            "author": {
                "@type": "Physician",
                "name": "Dr. Tamara Zach MD",
                "medicalSpecialty": "Neurology"
            },
            "publisher": {
                "@type": "MedicalBusiness",
                "name": "Rose Medical Pavilion",
                "url": "https://rosemedicalpavilion.com"
            },
            "mainEntityOfPage": f"https://rosemedicalpavilion.com/blogs/{slug_dir}/"
        }
        html, ok = inject_schema(html, [schema])
        if ok:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html)
            updated += 1
    return updated


def main():
    hp = process_homepage()
    print(f"Homepage: {'updated' if hp else 'skipped'}")
    c = process_condition_pages()
    print(f"Condition pages updated: {c}")
    b = process_blog_posts()
    print(f"Blog posts updated: {b}")


if __name__ == "__main__":
    main()
