import { writeFileSync } from 'node:fs';
import { page, header } from './page.mjs';
import { txt, dimH } from './svgkit.mjs';
import { XS, LV, BLOCS, DMIN, DMAX, AVANCEE, COL, depthAt, doors, developpe } from './geo.mjs';

// A3 paysage a 96 px/pouce : 420 x 297 mm
const W = 1587, H = 1123;
const S = 75.5906;                       // 1 m = 20 mm = echelle 1:50
const X0 = 150, YF = 178;                // origine facade (x = 0, profondeur 0)
const px = (m) => +(X0 + m * S).toFixed(2);
const py = (d) => +(YF + d * S).toFixed(2);
const wm = (m) => +(m * S).toFixed(2);
const C = { beton: '#4A443B', mur: '#E8E0D2', int: '#EFEAE0', ink: '#23211E', dim: '#8C8478',
  gridF: '#DCD4C4', gridM: '#BEB29B', ghost: '#B9A98C', accent: '#474B4E', vide: '#EDE9E1' };
const VOID = XS.vide;

function grille(dMax) {
  const g = [];
  for (let m = 0; m <= 17.5001; m += 0.25) {
    const strong = Math.abs(m - Math.round(m)) < 1e-6;
    g.push(`<line x1="${px(m)}" y1="${py(0)}" x2="${px(m)}" y2="${py(dMax)}" stroke="${strong ? C.gridM : C.gridF}" stroke-width="${strong ? 0.8 : 0.5}"/>`);
  }
  for (let d = 0; d <= dMax + 1e-6; d += 0.25) {
    const strong = Math.round(d * 100) % 50 === 0;
    g.push(`<line x1="${px(0)}" y1="${py(d)}" x2="${px(17.5)}" y2="${py(d)}" stroke="${strong ? C.gridM : C.gridF}" stroke-width="${strong ? 0.8 : 0.5}"/>`);
  }
  return g.join('\n');
}

function graduations(dMax) {
  const g = [];
  for (let m = 0; m <= 17.5001; m += 1) {
    g.push(`<line x1="${px(m)}" y1="${py(dMax)}" x2="${px(m)}" y2="${py(dMax) + 7}" stroke="${C.ink}" stroke-width="1"/>`);
    g.push(txt(px(m), py(dMax) + 22, String(m), { size: 10, fill: C.dim, weight: 600 }));
  }
  g.push(`<line x1="${px(17.5)}" y1="${py(dMax)}" x2="${px(17.5)}" y2="${py(dMax) + 7}" stroke="${C.ink}" stroke-width="1"/>`);
  g.push(txt(px(17.5), py(dMax) + 22, '17.50', { size: 10, fill: C.ink, weight: 700 }));
  for (let d = 0; d <= dMax + 1e-6; d += 0.5) {
    g.push(`<line x1="${px(0) - 7}" y1="${py(d)}" x2="${px(0)}" y2="${py(d)}" stroke="${C.ink}" stroke-width="1"/>`);
    g.push(txt(px(0) - 12, py(d) + 4, d.toFixed(2), { size: 10, fill: C.dim, weight: 600, anchor: 'end' }));
  }
  g.push(txt(0, 0, 'PROFONDEUR DEPUIS LE NU DE FACADE (m)', { size: 9, fill: C.dim, ls: '0.14em', weight: 700, transform: `translate(${px(0) - 72} ${py(dMax / 2)}) rotate(-90)` }));
  g.push(txt(px(8.75), py(dMax) + 44, 'ABSCISSE LE LONG DE LA FACADE (m)', { size: 9, fill: C.dim, ls: '0.14em', weight: 700 }));
  return g.join('\n');
}

// ossature commune : mur de facade, poteaux, portes-balcon, interieur
function ossature(hInt = 1.45) {
  const g = [];
  g.push(`<rect x="${px(0)}" y="${py(-hInt)}" width="${wm(17.5)}" height="${wm(hInt - 0.30)}" fill="${C.int}"/>`);
  g.push(`<rect x="${px(0)}" y="${py(-0.30)}" width="${wm(17.5)}" height="${wm(0.30)}" fill="${C.beton}"/>`);
  for (const [a, b] of [XS.c1, XS.c2, XS.c3, XS.c4])
    g.push(`<rect x="${px(a)}" y="${py(-0.55)}" width="${wm(b - a)}" height="${wm(0.55)}" fill="${C.beton}"/>`);
  for (const bay of [XS.bayA, XS.bayB]) for (const [a, b] of doors(bay)) {
    g.push(`<rect x="${px(a)}" y="${py(-0.32)}" width="${wm(b - a)}" height="${wm(0.34)}" fill="#FFFFFF"/>`);
    g.push(`<rect x="${px(a)}" y="${py(-0.20)}" width="${wm((b - a) / 2)}" height="${wm(0.07)}" fill="${C.accent}"/>`);
    g.push(`<rect x="${px(a + (b - a) / 2)}" y="${py(-0.07)}" width="${wm((b - a) / 2)}" height="${wm(0.07)}" fill="${C.accent}"/>`);
    g.push(txt(px((a + b) / 2), py(-0.42), 'PB 1.80', { size: 8.5, fill: C.dim, ls: '0.08em', weight: 700 }));
  }
  g.push(txt(px(3.925), py(-0.95), 'INTERIEUR LOGEMENT', { size: 9.5, fill: C.dim, ls: '0.18em', weight: 700 }));
  g.push(txt(px(13.575), py(-0.95), 'INTERIEUR LOGEMENT', { size: 9.5, fill: C.dim, ls: '0.18em', weight: 700 }));
  return g.join('\n');
}

function chaine(y) {
  const ch = [[0, 0.55, '0.55'], [0.55, 1.45, '0.90'], [1.45, 3.25, '1.80'], [3.25, 4.60, '1.35'],
    [4.60, 6.40, '1.80'], [6.40, 7.30, '0.90'], [7.30, 7.85, '0.55'], [7.85, 9.65, '1.80'],
    [9.65, 10.20, '0.55'], [10.20, 11.10, '0.90'], [11.10, 12.90, '1.80'], [12.90, 14.25, '1.35'],
    [14.25, 16.05, '1.80'], [16.05, 16.95, '0.90'], [16.95, 17.50, '0.55']];
  return ch.map(([a, b, t]) => dimH(px(a), px(b), y, t, { size: 9.5 })).join('\n')
    + dimH(px(0), px(17.5), y + 42, '17.50', { size: 13, weight: 700 });
}

const foot = (items) => `<div style="padding: 18px 44px 26px">
  <div class="rule" style="margin-bottom: 16px"></div>
  <div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 26px">
    ${items.map(([t, d]) => `<div>
      <div style="font-family: 'Space Grotesk', 'Helvetica Neue', Arial, sans-serif; font-size: 13px; font-weight: 600">${t}</div>
      <div style="font-size: 12px; line-height: 1.6; color: #6E6659; margin-top: 5px; text-wrap: pretty">${d}</div>
    </div>`).join('\n    ')}
  </div>
  <div class="eyebrow" style="margin: 24px 0 10px">Notes</div>
  <div style="display: flex; flex-direction: column; gap: 26px">
    ${[0, 1, 2].map(() => '<div style="height: 1px; background: #D3C9B7"></div>').join('\n    ')}
  </div>
</div>`;

// ---------------------------------------------------------------------------
// Gabarit 1 — onde de rive des balcons
// ---------------------------------------------------------------------------
{
  const DMAXG = 3.60, SVGH = 640;
  const g = [];
  g.push(`<rect x="${px(0)}" y="${py(0)}" width="${wm(17.5)}" height="${wm(DMAXG)}" fill="#FFFFFF"/>`);
  g.push(grille(DMAXG));
  // vide central, traverse tout le niveau
  g.push(`<rect x="${px(VOID[0])}" y="${py(-1.45)}" width="${wm(1.80)}" height="${wm(1.45 + DMAXG)}" fill="${C.vide}"/>`);
  g.push(`<rect x="${px(VOID[0])}" y="${py(-1.45)}" width="${wm(1.80)}" height="${wm(1.45 + DMAXG)}" fill="none" stroke="${C.dim}" stroke-width="1.2" stroke-dasharray="7 5"/>`);
  g.push(txt(0, 0, 'VIDE CENTRAL 1.80', { size: 9.5, fill: C.dim, ls: '0.14em', weight: 700, transform: `translate(${px(8.75) + 4} ${py(1.9)}) rotate(90)` }));
  g.push(ossature(1.45));
  // trace actuel, en repere leger
  for (let bi = 0; bi < BLOCS.length; bi++) {
    const [b1, b2] = BLOCS[bi], pts = [];
    for (let i = 0; i <= 400; i++) {
      const m = b1 + (b2 - b1) * i / 400;
      pts.push(`${i ? 'L' : 'M'} ${px(m)} ${py(depthAt(m, bi))}`);
    }
    g.push(`<path d="${pts.join(' ')}" fill="none" stroke="${C.ghost}" stroke-width="1.6" stroke-dasharray="3 5" opacity="0.9"/>`);
  }
  g.push(`<path d="M ${px(0.75)} ${py(0.42)} l 34 0" stroke="${C.ghost}" stroke-width="1.6" stroke-dasharray="3 5"/>`);
  g.push(txt(px(0.75) + 42, py(0.42) + 4, 'TRACE RETENU — RELEVE SUR VOTRE CROQUIS DU 23.08',
    { size: 9.5, fill: C.ghost, ls: '0.08em', weight: 700, anchor: 'start' }));
  g.push(graduations(DMAXG));
  g.push(chaine(py(DMAXG) + 76));

  const body = `<div style="width: ${W}px; background: #FFFFFF">
${header({ w: W, kicker: 'Gabarit à dessiner · niveau courant R+3 à R+6',
  title: 'Dessine l’onde de rive', sub: 'Tout ce qui est en noir est figé : mur, poteaux de 0,55 m, portes-balcon de 1,80 m, vide central. La zone quadrillée est libre — trace la rive du balcon dedans. Un carreau = 0,25 m.',
  right: 'A3 PAYSAGE · ÉCHELLE 1:50<br>UN CARREAU = 0,25 m<br>COTES EN MÈTRES' })}
<svg viewBox="0 0 ${W} ${SVGH}" width="${W}" height="${SVGH}" xmlns="http://www.w3.org/2000/svg" style="display: block">${g.join('\n')}</svg>
${foot([
  ['Ce qu’il me faut', 'La ligne de rive, d’un poteau à l’autre. Si tu peux, note la profondeur aux crêtes et aux creux en lisant la règle de gauche — sinon je la relève sur ton dessin.'],
  ['Ce qui est contraint', 'Le tracé retenu part du poteau perpendiculairement au nu, sort à 1,80 m au grand lobe, revient à 0,79 m au creux médian, ressort à 1,45 m au petit lobe, pour un développé de ' + developpe().toFixed(2) + ' ml par balcon.'],
  ['Le bloc de droite', 'Dessine seulement le bloc gauche si tu veux : je reporte en symétrie. Si tu veux deux ondes différentes, dessine les deux.'],
])}
</div>`;
  writeFileSync('Gabarit-Onde.dc.html', page({ body, props: JSON.stringify({ $preview: { width: W, height: H } }) }));
  console.log('Gabarit-Onde.dc.html ok');
}

// ---------------------------------------------------------------------------
// Gabarit 2 — terrasses du R+2
// ---------------------------------------------------------------------------
{
  const DMAXG = 4.60, SVGH = 700;
  const g = [];
  g.push(`<rect x="${px(0)}" y="${py(0)}" width="${wm(17.5)}" height="${wm(DMAXG)}" fill="#FFFFFF"/>`);
  g.push(grille(DMAXG));
  // nu avant du parking : limite dure de la dalle
  g.push(`<line x1="${px(0)}" y1="${py(AVANCEE)}" x2="${px(17.5)}" y2="${py(AVANCEE)}" stroke="${C.ink}" stroke-width="2.4"/>`);
  g.push(txt(px(0.15), py(AVANCEE) - 11, 'NU AVANT DU PARKING — LIMITE DE DALLE, PROFONDEUR 4.00 m',
    { size: 9.5, fill: C.ink, ls: '0.1em', weight: 700, anchor: 'start' }));
  for (let m = 0; m < 17.5; m += 0.34)
    g.push(`<line x1="${px(m)}" y1="${py(AVANCEE)}" x2="${px(m + 0.22)}" y2="${py(AVANCEE) + 11}" stroke="${C.dim}" stroke-width="0.7" opacity="0.7"/>`);
  // vide central laisse ouvert dans la dalle
  g.push(`<rect x="${px(VOID[0])}" y="${py(-1.45)}" width="${wm(1.80)}" height="${wm(1.45 + AVANCEE)}" fill="${C.vide}"/>`);
  g.push(`<rect x="${px(VOID[0])}" y="${py(-1.45)}" width="${wm(1.80)}" height="${wm(1.45 + AVANCEE)}" fill="none" stroke="${C.ink}" stroke-width="1.6" stroke-dasharray="9 5"/>`);
  for (let d = -1.45; d < AVANCEE - 0.5; d += 0.34)
    g.push(`<line x1="${px(VOID[0])}" y1="${py(d)}" x2="${px(VOID[1])}" y2="${py(d + 0.5)}" stroke="${C.dim}" stroke-width="0.6" opacity="0.55"/>`);
  g.push(txt(0, 0, 'VIDE 1.80 — OUVERT', { size: 9.5, fill: C.ink, ls: '0.12em', weight: 700, transform: `translate(${px(8.75) + 4} ${py(2.05)}) rotate(90)` }));
  g.push(ossature(1.45));
  g.push(txt(px(3.925), py(2.0), 'TERRASSE LOGEMENT GAUCHE — 7.85 × 4.00 m', { size: 11, fill: C.ghost, ls: '0.14em', weight: 700 }));
  g.push(txt(px(13.575), py(2.0), 'TERRASSE LOGEMENT DROIT — 7.85 × 4.00 m', { size: 11, fill: C.ghost, ls: '0.14em', weight: 700 }));
  g.push(graduations(DMAXG));
  g.push(chaine(py(DMAXG) + 76));

  const body = `<div style="width: ${W}px; background: #FFFFFF">
${header({ w: W, kicker: 'Gabarit à dessiner · niveau R+2, sur la toiture du parking',
  title: 'Dessine les deux terrasses', sub: 'La dalle du parking s’arrête à 4,00 m : c’est la seule limite dure. Le vide central de 1,80 m est laissé ouvert. Dessine ce que tu veux dedans — ligne de garde-corps, jardinières, cloison de séparation, auvent. Un carreau = 0,25 m.',
  right: 'A3 PAYSAGE · ÉCHELLE 1:50<br>UN CARREAU = 0,25 m<br>COTES EN MÈTRES' })}
<svg viewBox="0 0 ${W} ${SVGH}" width="${W}" height="${SVGH}" xmlns="http://www.w3.org/2000/svg" style="display: block">${g.join('\n')}</svg>
${foot([
  ['Ce qu’il me faut', 'La ligne du garde-corps de chaque terrasse, et la façon dont tu sépares les deux logements. Dis-moi aussi si le garde-corps reprend l’onde des balcons ou s’il reste droit.'],
  ['Ce qui est contraint', 'La dalle ne va pas au-delà de 4,00 m. Le vide de 1,80 m sépare les deux terrasses — si tu veux le fermer ou le réduire à ce niveau, dessine-le, c’est faisable.'],
  ['Tu peux aussi ajouter', 'Un local technique, un point d’eau, une jardinière filante, un brise-vue entre les deux terrasses. Dessine-le à sa place, même en gros : je remets au propre.'],
])}
</div>`;
  writeFileSync('Gabarit-Terrasse.dc.html', page({ body, props: JSON.stringify({ $preview: { width: W, height: H } }) }));
  console.log('Gabarit-Terrasse.dc.html ok');
}
