import os, re

root = r"D:\Downloads\rose-medical-static"

old_marker = "(function fixGap(){"

new_script = '''<script>
(function fixGap(){
  function fix(){
    // Fix back-to-top button pushed to absolute bottom
    var btn = document.getElementById("mkdf-back-to-top");
    if(btn){
      btn.style.setProperty("position","fixed","important");
      btn.style.setProperty("bottom","24px","important");
      btn.style.setProperty("right","24px","important");
    }
    // Clear any JS-set body/wrapper heights
    document.body.style.removeProperty("padding-bottom");
    document.body.style.removeProperty("margin-bottom");
    document.body.style.removeProperty("height");
    document.body.style.removeProperty("min-height");
    [".mkdf-wrapper",".mkdf-wrapper-inner",".mkdf-content",".mkdf-content-inner"].forEach(function(s){
      var el = document.querySelector(s);
      if(el){ el.style.removeProperty("height"); el.style.removeProperty("min-height"); }
    });
  }
  document.addEventListener("DOMContentLoaded", fix);
  window.addEventListener("load", fix);
  // MutationObserver to catch JS overrides
  document.addEventListener("DOMContentLoaded", function(){
    var btn = document.getElementById("mkdf-back-to-top");
    if(btn){
      new MutationObserver(function(){ fix(); })
        .observe(btn, {attributes:true, attributeFilter:["style"]});
    }
    new MutationObserver(function(){ fix(); })
      .observe(document.body, {attributes:true, attributeFilter:["style"]});
  });
  [100,300,600,1000].forEach(function(ms){ setTimeout(fix,ms); });
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
        new_html = re.sub(r'<script>\s*\(function fixGap\(\).*?</script>', new_script, html, flags=re.DOTALL)
        if new_html != html:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_html)
            count += 1

print(f"Updated {count} files")
