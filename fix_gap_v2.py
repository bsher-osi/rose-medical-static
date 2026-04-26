import os, re

root = r"D:\Downloads\rose-medical-static"

old_script = '''<script>
document.addEventListener("DOMContentLoaded",function(){
  var els = document.querySelectorAll(".mkdf-wrapper,.mkdf-wrapper-inner,.mkdf-content,.mkdf-content-inner");
  els.forEach(function(el){ el.style.removeProperty("height"); el.style.removeProperty("min-height"); });
  setTimeout(function(){
    els.forEach(function(el){ el.style.removeProperty("height"); el.style.removeProperty("min-height"); });
  }, 500);
});
</script>'''

new_script = '''<script>
(function fixGap(){
  var sel = ".mkdf-wrapper,.mkdf-wrapper-inner,.mkdf-content,.mkdf-content-inner";
  function clear(){
    document.querySelectorAll(sel).forEach(function(el){
      el.style.removeProperty("height");
      el.style.removeProperty("min-height");
    });
    document.documentElement.style.removeProperty("height");
    document.body.style.removeProperty("height");
    document.body.style.removeProperty("min-height");
  }
  document.addEventListener("DOMContentLoaded", clear);
  window.addEventListener("load", clear);
  [100,300,600,1200].forEach(function(ms){ setTimeout(clear, ms); });
})();
</script>'''

count = 0
for dirpath, dirnames, filenames in os.walk(root):
    for fname in filenames:
        if fname != "index.html":
            continue
        fpath = os.path.join(dirpath, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            html = f.read()
        new_html = html.replace(old_script, new_script)
        if new_html != html:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_html)
            count += 1

print(f"Updated {count} files")
