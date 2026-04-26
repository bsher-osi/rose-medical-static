import os, re

root = r"D:\Downloads\rose-medical-static"

old_script_marker = "(function fixGap(){"

new_script = '''<script>
(function fixGap(){
  function clearBodyPad(){
    document.body.style.setProperty("padding-bottom","0","important");
    document.body.style.setProperty("margin-bottom","0","important");
    document.documentElement.style.setProperty("padding-bottom","0","important");
    [".mkdf-wrapper",".mkdf-wrapper-inner",".mkdf-content",".mkdf-content-inner"].forEach(function(s){
      var el = document.querySelector(s);
      if(el){ el.style.removeProperty("height"); el.style.removeProperty("min-height"); }
    });
  }
  // Run immediately and on load
  document.addEventListener("DOMContentLoaded", clearBodyPad);
  window.addEventListener("load", clearBodyPad);
  // Watch for any inline style mutation on body
  var obs = new MutationObserver(function(mutations){
    mutations.forEach(function(m){
      if(m.attributeName === "style") clearBodyPad();
    });
  });
  document.addEventListener("DOMContentLoaded", function(){
    obs.observe(document.body, {attributes:true, attributeFilter:["style"]});
    clearBodyPad();
  });
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
        # Replace existing fixGap script block
        new_html = re.sub(r'<script>\s*\(function fixGap\(\).*?</script>', new_script, html, flags=re.DOTALL)
        if new_html != html:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_html)
            count += 1

print(f"Updated {count} files")
