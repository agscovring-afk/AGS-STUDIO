import { writeFileSync } from 'node:fs';
import { elevation, annotations, PALETTE_A } from './elevation.mjs';
import { page, header } from './page.mjs';
import { developpe } from './geo.mjs';

const W = 1160, SVGH = 1272;
const P = { ...PALETTE_A, wall: '{{wall}}', accent: '{{accent}}' };
const E = elevation(P, { scale: 42, x0: 215, y0: 1092 });

const LEG = [
  ['Monocouche gratté', 'Voiles, poteaux et acrotère. Teinte ivoire sablé, grain fin, joints creux horizontaux au droit de chaque plancher.'],
  ['Aquapanel cintré', `Bandeaux de rive ondulés. ${developpe().toFixed(1)} ml par balcon × 8 balcons + les deux acrotères de terrasse : ≈ 99 ml.`],
  ['Garde-corps mixte inox + verre', 'Suit l’onde. Barreaudage inox 304 Ø 16 aux creux et aux crêtes, panneaux verre feuilleté 8.8.4 de 1,09 m entre les deux. Main courante inox Ø 42 continue, h = 1,10 m.'],
  ['Brise-vue aluminium', 'Vide central 1,80 m — lames verticales anodisées bronze, du R+2 au niveau toiture. Intimité des deux balcons en vis-à-vis.'],
  ['Porte-balcon aluminium', '2 vantaux coulissants, 1,80 m × 2,40 m, rupture de pont thermique, double vitrage 4/16/4.'],
  ['Terrasses R+2', 'Une par logement — 7,85 m chacune sur 4,00 m de profondeur, séparées par le vide central laissé ouvert.'],
  ['Ventilation parking R+1', 'Brise-vue aluminium à lames horizontales — ventilation naturelle du niveau parking, façade fermée visuellement.'],
  ['Couvertine aluminium', 'Bronze anodisé, en tête d’acrotère et de poteau, avec goutte d’eau. Souligne le couronnement.'],
  ['Éclairage linéaire LED', 'Gorge de 5 cm en sous-face de chaque bandeau cintré : la lumière lèche la courbe et la dessine sur toute sa longueur. ≈ 99 ml, 3000 K, IP65.'],
  ['Brise-vue rétroéclairé', 'Rampe LED derrière les lames du vide central : la faille devient la seule verticale lumineuse de la façade.'],
];

const legend = `<div style="padding: 26px 44px 40px">
  <div style="display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 22px 24px">
    ${LEG.map(([t, d], i) => `<div style="display: flex; gap: 11px; align-items: flex-start">
      <div style="flex: 0 0 auto; width: 21px; height: 21px; border: 1px solid #23211E; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; color: #23211E; margin-top: 1px">${i + 1}</div>
      <div>
        <div style="font-family: 'Space Grotesk', 'Helvetica Neue', Arial, sans-serif; font-size: 13px; font-weight: 600; letter-spacing: -0.01em">${t}</div>
        <div style="font-size: 11.5px; line-height: 1.55; color: #6E6659; margin-top: 4px; text-wrap: pretty">${d}</div>
      </div>
    </div>`).join('\n    ')}
  </div>
</div>`;

const body = `<div style="width: ${W}px; background: #F1EDE5">
${header({
  w: W,
  kicker: 'Immeuble R+6 · logements · Algérie',
  title: 'Façade principale',
  sub: 'Variante A « Ivoire &amp; Bronze » — direction retenue. Monocouche gratté, bandeaux de rive cintrés en Aquapanel soulignés d’une gorge lumineuse, garde-corps mixte inox et verre suivant l’onde, brise-vue aluminium anodisé bronze.',
  right: 'ÉCHELLE 1:100<br>COTES EN MÈTRES<br>NIVEAUX / NGF PROJET<br>VARIANTE A — RETENUE',
})}
<svg viewBox="0 0 ${W} ${SVGH}" width="${W}" height="${SVGH}" xmlns="http://www.w3.org/2000/svg" style="display: block">
${E.svg}
${annotations(PALETTE_A, E)}
</svg>
<div class="rule" style="margin: 0 44px"></div>
${legend}
</div>`;

const props = JSON.stringify({
  $preview: { width: W, height: 1790 },
  wall: { editor: 'color', default: '#E8E0D2', section: 'Teintes', options: ['#E8E0D2', '#EFEDE8', '#D9CDB6', '#C9BCA4'] },
  accent: { editor: 'color', default: '#8A6E4C', section: 'Teintes', options: ['#8A6E4C', '#3A3E41', '#6E7A6B', '#9A5B3E'] },
}).replace(/&/g, '&amp;').replace(/'/g, '&#39;');

writeFileSync('Main.dc.html', page({ body, props }));
console.log('Main.dc.html', (page({ body, props }).length / 1024).toFixed(1), 'KB');
