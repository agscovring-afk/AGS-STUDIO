import { writeFileSync } from 'node:fs';
import { page, header } from './page.mjs';
import { txt } from './svgkit.mjs';
import { LV, XS, BALCONS, FASCIA, GC, PBH, DMIN, DMAX, AVANCEE, RETRAIT,
         AXE, BV_EP, GCN, PBN, depthAt, doors, gcSegments, BLOCS } from './geo.mjs';
import { CAM, p, path, strip, quad } from './perspective.mjs';

const W = 1180, H = 1085, N = 130;
const DF = CAM.dFacade, DP = CAM.dParking;
const VOID = [XS.vide[0], XS.vide[1]];
const PIERS = [XS.c1, XS.c2, XS.c3, XS.c4];
const LIT = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1];

const bi = (blk) => (blk[0] === BLOCS[0][0] ? 0 : 1);
const depthOf = (m, blk) => depthAt(m, bi(blk));
const sample = (blk, fY, fZ) => {
  const out = [];
  for (let i = 0; i <= N; i++) {
    const m = blk[0] + (blk[1] - blk[0]) * i / N, d = depthOf(m, blk);
    out.push(p(m, fY(d), fZ(d)));
  }
  return out;
};

// ---------------------------------------------------------------------------
function scene(night) {
  const C = night
    ? { wall: '#2C2D2D', wallSh: '#212324', bay: '#191B1C', pier: '#3D3D3A', aquaTop: '#5F5749',
        aquaBot: '#F7EBD4', soffitN: '#FFE7B4', soffitF: '#A8783A', accent: '#E8A757', accentD: '#6E4A1C',
        inox: '#93A4AA', rail: '#E9F2F4', glass: '#3A4E56', glassO: 0.5, sky: ['#070D18', '#101E32', '#22364C', '#2E4050'],
        podium: '#26272A', podiumT: '#1A1B1E', ground: '#111214', ctx: '#0B0D10', ctxO: 0.85, lbl: '#B9C4CB' }
    : { wall: '#F2F0EA', wallSh: '#DFDCD3', bay: '#C9C5BA', pier: '#FCFBF8', aquaTop: '#FFFFFF',
        aquaBot: '#E5E2DA', soffitN: '#CFCCC3', soffitF: '#A19E95', accent: '#474B4E', accentD: '#2E3236',
        inox: '#C8CED0', rail: '#FFFFFF', glass: '#A6BCC1', glassO: 0.55, sky: ['#5C8FBF', '#8FB6D6', '#C7D9E4', '#E5E4DC'],
        podium: '#E4E1D8', podiumT: '#CBC7BC', ground: '#A8A49A', ctx: '#2E2A24', ctxO: 0.3, lbl: '#3A352E' };
  const g = [];

  g.push(`<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0.25" y2="1">
    <stop offset="0" stop-color="${C.sky[0]}"/><stop offset="0.42" stop-color="${C.sky[1]}"/>
    <stop offset="0.78" stop-color="${C.sky[2]}"/><stop offset="1" stop-color="${C.sky[3]}"/></linearGradient>
  <linearGradient id="aq" x1="0" y1="0" x2="0.05" y2="1">
    <stop offset="0" stop-color="${C.aquaTop}"/><stop offset="${night ? 0.38 : 0.55}" stop-color="${night ? '#A2937A' : '#F2EDE4'}"/>
    <stop offset="1" stop-color="${C.aquaBot}"/></linearGradient>
  <linearGradient id="sof" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="${C.soffitN}"/><stop offset="1" stop-color="${C.soffitF}"/></linearGradient>
  <linearGradient id="gl" x1="0" y1="0" x2="0.3" y2="1">
    <stop offset="0" stop-color="${night ? '#5E7681' : '#E7EFF0'}" stop-opacity="${C.glassO + 0.3}"/>
    <stop offset="1" stop-color="${C.glass}" stop-opacity="${C.glassO}"/></linearGradient>
  <filter id="bloom" x="-70%" y="-70%" width="240%" height="240%"><feGaussianBlur stdDeviation="9"/></filter>
  <filter id="bloomS" x="-90%" y="-90%" width="280%" height="280%"><feGaussianBlur stdDeviation="4"/></filter>
</defs>`);
  g.push(`<rect x="0" y="0" width="${W}" height="${H}" fill="url(#sky)"/>`);

  // ---- tour : nu de facade, vide central ouvert --------------------------
  for (const blk of BLOCS) g.push(`<path d="${quad(blk[0], blk[1], DF, LV.r2, LV.acr)}" fill="${C.wall}"/>`);

  // vide central : deux balcons cote a cote, le brise-vue ENTRE eux
  // (precise le 23.08 : le brise-vue separe les deux logements, il n'est pas
  // tendu en facade ; on le voit ici par la tranche, sur l'axe du vide)
  g.push(`<path d="${quad(VOID[0], VOID[1], DF + RETRAIT, LV.r2, LV.toit)}" fill="${night ? '#241C12' : '#8E8A80'}"/>`);
  for (const z of BALCONS) {
    for (const [a, b] of [[VOID[0], AXE - BV_EP / 2], [AXE + BV_EP / 2, VOID[1]]]) {
      const c = (a + b) / 2, on = night;
      const d = quad(c - PBN / 2, c + PBN / 2, DF + RETRAIT, z + 0.02, z + PBH);
      if (on) g.push(`<path d="${d}" fill="#FFCE85" opacity="0.45" filter="url(#bloom)"/>`);
      g.push(`<path d="${d}" fill="${on ? '#FFD9A2' : '#2E3436'}"/>`);
      g.push(`<path d="${d}" fill="none" stroke="${C.accent}" stroke-width="1.5"/>`);
      // dalle et garde-corps du balcon, 0,70 m en arriere du nu de facade
      g.push(`<path d="${quad(a, b, DF + GCN, z - 0.20, z)}" fill="${C.wall}"/>`);
      g.push(`<path d="${quad(a, b, DF + GCN, z + 0.05, z + GC)}" fill="${C.glass}" opacity="0.35"/>`);
      g.push(`<path d="${path([p(a, DF + GCN, z + GC), p(b, DF + GCN, z + GC)])}" stroke="${C.inox}" stroke-width="2.4" fill="none"/>`);
    }
  }
  // le brise-vue separateur, sur l'axe, du R+2 a la toiture
  g.push(`<path d="${quad(AXE - BV_EP / 2, AXE + BV_EP / 2, DF + GCN, LV.r2, LV.toit)}" fill="${C.accent}"/>`);
  for (let x = AXE - BV_EP / 2 + 0.05; x < AXE + BV_EP / 2 - 0.02; x += 0.10)
    g.push(`<path d="${path([p(x, DF + GCN, LV.r2), p(x, DF + GCN, LV.toit)])}" stroke="${C.accentD}" stroke-width="2" fill="none"/>`);

  // ---- baies en retrait, menuiseries -------------------------------------
  let door = 0;
  for (const z of [LV.r2, ...BALCONS]) {
    for (const bay of [XS.bayA, XS.bayB]) {
      g.push(`<path d="${quad(bay[0], bay[1], DF + 0.12, z, z + 3.06)}" fill="${C.bay}" opacity="${night ? 1 : 0.55}"/>`);
      for (const [a, b] of doors(bay)) {
        const d = quad(a, b, DF + 0.10, z, z + PBH);
        const on = night && LIT[door % LIT.length];
        if (on) g.push(`<path d="${d}" fill="#FFCE85" opacity="0.5" filter="url(#bloom)"/>`);
        g.push(`<path d="${d}" fill="${on ? '#FFD9A2' : night ? '#15181A' : '#2E3436'}"/>`);
        g.push(`<path d="${d}" fill="none" stroke="${C.accent}" stroke-width="1.7" opacity="${night ? 0.65 : 1}"/>`);
        g.push(`<path d="${path([p((a + b) / 2, DF + 0.10, z), p((a + b) / 2, DF + 0.10, z + PBH)])}" stroke="${night ? '#8A6E4C' : C.accent}" stroke-width="1.3" fill="none" opacity="0.85"/>`);
        door++;
      }
      // brise-vue vertical d'intimite, en bout de balcon cote vide
      const bx = bay === XS.bayA ? bay[1] - 0.14 : bay[0];
      g.push(`<path d="${quad(bx, bx + 0.14, DF - DMIN, z, z + 2.20)}" fill="${C.accentD}"/>`);
    }
  }

  // ---- poteaux, acrotere, couvertine -------------------------------------
  for (const [a, b] of PIERS) {
    g.push(`<path d="${quad(a, b, DF - 0.06, LV.r2, LV.acr + 0.50)}" fill="${C.pier}"/>`);
    g.push(`<path d="${quad(a, a + 0.05, DF - 0.07, LV.r2, LV.acr + 0.50)}" fill="#FFFFFF" opacity="${night ? 0.10 : 0.5}"/>`);
    g.push(`<path d="${quad(b - 0.09, b, DF - 0.06, LV.r2, LV.acr + 0.50)}" fill="#000000" opacity="0.18"/>`);
    g.push(`<path d="${quad(a, b, DF - 0.07, LV.acr + 0.40, LV.acr + 0.50)}" fill="${C.accent}"/>`);
  }
  for (const blk of BLOCS) {
    g.push(`<path d="${quad(blk[0], blk[1], DF, LV.toit, LV.acr)}" fill="${C.wall}"/>`);
    g.push(`<path d="${quad(blk[0], blk[1], DF - 0.02, LV.acr - 0.10, LV.acr)}" fill="${C.accent}"/>`);
  }

  // ---- balcons ondules, du plus lointain (haut) au plus proche (bas) -----
  const balcon = (blk, zs, Yfront, Yback) => {
    const s = [];
    const rTop = sample(blk, Yfront, () => zs + 0.02);
    const rBot = sample(blk, Yfront, () => zs - FASCIA);
    const sofF = blk.map ? null : null;
    const sBack = sample(blk, () => Yback, () => zs - 0.20);
    // sous-face : de la rive jusqu'au nu de facade (apparait SOUS le bandeau)
    if (night) s.push(`<path d="${strip(rBot, sBack)}" fill="#FFD48F" opacity="0.8" filter="url(#bloom)"/>`);
    s.push(`<path d="${strip(rBot, sBack)}" fill="url(#sof)"/>`);
    // bandeau de rive Aquapanel
    s.push(`<path d="${strip(rTop, rBot)}" fill="url(#aq)"/>`);
    s.push(`<path d="${path(rBot)}" fill="none" stroke="${night ? '#FFF0CE' : C.aquaBot}" stroke-width="${night ? 2.4 : 1.3}"/>`);
    if (night) s.push(`<path d="${path(rBot)}" fill="none" stroke="#FFE3AE" stroke-width="5.5" opacity="0.75" filter="url(#bloomS)"/>`);
    s.push(`<path d="${path(rTop)}" fill="none" stroke="${night ? '#655C4C' : '#FFFFFF'}" stroke-width="1.3" opacity="0.8"/>`);
    // joues de rive : retour du bandeau jusqu'au nu de facade
    for (const m of [blk[0], blk[1]]) {
      const d = depthOf(m, blk), Yf = Yfront(d);
      s.push(`<path d="${path([p(m, Yf, zs + 0.02), p(m, Yback, zs + 0.02), p(m, Yback, zs - 0.20), p(m, Yf, zs - FASCIA)])} Z" fill="${night ? '#8E8065' : '#CFC5B2'}"/>`);
    }
    return s.join('\n');
  };

  const gardeCorps = (blk, zs, Yfront) => {
    const s = [];
    const Yg = (d) => Yfront(d) + 0.10;
    const low = sample(blk, Yg, () => zs + 0.10);
    const top = sample(blk, Yg, () => zs + GC);
    const idx = (m) => Math.max(0, Math.min(N, Math.round((m - blk[0]) / (blk[1] - blk[0]) * N)));
    for (const seg of gcSegments(bi(blk))) {
      const i1 = idx(seg.x1), i2 = idx(seg.x2);
      if (i2 <= i1) continue;
      if (seg.kind === 'verre') {
        const a = sample(blk, Yg, () => zs + 0.17).slice(i1, i2 + 1);
        const b = sample(blk, Yg, () => zs + GC - 0.10).slice(i1, i2 + 1);
        s.push(`<path d="${strip(b, a)}" fill="url(#gl)"/>`);
        s.push(`<path d="${path(a)}" fill="none" stroke="${C.inox}" stroke-width="1.6"/>`);
      } else {
        for (let m = seg.x1 + 0.055; m < seg.x2 - 0.03; m += 0.11) {
          const i = idx(m);
          s.push(`<path d="${path([low[i], top[i]])}" stroke="${C.inox}" stroke-width="1.5" fill="none"/>`);
        }
      }
      const ie = Math.min(N, i2);
      s.push(`<path d="${path([low[ie], top[ie]])}" stroke="${C.inox}" stroke-width="2.4" fill="none"/>`);
    }
    s.push(`<path d="${path([low[0], top[0]])}" stroke="${C.inox}" stroke-width="2.4" fill="none"/>`);
    s.push(`<path d="${path(top)}" fill="none" stroke="${C.inox}" stroke-width="3"/>`);
    s.push(`<path d="${path(top.map(([x, y]) => [x, +(y + 1.4).toFixed(2)]))}" fill="none" stroke="${C.rail}" stroke-width="1.1" opacity="0.8"/>`);
    return s.join('\n');
  };

  for (let i = BALCONS.length - 1; i >= 0; i--) {
    const zs = BALCONS[i];
    for (const blk of BLOCS) {
      // ombre portee du balcon sur la facade en retrait
      g.push(`<path d="${quad(blk[0], blk[1], DF + 0.06, zs - 1.15, zs - FASCIA)}" fill="#000000" opacity="${night ? 0.30 : 0.16}"/>`);
      g.push(gardeCorps(blk, zs, (d) => DF - d));
      g.push(balcon(blk, zs, (d) => DF - d, DF));
    }
  }

  // ---- socle parking, au premier plan ------------------------------------
  g.push(`<path d="${quad(0, 17.5, DP, -0.30, LV.r2)}" fill="${C.podium}"/>`);
  g.push(`<path d="${quad(0, 17.5, DP, LV.r2 - 0.12, LV.r2)}" fill="${C.podiumT}"/>`);
  // maconnerie pleine, ventilee par une seule bande de brise-vue de 0,80 m
  const bandeVent = (segs, z0) => {
    for (const [a, b] of segs) {
      g.push(`<path d="${quad(a, b, DP - 0.02, z0, z0 + 0.80)}" fill="${night ? '#101113' : C.accentD}"/>`);
      for (let z = z0 + 0.08; z < z0 + 0.80; z += 0.14)
        g.push(`<path d="${quad(a, b, DP - 0.03, z, z + 0.07)}" fill="${night ? '#5E5646' : C.accent}" opacity="0.92"/>`);
    }
  };
  bandeVent([[0.55, 7.30], [7.85, 9.65], [10.20, 16.95]], LV.r1 + 1.55);
  bandeVent([[0.55, 1.40], [6.60, 7.30], [7.85, 9.65], [10.20, 10.90], [16.10, 16.95]], 1.35);
  // bandeau alu + portes de garage + hall
  if (night) g.push(`<path d="${quad(-0.3, 17.8, DP - 0.1, 2.44, 2.62)}" fill="#FFCE85" opacity="0.65" filter="url(#bloom)"/>`);
  g.push(`<path d="${quad(-0.3, 17.8, DP - 0.1, 2.44, 2.58)}" fill="${night ? '#FFD9A2' : C.accent}"/>`);
  for (const [a, b] of [[1.40, 6.60], [10.90, 16.10]]) {
    g.push(`<path d="${quad(a, b, DP - 0.04, 0.20, 2.30)}" fill="${night ? '#141517' : C.accentD}"/>`);
    for (let z = 0.58; z < 2.30; z += 0.38)
      g.push(`<path d="${quad(a, b, DP - 0.05, z, z + 0.04)}" fill="${night ? '#4A3B25' : C.accent}" opacity="0.75"/>`);
  }
  const hall = quad(VOID[0] - 0.05, VOID[1] + 0.05, DP - 0.04, 0, 2.10);
  if (night) g.push(`<path d="${hall}" fill="#FFE0AE" opacity="0.85" filter="url(#bloom)"/>`);
  g.push(`<path d="${hall}" fill="${night ? '#FFEBC6' : '#E8D9BC'}"/>`);

  // ---- les deux terrasses R+2 : acrotere droit au nu du parking -----------
  for (const blk of BLOCS) {
    const zt = LV.r2 + FASCIA;
    if (night) g.push(`<path d="${quad(blk[0], blk[1], DP, LV.r2, LV.r2 + 0.10)}" fill="#FFD48F" opacity="0.8" filter="url(#bloom)"/>`);
    g.push(`<path d="${quad(blk[0], blk[1], DP, LV.r2, zt)}" fill="url(#aq)"/>`);
    g.push(`<path d="${quad(blk[0], blk[1], DP, LV.r2, LV.r2 + 0.07)}" fill="${night ? '#FFF0CE' : C.aquaBot}"/>`);
    g.push(`<path d="${quad(blk[0] + 0.04, blk[1] - 0.04, DP - 0.10, zt + 0.17, zt + GC - 0.10)}" fill="url(#gl)"/>`);
    const n = Math.max(2, Math.round((blk[1] - blk[0]) / 1.35));
    for (let k = 0; k <= n; k++) {
      const m = blk[0] + (blk[1] - blk[0]) * k / n;
      g.push(`<path d="${path([p(m, DP - 0.10, zt + 0.08), p(m, DP - 0.10, zt + GC)])}" stroke="${C.inox}" stroke-width="2.2" fill="none"/>`);
    }
    g.push(`<path d="${quad(blk[0], blk[1], DP - 0.10, zt + GC - 0.09, zt + GC)}" fill="${C.inox}"/>`);
  }

  // ---- contexte : la venelle enserre le pied de l'immeuble ----------------
  g.push(`<path d="M 0 ${H} L 0 ${H - 330} C 34 ${H - 288} 56 ${H - 156} 62 ${H} Z" fill="${C.ctx}" opacity="${C.ctxO}"/>`);
  g.push(`<path d="M ${W} ${H} L ${W} ${H - 370} C ${W - 40} ${H - 322} ${W - 64} ${H - 148} ${W - 70} ${H} Z" fill="${C.ctx}" opacity="${C.ctxO * 0.92}"/>`);

  // ---- reperes de niveau --------------------------------------------------
  for (const [z, name] of [[LV.r2, 'R+2'], [LV.r3, 'R+3'], [LV.r4, 'R+4'], [LV.r5, 'R+5'], [LV.r6, 'R+6'], [LV.r7, 'R+7'], [LV.r8, 'R+8']]) {
    const [x, y] = p(17.5, DF, z);
    g.push(`<path d="${path([[x + 4, y], [x + 22, y]])}" stroke="${C.lbl}" stroke-width="0.8" opacity="0.5" fill="none"/>`);
    g.push(txt(x + 28, y + 4, name, { size: 10, anchor: 'start', weight: 600, fill: C.lbl, ls: '0.1em' }));
  }
  return g.join('\n');
}

const PLANCHES = [
  { file: 'Vue.dc.html', night: false, kicker: 'Ambiance · vue depuis la venelle', title: 'Rives ondulées',
    sub: 'Perspective à trois points depuis le pied de l’immeuble — onde de rive relevée sur votre croquis, garde-corps mixte inox et verre noir, fente centrale de 1,80 m creusée de 1,50 m : deux petits balcons de 0,70 × 0,80 m, le brise-vue de 40 cm entre eux.',
    right: 'VUE D’AMBIANCE · JOUR<br>NON COTÉE<br>VARIANTE A' },
  { file: 'Vue-Nuit.dc.html', night: true, kicker: 'Ambiance · vue de nuit', title: 'La courbe allumée',
    sub: 'La gorge LED en sous-face lèche les 108 ml de rive cintrée : de nuit, la façade se réduit à six lignes de lumière qui ondulent, et à la faille centrale rétroéclairée.',
    right: 'VUE D’AMBIANCE · NUIT<br>NON COTÉE<br>VARIANTE A' },
];
for (const pl of PLANCHES) {
  const body = `<div style="width: ${W}px; background: #FFFFFF">
${header({ w: W, kicker: pl.kicker, title: pl.title, sub: pl.sub, right: pl.right })}
<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" xmlns="http://www.w3.org/2000/svg" style="display: block">${scene(pl.night)}</svg>
</div>`;
  writeFileSync(pl.file, page({ body, props: JSON.stringify({ $preview: { width: W, height: H + 250 } }) }));
  console.log(pl.file, 'ok');
}
