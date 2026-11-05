"""Ajoute les boutons « Partager » aux pages générées du site (idempotent)."""
import re, sys, os

ROOT = sys.argv[1]
PAGES = ['index.html', 'astrologie', 'formation-astrologie', 'hypnose', 'energetique',
         'qui-suis-je', 'avis', 'cabinet', 'contact', 'carte-cadeau', 'questions-frequentes',
         'articles-videos', 'videos-astrologie', 'videos-developpement-personnel', 'quiz']

ICON = ('<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" '
        'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="2.6"/>'
        '<circle cx="6" cy="12" r="2.6"/><circle cx="18" cy="19" r="2.6"/><path d="M8.3 10.8l7.4-4.3M8.3 13.2l7.4 4.3"/></svg>')

STYLE = '''<style id="partage-style">
.share-zone{max-width:1180px;margin:0 auto;padding:34px 20px 42px;text-align:center;border-top:1px solid var(--line,rgba(239,231,216,.12));}
.share-q{margin:0 0 14px;font-size:15.5px;color:var(--paper,#EFE7D8);opacity:.85;}
.share-btn{display:inline-flex;align-items:center;gap:10px;padding:11px 22px;border-radius:999px;cursor:pointer;
  font:inherit;font-size:15px;letter-spacing:.02em;color:var(--gold-soft,#DDAE5E);background:rgba(221,174,94,.07);
  border:1px solid var(--gold-soft,#DDAE5E);transition:background .25s ease,transform .25s ease;}
.share-btn:hover,.share-btn:focus-visible{background:rgba(221,174,94,.16);transform:translateY(-1px);}
.share-btn:focus-visible{outline:2px solid var(--gold-soft,#DDAE5E);outline-offset:3px;}
.share-btn-sm{padding:8px 16px;font-size:14px;}
.share-inline{margin-top:16px;display:flex;align-items:center;gap:12px;flex-wrap:wrap;}
.share-ok{display:block;min-height:1.4em;margin-top:8px;font-size:13.5px;color:var(--gold-soft,#DDAE5E);}
.share-inline .share-ok{display:inline;margin:0;}
</style>'''

SCRIPT = '''<script id="partage-script">
(function(){
  function copier(t){
    if(navigator.clipboard&&window.isSecureContext){return navigator.clipboard.writeText(t);}
    return new Promise(function(ok,ko){try{var a=document.createElement('textarea');a.value=t;a.setAttribute('readonly','');
      a.style.position='fixed';a.style.opacity='0';document.body.appendChild(a);a.select();
      var r=document.execCommand('copy');document.body.removeChild(a);r?ok():ko();}catch(e){ko(e);}});
  }
  document.addEventListener('click',function(e){
    var b=e.target.closest&&e.target.closest('[data-share]');if(!b)return;
    var url=b.getAttribute('data-share-url')||(location.origin+location.pathname);
    var titre=b.getAttribute('data-share-title')||document.title;
    var msg=b.parentNode.querySelector('.share-ok');
    function dire(t){if(!msg)return;msg.textContent=t;clearTimeout(msg._t);msg._t=setTimeout(function(){msg.textContent='';},3500);}
    if(navigator.share){navigator.share({title:titre,url:url}).catch(function(){});return;}
    copier(url).then(function(){dire('Lien copié ✓ Vous pouvez le coller où vous voulez.');},
      function(){dire(url);});
  });
})();
</script>'''

def bouton(label, extra='', cls='share-btn'):
    return ('<button type="button" class="%s" data-share data-umami-event="partage"%s>%s<span>%s</span></button>'
            % (cls, extra, ICON, label))

ZONE = ('<!-- partage -->\n<div class="share-zone"><p class="share-q">Cette page peut intéresser quelqu\'un autour de vous&nbsp;?</p>'
        + bouton('Partager cette page') + '<span class="share-ok" role="status" aria-live="polite"></span></div>\n<!-- /partage -->\n')

TARIFS = ('<!-- partage-tarifs --><div class="share-inline">'
          + bouton('Partager ces prestations',
                   ' data-share-url="https://liliangitton.fr/astrologie/#astro-prestations"'
                   ' data-share-title="Thème astral : prestations et tarifs — Lilian Gitton"',
                   'share-btn share-btn-sm')
          + '<span class="share-ok" role="status" aria-live="polite"></span></div><!-- /partage-tarifs -->')

def nettoie(h):
    h = re.sub(r'<!-- partage -->.*?<!-- /partage -->\n', '', h, flags=re.S)
    h = re.sub(r'<!-- partage-tarifs -->.*?<!-- /partage-tarifs -->', '', h, flags=re.S)
    h = re.sub(r'<style id="partage-style">.*?</style>\n?', '', h, flags=re.S)
    h = re.sub(r'<script id="partage-script">.*?</script>\n?', '', h, flags=re.S)
    return h

for p in PAGES:
    f = os.path.join(ROOT, p if p.endswith('.html') else os.path.join(p, 'index.html'))
    h = nettoie(open(f, encoding='utf-8').read())
    assert h.count('<footer') == 1, f
    h = h.replace('</head>', STYLE + '\n</head>', 1)
    i = h.index('<footer')
    h = h[:i] + ZONE + h[i:]
    if p == 'astrologie':
        a = 'Découvrez la carte cadeau</a>, à acheter en ligne.</p>'
        assert h.count(a) == 1
        h = h.replace(a, a + '\n      ' + TARIFS, 1)
    h = h.replace('</body>', SCRIPT + '\n</body>', 1)
    open(f, 'w', encoding='utf-8').write(h)
    print('ok', p)
