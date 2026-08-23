import { writeFileSync } from 'node:fs';
import { XS, LV, BLOCS, FASCIA, GC, PBH, AVANCEE, RETRAIT,
         AXE, BV_EP, GCN, PBN, depthAt, doors, gcSegments, developpe } from './geo.mjs';
import { page, header } from './page.mjs';
import { txt } from './svgkit.mjs';

// Vue plongeante : l'oeil se place dans le vide entre la terrasse du R+2 et le
// balcon du R+3 — 15 m de haut, 10 m devant le nu de facade, incline de 45°.
const W = 1180, H = 960;
const CAMH = 15, DF = 10, DP = DF - AVANCEE;
const PHI = -45 * Math.PI / 180, F = 1100, CX = 590, CY = 660, MC = 12.675;
const CO = Math.cos(PHI), SI = Math.sin(PHI);
const P = (m, Y, Z) => {
  const X = m - MC, z = Z - CAMH;
  const yp = Y * CO + z * SI, zp = -Y * SI + z * CO;
  return [+(CX + F * X / yp).toFixed(2), +(CY - F * zp / yp).toFixed(2)];
};
const path = (p) => p.map(([x, y], i) => `${i ? 'L' : 'M'} ${x} ${y}`).join(' ');
const quad = (m1, m2, Y1, Z1, Y2, Z2) => `${path([P(m1, Y1, Z1), P(m2, Y1, Z1), P(m2, Y2, Z2), P(m1, Y2, Z2)])} Z`;
const dalle = (m1, m2, Y1, Y2, Z) => `${path([P(m1, Y1, Z), P(m2, Y1, Z), P(m2, Y2, Z), P(m1, Y2, Z)])} Z`;
const line = (a, b, col, w, o = 1, extra = '') =>
  `<path d="${path([a, b])}" stroke="${col}" stroke-width="${w}" opacity="${o}" fill="none" ${extra}/>`;
const strip = (a, b) => `${path(a)} L ${b[b.length - 1][0]} ${b[b.length - 1][1]} ${path(b.slice().reverse()).slice(1)} Z`;

const C = { wall: '#F7F5F1', wallSh: '#E9E6DF', pier: '#FFFFFF',
  deck: '#EFECE4', deckJoint: '#D3CEC3', gravier: '#DAD5C9',
  aqua: '#FFFFFF', aquaSh: '#E6E3DA', soffit: '#D6D2C8', dalleB: '#FBFAF7',
  accent: '#474B4E', accentD: '#31353A', glass: '#1E2224', inox: '#AEB7BC',
  led: '#E7B94F', ink: '#23211E', dim: '#8C8478', fond: '#F1EFEA' };

const BLK = BLOCS[1], [M1, M2] = BLK, N = 150;
const rive = (Z, off = 0) => {
  const p = [];
  for (let i = 0; i <= N; i++) { const m = M1 + (M2 - M1) * i / N; p.push(P(m, DF - depthAt(m, 1) + off, Z)); }
  return p;
};
const nu = (Z) => { const p = []; for (let i = 0; i <= N; i++) { const m = M1 + (M2 - M1) * i / N; p.push(P(m, DF, Z)); } return p; };
const idx = (m) => Math.max(0, Math.min(N, Math.round((m - M1) / (M2 - M1) * N)));
const g = [];

g.push(`<rect x="0" y="0" width="${W}" height="${H}" fill="${C.fond}"/>`);

// ---- mur de facade, du R+2 au R+4 ---------------------------------------
g.push(`<path d="${quad(XS.vide[0], M2, DF, LV.r4 + 0.4, DF, LV.r2)}" fill="url(#murg)"/>`);
// vide central : deux balcons cote a cote, le brise-vue ENTRE eux
g.push(`<path d="${quad(XS.vide[0], XS.vide[1], DF + RETRAIT, LV.r4 + 0.4, DF + RETRAIT, LV.r2)}" fill="${C.wallSh}"/>`);
g.push(`<path d="${quad(XS.vide[0], XS.vide[0], DF, LV.r4 + 0.4, DF + RETRAIT, LV.r2)}" fill="${C.wallSh}" opacity="0.7"/>`);
for (const z of [LV.r3]) {
  for (const [a, b] of [[XS.vide[0], AXE - BV_EP / 2], [AXE + BV_EP / 2, XS.vide[1]]]) {
    const c = (a + b) / 2;
    g.push(`<path d="${quad(c - PBN / 2, c + PBN / 2, DF + RETRAIT, z + PBH, DF + RETRAIT, z)}" fill="url(#vitg)"/>`);
    g.push(`<path d="${dalle(a, b, DF + GCN, DF + RETRAIT, z)}" fill="${C.dalleB}"/>`);
    g.push(gcDroit(a, b, DF + GCN, DF + GCN, z));
  }
}
// le brise-vue separateur : sur l'axe, du fond de la niche au nu de facade
// sa joue, vue de biais : plan perpendiculaire au nu, de la facade au fond de niche
g.push(`<path d="${path([P(AXE, DF + GCN, LV.r4 + 0.4), P(AXE, DF + RETRAIT, LV.r4 + 0.4), P(AXE, DF + RETRAIT, LV.r2), P(AXE, DF + GCN, LV.r2)])} Z" fill="${C.accentD}"/>`);
g.push(`<path d="${quad(AXE - BV_EP / 2, AXE + BV_EP / 2, DF + GCN, LV.r4 + 0.4, DF + GCN, LV.r2)}" fill="${C.accent}"/>`);
for (let z = LV.r2 + 0.2; z < LV.r4 + 0.4; z += 0.2)
  g.push(line(P(AXE, DF + GCN, z), P(AXE, DF + RETRAIT, z), '#FFFFFF', 1, 0.25));
g.push(txt(...P(AXE + 0.5, DF + RETRAIT, LV.r4 + 0.1), 'BRISE-VUE ENTRE LES 2 BALCONS', { size: 8.5, fill: C.dim, ls: '0.1em', weight: 700, anchor: 'start' }));

// menuiseries du R+2 et du R+3 — alu TPR RAL 7024, verre reflechissant
for (const [z] of [[LV.r2], [LV.r3]])
  for (const [a, b] of doors(XS.bayB)) {
    g.push(`<path d="${quad(a, b, DF, z + PBH, DF, z)}" fill="url(#vitg)"/>`);
    g.push(`<path d="${quad(a, b, DF, z + PBH, DF, z)}" fill="none" stroke="${C.accent}" stroke-width="2.4"/>`);
    const mm = (a + b) / 2;
    g.push(line(P(mm, DF, z + PBH), P(mm, DF, z), C.accent, 2, 0.85));
  }

// ---- terrasse du R+2, sur la toiture du parking --------------------------
// dalles sur plots 60 x 60, une terrasse par appartement
const deckTone = `<linearGradient id="dkg" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#E7E3DA"/><stop offset="1" stop-color="${C.deck}"/></linearGradient>`;
g.push(`<path d="${dalle(XS.vide[1], M2, DP, DF, LV.r2)}" fill="url(#dkg)"/>`);
for (let m = XS.vide[1] + 0.6; m < M2 - 0.01; m += 0.6)
  g.push(line(P(m, DP, LV.r2), P(m, DF, LV.r2), C.deckJoint, 1, 0.6));
for (let y = DP + 0.6; y < DF - 0.01; y += 0.6)
  g.push(line(P(XS.vide[1], y, LV.r2), P(M2, y, LV.r2), C.deckJoint, 1, 0.6));
// bande centrale de separation, en gravier : les deux terrasses ne communiquent pas
g.push(`<path d="${dalle(XS.vide[0], XS.vide[1], DP, DF, LV.r2)}" fill="${C.gravier}"/>`);
for (let k = 0; k < 700; k++) {
  const m = XS.vide[0] + 0.1 + (k * 0.6180339887 % 1) * (XS.vide[1] - XS.vide[0] - 0.2);
  const y = DP + 0.1 + ((k * 0.3819660113 + 0.37) % 1) * (AVANCEE - 0.2);
  const [px, py] = P(m, y, LV.r2);
  g.push(`<circle cx="${px}" cy="${py}" r="1.9" fill="#A79F8D" opacity="0.75"/>`);
}

// ombre portee du balcon R+3 sur la terrasse, proportionnelle au porte-a-faux
{
  const a = [], b = [];
  for (let i = 0; i <= N; i++) {
    const m = M1 + (M2 - M1) * i / N, d = depthAt(m, 1);
    a.push(P(m, DF, LV.r2)); b.push(P(m, Math.max(DP, DF - d - 0.75), LV.r2));
  }
  g.push(`<path d="${strip(a, b)}" fill="#2E3236" opacity="0.13"/>`);
}
g.push(txt(...P(15.4, DP + 1.1, LV.r2), 'TERRASSE R+2', { size: 12, fill: '#7C7568', ls: '0.2em', weight: 700, anchor: 'middle' }));
g.push(txt(...P(15.4, DP + 0.45, LV.r2), '7,85 × 4,00 m — dalles sur plots', { size: 8.5, fill: C.dim, ls: '0.08em', weight: 600, anchor: 'middle' }));
g.push(txt(...P(8.75, DP + 1.6, LV.r2), 'BANDE DE SÉPARATION 1,80', { size: 9, fill: '#6E6659', ls: '0.14em', weight: 700, anchor: 'middle' }));

// garde-corps droit de la terrasse : verre feuillete + main courante inox
function gcDroit(m1, m2, Y1, Y2, Z) {
  const s = [];
  const a = P(m1, Y1, Z + GC), b = P(m2, Y2, Z + GC), c = P(m2, Y2, Z), d = P(m1, Y1, Z);
  s.push(`<path d="${path([a, b, c, d])} Z" fill="${C.glass}" opacity="0.13"/>`);
  const n = Math.max(2, Math.round(Math.hypot(m2 - m1, Y2 - Y1) / 1.35));
  for (let k = 0; k <= n; k++) {
    const t = k / n, mm = m1 + (m2 - m1) * t, yy = Y1 + (Y2 - Y1) * t;
    s.push(line(P(mm, yy, Z), P(mm, yy, Z + GC), C.inox, 2.2, 0.9));
  }
  s.push(line(a, b, C.inox, 3.4));
  return s.join('');
}
g.push(gcDroit(XS.vide[0], XS.vide[0], DF, DP, LV.r2));   // joue gauche du vide
g.push(gcDroit(XS.vide[1], XS.vide[1], DF, DP, LV.r2));   // joue droite du vide
g.push(gcDroit(M2, M2, DF, DP, LV.r2));                   // pignon droit
g.push(gcDroit(XS.vide[0], M2, DP, DP, LV.r2));           // nez de dalle, toute la largeur

// ---- balcon du R+3, au-dessus ------------------------------------------
{
  const Z = LV.r3, rTop = rive(Z), nuTop = nu(Z), rBot = rive(Z - FASCIA);
  g.push(`<path d="${strip(nuTop, rTop)}" fill="${C.dalleB}"/>`);          // dessus de la dalle
  // joints du carrelage du balcon, paralleles au nu
  for (let d = 0.4; d < 1.75; d += 0.4) {
    const p = [];
    for (let i = 0; i <= N; i++) {
      const m = M1 + (M2 - M1) * i / N, dd = depthAt(m, 1);
      if (dd <= d + 0.02) { if (p.length > 1) g.push(`<path d="${path(p)}" stroke="${C.deckJoint}" stroke-width="0.9" opacity="0.55" fill="none"/>`); p.length = 0; continue; }
      p.push(P(m, DF - d, Z));
    }
    if (p.length > 1) g.push(`<path d="${path(p)}" stroke="${C.deckJoint}" stroke-width="0.9" opacity="0.55" fill="none"/>`);
  }
  g.push(`<path d="${strip(rTop, rBot)}" fill="url(#aqg)"/>`);             // bandeau de rive Aquapanel
  g.push(`<path d="${path(rBot)}" fill="none" stroke="${C.ink}" stroke-width="1.6" opacity="0.55"/>`);
  g.push(`<path d="${path(rTop)}" fill="none" stroke="${C.ink}" stroke-width="2"/>`);
  g.push(`<path d="${path(rive(Z, -0.06))}" fill="none" stroke="${C.led}" stroke-width="2.4" stroke-dasharray="12 7"/>`);
  // garde-corps mixte au pas de 40 cm : un panneau de verre plat, puis 40 cm d'inox
  const gTop = rive(Z + GC, 0.10), gBot = rive(Z, 0.10);
  for (const seg of gcSegments(1)) {
    const i1 = idx(seg.x1), i2 = idx(seg.x2);
    if (i2 <= i1) continue;
    if (seg.kind === 'verre')
      g.push(`<path d="${strip(gTop.slice(i1, i2 + 1), gBot.slice(i1, i2 + 1))}" fill="${C.glass}" opacity="0.22"/>`);
    else
      for (let m = seg.x1 + 0.055; m < seg.x2 - 0.03; m += 0.11)
        g.push(line(gBot[idx(m)], gTop[idx(m)], C.inox, 1.7, 0.95));
  }
  g.push(`<path d="${path(gTop)}" fill="none" stroke="${C.inox}" stroke-width="3.4"/>`);
  g.push(txt(...P(15.4, DF - 0.45, Z), 'BALCON R+3', { size: 11, fill: '#7C7568', ls: '0.2em', weight: 700, anchor: 'middle' }));
}

// ---- sous-face du balcon du R+4, en tete de vue -------------------------
{
  const Z = LV.r4, rBot = rive(Z - FASCIA), nuBot = nu(Z - FASCIA);
  g.push(`<path d="${strip(nuBot, rBot)}" fill="${C.soffit}"/>`);
  g.push(`<path d="${path(rBot)}" fill="none" stroke="#BDB8AC" stroke-width="1.6"/>`);
  g.push(txt(...P(15.4, DF - 0.8, Z - FASCIA), 'SOUS-FACE DU BALCON R+4', { size: 9, fill: '#6E6A62', ls: '0.12em', weight: 700, anchor: 'middle' }));
}

// ---- reperes de lecture -------------------------------------------------
{
  const cote = (m, lab) => {
    const d = depthAt(m, 1), a = P(m, DF, LV.r3 + 0.02), b = P(m, DF - d, LV.r3 + 0.02);
    g.push(`<path d="${path([a, b])}" stroke="#B4392F" stroke-width="2.2" fill="none" stroke-dasharray="6 4"/>`);
    g.push(`<circle cx="${b[0]}" cy="${b[1]}" r="3.2" fill="#B4392F"/>`);
    g.push(txt(b[0], b[1] - 10, lab, { size: 10, fill: '#B4392F', weight: 700, anchor: 'middle' }));
  };
  cote(M1 + 1.96, '1,80');
  cote(M1 + 5.64, '1,10');
}

g.unshift(`<defs>
  <linearGradient id="aqg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${C.aqua}"/><stop offset="1" stop-color="${C.aquaSh}"/></linearGradient>
  <linearGradient id="murg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="${C.wall}"/></linearGradient>
  <linearGradient id="vitg" x1="0" y1="0" x2="0.35" y2="1"><stop offset="0" stop-color="#3A4247"/><stop offset="0.55" stop-color="#22272B"/><stop offset="1" stop-color="#171B1E"/></linearGradient>
  ${deckTone}
</defs>`);

const body = `<div style="width: ${W}px; background: #FFFFFF">
${header({ w: W, kicker: 'Vue plongeante · dans le vide entre la terrasse R+2 et le balcon R+3',
  title: 'La terrasse, et le balcon au-dessus',
  sub: `Bloc droit vu de dessus, l’œil à 15 m. En bas la terrasse du R+2 posée sur la toiture du parking, ses dalles sur plots et son garde-corps droit ; au milieu la fente de 1,80 m et ses deux petits balcons de 0,70 × 0,80 m séparés par le brise-vue de 40 cm ; au-dessus le balcon du R+3 dont la rive creuse un grand lobe de 1,80 m puis un petit de 1,45 m — ${developpe().toFixed(2)} ml de développé.`,
  right: 'VUE D’AMBIANCE<br>NON COTÉE<br>BLOC DROIT' })}
<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" xmlns="http://www.w3.org/2000/svg" style="display: block">${g.join('\n')}</svg>
</div>`;
writeFileSync('Vue-Haut.dc.html', page({ body, props: JSON.stringify({ $preview: { width: W, height: H + 200 } }) }));
console.log('Vue-Haut.dc.html ok');
