import { writeFileSync } from 'node:fs';
import { XS, LV, BLOCS, MIROIR, DMIN, DCREUX, DMAX, COL, RETRAIT, PBW, PBH,
         AXE, BV_EP, BALCON_NICHE, BALCON_NICHE_P, GCN, PBN,
         depthAt, ondeAt, doors, developpe, gcSegments } from './geo.mjs';
import { page, header } from './page.mjs';
import { txt, dimH, dimV } from './svgkit.mjs';

const W = 1587, SVGH = 760, S = 75.5906, X0 = 150, YF = 330;
const px = (m) => +(X0 + m * S).toFixed(2);
const py = (d) => +(YF + d * S).toFixed(2);
const wm = (m) => +(m * S).toFixed(2);
const C = { beton: '#4A443B', int: '#EFEAE0', dalle: '#EFEAE0', ink: '#23211E', dim: '#8C8478',
  accent: '#474B4E', glass: '#8FA9AE', inox: '#6E7A80', led: '#D9A94A', niche: '#E4DFD5' };
const NP = 700;
const g = [];

// ---- dalles de balcon, une par bloc -------------------------------------
const rive = (b) => {
  const [m1, m2] = BLOCS[b], pts = [];
  for (let i = 0; i <= NP; i++) { const m = m1 + (m2 - m1) * i / NP; pts.push([px(m), py(depthAt(m, b))]); }
  return pts;
};
const path = (p) => p.map(([x, y], i) => `${i ? 'M' : 'M'} ${x} ${y}`.replace(/^M/, i ? 'L' : 'M')).join(' ');
const off = (p, d) => p.map(([x, y], i) => `${i ? 'L' : 'M'} ${x} ${(y - d).toFixed(2)}`).join(' ');

g.push(`<defs><linearGradient id="dl" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#F2EDE3"/><stop offset="1" stop-color="#E2DACB"/></linearGradient></defs>`);

for (let b = 0; b < 2; b++) {
  const [m1, m2] = BLOCS[b], R = rive(b);
  g.push(`<path d="M ${px(m1)} ${py(0)} ${path(R).slice(1)} L ${px(m2)} ${py(0)} Z" fill="url(#dl)"/>`);
  g.push(`<path d="${path(R)}" fill="none" stroke="${C.ink}" stroke-width="2"/>`);
  g.push(`<path d="${off(R, wm(0.18))}" fill="none" stroke="${C.dim}" stroke-width="1" stroke-dasharray="5 4"/>`);
  g.push(`<path d="${off(R, wm(0.05))}" fill="none" stroke="${C.led}" stroke-width="2.2" stroke-dasharray="10 5"/>`);
  // garde-corps mixte, 10 cm en retrait de la rive
  const GO = wm(0.10);
  const idx = (m) => Math.max(0, Math.min(NP, Math.round((m - m1) / (m2 - m1) * NP)));
  for (const seg of gcSegments(b)) {
    const i1 = idx(seg.x1), i2 = idx(seg.x2), sub = R.slice(i1, i2 + 1);
    if (sub.length < 2) continue;
    if (seg.kind === 'verre') {
      g.push(`<path d="${off(sub, GO)}" fill="none" stroke="${C.glass}" stroke-width="6.5" stroke-linecap="round" opacity="0.9"/>`);
      g.push(`<path d="${off(sub, GO)}" fill="none" stroke="#EAF2F3" stroke-width="2"/>`);
    } else {
      g.push(`<path d="${off(sub, GO)}" fill="none" stroke="${C.inox}" stroke-width="2"/>`);
      for (let m = seg.x1 + 0.055; m < seg.x2 - 0.03; m += 0.11) {
        const [bx, by] = R[idx(m)];
        g.push(`<circle cx="${bx}" cy="${(by - GO).toFixed(2)}" r="2.5" fill="${C.inox}"/>`);
      }
    }
    const [ex, ey] = R[Math.min(NP, i2)];
    g.push(`<circle cx="${ex}" cy="${(ey - GO).toFixed(2)}" r="4" fill="none" stroke="${C.inox}" stroke-width="2"/>`);
  }
}

// ---- mur de facade, poteaux, menuiseries ---------------------------------
const INT = -2.40;                       // profondeur d'interieur montree au plan
for (const [m1, m2] of BLOCS) {
  g.push(`<rect x="${px(m1)}" y="${py(INT)}" width="${wm(m2 - m1)}" height="${wm(-INT - 0.30)}" fill="${C.int}"/>`);
  g.push(`<rect x="${px(m1)}" y="${py(-0.30)}" width="${wm(m2 - m1)}" height="${wm(0.30)}" fill="${C.beton}"/>`);
}
// Derriere le fond de niche : le logement. Confirme le 23.08 — la porte de
// chaque balcon du vide s'ouvre depuis l'interieur, pas depuis un couloir.
{
  const [n1, n2] = XS.vide, back = -RETRAIT - 0.30;   // -1.80, dos du refend
  g.push(`<rect x="${px(n1)}" y="${py(INT)}" width="${wm(n2 - n1)}" height="${wm(back - INT)}" fill="${C.int}"/>`);
  // refend mitoyen : il prolonge le brise-vue vers l'interieur
  g.push(`<rect x="${px(AXE - BV_EP / 2)}" y="${py(INT)}" width="${wm(BV_EP)}" height="${wm(back - INT)}" fill="${C.beton}"/>`);
  for (const c of [(n1 + AXE - BV_EP / 2) / 2, (AXE + BV_EP / 2 + n2) / 2]) {
    g.push(`<path d="M ${px(c - PBN / 2)} ${py(-RETRAIT)} A ${wm(PBN)} ${wm(PBN)} 0 0 ${c < AXE ? 0 : 1} ${px(c + (c < AXE ? -PBN / 2 : PBN / 2))} ${py(-RETRAIT - PBN)}" fill="none" stroke="${C.dim}" stroke-width="0.8" stroke-dasharray="4 3"/>`);
  }
}
for (const [a, b] of [XS.c1, XS.c2, XS.c3, XS.c4])
  g.push(`<rect x="${px(a)}" y="${py(-0.55)}" width="${wm(b - a)}" height="${wm(0.55)}" fill="${C.beton}"/>`);
for (const bay of [XS.bayA, XS.bayB]) for (const [a, b] of doors(bay)) {
  g.push(`<rect x="${px(a)}" y="${py(-0.32)}" width="${wm(b - a)}" height="${wm(0.34)}" fill="#FFFFFF"/>`);
  g.push(`<rect x="${px(a)}" y="${py(-0.20)}" width="${wm((b - a) / 2)}" height="${wm(0.07)}" fill="${C.accent}"/>`);
  g.push(`<rect x="${px(a + (b - a) / 2)}" y="${py(-0.07)}" width="${wm((b - a) / 2)}" height="${wm(0.07)}" fill="${C.accent}"/>`);
  g.push(txt(px((a + b) / 2), py(-0.42), 'PB 1.80 × 2.20', { size: 8.5, fill: C.dim, ls: '0.08em', weight: 700 }));
}
// ---- vide central : fente de 1,80, deux balcons au fond, brise-vue entre eux
// Corrige les 23.08 : le brise-vue fait 40 cm et separe deux petits balcons de
// 0,70 x 0,80 m ; leur garde-corps verre s'arrete a 0,70 m en arriere du nu, la
// fente reste ouverte devant — c'est le « vide » de la facade.
{
  const [n1, n2] = XS.vide, a = AXE, back = -RETRAIT - 0.30;
  const half = [[n1, a - BV_EP / 2], [a + BV_EP / 2, n2]];
  for (const [h1, h2] of half) {
    const c = (h1 + h2) / 2;
    // dalle du balcon : de la porte (a 1,50) jusqu'a 0,70 du nu
    g.push(`<rect x="${px(h1)}" y="${py(-RETRAIT)}" width="${wm(h2 - h1)}" height="${wm(BALCON_NICHE_P)}" fill="${C.dalle}"/>`);
    g.push(`<rect x="${px(h1)}" y="${py(-RETRAIT)}" width="${wm(h2 - h1)}" height="${wm(BALCON_NICHE_P)}" fill="none" stroke="${C.dim}" stroke-width="0.7"/>`);
    // refend de fond + porte-fenetre depuis le logement
    g.push(`<rect x="${px(h1)}" y="${py(back)}" width="${wm(h2 - h1)}" height="${wm(0.30)}" fill="${C.beton}"/>`);
    g.push(`<rect x="${px(c - PBN / 2)}" y="${py(back)}" width="${wm(PBN)}" height="${wm(0.32)}" fill="#FFFFFF"/>`);
    g.push(`<rect x="${px(c - PBN / 2)}" y="${py(back + 0.12)}" width="${wm(PBN)}" height="${wm(0.06)}" fill="${C.accent}"/>`);
    g.push(`<path d="M ${px(c - PBN / 2)} ${py(-RETRAIT)} A ${wm(PBN)} ${wm(PBN)} 0 0 ${c < a ? 0 : 1} ${px(c + (c < a ? -PBN / 2 : PBN / 2))} ${py(-RETRAIT - PBN)}" fill="none" stroke="${C.dim}" stroke-width="0.8" stroke-dasharray="4 3"/>`);
    // garde-corps verre feuillete, a 0,70 m en arriere du nu
    g.push(`<rect x="${px(h1 + 0.02)}" y="${py(-GCN) - wm(0.06)}" width="${wm(h2 - h1 - 0.04)}" height="${wm(0.06)}" fill="${C.glass}"/>`);
    g.push(`<rect x="${px(h1 + 0.02)}" y="${py(-GCN) - wm(0.06)}" width="${wm(h2 - h1 - 0.04)}" height="${wm(0.06)}" fill="none" stroke="${C.inox}" stroke-width="0.8"/>`);
  }
  // le brise-vue : 40 cm sur l'axe, du fond de la fente au garde-corps
  g.push(`<rect x="${px(a - BV_EP / 2)}" y="${py(-RETRAIT)}" width="${wm(BV_EP)}" height="${wm(BALCON_NICHE_P)}" fill="${C.accent}"/>`);
  for (let d = 0.06; d < BALCON_NICHE_P - 0.03; d += 0.13)
    g.push(`<rect x="${px(a - BV_EP / 2)}" y="${py(-RETRAIT + d)}" width="${wm(BV_EP)}" height="${wm(0.05)}" fill="#FFFFFF" opacity="0.38"/>`);
  // cotes du vide
  const yd = py(0.30);
  g.push(dimH(px(n1), px(a - BV_EP / 2), yd, BALCON_NICHE.toFixed(2), { size: 8 }));
  g.push(dimH(px(a - BV_EP / 2), px(a + BV_EP / 2), yd, BV_EP.toFixed(2), { size: 8 }));
  g.push(dimH(px(a + BV_EP / 2), px(n2), yd, BALCON_NICHE.toFixed(2), { size: 8 }));
  g.push(dimV(py(-RETRAIT), py(-GCN), px(a) - wm(1.02), BALCON_NICHE_P.toFixed(2), { size: 9 }));
  g.push(dimV(py(-GCN), py(0), px(a) - wm(1.02), GCN.toFixed(2), { size: 9 }));
}

// ---- cartouche du vide central, dans le creux entre les deux rives -------
{
  const cx = px(AXE), y0 = py(2.06);
  g.push(`<path d="M ${cx} ${py(0.06)} L ${cx} ${y0 - 13}" stroke="${C.dim}" stroke-width="0.8" stroke-dasharray="4 3"/>`);
  g.push(`<circle cx="${cx}" cy="${py(0.06)}" r="2.4" fill="${C.dim}"/>`);
  const rows = [
    ['VIDE CENTRAL — FENTE DE 1,80 CREUSÉE DE 1,50', C.ink, 8.5],
    ['2 petits balcons de 0,70 × 0,80 m, un par logement', C.dim, 8],
    ['Brise-vue RAL 7024 de 40 cm sur l’axe, entre les deux', C.accent, 8],
    ['Garde-corps verre à 0,70 m en arrière du nu ; porte 0,70 m', C.dim, 8],
  ];
  rows.forEach(([t, col, sz], i) => g.push(txt(cx, y0 + i * 15, t, { size: sz, fill: col, ls: i ? '0.02em' : '0.1em', weight: i ? 600 : 700 })));
}

g.push(txt(px(3.925), py(-1.55), 'LOGEMENT', { size: 10, fill: C.dim, ls: '0.18em', weight: 700 }));
g.push(txt(px(13.575), py(-1.55), 'LOGEMENT', { size: 10, fill: C.dim, ls: '0.18em', weight: 700 }));

// ---- cotes ---------------------------------------------------------------
const yc = py(DMAX) + 78;
[[0, 0.55, '0.55'], [0.55, 1.45, '0.90'], [1.45, 3.25, '1.80'], [3.25, 4.60, '1.35'],
 [4.60, 6.40, '1.80'], [6.40, 7.30, '0.90'], [7.30, 7.85, '0.55'], [7.85, 9.65, '1.80'],
 [9.65, 10.20, '0.55'], [10.20, 11.10, '0.90'], [11.10, 12.90, '1.80'], [12.90, 14.25, '1.35'],
 [14.25, 16.05, '1.80'], [16.05, 16.95, '0.90'], [16.95, 17.50, '0.55']]
  .forEach(([a, b, t]) => g.push(dimH(px(a), px(b), yc, t, { size: 9.5 })));
g.push(dimH(px(0), px(17.5), yc + 42, '17.50', { size: 13, weight: 700 }));
g.push(dimV(py(0), py(DMAX), px(-0.30), DMAX.toFixed(2), { size: 10 }));
g.push(dimV(py(0), py(DCREUX), px(-0.90), '0.80', { size: 10 }));
g.push(dimV(py(-RETRAIT), py(0), px(8.75) - wm(1.35), '1.50', { size: 10 }));
g.push(txt(0, 0, 'PROFONDEUR DE BALCON', { size: 8.5, fill: C.dim, ls: '0.14em', weight: 700, transform: `translate(${px(-1.35)} ${py(0.8)}) rotate(-90)` }));

// reperes
const note = (m, dT, dL, label, col) => {
  g.push(`<path d="M ${px(m)} ${py(dT)} L ${px(m)} ${py(dL + 0.09)}" stroke="${C.ink}" stroke-width="0.8"/>`);
  g.push(`<circle cx="${px(m)}" cy="${py(dT)}" r="2.4" fill="${C.ink}"/>`);
  g.push(txt(px(m), py(dL), label, { size: 8.5, fill: col ?? C.dim, ls: '0.1em', weight: 700 }));
};
note(11.61, depthAt(11.61, 1) - 0.06, 0.40, 'GRAND LOBE — PROF. 1.80 m');
note(13.57, depthAt(13.57, 1) - 0.06, 0.30, 'CREUX MEDIAN — PROF. 0.79 m');
note(15.29, depthAt(15.29, 1) - 0.06, 0.40, 'PETIT LOBE — PROF. 1.10 m');
note(3.925, depthAt(3.925, 0) - 0.06, 0.66, 'BLOC GAUCHE = MIROIR DU BLOC DROIT');
g.push(txt(px(1.30), py(0.34), 'GORGE LED + BANDEAU AQUAPANEL 18 cm', { size: 8.5, fill: C.led, ls: '0.1em', weight: 700, anchor: 'start' }));

// legende du garde-corps
{
  const segs = gcSegments(1);
  const nv = segs.filter((s) => s.kind === 'verre').length;
  const ni = segs.filter((s) => s.kind === 'inox').length;
  const pas = segs[0].ml, lv = nv * pas, li = ni * pas;
  const bx = px(0), by = py(DMAX) + 132;
  g.push(txt(bx, by, 'GARDE-CORPS MIXTE', { size: 9.5, anchor: 'start', fill: C.ink, ls: '0.16em', weight: 700 }));
  const row = (dy, draw, t1, t2) => {
    g.push(draw(bx + 12, by + dy));
    g.push(txt(bx + 40, by + dy + 3, t1, { size: 9.5, anchor: 'start', fill: C.ink, weight: 600 }));
    g.push(txt(bx + 40, by + dy + 16, t2, { size: 8.5, anchor: 'start', fill: C.dim, weight: 500 }));
  };
  row(26, (x, y) => `<line x1="${x - 10}" y1="${y}" x2="${x + 12}" y2="${y}" stroke="${C.glass}" stroke-width="6.5" stroke-linecap="round"/><line x1="${x - 10}" y1="${y}" x2="${x + 12}" y2="${y}" stroke="#EAF2F3" stroke-width="2"/>`,
    'Verre feuilleté 8.8.4 — panneaux de 40 cm', `${nv} panneaux plats de ${(pas * 100).toFixed(0)} cm par bloc — ${lv.toFixed(2)} ml`);
  row(60, (x, y) => `<line x1="${x - 10}" y1="${y}" x2="${x + 12}" y2="${y}" stroke="${C.inox}" stroke-width="2"/>` +
    [0, 6, 12, 18].map((d) => `<circle cx="${x - 9 + d}" cy="${y}" r="2.5" fill="${C.inox}"/>`).join(''),
    'Barreaudage inox Ø 16 — sections de 40 cm', `${ni} sections de ${(pas * 100).toFixed(0)} cm, en alternance — ${li.toFixed(2)} ml`);
}

const body = `<div style="width: ${W}px; background: #FFFFFF">
${header({ w: W, kicker: 'Plan · niveau courant R+3 à R+8',
  title: 'Onde de rive relevée', sub: `Tracé corrigé sur votre trait noir du 23.08 : la rive quitte le poteau perpendiculairement au nu — elle naît sur la façade comme un demi-cercle — creuse un grand lobe de 1,80 m, remonte à 0,79 m entre les deux portes, creuse un petit lobe de 1,10 m, puis revient au nu de la même façon. Développé ${developpe().toFixed(2)} ml par balcon. Le bloc gauche est le miroir du bloc droit. Garde-corps en alternance 40 cm de verre / 40 cm d'inox sur tout le développé.`,
  right: 'A3 PAYSAGE · ÉCHELLE 1:50<br>COTES EN MÈTRES<br>TRACÉ RETENU' })}
<svg viewBox="0 0 ${W} ${SVGH}" width="${W}" height="${SVGH}" xmlns="http://www.w3.org/2000/svg" style="display: block">${g.join('\n')}</svg>
</div>`;
writeFileSync('Plan-Balcon.dc.html', page({ body, props: JSON.stringify({ $preview: { width: W, height: SVGH + 200 } }) }));
console.log('Plan-Balcon.dc.html ok');
