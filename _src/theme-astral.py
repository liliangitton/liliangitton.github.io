"""Crée la page /theme-astral/ à partir de la page /astrologie/ (même en-tête, menu, pied de page).
Lancer à la racine du dépôt : python3 _src/theme-astral.py"""
import re, json, os

SITE = 'https://liliangitton.fr'
URL = '/theme-astral/'
TITLE = 'Thème astral à Orléans : consultation, déroulé et tarif'
DESC = ("Faire son thème astral à Orléans ou en visio avec Lilian Gitton, astrologue humaniste : "
        "ce qu'il apporte, déroulé de la consultation, tarifs (150 €, version approfondie 250 €).")

FAQ = [
    ("Allez-vous me prédire mon avenir ?",
     "Non, je ne prédis pas l'avenir. L'astrologie humaniste sert à mieux vous comprendre, à voir vos ressources et vos défis, "
     "et à donner du sens à ce que vous vivez. Les décisions restent les vôtres. Plus vous me parlez de vous, plus l'analyse est juste."),
    ("Dois-je préparer quelque chose ?",
     "Rien de compliqué : avant notre court échange téléphonique, demandez-vous simplement ce que vous en attendez. "
     "Une ou deux questions qui vous tiennent à cœur suffisent, elles me serviront de fil conducteur."),
    ("Combien de temps dure la consultation ?",
     "Comptez 15 minutes pour le premier échange, puis environ 1 h 30 pour la séance. L'enregistrement vous est envoyé ensuite."),
    ("Peut-on faire son thème astral à distance ?",
     "Oui, en visio ou par téléphone, où que vous viviez, au même tarif qu'au cabinet."),
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
      <p>Votre <strong>thème astral</strong>, c'est la carte du ciel au moment exact de votre naissance. Bien lu, il devient un miroir&nbsp;: il éclaire vos forces, vos fragilités et le chemin qui vous ressemble. Je vous propose de le découvrir ensemble, lors d'une <strong>consultation dans mon cabinet à Orléans</strong>, ou à distance.</p>
      <p class="astro-cta" style="margin-top:14px; font-size:16px;"><a class="xl" href="#ta-tarifs">Voir les tarifs&nbsp;→</a></p>
    </div>

    <div class="block">
      <h2 class="sous-titre" id="ta-apport">Ce que votre thème astral peut vous apporter</h2>
      <div class="body">
        <p>Je l'aborde avec l'<a class="xl" href="/astrologie/">astrologie humaniste</a>&nbsp;: il ne s'agit pas de prédire, mais de mieux vous connaître. Au fil de la consultation, vous découvrez&nbsp;:</p>
        <ul>
          <li>les <strong>talents et ressources</strong> sur lesquels vous appuyer&nbsp;;</li>
          <li>les <strong>difficultés qui reviennent</strong>, et la façon de les dépasser&nbsp;;</li>
          <li>un regard neuf sur votre histoire&nbsp;: ce que vous avez vécu prend du sens&nbsp;;</li>
          <li>les grandes <strong>périodes de votre vie</strong>, et les cycles qui s'annoncent&nbsp;;</li>
          <li>un lien plus profond avec votre être intérieur, votre Soi.</li>
        </ul>
      </div>
    </div>

    <div class="block">
      <h2 class="sous-titre" id="ta-deroule">Comment se déroule la consultation</h2>
      <div class="body">
        <ol>
          <li><strong>Un échange de 15 minutes par téléphone.</strong> Vous me dites ce qui vous amène et ce que vous espérez. Souvent, une ou deux questions essentielles se dégagent&nbsp;: elles guideront mon travail.</li>
          <li><strong>Je prépare votre thème en amont.</strong> D'abord une analyse technique avec les outils de l'astrologie, puis une lecture plus intuitive.</li>
          <li><strong>Nous nous retrouvons 1 h 30</strong> pour en parler ensemble, au cabinet ou à distance.</li>
          <li><strong>Vous recevez l'enregistrement</strong> de la séance, pour le réécouter à votre rythme.</li>
        </ol>
        <p>Mon intention&nbsp;: que vous repartiez <span class="u">acteur de votre vie</span>, avec vos propres prises de conscience. Vos choix vous appartiennent.</p>
        <p>À me transmettre avant la consultation&nbsp;: votre <strong>date, heure et lieu de naissance</strong>.</p>
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
            <p>La consultation complète, avec un regard plus poussé sur les blessures. Si cela peut vous aider, je vous propose ensuite des <a class="xl" href="/energetique/">soins énergétiques</a> ou de l'<a class="xl" href="/hypnose/">hypnose</a>.</p>
          </div>
        </div>
        <div class="service no-icon">
          <div class="service-inner">
            <h3 style="display:flex; align-items:baseline; gap:14px; flex-wrap:wrap;">Séance de suivi <span class="price" style="margin-top:0;">90 €</span></h3>
            <p>Environ 1 h 30 pour approfondir une question ou faire le point. Elle est réservée aux personnes dont j'ai déjà étudié le thème&nbsp;: on part ainsi sur des bases solides.</p>
          </div>
        </div>
      </div>
      <p style="margin-top:18px; font-size:15px;">🎁 Un thème astral, c'est aussi une belle idée de cadeau&nbsp;: <a class="xl" href="/carte-cadeau/">offrir une carte cadeau</a>.</p>
    </div>

    <div class="block">
      <h2 class="sous-titre" id="ta-lieu">En cabinet à Orléans ou à distance</h2>
      <div class="body">
        <p>Je vous reçois dans mon <a class="xl" href="/cabinet/">cabinet</a>, au 24 rue du Clos Rozé, 45100 Orléans, près du Jardin des Plantes.</p>
        <p>Vous habitez loin&nbsp;? La consultation se fait aussi <strong>en visio ou par téléphone</strong>, au même tarif.</p>
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
