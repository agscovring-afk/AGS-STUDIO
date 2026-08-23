import { writeFileSync } from 'node:fs';
import { XS, LV, BLOCS, BALCONS, MIROIR, COL, FASCIA, GC, PBH, PBW, AVANCEE, RETRAIT,
         AXE, BV_EP, GCN, PBN, BALCON_NICHE_P, DALLE, ACROTERE,
         FV_EP, FV_PANNEAU, FV_JOINT, CAD_L, CAD_EP, POTEAUX,
         depthAt, doors, gcSegments, developpe } from './geo.mjs';
import { page, header } from './page.mjs';
import { makeCam, poly, SUN, SUNDIR, shadeN, castY, castZ, haze, norm, dot, sub, rgb2hex, hex2rgb } from './camera.mjs';

const NUIT = process.argv.includes('--nuit');
const ZOOM = process.argv.includes('--zoom');
// Trois garde-corps a comparer, demandes le 24.08 : tout verre, fer forge,
// tout inox. 'mixte' reste le 40/40 verre-inox du dossier.
const GCTYPE = (process.argv.find((a) => a.startsWith('--gc=')) || '--gc=verre').slice(5);
const W = ZOOM ? 1600 : 1280, H = ZOOM ? 1120 : 1780;
const C = ZOOM
  ? makeCam({ eye: [1.2, 16.5, 9.4], look: [13.5, 0, 9.4], f: 2150, cx: 1075, cy: 1470 })
  : makeCam({ eye: [-6, 25, 1.60], look: [10, 0, 1.60], f: 1150, cx: 781, cy: 1530 });
const P = C.P;
const g = [];
const px = (p) => { const q = P(p); return `${q[0]} ${q[1]}`; };
const face = (pts, fill, extra = '') => `<path d="${poly(C, pts)}" fill="${fill}" ${extra}/>`;
const strip = (a, b, fill, extra = '') => {
  const pa = a.map(P).filter((q) => Number.isFinite(q[0]));
  const pb = b.map(P).filter((q) => Number.isFinite(q[0]));
  if (pa.length < 2 || pb.length < 2) return '';
  return `<path d="${pa.map(([x, y], i) => `${i ? 'L' : 'M'} ${x} ${y}`).join(' ')} ${pb.reverse().map(([x, y]) => `L ${x} ${y}`).join(' ')} Z" fill="${fill}" ${extra}/>`;
};

// --- palette matiere -------------------------------------------------------
const MAT = NUIT ? {
  mono: '#8792A3', beton: '#6E7684', aqua: '#98A2B0', soffit: '#5A6270',
  alu: '#23272B', verre: '#0E1418', inox: '#7F8A93', asphalte: '#1B1E22',
  trottoir: '#333840', ciel0: '#0B1A32', ciel1: '#1D3557', ciel2: '#3E5C7E',
  led: '#FFC46B', fenetre: '#FFD79A', horizon: '#2C4867',
  trav: '#7E735F', alu7024: '#2B2F33',
} : {
  mono: '#F4F1EA', beton: '#D9D5CB', aqua: '#FBFAF7', soffit: '#E7E3DA',
  alu: '#474B4E', verre: '#20272B', inox: '#C2C9CE', asphalte: '#8C8B85',
  trottoir: '#CFC9BC', ciel0: '#3D7FBE', ciel1: '#8FC0E4', ciel2: '#E4EFF6',
  led: '#F3D9A4', fenetre: '#2B3236', horizon: '#D8E6F0',
  trav: '#C9B695', alu7024: '#474B4E',
};
const SH = NUIT ? { amb: 0.46, kd: 0.20, sky: 0.12, bounce: 0.07 } : { amb: 0.52, kd: 0.80, sky: 0.14, bounce: 0.11 };
const S = (base, n, o = {}) => shadeN(base, n, { ...SH, ...o });
const NY = [0, 1, 0], NX = [-1, 0, 0], NZ = [0, 0, 1], NZm = [0, 0, -1];

// ===========================================================================
// DEFS — textures et filtres
// ===========================================================================
g.push(`<defs>
  <linearGradient id="ciel" x1="0" y1="0" x2="0.15" y2="1">
    <stop offset="0" stop-color="${MAT.ciel0}"/><stop offset="0.55" stop-color="${MAT.ciel1}"/>
    <stop offset="1" stop-color="${MAT.ciel2}"/></linearGradient>
  <linearGradient id="solG" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="${NUIT ? '#232E3C' : '#A6A8A3'}"/>
    <stop offset="0.15" stop-color="${NUIT ? '#171E27' : '#83837C'}"/>
    <stop offset="1" stop-color="${NUIT ? '#0D1218' : '#585853'}"/></linearGradient>
  <linearGradient id="gradFacade" x1="0" y1="0" x2="0.35" y2="1">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.16"/>
    <stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0"/>
    <stop offset="1" stop-color="#2C3A47" stop-opacity="0.13"/></linearGradient>
  <linearGradient id="gradPignon" x1="0" y1="0" x2="1" y2="0.15">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.10"/>
    <stop offset="1" stop-color="#26313C" stop-opacity="0.20"/></linearGradient>
  <radialGradient id="soleil" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#FFF6E0" stop-opacity="${NUIT ? 0 : 0.95}"/>
    <stop offset="0.45" stop-color="#FFE9BE" stop-opacity="${NUIT ? 0 : 0.35}"/>
    <stop offset="1" stop-color="#FFE9BE" stop-opacity="0"/></radialGradient>
  <filter id="nuages" x="-20%" y="-20%" width="140%" height="140%">
    <feTurbulence type="fractalNoise" baseFrequency="0.0016 0.0055" numOctaves="6" seed="7" result="t"/>
    <feColorMatrix in="t" type="matrix" result="a"
      values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  1.5 0 0 0 -0.42"/>
    <feGaussianBlur in="a" stdDeviation="2.5"/>
  </filter>
  <filter id="crepi" x="0%" y="0%" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.62" numOctaves="4" seed="3" result="n"/>
    <feDiffuseLighting in="n" lighting-color="#ffffff" surfaceScale="1.05" result="l">
      <feDistantLight azimuth="215" elevation="58"/>
    </feDiffuseLighting>
    <feComposite in="l" in2="SourceGraphic" operator="arithmetic" k1="1.06" k2="0" k3="0" k4="-0.05"/>
  </filter>
  <filter id="travertin" x="0%" y="0%" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.035 1.25" numOctaves="5" seed="13" result="n"/>
    <feDiffuseLighting in="n" lighting-color="#ffffff" surfaceScale="1.6" result="l">
      <feDistantLight azimuth="212" elevation="48"/>
    </feDiffuseLighting>
    <feComposite in="l" in2="SourceGraphic" operator="arithmetic" k1="1.14" k2="0" k3="0" k4="-0.10"/>
  </filter>
  <linearGradient id="wallwash" x1="0" y1="1" x2="0" y2="0">
    <stop offset="0" stop-color="#FFD9A0" stop-opacity="${NUIT ? 0.62 : 0.10}"/>
    <stop offset="0.22" stop-color="#FFCE8C" stop-opacity="${NUIT ? 0.34 : 0.05}"/>
    <stop offset="0.65" stop-color="#F5BE7C" stop-opacity="${NUIT ? 0.10 : 0}"/>
    <stop offset="1" stop-color="#F5BE7C" stop-opacity="0"/></linearGradient>
  <filter id="beton2" x="0%" y="0%" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.22" numOctaves="3" seed="11" result="n"/>
    <feDiffuseLighting in="n" lighting-color="#ffffff" surfaceScale="0.8" result="l">
      <feDistantLight azimuth="215" elevation="60"/>
    </feDiffuseLighting>
    <feComposite in="l" in2="SourceGraphic" operator="arithmetic" k1="1.03" k2="0" k3="0" k4="-0.02"/>
  </filter>
  <filter id="bitume" x="0%" y="0%" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.9 0.35" numOctaves="4" seed="19" result="n"/>
    <feDiffuseLighting in="n" lighting-color="#ffffff" surfaceScale="0.9" result="l">
      <feDistantLight azimuth="215" elevation="52"/>
    </feDiffuseLighting>
    <feComposite in="l" in2="SourceGraphic" operator="arithmetic" k1="1.10" k2="0" k3="0" k4="-0.08"/>
  </filter>
  <filter id="flou6"><feGaussianBlur stdDeviation="6"/></filter>
  <filter id="flou14"><feGaussianBlur stdDeviation="14"/></filter>
  <filter id="flou3"><feGaussianBlur stdDeviation="3"/></filter>
  <filter id="bloom" x="-60%" y="-60%" width="220%" height="220%">
    <feGaussianBlur stdDeviation="9" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="grain" x="0%" y="0%" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="5" result="n"/>
    <feColorMatrix in="n" type="saturate" values="0"/>
  </filter>
  <radialGradient id="vign" cx="0.5" cy="0.44" r="0.78">
    <stop offset="0.5" stop-color="#000" stop-opacity="0"/>
    <stop offset="1" stop-color="#000" stop-opacity="${NUIT ? 0.55 : 0.26}"/></radialGradient>
  <linearGradient id="vitre" x1="0" y1="0" x2="0.34" y2="1">
    <stop offset="0" stop-color="${NUIT ? '#101820' : '#8FB4CE'}"/>
    <stop offset="0.22" stop-color="${NUIT ? '#0D141A' : '#4E6B80'}"/>
    <stop offset="0.46" stop-color="${NUIT ? '#0B1116' : '#232E36'}"/>
    <stop offset="0.72" stop-color="${NUIT ? '#090E13' : '#1A222A'}"/>
    <stop offset="1" stop-color="${NUIT ? '#080C10' : '#222C33'}"/></linearGradient>
  <linearGradient id="spillBas" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFC97E" stop-opacity="0.30"/>
    <stop offset="0.45" stop-color="#F0B268" stop-opacity="0.10"/>
    <stop offset="1" stop-color="#E0A45E" stop-opacity="0"/></linearGradient>
  <linearGradient id="spillHaut" x1="0" y1="1" x2="0" y2="0">
    <stop offset="0" stop-color="#FFD08C" stop-opacity="0.34"/>
    <stop offset="1" stop-color="#FFD08C" stop-opacity="0"/></linearGradient>
  <linearGradient id="refletCiel" x1="0" y1="1" x2="0.55" y2="0">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>
    <stop offset="0.62" stop-color="#CFE3F2" stop-opacity="0.20"/>
    <stop offset="0.78" stop-color="#EAF3FA" stop-opacity="0.36"/>
    <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
  <linearGradient id="vitreLum" x1="0" y1="0" x2="0.3" y2="1">
    <stop offset="0" stop-color="#FFE7BC"/><stop offset="1" stop-color="#E8A857"/></linearGradient>
  <clipPath id="cadre"><rect x="0" y="0" width="${W}" height="${H}"/></clipPath>
</defs>`);
g.push(`<g clip-path="url(#cadre)">`);

// ===========================================================================
// CIEL
// ===========================================================================
g.push(`<rect x="0" y="0" width="${W}" height="${H}" fill="url(#ciel)"/>`);
g.push(`<rect x="0" y="0" width="${W}" height="${1560}" filter="url(#nuages)" opacity="${NUIT ? 0.10 : 0.42}"/>`);
{ // le soleil, hors champ a gauche, mais sa lueur est dans le cadre
  const q = P([-40, 60, 60]);
  if (Number.isFinite(q[0])) g.push(`<ellipse cx="${q[0]}" cy="${q[1]}" rx="620" ry="520" fill="url(#soleil)"/>`);
}
if (NUIT) for (let i = 0; i < 90; i++) {
  const x = (i * 137.5) % W, y = ((i * 61.8) % 700) + 20;
  g.push(`<circle cx="${x.toFixed(0)}" cy="${y.toFixed(0)}" r="${(0.5 + (i % 3) * 0.35).toFixed(1)}" fill="#DCE8FF" opacity="${(0.25 + (i % 5) * 0.12).toFixed(2)}"/>`);
}

// ===========================================================================
// CONTEXTE LOINTAIN — la ville derriere, noyee dans la brume
// ===========================================================================
{
  const blocs = [
    [-46, -34, -30, 15], [-33, -20, -26, 11], [-19, -30, -22, 18],
    [24, -26, -34, 14], [36, -34, -28, 19], [50, -22, -24, 12], [64, -30, -30, 16],
  ];
  for (const [x0, y0, x1, h] of blocs) {
    const d = Math.hypot(x0 + 6, y0 - 25);
    const c = haze(NUIT ? '#2A3A52' : '#C8C3B8', d, { d0: 25, k: 0.011, color: NUIT ? '#1B3050' : '#C6D8E6' });
    g.push(face([[x0, y0, 0], [x0 + 14, y0 + x1 * 0, 0], [x0 + 14, y0, h], [x0, y0, h]], c));
    g.push(face([[x0 + 14, y0, 0], [x0 + 14, y0 - 16, 0], [x0 + 14, y0 - 16, h * 0.92], [x0 + 14, y0, h]],
      haze(NUIT ? '#1E2C40' : '#ABA69B', d + 8, { d0: 25, k: 0.011, color: NUIT ? '#1B3050' : '#C6D8E6' })));
    if (NUIT) for (let k = 0; k < 26; k++) {
      const fx = x0 + 1.4 + (k % 6) * 2.1, fz = 2.5 + Math.floor(k / 6) * 3.2;
      if (fz > h - 1.5 || (k * 7) % 5 === 0) continue;
      const a = P([fx, y0, fz]), b = P([fx + 1.0, y0, fz + 1.5]);
      if (!Number.isFinite(a[0])) continue;
      g.push(`<rect x="${b[0]}" y="${b[1]}" width="${(a[0] - b[0]).toFixed(1)}" height="${(a[1] - b[1]).toFixed(1)}" fill="#FFD79A" opacity="0.5"/>`);
    }
  }
}

// ===========================================================================
// SOL — bitume, bordure, trottoir
// ===========================================================================
{
  const hz = P([0, 400, 0])[1];
  g.push(`<rect x="0" y="${hz - 2}" width="${W}" height="${H - hz + 2}" fill="url(#solG)"/>`);
  g.push(`<rect x="0" y="${hz - 2}" width="${W}" height="${H - hz + 2}" filter="url(#bitume)" opacity="0.20"/>`);
  // trottoir devant le socle : Y de 4.0 a 7.2, avec sa bordure
  const TR0 = AVANCEE, TR1 = AVANCEE + 3.2, X0 = -30, X1 = 60;
  g.push(face([[X0, TR0, 0.16], [X1, TR0, 0.16], [X1, TR1, 0.16], [X0, TR1, 0.16]], S(MAT.trottoir, NZ)));
  g.push(face([[X0, TR1, 0], [X1, TR1, 0], [X1, TR1, 0.16], [X0, TR1, 0.16]], S(MAT.trottoir, NY, { kd: SH.kd * 0.8 })));
  for (let x = X0; x < X1; x += 1.2)
    g.push(`<path d="${poly(C, [[x, TR0, 0.161], [x, TR1, 0.161]], false)}" stroke="${NUIT ? '#2B3038' : '#A29C90'}" stroke-width="1" fill="none" opacity="0.55"/>`);
  g.push(`<path d="${poly(C, [[X0, TR1, 0.161], [X1, TR1, 0.161]], false)}" stroke="${NUIT ? '#3A4049' : '#CFCABE'}" stroke-width="1.6" fill="none" opacity="0.8"/>`);
  // marquage au sol de la chaussee
  for (let x = -26; x < 58; x += 5.5)
    g.push(face([[x, 15.6, 0.012], [x + 2.6, 15.6, 0.012], [x + 2.6, 15.95, 0.012], [x, 15.95, 0.012]], NUIT ? '#7A776A' : '#E6E2D6', 'opacity="0.85"'));
  // pied de bordure : la ligne sombre qui pose le trottoir sur la chaussee
  g.push(`<path d="${poly(C, [[X0, TR1, 0.004], [X1, TR1, 0.004]], false)}" stroke="#1E2228" stroke-width="3" fill="none" opacity="0.42"/>`);
}

// ===========================================================================
// OMBRE PORTEE DU BATIMENT SUR LE SOL
// ===========================================================================
if (!NUIT) {
  const sil = [[0, AVANCEE, LV.r2], [17.5, AVANCEE, LV.r2], [17.5, 0, LV.acr], [0, 0, LV.acr]];
  g.push(`<path d="${poly(C, [
    [0, AVANCEE, 0], [17.5, AVANCEE, 0],
    castZ([17.5, AVANCEE, LV.r2], 0.16), castZ([17.5, 0, LV.acr], 0.16),
    castZ([0, 0, LV.acr], 0.16), castZ([0, AVANCEE, LV.r2], 0.16)])}"
    fill="#14161A" opacity="0.30" filter="url(#flou6)"/>`);
}

// ===========================================================================
// LE BATIMENT
// ===========================================================================
const PROF = 13;                                    // profondeur du corps de batiment
const NS = 150;                                     // finesse des courbes
const rive = (b, z, off = 0, dz = 0) => {
  const [m1, m2] = BLOCS[b], p = [];
  for (let i = 0; i <= NS; i++) { const m = m1 + (m2 - m1) * i / NS; p.push([m, depthAt(m, b) + off, z + dz]); }
  return p;
};
const nu = (b, z, y = 0) => { const [m1, m2] = BLOCS[b]; return [[m1, y, z], [m2, y, z]]; };

// --- pignon gauche (X = 0), il fuit vers l'arriere -------------------------
g.push(face([[0, 0, 0], [0, -PROF, 0], [0, -PROF, LV.acr], [0, 0, LV.acr]], S(MAT.mono, NX), 'filter="url(#crepi)"'));
g.push(face([[0, 0, 0], [0, -PROF, 0], [0, -PROF, LV.acr], [0, 0, LV.acr]], 'url(#gradPignon)'));
for (let k = 2; k <= 8; k++) {                       // baies de pignon
  const z = LV['r' + k] + 0.95;
  for (const y of [-2.6, -6.4, -10.0]) {
    g.push(face([[0.03, y, z - 0.05], [0.03, y - 1.55, z - 0.05], [0.03, y - 1.55, z + 1.55], [0.03, y, z + 1.55]],
      S(MAT.mono, NX, { kd: SH.kd * 0.42 })));
    g.push(face([[0.06, y - 0.07, z], [0.06, y - 1.48, z], [0.06, y - 1.48, z + 1.45], [0.06, y - 0.07, z + 1.45]],
      NUIT && (k * 3 + Math.round(y)) % 3 ? 'url(#vitreLum)' : 'url(#vitre)'));
    g.push(`<path d="${poly(C, [[0.07, y - 0.775, z], [0.07, y - 0.775, z + 1.45]], false)}" stroke="${MAT.alu}" stroke-width="1.4" fill="none" opacity="0.85"/>`);
  }
}

// --- masse de la tour : nu de facade du R+2 a l'acrotere -------------------
const murTour = S(MAT.mono, NY);
g.push(face([[0, 0, LV.r2 - 0.4], [17.5, 0, LV.r2 - 0.4], [17.5, 0, LV.acr], [0, 0, LV.acr]], murTour, 'filter="url(#crepi)"'));
g.push(face([[0, 0, LV.r2 - 0.4], [17.5, 0, LV.r2 - 0.4], [17.5, 0, LV.acr], [0, 0, LV.acr]], 'url(#gradFacade)'));
// occlusion douce en pied de tour et le long du pignon
g.push(`<linearGradient id="aoV" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2B3138" stop-opacity="0.22"/><stop offset="1" stop-color="#2B3138" stop-opacity="0"/></linearGradient>`);
g.push(face([[0, 0, LV.r2], [2.2, 0, LV.r2], [2.2, 0, LV.acr], [0, 0, LV.acr]], 'url(#aoV)'));

// --- facade ventilee : les quatre poteaux habilles de travertin -------------
// Le parement sort de 9 cm du nu sur ossature, lame d'air derriere. C'est le
// retour lateral du parement, eclaire autrement que sa face, qui donne le
// relief : sans lui un poteau habille ressemble a un aplat colle.
{
  const z0 = LV.r2 - 0.40, z1 = LV.acr;
  for (const [pa, pb] of POTEAUX) {
    // le parement deborde de 15 cm de part et d'autre du poteau : sans ce
    // debord la bande disparait derriere le garde-corps du balcon
    const a = Math.max(0, pa - 0.15), b = Math.min(17.5, pb + 0.15);
    // face du parement, au nu + 9 cm
    g.push(face([[a, FV_EP, z0], [b, FV_EP, z0], [b, FV_EP, z1], [a, FV_EP, z1]],
      S(MAT.trav, NY), 'filter="url(#travertin)"'));
    // retour gauche, seul visible depuis ce point de vue
    g.push(face([[a, 0, z0], [a, FV_EP, z0], [a, FV_EP, z1], [a, 0, z1]],
      S(MAT.trav, NX), 'filter="url(#travertin)"'));
    // joints creux ouverts entre panneaux de 1,20 m
    for (let z = z0 + FV_PANNEAU; z < z1; z += FV_PANNEAU) {
      g.push(`<path d="${poly(C, [[a, FV_EP, z], [b, FV_EP, z]], false)}" stroke="${NUIT ? '#0B0F14' : '#5E574A'}" stroke-width="2" fill="none" opacity="0.72"/>`);
      g.push(`<path d="${poly(C, [[a, FV_EP, z + FV_JOINT], [b, FV_EP, z + FV_JOINT]], false)}" stroke="${NUIT ? '#4A5460' : '#FBF6EA'}" stroke-width="1" fill="none" opacity="0.55"/>`);
    }
    // joint vertical au droit du retour, et arete vive
    g.push(`<path d="${poly(C, [[a, FV_EP, z0], [a, FV_EP, z1]], false)}" stroke="${NUIT ? '#C6CED6' : '#FFFFFF'}" stroke-width="1.4" fill="none" opacity="0.55"/>`);
    // ombre du parement sur le monocouche, a droite du poteau
    if (!NUIT) g.push(strip([[b, 0, z0], [b, 0, z1]],
      [castY([b, FV_EP, z0], 0), castY([b, FV_EP, z1], 0)], '#1A222C', 'opacity="0.30" filter="url(#flou3)"'));
    // lechage lumineux depuis le pied : les projecteurs encastres au R+2
    g.push(face([[a, FV_EP + 0.002, z0], [b, FV_EP + 0.002, z0], [b, FV_EP + 0.002, z0 + 9], [a, FV_EP + 0.002, z0 + 9]],
      'url(#wallwash)'));
  }
}

// --- joints creux au droit de chaque plancher -------------------------------
for (const k of [2, 3, 4, 5, 6, 7, 8]) {
  const z = LV['r' + k];
  g.push(`<path d="${poly(C, [[0, 0, z], [17.5, 0, z]], false)}" stroke="${NUIT ? '#0F1620' : '#B9B3A6'}" stroke-width="1.6" fill="none" opacity="0.7"/>`);
  g.push(`<path d="${poly(C, [[0, 0, z + 0.02], [17.5, 0, z + 0.02]], false)}" stroke="${NUIT ? '#7D8794' : '#FFFFFF'}" stroke-width="1" fill="none" opacity="0.5"/>`);
}

// --- le vide central : la fente, ses deux balcons, le brise-vue -------------
{
  const [n1, n2] = XS.vide;
  // fond de la fente, a 1,50 m : toujours dans l'ombre
  g.push(face([[n1, -RETRAIT, LV.r2], [n2, -RETRAIT, LV.r2], [n2, -RETRAIT, LV.acr - ACROTERE], [n1, -RETRAIT, LV.acr - ACROTERE]],
    S(MAT.mono, NY, { kd: 0, amb: SH.amb * 0.62 })));
  // joue gauche de la fente, vue de biais
  g.push(face([[n1, 0, LV.r2], [n1, -RETRAIT, LV.r2], [n1, -RETRAIT, LV.acr - ACROTERE], [n1, 0, LV.acr - ACROTERE]],
    S(MAT.mono, [1, 0, 0], { kd: 0, amb: SH.amb * 0.5 })));
  g.push(face([[n2, 0, LV.r2], [n2, -RETRAIT, LV.r2], [n2, -RETRAIT, LV.acr - ACROTERE], [n2, 0, LV.acr - ACROTERE]],
    S(MAT.mono, NX, { kd: SH.kd * 0.35 })));
  for (const z of BALCONS) {
    for (const [a, b] of [[n1, AXE - BV_EP / 2], [AXE + BV_EP / 2, n2]]) {
      const c = (a + b) / 2;
      g.push(face([[c - PBN / 2, -RETRAIT + 0.01, z + 0.05], [c + PBN / 2, -RETRAIT + 0.01, z + 0.05],
                   [c + PBN / 2, -RETRAIT + 0.01, z + PBH], [c - PBN / 2, -RETRAIT + 0.01, z + PBH]],
        NUIT && (Math.round(z * 7 + c)) % 3 ? 'url(#vitreLum)' : 'url(#vitre)'));
      // dalle du petit balcon + garde-corps verre
      g.push(face([[a, -GCN, z], [b, -GCN, z], [b, -RETRAIT, z], [a, -RETRAIT, z]], S(MAT.beton, NZm, { kd: 0 })));
      g.push(face([[a, -GCN, z - 0.20], [b, -GCN, z - 0.20], [b, -GCN, z], [a, -GCN, z]], S(MAT.mono, NY, { kd: SH.kd * 0.25 })));
      g.push(face([[a, -GCN, z + 0.05], [b, -GCN, z + 0.05], [b, -GCN, z + GC], [a, -GCN, z + GC]],
        NUIT ? '#0B1218' : '#26313A', 'opacity="0.55"'));
      g.push(`<path d="${poly(C, [[a, -GCN, z + GC], [b, -GCN, z + GC]], false)}" stroke="${MAT.inox}" stroke-width="2" fill="none" opacity="0.9"/>`);
    }
  }
  // le brise-vue : 40 cm sur l'axe, du fond de la fente au garde-corps
  const bvL = S(MAT.alu, [-1, 0, 0], { kd: SH.kd * 0.4, amb: SH.amb * 0.9 });
  g.push(face([[AXE - BV_EP / 2, -GCN, LV.r2], [AXE - BV_EP / 2, -RETRAIT, LV.r2],
               [AXE - BV_EP / 2, -RETRAIT, LV.acr - ACROTERE], [AXE - BV_EP / 2, -GCN, LV.acr - ACROTERE]], bvL));
  g.push(face([[AXE - BV_EP / 2, -GCN, LV.r2], [AXE + BV_EP / 2, -GCN, LV.r2],
               [AXE + BV_EP / 2, -GCN, LV.acr - ACROTERE], [AXE - BV_EP / 2, -GCN, LV.acr - ACROTERE]], S(MAT.alu, NY)));
  for (let z = LV.r2 + 0.16; z < LV.acr - ACROTERE; z += 0.16)
    g.push(`<path d="${poly(C, [[AXE - BV_EP / 2, -GCN, z], [AXE - BV_EP / 2, -RETRAIT, z]], false)}" stroke="#12161A" stroke-width="0.9" fill="none" opacity="0.5"/>`);
}

// --- les balcons ------------------------------------------------------------
// Trois passes, parce que l'ordre compte : d'abord les menuiseries qui sont
// dans le plan du mur, puis les ombres portees qui doivent tomber DESSUS,
// puis seulement les volumes des balcons, du plus haut (le plus loin) au plus
// bas (le plus pres), pour que les plus proches masquent les autres.
const sunAt = (m, b, dm = 0.02) => {
  const d0 = depthAt(m - dm, b), d1 = depthAt(m + dm, b);
  return norm([-(d1 - d0), 2 * dm, 0]);              // normale sortante en plan
};

// passe 1 — menuiseries en retrait de 12 cm dans le mur
for (const z of BALCONS) for (let b = 0; b < 2; b++) {
  for (const [a, bb] of doors(b ? XS.bayB : XS.bayA)) {
    const z0 = z + 0.03, z1 = z + PBH;
    const A = a - CAD_L, B = bb + CAD_L, Z0 = z0 - CAD_L, Z1 = z1 + CAD_L;
    // cadrage Alucobond RAL 7024 : un cadre en saillie de 5 cm autour de la baie
    for (const q of [[[A, Z0], [B, Z0], [B, Z0 + CAD_L], [A, Z0 + CAD_L]],
                     [[A, Z1 - CAD_L], [B, Z1 - CAD_L], [B, Z1], [A, Z1]],
                     [[A, Z0 + CAD_L], [a, Z0 + CAD_L], [a, Z1 - CAD_L], [A, Z1 - CAD_L]],
                     [[bb, Z0 + CAD_L], [B, Z0 + CAD_L], [B, Z1 - CAD_L], [bb, Z1 - CAD_L]]])
      g.push(face(q.map(([x, zz]) => [x, CAD_EP, zz]), S(MAT.alu7024, NY, { kd: SH.kd * 1.05 })));
    // retours du cadre : c'est eux qui donnent l'epaisseur
    g.push(face([[A, 0, Z0], [A, CAD_EP, Z0], [A, CAD_EP, Z1], [A, 0, Z1]], S(MAT.alu7024, NX, { kd: SH.kd * 0.5 })));
    g.push(face([[A, CAD_EP, Z1], [B, CAD_EP, Z1], [B, 0, Z1], [A, 0, Z1]], S(MAT.alu7024, NZ, { kd: SH.kd * 0.9 })));
    g.push(face([[A, CAD_EP, Z0], [B, CAD_EP, Z0], [B, 0, Z0], [A, 0, Z0]], S(MAT.alu7024, NZm, { kd: 0, amb: SH.amb * 0.7 })));
    if (!NUIT) g.push(strip([[B, 0, Z0], [B, 0, Z1]], [castY([B, CAD_EP, Z0], 0), castY([B, CAD_EP, Z1], 0)],
      '#18202A', 'opacity="0.26" filter="url(#flou3)"'));
    // tableau en retrait derriere le cadre
    g.push(face([[a, CAD_EP, z0], [a, -0.12, z0], [a, -0.12, z1], [a, CAD_EP, z1]],
      S(MAT.alu7024, [1, 0, 0], { kd: 0, amb: SH.amb * 0.6 })));
    g.push(face([[bb, CAD_EP, z0], [bb, -0.12, z0], [bb, -0.12, z1], [bb, CAD_EP, z1]],
      S(MAT.alu7024, NX, { kd: SH.kd * 0.45 })));
    g.push(face([[a, -0.12, z1], [bb, -0.12, z1], [bb, CAD_EP, z1], [a, CAD_EP, z1]],
      S(MAT.alu7024, NZm, { kd: 0, amb: SH.amb * 0.55 })));
    g.push(face([[a, -0.12, z + 0.03], [bb, -0.12, z + 0.03], [bb, -0.12, z + PBH], [a, -0.12, z + PBH]],
      NUIT && (Math.round(z * 3 + a)) % 3 ? 'url(#vitreLum)' : 'url(#vitre)'));
    if (!NUIT) g.push(face([[a, -0.118, z + 0.03], [bb, -0.118, z + 0.03], [bb, -0.118, z + PBH], [a, -0.118, z + PBH]], 'url(#refletCiel)'));
    const c = (a + bb) / 2;
    g.push(`<path d="${poly(C, [[c, -0.12, z + 0.03], [c, -0.12, z + PBH]], false)}" stroke="${MAT.alu}" stroke-width="1.8" fill="none" opacity="0.92"/>`);
    g.push(`<path d="${poly(C, [[a, -0.115, z + 0.03], [a, -0.115, z + PBH], [bb, -0.115, z + PBH], [bb, -0.115, z + 0.03]], false)}" stroke="${MAT.alu}" stroke-width="2.2" fill="none" opacity="0.9"/>`);
  }
  if (NUIT) {
    const bay = b ? XS.bayB : XS.bayA, dd = doors(bay), c = (dd[0][1] + dd[1][0]) / 2;
    g.push(face([[c - 0.03, 0.01, z + 0.35], [c + 0.03, 0.01, z + 0.35], [c + 0.03, 0.01, z + 2.25], [c - 0.03, 0.01, z + 2.25]],
      MAT.led, 'filter="url(#bloom)" opacity="0.95"'));
  }
}

// passe 2 — l'ombre que chaque balcon jette sur la facade, sous lui
if (!NUIT) for (const z of BALCONS) for (let b = 0; b < 2; b++) {
  const [m1, m2] = BLOCS[b], top = [], bot = [];
  for (let i = 0; i <= NS; i++) {
    const m = m1 + (m2 - m1) * i / NS, d = depthAt(m, b);
    top.push([m, 0, z - FASCIA]);
    bot.push(castY([m, d, z - FASCIA], 0));
  }
  g.push(strip(top, bot, '#16202B', 'opacity="0.42" filter="url(#flou3)"'));
}
// l'ombre du socle sur lui-meme, et celle de la tour sur la terrasse
if (!NUIT) {
  g.push(strip([[0, 0, LV.r2], [17.5, 0, LV.r2]],
    [castY([0, 0, LV.r2], 0), castY([17.5, 0, LV.r2], 0)], '#16202B', 'opacity="0.10"'));
}

// passe 3 — les volumes, du plus haut au plus bas
for (let li = BALCONS.length - 1; li >= 0; li--) {
  const z = BALCONS[li];
  for (let b = 0; b < 2; b++) {
    // sous-face : elle ne voit jamais le soleil
    g.push(strip(nu(b, z - FASCIA), rive(b, z - FASCIA), S(MAT.soffit, NZm, { kd: 0, amb: SH.amb * 0.86 })));
    g.push(strip(nu(b, z - FASCIA), rive(b, z - FASCIA), NUIT ? '#050A10' : '#22303C', 'opacity="0.22"'));

    // le bandeau de rive, facette par facette : c'est lui qui donne le relief
    {
      const hi = rive(b, z, 0, 0.06), lo = rive(b, z - FASCIA);
      for (let i = 0; i < NS; i++) {
        const m = (BLOCS[b][0] + (BLOCS[b][1] - BLOCS[b][0]) * (i + 0.5) / NS);
        const n = sunAt(m, b);
        const q = [hi[i], hi[i + 1], lo[i + 1], lo[i]].map(P);
        if (!q.every((v) => Number.isFinite(v[0]))) continue;
        g.push(`<path d="M ${q.map(([x, y]) => `${x} ${y}`).join(' L ')} Z" fill="${S(MAT.aqua, n)}" shape-rendering="crispEdges"/>`);
      }
      g.push(`<path d="${poly(C, hi, false)}" stroke="${NUIT ? '#8794A0' : '#FFFFFF'}" stroke-width="1.6" fill="none" opacity="0.8"/>`);
      g.push(`<path d="${poly(C, lo, false)}" stroke="${NUIT ? '#05090E' : '#7E7669'}" stroke-width="1.4" fill="none" opacity="0.5"/>`);
      if (NUIT) {
        // la gorge lave la sous-face au-dessus d'elle et le mur en dessous
        g.push(strip(rive(b, z - FASCIA, -0.02), rive(b, z - FASCIA, -0.02).map(([x, y, zz]) => [x, y - 1.15, zz]),
          'url(#spillHaut)'));
        g.push(strip([[BLOCS[b][0], 0, z - FASCIA], [BLOCS[b][1], 0, z - FASCIA]],
          [[BLOCS[b][0], 0, z - FASCIA - 1.9], [BLOCS[b][1], 0, z - FASCIA - 1.9]], 'url(#spillBas)'));
      }
      g.push(`<path d="${poly(C, rive(b, z - FASCIA, -0.06), false)}" stroke="${MAT.led}"
        stroke-width="${NUIT ? 4.5 : 2}" fill="none" opacity="${NUIT ? 0.95 : 0.3}" ${NUIT ? 'filter="url(#bloom)"' : ''}/>`);
    }

    // le garde-corps — quatre ecritures possibles sur la meme rive
    {
      const hi = rive(b, z + GC, 0.10), lo = rive(b, z + 0.05, 0.10);
      const [m1, m2] = BLOCS[b];
      const idx = (m) => Math.max(0, Math.min(NS, Math.round((m - m1) / (m2 - m1) * NS)));
      const barreau = (m, col, w) => {
        const i = idx(m);
        if (!hi[i] || !lo[i]) return;
        g.push(`<path d="${poly(C, [lo[i], hi[i]], false)}" stroke="${col}" stroke-width="${w}" fill="none" opacity="0.95"/>`);
      };
      const panneauVerre = (x1, x2) => {
        const i1 = idx(Math.min(x1, x2)), i2 = idx(Math.max(x1, x2));
        if (i2 <= i1) return;
        const n = sunAt((x1 + x2) / 2, b), refl = Math.max(0, dot(n, [0, 1, 0]));
        g.push(strip(hi.slice(i1, i2 + 1), lo.slice(i1, i2 + 1), NUIT ? '#070D13' : '#1E262D',
          `opacity="${(0.58 - 0.18 * refl).toFixed(2)}"`));
        g.push(strip(hi.slice(i1, i2 + 1), hi.slice(i1, i2 + 1).map(([x, y, zz]) => [x, y, zz - 0.34]),
          NUIT ? '#2A3B4C' : '#B7D2E4', `opacity="${(0.12 + 0.36 * refl).toFixed(2)}"`));
        // pinces inox aux deux bouts du panneau
        for (const i of [i1 + 1, i2 - 1]) {
          if (!lo[i]) continue;
          const q = P([lo[i][0], lo[i][1], lo[i][2] + 0.06]);
          if (Number.isFinite(q[0])) g.push(`<circle cx="${q[0]}" cy="${q[1]}" r="${ZOOM ? 3.4 : 1.6}" fill="${MAT.inox}"/>`);
        }
      };

      if (GCTYPE === 'verre') {
        // tout verre : les memes cordes de 38 cm, sans barreaudage
        for (const seg of gcSegments(b)) panneauVerre(seg.x1 + 0.012, seg.x2 - 0.012);
      } else if (GCTYPE === 'inox') {
        // tout inox : barreaudage continu au pas de 11 cm, deux lisses
        for (let m = m1 + 0.06; m < m2 - 0.03; m += 0.11) barreau(m, MAT.inox, ZOOM ? 3.4 : 1.5);
        for (const dz of [0.42, 0.78]) {
          const l = rive(b, z + 0.05 + dz, 0.10);
          g.push(`<path d="${poly(C, l, false)}" stroke="${MAT.inox}" stroke-width="${ZOOM ? 4 : 1.8}" fill="none" opacity="0.9"/>`);
        }
      } else if (GCTYPE === 'fer') {
        // fer forge : barreaux plats, et un registre de volutes entre deux lisses
        const FER = NUIT ? '#0E1216' : '#2B2C2E';
        for (let m = m1 + 0.06; m < m2 - 0.03; m += 0.13) barreau(m, FER, ZOOM ? 4.2 : 1.9);
        for (const dz of [0.30, 0.86]) {
          const l = rive(b, z + 0.05 + dz, 0.10);
          g.push(`<path d="${poly(C, l, false)}" stroke="${FER}" stroke-width="${ZOOM ? 6 : 2.6}" fill="none" opacity="0.95"/>`);
        }
        // les volutes : deux arcs opposes par module de 52 cm
        for (let m = m1 + 0.26; m < m2 - 0.26; m += 0.52) {
          const i0 = idx(m - 0.22), ic = idx(m), i1 = idx(m + 0.22);
          if (!hi[i0] || !hi[i1]) continue;
          const yA = z + 0.32, yB = z + 0.84;
          const A = P([lo[i0][0], lo[i0][1], yA]), B = P([lo[ic][0], lo[ic][1], (yA + yB) / 2]), D = P([lo[i1][0], lo[i1][1], yA]);
          const A2 = P([lo[i0][0], lo[i0][1], yB]), D2 = P([lo[i1][0], lo[i1][1], yB]);
          if (![A, B, D, A2, D2].every((q) => Number.isFinite(q[0]))) continue;
          const w = ZOOM ? 3.6 : 1.6;
          g.push(`<path d="M ${A[0]} ${A[1]} Q ${B[0]} ${B[1]} ${D[0]} ${D[1]}" fill="none" stroke="${FER}" stroke-width="${w}"/>`);
          g.push(`<path d="M ${A2[0]} ${A2[1]} Q ${B[0]} ${B[1]} ${D2[0]} ${D2[1]}" fill="none" stroke="${FER}" stroke-width="${w}"/>`);
          g.push(`<circle cx="${B[0]}" cy="${B[1]}" r="${ZOOM ? 3.2 : 1.4}" fill="${FER}"/>`);
        }
      } else {
        // mixte : 40 cm de verre, 40 cm d'inox, en alternance
        for (const seg of gcSegments(b)) {
          if (seg.kind === 'verre') panneauVerre(seg.x1 + 0.012, seg.x2 - 0.012);
          else for (let m = Math.min(seg.x1, seg.x2) + 0.055; m < Math.max(seg.x1, seg.x2) - 0.02; m += 0.11)
            barreau(m, MAT.inox, ZOOM ? 3.4 : 1.5);
        }
      }
      // main courante, commune aux quatre
      const MC = GCTYPE === 'fer' ? (NUIT ? '#161A1E' : '#33353A') : MAT.inox;
      g.push(`<path d="${poly(C, hi, false)}" stroke="${MC}" stroke-width="${ZOOM ? 7 : 3}" fill="none" stroke-linecap="round"/>`);
      g.push(`<path d="${poly(C, hi.map(([x, y, zz]) => [x, y, zz - 0.014]), false)}" stroke="${NUIT ? '#C8D4DC' : '#FFFFFF'}" stroke-width="${ZOOM ? 2 : 1}" fill="none" opacity="0.7"/>`);
      g.push(`<path d="${poly(C, lo, false)}" stroke="${NUIT ? '#0A1017' : '#6E7A84'}" stroke-width="${ZOOM ? 2.6 : 1.2}" fill="none" opacity="0.55"/>`);
    }
  }
}

// ===========================================================================
// ACROTERE ET COUVERTINE
// ===========================================================================
{
  const zt = LV.toit, za = LV.acr;
  g.push(face([[0, 0, zt], [17.5, 0, zt], [17.5, 0, za], [0, 0, za]], S(MAT.mono, NY), 'filter="url(#crepi)"'));
  g.push(face([[0, 0.06, za], [17.5, 0.06, za], [17.5, -0.11, za + 0.04], [0, -0.11, za + 0.04]], S(MAT.alu, NZ, { kd: SH.kd * 0.9 })));
  g.push(face([[0, 0.06, za], [17.5, 0.06, za], [17.5, 0.06, za - 0.05], [0, 0.06, za - 0.05]], S(MAT.alu, NY, { kd: SH.kd * 0.7 })));
  g.push(`<path d="${poly(C, [[0, 0.06, za + 0.002], [17.5, 0.06, za + 0.002]], false)}" stroke="${NUIT ? '#7E8A96' : '#FFFFFF'}" stroke-width="1.4" fill="none" opacity="0.6"/>`);
  // retour sur le pignon
  g.push(face([[0, 0.06, za], [0, -PROF, za], [0, -PROF, za + 0.04], [0, 0.06, za + 0.04]], S(MAT.alu, NX, { kd: SH.kd * 0.5 })));
}

// ===========================================================================
// SOCLE PARKING — RDC + R+1, en avancee de 4,00 m
// ===========================================================================
{
  const zt = LV.r2;
  // pignon gauche du socle
  g.push(face([[0, AVANCEE, 0], [0, -PROF, 0], [0, -PROF, zt], [0, AVANCEE, zt]], S(MAT.mono, NX), 'filter="url(#crepi)"'));
  // face avant du socle
  g.push(face([[0, AVANCEE, 0], [17.5, AVANCEE, 0], [17.5, AVANCEE, zt], [0, AVANCEE, zt]], S(MAT.mono, NY), 'filter="url(#crepi)"'));
  // arete verticale de l'angle
  g.push(`<path d="${poly(C, [[0, AVANCEE, 0], [0, AVANCEE, zt]], false)}" stroke="${NUIT ? '#0B121B' : '#FFFFFF'}" stroke-width="1.6" fill="none" opacity="0.55"/>`);
  // plinthe : 60 cm de beton lisse teinte, elle encaisse les projections
  g.push(face([[0, AVANCEE, 0], [17.5, AVANCEE, 0], [17.5, AVANCEE, 0.60], [0, AVANCEE, 0.60]],
    S(NUIT ? '#2A2F36' : '#8E8A82', NY)));
  g.push(face([[0, AVANCEE, 0], [0, -PROF, 0], [0, -PROF, 0.60], [0, AVANCEE, 0.60]],
    S(NUIT ? '#232830' : '#8E8A82', NX)));
  g.push(`<path d="${poly(C, [[0, AVANCEE, 0.60], [17.5, AVANCEE, 0.60]], false)}" stroke="${NUIT ? '#12161C' : '#6F6A62'}" stroke-width="1.4" fill="none" opacity="0.7"/>`);
  // portes de garage
  for (const [a, b] of [[1.1, 6.4], [11.1, 16.4]]) {
    g.push(face([[a, AVANCEE + 0.02, 0], [b, AVANCEE + 0.02, 0], [b, AVANCEE + 0.02, 2.42], [a, AVANCEE + 0.02, 2.42]], NUIT ? '#0D1116' : '#22272B'));
    for (let z = 0.14; z < 2.42; z += 0.20)
      g.push(`<path d="${poly(C, [[a + 0.03, AVANCEE + 0.03, z], [b - 0.03, AVANCEE + 0.03, z]], false)}" stroke="${NUIT ? '#1B2128' : '#3A4046'}" stroke-width="1.6" fill="none"/>`);
    g.push(face([[a - 0.05, AVANCEE + 0.03, 2.42], [b + 0.05, AVANCEE + 0.03, 2.42], [b + 0.05, AVANCEE + 0.03, 2.54], [a - 0.05, AVANCEE + 0.03, 2.54]], S(MAT.alu, NY)));
  }
  // entree pietonne
  g.push(face([[7.9, AVANCEE + 0.02, 0], [9.6, AVANCEE + 0.02, 0], [9.6, AVANCEE + 0.02, 2.42], [7.9, AVANCEE + 0.02, 2.42]], S(MAT.alu, NY, { kd: SH.kd * 0.6 })));
  g.push(face([[8.05, AVANCEE + 0.04, 0.05], [9.45, AVANCEE + 0.04, 0.05], [9.45, AVANCEE + 0.04, 2.24], [8.05, AVANCEE + 0.04, 2.24]],
    NUIT ? 'url(#vitreLum)' : 'url(#vitre)', NUIT ? 'filter="url(#bloom)" opacity="0.9"' : ''));
  // bandeau de 80 cm de lames brise-vue au niveau R+1
  for (const [a, b] of [[0.55, 7.30], [7.85, 9.65], [10.20, 16.95]]) {
    const z0 = LV.r1 + 1.55;
    g.push(face([[a, AVANCEE + 0.01, z0], [b, AVANCEE + 0.01, z0], [b, AVANCEE + 0.01, z0 + 0.80], [a, AVANCEE + 0.01, z0 + 0.80]],
      NUIT ? '#10151B' : '#2A2E31'));
    for (let z = z0 + 0.06; z < z0 + 0.80; z += 0.11) {
      g.push(`<path d="${poly(C, [[a, AVANCEE + 0.03, z], [b, AVANCEE + 0.03, z]], false)}" stroke="${S(MAT.alu, NY, { kd: SH.kd * 1.1 })}" stroke-width="3.4" fill="none"/>`);
      g.push(`<path d="${poly(C, [[a, AVANCEE + 0.03, z + 0.026], [b, AVANCEE + 0.03, z + 0.026]], false)}" stroke="${NUIT ? '#05080B' : '#181B1E'}" stroke-width="1.2" fill="none" opacity="0.8"/>`);
    }
  }
  // couronnement du socle + terrasses du R+2
  g.push(face([[0, AVANCEE, zt], [17.5, AVANCEE, zt], [17.5, 0, zt], [0, 0, zt]], S(MAT.beton, NZ, { kd: SH.kd * 0.55 })));
  g.push(face([[0, AVANCEE, zt], [17.5, AVANCEE, zt], [17.5, AVANCEE, zt + 0.10], [0, AVANCEE, zt + 0.10]], S(MAT.alu, NY, { kd: SH.kd * 0.8 })));
  const gcT = (a, b, y1, y2) => {
    const pts = [[a, y1, zt + 1.20], [b, y2, zt + 1.20]];
    g.push(face([[a, y1, zt + 0.14], [b, y2, zt + 0.14], [b, y2, zt + 1.16], [a, y1, zt + 1.16]],
      NUIT ? '#0A1017' : '#232C33', 'opacity="0.5"'));
    g.push(`<path d="${poly(C, pts, false)}" stroke="${MAT.inox}" stroke-width="2.6" fill="none" stroke-linecap="round"/>`);
    const n = Math.max(2, Math.round(Math.hypot(b - a, y2 - y1) / 1.35));
    for (let k = 0; k <= n; k++) {
      const t = k / n, mm = a + (b - a) * t, yy = y1 + (y2 - y1) * t;
      g.push(`<path d="${poly(C, [[mm, yy, zt + 0.14], [mm, yy, zt + 1.20]], false)}" stroke="${MAT.inox}" stroke-width="1.6" fill="none" opacity="0.85"/>`);
    }
  };
  gcT(0.1, 17.4, AVANCEE - 0.12, AVANCEE - 0.12);
  gcT(XS.vide[0], XS.vide[0], AVANCEE - 0.12, 0.1);
  gcT(XS.vide[1], XS.vide[1], AVANCEE - 0.12, 0.1);
}

// contact au sol : le trait sombre sans lequel un batiment flotte
{
  const ao = [];
  for (let x = 0; x <= 17.5; x += 0.5) ao.push([x, AVANCEE, 0.001]);
  g.push(`<path d="${poly(C, [...ao, [17.5, AVANCEE + 0.55, 0.001], ...ao.slice().reverse().map(([x, y, z]) => [x, y + 0.55, z])])}"
    fill="#161A20" opacity="0.42" filter="url(#flou6)"/>`);
  g.push(`<path d="${poly(C, [[0, AVANCEE, 0.004], [17.5, AVANCEE, 0.004]], false)}" stroke="#191D22" stroke-width="2.6" fill="none" opacity="0.42"/>`);
  g.push(`<path d="${poly(C, [[0, AVANCEE, 0.004], [0, -PROF, 0.004]], false)}" stroke="#191D22" stroke-width="2.6" fill="none" opacity="0.42"/>`);
}

// ===========================================================================
// PREMIER PLAN — echelle humaine, voitures, arbres
// ===========================================================================
const ombreSol = (x, y, rx, ry, op = 0.30) => {
  const s = castZ([x, y, 0], 0), q = P([s[0], s[1], 0.02]);
  if (!Number.isFinite(q[0])) return '';
  const k = P([x + rx, y, 0.02]);
  return `<ellipse cx="${q[0]}" cy="${q[1]}" rx="${Math.abs(k[0] - P([x, y, 0.02])[0]) * 1.6}" ry="${Math.abs(k[0] - P([x, y, 0.02])[0]) * 0.42}" fill="#12161C" opacity="${op}" filter="url(#flou3)"/>`;
};

const personne = (x, y, h, col) => {
  const o = [];
  if (!NUIT) {
    const s0 = castZ([x, y, 0.02], 0.02), s1 = castZ([x, y, h], 0.02);
    o.push(`<path d="${poly(C, [[x - 0.16, y, 0.02], [x + 0.16, y, 0.02], [s1[0] + 0.16, s1[1], 0.02], [s1[0] - 0.16, s1[1], 0.02]])}"
      fill="#141920" opacity="0.32" filter="url(#flou3)"/>`);
  }
  const b0 = P([x, y, 0.16]), t0 = P([x, y, 0.16 + h]);
  if (!Number.isFinite(b0[0])) return '';
  const u = Math.abs(P([x + 0.10, y, 0.16])[0] - b0[0]);      // 10 cm en px
  const hp = b0[1] - t0[1];
  const X0 = b0[0], Y0 = b0[1];
  o.push(`<path d="
    M ${X0 - u * 1.0} ${Y0}
    L ${X0 - u * 0.9} ${Y0 - hp * 0.46}
    L ${X0 - u * 1.85} ${Y0 - hp * 0.52}
    Q ${X0 - u * 2.2} ${Y0 - hp * 0.76} ${X0 - u * 1.5} ${Y0 - hp * 0.80}
    L ${X0 - u * 0.62} ${Y0 - hp * 0.815}
    L ${X0 + u * 0.62} ${Y0 - hp * 0.815}
    L ${X0 + u * 1.5} ${Y0 - hp * 0.80}
    Q ${X0 + u * 2.2} ${Y0 - hp * 0.76} ${X0 + u * 1.85} ${Y0 - hp * 0.52}
    L ${X0 + u * 0.9} ${Y0 - hp * 0.46}
    L ${X0 + u * 1.0} ${Y0}
    L ${X0 + u * 0.16} ${Y0}
    L ${X0} ${Y0 - hp * 0.42}
    L ${X0 - u * 0.16} ${Y0} Z" fill="${col}" opacity="0.94"/>`);
  o.push(`<ellipse cx="${X0}" cy="${Y0 - hp * 0.905}" rx="${u * 0.78}" ry="${u * 0.95}" fill="${col}" opacity="0.94"/>`);
  o.push(`<rect x="${X0 - u * 0.28}" y="${Y0 - hp * 0.845}" width="${u * 0.56}" height="${hp * 0.035}" fill="${col}" opacity="0.94"/>`);
  return o.join('');
};

const voiture = (x, y, L, col, sens = 1) => {
  const o = [];
  const p = (dx, dy, dz) => [x + dx * sens, y + dy, dz];
  if (!NUIT) o.push(`<path d="${poly(C, [castZ(p(-L / 2, -0.85, 1.45), 0.02), castZ(p(L / 2, -0.85, 1.45), 0.02),
    castZ(p(L / 2, 0.85, 1.45), 0.02), castZ(p(-L / 2, 0.85, 1.45), 0.02)])}" fill="#101418" opacity="0.34" filter="url(#flou6)"/>`);
  o.push(face([p(-L / 2, 0.85, 0.28), p(L / 2, 0.85, 0.28), p(L / 2, 0.85, 0.95), p(-L / 2, 0.85, 0.95)], col));
  o.push(`<path d="${poly(C, [p(-L / 2 + 0.35, 0.85, 0.95), p(-L / 2 + 1.15, 0.85, 1.45),
    p(L / 2 - 1.25, 0.85, 1.45), p(L / 2 - 0.35, 0.85, 0.95)])}" fill="${NUIT ? '#0A0F14' : '#2A3238'}"/>`);
  o.push(`<path d="${poly(C, [p(-L / 2 + 0.48, 0.86, 0.99), p(-L / 2 + 1.22, 0.86, 1.40),
    p(L / 2 - 1.32, 0.86, 1.40), p(L / 2 - 0.48, 0.86, 0.99)])}" fill="${NUIT ? '#141C24' : '#8FA8B6'}" opacity="0.75"/>`);
  o.push(face([p(-L / 2, 0.85, 0.24), p(L / 2, 0.85, 0.24), p(L / 2, 0.85, 0.30), p(-L / 2, 0.85, 0.30)], '#15181C'));
  for (const dx of [-L / 2 + 0.9, L / 2 - 0.9]) {
    const c = P(p(dx, 0.84, 0.32)), r = Math.abs(P(p(dx + 0.32, 0.84, 0.32))[0] - c[0]);
    o.push(`<circle cx="${c[0]}" cy="${c[1]}" r="${r}" fill="#191C20"/><circle cx="${c[0]}" cy="${c[1]}" r="${r * 0.5}" fill="#4A5057"/>`);
  }
  if (NUIT) for (const dx of [-L / 2 + 0.15, L / 2 - 0.15])
    o.push(`<circle cx="${P(p(dx, 0.85, 0.62))[0]}" cy="${P(p(dx, 0.85, 0.62))[1]}" r="5" fill="#FFE9B0" filter="url(#bloom)"/>`);
  return o.join('');
};

const palmier = (x, y, h) => {
  const o = [];
  if (!NUIT) o.push(`<path d="${poly(C, [castZ([x - 0.2, y, h], 0.02), castZ([x + 0.2, y, h], 0.02), [x + 0.2, y, 0.02], [x - 0.2, y, 0.02]])}" fill="#141A20" opacity="0.26" filter="url(#flou6)"/>`);
  const b = P([x, y, 0.16]), t = P([x, y, h]);
  if (!Number.isFinite(b[0])) return '';
  const wpx = Math.abs(P([x + 0.16, y, 0.16])[0] - b[0]);
  o.push(`<path d="M ${b[0] - wpx} ${b[1]} Q ${b[0] - wpx * 0.4} ${(b[1] + t[1]) / 2} ${t[0] - wpx * 0.55} ${t[1]}
    L ${t[0] + wpx * 0.55} ${t[1]} Q ${b[0] + wpx * 0.4} ${(b[1] + t[1]) / 2} ${b[0] + wpx} ${b[1]} Z"
    fill="${NUIT ? '#2A2A26' : '#8A7C64'}"/>`);
  const R = Math.abs(P([x + 2.3, y, h])[0] - t[0]);
  for (let k = 0; k < 11; k++) {
    const a = -Math.PI + k * Math.PI / 10, ex = t[0] + Math.cos(a) * R, ey = t[1] + Math.sin(a) * R * 0.5 + R * 0.16;
    o.push(`<path d="M ${t[0]} ${t[1]} Q ${(t[0] + ex) / 2 + Math.cos(a) * 6} ${(t[1] + ey) / 2 - R * 0.30} ${ex} ${ey}"
      stroke="${NUIT ? '#1D3026' : ['#4E6B3A', '#5C7A44', '#435E32'][k % 3]}" stroke-width="${(R * 0.10).toFixed(1)}" fill="none" stroke-linecap="round" opacity="0.95"/>`);
  }
  return o.join('');
};

g.push(voiture(24.5, 10.8, 4.5, NUIT ? '#20262C' : '#9AA3AB', 1));
g.push(voiture(2.0, 9.6, 4.7, NUIT ? '#1B2228' : '#3E4A57', 1));
g.push(voiture(13.5, 16.5, 4.4, NUIT ? '#171C22' : '#C7C3BC', 1));
g.push(palmier(-3.4, 6.2, 7.4));
g.push(palmier(21.8, 6.4, 6.6));
g.push(personne(6.6, 5.9, 1.74, NUIT ? '#12161B' : '#39404A'));
g.push(personne(7.35, 6.15, 1.66, NUIT ? '#141920' : '#6B5F62'));
g.push(personne(15.2, 5.7, 1.78, NUIT ? '#10151A' : '#2C3640'));
// lampadaire
{
  const x = 18.5, y = 6.4, h = 8.2;
  g.push(`<path d="${poly(C, [[x, y, 0.16], [x, y, h], [x - 1.6, y, h + 0.25]], false)}" stroke="${NUIT ? '#2A2F36' : '#7C818A'}" stroke-width="3" fill="none"/>`);
  if (NUIT) g.push(`<circle cx="${P([x - 1.6, y, h + 0.25])[0]}" cy="${P([x - 1.6, y, h + 0.25])[1]}" r="9" fill="#FFDDA0" filter="url(#bloom)"/>`);
}

// ===========================================================================
// POST — voile atmospherique, vignettage, grain
// ===========================================================================
g.push(`<rect x="0" y="0" width="${W}" height="${H}" fill="${NUIT ? '#0E1E38' : '#BFD6E8'}" opacity="${NUIT ? 0.10 : 0.07}"/>`);
g.push(`<rect x="0" y="0" width="${W}" height="${H}" fill="url(#vign)"/>`);
g.push(`<rect x="0" y="0" width="${W}" height="${H}" filter="url(#grain)" opacity="${NUIT ? 0.10 : 0.055}" style="mix-blend-mode:overlay"/>`);
g.push(`</g>`);

const svg = `<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" xmlns="http://www.w3.org/2000/svg" style="display:block">${g.join('\n')}</svg>`;
const stem = `photo-${NUIT ? 'nuit' : 'jour'}-${GCTYPE}${ZOOM ? '-zoom' : ''}`;
writeFileSync(stem + '.html',
  `<!doctype html><html><head><meta charset="utf-8"><style>@page{size:${(W / 96 * 25.4).toFixed(2)}mm ${(H / 96 * 25.4).toFixed(2)}mm;margin:0}html,body{margin:0;padding:0;background:${NUIT ? '#000' : '#fff'}}</style></head><body>${svg}</body></html>`);
const NOMGC = { verre: 'garde-corps tout verre', fer: 'garde-corps en fer forgé',
                inox: 'garde-corps tout inox', mixte: 'garde-corps mixte verre / inox' }[GCTYPE] || GCTYPE;
const body = `<div style="width: ${W}px; background: ${NUIT ? '#0A0F18' : '#FFFFFF'}">
${header({ w: W, kicker: `Perspective · ${ZOOM ? 'détail de façade' : 'rue'} · ${NUIT ? 'nuit' : 'jour'}`,
  title: ZOOM ? 'Le détail, à hauteur de balcon' : 'L’immeuble depuis la rue',
  sub: `${NOMGC.charAt(0).toUpperCase() + NOMGC.slice(1)}. Façade ventilée en travertin sur les quatre poteaux, saillie 13 cm sur ossature, joints creux ouverts tous les 1,20 m. Cadrage Alucobond RAL 7024 de 18 cm autour de chaque porte-balcon, en saillie de 5 cm. Onde de rive : grand lobe 1,80 m, creux 0,79 m, petit lobe 1,45 m — ${developpe().toFixed(2)} ml développés.`,
  right: (NUIT ? 'VUE DE NUIT' : 'VUE DE JOUR') + '<br>NON COTÉE<br>' + NOMGC.toUpperCase() })}
${svg}
</div>`;
writeFileSync(`Photo-${NUIT ? 'Nuit' : 'Jour'}-${GCTYPE}${ZOOM ? '-Zoom' : ''}.dc.html`,
  page({ body, props: JSON.stringify({ $preview: { width: W, height: H + 220 } }) }));
console.log(stem, 'ok —', (svg.length / 1024).toFixed(0), 'Ko');
