// Email obfuscation: reassemble protected email links on page load
(function(){
  var u = 'info', d = 'rosemedicalpavilion.com';
  var addr = u + '@' + d;
  var href = 'mailto:' + addr;
  // Text + link: show email address
  document.querySelectorAll('.rose-email').forEach(function(el){
    if(el.tagName === 'A') el.href = href;
    el.textContent = addr;
  });
  // Icon slot: fix href only, don't write text
  document.querySelectorAll('.rose-email-icon').forEach(function(el){
    if(el.tagName === 'A') el.href = href;
  });
})();
