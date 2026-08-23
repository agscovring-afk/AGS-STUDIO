import { writeFileSync } from 'node:fs';
import { page, header } from './page.mjs';
import { txt } from './svgkit.mjs';
import { gcSegments } from './geo.mjs';

const W = 900, H = 1124, CX = 450;

const U = (m) => m / 17.5;
const PIERS = [[0, .55], [7.30, 7.85], [9.65, 10.20], [16.95, 17.50]].map(([a, b]) => [U(a), U(b)]);
const BLOCS_M = [[0, 7.85], [9.65, 17.50]];
const BLOCKS = BLOCS_M.map(([a, b]) => [U(a), U(b)]);
const VOID = [U(7.85), U(9.65)];
const DOORS = [[1.45, 3.25], [4.60, 6.40], [11.10, 12.90], [14.25, 16.05]].map(([a, b]) => [U(a), U(b)]);
const LIT = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1];  // fenetres allumees, motif fixe

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
const poly = (pts) => pts.map(([x, y], i) => `${i ? 'L' : 'M'} ${x} ${y}`).join(' ');
const N = 160;

function rive(u1, u2, lv, lobes = 2) {
  const top = [], bot = [];
  for (let j = 0; j <= N; j++) {
    const t = j / N, u = u1 + (u2 - u1) * t, b = bulge(t, lobes);
    const x = sx(u, lv.hw), yt = lv.y + lv.A * b;
    top.push([x, +yt.toFixed(2)]);
    bot.push([x, +(yt + lv.T + lv.B * b).toFixed(2)]);
  }
  return { top, bot };
}
const band = (r) => `${poly(r.top)} L ${r.bot[N][0]} ${r.bot[N][1]} ${poly(r.bot.slice().reverse()).slice(1)} Z`;
const ribbon = (a, b) => `${poly(a)} L ${b[b.length - 1][0]} ${b[b.length - 1][1]} ${poly(b.slice().reverse()).slice(1)} Z`;

// Garde-corps mixte, decoupe sur les memes segments que l'elevation
function gardeCorps(m1, m2, top, lv, P) {
  const out = [];
  const idx = (m) => Math.max(0, Math.min(N, Math.round((m - m1) / (m2 - m1) * N)));
  const up = top.map(([x, y]) => [x, +(y - lv.gc).toFixed(2)]);
  for (const seg of gcSegments(m1, m2)) {
    const i1 = idx(seg.x1), i2 = idx(seg.x2);
    if (i2 <= i1) continue;
    if (seg.kind === 'verre') {
      out.push(`<path d="${ribbon(up.slice(i1, i2 + 1), top.slice(i1, i2 + 1))}" fill="url(#glg)"/>`);
    } else {
      for (let m = seg.x1 + 0.055; m < seg.x2 - 0.03; m += 0.11) {
        const i = idx(m);
        out.push(`<line x1="${up[i][0]}" y1="${up[i][1] + 2}" x2="${top[i][0]}" y2="${top[i][1]}" stroke="${P.inox}" stroke-width="1.5" opacity="0.95"/>`);
      }
    }
    const ie = Math.min(N, i2);
    out.push(`<line x1="${up[ie][0]}" y1="${up[ie][1]}" x2="${top[ie][0]}" y2="${top[ie][1]}" stroke="${P.inox}" stroke-width="2.2"/>`);
  }
  out.push(`<path d="${poly(up)}" fill="none" stroke="${P.inox}" stroke-width="2.8"/>`);
  out.push(`<path d="${poly(up.map(([x, y]) => [x, y + 1.3]))}" fill="none" stroke="${P.rail}" stroke-width="1" opacity="0.85"/>`);
  return out.join('\n');
}

// ---------------------------------------------------------------------------
function buildSvg(night) {
  const P = night
    ? { wall: '#2B2C2C', wallSh: '#202223', deep: '#12100D', pier: '#3B3B38', aqua: '#F6EAD2',
        aquaSh: '#8A7F6C', soffit: '#F3D9A6', accent: '#FFC272', accentDark: '#8A5F26',
        glass: '#33454C', inox: '#8FA0A6', rail: '#E8F1F3', led: '#FFD9A0' }
    : { wall: '#E6DDCD', wallSh: '#CFC2AA', deep: '#3A342C', pier: '#F0E9DC', aqua: '#FCFAF6',
        aquaSh: '#D7CFC2', soffit: '#C4BAA9', accent: '#8A6E4C', accentDark: '#4E3F2C',
        glass: '#9FB4B8', inox: '#C8CED0', rail: '#FFFFFF', led: '#F0DFBE' };
  const g = [];

  g.push(`<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0.25" y2="1">
    ${night
      ? `<stop offset="0" stop-color="#070D18"/><stop offset="0.42" stop-color="#101E32"/>
         <stop offset="0.78" stop-color="#22364C"/><stop offset="1" stop-color="#3D4A54"/>`
      : `<stop offset="0" stop-color="#5C8FBF"/><stop offset="0.42" stop-color="#8FB6D6"/>
         <stop offset="0.78" stop-color="#C7D9E4"/><stop offset="1" stop-color="#E5E4DC"/>`}
  </linearGradient>
  <linearGradient id="aqg" x1="0" y1="0" x2="0.06" y2="1">
    ${night
      ? `<stop offset="0" stop-color="#6D6455"/><stop offset="0.34" stop-color="#A79878"/><stop offset="1" stop-color="${P.aqua}"/>`
      : `<stop offset="0" stop-color="${P.aqua}"/><stop offset="0.45" stop-color="#F0EBE1"/><stop offset="1" stop-color="${P.aquaSh}"/>`}
  </linearGradient>
  <linearGradient id="sof" x1="0" y1="0" x2="0" y2="1">
    ${night
      ? `<stop offset="0" stop-color="#FFE7B4"/><stop offset="1" stop-color="#B07E3C"/>`
      : `<stop offset="0" stop-color="${P.soffit}"/><stop offset="1" stop-color="#9E9382"/>`}
  </linearGradient>
  <linearGradient id="glg" x1="0" y1="0" x2="0.3" y2="1">
    ${night
      ? `<stop offset="0" stop-color="#5C7580" stop-opacity="0.55"/><stop offset="1" stop-color="#22333A" stop-opacity="0.42"/>`
      : `<stop offset="0" stop-color="#E4EDEE" stop-opacity="0.9"/><stop offset="1" stop-color="${P.glass}" stop-opacity="0.5"/>`}
  </linearGradient>
  <linearGradient id="wallg" x1="0" y1="0" x2="0.2" y2="1">
    <stop offset="0" stop-color="${P.wall}"/><stop offset="1" stop-color="${P.wallSh}"/>
  </linearGradient>
  <filter id="bloom" x="-60%" y="-60%" width="220%" height="220%">
    <feGaussianBlur stdDeviation="9"/>
  </filter>
  <filter id="bloomS" x="-80%" y="-80%" width="260%" height="260%">
    <feGaussianBlur stdDeviation="4"/>
  </filter>
</defs>`);

  g.push(`<rect x="0" y="0" width="${W}" height="${H}" fill="url(#sky)"/>`);
  const bot = L[0];

  // volume general
  g.push(`<path d="M ${sx(0, TOP.hw)} ${TOP.y} L ${sx(1, TOP.hw)} ${TOP.y} L ${sx(1, bot.hw)} ${bot.y + 120} L ${sx(0, bot.hw)} ${bot.y + 120} Z" fill="url(#wallg)"/>`);

  // vide central : lames verticales bronze, retroeclairees la nuit
  g.push(`<path d="M ${sx(VOID[0], TOP.hw)} ${TOP.y} L ${sx(VOID[1], TOP.hw)} ${TOP.y} L ${sx(VOID[1], bot.hw)} ${bot.y + 190} L ${sx(VOID[0], bot.hw)} ${bot.y + 190} Z" fill="${night ? '#3A2A12' : P.deep}"/>`);
  if (night)
    g.push(`<path d="M ${sx(VOID[0], TOP.hw)} ${TOP.y} L ${sx(VOID[1], TOP.hw)} ${TOP.y} L ${sx(VOID[1], bot.hw)} ${bot.y + 190} L ${sx(VOID[0], bot.hw)} ${bot.y + 190} Z" fill="#FFB74F" opacity="0.55" filter="url(#bloom)"/>`);
  for (let k = 0; k <= 11; k++) {
    const u = VOID[0] + (VOID[1] - VOID[0]) * (k + 0.5) / 12;
    g.push(`<line x1="${sx(u, TOP.hw)}" y1="${TOP.y}" x2="${sx(u, bot.hw)}" y2="${bot.y + 190}" stroke="${P.accent}" stroke-width="3" opacity="0.92"/>`);
    g.push(`<line x1="${sx(u, TOP.hw) + 1.6}" y1="${TOP.y}" x2="${sx(u, bot.hw) + 2}" y2="${bot.y + 190}" stroke="${P.accentDark}" stroke-width="1.4" opacity="0.9"/>`);
  }

  // du plus lointain au plus proche
  let door = 0;
  for (let i = L.length - 1; i >= 0; i--) {
    const lv = L[i], up = i < L.length - 1 ? L[i + 1] : ROOF;
    const hwW = lv.hw * 0.945;
    const yTopWall = up.y + (up.T ?? 8) + 4, yBotWall = lv.y + lv.A * 0.15;

    for (const [w1, w2] of BLOCKS)
      g.push(`<path d="M ${sx(w1, up.hw * 0.945)} ${yTopWall} L ${sx(w2, up.hw * 0.945)} ${yTopWall} L ${sx(w2, hwW)} ${yBotWall} L ${sx(w1, hwW)} ${yBotWall} Z" fill="${P.wallSh}" opacity="0.92"/>`);
    for (const [u1, u2] of DOORS) {
      const a1 = sx(u1, hwW), a2 = sx(u2, hwW), b1 = sx(u1, up.hw * 0.945), b2 = sx(u2, up.hw * 0.945);
      const d = `M ${b1} ${yTopWall + 5} L ${b2} ${yTopWall + 5} L ${a2} ${yBotWall - 3} L ${a1} ${yBotWall - 3} Z`;
      const on = night && LIT[door % LIT.length];
      if (on) g.push(`<path d="${d}" fill="#FFCE85" opacity="0.5" filter="url(#bloom)"/>`);
      g.push(`<path d="${d}" fill="${on ? '#FFD9A2' : night ? '#171A1C' : '#2C3234'}"/>`);
      g.push(`<path d="${d}" fill="none" stroke="${P.accent}" stroke-width="1.6" opacity="${night ? 0.7 : 1}"/>`);
      g.push(`<line x1="${(b1 + b2) / 2}" y1="${yTopWall + 5}" x2="${(a1 + a2) / 2}" y2="${yBotWall - 3}" stroke="${night ? '#8A6E4C' : P.accent}" stroke-width="1.3" opacity="0.85"/>`);
      door++;
    }
    for (const [u1, u2] of PIERS)
      g.push(`<path d="M ${sx(u1, up.hw)} ${up.y} L ${sx(u2, up.hw)} ${up.y} L ${sx(u2, lv.hw)} ${lv.y + lv.A + 26} L ${sx(u1, lv.hw)} ${lv.y + lv.A + 26} Z" fill="${P.pier}" opacity="0.96"/>`);

    if (!lv.podium) for (let b = 0; b < BLOCKS.length; b++) {
      const [u1, u2] = BLOCKS[b], [m1, m2] = BLOCS_M[b];
      const r = rive(u1, u2, lv);
      g.push(gardeCorps(m1, m2, r.top, lv, P));
      const under = r.bot.map(([x, y]) => [x, +(y + lv.T * 0.5 + lv.B * 0.55).toFixed(2)]);
      if (night) g.push(`<path d="${ribbon(r.bot, under)}" fill="#FFD48F" opacity="0.75" filter="url(#bloom)"/>`);
      g.push(`<path d="${ribbon(r.bot, under)}" fill="url(#sof)"/>`);
      g.push(`<path d="${band(r)}" fill="url(#aqg)"/>`);
      g.push(`<path d="${poly(r.top)}" fill="none" stroke="${night ? '#6C6250' : '#FFFFFF'}" stroke-width="1.4" opacity="0.85"/>`);
      g.push(`<path d="${poly(r.bot)}" fill="none" stroke="${night ? '#FFF0CE' : P.aquaSh}" stroke-width="${night ? 2.2 : 1.2}"/>`);
      if (night) g.push(`<path d="${poly(r.bot)}" fill="none" stroke="#FFE3AE" stroke-width="5" opacity="0.7" filter="url(#bloomS)"/>`);
    }
  }

  // couronnement
  g.push(`<path d="M ${sx(0, TOP.hw)} ${TOP.y} L ${sx(1, TOP.hw)} ${TOP.y} L ${sx(1, ROOF.hw)} ${ROOF.y} L ${sx(0, ROOF.hw)} ${ROOF.y} Z" fill="${P.pier}"/>`);
  g.push(`<rect x="${sx(0, TOP.hw)}" y="${TOP.y}" width="${2 * TOP.hw}" height="7" fill="${P.accent}"/>`);

  // socle parking, au premier plan
  const pTop = 838, pBot = H, pHwT = 404, pHwB = 468;
  g.push(`<path d="M ${sx(0, pHwT)} ${pTop} L ${sx(1, pHwT)} ${pTop} L ${sx(1, pHwB)} ${pBot} L ${sx(0, pHwB)} ${pBot} Z" fill="${night ? '#26272A' : '#CFC3AC'}"/>`);
  g.push(`<rect x="${sx(0, pHwT)}" y="${pTop}" width="${2 * pHwT}" height="9" fill="${night ? '#1A1B1E' : '#B4A78F'}"/>`);
  for (let k = 0; k < 5; k++) {
    const yy = pTop + 28 + k * 22, f = (yy - pTop) / (pBot - pTop), hw = pHwT + (pHwB - pHwT) * f;
    for (const [u1, u2] of [[U(0.55), U(7.30)], [U(7.85), U(9.65)], [U(10.20), U(16.95)]])
      g.push(`<line x1="${sx(u1, hw)}" y1="${yy}" x2="${sx(u2, hw)}" y2="${yy}" stroke="${night ? '#6E5636' : P.accent}" stroke-width="6" opacity="${0.92 - k * 0.03}"/>`);
  }
  // les deux terrasses R+2, separees par le vide central laisse ouvert
  for (let b = 0; b < BLOCKS.length; b++) {
    const [u1, u2] = BLOCKS[b], [m1, m2] = BLOCS_M[b];
    const lv = { ...L[0], hw: pHwT, A: 34, T: 17, B: 16, gc: 32 };
    const r = rive(u1, u2, lv);
    g.push(gardeCorps(m1, m2, r.top, lv, P));
    const under = r.bot.map(([x, y]) => [x, y + 13]);
    if (night) g.push(`<path d="${ribbon(r.bot, under)}" fill="#FFD48F" opacity="0.75" filter="url(#bloom)"/>`);
    g.push(`<path d="${ribbon(r.bot, under)}" fill="url(#sof)"/>`);
    g.push(`<path d="${band(r)}" fill="url(#aqg)"/>`);
    g.push(`<path d="${poly(r.bot)}" fill="none" stroke="${night ? '#FFF0CE' : P.aquaSh}" stroke-width="${night ? 2.2 : 1.2}"/>`);
    if (night) g.push(`<path d="${poly(r.bot)}" fill="none" stroke="#FFE3AE" stroke-width="5" opacity="0.7" filter="url(#bloomS)"/>`);
  }

  // bandeau alu + portes de garage
  {
    const yb = pTop + 156, f = (yb - pTop) / (pBot - pTop), hw = pHwT + (pHwB - pHwT) * f;
    if (night) g.push(`<rect x="${sx(0, hw) - 20}" y="${yb - 6}" width="${2 * hw + 40}" height="24" fill="#FFCE85" opacity="0.6" filter="url(#bloom)"/>`);
    g.push(`<rect x="${sx(0, hw) - 6}" y="${yb}" width="${2 * hw + 12}" height="9" fill="${night ? '#FFD9A2' : P.accent}"/>`);
    g.push(`<path d="M ${sx(0, hw)} ${yb + 9} L ${sx(1, hw)} ${yb + 9} L ${sx(1, pHwB)} ${pBot} L ${sx(0, pHwB)} ${pBot} Z" fill="${night ? '#232427' : '#B7AB94'}"/>`);
    for (const [u1, u2] of [[U(1.40), U(6.60)], [U(10.90), U(16.10)]]) {
      g.push(`<path d="M ${sx(u1, hw)} ${yb + 22} L ${sx(u2, hw)} ${yb + 22} L ${sx(u2, pHwB)} ${pBot - 14} L ${sx(u1, pHwB)} ${pBot - 14} Z" fill="${night ? '#141517' : P.accentDark}"/>`);
      for (let k = 1; k < 4; k++) {
        const yy = yb + 22 + k * 22, ff = (yy - pTop) / (pBot - pTop), h2 = pHwT + (pHwB - pHwT) * ff;
        g.push(`<line x1="${sx(u1, h2)}" y1="${yy}" x2="${sx(u2, h2)}" y2="${yy}" stroke="${night ? '#4A3B25' : P.accent}" stroke-width="1.6" opacity="0.7"/>`);
      }
    }
    const e = `M ${sx(VOID[0], hw)} ${yb + 16} L ${sx(VOID[1], hw)} ${yb + 16} L ${sx(VOID[1], pHwB)} ${pBot - 14} L ${sx(VOID[0], pHwB)} ${pBot - 14} Z`;
    if (night) g.push(`<path d="${e}" fill="#FFE0AE" opacity="0.8" filter="url(#bloom)"/>`);
    g.push(`<path d="${e}" fill="${night ? '#FFEBC6' : '#E8D9BC'}"/>`);
    g.push(`<rect x="0" y="${pBot - 14}" width="${W}" height="14" fill="${night ? '#1B1C1E' : '#9C917E'}"/>`);
  }

  // contexte : mur de soutenement et talus qui enserrent la venelle
  g.push(`<path d="M 0 ${H} L 0 ${H - 210} C 52 ${H - 188} 84 ${H - 128} 96 ${H} Z" fill="${night ? '#0C0E11' : '#2E2A24'}" opacity="${night ? 0.85 : 0.30}"/>`);
  g.push(`<path d="M ${W} ${H} L ${W} ${H - 250} C ${W - 62} ${H - 214} ${W - 96} ${H - 120} ${W - 108} ${H} Z" fill="${night ? '#0C0E11' : '#2E2A24'}" opacity="${night ? 0.8 : 0.26}"/>`);

  L.forEach((lv) => {
    const x = sx(1, lv.hw) + 16;
    g.push(`<line x1="${sx(1, lv.hw) + 4}" y1="${lv.y + lv.A * 0.2}" x2="${x + 4}" y2="${lv.y + lv.A * 0.2}" stroke="${night ? '#8E9AA2' : '#2B2724'}" stroke-width="0.8" opacity="0.5"/>`);
    g.push(txt(x + 10, lv.y + lv.A * 0.2 + 4, lv.name, { size: 10, anchor: 'start', weight: 600, fill: night ? '#B9C4CB' : '#3A352E', ls: '0.1em' }));
  });
  return g.join('\n');
}

const PLANCHES = [
  { file: 'Vue.dc.html', night: false, kicker: 'Ambiance · vue depuis la venelle', title: 'Rives ondulées',
    sub: 'Contre-plongée depuis le pied de l’immeuble — lecture des bandeaux cintrés en Aquapanel, du garde-corps mixte inox / verre qui suit l’onde, et du filtre bronze du vide central.',
    right: 'VUE D’AMBIANCE · JOUR<br>NON COTÉE<br>VARIANTE A' },
  { file: 'Vue-Nuit.dc.html', night: true, kicker: 'Ambiance · vue de nuit', title: 'La courbe allumée',
    sub: 'La gorge LED en sous-face lèche les 99 ml de rive cintrée : de nuit, la façade se réduit à cinq lignes de lumière qui ondulent, et à la faille centrale rétroéclairée.',
    right: 'VUE D’AMBIANCE · NUIT<br>NON COTÉE<br>VARIANTE A' },
];

for (const pl of PLANCHES) {
  const body = `<div style="width: ${W}px; background: #F1EDE5">
${header({ w: W, kicker: pl.kicker, title: pl.title, sub: pl.sub, right: pl.right })}
<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" xmlns="http://www.w3.org/2000/svg" style="display: block">${buildSvg(pl.night)}</svg>
</div>`;
  writeFileSync(pl.file, page({ body, props: JSON.stringify({ $preview: { width: W, height: H + 260 } }) }));
  console.log(pl.file, 'ok');
}
