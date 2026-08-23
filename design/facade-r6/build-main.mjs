import { writeFileSync } from 'node:fs';
import { elevation, annotations, PALETTE_A } from './elevation.mjs';
import { page, header } from './page.mjs';
import { developpe } from './geo.mjs';

const W = 1160, SVGH = 1272;
const P = { ...PALETTE_A, wall: '{{wall}}', accent: '{{accent}}' };
const E = elevation(P, { scale: 42, x0: 215, y0: 1092 });

const LEG = [
  ['Monocouche gratté', 'Voiles, poteaux et acrotère. Teinte ivoire sablé, grain fin, joints creux horizontaux au droit de chaque plancher.'],
  ['Aquapanel cintré', `Habillage des bandeaux de rive ondulés. ${developpe().toFixed(1)} ml par balcon × 8 balcons, plus l’acrotère de terrasse R+2 en onde continue : ≈ 99 ml.`],
  ['Garde-corps verre + inox', 'Verre feuilleté 8.8.4 clair, montants et main courante inox 304 brossé Ø 42 mm. Hauteur 1.10 m.'],
  ['Brise-vue aluminium', 'Vide central 1.80 m — lames verticales anodisées bronze, du R+2 au niveau toiture. Intimité des deux balcons en vis-à-vis.'],
  ['Porte-balcon aluminium', '2 vantaux coulissants, 1.80 m de large × 2.40 m de haut, rupture de pont thermique, double vitrage 4/16/4.'],
  ['Terrasse R+2', 'Sur toiture du parking, 4.00 m de profondeur. Acrotère habillé Aquapanel + garde-corps verre et inox identique aux balcons.'],
  ['Ventilation parking R+1', 'Brise-vue aluminium à lames horizontales — ventilation naturelle du niveau parking, façade fermée visuellement.'],
  ['Couvertine aluminium', 'Bronze anodisé, en tête d’acrotère et de poteau, avec goutte d’eau. Souligne le couronnement.'],
];

const legend = `<div style="padding: 26px 44px 40px">
  <div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 22px 30px">
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
  sub: 'Variante A — « Ivoire &amp; Bronze ». Monocouche gratté, bandeaux de rive cintrés en Aquapanel, garde-corps verre feuilleté + inox brossé, brise-vue aluminium anodisé bronze.',
  right: 'ÉCHELLE 1:100<br>COTES EN MÈTRES<br>NIVEAUX / NGF PROJET<br>ÉTAT PROJETÉ',
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
