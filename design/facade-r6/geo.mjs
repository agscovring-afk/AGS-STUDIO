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
// ---------------------------------------------------------------------------
// Vide central. Precise les 23.08 : ce n'est pas un panneau de brise-vue tendu
// en facade. C'est une fente de 1,80 m creusee de 1,50 m dans la facade — le
// « vide » — et au fond de cette fente, DEUX petits balcons cote a cote, un par
// logement, avec le brise-vue ENTRE EUX.
//   . le fond de la fente, a 1,50 m du nu : le mur du logement et sa porte
//   . le balcon : 0,80 m de profondeur depuis la porte  -> son garde-corps
//     verre s'arrete a 0,70 m en arriere du nu de facade
//   . le brise-vue : 40 cm de large, sur l'axe, du fond au garde-corps, sur
//     toute la hauteur d'etage
// ---------------------------------------------------------------------------
export const AXE = 8.75;              // axe du vide, mitoyen des deux logements
export const BV_EP = 0.40;            // largeur du brise-vue separateur
export const JOUE = 0.00;             // pas de joue : les flancs sont ceux des blocs
export const BALCON_NICHE = (1.80 - BV_EP) / 2;   // 0.70 m de large par balcon
export const BALCON_NICHE_P = 0.80;   // profondeur, de la porte au garde-corps
export const GCN = 0.70;              // recul du garde-corps = 1.50 - 0.80
export const PBN = 0.70;              // porte-fenetre de ces balcons

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
// ONDE DE RIVE — tracé arrêté sur le croquis annoté du maître d'ouvrage.
// La rive part du nu de façade au droit du poteau, creuse un GRAND lobe de
// 1,80 m de profondeur, remonte à 0,79 m entre les deux portes, creuse un
// PETIT lobe de 1,10 m, puis revient au nu au droit du second poteau.
// Les profondeurs 1,80 et 1,10 sont celles relevées sur le croquis (traits
// rouge et jaune). Le trait noir du 23.08 précise la façon dont la rive quitte
// le poteau : elle en part perpendiculairement au nu, comme un demi-cercle qui
// prend naissance sur la façade, et non en s'écartant doucement. Les deux
// portées d'extrémité sont donc des quarts d'ellipse (tangente perpendiculaire
// au nu, tangente horizontale au sommet du lobe) et les portées intérieures un
// raccord en cosinus (tangente horizontale aux deux bouts, donc fond de lobe et
// creux médian bien plats). Courbe continue, dérivable, de courbure bornée.
// ---------------------------------------------------------------------------
export const ONDE = [
  [0.00, 0.00],   // au nu de façade, contre le poteau
  [1.96, 1.80],   // grand lobe
  [3.92, 0.79],   // creux médian, entre les deux portes
  [5.64, 1.10],   // petit lobe
  [7.85, 0.00],   // retour au nu, contre le second poteau
];

export function ondeAt(u) {
  const x = Math.min(BLOC, Math.max(0, u)), n = ONDE.length;
  for (let i = 0; i < n - 1; i++) {
    const [x0, y0] = ONDE[i], [x1, y1] = ONDE[i + 1];
    if (x > x1 && i < n - 2) continue;
    const t = (x - x0) / (x1 - x0);
    // naissance sur le poteau : quart d'ellipse, la rive part perpendiculaire au nu
    if (i === 0) return y1 * Math.sqrt(Math.max(0, 1 - (1 - t) * (1 - t)));
    // retour sur le second poteau : le quart d'ellipse symetrique
    if (i === n - 2) return y0 * Math.sqrt(Math.max(0, 1 - t * t));
    // entre deux extremums : raccord en cosinus, fonds plats
    return y0 + (y1 - y0) * (1 - Math.cos(Math.PI * t)) / 2;
  }
  return 0;
}

export const DMIN = 0.00, DCREUX = 0.79, DMAX = 1.80;   // au nu · creux médian · grand lobe
export const DPETIT = 1.10;                            // petit lobe

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
export const GC_PAS = 0.40;   // pas du garde-corps : 40 cm de verre, 40 cm d'inox

// Table longueur developpee <-> abscisse locale, pour poser le garde-corps au
// metre lineaire reel de la rive et non a la projection horizontale.
function arcTable(n = 4000) {
  const u = [0], s = [0];
  let px = 0, py = ondeAt(0), L = 0;
  for (let i = 1; i <= n; i++) {
    const x = BLOC * i / n, y = ondeAt(x);
    L += Math.hypot(x - px, y - py); px = x; py = y;
    u.push(x); s.push(L);
  }
  return { u, s, L };
}
function uAtArc(T, tab) {
  const { u, s } = tab, last = s.length - 1;
  if (T <= 0) return 0;
  if (T >= s[last]) return BLOC;
  let lo = 0, hi = last;
  while (hi - lo > 1) { const mid = (lo + hi) >> 1; if (s[mid] <= T) lo = mid; else hi = mid; }
  const f = (T - s[lo]) / ((s[hi] - s[lo]) || 1);
  return u[lo] + (u[hi] - u[lo]) * f;
}

// Le garde-corps alterne, sur toute la longueur developpee, un panneau de verre
// feuillete de 40 cm et un panneau de barreaudage inox de 40 cm. Un plat de
// 40 cm epouse n'importe quel rayon de la rive sans fleche visible : c'est ce
// qui rend le verre posable sur une courbe. Le pas est ajuste au centimetre
// pres pour tomber juste sur les deux poteaux.
export function gcSegmentsLocal() {
  const tab = arcTable(), L = tab.L;
  const nb = Math.max(2, 2 * Math.round(L / (2 * GC_PAS)));   // nombre pair : verre aux deux bouts
  const pas = L / nb;
  const out = [];
  for (let k = 0; k < nb; k++)
    out.push({ kind: k % 2 ? 'inox' : 'verre', ml: pas,
               x1: uAtArc(k * pas, tab), x2: uAtArc((k + 1) * pas, tab) });
  return out;
}

// segments d'un bloc, exprimes en abscisses de facade et dans l'ordre croissant
export function gcSegments(b) {
  const [a, z] = BLOCS[b], loc = gcSegmentsLocal();
  const segs = loc.map((s) => MIROIR[b]
    ? { kind: s.kind, ml: s.ml, x1: z - s.x2, x2: z - s.x1 }
    : { kind: s.kind, ml: s.ml, x1: a + s.x1, x2: a + s.x2 });
  return segs.sort((p, q) => p.x1 - q.x1);
}

export const fmt = (v, d = 2) => v.toFixed(d);

// Vide central : sous la terrasse il est plein et avance avec le socle parking ;
// au-dessus il se creuse de 1,50 m en arriere du nu de facade.
export const RETRAIT = 1.50;
