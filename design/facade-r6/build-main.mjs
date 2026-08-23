import { writeFileSync } from 'node:fs';
import { elevation, annotations, PALETTE_A } from './elevation.mjs';
import { page, header } from './page.mjs';
import { developpe } from './geo.mjs';

const W = 1160, SVGH = 1404;
const P = { ...PALETTE_A };   // couleurs figees : monocouche blanc, alu RAL 7024
const E = elevation(P, { scale: 37, x0: 244, y0: 1240 });

const LEG = [
  ['Monocouche blanc', 'Toute la façade en monocouche blanc, grain fin gratté. Joints creux horizontaux au droit de chaque plancher ; fonds de baie en retrait, légèrement plus sourds.'],
  ['Aquapanel cintré', `Bandeaux de rive ondulés, tracé relevé sur votre croquis. ${developpe().toFixed(2)} ml par balcon × 12 balcons (6 niveaux × 2 blocs) : ≈ ${(developpe() * 12).toFixed(0)} ml.`],
  ['Garde-corps mixte inox + verre noir', 'Suit l’onde au pas de 40 cm : 40 cm de verre feuilleté teinté noir, 40 cm de barreaudage inox 304 Ø 16, en alternance sur tout le développé. À 40 cm le verre reste plat sur n’importe quel rayon. Main courante inox Ø 42 continue, h = 1,10 m.'],
  ['Brise-vue aluminium', '40 cm de large, sur l’axe du vide, ENTRE les deux petits balcons — pas en façade. Lames RAL 7024 du fond de la fente au garde-corps, du R+2 à la toiture : chaque voisin est chez lui.'],
  ['Porte-balcon aluminium', 'TPR série 65, RAL 7024 gris graphite. 2 vantaux coulissants, 1,80 m × 2,20 m, rupture de pont thermique, double vitrage 4/16/4.'],
  ['Balcons du vide central', 'Fente de 1,80 m creusée de 1,50 m. Au fond, deux petits balcons de 0,70 × 0,80 m, un par logement, porte-fenêtre de 0,70 m. Garde-corps en verre feuilleté, à 0,70 m en arrière du nu.'],
  ['Ventilation parking R+1', 'Brise-vue aluminium à lames horizontales — ventilation naturelle du niveau parking, façade fermée visuellement.'],
  ['Couvertine aluminium', 'RAL 7024, en tête d’acrotère et de poteau, avec goutte d’eau. Souligne le couronnement.'],
  ['Éclairage linéaire LED', `Gorge de 5 cm en sous-face de chaque bandeau cintré : la lumière lèche la courbe et la dessine sur toute sa longueur. ≈ ${(developpe() * 12).toFixed(0)} ml, 3000 K, IP65.`],
  ['Éclairage vertical de balcon', 'Profil LED encastré dans le trumeau entre les deux portes-balcon, 1,90 m de haut. Deux par balcon, sur le même circuit que la gorge de rive.'],
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

const body = `<div style="width: ${W}px; background: #FFFFFF">
${header({
  w: W,
  kicker: 'Immeuble R+8 · logements · Algérie',
  title: 'Façade principale',
  sub: 'Variante A « Blanc &amp; Graphite » — direction retenue. Monocouche blanc sur toute la façade, bandeaux de rive cintrés en Aquapanel blanc, garde-corps mixte inox et verre feuilleté noir suivant l’onde, aluminium RAL 7024 gris graphite.',
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
  $preview: { width: W, height: 2030 },
  wall: { editor: 'color', default: '#E8E0D2', section: 'Teintes', options: ['#E8E0D2', '#EFEDE8', '#D9CDB6', '#C9BCA4'] },
  accent: { editor: 'color', default: '#8A6E4C', section: 'Teintes', options: ['#8A6E4C', '#3A3E41', '#6E7A6B', '#9A5B3E'] },
}).replace(/&/g, '&amp;').replace(/'/g, '&#39;');

writeFileSync('Main.dc.html', page({ body, props }));
console.log('Main.dc.html', (page({ body, props }).length / 1024).toFixed(1), 'KB');
