// Email obfuscation: reassemble protected email links on page load
(function(){
  var u = 'info', d = 'rosemedicalpavilion.com';
  var addr = u + '@' + d;
  var href = 'mailto:' + addr;
  document.querySelectorAll('.rose-email, .rose-email-icon').forEach(function(el){
    if(el.tagName === 'A') el.href = href;
    // Don't write text into the icon slot (mkdf-icon-info-icon div) — only the text slot
    var inIconSlot = el.closest ? el.closest('.mkdf-icon-info-icon') : false;
    if(!inIconSlot) el.textContent = addr;
  });
})();
