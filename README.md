# liliangitton.github.io

Site de Lilian Gitton (liliangitton.fr), hébergé sur GitHub Pages.

## Organisation

- `_src/source.html` : **la source du site** (version « une seule page » avec tous les contenus). C'est ce fichier qu'on modifie pour changer un texte.
- `_src/build.py` : génère les pages du site à partir de la source. Lancer `python3 _src/build.py` à la racine du dépôt.
- Fichiers générés (ne pas les modifier à la main, ils sont réécrits à chaque génération) : `index.html`, un dossier par page (`astrologie/`, `formation-astrologie/`, `hypnose/`, `energetique/`, `qui-suis-je/`, `avis/`, `cabinet/`, `contact/`, `articles-videos/`, `mentions-legales/`, `cgv/`), `404.html`, `sitemap.xml`, `robots.txt`, `assets/`, `img/`.
- `_src/partage.py` : ajoute les boutons « Partager » aux pages (lancé automatiquement à la fin de `build.py`, ou seul : `python3 _src/partage.py .`).
- `_src/theme-astral.py` : crée la page `theme-astral/` à partir de la page `astrologie/`.
- **Attention** : depuis le 5 nov. 2026, certaines pages générées ont été modifiées directement (mots-clés hypnose, énergétique, astrologie ; page Thème astral ; entrée de menu). Ne pas relancer `build.py` sans reporter d'abord ces changements dans la source, sinon ils seraient effacés.
- `quiz/` : le quiz d'astrologie (page indépendante).
