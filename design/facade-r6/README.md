# Façade immeuble R+6 — dossier de conception

Planches de façade générées pour un immeuble de logements R+6 (Algérie),
publiées sur un canvas Claude Design.

## Relevé de départ (client)

| Donnée | Valeur |
| --- | --- |
| Largeur totale de façade | 17,50 m |
| Poteau | 0,55 m |
| Ouverture de balcon | ~7,00 m (×2) |
| Vide central | ~1,80 m |
| Avancée parking RDC + R+1 | 4,00 m |
| Porte-balcon aluminium | 1,80 m (×2 par balcon) |
| Développé des courbes de rive | ~10 ml par balcon |

Matériaux imposés : monocouche, garde-corps verre + inox, brise-vue
aluminium, Aquapanel sur les rives cintrées.

## Découpage retenu

`0,55 + 6,75 + 0,55 + 1,80 + 0,55 + 6,75 + 0,55 = 17,50 m`

L'ouverture libre est prise à 6,75 m (entraxe de poteaux 7,30 m) pour
boucler exactement les 17,50 m relevés.

## Fichiers

| Fichier | Rôle |
| --- | --- |
| `geo.mjs` | Géométrie partagée : cotes, niveaux, onde de rive, développé |
| `svgkit.mjs` | Primitives de dessin technique (cotes, niveaux, renvois) |
| `perspective.mjs` | Projection perspective à trois points des vues d'ambiance |
| `page.mjs` | Gabarit commun des planches (typographie, bandeau de titre) |
| `elevation.mjs` | Générateur d'élévation, paramétré par palette |
| `build-*.mjs` | Un script par planche (`build-vue.mjs` sort le jour et la nuit) |
| `*.dc.html` | Planches générées (artboards du canvas) |
| `canvas.json` | Mise en page du canvas, pages et notes |
| `preview.mjs` | Sort une planche en HTML simple pour contrôle local |
| `renders/` | Vues d'ambiance en PNG et gabarits en PNG + PDF A3 |

## Parti retenu

- **Garde-corps mixte inox / verre**, tracé sur l'onde : aux creux et aux crêtes
  le rayon de rive tombe à 0,35 m, le verre ne s'y cintre pas — 5 sections de
  barreaudage inox Ø 16 par bloc (3,50 m) ; sur les portions quasi droites,
  4 panneaux de verre feuilleté 8.8.4 plats de 1,09 m (4,35 m).
  La découpe est calculée par `gcSegments()` dans `geo.mjs`.
- **Deux terrasses au R+2**, une par logement : 7,85 m chacune sur 4,00 m de
  profondeur, séparées par le vide central de 1,80 m laissé ouvert dans la
  dalle de toiture du parking.
- **Éclairage** : gorge LED de 5 cm en sous-face de chaque rive cintrée
  (≈ 99 ml), rampe verticale derrière les lames du vide central, bandeau
  lumineux au-dessus de l'entrée.

## Vues d'ambiance

Les vues jour et nuit sont construites sur une vraie projection à trois points
(`perspective.mjs`) : caméra à 30 m du nu de façade, œil à 1,60 m, basculée de
32° vers le haut. Chaque point est projeté depuis ses coordonnées réelles
(X, distance caméra, altitude), la rive de balcon comprise — c'est ce qui donne
son relief à l'onde : la crête, plus proche, monte dans l'image et découvre sa
sous-face, le creux redescend. Les horizontales restent horizontales et les
verticales convergent vers un point de fuite unique.

## Gabarits à dessiner

`build-gabarits.mjs` sort deux planches A3 paysage à l'échelle 1:50 (96 px/pouce,
un carreau de 0,25 m) destinées à être imprimées ou annotées à l'écran :

- **Gabarit-Onde** — niveau courant, la zone de balcon laissée vide avec le tracé
  actuel en repère léger, pour redessiner la rive.
- **Gabarit-Terrasse** — niveau R+2, la dalle du parking et le vide central
  posés comme limites dures, le reste libre.

Les PDF sont produits par Chromium (`--print-to-pdf` avec `@page { size: A3
landscape; margin: 0 }`) ; le conteneur est bridé à 1118 px de haut pour tenir
sur une seule page.

## Regénérer

```sh
for b in main vue coupe plan materiaux variantes gabarits; do node build-$b.mjs; done
```

Puis re-seeder le canvas avec `seed-canvas.mjs` de la skill `design`.
