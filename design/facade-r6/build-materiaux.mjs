import { writeFileSync } from 'node:fs';
import { page, header } from './page.mjs';
import { developpe } from './geo.mjs';

const W = 940;
const dev = developpe();

const MAT = [
  { n: 'Monocouche gratté', t: 'Blanc', sw: ['#F4F2ED', '#E0DDD5'], ref: 'Enduit monocouche épaisseur 15 mm, finition grattée fin, sur maçonnerie et voiles béton',
    pts: ['Blanc sur l’ensemble des voiles, poteaux, allèges et acrotères',
          'Joint creux horizontal 15 × 15 mm au droit de chaque plancher',
          'Poteaux de 55 cm laissés en léger relief — nu extérieur +2 cm sur l’allège'] },
  { n: 'Aquapanel cintré', t: 'Blanc pur', sw: ['#FFFFFF', '#E3DCD0'], ref: 'Plaque ciment 12,5 mm cintrée sur ossature, enduit + peinture façade blanc mat',
    pts: [`Bandeaux de rive ondulés, développé ${dev.toFixed(2)} ml par balcon`,
          'Balcons R+3 à R+6 × 2 blocs = 8 rives → ' + (dev * 8).toFixed(0) + ' ml',
          'Acrotère de terrasse R+2, onde continue sur 17,50 m → 20 ml',
          'Soit ≈ 99 ml au total ; retombée 45 cm → ≈ ' + (99 * 0.45).toFixed(0) + ' m² développés, sous-face comprise',
          'Rayon de cintrage mini ≈ 0,60 m — compatible plaque cintrée à sec'] },
  { n: 'Garde-corps mixte inox + verre', t: 'Inox brossé / verre clair', sw: ['#B7BEC2', '#C3D0D2'], ref: 'Barreaudage inox 304 brossé Ø 16 mm et panneaux de verre feuilleté 8.8.4 plats, main courante inox Ø 42 mm continue',
    pts: ['Hauteur 1,10 m ; le tracé suit exactement l’onde de rive, à 10 cm en retrait du nu',
          'Pas de 40 cm : un panneau de verre feuilleté plat, puis 40 cm de barreaudage inox, en alternance',
          '24 panneaux par bloc — 12 de verre (4,82 ml) et 12 d’inox (4,82 ml) ; à 40 cm la flèche du plat reste invisible sur la courbe',
          'Barreaux espacés de 11 cm ; linéaire total ≈ 116 ml, même tracé que les bandeaux Aquapanel'] },
  { n: 'Brise-vue aluminium', t: 'RAL 7024 gris graphite', sw: ['#474B4E', '#31353A'], ref: 'Lames aluminium RAL 7024, même teinte que les menuiseries, ossature alu, fixation sur poteaux béton',
    pts: ['Vide central : le brise-vue est ENTRE les deux balcons, sur l’axe — 1,50 m de profondeur × 22,8 m de haut, du R+2 à la toiture (≈ 34 m²)',
          'Séparations d’intimité en bout de balcon, 1,30 m de haut',
          'Ventilation du parking R+1 — lames horizontales pare-vue (≈ 34 m²)'] },
  { n: 'Menuiseries aluminium', t: 'TPR série 65 · RAL 7024', sw: ['#474B4E', '#2C3234'], ref: 'Portes-balcon TPR série 65 à rupture de pont thermique, 2 vantaux coulissants, RAL 7024 gris graphite, double vitrage 4/16/4',
    pts: ['1,80 m de large × 2,20 m de haut',
          '2 par balcon × 2 blocs × 5 niveaux = 20 unités en façade principale',
          '+ 2 par niveau côté vide central = 10 unités',
          'Couvertine alu RAL 7024 en tête d’acrotère et de poteau'] },
  { n: 'Éclairage architectural', t: 'LED blanc chaud 3000 K', sw: ['#F2C46A', '#474B4E'], ref: 'Rubans LED IP65 en gorge aluminium, alimentation depuis les gaines de balcon, gradation par niveau',
    pts: ['Gorge de 5 cm en sous-face de chaque bandeau cintré : la lumière lèche la courbe et la dessine sur toute sa longueur — ≈ 99 ml',
          'Rampe verticale derrière les lames du vide central, du R+2 à la toiture — ≈ 15 ml, la faille devient la seule verticale lumineuse',
          'Bandeau lumineux au-dessus de l’entrée et des portes de garage — 17,50 ml',
          'Spots encastrés en sous-face de balcon pour l’usage courant, sur un circuit séparé de celui de la façade'] },
];

const NOTES = [
  ['Découpage horizontal', '0,55 + 6,75 + 0,55 + 1,80 + 0,55 + 6,75 + 0,55 = 17,50 m. L’ouverture libre est arrêtée à 6,75 m entre nus de poteaux, soit 7,30 m d’entraxe — c’est la lecture retenue des ~7,00 m relevés, et elle boucle exactement la largeur de 17,50 m.'],
  ['Niveaux et hauteurs', 'RDC + R+1 en parking, R+2 à R+6 en logements — cinq lignes ondulées en façade : l’acrotère de la terrasse R+2, puis les balcons du R+3 au R+6. Hauteurs sous plancher retenues : 3,40 m au RDC, 3,06 m à chaque étage, acrotère 1,00 m → 22,76 m hors tout.'],
  ['Onde de rive', 'Deux ondes par balcon, profondeur 1,30 m au creux et 3,00 m à la crête — c’est cette amplitude qui produit les 9,92 ml de développé, conformes aux ~10 ml relevés. Variante d’exécution si la console de 3,00 m pose problème au ferraillage : trois ondes moins creuses, à développé équivalent.'],
  ['Terrasses R+2', 'Une terrasse par logement : deux plateaux de 7,85 m sur 4,00 m de profondeur, séparés par le vide central de 1,80 m laissé ouvert dans la dalle de toiture du parking. Chaque acrotère reprend l’onde des balcons, au même pas.'],
];

const card = (m, wide) => `<div style="border: 1px solid #D3C9B7; background: #FBFAF7; padding: 20px 22px 22px${wide ? '; grid-column: span 2' : ''}">
  <div style="display: flex; gap: 14px; align-items: center">
    <div style="display: flex; gap: 0; flex: 0 0 auto">
      ${m.sw.map((c, i) => `<div style="width: 34px; height: 34px; background: ${c}; border: 1px solid rgba(35,33,30,.18); ${i ? 'margin-left: -1px' : ''}"></div>`).join('')}
    </div>
    <div>
      <div style="font-family: 'Space Grotesk', 'Helvetica Neue', Arial, sans-serif; font-size: 16px; font-weight: 600; letter-spacing: -0.012em">${m.n}</div>
      <div style="font-size: 11px; font-weight: 600; letter-spacing: .14em; color: #8C8478; text-transform: uppercase; margin-top: 3px">${m.t}</div>
    </div>
  </div>
  <div style="font-size: 12px; line-height: 1.55; color: #4C463C; margin-top: 14px; padding-top: 13px; border-top: 1px solid #E0D8C8; text-wrap: pretty">${m.ref}</div>
  <ul style="margin: 12px 0 0; padding-left: 16px; font-size: 12px; line-height: 1.6; color: #6E6659${wide ? '; columns: 2; column-gap: 34px' : ''}">
    ${m.pts.map((p) => `<li style="margin-top: 4px; text-wrap: pretty">${p}</li>`).join('')}
  </ul>
</div>`;

const body = `<div style="width: ${W}px; background: #FFFFFF">
${header({ w: W, kicker: 'Matériaux, finitions &amp; hypothèses', title: 'Palette de façade',
  sub: 'Les quatre matériaux demandés, leur mise en œuvre et les quantités qui en découlent — puis le parti dimensionnel arrêté, sur lequel s’appuient toutes les planches.',
  right: 'VARIANTE A — RETENUE<br>« BLANC &amp; GRAPHITE »<br>QUANTITÉS ESTIMATIVES' })}
<div style="padding: 28px 44px 8px; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px">
  ${MAT.map((m, i) => card(m, i === MAT.length - 1 && MAT.length % 2 === 1)).join('\n  ')}
</div>
<div style="padding: 26px 44px 44px">
  <div class="rule" style="margin-bottom: 22px"></div>
  <div class="eyebrow" style="margin-bottom: 16px">Parti dimensionnel arrêté — validé le 23.08.2026</div>
  <div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px 34px">
    ${NOTES.map(([t, d]) => `<div>
      <div style="font-family: 'Space Grotesk', 'Helvetica Neue', Arial, sans-serif; font-size: 13.5px; font-weight: 600">${t}</div>
      <div style="font-size: 12px; line-height: 1.6; color: #6E6659; margin-top: 5px; text-wrap: pretty">${d}</div>
    </div>`).join('\n    ')}
  </div>
</div>
</div>`;

writeFileSync('Materiaux.dc.html', page({ body, props: JSON.stringify({ $preview: { width: W, height: 1700 } }) }));
console.log('Materiaux.dc.html ok');
