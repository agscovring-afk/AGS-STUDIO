import { writeFileSync } from 'node:fs';
import { XS, LV, BLOCS, MIROIR, DMIN, DCREUX, DMAX, COL, RETRAIT, PBW, PBH,
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

// ---- niche centrale, creusee de 1,50 m ----------------------------------
g.push(`<rect x="${px(XS.vide[0])}" y="${py(-RETRAIT)}" width="${wm(1.80)}" height="${wm(RETRAIT)}" fill="${C.niche}"/>`);
g.push(`<rect x="${px(XS.vide[0])}" y="${py(-RETRAIT)}" width="${wm(1.80)}" height="${wm(0.30)}" fill="${C.beton}"/>`);
for (const x of [XS.vide[0], XS.vide[1] - 0.30])
  g.push(`<rect x="${px(x)}" y="${py(-RETRAIT)}" width="${wm(0.30)}" height="${wm(RETRAIT)}" fill="${C.beton}"/>`);
// deux balcons en vis-a-vis sur les joues de la niche
for (const [x, s] of [[XS.vide[0] + 0.30, 1], [XS.vide[1] - 0.30, -1]]) {
  g.push(`<rect x="${px(s > 0 ? x : x - 0.10)}" y="${py(-1.28)}" width="${wm(0.10)}" height="${wm(0.90)}" fill="#FFFFFF"/>`);
  g.push(`<rect x="${px(s > 0 ? x : x - 0.06)}" y="${py(-1.24)}" width="${wm(0.06)}" height="${wm(0.82)}" fill="${C.accent}"/>`);
}
g.push(txt(0, 0, 'NICHE 1.80 × 1.50 — 2 LOGEMENTS EN VIS-A-VIS', { size: 8.5, fill: C.dim, ls: '0.1em', weight: 700, transform: `translate(${px(8.75) + 4} ${py(-0.72)}) rotate(90)` }));
// brise-vue au nu de facade
for (let x = XS.vide[0] + 0.08; x < XS.vide[1]; x += 0.15)
  g.push(`<rect x="${px(x)}" y="${py(0) - wm(0.08)}" width="${wm(0.05)}" height="${wm(0.08)}" fill="${C.accent}"/>`);

// ---- mur de facade, poteaux, menuiseries ---------------------------------
for (const [m1, m2] of BLOCS) {
  g.push(`<rect x="${px(m1)}" y="${py(-1.75)}" width="${wm(m2 - m1)}" height="${wm(1.45)}" fill="${C.int}"/>`);
  g.push(`<rect x="${px(m1)}" y="${py(-0.30)}" width="${wm(m2 - m1)}" height="${wm(0.30)}" fill="${C.beton}"/>`);
}
for (const [a, b] of [XS.c1, XS.c2, XS.c3, XS.c4])
  g.push(`<rect x="${px(a)}" y="${py(-0.55)}" width="${wm(b - a)}" height="${wm(0.55)}" fill="${C.beton}"/>`);
for (const bay of [XS.bayA, XS.bayB]) for (const [a, b] of doors(bay)) {
  g.push(`<rect x="${px(a)}" y="${py(-0.32)}" width="${wm(b - a)}" height="${wm(0.34)}" fill="#FFFFFF"/>`);
  g.push(`<rect x="${px(a)}" y="${py(-0.20)}" width="${wm((b - a) / 2)}" height="${wm(0.07)}" fill="${C.accent}"/>`);
  g.push(`<rect x="${px(a + (b - a) / 2)}" y="${py(-0.07)}" width="${wm((b - a) / 2)}" height="${wm(0.07)}" fill="${C.accent}"/>`);
  g.push(txt(px((a + b) / 2), py(-0.42), 'PB 1.80 × 2.20', { size: 8.5, fill: C.dim, ls: '0.08em', weight: 700 }));
}
g.push(txt(px(3.925), py(-1.15), 'LOGEMENT', { size: 10, fill: C.dim, ls: '0.18em', weight: 700 }));
g.push(txt(px(13.575), py(-1.15), 'LOGEMENT', { size: 10, fill: C.dim, ls: '0.18em', weight: 700 }));

// ---- cotes ---------------------------------------------------------------
const yc = py(DMAX) + 78;
[[0, 0.55, '0.55'], [0.55, 1.45, '0.90'], [1.45, 3.25, '1.80'], [3.25, 4.60, '1.35'],
 [4.60, 6.40, '1.80'], [6.40, 7.30, '0.90'], [7.30, 7.85, '0.55'], [7.85, 9.65, '1.80'],
 [9.65, 10.20, '0.55'], [10.20, 11.10, '0.90'], [11.10, 12.90, '1.80'], [12.90, 14.25, '1.35'],
 [14.25, 16.05, '1.80'], [16.05, 16.95, '0.90'], [16.95, 17.50, '0.55']]
  .forEach(([a, b, t]) => g.push(dimH(px(a), px(b), yc, t, { size: 9.5 })));
g.push(dimH(px(0), px(17.5), yc + 42, '17.50', { size: 13, weight: 700 }));
g.push(dimV(py(0), py(DMAX), px(-0.30), '1.60', { size: 10 }));
g.push(dimV(py(0), py(DCREUX), px(-0.90), '0.80', { size: 10 }));
g.push(dimV(py(-RETRAIT), py(0), px(8.75) - wm(1.35), '1.50', { size: 10 }));
g.push(txt(0, 0, 'PROFONDEUR DE BALCON', { size: 8.5, fill: C.dim, ls: '0.14em', weight: 700, transform: `translate(${px(-1.35)} ${py(0.8)}) rotate(-90)` }));

// reperes
const note = (m, dT, dL, label, col) => {
  g.push(`<path d="M ${px(m)} ${py(dT)} L ${px(m)} ${py(dL + 0.09)}" stroke="${C.ink}" stroke-width="0.8"/>`);
  g.push(`<circle cx="${px(m)}" cy="${py(dT)}" r="2.4" fill="${C.ink}"/>`);
  g.push(txt(px(m), py(dL), label, { size: 8.5, fill: col ?? C.dim, ls: '0.1em', weight: 700 }));
};
note(11.99, depthAt(11.85, 1) - 0.06, 0.40, 'GRAND LOBE Ø 1.80 — PROF. 0.90');
note(13.575, depthAt(13.55, 1) - 0.06, 0.30, 'PETIT LOBE Ø 1.10 — PROF. 0.55');
note(15.14, depthAt(15.90, 1) - 0.06, 0.40, 'GRAND LOBE Ø 1.80 — PROF. 0.90');
note(3.925, depthAt(3.925, 0) - 0.06, 0.66, 'BLOC GAUCHE = MIROIR DU BLOC DROIT');
g.push(txt(px(1.30), py(0.34), 'GORGE LED + BANDEAU AQUAPANEL 18 cm', { size: 8.5, fill: C.led, ls: '0.1em', weight: 700, anchor: 'start' }));

// legende du garde-corps
{
  const segs = gcSegments(1);
  const lv = segs.filter((s) => s.kind === 'verre').reduce((a, s) => a + s.x2 - s.x1, 0);
  const li = segs.filter((s) => s.kind === 'inox').reduce((a, s) => a + s.x2 - s.x1, 0);
  const bx = px(0), by = py(DMAX) + 132;
  g.push(txt(bx, by, 'GARDE-CORPS MIXTE', { size: 9.5, anchor: 'start', fill: C.ink, ls: '0.16em', weight: 700 }));
  const row = (dy, draw, t1, t2) => {
    g.push(draw(bx + 12, by + dy));
    g.push(txt(bx + 40, by + dy + 3, t1, { size: 9.5, anchor: 'start', fill: C.ink, weight: 600 }));
    g.push(txt(bx + 40, by + dy + 16, t2, { size: 8.5, anchor: 'start', fill: C.dim, weight: 500 }));
  };
  row(26, (x, y) => `<line x1="${x - 10}" y1="${y}" x2="${x + 12}" y2="${y}" stroke="${C.glass}" stroke-width="6.5" stroke-linecap="round"/><line x1="${x - 10}" y1="${y}" x2="${x + 12}" y2="${y}" stroke="#EAF2F3" stroke-width="2"/>`,
    'Verre feuilleté bombé 8.8.4', `sur les portions droites de la rive — ${lv.toFixed(2)} m par bloc`);
  row(60, (x, y) => `<line x1="${x - 10}" y1="${y}" x2="${x + 12}" y2="${y}" stroke="${C.inox}" stroke-width="2"/>` +
    [0, 6, 12, 18].map((d) => `<circle cx="${x - 9 + d}" cy="${y}" r="2.5" fill="${C.inox}"/>`).join(''),
    'Barreaudage inox Ø 16', `aux creux et aux crêtes — ${li.toFixed(2)} m par bloc`);
}

const body = `<div style="width: ${W}px; background: #FFFFFF">
${header({ w: W, kicker: 'Plan · niveau courant R+3 à R+8',
  title: 'Onde de rive relevée', sub: `Tracé repris de votre croquis du 23.08 : la rive est tracée au compas : elle part du nu de façade au droit du poteau et décrit trois demi-cercles tangents — deux grands de Ø 1,80 m devant chaque porte-balcon, un petit de Ø 1,10 m entre les deux. Développé ${developpe().toFixed(2)} ml par balcon. Le bloc gauche est le miroir du bloc droit. La niche centrale de 1,80 m se creuse de 1,50 m en arrière du nu de façade.`,
  right: 'A3 PAYSAGE · ÉCHELLE 1:50<br>COTES EN MÈTRES<br>TRACÉ RETENU' })}
<svg viewBox="0 0 ${W} ${SVGH}" width="${W}" height="${SVGH}" xmlns="http://www.w3.org/2000/svg" style="display: block">${g.join('\n')}</svg>
</div>`;
writeFileSync('Plan-Balcon.dc.html', page({ body, props: JSON.stringify({ $preview: { width: W, height: SVGH + 200 } }) }));
console.log('Plan-Balcon.dc.html ok');
