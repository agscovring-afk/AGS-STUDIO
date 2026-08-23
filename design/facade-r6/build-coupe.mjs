import { writeFileSync } from 'node:fs';
import { LV, DMIN, DMAX, FASCIA, GC, AVANCEE, PBH } from './geo.mjs';
import { page, header } from './page.mjs';
import { txt, dimH, dimV, levelMark } from './svgkit.mjs';

const W = 900, H = 1218, S = 38, X0 = 268, Y0 = 1010;
const XF = 4.20, XP = XF + AVANCEE;                   // nu de facade / nu avant du parking
const px = (m) => +(X0 + m * S).toFixed(2), py = (h) => +(Y0 - h * S).toFixed(2);
const wm = (m) => +(m * S).toFixed(2);
const R = (x1, x2, h1, h2, fill, ex = '') => `<rect x="${px(x1)}" y="${py(h2)}" width="${wm(x2 - x1)}" height="${wm(h2 - h1)}" fill="${fill}" ${ex}/>`;
const C = { beton: '#4A443B', betonL: '#7B7264', aqua: '#FBF9F5', accent: '#8A6E4C',
  inox: '#9FA6AA', ink: '#23211E', dim: '#8C8478', vue: '#D3C9B6', sol: '#CFC3AC' };
const DALLE = 0.20, LIVING = [LV.r3, LV.r4, LV.r5, LV.r6];
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
for (const [h, b] of [[LV.r1, XP], [LV.r2, XP], [LV.r3, XF], [LV.r4, XF], [LV.r5, XF], [LV.r6, XF], [LV.toit, XF]])
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
  g.push(`<path d="M ${px(XF)} ${py(h - DALLE)} L ${px(XF + DMIN)} ${py(h - DALLE)} L ${px(XF + DMIN)} ${py(h + 0.02)}" fill="none" stroke="${C.ink}" stroke-width="1.3" stroke-dasharray="7 4"/>`);
  // garde-corps verre + inox, lisible en coupe
  g.push(R(XF + DMAX - 0.10, XF + DMAX - 0.02, h + 0.05, h + GC - 0.06, 'url(#gl2)'));
  g.push(`<line x1="${px(XF + DMAX - 0.06)}" y1="${py(h)}" x2="${px(XF + DMAX - 0.06)}" y2="${py(h + GC)}" stroke="${C.inox}" stroke-width="2.6"/>`);
  g.push(R(XF + DMAX - 0.22, XF + DMAX + 0.08, h + GC - 0.09, h + GC, C.inox));
  g.push(R(XF - 0.28, XF, h, h + PBH, C.accent, 'opacity="0.92"'));
  g.push(txt(px(XF + DMAX / 2), py(h) + 22, 'BALCON', { size: 8.5, fill: C.dim, ls: '0.16em', weight: 700 }));
  g.push(txt(px(XF / 2), py(h) + 26, 'LOGEMENT', { size: 8.5, fill: C.dim, ls: '0.16em', weight: 700 }));
}

// ---- terrasse R+2 --------------------------------------------------------
g.push(R(XF, XP, LV.r2, LV.r2 + 0.07, '#DED4C1'));
g.push(R(XP - 0.24, XP + 0.02, LV.r2, LV.r2 + FASCIA, C.aqua));
g.push(R(XP - 0.16, XP - 0.08, LV.r2 + FASCIA + 0.05, LV.r2 + FASCIA + GC - 0.06, 'url(#gl2)'));
g.push(`<line x1="${px(XP - 0.12)}" y1="${py(LV.r2 + FASCIA)}" x2="${px(XP - 0.12)}" y2="${py(LV.r2 + FASCIA + GC)}" stroke="${C.inox}" stroke-width="2.6"/>`);
g.push(R(XP - 0.28, XP + 0.04, LV.r2 + FASCIA + GC - 0.09, LV.r2 + FASCIA + GC, C.inox));
g.push(R(XF - 0.28, XF, LV.r2, LV.r2 + PBH, C.accent, 'opacity="0.92"'));
g.push(txt(px((XF + XP) / 2), py(LV.r2) + 26, 'TERRASSE R+2 — 4.00 m', { size: 9, fill: C.dim, ls: '0.14em', weight: 700 }));
g.push(txt(px(XF / 2), py(LV.r2) + 26, 'LOGEMENT', { size: 8.5, fill: C.dim, ls: '0.16em', weight: 700 }));

// ---- parking -------------------------------------------------------------
g.push(R(XP - 0.10, XP, LV.r1 + 0.70, LV.r1 + 2.50, C.accent));
const car = (x, h) => `<path d="M ${px(x)} ${py(h)} l ${wm(0.42)} ${-wm(0.38)} l ${wm(1.15)} 0 l ${wm(0.48)} ${wm(0.38)} l ${wm(1.35)} 0 l ${wm(0.26)} ${wm(0.26)} l 0 ${wm(0.48)} l ${-wm(3.66)} 0 l 0 ${-wm(0.48)} z" fill="${C.vue}" stroke="${C.betonL}" stroke-width="0.8"/>`;
for (const h of [LV.r1 - DALLE, LV.r2 - DALLE]) g.push(car(0.55, h) + car(4.45, h));
for (const [h, t] of [[1.30, 'PARKING RDC'], [4.70, 'PARKING R+1']])
  g.push(txt(px(XP / 2), py(h), t, { size: 9.5, fill: C.dim, ls: '0.16em', weight: 700 }));

// silhouette d'echelle sur le balcon du R+4
{
  const bx = XF + 1.9, bh = LV.r4;
  g.push(`<g fill="${C.betonL}" opacity="0.85"><circle cx="${px(bx)}" cy="${py(bh + 1.62)}" r="${wm(0.11)}"/>
    <path d="M ${px(bx) - wm(0.17)} ${py(bh + 1.48)} l ${wm(0.34)} 0 l ${wm(0.05)} ${wm(0.62)} l ${-wm(0.11)} 0 l ${-wm(0.04)} ${wm(0.86)} l ${-wm(0.14)} 0 l ${-wm(0.04)} ${-wm(0.5)} l ${-wm(0.04)} ${wm(0.5)} l ${-wm(0.14)} 0 l ${-wm(0.04)} ${-wm(0.86)} l ${-wm(0.11)} 0 z"/></g>`);
}

// ligne de rupture
g.push(`<path d="M ${px(-0.06)} ${py(LV.acr + 0.5)} L ${px(-0.06)} ${py(-0.6)}" fill="none" stroke="${C.ink}" stroke-width="1.2"/>`);
g.push(`<path d="M ${px(-0.06)} ${py(12.2)} l -9 -8 l 18 -7" fill="none" stroke="${C.ink}" stroke-width="1.2"/>`);
g.push(txt(0, 0, 'COUPE PARTIELLE — PROFONDEUR DU BATIMENT A CONFIRMER', { size: 8.5, fill: C.dim, ls: '0.12em', weight: 600, transform: `translate(${px(-0.06) - 15} ${py(11.8)}) rotate(-90)` }));

// ---- cotes et niveaux ----------------------------------------------------
const yc = py(-0.9) + 42;
g.push(dimH(px(XF), px(XF + DMIN), yc, '1.30', { size: 10.5 }));
g.push(dimH(px(XF), px(XF + DMAX), yc + 30, '3.00', { size: 10.5 }));
g.push(dimH(px(XF), px(XP), yc + 62, '4.00', { size: 13, weight: 700 }));
g.push(`<line x1="${px(XF)}" y1="${py(-0.9)}" x2="${px(XF)}" y2="${yc + 70}" stroke="${C.dim}" stroke-width="0.7" stroke-dasharray="3 3"/>`);
g.push(txt(px(XF), yc + 88, 'BALCON 1.30 → 3.00 m  ·  AVANCEE DU PARKING 4.00 m SUR LE NU DE FACADE',
  { size: 9, fill: C.dim, ls: '0.13em', weight: 600, anchor: 'start' }));
const xv = px(0) - 76;
[[LV.rdc, LV.r1, '3.40'], [LV.r1, LV.r2, '3.06'], [LV.r2, LV.r3, '3.06'], [LV.r3, LV.r4, '3.06'],
 [LV.r4, LV.r5, '3.06'], [LV.r5, LV.r6, '3.06'], [LV.r6, LV.toit, '3.06'], [LV.toit, LV.acr, '1.00']]
  .forEach(([a, b, t]) => g.push(dimV(py(a), py(b), xv, t, { size: 10 })));
g.push(dimV(py(0), py(LV.acr), xv - 44, '22.76', { size: 12.5, weight: 700 }));
[[LV.rdc, '± 0.00', 'RDC — PARKING'], [LV.r1, '+ 3.40', 'R+1 — PARKING'], [LV.r2, '+ 6.46', 'R+2 — TERRASSE'],
 [LV.r3, '+ 9.52', 'R+3'], [LV.r4, '+ 12.58', 'R+4'], [LV.r5, '+ 15.64', 'R+5'], [LV.r6, '+ 18.70', 'R+6'],
 [LV.toit, '+ 21.76', 'TOITURE'], [LV.acr, '+ 22.76', 'HAUT ACROTERE']]
  .forEach(([h, alt, t]) => g.push(levelMark(px(XP) + 92, py(h), alt, t)));

const body = `<div style="width: ${W}px; background: #F1EDE5">
${header({ w: W, kicker: 'Coupe A-A · transversale', title: 'Avancée parking &amp; terrasse',
  sub: 'Le socle parking RDC + R+1 avance de 4.00 m sur le nu de façade ; sa toiture devient la terrasse du R+2. Au-dessus, les balcons en console suivent l’onde de rive, de 1.30 m au creux à 3.00 m à la crête.',
  right: 'ÉCHELLE 1:100<br>COTES EN MÈTRES<br>ÉTAT PROJETÉ' })}
<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" xmlns="http://www.w3.org/2000/svg" style="display: block">${g.join('\n')}</svg>
</div>`;
writeFileSync('Coupe.dc.html', page({ body, props: JSON.stringify({ $preview: { width: W, height: H + 200 } }) }));
console.log('Coupe.dc.html ok');
