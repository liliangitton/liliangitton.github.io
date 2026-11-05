"""Crée la page /theme-astral/ à partir de la page /astrologie/ (même en-tête, menu, pied de page).
Lancer à la racine du dépôt : python3 _src/theme-astral.py"""
import re, json, os

SITE = 'https://liliangitton.fr'
URL = '/theme-astral/'
TITLE = 'Thème astral à Orléans : consultation, déroulé et tarif'
DESC = ("Faire son thème astral à Orléans ou en visio avec Lilian Gitton, astrologue humaniste : "
        "ce qu'il apporte, déroulé de la consultation, tarifs (150 €, version approfondie 250 €).")

FAQ = [
    ("Faut-il croire en l'astrologie ? Êtes-vous devin ?",
     "Je ne suis pas devin. L'astrologie que je pratique est humaniste : elle ne cherche pas à prédire, mais à mieux "
     "se comprendre, à repérer ses potentiels et ses défis, et à mettre du sens à sa vie. Vous restez toujours acteur "
     "de votre vie, et plus vous m'en dites sur vous, mieux je peux vous accompagner."),
    ("Comment se préparer à un thème astral ?",
     "Nous en parlons d'abord ensemble lors d'un entretien téléphonique d'une quinzaine de minutes. Ce qu'il est utile "
     "de savoir, c'est ce que vous attendez de votre thème astral. Une ou deux questions centrales peuvent ressortir : "
     "je les étudierai comme fil conducteur de votre thème."),
    ("Combien de temps dure la consultation ?",
     "Un premier entretien de 15 minutes, puis la séance de restitution d'environ 1 h 30. "
     "Un enregistrement de la séance vous est ensuite envoyé."),
    ("Peut-on faire son thème astral à distance ?",
     "Oui, en visioconférence ou par téléphone, même si vous êtes à l'autre bout du monde. "
     "Les tarifs sont les mêmes qu'au cabinet."),
    ("Comment payer ?",
     "En espèces, par chèque, par carte ou par virement. Pour d'autres moyens de paiement, n'hésitez pas à me poser la question."),
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
      <p>Que vous traversiez une période de questionnements, un changement de vie, ou simplement l'envie de mieux vous connaître, <strong>votre thème astral est un point de départ</strong>. Astrologue à Orléans, je vous reçois pour l'<strong>analyse de votre thème astral</strong> au cabinet, ou à distance en visio ou par téléphone.</p>
      <p class="astro-cta" style="margin-top:14px; font-size:16px;"><a class="xl" href="#ta-tarifs">Voir les tarifs&nbsp;→</a></p>
    </div>

    <div class="block">
      <h2 class="sous-titre" id="ta-apport">Ce que votre thème astral peut vous apporter</h2>
      <div class="body">
        <p>Le thème astral, ou carte du ciel, est l'image du ciel au moment de votre naissance. Je l'analyse selon l'<a class="xl" href="/astrologie/">astrologie humaniste</a>&nbsp;: un outil de connaissance de soi, pas de prédiction. Il peut vous aider à&nbsp;:</p>
        <ul>
          <li>comprendre vos <strong>potentiels</strong>&nbsp;;</li>
          <li>mieux cerner vos <strong>défis</strong> pour les transcender&nbsp;;</li>
          <li>mettre du sens à votre vie, aux événements passés et présents&nbsp;;</li>
          <li>voir vos différents <strong>cycles à venir</strong>&nbsp;;</li>
          <li>et surtout vous rapprocher de votre Soi, de qui vous êtes en profondeur.</li>
        </ul>
      </div>
    </div>

    <div class="block">
      <h2 class="sous-titre" id="ta-deroule">Comment se déroule la consultation</h2>
      <div class="body">
        <ol>
          <li><strong>Un premier entretien de 15 minutes</strong>, par téléphone, pour me dire ce que vous attendez de votre thème. Une ou deux questions centrales peuvent ressortir&nbsp;: elles deviendront le fil conducteur de l'étude.</li>
          <li><strong>L'étude de votre thème avant de vous rencontrer.</strong> Je réalise un travail de recherche technique, avec les différents outils astrologiques à ma disposition, que je complète par une approche plus intuitive.</li>
          <li><strong>Un deuxième entretien d'1 h 30</strong> pour vous restituer votre thème, au cabinet ou à distance.</li>
          <li><strong>Un enregistrement de la séance</strong> vous est ensuite envoyé, pour y revenir quand vous le souhaitez.</li>
        </ol>
        <p>Tout au long de la consultation, je veille à ce que vous restiez <span class="u">acteur de votre vie</span>, en favorisant vos prises de conscience et votre libre arbitre.</p>
        <p>Pour préparer votre thème, j'ai besoin de votre <strong>date, heure et lieu de naissance</strong>.</p>
      </div>
    </div>

    <div class="block">
      <h2 class="sous-titre" id="ta-tarifs">Tarifs</h2>
      <div class="service-list" style="border-top:1px solid var(--line); margin-top:24px;">
        <div class="service no-icon">
          <div class="service-inner">
            <h3 style="display:flex; align-items:baseline; gap:14px; flex-wrap:wrap;">Thème astral <span class="price" style="margin-top:0;">150 €</span></h3>
            <p>Entretien préalable de 15 minutes, étude de votre thème, séance de restitution d'1 h 30 et enregistrement.</p>
          </div>
        </div>
        <div class="service no-icon">
          <div class="service-inner">
            <h3 style="display:flex; align-items:baseline; gap:14px; flex-wrap:wrap;">Version approfondie <span class="price" style="margin-top:0;">250 €</span></h3>
            <p>Tout le contenu du thème astral, avec en plus une étude plus approfondie des blessures et, si besoin, une proposition de <a class="xl" href="/energetique/">soins énergétiques</a> et/ou d'<a class="xl" href="/hypnose/">hypnose</a> pour un accompagnement.</p>
          </div>
        </div>
        <div class="service no-icon">
          <div class="service-inner">
            <h3 style="display:flex; align-items:baseline; gap:14px; flex-wrap:wrap;">Séance de suivi <span class="price" style="margin-top:0;">90 €</span></h3>
            <p>Un entretien d'environ 1 h 30 pour une question précise ou pour faire le point. Je la réserve aux personnes qui ont déjà réalisé leur thème astral avec moi, pour travailler sur des bases solides.</p>
          </div>
        </div>
      </div>
      <p style="margin-top:18px; font-size:15px;">🎁 Envie de l'offrir&nbsp;? <a class="xl" href="/carte-cadeau/">Découvrez la carte cadeau</a>, à acheter en ligne.</p>
    </div>

    <div class="block">
      <h2 class="sous-titre" id="ta-lieu">Au cabinet à Orléans ou à distance</h2>
      <div class="body">
        <p>Je vous reçois dans mon <a class="xl" href="/cabinet/">cabinet</a>, au 24 rue du Clos Rozé, 45100 Orléans, près du Jardin des Plantes.</p>
        <p>Votre thème astral peut aussi se faire <strong>à distance, en visioconférence ou par téléphone</strong>, où que vous soyez. Les tarifs sont les mêmes qu'au cabinet.</p>
      </div>
    </div>

    <div class="block">
      <h2 class="sous-titre" id="ta-questions">Vos questions sur le thème astral</h2>
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
