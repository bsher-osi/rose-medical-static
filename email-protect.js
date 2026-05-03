// Email obfuscation: reassemble protected email links on page load
(function(){
  var u = 'info', d = 'rosemedicalpavilion.com';
  var addr = u + '@' + d;
  var href = 'mailto:' + addr;
  document.querySelectorAll('.rose-email').forEach(function(el){
    if(el.tagName === 'A') el.href = href;
    el.textContent = addr;
  });
})();
