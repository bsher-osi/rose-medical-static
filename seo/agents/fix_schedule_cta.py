#!/usr/bin/env python3
"""
Wrap the bare "Schedule a Consultation" h3+p into a styled grey box
across all condition pages, localized pages, and blog posts.
"""
import os, re, glob

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# Match the bare h3 + p pattern (with optional leading whitespace)
PAT = re.compile(
    r'([ \t]*)<h3>Schedule a(?:n Appointment| Consultation)</h3>\s*'
    r'([ \t]*)<p>(.*?)</p>',
    re.DOTALL
)

BOX = '''\
<div style="margin:2em 0;padding:1.5em 2em;background:#f5f5f5;border-radius:8px;border-top:3px solid #005da8;">
  <h3 style="margin:0 0 0.6em;color:#005da8;font-size:1.2rem;">Schedule a Consultation</h3>
  <p style="margin:0 0 1em;color:#2c2c2c;">{body}</p>
  <a href="/schedule-online/" style="display:inline-block;background:#de7f68;color:#fff;padding:10px 22px;border-radius:4px;text-decoration:none;font-weight:600;font-size:0.95rem;">Schedule Online &rarr;</a>
</div>'''


def process_file(path):
    with open(path, encoding='utf-8') as f:
        html = f.read()

    if 'fix-schedule-cta' in html:
        return False  # already done

    def replacer(m):
        body = m.group(3).strip()
        return '<!-- fix-schedule-cta -->\n' + BOX.format(body=body)

    new_html, n = PAT.subn(replacer, html)
    if n == 0:
        return False

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    return True


def main():
    patterns = [
        '*/index.html',
        'blogs/*/index.html',
        'conditions-we-treat/index.html',
    ]
    updated = skipped = 0
    seen = set()
    for pat in patterns:
        for path in glob.glob(os.path.join(REPO_ROOT, pat)):
            if path in seen:
                continue
            seen.add(path)
            if process_file(path):
                updated += 1
                print(f'  updated: {os.path.relpath(path, REPO_ROOT)}')
            else:
                skipped += 1

    print(f'\nDone. Updated: {updated}  Skipped: {skipped}')


if __name__ == '__main__':
    main()
