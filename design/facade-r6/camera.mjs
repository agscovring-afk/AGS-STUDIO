// Camera photographique a decentrement (shift lens), comme en photo d'archi :
// l'axe reste horizontal et le capteur monte, donc les verticales restent
// verticales et seules les horizontales fuient. C'est ce qui distingue une
// photo d'architecture d'une photo de telephone prise en levant la tete.
//
// Monde : X = abscisse de facade (m), Y = distance devant le nu (m, positif
// vers la rue), Z = altitude (m).

export const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
export const add = (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
export const mul = (a, k) => [a[0] * k, a[1] * k, a[2] * k];
export const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
export const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
export const norm = (a) => { const l = Math.hypot(a[0], a[1], a[2]) || 1; return [a[0] / l, a[1] / l, a[2] / l]; };

export function makeCam({ eye, look, f, cx, cy }) {
  const F = norm([look[0] - eye[0], look[1] - eye[1], 0]);   // axe horizontal
  const R = norm(cross([0, 0, 1], F));                        // droite
  const U = [0, 0, 1];                                        // haut = vertical vrai
  const P = (p) => {
    const d = sub(p, eye), z = dot(d, F);
    if (z <= 0.05) return [NaN, NaN, z];
    return [+(cx + f * dot(d, R) / z).toFixed(2), +(cy - f * dot(d, U) / z).toFixed(2), z];
  };
  return { P, F, R, U, eye, f };
}

// Chemin SVG a partir d'une liste de points monde
export const poly = (C, pts, close = true) => {
  const s = pts.map((p) => C.P(p)).filter((q) => Number.isFinite(q[0]));
  if (s.length < 2) return '';
  return s.map(([x, y], i) => `${i ? 'L' : 'M'} ${x} ${y}`).join(' ') + (close ? ' Z' : '');
};

// ---------------------------------------------------------------------------
// Soleil et matiere
// ---------------------------------------------------------------------------
// Direction de propagation de la lumiere : elle vient de la gauche, de devant,
// et d'assez haut — fin d'apres-midi d'ete en Algerie.
export const SUN = norm([0.34, -0.56, -0.76]);
export const SUNDIR = mul(SUN, -1);                 // vers le soleil

const clamp = (v) => Math.max(0, Math.min(255, Math.round(v)));
export const hex2rgb = (h) => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
export const rgb2hex = (r) => '#' + r.map((v) => clamp(v).toString(16).padStart(2, '0')).join('');

// Eclairement d'une facette : soleil + ciel (venant du haut, froid) + rebond
// du sol (venant du bas, chaud). C'est le minimum pour que le blanc ne soit
// pas plat.
export function shadeN(baseHex, n, o = {}) {
  const kd = o.kd ?? 0.72, amb = o.amb ?? 0.30, sky = o.sky ?? 0.16, bounce = o.bounce ?? 0.10;
  const s = Math.max(0, dot(n, SUNDIR));
  const up = Math.max(0, n[2]), down = Math.max(0, -n[2]);
  const f = amb + kd * s * (o.shadow ?? 1) + sky * up + bounce * down;
  const [r, g, b] = hex2rgb(baseHex);
  // le soleil rechauffe, l'ombre bleuit
  const w = s * (o.shadow ?? 1);
  return rgb2hex([r * f * (1 + 0.055 * w), g * f * (1 + 0.012 * w), b * f * (1 - 0.055 * w + 0.10 * (1 - w))]);
}

// Ombre portee d'un point sur le plan Y = y0 (la facade)
export function castY(p, y0 = 0) {
  const t = (y0 - p[1]) / SUN[1];
  return [p[0] + t * SUN[0], y0, p[2] + t * SUN[2]];
}
// Ombre portee d'un point sur le sol Z = z0
export function castZ(p, z0 = 0) {
  const t = (z0 - p[2]) / SUN[2];
  return [p[0] + t * SUN[0], p[1] + t * SUN[1], z0];
}

// Perspective atmospherique : plus c'est loin, plus ca se noie dans le ciel
export function haze(hex, dist, o = {}) {
  const d0 = o.d0 ?? 40, k = o.k ?? 0.0042, hz = hex2rgb(o.color ?? '#B9CBDA');
  const a = Math.min(0.82, Math.max(0, (dist - d0) * k));
  const c = hex2rgb(hex);
  return rgb2hex(c.map((v, i) => v * (1 - a) + hz[i] * a));
}
