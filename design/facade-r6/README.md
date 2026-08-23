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
| `page.mjs` | Gabarit commun des planches (typographie, bandeau de titre) |
| `elevation.mjs` | Générateur d'élévation, paramétré par palette |
| `build-*.mjs` | Un script par planche (`build-vue.mjs` sort le jour et la nuit) |
| `*.dc.html` | Planches générées (artboards du canvas) |
| `canvas.json` | Mise en page du canvas, pages et notes |
| `preview.mjs` | Sort une planche en HTML simple pour contrôle local |
| `renders/` | Vues d'ambiance exportées en PNG (jour / nuit) |

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

## Regénérer

```sh
for b in main vue coupe plan materiaux variantes; do node build-$b.mjs; done
```

Puis re-seeder le canvas avec `seed-canvas.mjs` de la skill `design`.
