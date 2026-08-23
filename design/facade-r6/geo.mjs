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
export const PBH = 2.40;
export const FASCIA = 0.45;   // bandeau courbe Aquapanel (retombee de rive)
export const GC = 1.10;       // garde-corps verre + inox
export const AVANCEE = 4.00;  // avancee parking RDC + R+1
export const DMIN = 1.30;     // profondeur balcon au creux de l'onde
export const DMAX = 3.00;     // profondeur balcon a la crete
export const LOBES = 2;       // nombre d'ondes par balcon

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

// Niveaux (altitude du nu superieur de dalle)
export const LV = {
  rdc: 0.00, r1: 3.40, r2: 6.46, r3: 9.52,
  r4: 12.58, r5: 15.64, r6: 18.70, toit: 21.76, acr: 22.76,
};
export const BALCONS = [LV.r3, LV.r4, LV.r5, LV.r6];   // balcons ondules en console
export const HET = 3.06;

// Portes-balcon : 0.90 | 1.80 | 1.35 | 1.80 | 0.90 = 6.75
export function doors(bay) {
  const [a] = bay;
  return [[a + 0.90, a + 2.70], [a + 4.05, a + 5.85]];
}

// Onde de rive en plan : profondeur(t), t de 0 a 1 sur la largeur de la baie
export function depthAt(t) {
  return DMIN + (DMAX - DMIN) * (1 - Math.cos(2 * Math.PI * LOBES * t)) / 2;
}

// Longueur developpee reelle de la rive ondulee
export function developpe(span = BAY, n = 4000) {
  let L = 0, px = 0, py = depthAt(0);
  for (let i = 1; i <= n; i++) {
    const t = i / n, x = t * span, y = depthAt(t);
    L += Math.hypot(x - px, y - py); px = x; py = y;
  }
  return L;
}

export const fmt = (v, d = 2) => v.toFixed(d);
