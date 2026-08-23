import { writeFileSync } from 'node:fs';
import { XS, BLOCS, LOBES, DMIN, DCREUX, DMAX, FASCIA, GC, PBW, PBH, HSP, DALLE,
         depthAt, ondeAt, doors, developpe, gcSegments } from './geo.mjs';
import { page, header } from './page.mjs';
import { txt, dimH, dimV } from './svgkit.mjs';

// A2 paysage a 96 px/pouce, echelle 1:25
const W = 2244, SVGH = 1318, S = 151.181;
const C = { beton: '#4A443B', betonL: '#7B7264', int: '#F2EDE3', mur: '#D5C4AC', blanc: '#F7F4ED',
  aqua: '#FAF8F3', accent: '#474B4E', accentD: '#2E3236', glass: '#1E2224', inox: '#9BA5AA',
  led: '#E7B94F', ink: '#23211E', dim: '#8C8478', sol: '#E4DFD5' };
const BLK = BLOCS[1], [M1, M2] = BLK, BAY = XS.bayB, D = doors(BAY);
const g = [];
const hat = (x1, y1, x2, y2, n = 9) => {
  let s = '';
  for (let i = 0; i <= n; i++) { const t = i / n; s += `<line x1="${x1 + (x2 - x1) * t}" y1="${y1}" x2="${x1 + (x2 - x1) * t - 7}" y2="${y2}" stroke="${C.dim}" stroke-width="0.6" opacity="0.6"/>`; }
  return s;
};
const cartouche = (x, y, t, sc) => txt(x, y, `${t}   ·   1:25`, { size: 12.5, anchor: 'start', fill: C.ink, ls: '0.18em', weight: 700 });

// ===========================================================================
// 1 — ELEVATION INTERIEURE DU BALCON  (on regarde le mur depuis le balcon)
// ===========================================================================
{
  const x0 = 118, sol = 610;
  const px = (m) => +(x0 + (m - M1) * S).toFixed(2), py = (h) => +(sol - h * S).toFixed(2);
  const wm = (m) => +(m * S).toFixed(2);
  const R = (a, b, h1, h2, f, ex = '') => `<rect x="${px(a)}" y="${py(h2)}" width="${wm(b - a)}" height="${wm(h2 - h1)}" fill="${f}" ${ex}/>`;
  g.push(cartouche(x0, 58, '1 · ELEVATION INTERIEURE DU BALCON'));
  g.push(R(M1, M2, 0, HSP, C.mur));
  for (const [a, b] of [XS.c3, XS.c4]) g.push(R(a, b, 0, HSP, C.blanc));
  g.push(R(M1, M2, HSP, HSP + DALLE, C.beton));                       // dalle du niveau au-dessus
  g.push(hat(px(M1), py(HSP + DALLE), px(M2), py(HSP), 46));
  g.push(R(M1, M2, -DALLE, 0, C.beton));                              // dalle du balcon
  g.push(hat(px(M1), py(0), px(M2), py(-DALLE), 46));
  for (const [a, b] of D) {                                           // portes-balcon 1.80 x 2.20
    g.push(R(a, b, 0, PBH, C.glass));
    g.push(R(a, b, 0, PBH, 'none', `stroke="${C.accent}" stroke-width="4"`));
    g.push(`<line x1="${px((a + b) / 2)}" y1="${py(0)}" x2="${px((a + b) / 2)}" y2="${py(PBH)}" stroke="${C.accent}" stroke-width="3"/>`);
    for (const s of [-1, 1]) g.push(R((a + b) / 2 + s * 0.10 - 0.03, (a + b) / 2 + s * 0.10 + 0.03, 1.00, 1.42, C.inox));
    g.push(`<path d="M ${px(a + 0.10)} ${py(PBH - 0.14)} l ${wm(0.55)} 0 M ${px(a + 0.10)} ${py(PBH - 0.14)} l 0 ${wm(0.42)}" stroke="#5A6468" stroke-width="1.4" fill="none" opacity="0.6"/>`);
    g.push(txt(px((a + b) / 2), py(PBH) - 14, 'PORTE-BALCON 1.80 × 2.20 — ALU TPR 65 RAL 7024', { size: 9, fill: C.dim, ls: '0.08em', weight: 700 }));
  }
  const xm = (D[0][1] + D[1][0]) / 2;                                 // profil LED vertical
  g.push(R(xm - 0.05, xm + 0.05, 0.30, 2.20, C.accentD));
  g.push(R(xm - 0.03, xm + 0.03, 0.32, 2.18, C.led));
  g.push(`<path d="M ${px(xm)} ${py(2.30)} l 0 -26" stroke="${C.ink}" stroke-width="0.8"/>`);
  g.push(txt(px(xm), py(2.30) - 32, 'PROFIL LED VERTICAL 1.90 m', { size: 9, fill: C.led, ls: '0.09em', weight: 700 }));
  // cotes
  g.push(dimH(px(D[0][0]), px(D[0][1]), py(0) + 46, '1.80', { size: 11 }));
  g.push(dimH(px(D[1][0]), px(D[1][1]), py(0) + 46, '1.80', { size: 11 }));
  g.push(dimH(px(D[0][1]), px(D[1][0]), py(0) + 46, '1.35', { size: 11 }));
  g.push(dimH(px(M1), px(D[0][0]), py(0) + 46, '1.45', { size: 11 }));
  g.push(dimH(px(D[1][1]), px(M2), py(0) + 46, '1.45', { size: 11 }));
  g.push(dimH(px(M1), px(M2), py(0) + 92, '7.85', { size: 13, weight: 700 }));
  g.push(dimV(py(0), py(PBH), px(M1) - 44, '2.20', { size: 11 }));
  g.push(dimV(py(0), py(HSP), px(M1) - 96, '3.06', { size: 12, weight: 700 }));
  g.push(txt(0, 0, 'HAUTEUR LIBRE', { size: 9, fill: C.dim, ls: '0.14em', weight: 700, transform: `translate(${px(M1) - 128} ${py(HSP / 2)}) rotate(-90)` }));
}

// ===========================================================================
// coupes verticales : au creux et a la crete
// ===========================================================================
function coupe(x0, sol, prof, titre, titreY, full) {
  const INT = 1.05, MUR = 0.30;
  const px = (d) => +(x0 + (d + INT + MUR) * S).toFixed(2);   // d = profondeur depuis le nu exterieur
  const py = (h) => +(sol - h * S).toFixed(2);
  const wm = (m) => +(m * S).toFixed(2);
  const R = (d1, d2, h1, h2, f, ex = '') => `<rect x="${px(d1)}" y="${py(h2)}" width="${wm(d2 - d1)}" height="${wm(h2 - h1)}" fill="${f}" ${ex}/>`;
  const s = [];
  s.push(cartouche(x0, titreY, titre));
  // dalle du balcon en console + dalle interieure
  s.push(R(-INT - MUR, prof, -DALLE, 0, C.beton));
  s.push(hat(px(-INT - MUR), py(0), px(prof), py(-DALLE), 22));
  s.push(R(-INT - MUR, prof, -DALLE, 0, 'none', `stroke="${C.ink}" stroke-width="1.4"`));
  // retombee de rive + Aquapanel + gorge LED
  s.push(R(prof - 0.16, prof, -FASCIA, 0, C.beton));
  s.push(R(prof - 0.20, prof + 0.03, -FASCIA, 0.02, C.aqua));
  s.push(R(prof - 0.20, prof + 0.03, -FASCIA, 0.02, 'none', `stroke="${C.betonL}" stroke-width="1"`));
  s.push(R(prof - 0.16, prof - 0.09, -FASCIA, -FASCIA + 0.06, C.led));
  s.push(`<path d="M ${px(prof - 0.125)} ${py(-FASCIA)} l ${wm(0.34)} ${wm(0.30)} M ${px(prof - 0.125)} ${py(-FASCIA)} l ${wm(0.06)} ${wm(0.42)} M ${px(prof - 0.125)} ${py(-FASCIA)} l ${-wm(0.22)} ${wm(0.38)}" fill="none" stroke="#C79A3E" stroke-width="1.2" opacity="0.8"/>`);
  // garde-corps : verre feuillete noir + montant et main courante inox
  s.push(R(prof - 0.12, prof - 0.05, 0.02, 0.14, C.inox));
  s.push(R(prof - 0.11, prof - 0.06, 0.14, GC - 0.06, C.glass));
  s.push(`<line x1="${px(prof - 0.085)}" y1="${py(0.02)}" x2="${px(prof - 0.085)}" y2="${py(GC)}" stroke="${C.inox}" stroke-width="3"/>`);
  s.push(R(prof - 0.16, prof - 0.01, GC - 0.06, GC, C.inox));
  // mur de facade + porte-balcon
  const HT = full ? HSP : 1.40;
  s.push(R(-MUR, 0, -DALLE, HT + (full ? DALLE : 0), C.beton));
  s.push(hat(px(-MUR), py(HT + (full ? DALLE : 0)), px(0), py(-DALLE), full ? 26 : 12));
  s.push(R(-0.09, 0, 0, Math.min(PBH, HT), C.accent));
  s.push(R(-0.06, -0.02, 0, Math.min(PBH, HT), C.glass));
  if (full) {
    s.push(R(-INT - MUR, 0, HSP, HSP + DALLE, C.beton));
    s.push(hat(px(-INT - MUR), py(HSP + DALLE), px(0), py(HSP), 14));
    s.push(R(0, prof, HSP, HSP + DALLE, C.beton, 'opacity="0.35"'));
    s.push(R(prof - 0.20, prof + 0.03, HSP - FASCIA, HSP + 0.02, C.aqua, 'opacity="0.45"'));
    s.push(txt(px(prof / 2), py(HSP) + 22, 'BALCON DU NIVEAU AU-DESSUS', { size: 8.5, fill: C.dim, ls: '0.1em', weight: 700 }));
  }
  // sols finis
  s.push(R(-INT - MUR, -MUR, 0, 0.05, C.sol));
  s.push(R(0, prof - 0.16, 0, 0.04, C.sol));
  s.push(txt(px(-(INT + MUR) / 2 - MUR / 2), py(full ? 1.5 : 0.9), 'LOGEMENT', { size: 10, fill: C.dim, ls: '0.16em', weight: 700 }));
  // cotes
  s.push(dimH(px(0), px(prof), py(-FASCIA) + 58, prof.toFixed(2), { size: 12.5, weight: 700 }));
  s.push(txt(px(prof / 2), py(-FASCIA) + 76, 'PORTE-A-FAUX', { size: 8.5, fill: C.dim, ls: '0.14em', weight: 700 }));
  s.push(dimV(py(0), py(GC), px(prof) + 46, '1.10', { size: 10.5 }));
  s.push(dimV(py(-FASCIA), py(0), px(prof) + 46, '0.45', { size: 10 }));
  if (full) {
    const ren = (dx, hy, tx, ty, lab, col) => {
      s.push(`<path d="M ${px(dx)} ${py(hy)} L ${px(tx)} ${py(ty)}" stroke="${C.ink}" stroke-width="0.8"/>`);
      s.push(`<circle cx="${px(dx)}" cy="${py(hy)}" r="2.6" fill="${C.ink}"/>`);
      s.push(txt(px(tx) + 6, py(ty) + 4, lab, { size: 9, anchor: 'start', fill: col ?? C.dim, ls: '0.08em', weight: 700 }));
    };
    ren(prof - 0.02, -0.22, prof + 0.30, -0.62, 'BANDEAU AQUAPANEL CINTRE');
    ren(prof - 0.125, -FASCIA + 0.03, prof + 0.30, -0.98, 'GORGE LED 5 cm', C.led);
    ren(prof - 0.085, 0.72, prof + 0.30, 1.26, 'VERRE FEUILLETE NOIR + INOX');
    ren(-0.045, 1.70, 0.78, 2.36, 'PORTE-BALCON ALU RAL 7024');
    s.push(dimV(py(0), py(PBH), px(-INT - MUR) - 42, '2.20', { size: 10.5 }));
    s.push(dimV(py(0), py(HSP), px(-INT - MUR) - 92, '3.06', { size: 11.5, weight: 700 }));
    s.push(dimV(py(HSP), py(HSP + DALLE), px(-INT - MUR) - 42, '0.20', { size: 9.5 }));
  } else {
    s.push(dimV(py(-DALLE), py(0), px(-INT - MUR) - 42, '0.20', { size: 9.5 }));
  }
  return s.join('\n');
}
g.push(coupe(1470, 610, DMAX, '2 · COUPE A-A — AU GRAND LOBE (Ø 1.80)', 58, true));
g.push(coupe(1470, 1128, DCREUX, '3 · COUPE B-B — AU PETIT LOBE (Ø 1.10)', 790, false));

// ===========================================================================
// 4 — PLAN DU BALCON
// ===========================================================================
{
  const x0 = 118, yf = 900;
  const px = (m) => +(x0 + (m - M1) * S).toFixed(2), py = (d) => +(yf + d * S).toFixed(2);
  const wm = (m) => +(m * S).toFixed(2);
  g.push(cartouche(x0, 780, '4 · PLAN DU BALCON — ONDE DE RIVE'));
  const N = 500, pts = [];
  for (let i = 0; i <= N; i++) { const m = M1 + (M2 - M1) * i / N; pts.push([px(m), py(depthAt(m, 1))]); }
  const pth = (p, d = 0) => p.map(([x, y], i) => `${i ? 'L' : 'M'} ${x} ${(y - d).toFixed(2)}`).join(' ');
  g.push(`<path d="M ${px(M1)} ${py(0)} ${pth(pts).slice(1)} L ${px(M2)} ${py(0)} Z" fill="${C.sol}"/>`);
  g.push(`<path d="${pth(pts)}" fill="none" stroke="${C.ink}" stroke-width="2.4"/>`);
  g.push(`<path d="${pth(pts, wm(0.20))}" fill="none" stroke="${C.betonL}" stroke-width="1.2" stroke-dasharray="6 4"/>`);
  g.push(`<path d="${pth(pts, wm(0.05))}" fill="none" stroke="${C.led}" stroke-width="2.6" stroke-dasharray="12 6"/>`);
  const idx = (m) => Math.max(0, Math.min(N, Math.round((m - M1) / (M2 - M1) * N)));
  for (const seg of gcSegments(1)) {
    const sub = pts.slice(idx(seg.x1), idx(seg.x2) + 1);
    if (sub.length < 2) continue;
    if (seg.kind === 'verre') {
      g.push(`<path d="${pth(sub, wm(0.10))}" fill="none" stroke="${C.glass}" stroke-width="7" stroke-linecap="round"/>`);
      g.push(`<path d="${pth(sub, wm(0.10))}" fill="none" stroke="#7C868A" stroke-width="2"/>`);
    } else {
      g.push(`<path d="${pth(sub, wm(0.10))}" fill="none" stroke="${C.inox}" stroke-width="2"/>`);
      for (let m = seg.x1 + 0.055; m < seg.x2 - 0.03; m += 0.11) {
        const [bx, by] = pts[idx(m)];
        g.push(`<circle cx="${bx}" cy="${(by - wm(0.10)).toFixed(2)}" r="3.4" fill="${C.inox}"/>`);
      }
    }
  }
  // mur, poteaux, portes
  g.push(`<rect x="${px(M1)}" y="${py(-1.15)}" width="${wm(M2 - M1)}" height="${wm(0.85)}" fill="${C.int}"/>`);
  g.push(`<rect x="${px(M1)}" y="${py(-0.30)}" width="${wm(M2 - M1)}" height="${wm(0.30)}" fill="${C.beton}"/>`);
  for (const [a, b] of [XS.c3, XS.c4]) g.push(`<rect x="${px(a)}" y="${py(-0.55)}" width="${wm(b - a)}" height="${wm(0.55)}" fill="${C.beton}"/>`);
  for (const [a, b] of D) {
    g.push(`<rect x="${px(a)}" y="${py(-0.32)}" width="${wm(b - a)}" height="${wm(0.34)}" fill="#FFFFFF"/>`);
    g.push(`<rect x="${px(a)}" y="${py(-0.22)}" width="${wm((b - a) / 2)}" height="${wm(0.08)}" fill="${C.accent}"/>`);
    g.push(`<rect x="${px(a + (b - a) / 2)}" y="${py(-0.10)}" width="${wm((b - a) / 2)}" height="${wm(0.08)}" fill="${C.accent}"/>`);
    g.push(`<path d="M ${px(a + 0.15)} ${py(-0.05)} l ${wm(0.55)} 0" stroke="${C.dim}" stroke-width="1.2" marker-end=""/>`);
    g.push(txt(px((a + b) / 2), py(-0.62), 'PB 1.80 — 2 VANTAUX COULISSANTS', { size: 9, fill: C.dim, ls: '0.08em', weight: 700 }));
  }
  const xm = (D[0][1] + D[1][0]) / 2;
  g.push(`<rect x="${px(xm - 0.05)}" y="${py(-0.30)}" width="${wm(0.10)}" height="${wm(0.10)}" fill="${C.led}"/>`);
  // reperes de coupe
  for (const [m, lab] of [[11.99, 'A'], [13.575, 'B']]) {
    g.push(`<path d="M ${px(m)} ${py(-1.30)} L ${px(m)} ${py(DMAX + 0.22)}" stroke="${C.ink}" stroke-width="1.4" stroke-dasharray="14 5 3 5"/>`);
    for (const yy of [py(-1.30), py(DMAX + 0.22)]) {
      g.push(`<circle cx="${px(m)}" cy="${yy}" r="12" fill="#FFFFFF" stroke="${C.ink}" stroke-width="1.6"/>`);
      g.push(txt(px(m), yy + 5, lab, { size: 13, weight: 700, fill: C.ink }));
    }
  }
  // cotes
  const yc = py(DMAX) + 88;
  [[M1, 10.20, '0.55'], [10.20, 11.10, '0.90'], [11.10, 12.90, '1.80'], [12.90, 14.25, '1.35'],
   [14.25, 16.05, '1.80'], [16.05, 16.95, '0.90'], [16.95, M2, '0.55']]
    .forEach(([a, b, t]) => g.push(dimH(px(a), px(b), yc, t, { size: 11 })));
  g.push(dimH(px(M1), px(M2), yc + 48, '7.85', { size: 13, weight: 700 }));
  g.push(dimV(py(0), py(DMAX), px(M1) - 50, DMAX.toFixed(2), { size: 11 }));
  g.push(dimV(py(0), py(DCREUX), px(M1) - 104, DCREUX.toFixed(2), { size: 11 }));
  g.push(txt(0, 0, 'PROFONDEUR', { size: 9, fill: C.dim, ls: '0.14em', weight: 700, transform: `translate(${px(M1) - 128} ${py(0.9)}) rotate(-90)` }));
  g.push(txt(px(10.35), py(0.34), `DEVELOPPE ${developpe().toFixed(2)} ml`, { size: 10, fill: C.ink, ls: '0.12em', weight: 700, anchor: 'start' }));
  // trace au compas : centre et rayon de chaque lobe, poses sur le nu de facade
  for (const { c, r } of LOBES) {
    const cx = px(M1 + c), cy = py(0), d = r * S * 0.7071;
    g.push(`<circle cx="${cx}" cy="${cy}" r="3.6" fill="#FFFFFF" stroke="${C.ink}" stroke-width="1.5"/>`);
    g.push(`<path d="M ${cx - 9} ${cy} l 18 0 M ${cx} ${cy - 9} l 0 18" stroke="${C.ink}" stroke-width="1"/>`);
    g.push(`<path d="M ${cx} ${cy} l ${d.toFixed(1)} ${d.toFixed(1)}" stroke="${C.ink}" stroke-width="1" stroke-dasharray="5 4"/>`);
    g.push(txt(cx + d * 0.55, cy + d * 0.55 - 7, 'R ' + r.toFixed(2), { size: 9.5, fill: C.ink, weight: 700, anchor: 'start' }));
    g.push(txt(cx, cy - 16, 'Ø ' + (2 * r).toFixed(2), { size: 9.5, fill: C.ink, weight: 700 }));
  }
}

const LEG = [
  ['Bandeau de rive', 'Aquapanel cintré 12,5 mm sur ossature, retombée 0,45 m, finition blanche. Épaisseur d’habillage 0,20 m au nu de la dalle.'],
  ['Gorge LED', 'Profil aluminium encastré de 5 cm en sous-face du bandeau, ruban LED 3000 K IP65 — alimentation à prévoir dans la dalle avant habillage.'],
  ['Garde-corps', 'Verre feuilleté teinté noir 8.8.4, montants et main courante inox Ø 42, h = 1,10 m au-dessus du sol fini. Barreaudage inox aux creux et aux crêtes.'],
  ['Porte-balcon', 'Aluminium TPR série 65 à rupture de pont thermique, RAL 7024, 2 vantaux coulissants, 1,80 × 2,20 m, double vitrage 4/16/4.'],
  ['Profil LED vertical', 'Encastré dans le trumeau entre les deux portes, 1,90 m de haut, même circuit que la gorge de rive.'],
  ['Structure', 'Dalle 0,20 m, hauteur libre 3,06 m. Console nulle au nu de façade, 0,90 m au grand lobe, 0,55 m au petit — ferraillage à valider par le BET.'],
];

const body = `<div style="width: ${W}px; background: #FFFFFF">
${header({ w: W, kicker: 'Détail · balcon type, niveau courant R+3 à R+8',
  title: 'Balcon — les quatre vues',
  sub: 'Le même balcon vu de face depuis l’intérieur, coupé au grand lobe et au petit lobe, et en plan. Les deux coupes montrent la même construction à ses deux profondeurs extrêmes : c’est là que se lit l’ondulation.',
  right: 'A2 PAYSAGE · ÉCHELLE 1:25<br>COTES EN MÈTRES<br>BLOC DROIT — GAUCHE EN MIROIR' })}
<svg viewBox="0 0 ${W} ${SVGH}" width="${W}" height="${SVGH}" xmlns="http://www.w3.org/2000/svg" style="display: block">${g.join('\n')}</svg>
<div style="padding: 10px 44px 34px">
  <div class="rule" style="margin-bottom: 18px"></div>
  <div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px 40px">
    ${LEG.map(([t, d]) => `<div>
      <div style="font-family: 'Space Grotesk', 'Helvetica Neue', Arial, sans-serif; font-size: 13px; font-weight: 600">${t}</div>
      <div style="font-size: 11.5px; line-height: 1.55; color: #6E6659; margin-top: 4px; text-wrap: pretty">${d}</div>
    </div>`).join('\n    ')}
  </div>
</div>
</div>`;
writeFileSync('Detail-Balcon.dc.html', page({ body, props: JSON.stringify({ $preview: { width: W, height: 1620 } }) }));
console.log('Detail-Balcon.dc.html ok');
