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
// Onde de rive RELEVEE sur le croquis du maitre d'ouvrage (bloc droit,
// planche « Dessine l'onde de rive », retour du 23.08.2026).
// 33 profondeurs regulierement reparties du bord gauche au bord droit
// du bloc, interpolees par un cubique monotone (Fritsch-Carlson) : pas
// d'oscillation parasite, tangentes continues, longueur developpee preservee.
export const ONDE_RELEVEE = [0.52, 0.80, 1.12, 1.40, 1.47, 1.50, 1.55, 1.59, 1.60, 1.57, 1.50, 1.39, 1.24, 1.08, 0.94, 0.84, 0.79, 0.80, 0.88, 1.05, 1.25, 1.36, 1.40, 1.41, 1.40, 1.38, 1.35, 1.30, 1.23, 1.12, 0.96, 0.66, 0.38];

const _m = (() => {                       // pentes monotones, calculees une fois
  const y = ONDE_RELEVEE, n = y.length, h = BLOC / (n - 1);
  const d = [], m = new Array(n).fill(0);
  for (let i = 0; i < n - 1; i++) d.push((y[i + 1] - y[i]) / h);
  m[0] = d[0]; m[n - 1] = d[n - 2];
  for (let i = 1; i < n - 1; i++) m[i] = d[i - 1] * d[i] <= 0 ? 0 : (d[i - 1] + d[i]) / 2;
  for (let i = 0; i < n - 1; i++) {
    if (d[i] === 0) { m[i] = 0; m[i + 1] = 0; continue; }
    const a = m[i] / d[i], b = m[i + 1] / d[i], s = a * a + b * b;
    if (s > 9) { const t = 3 / Math.sqrt(s); m[i] = t * a * d[i]; m[i + 1] = t * b * d[i]; }
  }
  return m;
})();

export function ondeAt(u) {
  const y = ONDE_RELEVEE, n = y.length, h = BLOC / (n - 1);
  const x = Math.min(BLOC, Math.max(0, u));
  let i = Math.min(n - 2, Math.floor(x / h));
  const t = (x - i * h) / h, t2 = t * t, t3 = t2 * t;
  return (2 * t3 - 3 * t2 + 1) * y[i] + (t3 - 2 * t2 + t) * h * _m[i]
       + (-2 * t3 + 3 * t2) * y[i + 1] + (t3 - t2) * h * _m[i + 1];
}


export const DMIN = 0.38, DCREUX = 0.79, DMAX = 1.61;   // bords · creux median · crete

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
export const R_VERRE = 3.00;
export const GC_MINI = 0.45;   // longueur mini d'un segment, pour rester posable

export function gcSegmentsLocal() {
  const step = 0.025, n = Math.round(BLOC / step);
  const raw = [];
  for (let i = 0; i < n; i++) raw.push(rayonAt((i + 0.5) * step) < R_VERRE ? 'inox' : 'verre');
  // regrouper
  let segs = [];
  let cur = { kind: raw[0], x1: 0, x2: step };
  for (let i = 1; i < n; i++) {
    if (raw[i] === cur.kind) cur.x2 = (i + 1) * step;
    else { segs.push(cur); cur = { kind: raw[i], x1: i * step, x2: (i + 1) * step }; }
  }
  cur.x2 = BLOC; segs.push(cur);
  // absorber les segments trop courts dans le voisin
  let changed = true;
  while (changed && segs.length > 1) {
    changed = false;
    for (let i = 0; i < segs.length; i++) {
      if (segs[i].x2 - segs[i].x1 >= GC_MINI) continue;
      const prev = segs[i - 1], next = segs[i + 1];
      const host = !prev ? next : !next ? prev
        : (prev.x2 - prev.x1) >= (next.x2 - next.x1) ? prev : next;
      if (host === prev) host.x2 = segs[i].x2; else host.x1 = segs[i].x1;
      segs.splice(i, 1); changed = true; break;
    }
  }
  // fusionner les voisins de meme nature
  const out = [segs[0]];
  for (let i = 1; i < segs.length; i++) {
    if (segs[i].kind === out[out.length - 1].kind) out[out.length - 1].x2 = segs[i].x2;
    else out.push(segs[i]);
  }
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
