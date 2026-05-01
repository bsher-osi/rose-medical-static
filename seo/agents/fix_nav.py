#!/usr/bin/env python3
"""Replace simplified flat nav in blog posts and interior pages with full dropdown nav."""
import os, re

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

FULL_NAV = '''<div class="mkdf-menu-area mkdf-menu-right"><div class="mkdf-grid"><div class="mkdf-vertical-align-containers">
  <div class="mkdf-position-left"><div class="mkdf-position-left-inner">
    <div class="mkdf-logo-wrapper"><a href="/"><img class="mkdf-normal-logo" src="/wp-content/uploads/2023/11/Rose-Logo_ROSE-2.png" width="1201" height="1200" alt="Rose Medical Pavilion"><img class="mkdf-dark-logo" src="/wp-content/uploads/2023/11/Rose-Logo_ROSE-2.png" width="1201" height="1200" alt="Rose Medical Pavilion"></a></div>
  </div></div>
  <div class="mkdf-position-right"><div class="mkdf-position-right-inner">
    <nav class="mkdf-main-menu mkdf-drop-down mkdf-default-nav"><ul class="clearfix">
<li class="menu-item narrow"><a href="/"><span class="item_outer"><span class="item_text">Home</span></span></a></li>
<li class="menu-item menu-item-has-children has_sub narrow"><a href="/about-us/"><span class="item_outer"><span class="item_text">About Us</span><i class="mkdf-menu-arrow fa fa-angle-down"></i></span></a>
<div class="second"><div class="inner"><ul>
  <li class="menu-item"><a href="/about-us/announcements/"><span class="item_outer"><span class="item_text">Announcements</span></span></a></li>
</ul></div></div>
</li>
<li class="menu-item menu-item-has-children has_sub narrow"><a href="/conditions-we-treat/"><span class="item_outer"><span class="item_text">Conditions We Treat</span><i class="mkdf-menu-arrow fa fa-angle-down"></i></span></a>
<div class="second"><div class="inner"><ul>
  <li class="menu-item"><a href="/pediatric-epilepsy-phoenix/"><span class="item_outer"><span class="item_text">Epilepsy</span></span></a></li>
  <li class="menu-item"><a href="/pediatric-seizures-phoenix/"><span class="item_outer"><span class="item_text">Seizures</span></span></a></li>
  <li class="menu-item"><a href="/pediatric-headaches-phoenix/"><span class="item_outer"><span class="item_text">Headaches &amp; Migraines</span></span></a></li>
  <li class="menu-item"><a href="/developmental-delays-phoenix/"><span class="item_outer"><span class="item_text">Developmental Delays</span></span></a></li>
  <li class="menu-item"><a href="/tourette-syndrome-phoenix/"><span class="item_outer"><span class="item_text">Tourette Syndrome</span></span></a></li>
  <li class="menu-item"><a href="/cerebral-palsy-muscle-disease-phoenix/"><span class="item_outer"><span class="item_text">Cerebral Palsy &amp; Muscle Disease</span></span></a></li>
  <li class="menu-item"><a href="/movement-disorders-phoenix/"><span class="item_outer"><span class="item_text">Movement Disorders</span></span></a></li>
  <li class="menu-item"><a href="/tic-disorders-phoenix/"><span class="item_outer"><span class="item_text">Tic Disorders</span></span></a></li>
  <li class="menu-item"><a href="/pediatric-concussion-phoenix/"><span class="item_outer"><span class="item_text">Concussion</span></span></a></li>
  <li class="menu-item"><a href="/traumatic-brain-injury-phoenix/"><span class="item_outer"><span class="item_text">Traumatic Brain Injury</span></span></a></li>
  <li class="menu-item"><a href="/nerve-injury-phoenix/"><span class="item_outer"><span class="item_text">Nerve Injury</span></span></a></li>
  <li class="menu-item"><a href="/brain-mri-children-phoenix/"><span class="item_outer"><span class="item_text">Brain MRI</span></span></a></li>
  <li class="menu-item"><a href="/pediatric-eeg-phoenix/"><span class="item_outer"><span class="item_text">EEG Testing</span></span></a></li>
  <li class="menu-item"><a href="/visual-disturbances-children-phoenix/"><span class="item_outer"><span class="item_text">Visual Disturbances</span></span></a></li>
  <li class="menu-item"><a href="/dizziness-vertigo-children-phoenix/"><span class="item_outer"><span class="item_text">Dizziness &amp; Vertigo</span></span></a></li>
  <li class="menu-item"><a href="/syncope-loss-of-consciousness-phoenix/"><span class="item_outer"><span class="item_text">Syncope / Loss of Consciousness</span></span></a></li>
  <li class="menu-item"><a href="/insomnia-children-phoenix/"><span class="item_outer"><span class="item_text">Insomnia</span></span></a></li>
  <li class="menu-item"><a href="/sleep-disorders-children-phoenix/"><span class="item_outer"><span class="item_text">Sleep Disorders</span></span></a></li>
</ul></div></div>
</li>
<li class="menu-item narrow"><a href="/blogs/"><span class="item_outer"><span class="item_text">Blog</span></span></a></li>
<li class="menu-item narrow"><a href="/refer-a-patient/"><span class="item_outer"><span class="item_text">Refer a Patient</span></span></a></li>
<li class="menu-item narrow"><a href="/careers/"><span class="item_outer"><span class="item_text">Careers</span></span></a></li>
<li class="menu-item menu-item-has-children has_sub narrow"><a href="https://www.onpatient.com/login/"><span class="item_outer"><span class="item_text">Patient Portal</span><i class="mkdf-menu-arrow fa fa-angle-down"></i></span></a>
<div class="second"><div class="inner"><ul>
  <li class="menu-item"><a href="/wp-content/uploads/2025/03/Onpatient-portal-sign-up-directions.pdf"><span class="item_outer"><span class="item_text">Portal Sign-Up Instructions</span></span></a></li>
</ul></div></div>
</li>
<li class="menu-item menu-item-has-children has_sub narrow"><a href="/contact-us/"><span class="item_outer"><span class="item_text">Contact Us</span><i class="mkdf-menu-arrow fa fa-angle-down"></i></span></a>
<div class="second"><div class="inner"><ul>
  <li class="menu-item"><a href="/schedule-online/"><span class="item_outer"><span class="item_text">Schedule Online</span></span></a></li>
</ul></div></div>
</li>
    </ul></nav>
  </div></div>
</div></div></div>'''

# Pattern to match the old simplified header area in blog posts / conditions-we-treat
OLD_NAV_PATTERN = re.compile(
    r'<div class="mkdf-menu-area mkdf-menu-right">.*?</div></div></div>\s*\n</header>',
    re.DOTALL
)

TARGETS = []
# Blog posts
for slug in os.listdir(os.path.join(REPO_ROOT, "blogs")):
    path = os.path.join(REPO_ROOT, "blogs", slug, "index.html")
    if os.path.exists(path):
        TARGETS.append(path)
# Conditions we treat
TARGETS.append(os.path.join(REPO_ROOT, "conditions-we-treat", "index.html"))

for path in TARGETS:
    with open(path, encoding="utf-8") as f:
        html = f.read()

    # Check if it has the simplified flat nav (blog template style)
    if '<li class="menu-item narrow"><a href="/"><span class="item_outer"><span class="item_text">Home</span></span></a></li>' not in html:
        print(f"  skip (already full nav or no match): {path}")
        continue

    # Also ensure modules.min.js is present before </body>
    if 'modules.min.js' not in html:
        html = html.replace(
            '</body>',
            '<script src="/wp-content/themes/mediclinic/assets/js/modules.min.js?ver=6.9.4"></script>\n</body>'
        )

    # Replace the header nav section
    match = OLD_NAV_PATTERN.search(html)
    if match:
        html = html[:match.start()] + FULL_NAV + '\n</header>' + html[match.end():]
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  updated: {path}")
    else:
        print(f"  no match for old nav pattern: {path}")

print("Done.")
