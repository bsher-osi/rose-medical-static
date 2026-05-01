#!/usr/bin/env python3
"""
Generate blog posts for Rose Medical Pavilion using Claude AI.

Usage:
  python blog_writer.py --topic childhood-seizures-arizona-guide
  python blog_writer.py --all
  python blog_writer.py --count 3
  python blog_writer.py --count 2 --dry-run
"""

import argparse
import os
import re
import sys
import yaml
from datetime import date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "../config.yml")
BLOG_DIR = os.path.join(REPO_ROOT, "blogs")

HTML_TEMPLATE = '''<!DOCTYPE html>
<html dir="ltr" lang="en-US" prefix="og: https://ogp.me/ns#">
<head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=yes">
<title>{title} | Rose Medical Pavilion Blog</title>
<meta name="description" content="{description}">
<link rel="canonical" href="https://rosemedicalpavilion.com/blogs/{slug}/">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="https://rosemedicalpavilion.com/blogs/{slug}/">
<meta property="og:type" content="article">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BlogPosting",
  "headline":"{title}",
  "description":"{description}",
  "url":"https://rosemedicalpavilion.com/blogs/{slug}/",
  "datePublished":"{pub_date}",
  "author":{{"@type":"Physician","name":"Dr. Tamara Zach MD","url":"https://rosemedicalpavilion.com/about-us/"}},
  "publisher":{{"@type":"Organization","name":"Rose Medical Pavilion","url":"https://rosemedicalpavilion.com/"}}
}}
</script>
<link rel="stylesheet" href="/wp-content/themes/mediclinic/style.css?ver=6.9.4">
<link rel="stylesheet" href="/wp-content/themes/mediclinic/assets/css/modules.min.css?ver=6.9.4">
<link rel="stylesheet" href="/wp-content/themes/mediclinic/assets/css/font-awesome/css/font-awesome.min.css?ver=6.9.4">
<link rel="stylesheet" href="/wp-content/themes/mediclinic/assets/css/ion-icons/css/ionicons.min.css?ver=6.9.4">
<link rel="stylesheet" href="/wp-content/themes/mediclinic/assets/css/style_dynamic.css?ver=1704067333">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Poppins%3A300%2C400%2C500%7COpen+Sans%3A300%2C400%2C500&subset=latin-ext">
<link rel="stylesheet" href="/refresh.css">
<script src="/wp-includes/js/jquery/jquery.min.js?ver=3.7.1"></script>
<script src="https://www.googletagmanager.com/gtag/js?id=GT-TX5XVLK" async></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","GT-TX5XVLK");</script>
</head>
<body class="single-post">
<div class="mkdf-wrapper"><div class="mkdf-wrapper-inner">
<header class="mkdf-page-header">
<div class="mkdf-menu-area mkdf-menu-right"><div class="mkdf-grid"><div class="mkdf-vertical-align-containers">
  <div class="mkdf-position-left"><div class="mkdf-position-left-inner">
    <div class="mkdf-logo-wrapper"><a href="/"><img src="/wp-content/uploads/2023/11/Rose-Logo_ROSE-2.png" width="200" alt="Rose Medical Pavilion"></a></div>
  </div></div>
  <div class="mkdf-position-right"><div class="mkdf-position-right-inner">
    <nav class="mkdf-main-menu mkdf-drop-down mkdf-default-nav"><ul class="clearfix">
      <li class="menu-item narrow"><a href="/"><span class="item_outer"><span class="item_text">Home</span></span></a></li>
      <li class="menu-item narrow"><a href="/about-us/"><span class="item_outer"><span class="item_text">About Us</span></span></a></li>
      <li class="menu-item narrow"><a href="/conditions-we-treat/"><span class="item_outer"><span class="item_text">Conditions We Treat</span></span></a></li>
      <li class="menu-item narrow"><a href="/blogs/"><span class="item_outer"><span class="item_text">Blog</span></span></a></li>
      <li class="menu-item narrow"><a href="/refer-a-patient/"><span class="item_outer"><span class="item_text">Refer a Patient</span></span></a></li>
      <li class="menu-item narrow"><a href="/careers/"><span class="item_outer"><span class="item_text">Careers</span></span></a></li>
      <li class="menu-item narrow"><a href="/contact-us/"><span class="item_outer"><span class="item_text">Contact Us</span></span></a></li>
      <li class="menu-item narrow"><a href="/schedule-online/"><span class="item_outer"><span class="item_text">Schedule Online</span></span></a></li>
    </ul></nav>
  </div></div>
</div></div></div>
</header>
<div class="mkdf-content"><div class="mkdf-content-inner">
<div class="mkdf-title mkdf-standard-type mkdf-content-left-alignment mkdf-preload-background mkdf-has-background" style="height:200px;background-image:url(/wp-content/uploads/2017/04/blog-parallax-1.jpg);">
  <div class="mkdf-title-holder" style="height:200px;"><div class="mkdf-container clearfix"><div class="mkdf-container-inner">
    <div class="mkdf-title-subtitle-holder"><div class="mkdf-title-subtitle-holder-inner">
      <h1 class="mkdf-page-title entry-title"><span>{title}</span></h1>
    </div></div>
  </div></div></div>
</div>
<div class="mkdf-container mkdf-default-page-template"><div class="mkdf-container-inner clearfix">
<div class="mkdf-grid-row"><div class="mkdf-page-content-holder mkdf-grid-col-12">
<nav aria-label="Breadcrumb" style="margin-bottom:1em;font-size:0.9em;">
  <a href="/">Home</a> &rsaquo; <a href="/blogs/">Blog</a> &rsaquo; {title}
</nav>
<p style="color:#888;font-size:0.9em;">By Dr. Tamara Zach MD &mdash; {pub_date_display}</p>
{body}
<hr style="margin:2em 0;">
<div style="background:#f8f4f2;padding:1.5em;border-left:4px solid #de7f68;">
  <h3 style="margin-top:0;">Schedule an Appointment</h3>
  <p>Questions about your child's neurological health? Dr. Tamara Zach MD at Rose Medical Pavilion is here to help. Call <strong><a href="tel:+16232577673">(623) 257-ROSE (7673)</a></strong> or <a href="/schedule-online/">schedule online</a>.</p>
</div>
</div></div>
</div></div>
</div></div>
</div></div>
<footer class="rose-footer">
  <div class="rose-footer-inner">
    <div class="rose-footer-col"><i class="ion-android-call rose-footer-icon"></i><h4>Call</h4><p>(623) 257-ROSE (7673)</p></div>
    <div class="rose-footer-col"><i class="ion-location rose-footer-icon"></i><h4>Location</h4><p>22044 N 44th St, Suite 200<br>Phoenix, AZ 85050</p></div>
    <div class="rose-footer-col"><i class="ion-calendar rose-footer-icon"></i><h4>Request an appointment</h4>
      <a href="/schedule-online/" class="rose-footer-btn rose-footer-btn-coral">Schedule Online</a>
      <a href="/refer-a-patient/" class="rose-footer-btn rose-footer-btn-blue">Refer Patient</a>
    </div>
  </div>
  <div class="rose-footer-bottom"><p>&copy; 2026 Rose Medical Pavilion All Rights Reserved</p></div>
</footer>
</body></html>
'''


def send_draft_email(topics_written, config):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    smtp_user = os.environ.get("SMTP_USER", "")
    smtp_pass = os.environ.get("SMTP_PASS", "")
    if not smtp_user or not smtp_pass:
        print("No SMTP credentials — skipping draft email")
        return

    previews = ""
    for slug, title, body in topics_written:
        previews += f"""
<div style="border:1px solid #eee;border-radius:4px;padding:1.5em;margin-bottom:1.5em;">
  <h3 style="color:#005da8;margin-top:0;">{title}</h3>
  <p style="font-size:0.85em;color:#888;">URL: https://rosemedicalpavilion.com/blogs/{slug}/</p>
  {body[:2000]}{'...' if len(body) > 2000 else ''}
</div>"""

    slugs = ", ".join(s for s, _, __ in topics_written)
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"[Blog Drafts for Review] {len(topics_written)} new post(s) — auto-publish in 24 hrs"
    msg["From"] = "Rose Medical Pavilion <benjamin@rosemedicalpavilion.com>"
    msg["To"] = "tz@rosemedicalpavilion.com, benjaminsher@gmail.com"

    plain = f"""New blog post drafts for review.

Posts: {slugs}
These will auto-publish in approximately 24 hours.

To REJECT a post before it goes live, go to:
https://github.com/bsher-osi/rose-medical-static/actions
and run the "Reject Blog Draft" workflow with the slug name.

— Rose Medical Pavilion Blog Automation
"""
    html = f"""<html><body style="font-family:Arial,sans-serif;color:#333;max-width:700px;margin:0 auto;">
<div style="background:#005da8;padding:20px 32px;">
  <h2 style="color:#fff;margin:0;">Blog Drafts for Review</h2>
</div>
<div style="padding:24px;">
  <p><strong>{len(topics_written)} new post(s)</strong> will auto-publish in ~24 hours.</p>
  <p style="color:#888;font-size:0.9em;">To reject a post, run the <em>Reject Blog Draft</em> workflow on GitHub Actions with the post slug.</p>
  <hr style="border:none;border-top:1px solid #eee;margin:20px 0;">
  {previews}
</div>
</body></html>"""

    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(smtp_user, smtp_pass)
        server.sendmail(
            "benjamin@rosemedicalpavilion.com",
            ["tz@rosemedicalpavilion.com", "benjaminsher@gmail.com"],
            msg.as_string()
        )
    print(f"Draft review email sent for: {slugs}")


def load_config():
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def generate_post(topic, config):
    import anthropic
    practice = config["practice"]

    keywords_str = ", ".join(topic.get("keywords", []))
    prompt = f"""Write a high-quality blog post for a pediatric neurology practice website.

Practice: {practice['name']}
Doctor: {practice['doctor']}
Location: Phoenix, AZ
Title: {topic['title']}
Target keywords: {keywords_str}
Category: {topic.get('category', 'neurology')}

Requirements:
- 900-1100 words
- Use H2 and H3 headings
- Arizona-specific content (heat, AzEIP, AHCCCS, local resources when relevant)
- E-E-A-T signals: cite medical expertise, reference Dr. Tamara Zach MD naturally
- End with a brief CTA to schedule at Rose Medical Pavilion (no contact info needed — we add that)
- Return HTML only (h2, h3, p, ul, ol tags — no full page wrapper, no <html>/<body>/<head>)
- Do not include the H1 title (we add that separately)
- Naturally include 2-3 internal links to relevant pages on the site (use full anchor tags):
  * Seizures/epilepsy topics: <a href="/pediatric-seizures-phoenix/">pediatric seizures</a> or <a href="/pediatric-epilepsy-phoenix/">pediatric epilepsy</a>
  * Headache/migraine topics: <a href="/pediatric-headaches-phoenix/">pediatric headaches</a>
  * EEG/brain monitoring: <a href="/pediatric-eeg-phoenix/">pediatric EEG</a>
  * Concussion topics: <a href="/pediatric-concussion-phoenix/">pediatric concussion care</a>
  * Tics/Tourette topics: <a href="/tics/">tics and Tourette syndrome</a>
  * General "about our practice": <a href="/about-us/">about Dr. Tamara Zach MD</a>
  Only link to pages that are genuinely relevant to the post content.

Write the post now:"""

    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )
    text = message.content[0].text.strip()
    # Strip markdown code fences if Claude wrapped the response
    if text.startswith("```"):
        text = re.sub(r"^```[a-z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text)
    return text.strip()


def build_html(topic, body):
    slug = topic["slug"]
    title = topic["title"]
    today = date.today()
    description = f"{title} — Expert pediatric neurology insights from Dr. Zach Rose MD at Rose Medical Pavilion, Phoenix AZ."
    return HTML_TEMPLATE.format(
        title=title,
        description=description,
        slug=slug,
        pub_date=today.isoformat(),
        pub_date_display=today.strftime("%B %d, %Y"),
        body=body,
    )


def main():
    parser = argparse.ArgumentParser(description="Generate blog posts for Rose Medical Pavilion")
    parser.add_argument("--topic", help="Blog topic slug")
    parser.add_argument("--all", action="store_true", help="Generate all blog topics")
    parser.add_argument("--count", type=int, default=0, help="Generate N random unwritten topics")
    parser.add_argument("--dry-run", action="store_true", help="Print topics without generating")
    parser.add_argument("--force", action="store_true", help="Overwrite existing posts")
    args = parser.parse_args()

    config = load_config()
    topics = config.get("blog_topics", [])

    if args.topic:
        topics = [t for t in topics if t["slug"] == args.topic]
        if not topics:
            print(f"Topic not found: {args.topic}")
            sys.exit(1)
    elif args.count:
        unwritten = []
        for t in topics:
            out_path = os.path.join(BLOG_DIR, t["slug"], "index.html")
            if not os.path.exists(out_path):
                unwritten.append(t)
        topics = unwritten[:args.count]
        if not topics:
            print("All topics already generated. Use --force to regenerate.")
            sys.exit(0)
    elif not args.all:
        parser.print_help()
        sys.exit(1)

    topics_written = []
    for topic in topics:
        out_dir = os.path.join(BLOG_DIR, topic["slug"])
        out_path = os.path.join(out_dir, "index.html")

        if os.path.exists(out_path) and not args.force:
            print(f"  skip (exists): {topic['slug']}")
            continue

        if args.dry_run:
            print(f"  [dry-run] {topic['title']}")
            continue

        print(f"  generating: {topic['title']} ...")
        try:
            body = generate_post(topic, config)
            html = build_html(topic, body)
            os.makedirs(out_dir, exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(html)
            topics_written.append((topic["slug"], topic["title"], body))
            print(f"    wrote: /blogs/{topic['slug']}/index.html")
        except Exception as e:
            print(f"    ERROR: {e}")

    if topics_written:
        try:
            send_draft_email(topics_written, config)
        except Exception as e:
            print(f"  Email error: {e}")

    print("\nDone.")


if __name__ == "__main__":
    main()
