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
| `build-*.mjs` | Un script par planche |
| `*.dc.html` | Planches générées (artboards du canvas) |
| `canvas.json` | Mise en page du canvas, pages et notes |
| `preview.mjs` | Sort une planche en HTML simple pour contrôle local |

## Regénérer

```sh
node build-main.mjs && node build-vue.mjs && node build-coupe.mjs \
  && node build-plan.mjs && node build-materiaux.mjs && node build-variantes.mjs
```

Puis re-seeder le canvas avec `seed-canvas.mjs` de la skill `design`.
