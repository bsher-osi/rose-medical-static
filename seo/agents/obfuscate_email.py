#!/usr/bin/env python3
"""
Obfuscate info@rosemedicalpavilion.com across all static HTML pages.
- Replaces mailto: hrefs with # and adds class="rose-email"
- Replaces plain text instances with <span class="rose-email"></span>
- Injects email-protect.js before </body> if not already present
"""
import os, re, glob

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
EMAIL = "info@rosemedicalpavilion.com"
MAILTO = f"mailto:{EMAIL}"
SCRIPT_TAG = '<script src="/email-protect.js"></script>'

# Pattern: <a href="mailto:info@...">...visible text...</a>
MAILTO_PAT = re.compile(
    r'<a\b([^>]*?)href=["\']mailto:info@rosemedicalpavilion\.com["\']([^>]*?)>(.*?)</a>',
    re.DOTALL | re.IGNORECASE
)
# Plain text email not inside an <a>
PLAIN_PAT = re.compile(r'(?<!mailto:)(?<!["\'])info@rosemedicalpavilion\.com(?!["\'])')


def process(path):
    with open(path, encoding='utf-8') as f:
        html = f.read()

    if 'rose-email' in html:
        return False  # already done

    # Replace mailto: links
    def replace_link(m):
        before, after, text = m.group(1), m.group(2), m.group(3)
        # strip existing href-related attrs already handled
        before = before.strip()
        after = after.strip()
        attrs = ((' ' + before) if before else '') + ((' ' + after) if after else '')
        return f'<a href="#"{attrs} class="rose-email"></a>'

    html = MAILTO_PAT.sub(replace_link, html)

    # Replace remaining plain-text email occurrences (not in href strings)
    # Be careful not to replace inside script/style blocks carelessly
    html = PLAIN_PAT.sub('<span class="rose-email"></span>', html)

    # Inject script before </body>
    if SCRIPT_TAG not in html:
        html = html.replace('</body>', SCRIPT_TAG + '\n</body>', 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return True


def main():
    files = glob.glob(os.path.join(REPO_ROOT, '*/index.html')) + \
            glob.glob(os.path.join(REPO_ROOT, 'index.html')) + \
            glob.glob(os.path.join(REPO_ROOT, 'blogs/*/index.html'))
    updated = skipped = 0
    for path in files:
        if 'seo/' in path.replace('\\', '/'):
            continue
        if process(path):
            updated += 1
        else:
            skipped += 1
    print(f"Done. Updated: {updated}  Skipped (already done): {skipped}")


if __name__ == '__main__':
    main()
