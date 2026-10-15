#!/usr/bin/env python3
"""Génère le site multi-pages à partir de _src/source.html (version « une seule page »).

Usage : python3 _src/build.py [dossier_de_sortie]   (par défaut : la racine du dépôt)
"""
import base64, hashlib, json, os, re, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else ROOT
SITE = 'https://liliangitton.fr'

src = open(os.path.join(HERE, 'source.html'), encoding='utf-8').read()

def must(cond, msg):
    if not cond:
        raise SystemExit('ERREUR : ' + msg)

# ------------------------------------------------------------------ images
os.makedirs(os.path.join(OUT, 'img'), exist_ok=True)
os.makedirs(os.path.join(OUT, 'assets'), exist_ok=True)

def save_img(name, data_uri):
    m = re.match(r'data:image/\w+;base64,(.*)$', data_uri, re.S)
    must(m, 'data URI image invalide pour ' + name)
    open(os.path.join(OUT, 'img', name), 'wb').write(base64.b64decode(m.group(1)))
    return '/img/' + name

def find_uri(pattern):
    m = re.search(pattern, src, re.S)
    must(m, 'motif introuvable : ' + pattern)
    return m.group(1)

URI = r'(data:image/\w+;base64,[A-Za-z0-9+/=]+)'
og_uri = find_uri(r'<meta property="og:image" content="' + URI)
fav_uri = find_uri(r'<link rel="icon"[^>]*href="' + URI)
apple_uri = find_uri(r'<link rel="apple-touch-icon"[^>]*href="' + URI)
wm_uri = find_uri(r'<img class="header-watermark" src="' + URI)
portrait_uri = find_uri(r'<img class="portrait" src="' + URI)
cab_uri = find_uri(r'<figure class="cabinet-photo">\s*<img src="' + URI)
IMG = {
    'partage': save_img('partage.jpg', og_uri),
    'fav': save_img('favicon-32.png', fav_uri),
    'apple': save_img('apple-touch-icon.png', apple_uri),
    'wm': save_img('header-watermark.png', wm_uri),
    'portrait': save_img('portrait.jpg', portrait_uri),
    'cabinet': save_img('cabinet.jpg', cab_uri),
}
# les images ne sont plus en base64 dans le code
for k, v in [(og_uri, None), (fav_uri, None)]:
    pass

# ------------------------------------------------------------------ CSS
css = re.search(r'<style>\n(.*?)</style>', src, re.S).group(1)

def dup_h2(m):
    sel, body = m.group(1), m.group(2)
    if not re.search(r'\bh2\b', sel) or re.search(r'\bh1\b', sel):
        return m.group(0)
    parts = [p.strip() for p in sel.split(',')]
    extra = []
    for p in parts:
        if re.search(r'\bh2\b', p):
            q = re.sub(r'^h2\b', 'h1.page-h1', p.strip())
            q = re.sub(r'\bh2\b', 'h1', q)
            extra.append(q)
    return sel.rstrip() + ',\n  ' + ', '.join(extra) + '{' + body + '}'

css = re.sub(r'([^{}@]+)\{([^{}]*)\}', dup_h2, css)
css += '''
/* H1 de page (promus depuis les anciens H2) */
h1.page-h1 svg.section-illustration{vertical-align:middle;}
.page-h1 + .page-sub{margin-top:6px;}
'''
css_hash = hashlib.md5(css.encode()).hexdigest()[:8]
open(os.path.join(OUT, 'assets', 'site.css'), 'w', encoding='utf-8').write(css)
CSS_HREF = '/assets/site.css?v=' + css_hash

# ------------------------------------------------------------------ morceaux du corps
def between(s, a, b, incl=True, start=0):
    i = s.index(a, start)
    j = s.index(b, i) + (len(b) if incl else 0)
    return s[i:j]

header_html = between(src, '<header>', '</header>')
header_html = header_html.replace('src="' + wm_uri + '"', 'src="' + IMG['wm'] + '" alt="" aria-hidden="true"')
nav_script = between(src, '<script>\n  var navToggle', '</script>')
footer_html = between(src, '<footer>', '</footer>')
warp_html = between(src, '<div class="warp"', '</div>')
btt_html = between(src, '<button type="button" class="back-to-top"', '</button>')
cookie_html = between(src, '<div class="cookie-banner"', '</div>\n</div>', incl=False)
cookie_html = cookie_html + '</div>'

pre_scripts = re.findall(r'<script>\n.*?</script>', src[src.index('</header>'):src.index('<section class="hero"')], re.S)
must(len(pre_scripts) == 1, 'scripts avant sections : %d' % len(pre_scripts))
nav_script = pre_scripts[0]
post_scripts = re.findall(r'<script>\n.*?</script>', src[src.index('<footer>'):], re.S)
must(len(post_scripts) == 4, 'scripts après footer : %d' % len(post_scripts))
stars_script, warp_script, wheel_script, _copier = post_scripts
must("Sillage d'étoiles" in warp_script and 'astroWheel' in wheel_script, 'ordre des scripts')

# sections
def section(sid):
    m = re.search(r'<section[^>]*\bid="%s"[^>]*>.*?</section>' % sid, src, re.S)
    must(m, 'section ' + sid)
    return m.group(0)

SEC = {sid: section(sid) for sid in
       ['accueil', 'astrologie', 'energetique', 'hypnose', 'apropos', 'avis', 'contact', 'cabinet', 'blog', 'mentions', 'cgv']}

# ---- astrologie : séparation formation / reste
astro = SEC['astrologie']
i_form = astro.index('<div class="block" id="astro-initiation">')
i_dist = astro.index('<div class="block card-block" style="grid-column:1 / -1;">')
i_nav = astro.index('<nav class="next-steps"')
astro_head = astro[:i_form]
form_block = astro[i_form:i_dist].rstrip() + '\n\n'
dist_block = astro[i_dist:i_nav]
astro_tail = astro[i_nav:]

# illustration du titre astrologie (réutilisée pour la page formation)
illu = re.search(r'<svg class="section-illustration".*?</svg>', astro_head, re.S).group(0)

teaser = '''    <div class="block card-block" style="grid-column:1 / -1;">
      <h3 id="astro-formation">Formation en astrologie</h3>
      <div class="body">
        <p>Envie d'apprendre à lire et à analyser un thème astral par vous-même&nbsp;? Je propose une <strong>formation en astrologie à Orléans et en ligne</strong>, pour débutants comme pour confirmés, en groupe ou en individuel.</p>
        <p class="astro-cta" style="margin-top:14px; font-size:16px;"><a class="xl" href="#astro-initiation">Découvrir la formation en astrologie&nbsp;→</a></p>
      </div>
    </div>

'''
astro_page = astro_head + teaser + dist_block + astro_tail

formation_page = '''<section id="astrologie" class="page-formation">
  <div class="wrap">
    <div class="section-head">
      <div class="kicker">Astrologie</div>
      <h1 class="page-h1">Formation en astrologie à Orléans et en ligne ''' + illu + '''</h1>
      <p>Que vous soyez débutant ou déjà confirmé, apprenez à analyser un thème astral à votre rythme, en groupe ou en individuel, à Orléans ou en visioconférence.</p>
    </div>

    ''' + form_block + dist_block.replace('<h3 id="astro-distance">', '<h3 id="astro-distance">') + '''    <nav class="next-steps" aria-label="Pour aller plus loin"><span class="ns-label">Pour aller plus loin</span><div class="ns-row"><a class="ns-link" href="#astrologie">L'astrologie et les prestations →</a><a class="ns-link" href="/quiz/">Le quiz d'astrologie →</a><a class="btn btn-primary" href="#contact">Prendre rendez-vous</a></div></nav>
  </div>
</section>'''

# ---- titres H1
def promote_h1(html, new_text=None, keep_svg=True):
    """Transforme le premier <h2> de la section en <h1 class="page-h1">, avec un nouveau texte éventuel."""
    m = re.search(r'<h2([^>]*)>(.*?)</h2>', html, re.S)
    must(m, 'h2 introuvable')
    inner = m.group(2)
    svg = re.search(r'<svg class="section-illustration".*?</svg>', inner, re.S)
    if new_text is not None:
        inner = new_text + ((' ' + svg.group(0)) if svg and keep_svg else '')
    attrs = m.group(1)
    new = '<h1 class="page-h1"%s>%s</h1>' % (attrs, inner)
    return html[:m.start()] + new + html[m.end():]

H1 = {
    'astrologie': 'Astrologue à Orléans et à distance',
    'energetique': 'Soins énergétiques à Orléans et à distance',
    'hypnose': 'Hypnose humaniste à Orléans et à distance',
    'apropos': 'Lilian Gitton, astrologue, hypnothérapeute et énergéticien',
    'avis': None,
    'contact': 'Prendre rendez-vous',
    'cabinet': 'Le cabinet à Orléans',
    'blog': 'Mes articles et vidéos',
    'mentions': None,
    'cgv': None,
}
astro_page = promote_h1(astro_page, H1['astrologie'])
CONTENT = {
    'accueil': SEC['accueil'],
    'astrologie': astro_page,
    'formation': formation_page,
}
for k in ['energetique', 'hypnose', 'apropos', 'avis', 'contact', 'cabinet', 'blog', 'mentions', 'cgv']:
    CONTENT[k] = promote_h1(SEC[k], H1[k])

# images : liens vers les fichiers, textes alternatifs plus parlants
CONTENT['accueil'] = CONTENT['accueil'].replace(
    '<img id="homePortrait" alt="Lilian Gitton, hypnothérapeute, énergéticien et astrologue">',
    '<img id="homePortrait" src="%s" alt="Lilian Gitton, astrologue, hypnothérapeute et énergéticien à Orléans">' % IMG['portrait'])
CONTENT['accueil'] = CONTENT['accueil'].replace(
    '<img id="homeCabinet" alt=', '<img id="homeCabinet" src="%s" loading="lazy" alt=' % IMG['cabinet'])
must('src="/img/portrait.jpg"' in CONTENT['accueil'] and 'src="/img/cabinet.jpg"' in CONTENT['accueil'], 'images accueil')
CONTENT['apropos'] = CONTENT['apropos'].replace('<img class="portrait" src="' + portrait_uri + '"',
    '<img class="portrait" src="%s" alt="Lilian Gitton, astrologue, hypnothérapeute et énergéticien à Orléans"' % IMG['portrait'])
# l'alt d'origine éventuel (doublon d'attribut)
CONTENT['apropos'] = re.sub(r'(<img class="portrait"[^>]*?) alt="Lilian Gitton, hypnothérapeute, énergéticien et astrologue"', r'\1', CONTENT['apropos'])
CONTENT['cabinet'] = CONTENT['cabinet'].replace('<img src="' + cab_uri + '"', '<img src="%s" loading="lazy"' % IMG['cabinet'])
for k, v in CONTENT.items():
    must('base64' not in v, 'base64 restant dans ' + k)

# ------------------------------------------------------------------ pages
PAGES = [
    dict(key='accueil', url='/', nav='/', title="Astrologue, hypnothérapeute, énergéticien à Orléans",
         desc="Lilian Gitton, astrologue, hypnothérapeute et énergéticien à Orléans : thème astral, hypnose humaniste et soins énergétiques, en cabinet ou à distance."),
    dict(key='astrologie', url='/astrologie/', nav='/astrologie/', title="Astrologue à Orléans : thème astral, en cabinet ou en visio",
         desc="Astrologue à Orléans : analyse de thème astral selon l'astrologie humaniste, en cabinet ou en visio. Découvrez la démarche, les prestations et les tarifs."),
    dict(key='formation', url='/formation-astrologie/', nav='/astrologie/', title="Formation en astrologie à Orléans et en ligne, débutants et confirmés",
         desc="Formation en astrologie à Orléans et en ligne : cours pour débutants et confirmés, en groupe ou en individuel, pour apprendre à analyser un thème astral."),
    dict(key='hypnose', url='/hypnose/', nav='/hypnose/', title="Hypnose humaniste à Orléans et à distance, hypnothérapeute",
         desc="Hypnose humaniste à Orléans et à distance avec Lilian Gitton, hypnothérapeute : séances en cabinet ou en visio, pour être accompagné à votre rythme."),
    dict(key='energetique', url='/energetique/', nav='/energetique/', title="Soins énergétiques à Orléans : rééquilibrage, chakras, aura",
         desc="Soins énergétiques à Orléans et à distance : rééquilibrage énergétique, harmonisation des chakras, nettoyage de l'aura et ancrage, avec Lilian Gitton."),
    dict(key='apropos', url='/qui-suis-je/', nav='/qui-suis-je/', title="Qui est Lilian Gitton ? Astrologue, hypnothérapeute et énergéticien",
         desc="Qui est Lilian Gitton ? Astrologue, hypnothérapeute et énergéticien à Orléans : son parcours, sa façon d'accompagner et les pratiques qu'il propose."),
    dict(key='avis', url='/avis/', nav='/avis/', title="Avis clients sur Lilian Gitton, Orléans",
         desc="Avis de clients sur Lilian Gitton, astrologue, hypnothérapeute et énergéticien à Orléans : leurs témoignages sur le thème astral, l'hypnose et les soins."),
    dict(key='cabinet', url='/cabinet/', nav='/cabinet/', title="Cabinet à Orléans : adresse, accès et plan",
         desc="Le cabinet de Lilian Gitton à Orléans, 24 rue du Clos Rozé, près du Jardin des Plantes : adresse, accès et plan pour venir en séance."),
    dict(key='contact', url='/contact/', nav='/contact/', title="Prendre rendez-vous avec Lilian Gitton, à Orléans ou en visio",
         desc="Prenez rendez-vous avec Lilian Gitton, à Orléans ou en visio : téléphone, e-mail, WhatsApp. Une question ? Écrivez-moi, on en parle simplement."),
    dict(key='blog', url='/articles-videos/', nav='/articles-videos/', title="Articles et vidéos sur l'astrologie et le développement personnel",
         desc="Articles et vidéos de Lilian Gitton sur l'astrologie, la spiritualité et le développement personnel : vidéos pédagogiques et textes à lire."),
    dict(key='mentions', url='/mentions-legales/', nav='', title="Mentions légales — Lilian Gitton",
         desc="Mentions légales du site de Lilian Gitton, astrologue, hypnothérapeute et énergéticien à Orléans."),
    dict(key='cgv', url='/cgv/', nav='', title="Conditions générales de vente — Lilian Gitton",
         desc="Conditions générales de vente des prestations de Lilian Gitton : astrologie, hypnose humaniste et soins énergétiques à Orléans et à distance."),
]
URL_OF = {p['key']: p['url'] for p in PAGES}

SECTION_URL = {
    'accueil': '/', 'astrologie': '/astrologie/', 'energetique': '/energetique/', 'hypnose': '/hypnose/',
    'apropos': '/qui-suis-je/', 'avis': '/avis/', 'contact': '/contact/', 'cabinet': '/cabinet/',
    'blog': '/articles-videos/', 'mentions': '/mentions-legales/', 'cgv': '/cgv/',
    'astro-initiation': '/formation-astrologie/',
}
SECTION_IDS = set(SECTION_URL) - {'astro-initiation'}

def ids_of(html):
    return set(re.findall(r'\bid="([^"]+)"', html))

# page qui « possède » chaque identifiant (priorité = ordre de PAGES)
OWNER = {}
for p in PAGES:
    for i in ids_of(CONTENT[p['key']]):
        OWNER.setdefault(i, p['key'])

def target(i):
    if i in SECTION_URL:
        return SECTION_URL[i]
    if i in OWNER:
        return URL_OF[OWNER[i]] + '#' + i
    print('  ! ancre inconnue : #' + i)
    return '/#' + i

def rewrite(html, own, absolute=False):
    def r(m):
        i = m.group(1)
        if not i:
            return m.group(0)
        if not absolute and i in own and i not in SECTION_IDS:
            return m.group(0)
        return 'href="%s"' % target(i)
    return re.sub(r'href="#([^"]*)"', r, html)

# --------------------------------------------------------------- JSON-LD
ld = json.loads(re.search(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', src, re.S).group(1))
ld.pop('aggregateRating', None)
ld.pop('review', None)
ld['url'] = SITE + '/'
ld['image'] = SITE + IMG['partage']
ld['@id'] = SITE + '/#cabinet'

def jsonld(p):
    blocks = [ld]
    if p['key'] != 'accueil':
        crumbs = [{'@type': 'ListItem', 'position': 1, 'name': 'Accueil', 'item': SITE + '/'},
                  {'@type': 'ListItem', 'position': 2, 'name': p['title'], 'item': SITE + p['url']}]
        blocks.append({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': crumbs})
    return '\n'.join('<script type="application/ld+json">\n%s\n</script>' % json.dumps(b, ensure_ascii=False, indent=2) for b in blocks)

# --------------------------------------------------------------- éléments d'en-tête communs
fonts_links = re.findall(r'<link rel="preconnect"[^>]*>|<link href="https://fonts\.googleapis[^>]*>', src)
manifest = re.search(r'<link rel="manifest"[^>]*>', src).group(0)
apple_meta = re.findall(r'<meta name="(?:apple-mobile-web-app-[a-z-]+|mobile-web-app-capable|theme-color)"[^>]*>', src)

# --------------------------------------------------------------- scripts adaptés
def adapt_nav_script(s):
    # 1. 2e appui : le 1er appui sur une rubrique à sous-menu ne fait que déplier le sous-menu
    a = "      keepPanelOpen = true;   // le changement de rubrique qui suit ne doit pas refermer le menu"
    must(a in s, 'nav: keepPanelOpen')
    s = s.replace(a, "      e.preventDefault();\n" + a)
    # 2. navigation par onglets -> vraies pages
    i0 = s.index("  // Navigation par onglets")
    i1 = s.index("    // Orbite des icônes")
    new_nav = '''  // Chaque rubrique est maintenant une vraie page ; ce code gère seulement les ancres à l'intérieur d'une page
  document.addEventListener('DOMContentLoaded', function(){
    var tabSections = Array.prototype.slice.call(document.querySelectorAll('section[id]'));
    tabSections.forEach(function(s){ s.classList.add('tab-active'); });
    document.dispatchEvent(new CustomEvent('tabchange', { detail: tabSections[0] ? tabSections[0].id : '' }));

    function scrollToId(id, smooth){
      var target = document.getElementById(id);
      if(!target) return false;
      var headerEl = document.querySelector('header');
      var headerH = headerEl ? headerEl.offsetHeight : 0;
      var top = target.getBoundingClientRect().top + window.pageYOffset - headerH - 14;
      window.scrollTo({ top: top, behavior: smooth ? 'smooth' : 'auto' });
      return true;
    }

    // Lien vers une ancre de la page en cours : défilement doux, en tenant compte du bandeau
    document.addEventListener('click', function(e){
      if(e.defaultPrevented || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey || e.button) return;
      var link = e.target.closest && e.target.closest('a[href]');
      if(!link || link.target === '_blank') return;
      var u;
      try{ u = new URL(link.getAttribute('href'), location.href); }catch(err){ return; }
      if(u.origin !== location.origin || u.pathname !== location.pathname) return;
      if(!u.hash){
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: 'smooth' });
        return;
      }
      var id = decodeURIComponent(u.hash.slice(1));
      if(!document.getElementById(id)) return;
      e.preventDefault();
      try{ history.replaceState(null, '', u.pathname + u.hash); }catch(err){}
      setTimeout(function(){ scrollToId(id, true); }, 60);
    });

    // Arrivée sur une page avec une ancre dans l'adresse
    if(location.hash){
      var hid = decodeURIComponent(location.hash.slice(1));
      setTimeout(function(){ scrollToId(hid, false); }, 150);
      window.addEventListener('load', function(){ setTimeout(function(){ scrollToId(hid, false); }, 150); });
    }

'''
    s = s[:i0] + new_nav + s[i1:]
    # 3. page en cours soulignée
    m = re.search(r"      function mark\(id\)\{.*?if\(cur\) mark\(cur\.id\);\n", s, re.S)
    must(m, 'nav: mark')
    s = s[:m.start()] + '''      var here = document.body.getAttribute('data-nav') || '';
      links.forEach(function(a){
        if(here && a.getAttribute('href') === here){ a.setAttribute('aria-current', 'page'); }
        else { a.removeAttribute('aria-current'); }
      });
''' + s[m.end():]
    s = s.replace("""document.querySelectorAll('.nav ul > li > a[href^="#"]')""", """document.querySelectorAll('.nav ul > li > a[href]')""")
    must('a[href^="#"]' not in s.split('Bandeau compact')[1].split('Bouton Contact')[0], 'nav: sélecteur de liens')
    return s

nav_script_new = adapt_nav_script(nav_script)

def adapt_warp(s):
    return s.replace("document.querySelectorAll('h2')", "document.querySelectorAll('h2, h1.page-h1')")

warp_new = adapt_warp(warp_script)
must("h1.page-h1" in warp_new, 'warp h1')
stars_new = stars_script.replace("h2, .about-top .body", "h2, h1.page-h1, .about-top .body")
must('h1.page-h1' in stars_new, 'reveal h1')

legacy_map = {}
for i in sorted(OWNER):
    t = target(i)
    if t != '/' and not t.startswith('/#'):
        legacy_map[i] = t
for i, t in SECTION_URL.items():
    if t != '/':
        legacy_map[i] = t
legacy_script = '<script>(function(){var h=location.hash.slice(1);if(!h)return;var m=%s;if(m[h])location.replace(m[h]);})();</script>' % json.dumps(legacy_map, ensure_ascii=False, separators=(',', ':'))

# --------------------------------------------------------------- assemblage
def build_page(p):
    key = p['key']
    content = CONTENT[key]
    own = ids_of(content)
    content = rewrite(content, own)
    content = content.replace('<section', '<section', 1)
    content = re.sub(r'<section((?:(?!>)[^>])*)\bclass="([^"]*)"', lambda m: '<section%sclass="%s tab-active"' % (m.group(1), m.group(2)), content, count=1) \
        if re.match(r'<section[^>]*\bclass="', content) else content.replace('<section', '<section class="tab-active"', 1)
    canon = SITE + p['url']
    title_full = p['title'] if p['key'] != 'accueil' else p['title']
    head = ['<!DOCTYPE html>', '<html lang="fr">', '<head>', '<meta charset="UTF-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
            '<title>%s</title>' % title_full,
            '<meta name="description" content="%s">' % p['desc'],
            '<meta name="robots" content="index, follow, max-image-preview:large">',
            '<link rel="canonical" href="%s">' % canon,
            '<meta property="og:type" content="website">', '<meta property="og:locale" content="fr_FR">',
            '<meta property="og:site_name" content="Lilian Gitton">',
            '<meta property="og:title" content="%s">' % title_full,
            '<meta property="og:description" content="%s">' % p['desc'],
            '<meta property="og:image" content="%s%s">' % (SITE, IMG['partage']),
            '<meta property="og:url" content="%s">' % canon,
            '<meta name="twitter:card" content="summary_large_image">',
            '<meta name="twitter:title" content="%s">' % title_full,
            '<meta name="twitter:description" content="%s">' % p['desc'],
            '<meta name="twitter:image" content="%s%s">' % (SITE, IMG['partage']),
            ] + fonts_links + [
            '<link rel="stylesheet" href="%s">' % CSS_HREF,
            '<link rel="icon" type="image/png" sizes="32x32" href="%s">' % IMG['fav'],
            manifest] + apple_meta + [
            '<link rel="apple-touch-icon" sizes="180x180" href="%s">' % IMG['apple'],
            jsonld(p)]
    if key == 'accueil':
        head.append(legacy_script)
    head.append('</head>')
    body = ['<body data-nav="%s">' % p['nav'],
            '<div class="stars-bg" id="starsBg"></div>', '<div class="grain"></div>', '<div class="site-content">',
            rewrite(header_html, set(), absolute=True), nav_script_new, warp_new, content,
            rewrite(footer_html, set(), absolute=True), warp_html, btt_html]
    if key == 'cabinet':
        body.append(cookie_html)
    body.append('</div>')
    body.append(stars_new)
    if 'id="astroWheel"' in content:
        body.append(wheel_script)
    body.append('</body>\n</html>\n')
    return '\n'.join(head) + '\n' + '\n'.join(body)

# nettoyage : le cookie banner ne sert qu'à la page cabinet
for p in PAGES:
    html = build_page(p)
    d = OUT if p['url'] == '/' else os.path.join(OUT, p['url'].strip('/'))
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(html)
    print('%-26s %7d octets' % (p['url'], len(html.encode())))

# --------------------------------------------------------------- 404, sitemap, robots
notfound_content = '''<section id="introuvable" class="tab-active">
  <div class="wrap">
    <div class="section-head">
      <div class="kicker">Erreur 404</div>
      <h1 class="page-h1">Cette page est introuvable</h1>
      <p>La page que vous cherchez n'existe plus ou a changé d'adresse. Voici de quoi retrouver votre chemin&nbsp;:</p>
    </div>
    <nav class="next-steps" aria-label="Pour aller plus loin"><div class="ns-row"><a class="ns-link" href="/">Retour à l'accueil →</a><a class="ns-link" href="/astrologie/">Astrologie →</a><a class="ns-link" href="/hypnose/">Hypnose humaniste →</a><a class="ns-link" href="/energetique/">Soins énergétiques →</a><a class="btn btn-primary" href="/contact/">Prendre rendez-vous</a></div></nav>
  </div>
</section>'''
CONTENT['_404'] = notfound_content
p404 = dict(key='_404', url='/404.html', nav='', title='Page introuvable — Lilian Gitton', desc='Page introuvable sur le site de Lilian Gitton.')
h404 = build_page(p404).replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">')
h404 = re.sub(r'<link rel="canonical"[^>]*>\n', '', h404)
open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8').write(h404)

today = datetime.date.today().isoformat()
urls = ''.join('  <url><loc>%s%s</loc><lastmod>%s</lastmod></url>\n' % (SITE, p['url'], today) for p in PAGES)
urls += '  <url><loc>%s/quiz/</loc><lastmod>%s</lastmod></url>\n' % (SITE, today)
open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8').write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n')
open(os.path.join(OUT, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\nDisallow: /_src/\n\nSitemap: %s/sitemap.xml\n' % SITE)
print('OK')
