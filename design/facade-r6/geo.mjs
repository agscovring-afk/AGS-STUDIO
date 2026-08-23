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
// ONDE DE RIVE — relevee sur le croquis du maitre d'ouvrage (bloc droit).
// Points de controle : abscisse depuis le bord de bloc, profondeur du balcon.
// Raccord en cosinus releve : tangente horizontale a chaque extremum, donc
// une courbe continue, derivable, et de courbure bornee.
// ---------------------------------------------------------------------------
// ---------------------------------------------------------------------------
// ONDE DE RIVE — deuxieme releve, croquis du 23.08 repris sur le plan de detail.
// La rive part du nu de facade au droit des poteaux, plonge franchement, puis
// file a plat au fond de chaque lobe avant de remonter au creux median.
// Points de controle : abscisse depuis le bord de bloc, profondeur.
// Raccord en cosinus releve : tangente horizontale a chaque point, donc des
// fonds de lobe VRAIMENT plats et des transitions douces mais franches.
// ---------------------------------------------------------------------------
export const ONDE = [
  [0.00, 0.00],   // depart au nu de facade, contre le poteau
  [0.90, 1.58],   // plongee du premier lobe
  [2.45, 1.58],   // fond plat
  [3.90, 0.79],   // creux median
  [5.45, 1.42],   // second lobe
  [7.05, 1.42],   // fond plat
  [7.85, 0.00],   // retour au nu de facade, contre le poteau
];

export function ondeAt(u) {
  const x = Math.min(BLOC, Math.max(0, u));
  for (let i = 0; i < ONDE.length - 1; i++) {
    const [x0, y0] = ONDE[i], [x1, y1] = ONDE[i + 1];
    if (x <= x1 || i === ONDE.length - 2) {
      const t = (x - x0) / (x1 - x0);
      return y0 + (y1 - y0) * (1 - Math.cos(Math.PI * t)) / 2;
    }
  }
  return ONDE[ONDE.length - 1][1];
}

export const DMIN = 0.00, DCREUX = 0.79, DMAX = 1.58;   // au droit des poteaux · creux median · fond de lobe

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
export const GC_INOX = 0.30;   // demi-largeur du barreaudage autour d'un point de controle
export const GC_MINI = 0.45;   // longueur mini d'un segment, pour rester posable

// Le verre feuillete plat ne suit une rive que la ou elle est droite. Avec un
// raccord en cosinus la courbure est nulle au milieu de chaque portee et
// maximale aux points de controle : on met donc du barreaudage inox autour de
// chaque point de controle, du verre entre les deux.
export function gcSegmentsLocal() {
  let segs = [];
  for (const [x] of ONDE) segs.push({ kind: 'inox', x1: Math.max(0, x - GC_INOX), x2: Math.min(BLOC, x + GC_INOX) });
  // fusionner les zones inox qui se chevauchent ou laissent un verre trop court
  const merged = [segs[0]];
  for (let i = 1; i < segs.length; i++) {
    const prev = merged[merged.length - 1];
    if (segs[i].x1 - prev.x2 < GC_MINI) prev.x2 = segs[i].x2;
    else merged.push(segs[i]);
  }
  // intercaler le verre
  const out = [];
  let cursor = 0;
  for (const seg of merged) {
    if (seg.x1 > cursor + 1e-6) out.push({ kind: 'verre', x1: cursor, x2: seg.x1 });
    out.push(seg); cursor = seg.x2;
  }
  if (cursor < BLOC - 1e-6) out.push({ kind: 'verre', x1: cursor, x2: BLOC });
  return out;
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
