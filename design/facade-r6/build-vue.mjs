import { writeFileSync } from 'node:fs';
import { page, header } from './page.mjs';
import { txt } from './svgkit.mjs';

const W = 900, H = 1124, CX = 450;
const P = { wall: '#E6DDCD', wallSh: '#CFC2AA', deep: '#3A342C', pier: '#F0E9DC',
  aqua: '#FCFAF6', aquaSh: '#D7CFC2', soffit: '#C4BAA9',
  accent: '#8A6E4C', accentDark: '#4E3F2C', glass: '#9FB4B8', inox: '#C8CED0' };

// abscisses en fraction de la largeur de facade (17.50 m)
const U = (m) => m / 17.5;
const PIERS = [[0, .55], [7.30, 7.85], [9.65, 10.20], [16.95, 17.50]].map(([a, b]) => [U(a), U(b)]);
const BLOCKS = [[U(0), U(7.85)], [U(9.65), U(17.5)]];
const VOID = [U(7.85), U(9.65)];
const DOORS = [[1.45, 3.25], [4.60, 6.40], [11.10, 12.90], [14.25, 16.05]].map(([a, b]) => [U(a), U(b)]);

// niveaux en contre-plongee : plus on monte, plus l'onde s'aplatit
const L = [
  { y: 772, hw: 374, A: 42, T: 21, B: 22, gc: 30, name: 'R+2', podium: true },
  { y: 620, hw: 353, A: 35, T: 18, B: 18, gc: 26, name: 'R+3' },
  { y: 494, hw: 335, A: 29, T: 16, B: 15, gc: 22, name: 'R+4' },
  { y: 390, hw: 319, A: 24, T: 14, B: 12, gc: 19, name: 'R+5' },
  { y: 304, hw: 305, A: 19, T: 12, B: 10, gc: 16, name: 'R+6' },
];
const ROOF = { y: 238, hw: 293 }, TOP = { y: 210, hw: 289 };

const sx = (u, hw) => +(CX + (u - 0.5) * 2 * hw).toFixed(2);
const bulge = (t, n = 2) => (1 - Math.cos(2 * Math.PI * n * t)) / 2;

function rive(u1, u2, lv, N = 128, lobes = 2) {
  const top = [], bot = [];
  for (let j = 0; j <= N; j++) {
    const t = j / N, u = u1 + (u2 - u1) * t, b = bulge(t, lobes);
    const x = sx(u, lv.hw), yt = lv.y + lv.A * b;
    top.push([x, +yt.toFixed(2)]);
    bot.push([x, +(yt + lv.T + lv.B * b).toFixed(2)]);
  }
  return { top, bot };
}
const poly = (pts) => pts.map(([x, y], i) => `${i ? 'L' : 'M'} ${x} ${y}`).join(' ');
const band = (r) => `${poly(r.top)} L ${r.bot[r.bot.length - 1][0]} ${r.bot[r.bot.length - 1][1]} ${poly(r.bot.slice().reverse()).slice(1)} Z`;

const g = [];
g.push(`<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0.25" y2="1">
    <stop offset="0" stop-color="#5C8FBF"/><stop offset="0.42" stop-color="#8FB6D6"/>
    <stop offset="0.78" stop-color="#C7D9E4"/><stop offset="1" stop-color="#E5E4DC"/>
  </linearGradient>
  <linearGradient id="aqg" x1="0" y1="0" x2="0.1" y2="1">
    <stop offset="0" stop-color="${P.aqua}"/><stop offset="0.45" stop-color="#F0EBE1"/><stop offset="1" stop-color="${P.aquaSh}"/>
  </linearGradient>
  <linearGradient id="sof" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="${P.soffit}"/><stop offset="1" stop-color="#9E9382"/>
  </linearGradient>
  <linearGradient id="glg" x1="0" y1="0" x2="0.3" y2="1">
    <stop offset="0" stop-color="#E4EDEE" stop-opacity="0.9"/><stop offset="1" stop-color="${P.glass}" stop-opacity="0.5"/>
  </linearGradient>
  <linearGradient id="wallg" x1="0" y1="0" x2="0.2" y2="1">
    <stop offset="0" stop-color="${P.wall}"/><stop offset="1" stop-color="${P.wallSh}"/>
  </linearGradient>
</defs>`);

g.push(`<rect x="0" y="0" width="${W}" height="${H}" fill="url(#sky)"/>`);

// ---- volume general : trapeze de la tour ---------------------------------
const bot = L[0];
g.push(`<path d="M ${sx(0, TOP.hw)} ${TOP.y} L ${sx(1, TOP.hw)} ${TOP.y} L ${sx(1, bot.hw)} ${bot.y + 120} L ${sx(0, bot.hw)} ${bot.y + 120} Z" fill="url(#wallg)"/>`);

// ---- vide central : lames verticales bronze ------------------------------
g.push(`<path d="M ${sx(VOID[0], TOP.hw)} ${TOP.y} L ${sx(VOID[1], TOP.hw)} ${TOP.y} L ${sx(VOID[1], bot.hw)} ${bot.y + 40} L ${sx(VOID[0], bot.hw)} ${bot.y + 40} Z" fill="${P.deep}"/>`);
for (let k = 0; k <= 11; k++) {
  const u = VOID[0] + (VOID[1] - VOID[0]) * (k + 0.5) / 12;
  g.push(`<line x1="${sx(u, TOP.hw)}" y1="${TOP.y}" x2="${sx(u, bot.hw)}" y2="${bot.y + 40}" stroke="${P.accent}" stroke-width="3" opacity="0.9"/>`);
  g.push(`<line x1="${sx(u, TOP.hw) + 1.6}" y1="${TOP.y}" x2="${sx(u, bot.hw) + 2}" y2="${bot.y + 40}" stroke="${P.accentDark}" stroke-width="1.4" opacity="0.9"/>`);
}

// ---- du plus lointain (haut) au plus proche (bas) -------------------------
for (let i = L.length - 1; i >= 0; i--) {
  const lv = L[i], up = i < L.length - 1 ? L[i + 1] : ROOF;
  const hwW = lv.hw * 0.945;                       // plan de facade, en retrait

  // paroi en retrait + menuiseries
  const yTopWall = (up.y ?? ROOF.y) + (up.T ?? 8) + 4, yBotWall = lv.y + lv.A * 0.15;
  for (const [w1, w2] of BLOCKS)
    g.push(`<path d="M ${sx(w1, up.hw * 0.945)} ${yTopWall} L ${sx(w2, up.hw * 0.945)} ${yTopWall} L ${sx(w2, hwW)} ${yBotWall} L ${sx(w1, hwW)} ${yBotWall} Z" fill="${P.wallSh}" opacity="0.92"/>`);
  for (const [u1, u2] of DOORS) {
    const a1 = sx(u1, hwW), a2 = sx(u2, hwW), b1 = sx(u1, up.hw * 0.945), b2 = sx(u2, up.hw * 0.945);
    g.push(`<path d="M ${b1} ${yTopWall + 5} L ${b2} ${yTopWall + 5} L ${a2} ${yBotWall - 3} L ${a1} ${yBotWall - 3} Z" fill="#2C3234"/>`);
    g.push(`<path d="M ${b1} ${yTopWall + 5} L ${b2} ${yTopWall + 5} L ${a2} ${yBotWall - 3} L ${a1} ${yBotWall - 3} Z" fill="none" stroke="${P.accent}" stroke-width="1.6"/>`);
    g.push(`<line x1="${(b1 + b2) / 2}" y1="${yTopWall + 5}" x2="${(a1 + a2) / 2}" y2="${yBotWall - 3}" stroke="${P.accent}" stroke-width="1.3" opacity="0.85"/>`);
  }
  // poteaux
  for (const [u1, u2] of PIERS)
    g.push(`<path d="M ${sx(u1, up.hw)} ${up.y} L ${sx(u2, up.hw)} ${up.y} L ${sx(u2, lv.hw)} ${lv.y + lv.A + 26} L ${sx(u1, lv.hw)} ${lv.y + lv.A + 26} Z" fill="${P.pier}" opacity="0.96"/>`);

  // garde-corps verre + inox (derriere la rive)
  if (!lv.podium) for (const [u1, u2] of BLOCKS) {
    const r = rive(u1, u2, lv);
    const gcTop = r.top.map(([x, y]) => [x, +(y - lv.gc).toFixed(2)]);
    g.push(`<path d="${poly(gcTop)} L ${r.top[r.top.length - 1][0]} ${r.top[r.top.length - 1][1]} ${poly(r.top.slice().reverse()).slice(1)} Z" fill="url(#glg)"/>`);
    g.push(`<path d="${poly(gcTop)}" fill="none" stroke="${P.inox}" stroke-width="2.6"/>`);
    g.push(`<path d="${poly(gcTop.map(([x, y]) => [x, y + 1.2]))}" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.8"/>`);
  }
  // rive ondulee : sous-face + bandeau Aquapanel
  if (!lv.podium) for (const [u1, u2] of BLOCKS) {
    const r = rive(u1, u2, lv);
    const under = r.bot.map(([x, y]) => [x, +(y + lv.T * 0.5 + lv.B * 0.55).toFixed(2)]);
    g.push(`<path d="${poly(r.bot)} L ${under[under.length - 1][0]} ${under[under.length - 1][1]} ${poly(under.slice().reverse()).slice(1)} Z" fill="url(#sof)"/>`);
    g.push(`<path d="${band(r)}" fill="url(#aqg)"/>`);
    g.push(`<path d="${poly(r.top)}" fill="none" stroke="#FFFFFF" stroke-width="1.4" opacity="0.85"/>`);
    g.push(`<path d="${poly(r.bot)}" fill="none" stroke="${P.aquaSh}" stroke-width="1.2"/>`);
  }
}

// ---- couronnement --------------------------------------------------------
g.push(`<path d="M ${sx(0, TOP.hw)} ${TOP.y} L ${sx(1, TOP.hw)} ${TOP.y} L ${sx(1, ROOF.hw)} ${ROOF.y} L ${sx(0, ROOF.hw)} ${ROOF.y} Z" fill="${P.pier}"/>`);
g.push(`<path d="M ${sx(0, TOP.hw)} ${TOP.y} L ${sx(1, TOP.hw)} ${TOP.y} L ${sx(1, TOP.hw)} ${TOP.y + 7} L ${sx(0, TOP.hw)} ${TOP.y + 7} Z" fill="${P.accent}"/>`);

// ---- socle parking, au premier plan --------------------------------------
const pTop = 838, pBot = H, pHwT = 404, pHwB = 468;
g.push(`<path d="M ${sx(0, pHwT)} ${pTop} L ${sx(1, pHwT)} ${pTop} L ${sx(1, pHwB)} ${pBot} L ${sx(0, pHwB)} ${pBot} Z" fill="#CFC3AC"/>`);
g.push(`<path d="M ${sx(0, pHwT)} ${pTop} L ${sx(1, pHwT)} ${pTop} L ${sx(1, pHwT)} ${pTop + 9} L ${sx(0, pHwT)} ${pTop + 9} Z" fill="#B4A78F"/>`);
for (let k = 0; k < 5; k++) {
  const yy = pTop + 28 + k * 22, f = (yy - pTop) / (pBot - pTop), hw = pHwT + (pHwB - pHwT) * f;
  for (const [u1, u2] of [[U(0.55), U(7.30)], [U(7.85), U(9.65)], [U(10.20), U(16.95)]])
    g.push(`<line x1="${sx(u1, hw)}" y1="${yy}" x2="${sx(u2, hw)}" y2="${yy}" stroke="${P.accent}" stroke-width="6" opacity="${0.92 - k * 0.03}"/>`);
}
// garde-corps de la terrasse R+2, sur l'acrotere du parking
{
  const r = rive(0, 1, { ...L[0], hw: pHwT, A: 34, T: 17, B: 16 }, 160, 4);
  const gcTop = r.top.map(([x, y]) => [x, +(y - 34).toFixed(2)]);
  g.push(`<path d="${poly(gcTop)} L ${r.top[r.top.length - 1][0]} ${r.top[r.top.length - 1][1]} ${poly(r.top.slice().reverse()).slice(1)} Z" fill="url(#glg)"/>`);
  g.push(`<path d="${poly(gcTop)}" fill="none" stroke="${P.inox}" stroke-width="3"/>`);
  g.push(`<path d="${band(r)}" fill="url(#aqg)"/>`);
  const under = r.bot.map(([x, y]) => [x, y + 13]);
  g.push(`<path d="${poly(r.bot)} L ${under[under.length - 1][0]} ${under[under.length - 1][1]} ${poly(under.slice().reverse()).slice(1)} Z" fill="url(#sof)"/>`);
}

// bandeau alu + portes de garage au RDC
{
  const yb = pTop + 156, f = (yb - pTop) / (pBot - pTop), hw = pHwT + (pHwB - pHwT) * f;
  g.push(`<rect x="${sx(0, hw) - 6}" y="${yb}" width="${2 * hw + 12}" height="9" fill="${P.accent}"/>`);
  g.push(`<path d="M ${sx(0, hw)} ${yb + 9} L ${sx(1, hw)} ${yb + 9} L ${sx(1, pHwB)} ${pBot} L ${sx(0, pHwB)} ${pBot} Z" fill="#B7AB94"/>`);
  for (const [u1, u2] of [[U(1.40), U(6.60)], [U(10.90), U(16.10)]]) {
    g.push(`<path d="M ${sx(u1, hw)} ${yb + 22} L ${sx(u2, hw)} ${yb + 22} L ${sx(u2, pHwB)} ${pBot - 14} L ${sx(u1, pHwB)} ${pBot - 14} Z" fill="${P.accentDark}"/>`);
    for (let k = 1; k < 4; k++) {
      const yy = yb + 22 + k * 22, ff = (yy - pTop) / (pBot - pTop), h2 = pHwT + (pHwB - pHwT) * ff;
      g.push(`<line x1="${sx(u1, h2)}" y1="${yy}" x2="${sx(u2, h2)}" y2="${yy}" stroke="${P.accent}" stroke-width="1.6" opacity="0.7"/>`);
    }
  }
  g.push(`<path d="M ${sx(VOID[0], hw)} ${yb + 16} L ${sx(VOID[1], hw)} ${yb + 16} L ${sx(VOID[1], pHwB)} ${pBot - 14} L ${sx(VOID[0], pHwB)} ${pBot - 14} Z" fill="#E8D9BC"/>`);
  g.push(`<rect x="0" y="${pBot - 14}" width="${W}" height="14" fill="#9C917E"/>`);
}

// contexte : mur de soutenement et talus qui enserrent la venelle
g.push(`<path d="M 0 ${H} L 0 ${H - 210} C 52 ${H - 188} 84 ${H - 128} 96 ${H} Z" fill="#2E2A24" opacity="0.30"/>`);
g.push(`<path d="M ${W} ${H} L ${W} ${H - 250} C ${W - 62} ${H - 214} ${W - 96} ${H - 120} ${W - 108} ${H} Z" fill="#2E2A24" opacity="0.26"/>`);

// ---- reperes ------------------------------------------------------------
L.forEach((lv) => {
  const x = sx(1, lv.hw) + 16;
  g.push(`<line x1="${sx(1, lv.hw) + 4}" y1="${lv.y + lv.A * 0.2}" x2="${x + 4}" y2="${lv.y + lv.A * 0.2}" stroke="#2B2724" stroke-width="0.8" opacity="0.5"/>`);
  g.push(txt(x + 10, lv.y + lv.A * 0.2 + 4, lv.name, { size: 10, anchor: 'start', weight: 600, fill: '#3A352E', ls: '0.1em' }));
});

const body = `<div style="width: ${W}px; background: #F1EDE5">
${header({ w: W, kicker: 'Ambiance · vue depuis la venelle', title: 'Rives ondulées',
  sub: 'Contre-plongée depuis le pied de l’immeuble — lecture des bandeaux cintrés en Aquapanel, du filtre bronze du vide central et du socle parking.',
  right: 'VUE D’AMBIANCE<br>NON COTÉE<br>VARIANTE A' })}
<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" xmlns="http://www.w3.org/2000/svg" style="display: block">${g.join('\n')}</svg>
</div>`;

writeFileSync('Vue.dc.html', page({ body, props: JSON.stringify({ $preview: { width: W, height: H + 190 } }) }));
console.log('Vue.dc.html ok');
