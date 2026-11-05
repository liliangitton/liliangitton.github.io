"""Crée la page /theme-astral/ à partir de la page /astrologie/ (même en-tête, menu, pied de page).
Lancer à la racine du dépôt : python3 _src/theme-astral.py"""
import re, json, os

SITE = 'https://liliangitton.fr'
URL = '/theme-astral/'
TITLE = 'Thème astral à Orléans : déroulé et tarifs | Lilian Gitton'
DESC = ("Faire son thème astral à Orléans ou à distance avec Lilian Gitton, astrologue humaniste : "
        "ce qu'il peut vous apporter, déroulé, tarifs (150 €, version approfondie 250 €).")

FAQ = [
    ("Dois-je préparer quelque chose ?",
     "Rien de compliqué : avant notre court échange téléphonique, demandez-vous simplement ce que vous en attendez. "
     "Une ou deux questions qui vous tiennent à cœur suffisent, elles me serviront de fil conducteur."),
    ("Comment payer ?",
     "Espèces, chèque, carte bancaire ou virement. Un autre moyen ? Demandez-moi."),
    ("Peut-on offrir un thème astral ?",
     "Oui, avec la carte cadeau, à acheter en ligne. Elle est valable un an."),
]

def faq_html():
    out = []
    for q, a in FAQ:
        a_html = a.replace('carte cadeau', '<a class="xl" href="/carte-cadeau/">carte cadeau</a>', 1)
        out.append('      <details><summary>%s</summary><div class="faq-a"><p>%s</p></div></details>' % (q, a_html))
    return '\n'.join(out)

CONTENT = '''<section class="tab-active" id="theme-astral">
  <div class="wrap">
    <div class="section-head">
      <div class="kicker">Astrologie</div>
      <h1 class="page-h1">Thème astral à Orléans et à distance</h1>
      <p>Que vous traversiez une période de questionnements, un changement de vie, ou simplement l'envie de mieux vous connaître, <strong>votre thème astral est un point de départ</strong>. Je vous reçois au cabinet à Orléans, ou à distance.</p>
      <p class="astro-cta" style="margin-top:14px; font-size:16px;"><a class="xl" href="#ta-tarifs">Voir les tarifs&nbsp;→</a></p>
    </div>

    <div class="block">
      <h2 class="sous-titre" id="ta-apport">Ce que votre thème astral peut vous apporter</h2>
      <div class="body">
        <p>L'étude de votre thème astral : comprendre ses potentiels ; mieux cerner ses défis pour les transcender ; mettre du sens à sa vie, aux événements passés, présents et voir ses différents cycles à venir ; et surtout peut aider à se rapprocher de son Soi, de qui nous sommes en profondeur.</p>
      </div>
    </div>

    <div class="block">
      <h2 class="sous-titre" id="ta-methode">Ma façon de travailler</h2>
      <div class="body">
        <p>Toutes ces prestations seront réalisées avec rigueur, et dans une démarche d'adaptation à qui vous êtes et où vous en êtes dans votre chemin de vie. Ma "recette" consiste à réaliser un <span class="u">travail de recherche technique</span> (en utilisant les différentes connaissances et outils astrologiques que j'ai à ma disposition) que je complèterai par une <span class="u">approche plus intuitionnelle</span>. Je porterai une attention particulière à ce que vous soyez toujours positionné comme <strong>acteur de votre vie</strong>, en favorisant vos prises de conscience et votre libre arbitre.</p>
        <p>Il est à noter que <strong>je ne suis pas devin</strong>, et que plus vous m'en direz sur vous, mieux je pourrai vous accompagner&nbsp;!</p>
      </div>
    </div>

    <div class="block">
      <h2 class="sous-titre" id="ta-deroule">Comment se déroule le thème astral</h2>
      <div class="body">
        <ol>
          <li><span class="u">Un premier entretien de 15 minutes</span> pour me dire ce que vous attendez du thème.</li>
          <li>L'étude de votre thème avant de vous rencontrer.</li>
          <li>Un <span class="u">deuxième entretien d'1 heure 30</span> pour vous restituer votre thème.</li>
          <li><span class="u">Un enregistrement de la séance</span> vous sera envoyé.</li>
        </ol>
        <p>Pour préparer votre thème, j'ai besoin de votre <strong>date, heure et lieu de naissance</strong>.</p>
      </div>
    </div>

    <div class="block">
      <h2 class="sous-titre" id="ta-tarifs">Tarifs</h2>
      <div class="service-list" style="border-top:1px solid var(--line); margin-top:24px;">
        <div class="service no-icon"><div class="service-inner">
          <h3 style="display:flex; align-items:baseline; gap:14px; flex-wrap:wrap;">Thème astral <span class="price" style="margin-top:0;">150 €</span></h3>
        </div></div>
        <div class="service no-icon"><div class="service-inner">
          <h3 style="display:flex; align-items:baseline; gap:14px; flex-wrap:wrap;">Version approfondie <span class="price" style="margin-top:0;">250 €</span></h3>
          <p>En plus de la prestation à 150 €&nbsp;: étude plus approfondie des blessures et, si besoin, proposition de <a class="xl" href="/energetique/">soins énergétiques</a> et/ou <a class="xl" href="/hypnose/">hypnose</a> pour un accompagnement.</p>
        </div></div>
        <div class="service no-icon"><div class="service-inner">
          <h3 style="display:flex; align-items:baseline; gap:14px; flex-wrap:wrap;">La séance <span class="price" style="margin-top:0;">90 €</span></h3>
          <p>Il est possible d'avoir des entretiens (durée environ 1h30) pour des questions spécifiques ou pour faire un point, mais je réserve ces séances à des personnes qui ont déjà réalisé leur thème astral avec moi, de manière à pouvoir travailler sur des bases solides et en profondeur.</p>
        </div></div>
      </div>
      <p style="margin-top:18px; font-size:15px;">🎁 Envie de l'offrir&nbsp;? <a class="xl" href="/carte-cadeau/">Découvrez la carte cadeau</a>, à acheter en ligne.</p>
    </div>

    <div class="block">
      <h2 class="sous-titre" id="ta-lieu">Au cabinet à Orléans ou à distance</h2>
      <div class="body">
        <p>Je vous reçois dans mon <a class="xl" href="/cabinet/">cabinet</a>, au 24 rue du Clos Rozé, 45100 Orléans, près du Jardin des Plantes. Le thème astral peut aussi se faire à distance, en <strong>visioconférence ou par téléphone</strong>. Les tarifs sont les mêmes qu'en présentiel.</p>
      </div>
    </div>

    <div class="block">
      <h2 class="sous-titre" id="ta-questions">Vos questions</h2>
      <div class="faq">
%(faq)s
      </div>
    </div>

    <div class="block">
      <div class="body">
        <p style="font-size:17px;">Pour prendre rendez-vous&nbsp;: <a class="xl" href="tel:+33687035649">06 87 03 56 49</a>, ou depuis la <a class="xl" href="/contact/">page de contact</a>.</p>
      </div>
    </div>

    <nav class="next-steps" aria-label="Pour aller plus loin"><span class="ns-label">Pour aller plus loin</span><div class="ns-row"><a class="ns-link" href="/astrologie/">L'astrologie humaniste →</a><a class="ns-link" href="/avis/">Les avis clients →</a><a class="ns-link" href="/formation-astrologie/">Formation en astrologie →</a><a class="btn btn-primary" href="/contact/">Prendre rendez-vous</a></div></nav>
  </div>
</section>
''' % {'faq': faq_html()}

src = open('astrologie/index.html', encoding='utf-8').read()

# en-tête : titre, description, adresse
canon_old = SITE + '/astrologie/'
t_old = re.search(r'<title>(.*?)</title>', src).group(1)
d_old = re.search(r'<meta name="description" content="(.*?)">', src).group(1)
h = src.replace(t_old, TITLE).replace(d_old, DESC)
h = h.replace('<link rel="canonical" href="%s">' % canon_old, '<link rel="canonical" href="%s%s">' % (SITE, URL))
h = h.replace('<meta property="og:url" content="%s">' % canon_old, '<meta property="og:url" content="%s%s">' % (SITE, URL))
assert TITLE in h and (SITE + URL) in h

# données structurées : on garde ProfessionalService, on remplace le reste
blocks = re.findall(r'<script type="application/ld\+json">\s*\{.*?\}\s*</script>\n?', h, re.S)
keep = [b for b in blocks if '"ProfessionalService"' in b]
assert len(keep) == 1
for b in blocks:
    h = h.replace(b, '', 1)
service = {"@context": "https://schema.org", "@type": "Service", "name": "Analyse de thème astral",
           "serviceType": "Consultation d'astrologie", "areaServed": "Orléans",
           "provider": {"@type": "ProfessionalService", "name": "Lilian Gitton", "url": SITE + "/"},
           "url": SITE + URL,
           "offers": [{"@type": "Offer", "name": "Thème astral", "price": "150", "priceCurrency": "EUR"},
                      {"@type": "Offer", "name": "Thème astral, version approfondie", "price": "250", "priceCurrency": "EUR"},
                      {"@type": "Offer", "name": "Séance de suivi", "price": "90", "priceCurrency": "EUR"}]}
faqld = {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE + "/"},
    {"@type": "ListItem", "position": 2, "name": "Astrologie", "item": SITE + "/astrologie/"},
    {"@type": "ListItem", "position": 3, "name": "Thème astral", "item": SITE + URL}]}
ld = keep[0] + ''.join('<script type="application/ld+json">\n%s\n</script>\n' % json.dumps(x, ensure_ascii=False, indent=2)
                       for x in (service, faqld, crumbs))
h = h.replace('</head>', ld + '</head>', 1)

# contenu
sec = re.search(r'<section class="tab-active" id="astrologie">.*?</section>\n', h, re.S)
assert sec
h = h.replace(sec.group(0), CONTENT, 1)
# la roue astrologique n'existe pas sur cette page : on retire son script
h = re.sub(r'<script>\n(?:(?!</script>).)*astroWheel(?:(?!</script>).)*</script>\n?', '', h, flags=re.S)
assert 'astroWheel' not in h
# le bouton « Partager ces prestations » appartient à la page astrologie
assert 'partage-tarifs' not in h

os.makedirs('theme-astral', exist_ok=True)
open('theme-astral/index.html', 'w', encoding='utf-8').write(h)
print('theme-astral/index.html', len(h.encode()), 'octets')
