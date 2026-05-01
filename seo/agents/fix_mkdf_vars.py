#!/usr/bin/env python3
"""
Fix blog posts and conditions-we-treat:
1. Inject mkdfGlobalVars so modules.min.js can initialize dropdowns
2. Add top bar to blog posts
3. Fix conditions-we-treat card text color and hero contrast
"""
import os, re

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

MKDF_VARS = '''<script>var mkdfGlobalVars={"vars":{"mkdfAddForAdminBar":0,"mkdfElementAppearAmount":-100,"mkdfAjaxUrl":"/wp-admin/admin-ajax.php","mkdfStickyHeaderHeight":0,"mkdfStickyHeaderTransparencyHeight":70,"mkdfTopBarHeight":46,"mkdfLogoAreaHeight":0,"mkdfMenuAreaHeight":90,"mkdfMobileHeaderHeight":70}};var mkdfPerPageVars={"vars":{"mkdfStickyScrollAmount":0,"mkdfHeaderTransparencyHeight":0}};</script>'''

TOP_BAR = '''<div class="mkdf-top-bar">
  <div class="mkdf-grid">
    <div class="mkdf-vertical-align-containers">
      <div class="mkdf-position-left"><div class="mkdf-position-left-inner">
        <span style="font-size:13px;color:#6b6b6b;font-weight:400;">Dr. Tamara Zach</span>
      </div></div>
      <div class="mkdf-position-right"><div class="mkdf-position-right-inner">
        <a href="tel:+16232577673" style="font-size:13px;color:#6b6b6b;">(623) 257-ROSE (7673)</a>
        &nbsp;&nbsp;|&nbsp;&nbsp; <span style="font-size:13px;color:#6b6b6b;">Mon&ndash;Fri: 8:00AM&ndash;4:00PM</span>
        &nbsp;&nbsp;|&nbsp;&nbsp; <a href="mailto:info@rosemedicalpavilion.com" style="font-size:13px;color:#6b6b6b;">info@rosemedicalpavilion.com</a>
      </div></div>
    </div>
  </div>
</div>
'''

# Files to update
BLOG_DIRS = [d for d in os.listdir(os.path.join(REPO_ROOT, "blogs"))
             if os.path.isdir(os.path.join(REPO_ROOT, "blogs", d))]
TARGETS = [os.path.join(REPO_ROOT, "blogs", d, "index.html") for d in BLOG_DIRS]
TARGETS.append(os.path.join(REPO_ROOT, "conditions-we-treat", "index.html"))

for path in TARGETS:
    if not os.path.exists(path):
        continue
    with open(path, encoding="utf-8") as f:
        html = f.read()

    changed = False

    # 1. Inject mkdfGlobalVars before modules.min.js
    if "mkdfGlobalVars" not in html and "modules.min.js" in html:
        html = html.replace(
            '<script src="/wp-content/themes/mediclinic/assets/js/modules.min.js',
            MKDF_VARS + '\n<script src="/wp-content/themes/mediclinic/assets/js/modules.min.js'
        )
        changed = True

    # 2. Add top bar to blog posts (not conditions-we-treat which already has it)
    is_blog = "/blogs/" in path.replace("\\", "/")
    if is_blog and "mkdf-top-bar" not in html and "<header class=\"mkdf-page-header\">" in html:
        html = html.replace(
            '<header class="mkdf-page-header">\n<div class="mkdf-menu-area',
            '<header class="mkdf-page-header">\n' + TOP_BAR + '<div class="mkdf-menu-area'
        )
        changed = True

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  updated: {os.path.basename(os.path.dirname(path))}")
    else:
        print(f"  skip: {os.path.basename(os.path.dirname(path))}")

print("Done.")
