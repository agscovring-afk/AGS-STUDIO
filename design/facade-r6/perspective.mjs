// ---------------------------------------------------------------------------
// Projection perspective a trois points, camera basculee vers le haut.
// Repere : X = ecart horizontal au centre de facade (m, +vers la droite)
//          Y = distance a la camera (m, + vers le fond)
//          Z = altitude au-dessus du terrain (m)
// La camera est a l'altitude EYE, basculee de PHI vers le haut.
// Les horizontales restent horizontales, les verticales convergent vers un
// point de fuite unique — c'est ce qui manquait au rendu precedent.
// ---------------------------------------------------------------------------
export const CAM = {
  dFacade: 22,      // recul de la camera par rapport au nu de facade
  dParking: 18,     // nu avant du socle parking (avancee de 4,00 m)
  phi: 40 * Math.PI / 180,
  f: 800,
  eye: 1.60,
  cx: 590,
  cy: 271,
};

const CO = Math.cos(CAM.phi), SI = Math.sin(CAM.phi);

export function P(X, Y, Z) {
  const z = Z - CAM.eye;
  const yp = Y * CO + z * SI;
  const zp = -Y * SI + z * CO;
  return [+(CAM.cx + CAM.f * X / yp).toFixed(2), +(CAM.cy - CAM.f * zp / yp).toFixed(2)];
}

// abscisse de facade (0 a 17,50) -> ecart au centre
export const XC = (m) => m - 8.75;
export const p = (m, Y, Z) => P(XC(m), Y, Z);

export const path = (pts) => pts.map(([x, y], i) => `${i ? 'L' : 'M'} ${x} ${y}`).join(' ');
export const strip = (a, b) => `${path(a)} L ${b[b.length - 1][0]} ${b[b.length - 1][1]} ${path(b.slice().reverse()).slice(1)} Z`;
// rectangle pris dans un plan vertical a distance Y constante
export const quad = (m1, m2, Y, Z1, Z2) =>
  `${path([p(m1, Y, Z2), p(m2, Y, Z2), p(m2, Y, Z1), p(m1, Y, Z1)])} Z`;
