#!/usr/bin/env python3
"""Génère une carte cadeau Lilian Gitton en PDF (format A5 paysage).

Exemple :
  python3 _src/carte-cadeau/generer.py --pour "Marie Dupont" --prestation theme \
      --de "Jean Martin" --numero 2026-001 --date 2026-11-04 --sortie carte.pdf

Prestations : theme, approfondi, hypnose, energie, ou un texte libre
(ex. --prestation "Carte cadeau d'une valeur de 80 €").
"""
import argparse, base64, datetime, html, os, sys

ICI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(ICI, '..', '..'))

PRESTATIONS = {
    'theme': ("Une analyse de thème astral",
              "Entretien préalable de 15 minutes, étude du thème, puis séance d'1 h 30 avec enregistrement."),
    'approfondi': ("Une analyse de thème astral approfondie",
                   "Le thème astral complet, avec une étude approfondie des blessures et un accompagnement adapté."),
    'hypnose': ("Une séance d'hypnose humaniste",
                "Au cabinet à Orléans ou en visioconférence."),
    'energie': ("Un soin énergétique",
                "Rééquilibrage énergétique, au cabinet à Orléans ou à distance."),
}
MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août',
        'septembre', 'octobre', 'novembre', 'décembre']


def date_fr(d):
    return '%d%s %s %d' % (d.day, 'er' if d.day == 1 else '', MOIS[d.month - 1], d.year)


def un_an_apres(d):
    try:
        return d.replace(year=d.year + 1)
    except ValueError:  # 29 février
        return d.replace(year=d.year + 1, day=28)


def b64(path):
    return base64.b64encode(open(path, 'rb').read()).decode()


def fabriquer_html(pour, prestation, de, numero, achat):
    titre, detail = PRESTATIONS.get(prestation, (prestation, ''))
    fin = un_an_apres(achat)
    e = html.escape
    de_html = '<div class="de">De la part de <strong>%s</strong></div>' % e(de) if de else ''
    detail_html = '<div class="detail">%s</div>' % e(detail) if detail else ''
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<style>
@font-face{{font-family:'Fraunces';src:url(data:font/woff2;base64,{b64(SITE + '/fonts/fraunces-roman.woff2')}) format('woff2');}}
@font-face{{font-family:'Fraunces';font-style:italic;src:url(data:font/woff2;base64,{b64(SITE + '/fonts/fraunces-italic.woff2')}) format('woff2');}}
@font-face{{font-family:'Sora';src:url(data:font/woff2;base64,{b64(SITE + '/fonts/sora.woff2')}) format('woff2');}}
@page{{size:210mm 148mm;margin:0;}}
*{{box-sizing:border-box;}}
html,body{{margin:0;width:210mm;height:148mm;}}
body{{font-family:'Sora',sans-serif;color:#EFE7D8;-webkit-print-color-adjust:exact;print-color-adjust:exact;
  background:radial-gradient(ellipse at 20% 0%,#3b2a52 0%,#241a33 45%,#18131C 100%);position:relative;overflow:hidden;}}
.etoiles{{position:absolute;inset:0;}}
.etoiles i{{position:absolute;width:2px;height:2px;border-radius:50%;background:#EFE7D8;opacity:.55;}}
.cadre{{position:absolute;inset:7mm;border:0.4mm solid rgba(221,174,94,.75);border-radius:3mm;}}
.cadre2{{position:absolute;inset:9mm;border:0.2mm solid rgba(221,174,94,.35);border-radius:2mm;}}
.logo{{position:absolute;right:14mm;top:13mm;width:30mm;opacity:.5;filter:invert(1);}}
.contenu{{position:absolute;left:18mm;right:18mm;top:15mm;bottom:15mm;display:flex;flex-direction:column;}}
.kicker{{font-size:8.5pt;letter-spacing:.32em;text-transform:uppercase;color:#DDAE5E;}}
h1{{font-family:'Fraunces',serif;font-style:italic;font-weight:400;font-size:34pt;line-height:1;margin:3mm 0 0;color:#DDAE5E;}}
.pour{{margin-top:9mm;font-size:10pt;color:#B7ABC4;}}
.nom{{font-family:'Fraunces',serif;font-size:24pt;line-height:1.15;margin-top:1mm;}}
.de{{font-size:10pt;color:#B7ABC4;margin-top:2mm;}}
.de strong{{color:#EFE7D8;font-weight:400;}}
.presta{{margin-top:7mm;font-family:'Fraunces',serif;font-size:15pt;}}
.detail{{font-size:9pt;color:#B7ABC4;margin-top:1.5mm;max-width:150mm;}}
.voeu{{margin-top:auto;font-family:'Fraunces',serif;font-style:italic;font-size:12pt;color:#DDAE5E;margin-bottom:5mm;}}
.bas{{display:flex;justify-content:space-between;align-items:flex-end;gap:8mm;
  border-top:0.2mm solid rgba(239,231,216,.2);padding-top:3.5mm;font-size:8.5pt;color:#B7ABC4;line-height:1.55;}}
.bas strong{{color:#EFE7D8;font-weight:400;}}
.droite{{text-align:right;}}
</style></head><body>
<div class="etoiles">{''.join('<i style="left:%dmm;top:%dmm;opacity:%.2f"></i>' % (x, y, o) for x, y, o in [(30,22,.6),(64,11,.4),(102,28,.7),(140,16,.5),(176,40,.4),(188,96,.6),(150,124,.35),(58,132,.5),(18,88,.45),(120,72,.3),(84,58,.25),(196,120,.5)])}</div>
<div class="cadre"></div><div class="cadre2"></div>
<img class="logo" src="data:image/png;base64,{b64(SITE + '/img/header-watermark.png')}" alt="">
<div class="contenu">
  <div class="kicker">Lilian Gitton · Orléans</div>
  <h1>Carte cadeau</h1>
  <div class="pour">Offerte à</div>
  <div class="nom">{e(pour)}</div>
  {de_html}
  <div class="presta">{e(titre)}</div>
  {detail_html}
  <div class="voeu">Un moment pour soi, pour mieux se connaître et avancer sur son chemin.</div>
  <div class="bas">
    <div>Pour prendre rendez-vous&nbsp;: <strong>06 87 03 56 49</strong><br>
      liliangitton.fr · 24 rue du Clos Rozé, 45100 Orléans</div>
    <div class="droite">Carte n° <strong>{e(numero)}</strong><br>
      Valable jusqu'au <strong>{date_fr(fin)}</strong></div>
  </div>
</div>
</body></html>"""


def main():
    a = argparse.ArgumentParser()
    a.add_argument('--pour', required=True)
    a.add_argument('--prestation', required=True)
    a.add_argument('--de', default='')
    a.add_argument('--numero', required=True)
    a.add_argument('--date', default=datetime.date.today().isoformat(), help="date d'achat AAAA-MM-JJ")
    a.add_argument('--sortie', required=True, help='fichier PDF à créer')
    a.add_argument('--image', help='crée aussi une image PNG (aperçu)')
    o = a.parse_args()
    page = fabriquer_html(o.pour, o.prestation, o.de, o.numero, datetime.date.fromisoformat(o.date))
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 794, 'height': 559}, device_scale_factor=2)
        pg.set_content(page, wait_until='load')
        pg.evaluate('document.fonts.ready')
        pg.pdf(path=o.sortie, width='210mm', height='148mm', print_background=True)
        if o.image:
            pg.screenshot(path=o.image)
        b.close()
    print('Carte créée :', o.sortie)


if __name__ == '__main__':
    sys.exit(main())
