#!/usr/bin/env python3
"""
Replace the simplified header on blog posts and conditions-we-treat with
the full site header (sticky header + mobile hamburger menu) from About Us.
Also fixes body class and updates blog_writer.py template.
"""
import os, re

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

BODY_CLASS = 'class="page-template-default page wp-theme-mediclinic mkdf-core-2.0 mediclinic-ver-2.0 mkdf-grid-1200 mkdf-sticky-header-on-scroll-down-up mkdf-dropdown-animate-height mkdf-header-standard mkdf-menu-area-in-grid-shadow-disable mkdf-default-mobile-header mkdf-sticky-up-mobile-header"'

FULL_HEADER = '''\
<div class="mkdf-top-bar">
  <div class="mkdf-grid">
    <div class="mkdf-vertical-align-containers">
      <div class="mkdf-position-left"><div class="mkdf-position-left-inner">
        <div class="widget widget_text mkdf-top-bar-widget"><div class="textwidget"><span style="font-weight:400;">Dr. Tamara Zach</span></div></div>
      </div></div>
      <div class="mkdf-position-right"><div class="mkdf-position-right-inner">
        <div class="widget mkdf-icon-info-widget"><div class="mkdf-info-icon clearfix mkdf-icon-info-icon-medium">
          <div class="mkdf-icon-info-icon"><a href="tel:+16232577673"><span class="mkdf-icon-shortcode mkdf-normal"><i class="mkdf-icon-ion-icon ion-android-call mkdf-icon-element" style="color:#005da8;font-size:15px"></i></span></a></div>
          <div class="mkdf-info-icon-content"><a href="tel:+16232577673"><span class="mkdf-info-icon-title-text" style="color:#6b6b6b;font-size:13px;font-weight:400">(623) 257-ROSE (7673)</span></a></div>
        </div></div>
        <div class="widget mkdf-icon-info-widget"><div class="mkdf-info-icon clearfix mkdf-icon-info-icon-medium">
          <div class="mkdf-icon-info-icon"><span class="mkdf-icon-shortcode mkdf-normal"><i class="mkdf-icon-ion-icon ion-ios-clock mkdf-icon-element" style="color:#005da8;font-size:15px"></i></span></div>
          <div class="mkdf-info-icon-content"><span class="mkdf-info-icon-title-text" style="color:#6b6b6b;font-size:13px;font-weight:400">Mon - Fri: 8:00AM - 4:00PM</span></div>
        </div></div>
        <div class="widget mkdf-icon-info-widget"><div class="mkdf-info-icon clearfix mkdf-icon-info-icon-medium">
          <div class="mkdf-icon-info-icon"><a href="mailto:info@rosemedicalpavilion.com"><span class="mkdf-icon-shortcode mkdf-normal"><i class="mkdf-icon-ion-icon ion-ios-email mkdf-icon-element" style="color:#005da8;font-size:20px"></i></span></a></div>
          <div class="mkdf-info-icon-content"><a href="mailto:info@rosemedicalpavilion.com"><span class="mkdf-info-icon-title-text" style="color:#6b6b6b;font-size:13px;font-weight:400">info@rosemedicalpavilion.com</span></a></div>
        </div></div>
      </div></div>
    </div>
  </div>
</div>

<header class="mkdf-page-header">
<div class="mkdf-menu-area mkdf-menu-right"><div class="mkdf-grid"><div class="mkdf-vertical-align-containers">
  <div class="mkdf-position-left"><div class="mkdf-position-left-inner">
    <div class="mkdf-logo-wrapper">
      <a itemprop="url" href="/" style="height:auto;display:flex;align-items:center;">
        <img fetchpriority="high" itemprop="image" class="mkdf-normal-logo" src="/wp-content/uploads/2023/11/Rose-Logo_ROSE-2.png" width="1201" height="1200" alt="logo">
        <img itemprop="image" class="mkdf-dark-logo" src="/wp-content/uploads/2023/11/Rose-Logo_ROSE-2.png" width="1201" height="1200" alt="dark logo">
      </a>
    </div>
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
<li class="menu-item narrow"><a href="/refer-a-patient/"><span class="item_outer"><span class="item_text">Refer a patient</span></span></a></li>
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
</div></div></div>
<div class="mkdf-sticky-header">
  <div class="mkdf-sticky-holder">
    <div class="mkdf-vertical-align-containers">
      <div class="mkdf-position-left"><div class="mkdf-position-left-inner">
        <div class="mkdf-logo-wrapper">
          <a itemprop="url" href="/" style="height:auto;display:flex;align-items:center;">
            <img fetchpriority="high" itemprop="image" class="mkdf-normal-logo" src="/wp-content/uploads/2023/11/Rose-Logo_ROSE-2.png" width="1201" height="1200" alt="logo">
          </a>
        </div>
      </div></div>
      <div class="mkdf-position-right"><div class="mkdf-position-right-inner">
        <nav class="mkdf-main-menu mkdf-drop-down mkdf-sticky-nav"><ul class="clearfix">
          <li class="menu-item narrow"><a href="/"><span class="item_outer"><span class="item_text">Home</span><span class="plus"></span></span></a></li>
          <li class="menu-item narrow"><a href="/about-us/"><span class="item_outer"><span class="item_text">About Us</span><span class="plus"></span></span></a></li>
          <li class="menu-item narrow"><a href="/conditions-we-treat/"><span class="item_outer"><span class="item_text">Conditions We Treat</span><span class="plus"></span></span></a></li>
          <li class="menu-item narrow"><a href="/blogs/"><span class="item_outer"><span class="item_text">Blog</span><span class="plus"></span></span></a></li>
          <li class="menu-item narrow"><a href="/contact-us/"><span class="item_outer"><span class="item_text">Contact Us</span><span class="plus"></span></span></a></li>
        </ul></nav>
      </div></div>
    </div>
  </div>
</div>
</header>

<header class="mkdf-mobile-header">
<div class="mkdf-mobile-header-inner">
  <div class="mkdf-mobile-header-holder">
    <div class="mkdf-grid">
      <div class="mkdf-vertical-align-containers">
        <div class="mkdf-mobile-menu-opener">
          <a href="javascript:void(0)"><span class="mkdf-mobile-menu-icon"><i class="fa fa-bars" aria-hidden="true"></i></span></a>
        </div>
        <div class="mkdf-position-center"><div class="mkdf-position-center-inner">
          <div class="mkdf-mobile-logo-wrapper">
            <a itemprop="url" href="/"><img itemprop="image" class="mkdf-normal-logo" src="/wp-content/uploads/2023/11/Rose-Logo_ROSE-2.png" width="1201" height="1200" alt="Mobile Logo"></a>
          </div>
        </div></div>
      </div>
    </div>
  </div>
  <nav class="mkdf-mobile-nav" role="navigation" aria-label="Mobile Menu">
    <div class="mkdf-grid"><ul>
      <li class="menu-item"><a href="/"><span>Home</span></a></li>
      <li class="menu-item"><a href="/about-us/"><span>About Us</span></a></li>
      <li class="menu-item menu-item-has-children has_sub"><a href="/conditions-we-treat/" class="mkdf-mobile-no-link"><span>Conditions We Treat</span></a><span class="mobile_arrow"><i class="mkdf-sub-arrow fa fa-angle-right"></i><i class="fa fa-angle-down"></i></span>
        <ul class="sub_menu">
          <li><a href="/pediatric-epilepsy-phoenix/"><span>Epilepsy</span></a></li>
          <li><a href="/pediatric-seizures-phoenix/"><span>Seizures</span></a></li>
          <li><a href="/pediatric-headaches-phoenix/"><span>Headaches &amp; Migraines</span></a></li>
          <li><a href="/developmental-delays-phoenix/"><span>Developmental Delays</span></a></li>
          <li><a href="/tourette-syndrome-phoenix/"><span>Tourette Syndrome</span></a></li>
          <li><a href="/cerebral-palsy-muscle-disease-phoenix/"><span>Cerebral Palsy &amp; Muscle Disease</span></a></li>
          <li><a href="/movement-disorders-phoenix/"><span>Movement Disorders</span></a></li>
          <li><a href="/tic-disorders-phoenix/"><span>Tic Disorders</span></a></li>
          <li><a href="/pediatric-concussion-phoenix/"><span>Concussion</span></a></li>
          <li><a href="/traumatic-brain-injury-phoenix/"><span>Traumatic Brain Injury</span></a></li>
          <li><a href="/brain-mri-children-phoenix/"><span>Brain MRI</span></a></li>
          <li><a href="/pediatric-eeg-phoenix/"><span>EEG Testing</span></a></li>
          <li><a href="/sleep-disorders-children-phoenix/"><span>Sleep Disorders</span></a></li>
          <li><a href="/insomnia-children-phoenix/"><span>Insomnia</span></a></li>
        </ul>
      </li>
      <li class="menu-item"><a href="/blogs/"><span>Blog</span></a></li>
      <li class="menu-item"><a href="/refer-a-patient/"><span>Refer a patient</span></a></li>
      <li class="menu-item"><a href="/careers/"><span>Careers</span></a></li>
      <li class="menu-item"><a href="https://www.onpatient.com/login/"><span>Patient Portal</span></a></li>
      <li class="menu-item"><a href="/contact-us/"><span>Contact Us</span></a></li>
    </ul></div>
  </nav>
</div>
</header>'''

# Old header pattern used in blog posts / CWT (starts after mkdf-wrapper-inner, before mkdf-content)
OLD_HEADER_PAT = re.compile(
    r'<header class="mkdf-page-header">\s*<div class="mkdf-top-bar">.*?</header>\s*(?=<div class="mkdf-content|<div class="cwt-hero)',
    re.DOTALL
)
# Also handle pages that have mkdf-top-bar BEFORE <header>
OLD_TOPBAR_HEADER_PAT = re.compile(
    r'<div class="mkdf-top-bar">.*?</header>\s*(?=<div class="mkdf-content|<div class="cwt-hero)',
    re.DOTALL
)

TARGETS = []
for slug in os.listdir(os.path.join(REPO_ROOT, "blogs")):
    p = os.path.join(REPO_ROOT, "blogs", slug, "index.html")
    if os.path.exists(p):
        TARGETS.append(p)
TARGETS.append(os.path.join(REPO_ROOT, "conditions-we-treat", "index.html"))

for path in TARGETS:
    with open(path, encoding="utf-8") as f:
        html = f.read()

    if "mkdf-sticky-header" in html:
        print(f"  skip (already full header): {os.path.basename(os.path.dirname(path))}")
        continue

    # Fix body class
    for old_body in ['class="single-post"', 'class="page-template-default page"']:
        if old_body in html:
            html = html.replace(old_body, BODY_CLASS, 1)

    # Replace old header block
    m = OLD_TOPBAR_HEADER_PAT.search(html)
    if m:
        html = html[:m.start()] + FULL_HEADER + "\n" + html[m.end():]
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  updated: {os.path.basename(os.path.dirname(path))}")
    else:
        print(f"  no match: {path}")

print("Done.")
