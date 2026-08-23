# Immeuble R+8 — façade principale

Dossier de conception d'une façade, de l'esquisse au carnet de détails.
**État : en pause, prêt à reprendre.** Tout ce qui suit est arrêté avec le
client sauf la section « Reste à trancher ».

- Branche : `claude/modern-facade-design-75kmrf`
- Canvas publié : https://claude.ai/code/artifact/82ec51bf-f512-45b1-976a-8cdb1f72d38a
- Livrable client : `KASSI/` (16 planches PDF à l'échelle vraie + 18 PNG)

---

## 1. Le projet en une page

Immeuble de logements en Algérie, R+8 sur un socle de parking.
La façade fait 17,50 m et se lit en deux blocs séparés par une fente
centrale. Chaque bloc porte un balcon dont la rive n'est pas droite : elle
part du poteau perpendiculairement au nu, creuse un grand lobe, revient,
creuse un petit lobe, et rejoint le second poteau. C'est **l'onde**, et
c'est le sujet du projet.

| | |
|---|---|
| Largeur totale | 17,50 m |
| Poteaux | 0,55 m (4, aux extrémités et de part et d'autre de la fente) |
| Baie de balcon | 6,75 m libre (× 2) |
| Fente centrale | 1,80 m, creusée de 1,50 m |
| Hauteur d'étage | 3,26 m (dalle 0,20 + 3,06 sous plafond) |
| RDC | 2,60 m sous plafond |
| Socle parking | RDC + R+1, en avancée de 4,00 m sur le nu |
| Terrasses | R+2, sur la toiture du parking |
| Balcons ondulés | R+3 à R+8, soit 6 niveaux × 2 blocs = 12 balcons |
| Acrotère | + 29,88 |

Altitudes : `0 / 2,80 / 6,06 / 9,32 / 12,58 / 15,84 / 19,10 / 22,36 / 25,62 / 28,88 / 29,88`

---

## 2. L'onde de rive — arrêtée le 23.08

Relevée sur le croquis du client, puis corrigée deux fois sur ses
annotations. Abscisse locale mesurée depuis le poteau, bloc droit ; **le
bloc gauche en est le miroir exact**.

| Abscisse | Profondeur | |
|---|---|---|
| 0,00 | 0,00 | naissance sur le poteau |
| 1,96 | **1,80** | grand lobe |
| 3,92 | **0,79** | creux médian, entre les deux portes |
| 5,64 | **1,10** | petit lobe |
| 7,85 | 0,00 | retour sur le second poteau |

**Développé 9,63 ml par balcon**, 12 balcons.

Le point qui a demandé trois tours : la rive **quitte le poteau
perpendiculairement au nu**, comme un demi-cercle qui prend appui sur la
façade — elle ne s'en écarte pas doucement. D'où le raccord retenu :
- portées d'extrémité → **quart d'ellipse** (tangente perpendiculaire au nu,
  tangente horizontale au sommet du lobe)
- portées intérieures → **raccord en cosinus** (fonds de lobe et creux plats)

C'est `ondeAt()` dans `geo.mjs`. Rayon minimal rencontré : **0,77 m**, à la
crête et au creux.

---

## 3. Le vide central — arrêté le 23.08

Ce n'est pas un panneau de brise-vue tendu en façade. C'est une **fente de
1,80 m creusée de 1,50 m**, et au fond deux petits balcons côte à côte, un
par logement, avec le brise-vue **entre eux**.

| | |
|---|---|
| Balcon | 0,70 × 0,80 m, un par logement |
| Brise-vue | **40 cm** de large, sur l'axe (x = 8,75), du refend de fond au garde-corps, du R+2 à la toiture |
| Porte-fenêtre | 0,70 m, **au fond de la fente, depuis le logement** |
| Garde-corps | verre feuilleté, à **0,70 m en arrière du nu** |

La fente reste donc ouverte sur 0,70 m devant les balcons : c'est ce qui
fait le « vide » de la façade.

Au R+2 la bande centrale n'est pas un balcon mais le vide qui sépare les
deux terrasses ; les balcons de la fente commencent au R+3.

---

## 4. Le garde-corps — arrêté le 23.08

**40 cm de verre feuilleté 8.8.4, puis 40 cm de barreaudage inox Ø 16, en
alternance sur tout le développé.** 24 panneaux par balcon, 12 de chaque,
4,82 ml de chacun. Main courante inox Ø 42 continue à 1,10 m.
Pas ajusté au centimètre près pour tomber juste sur les deux poteaux.

**Point ouvert honnête, chiffré sur la planche G3** : un panneau plat de
40 cm posé sur un rayon de 0,77 m s'écarte de la courbe théorique de
**23 mm** au plus défavorable (5 à 10 mm partout ailleurs), et la rotation
d'un panneau au suivant atteint **19°** — il faut des pinces à rotule, pas
des pinces droites. La parade est chiffrée : passer à 20 cm dans les deux
zones serrées ramène la flèche à 6 mm et la rotation à 9°.
**Le client a vu le chiffre, il n'a pas encore tranché.**

---

## 5. Matériaux

| | |
|---|---|
| Façade | monocouche **blanc**, grain fin gratté, joint creux 15 × 15 à chaque plancher |
| Bandeaux de rive | Aquapanel Outdoor 12,5 mm sur ossature cintrée, retombée 0,45 m, habillage 0,20 m au nu de la dalle |
| Éclairage | gorge LED 50 × 50 en sous-face de chaque bandeau, 3000 K IP65 + profil vertical 60 × 40 dans le trumeau, h 1,90 m |
| Menuiseries | aluminium **TPR série 65** à rupture de pont thermique, **RAL 7024**, double vitrage 4/16/4 |
| Porte-balcon | 1,80 × 2,20 m, 2 vantaux coulissants, 2 par balcon |
| Brise-vue et couvertines | aluminium **RAL 7024** |
| Garde-corps | verre feuilleté teinté noir + inox 316 brossé |
| Ventilation parking | bande de 0,80 m de lames alu horizontales au R+1 |

---

## 6. Reste à trancher

1. **La question de fond, jamais tranchée.** Les « 7 m » de baie donnés au
   départ : est-ce l'**entraxe des poteaux** (retenu — donne 6,75 libre et
   17,50 au total, tout le dossier est calé dessus) ou la **largeur
   libre** (la façade passerait alors à 18,00 m et tout se décale) ?
2. Le garde-corps : on reste à 40/40 partout, ou 20 cm dans les deux zones
   serrées ? (voir § 4)
3. Le garde-corps des balcons de la fente : à 0,70 m en arrière du nu comme
   dessiné, ou aligné sur la façade ? Si aligné, le creusement passe de
   1,50 à 0,80 m — une seule cote à changer.

---

## 7. Comment c'est fait

Tout est généré. Aucun dessin n'est saisi à la main : on change une valeur
dans `geo.mjs` et les 20 planches se refont.

```
geo.mjs        LA SOURCE DE VÉRITÉ. Toute la géométrie, l'onde, la
               segmentation du garde-corps, le vide central. Rien d'autre
               ne définit une cote.
elevation.mjs  l'élévation paramétrique + la palette
camera.mjs     caméra photo à décentrement + modèle d'éclairement (soleil,
               ciel, rebond) + ombres portées sur façade et sur sol
perspective.mjs perspective 3 points des contre-plongées
detailkit.mjs  trames du carnet de détails (béton, brique, isolant…)
svgkit.mjs     cotes, repères de niveau, textes
page.mjs       gabarit de planche commun
preview.mjs    sort un .dc.html en HTML simple, pour les captures

build-*.mjs    une planche chacun
export-kassi.mjs  sort le dossier client KASSI/ (PDF échelle vraie + PNG)
```

Refaire tout le dossier :

```bash
cd design/facade-r6
for f in build-*.mjs; do node "$f"; done
node build-photo.mjs && node build-photo.mjs --nuit
SP=/tmp node export-kassi.mjs        # regénère KASSI/
```

Republier le canvas (20 artboards) :

```bash
S=<skill design>/design
node $S/seed-canvas.mjs --template $S/payload.template.html \
  --out facade-immeuble-r6.html --title "Façade immeuble R+6 — dossier technique" \
  --canvas canvas.json $(for f in *.dc.html; do printf -- "--artboard %s " "$f"; done)
```
puis publier `facade-immeuble-r6.html` sur l'URL du canvas ci-dessus
(contract `0.1.31`, capabilities `{self:{}, downloads:{}}`, favicon 🏗️).

Captures : Chromium headless, `--force-device-scale-factor=2`.
PDF à l'échelle vraie : `@page { size: <L>mm <H>mm; margin: 0 }` avec
L = largeur_px / 96 × 25,4. **Imprimer à 100 %, jamais « ajuster à la
page »**, sinon les cotes sont fausses.

---

## 8. Les 20 planches

**Dossier technique** — Synthèse (données à valider) · Façade principale
1:100 · Plan niveau courant (onde) 1:50 · Plan terrasses R+2 · Plan RDC
parking · Coupe A-A · Détail balcon 4 vues 1:25 · Détails coupes verticales
1:10 · Détails coupes horizontales 1:10 · Détail garde-corps 1:20 et 1:5 ·
Matériaux · 2 gabarits

**Ambiances** — Contre-plongée jour · Contre-plongée nuit · Vue plongeante
entre terrasse et balcon · Perspective rue jour · Perspective rue nuit

**Variantes écartées** — B « Graphite & Verre » · C « Rubans continus »

---

## 9. Historique des corrections du client

Utile pour ne pas refaire les mêmes erreurs en reprenant :

- la première contre-plongée a été jugée **déformée** → d'où la caméra à
  décentrement, qui garde les verticales verticales
- l'onde a été inversée une fois dans la vue de dessus (pour une surface au
  dessus de l'œil, le plus proche est le plus **bas** dans le cadre)
- « قطر 1,1 / 1,8 » a d'abord été lu comme des **diamètres** de demi-cercles :
  ce sont des **profondeurs**
- une élévation orthogonale **ne peut pas** montrer une courbe qui se
  développe en plan → la courbe s'y lit à l'ombre portée proportionnelle à
  la profondeur, plus un trait pointillé qui trace le plan
- la façade passait par les jetons de thème du canvas et sortait crème :
  le monocouche blanc et le RAL 7024 sont maintenant figés dans les planches

---

*Reprise : lire ce fichier, puis `geo.mjs`. Tout le reste en découle.*
