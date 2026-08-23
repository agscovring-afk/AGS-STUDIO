import { writeFileSync } from 'node:fs';
import { XS, DMIN, DMAX, PBW, doors, depthAt, developpe, gcSegments } from './geo.mjs';
import { page, header } from './page.mjs';
import { txt, dimH, dimV } from './svgkit.mjs';

const W = 1120, H = 800, S = 88, X0 = 132, YF = 236;   // YF = nu de facade
const px = (m) => +(X0 + m * S).toFixed(2), py = (d) => +(YF + d * S).toFixed(2);
const wm = (m) => +(m * S).toFixed(2);
const C = { beton: '#4A443B', wall: '#E8E0D2', dalle: '#F2EDE3', aqua: '#FBF9F5', inox2: '#6E7A80',
  accent: '#8A6E4C', glass: '#A9BBBE', inox: '#8E969A', ink: '#23211E', dim: '#8C8478' };
const BAY = XS.bayA, D = doors(BAY);
const g = [];

// rive ondulee : onde sur l'ouverture libre, rive droite au droit des poteaux
const NP = 900;
const depthOf = (x) => (x < BAY[0] || x > BAY[1]) ? DMIN : depthAt((x - BAY[0]) / (BAY[1] - BAY[0]));
const rivePts = [];
for (let i = 0; i <= NP; i++) { const x = 7.85 * i / NP; rivePts.push([px(x), py(depthOf(x))]); }
const idx = (m) => Math.max(0, Math.min(NP, Math.round(m / 7.85 * NP)));
const rive = rivePts.map(([x, y], i) => `${i ? 'L' : 'M'} ${x.toFixed(2)} ${y.toFixed(2)}`).join(' ');
const off = (d) => rivePts.map(([x, y], i) => `${i ? 'L' : 'M'} ${x.toFixed(2)} ${(y - d).toFixed(2)}`).join(' ');
const offSlice = (d, i1, i2) => rivePts.slice(i1, i2 + 1).map(([x, y], i) => `${i ? 'L' : 'M'} ${x.toFixed(2)} ${(y - d).toFixed(2)}`).join(' ');

g.push(`<defs><linearGradient id="dl" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#EFEAE0"/><stop offset="1" stop-color="#E0D8C9"/></linearGradient></defs>`);
// dalle de balcon
g.push(`<path d="M ${px(0)} ${py(0)} ${rive.slice(1)} L ${px(7.85)} ${py(0)} Z" fill="url(#dl)"/>`);
g.push(`<path d="${rive}" fill="none" stroke="${C.ink}" stroke-width="2"/>`);
g.push(`<path d="${off(wm(0.18))}" fill="none" stroke="${C.dim}" stroke-width="1" stroke-dasharray="5 4"/>`);
// gorge LED, 5 cm en sous-face de la rive
g.push(`<path d="${off(wm(0.05))}" fill="none" stroke="#E0B45E" stroke-width="2" stroke-dasharray="9 5"/>`);
// garde-corps mixte inox / verre, a 10 cm en retrait de la rive
const GCOFF = wm(0.10);
for (const seg of gcSegments(0, 7.85)) {
  const i1 = idx(seg.x1), i2 = idx(seg.x2);
  if (seg.kind === 'verre') {
    g.push(`<path d="${offSlice(GCOFF, i1, i2)}" fill="none" stroke="${C.glass}" stroke-width="6.5" opacity="0.9" stroke-linecap="round"/>`);
    g.push(`<path d="${offSlice(GCOFF, i1, i2)}" fill="none" stroke="#E8F1F2" stroke-width="2" opacity="0.9"/>`);
  } else {
    g.push(`<path d="${offSlice(GCOFF, i1, i2)}" fill="none" stroke="${C.inox}" stroke-width="2"/>`);
    for (let m = seg.x1 + 0.055; m < seg.x2 - 0.03; m += 0.11) {
      const [bx, by] = rivePts[idx(m)];
      g.push(`<circle cx="${bx.toFixed(2)}" cy="${(by - GCOFF).toFixed(2)}" r="2.6" fill="${C.inox}"/>`);
    }
  }
  const [ex, ey] = rivePts[Math.min(NP, i2)];
  g.push(`<circle cx="${ex.toFixed(2)}" cy="${(ey - GCOFF).toFixed(2)}" r="4" fill="none" stroke="${C.inox}" stroke-width="2"/>`);
}
// mur de facade + menuiseries
g.push(`<rect x="${px(0)}" y="${py(0) - wm(0.30)}" width="${wm(7.85)}" height="${wm(0.30)}" fill="${C.beton}"/>`);
for (const [a, b] of [XS.c1, [7.30, 7.85]])
  g.push(`<rect x="${px(a)}" y="${py(0) - wm(0.55)}" width="${wm(b - a)}" height="${wm(0.55)}" fill="${C.beton}"/>`);
for (const [a, b] of D) {
  g.push(`<rect x="${px(a)}" y="${py(0) - wm(0.32)}" width="${wm(b - a)}" height="${wm(0.34)}" fill="#F1EDE5"/>`);
  g.push(`<rect x="${px(a)}" y="${py(0) - wm(0.20)}" width="${wm((b - a) / 2)}" height="${wm(0.09)}" fill="${C.accent}"/>`);
  g.push(`<rect x="${px(a + (b - a) / 2)}" y="${py(0) - wm(0.09)}" width="${wm((b - a) / 2)}" height="${wm(0.09)}" fill="${C.accent}"/>`);
  g.push(txt(px((a + b) / 2), py(0) - wm(0.44), 'PB 1.80', { size: 8.5, fill: C.dim, ls: '0.1em', weight: 700 }));
}
g.push(`<rect x="${px(0)}" y="${py(0) - wm(1.72)}" width="${wm(7.85)}" height="${wm(1.30)}" fill="#EDE7DA" opacity="0.7"/>`);
g.push(txt(px(3.925), py(0) - wm(1.05), 'SEJOUR / CHAMBRE', { size: 9.5, fill: C.dim, ls: '0.18em', weight: 700 }));
// brise-vue de separation en bout de balcon
g.push(`<rect x="${px(7.30)}" y="${py(0)}" width="${wm(0.09)}" height="${wm(DMIN)}" fill="${C.accent}"/>`);
// vide central + balcon en vis-a-vis
g.push(`<rect x="${px(7.85)}" y="${py(-1.72)}" width="${wm(1.80)}" height="${wm(DMIN + 1.72)}" fill="#EDE9E1"/>`);
g.push(`<rect x="${px(7.85)}" y="${py(-1.72)}" width="${wm(1.80)}" height="${wm(DMIN + 1.72)}" fill="none" stroke="${C.dim}" stroke-width="1" stroke-dasharray="6 4"/>`);
for (let x = 7.90; x < 9.65; x += 0.15) g.push(`<rect x="${px(x)}" y="${py(DMIN) - 8}" width="${wm(0.05)}" height="10" fill="${C.accent}"/>`);
g.push(txt(0, 0, 'VIDE CENTRAL 1.80', { size: 9, fill: C.dim, ls: '0.14em', weight: 700, transform: `translate(${px(8.75) + 4} ${py(-0.35)}) rotate(90)`, anchor: 'start' }));
g.push(dimH(px(7.85), px(9.65), py(-1.72) - 26, '1.80', { size: 10 }));
// annotations de rive, au-dessus des aplats
const note = (m, dTarget, dText, label, color) => {
  g.push(`<path d="M ${px(m)} ${py(dTarget)} L ${px(m)} ${py(dText + 0.10)}" stroke="${C.ink}" stroke-width="0.8"/>`);
  g.push(`<circle cx="${px(m)}" cy="${py(dTarget)}" r="2.4" fill="${C.ink}"/>`);
  g.push(txt(px(m), py(dText), label, { size: 8.5, fill: color ?? C.dim, ls: '0.1em', weight: 700 }));
};
note(1.35, depthOf(1.35), 0.52, 'BANDEAU AQUAPANEL CINTRE 18 cm + GORGE LED');
note(2.2375, DMAX - 0.10, 1.06, 'BARREAUDAGE INOX Ø 16 — RAYON DE RIVE 0,35 m', C.inox2);
note(5.10, depthOf(5.10) - 0.10, 0.52, 'VERRE FEUILLETE 8.8.4 — PANNEAU PLAT 1,09 m');
g.push(txt(px(7.22), py(DMIN) - 16, 'BRISE-VUE ALU — SEPARATION', { size: 8.5, fill: C.accent, ls: '0.1em', weight: 700, anchor: 'end' }));
g.push(txt(px(9.70), py(DMIN) + 30, 'BALCONS EN VIS-A-VIS DANS LE VIDE — VOIR FACADE', { size: 8.5, fill: C.dim, ls: '0.1em', weight: 700, anchor: 'end' }));

// cotes
const yc = py(DMAX) + 94;
const ch = [[0, 0.55, '0.55'], [0.55, 1.45, '0.90'], [1.45, 3.25, '1.80'], [3.25, 4.60, '1.35'],
            [4.60, 6.40, '1.80'], [6.40, 7.30, '0.90'], [7.30, 7.85, '0.55']];
ch.forEach(([a, b, t]) => g.push(dimH(px(a), px(b), yc, t, { size: 10 })));
g.push(dimH(px(0.55), px(7.30), yc + 46, '6.75 — ouverture libre', { size: 11.5, weight: 700 }));
g.push(dimH(px(0), px(7.85), yc + 88, '7.85 — largeur du bloc', { size: 11.5, weight: 700 }));
g.push(dimV(py(0), py(DMIN), px(-0.28), '1.30', { size: 10 }));
g.push(dimV(py(0), py(DMAX), px(-0.86), '3.00', { size: 10 }));
// repere du developpe
g.push(`<path d="M ${px(0.55)} ${py(DMAX) + 26} L ${px(7.30)} ${py(DMAX) + 26}" stroke="${C.accent}" stroke-width="2"/>`);
g.push(txt(px(3.925), py(DMAX) + 46, `RIVE ONDULEE — 2 ONDES · DEVELOPPE ${developpe().toFixed(2)} ml (≈ 10 ml relevés)`,
  { size: 9.5, fill: C.accent, ls: '0.1em', weight: 700 }));

{
  const bx = px(8.05), by = py(DMAX) + 30;
  g.push(`<rect x="${bx}" y="${by}" width="270" height="128" fill="#F7F4ED" stroke="#D3C9B7" stroke-width="1"/>`);
  g.push(txt(bx + 16, by + 24, 'GARDE-CORPS MIXTE', { size: 9.5, anchor: 'start', fill: C.ink, ls: '0.16em', weight: 700 }));
  const row = (dy, draw, t1, t2) => {
    g.push(draw(bx + 20, by + dy));
    g.push(txt(bx + 46, by + dy + 3, t1, { size: 9.5, anchor: 'start', fill: C.ink, weight: 600 }));
    g.push(txt(bx + 46, by + dy + 16, t2, { size: 8.5, anchor: 'start', fill: C.dim, weight: 500 }));
  };
  row(48, (x, y) => `<line x1="${x - 8}" y1="${y}" x2="${x + 12}" y2="${y}" stroke="${C.glass}" stroke-width="6.5" stroke-linecap="round"/><line x1="${x - 8}" y1="${y}" x2="${x + 12}" y2="${y}" stroke="#E8F1F2" stroke-width="2"/>`,
      'Verre feuilleté 8.8.4', '4 panneaux plats de 1,09 m — 4,35 m par bloc');
  row(88, (x, y) => `<line x1="${x - 8}" y1="${y}" x2="${x + 12}" y2="${y}" stroke="${C.inox}" stroke-width="2"/>` +
      [0, 5, 10].map((d) => `<circle cx="${x - 6 + d * 1.8}" cy="${y}" r="2.6" fill="${C.inox}"/>`).join(''),
      'Barreaudage inox Ø 16', '5 sections aux creux et crêtes — 3,50 m par bloc');
}

const body = `<div style="width: ${W}px; background: #F1EDE5">
${header({ w: W, kicker: 'Plan · balcon type (bloc gauche)', title: 'Onde de rive &amp; portes-balcon',
  sub: 'Ouverture libre 6,75 m entre nus de poteaux, deux portes-balcon aluminium de 1,80 m. La rive décrit deux ondes, de 1,30 m au creux à 3,00 m à la crête — développé ' + developpe().toFixed(2) + ' ml. Le garde-corps suit exactement ce tracé : barreaudage inox là où le rayon tombe à 0,35 m, verre feuilleté plat sur les portions quasi droites.',
  right: 'ÉCHELLE 1:50<br>COTES EN MÈTRES<br>BLOC DROIT SYMÉTRIQUE' })}
<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" xmlns="http://www.w3.org/2000/svg" style="display: block">${g.join('\n')}</svg>
</div>`;
writeFileSync('Plan-Balcon.dc.html', page({ body, props: JSON.stringify({ $preview: { width: W, height: H + 200 } }) }));
console.log('Plan-Balcon.dc.html ok');
