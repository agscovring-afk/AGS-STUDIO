import { writeFileSync } from 'node:fs';
import { LV, ETAGES, BALCONS, DMIN, DCREUX, DMAX, FASCIA, GC, AVANCEE, PBH, HSP, DALLE, RETRAIT } from './geo.mjs';
import { page, header } from './page.mjs';
import { txt, dimH, dimV, levelMark } from './svgkit.mjs';

const W = 900, H = 1330, S = 33, X0 = 262, Y0 = 1096;
const XF = 4.20, XP = XF + AVANCEE;                   // nu de facade / nu avant du parking
const px = (m) => +(X0 + m * S).toFixed(2), py = (h) => +(Y0 - h * S).toFixed(2);
const wm = (m) => +(m * S).toFixed(2);
const R = (x1, x2, h1, h2, fill, ex = '') => `<rect x="${px(x1)}" y="${py(h2)}" width="${wm(x2 - x1)}" height="${wm(h2 - h1)}" fill="${fill}" ${ex}/>`;
const C = { beton: '#4A443B', betonL: '#7B7264', aqua: '#FFFFFF', accent: '#474B4E',
  inox: '#9FA6AA', ink: '#23211E', dim: '#8C8478', vue: '#D3C9B6', sol: '#CFC3AC' };
const LIVING = BALCONS;
const g = [];
g.push(`<defs><linearGradient id="gl2" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#DCE6E5" stop-opacity="0.95"/><stop offset="1" stop-color="#A9BBBE" stop-opacity="0.55"/></linearGradient></defs>`);

// ---- terrain -------------------------------------------------------------
const TP = [[-1.7, 8.6], [-0.35, 6.7], [0, 3.1], [0, -0.35], [XP + 2.6, -0.72]];
const tpath = TP.map(([x, h], i) => `${i ? 'L' : 'M'} ${px(x)} ${py(h)}`).join(' ');
g.push(`<path d="${tpath} L ${px(XP + 2.6)} ${py(-2.9)} L ${px(-1.7)} ${py(-2.9)} Z" fill="${C.sol}"/>`);
g.push(`<path d="${tpath}" fill="none" stroke="${C.ink}" stroke-width="1.6"/>`);
for (let i = 0; i < TP.length - 1; i++) {
  const [x1, h1] = TP[i], [x2, h2] = TP[i + 1], n = Math.max(2, Math.round(Math.hypot(px(x2) - px(x1), py(h2) - py(h1)) / 13));
  for (let k = 0; k < n; k++) {
    const t = k / n, X = px(x1) + (px(x2) - px(x1)) * t, Y = py(h1) + (py(h2) - py(h1)) * t;
    g.push(`<line x1="${X.toFixed(1)}" y1="${Y.toFixed(1)}" x2="${(X - 8).toFixed(1)}" y2="${(Y + 10).toFixed(1)}" stroke="${C.dim}" stroke-width="0.7" opacity="0.65"/>`);
  }
}

// ---- ossature coupee -----------------------------------------------------
g.push(R(0, XP, -0.30, 0, C.beton));
for (const [h, b] of [[LV.r1, XP], [LV.r2, XP], ...BALCONS.map((h) => [h, XF]), [LV.toit, XF]])
  g.push(R(0, b, h - DALLE, h, C.beton));
g.push(R(0, 0.28, -0.30, LV.toit, C.beton));
g.push(R(XF - 0.28, XF, LV.r2, LV.acr, C.beton));
g.push(R(XP - 0.24, XP, -0.30, LV.r2, C.beton));
g.push(R(XF - 0.28, XF, LV.acr - 0.10, LV.acr, C.accent));

// ---- balcons en console --------------------------------------------------
for (const h of LIVING) {
  g.push(R(XF, XF + DMAX, h - DALLE, h, C.beton));
  g.push(R(XF + DMAX - 0.18, XF + DMAX + 0.02, h - FASCIA, h + 0.02, C.aqua));
  g.push(R(XF + DMAX - 0.18, XF + DMAX + 0.02, h - FASCIA, h + 0.02, 'none', `stroke="${C.betonL}" stroke-width="0.9"`));
  g.push(`<path d="M ${px(XF)} ${py(h - DALLE)} L ${px(XF + DCREUX)} ${py(h - DALLE)} L ${px(XF + DCREUX)} ${py(h + 0.02)}" fill="none" stroke="${C.ink}" stroke-width="1.3" stroke-dasharray="7 4"/>`);
  // garde-corps : la coupe passe a la crete de l'onde, donc en barreaudage inox
  g.push(R(XF + DMAX - 0.10, XF + DMAX - 0.03, h + 0.08, h + 0.15, C.inox));
  g.push(`<line x1="${px(XF + DMAX - 0.065)}" y1="${py(h + 0.10)}" x2="${px(XF + DMAX - 0.065)}" y2="${py(h + GC)}" stroke="${C.inox}" stroke-width="2.4"/>`);
  g.push(R(XF + DMAX - 0.22, XF + DMAX + 0.08, h + GC - 0.09, h + GC, C.inox));
  // gorge LED en sous-face du bandeau cintre
  g.push(R(XF + DMAX - 0.20, XF + DMAX - 0.13, h - FASCIA, h - FASCIA + 0.07, '#F2C46A'));
  g.push(`<path d="M ${px(XF + DMAX - 0.165)} ${py(h - FASCIA)} l ${wm(0.55)} ${wm(0.42)} M ${px(XF + DMAX - 0.165)} ${py(h - FASCIA)} l ${wm(0.16)} ${wm(0.66)} M ${px(XF + DMAX - 0.165)} ${py(h - FASCIA)} l ${-wm(0.28)} ${wm(0.60)}" fill="none" stroke="#C79A3E" stroke-width="1" opacity="0.75"/>`);
  g.push(R(XF - 0.28, XF, h, h + PBH, C.accent, 'opacity="0.92"'));
  g.push(txt(px(XF + DMAX / 2), py(h) - 50, 'BALCON', { size: 8.5, fill: C.dim, ls: '0.16em', weight: 700 }));
  g.push(txt(px(XF / 2), py(h) - 50, 'LOGEMENT', { size: 8.5, fill: C.dim, ls: '0.16em', weight: 700 }));
}

// ---- terrasse R+2 --------------------------------------------------------
g.push(R(XF, XP, LV.r2, LV.r2 + 0.07, '#DED4C1'));
g.push(R(XP - 0.24, XP + 0.02, LV.r2, LV.r2 + FASCIA, C.aqua));
g.push(R(XP - 0.17, XP - 0.09, LV.r2 + FASCIA + 0.03, LV.r2 + FASCIA + 0.10, C.inox));
g.push(`<line x1="${px(XP - 0.13)}" y1="${py(LV.r2 + FASCIA + 0.05)}" x2="${px(XP - 0.13)}" y2="${py(LV.r2 + FASCIA + GC)}" stroke="${C.inox}" stroke-width="2.4"/>`);
g.push(R(XP - 0.20, XP - 0.13, LV.r2, LV.r2 + 0.07, '#F2C46A'));
g.push(R(XP - 0.28, XP + 0.04, LV.r2 + FASCIA + GC - 0.09, LV.r2 + FASCIA + GC, C.inox));
g.push(R(XF - 0.28, XF, LV.r2, LV.r2 + PBH, C.accent, 'opacity="0.92"'));
g.push(txt(px((XF + XP) / 2) - 16, py(LV.r2) - 50, 'TERRASSE R+2 — 4.00 m', { size: 9, fill: C.dim, ls: '0.14em', weight: 700 }));
g.push(txt(px(XF / 2), py(LV.r2) - 50, 'LOGEMENT', { size: 8.5, fill: C.dim, ls: '0.16em', weight: 700 }));

// ---- parking -------------------------------------------------------------
g.push(R(XP - 0.10, XP, LV.r1 + 1.55, LV.r1 + 2.35, C.accent));
g.push(R(XP - 0.10, XP, 1.35, 2.15, C.accent));
const car = (x, h) => `<path d="M ${px(x)} ${py(h)} l ${wm(0.42)} ${-wm(0.38)} l ${wm(1.15)} 0 l ${wm(0.48)} ${wm(0.38)} l ${wm(1.35)} 0 l ${wm(0.26)} ${wm(0.26)} l 0 ${wm(0.48)} l ${-wm(3.66)} 0 l 0 ${-wm(0.48)} z" fill="${C.vue}" stroke="${C.betonL}" stroke-width="0.8"/>`;
for (const h of [LV.r1 - DALLE, LV.r2 - DALLE]) g.push(car(0.55, h) + car(4.45, h));
for (const [h, t] of [[1.10, 'PARKING RDC'], [4.20, 'PARKING R+1']])
  g.push(txt(px(XP / 2), py(h), t, { size: 9.5, fill: C.dim, ls: '0.16em', weight: 700 }));

// silhouette d'echelle sur le balcon du R+4
{
  const bx = XF + 2.62, bh = LV.r4;
  g.push(`<g fill="${C.betonL}" opacity="0.85"><circle cx="${px(bx)}" cy="${py(bh + 1.62)}" r="${wm(0.11)}"/>
    <path d="M ${px(bx) - wm(0.17)} ${py(bh + 1.48)} l ${wm(0.34)} 0 l ${wm(0.05)} ${wm(0.62)} l ${-wm(0.11)} 0 l ${-wm(0.04)} ${wm(0.86)} l ${-wm(0.14)} 0 l ${-wm(0.04)} ${-wm(0.5)} l ${-wm(0.04)} ${wm(0.5)} l ${-wm(0.14)} 0 l ${-wm(0.04)} ${-wm(0.86)} l ${-wm(0.11)} 0 z"/></g>`);
}

// renvoi eclairage
{
  const h = LV.r5, xa = px(XF + DMAX) + 30, ya = py(h - FASCIA) + 34;
  g.push(`<line x1="${px(XF + DMAX - 0.13)}" y1="${py(h - FASCIA) + 3}" x2="${xa}" y2="${ya}" stroke="${C.ink}" stroke-width="0.8"/>`);
  g.push(`<circle cx="${px(XF + DMAX - 0.13)}" cy="${py(h - FASCIA) + 3}" r="2.2" fill="${C.ink}"/>`);
  g.push(txt(xa + 4, ya + 4, 'GORGE LED 5 cm', { size: 8.5, anchor: 'start', fill: '#B08334', ls: '0.1em', weight: 700 }));
  g.push(txt(xa + 4, ya + 17, 'EN SOUS-FACE DE RIVE', { size: 8.5, anchor: 'start', fill: C.dim, ls: '0.1em', weight: 700 }));
}

// ligne de rupture
g.push(`<path d="M ${px(-0.06)} ${py(LV.acr + 0.5)} L ${px(-0.06)} ${py(-0.6)}" fill="none" stroke="${C.ink}" stroke-width="1.2"/>`);
g.push(`<path d="M ${px(-0.06)} ${py(12.2)} l -9 -8 l 18 -7" fill="none" stroke="${C.ink}" stroke-width="1.2"/>`);
g.push(txt(0, 0, 'COUPE PARTIELLE — PROFONDEUR DU BATIMENT A CONFIRMER', { size: 8.5, fill: C.dim, ls: '0.12em', weight: 600, transform: `translate(${px(-0.06) - 15} ${py(11.8)}) rotate(-90)` }));

// ---- cotes et niveaux ----------------------------------------------------
const yc = py(-0.9) + 42;
g.push(dimH(px(XF), px(XF + DCREUX), yc, DCREUX.toFixed(2), { size: 10.5 }));
g.push(dimH(px(XF), px(XF + DMAX), yc + 30, DMAX.toFixed(2), { size: 10.5 }));
g.push(dimH(px(XF), px(XP), yc + 62, '4.00', { size: 13, weight: 700 }));
g.push(`<line x1="${px(XF)}" y1="${py(-0.9)}" x2="${px(XF)}" y2="${yc + 70}" stroke="${C.dim}" stroke-width="0.7" stroke-dasharray="3 3"/>`);
g.push(txt(px(XF), yc + 88, `BALCON ${DCREUX.toFixed(2)} → ${DMAX.toFixed(2)} m  ·  AVANCEE DU PARKING 4.00 m SUR LE NU DE FACADE`,
  { size: 9, fill: C.dim, ls: '0.13em', weight: 600, anchor: 'start' }));
g.push(txt(px(0), yc + 110, 'LES DEUX TERRASSES R+2 SONT SEPAREES PAR LE VIDE CENTRAL — VOIR FACADE',
  { size: 9, fill: C.dim, ls: '0.11em', weight: 600, anchor: 'start' }));
const xv = px(0) - 76;
for (let i = 0; i < ETAGES.length - 1; i++)
  g.push(dimV(py(ETAGES[i][0]), py(ETAGES[i + 1][0]), xv, (ETAGES[i + 1][0] - ETAGES[i][0]).toFixed(2), { size: 9.5 }));
g.push(dimV(py(0), py(LV.acr), xv - 44, LV.acr.toFixed(2), { size: 12.5, weight: 700 }));
ETAGES.forEach(([h, alt, t]) => g.push(levelMark(px(XP) + 92, py(h), alt, t)));

const body = `<div style="width: ${W}px; background: #FFFFFF">
${header({ w: W, kicker: 'Coupe A-A · transversale', title: 'Avancée parking &amp; terrasse',
  sub: 'Le socle parking RDC + R+1 avance de 4.00 m sur le nu de façade ; sa toiture devient la terrasse du R+2. Au-dessus, les balcons en console suivent l’onde de rive, de 0,79 m au creux à 1,60 m à la crête — tracé relevé sur votre croquis. Hauteur libre 3,06 m, dalle 0,20 m ; RDC 2,60 m libre.',
  right: 'ÉCHELLE 1:100<br>COTES EN MÈTRES<br>ÉTAT PROJETÉ' })}
<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" xmlns="http://www.w3.org/2000/svg" style="display: block">${g.join('\n')}</svg>
</div>`;
writeFileSync('Coupe.dc.html', page({ body, props: JSON.stringify({ $preview: { width: W, height: H + 210 } }) }));
console.log('Coupe.dc.html ok');
