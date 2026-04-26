import os, re

root = r"D:\Downloads\rose-medical-static"

# Pattern: footer inside wrapper, need to move it after wrapper closes
# Structure to find:
#   <footer class="rose-footer">...</footer>
#   </div> <!-- close div.mkdf-wrapper-inner  -->
# </div> <!-- close div.mkdf-wrapper -->
#
# Desired:
#   </div> <!-- close div.mkdf-wrapper-inner  -->
# </div> <!-- close div.mkdf-wrapper -->
# <footer class="rose-footer">...</footer>

footer_pattern = re.compile(
    r'(<footer class="rose-footer">.*?</footer>)\s*\n(\s*</div>[^\n]*mkdf-wrapper-inner[^\n]*\n</div>[^\n]*mkdf-wrapper[^\n]*)',
    re.DOTALL
)

count = 0
for dirpath, dirnames, filenames in os.walk(root):
    for fname in filenames:
        if fname != "index.html":
            continue
        fpath = os.path.join(dirpath, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            html = f.read()
        
        m = footer_pattern.search(html)
        if not m:
            continue
        
        footer_html = m.group(1)
        closing_divs = m.group(2)
        
        new_html = html.replace(
            m.group(0),
            closing_divs + "\n" + footer_html
        )
        
        if new_html != html:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_html)
            count += 1

print(f"Moved footer outside wrapper in {count} files")
