import os, re

root = r"D:\Downloads\rose-medical-static"

fix_script = '''<script>
document.addEventListener("DOMContentLoaded",function(){
  var els = document.querySelectorAll(".mkdf-wrapper,.mkdf-wrapper-inner,.mkdf-content,.mkdf-content-inner");
  els.forEach(function(el){ el.style.removeProperty("height"); el.style.removeProperty("min-height"); });
  setTimeout(function(){
    els.forEach(function(el){ el.style.removeProperty("height"); el.style.removeProperty("min-height"); });
  }, 500);
});
</script>'''

count = 0
for dirpath, dirnames, filenames in os.walk(root):
    for fname in filenames:
        if fname != "index.html":
            continue
        fpath = os.path.join(dirpath, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            html = f.read()
        if fix_script.strip()[:30] in html:
            continue
        new_html = html.replace("</body>", fix_script + "\n</body>", 1)
        if new_html != html:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_html)
            count += 1

print(f"Patched {count} files")
