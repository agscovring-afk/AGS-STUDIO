// ---------------------------------------------------------------------------
// Geometrie partagee - Facade principale, batiment R+6
// Toutes les valeurs en METRES. Releve client :
//   largeur totale 17.50 | poteau 0.55 | baie balcon ~7.00 | vide central ~1.80
// ---------------------------------------------------------------------------
export const W = 17.50;
export const COL = 0.55;
export const BAY = 6.75;      // ouverture libre entre nus de poteaux
export const VOID = 1.80;     // vide central
export const PBW = 1.80;      // porte-balcon alu
export const PBH = 2.20;
export const MENUISERIE = 'Aluminium TPR série 65 à rupture de pont thermique, RAL 7024 gris graphite';
export const FASCIA = 0.45;   // bandeau courbe Aquapanel (retombee de rive)
export const GC = 1.10;       // garde-corps
export const AVANCEE = 4.00;  // avancee parking RDC + R+1
export const BLOC = 7.85;     // largeur d'un bloc

// Decoupage horizontal : 0.55 + 6.75 + 0.55 + 1.80 + 0.55 + 6.75 + 0.55 = 17.50
export const XS = {
  c1:   [0.00,  0.55],
  bayA: [0.55,  7.30],
  c2:   [7.30,  7.85],
  vide: [7.85,  9.65],
  c3:   [9.65, 10.20],
  bayB: [10.20, 16.95],
  c4:   [16.95, 17.50],
};
export const BLOCS = [[0, 7.85], [9.65, 17.50]];
export const MIROIR = [true, false];   // le croquis porte sur le bloc droit ; le gauche en est le miroir

// Niveaux, calcules depuis les cotes du chantier :
//   3,06 m de hauteur libre entre dalles + 0,20 m d'epaisseur de dalle
//   = 3,26 m d'un nu superieur de dalle au suivant.
// RDC + R+1 en parking, R+2 en terrasses, puis SIX niveaux de balcons ondules.
export const HSP = 3.06;       // hauteur libre sous dalle, etages courants
export const HSP_RDC = 2.60;   // hauteur libre du RDC
export const DALLE = 0.20;     // epaisseur de dalle
export const ACROTERE = 1.00;
const _h = HSP + DALLE;        // 3,26 m d'un nu de dalle au suivant
const _r = HSP_RDC + DALLE;    // 2,80 m au RDC
const _n = (k) => _r + (k - 1) * _h;
export const LV = {
  rdc: 0, r1: _r, r2: _n(2), r3: _n(3), r4: _n(4), r5: _n(5),
  r6: _n(6), r7: _n(7), r8: _n(8), toit: _n(9), acr: _n(9) + ACROTERE,
};
export const BALCONS = [LV.r3, LV.r4, LV.r5, LV.r6, LV.r7, LV.r8];
const _alt = (h) => (h === 0 ? '± 0.00' : '+ ' + h.toFixed(2));
export const ETAGES = [
  [LV.rdc, _alt(LV.rdc), 'RDC — PARKING'], [LV.r1, _alt(LV.r1), 'R+1 — PARKING'],
  [LV.r2, _alt(LV.r2), 'R+2 — TERRASSES'], [LV.r3, _alt(LV.r3), 'R+3'],
  [LV.r4, _alt(LV.r4), 'R+4'], [LV.r5, _alt(LV.r5), 'R+5'], [LV.r6, _alt(LV.r6), 'R+6'],
  [LV.r7, _alt(LV.r7), 'R+7'], [LV.r8, _alt(LV.r8), 'R+8 — DERNIER NIVEAU'],
  [LV.toit, _alt(LV.toit), 'TOITURE'], [LV.acr, _alt(LV.acr), 'HAUT ACROTERE'],
];
export const NIVEAUX_LOGEMENT = [LV.r2, LV.r3, LV.r4, LV.r5, LV.r6, LV.r7, LV.r8];
export const HET = _h;
export const HTOT = LV.acr;

// Portes-balcon : 0.90 | 1.80 | 1.35 | 1.80 | 0.90 = 6.75
export function doors(bay) {
  const [a] = bay;
  return [[a + 0.90, a + 2.70], [a + 4.05, a + 5.85]];
}

// ---------------------------------------------------------------------------
// ONDE DE RIVE — troisieme releve : la rive est tracee AU COMPAS.
// Elle part du nu de facade au droit du poteau, reste droite jusqu'a la
// premiere porte, puis decrit trois demi-cercles tangents au nu :
//   deux GRANDS de diametre 1.80 m — soit exactement la largeur d'une
//   porte-balcon — un devant chaque porte, et un PETIT de diametre 1.10 m
//   entre les deux. Elle revient au nu de facade au droit du second poteau.
// Chaque lobe se trace a la ficelle depuis un centre pose sur le nu.
// ---------------------------------------------------------------------------
export const R_GRAND = 0.90;   // demi-cercle de 1.80 m de diametre
export const R_PETIT = 0.55;   // demi-cercle de 1.10 m de diametre

// centres des lobes, en abscisse locale depuis le bord de bloc
export const LOBES = [
  { c: 2.35, r: R_GRAND },   // devant la premiere porte-balcon
  { c: 3.925, r: R_PETIT },  // entre les deux portes
  { c: 5.50, r: R_GRAND },   // devant la seconde porte-balcon
];

export function ondeAt(u) {
  const x = Math.min(BLOC, Math.max(0, u));
  for (const { c, r } of LOBES) {
    const d = x - c;
    if (Math.abs(d) <= r) return Math.sqrt(r * r - d * d);
  }
  return 0;
}

export const DMIN = 0.00, DCREUX = 0.55, DMAX = 0.90;   // au nu · lobe petit · lobe grand

export function depthAt(m, b) {
  const [a, z] = BLOCS[b];
  return ondeAt(MIROIR[b] ? z - m : m - a);
}
export const blocOf = (m) => (m <= 8.75 ? 0 : 1);

export function developpe(n = 4000) {
  let L = 0, px = 0, py = ondeAt(0);
  for (let i = 1; i <= n; i++) {
    const x = BLOC * i / n, y = ondeAt(x);
    L += Math.hypot(x - px, y - py); px = x; py = y;
  }
  return L;
}

// rayon de courbure de la rive a l'abscisse locale u
export function rayonAt(u, h = 0.02) {
  const y0 = ondeAt(u - h), y1 = ondeAt(u), y2 = ondeAt(u + h);
  const d1 = (y2 - y0) / (2 * h), d2 = (y2 - 2 * y1 + y0) / (h * h);
  return Math.abs(d2) < 1e-9 ? Infinity : Math.pow(1 + d1 * d1, 1.5) / Math.abs(d2);
}

// ---------------------------------------------------------------------------
// Garde-corps mixte inox / verre.
// Un panneau de verre feuillete plat de ~1,10 m ne suit une rive courbe que si
// le rayon reste grand : en dessous de R_VERRE la fleche du panneau devient
// visible, on passe au barreaudage inox qui epouse n'importe quel rayon.
// ---------------------------------------------------------------------------
export const GC_MINI = 0.45;   // longueur mini d'un segment, pour rester posable

// Le verre feuillete plat ne suit une rive que la ou elle est droite. Les trois
// lobes sont des arcs de 0.55 et 0.90 m de rayon : trop serres pour du verre,
// on les fait en barreaudage inox. Les parties droites prennent le verre.
export function gcSegmentsLocal() {
  const cuts = [];
  for (const { c, r } of LOBES) cuts.push([c - r, c + r]);
  const out = [];
  let cursor = 0;
  for (const [a, b] of cuts) {
    if (a > cursor + 1e-6) out.push({ kind: a - cursor < GC_MINI ? 'inox' : 'verre', x1: cursor, x2: a });
    out.push({ kind: 'inox', x1: a, x2: b });
    cursor = b;
  }
  if (cursor < BLOC - 1e-6) out.push({ kind: 'verre', x1: cursor, x2: BLOC });
  // fusionner les voisins de meme nature
  const m = [out[0]];
  for (let i = 1; i < out.length; i++) {
    if (out[i].kind === m[m.length - 1].kind) m[m.length - 1].x2 = out[i].x2;
    else m.push(out[i]);
  }
  return m;
}

// segments d'un bloc, exprimes en abscisses de facade et dans l'ordre croissant
export function gcSegments(b) {
  const [a, z] = BLOCS[b], loc = gcSegmentsLocal();
  const segs = loc.map((s) => MIROIR[b]
    ? { kind: s.kind, x1: z - s.x2, x2: z - s.x1 }
    : { kind: s.kind, x1: a + s.x1, x2: a + s.x2 });
  return segs.sort((p, q) => p.x1 - q.x1);
}

export const fmt = (v, d = 2) => v.toFixed(d);

// Vide central : sous la terrasse il est plein et avance avec le socle parking ;
// au-dessus il se creuse de 1,50 m en arriere du nu de facade.
export const RETRAIT = 1.50;
