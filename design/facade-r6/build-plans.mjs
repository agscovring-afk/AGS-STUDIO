import { writeFileSync } from 'node:fs';
import { XS, BLOCS, AVANCEE, RETRAIT, PBW, PBH, doors } from './geo.mjs';
import { page, header } from './page.mjs';
import { txt, dimH, dimV } from './svgkit.mjs';

const W = 1587, S = 75.5906, X0 = 150;
const C = { beton: '#4A443B', int: '#EFEAE0', ink: '#23211E', dim: '#8C8478',
  accent: '#474B4E', glass: '#1E2224', inox: '#6E7A80', dalle: '#F2EDE3', bande: '#E4DFD5' };
const VOID = XS.vide;

function base(YF, hInt, g) {
  const px = (m) => +(X0 + m * S).toFixed(2), py = (d) => +(YF + d * S).toFixed(2), wm = (m) => +(m * S).toFixed(2);
  for (const [m1, m2] of BLOCS) {
    g.push(`<rect x="${px(m1)}" y="${py(-hInt)}" width="${wm(m2 - m1)}" height="${wm(hInt - 0.30)}" fill="${C.int}"/>`);
    g.push(`<rect x="${px(m1)}" y="${py(-0.30)}" width="${wm(m2 - m1)}" height="${wm(0.30)}" fill="${C.beton}"/>`);
  }
  for (const [a, b] of [XS.c1, XS.c2, XS.c3, XS.c4])
    g.push(`<rect x="${px(a)}" y="${py(-0.55)}" width="${wm(b - a)}" height="${wm(0.55)}" fill="${C.beton}"/>`);
  for (const bay of [XS.bayA, XS.bayB]) for (const [a, b] of doors(bay)) {
    g.push(`<rect x="${px(a)}" y="${py(-0.32)}" width="${wm(b - a)}" height="${wm(0.34)}" fill="#FFFFFF"/>`);
    g.push(`<rect x="${px(a)}" y="${py(-0.20)}" width="${wm((b - a) / 2)}" height="${wm(0.07)}" fill="${C.accent}"/>`);
    g.push(`<rect x="${px(a + (b - a) / 2)}" y="${py(-0.07)}" width="${wm((b - a) / 2)}" height="${wm(0.07)}" fill="${C.accent}"/>`);
    g.push(txt(px((a + b) / 2), py(-0.42), 'PB 1.80 × 2.20', { size: 8.5, fill: C.dim, ls: '0.08em', weight: 700 }));
  }
  return { px, py, wm };
}

const chaine = (px, y) => [[0, 0.55, '0.55'], [0.55, 7.30, '6.75'], [7.30, 7.85, '0.55'], [7.85, 9.65, '1.80'],
  [9.65, 10.20, '0.55'], [10.20, 16.95, '6.75'], [16.95, 17.50, '0.55']]
  .map(([a, b, t]) => dimH(px(a), px(b), y, t, { size: 10 })).join('\n')
  + dimH(px(0), px(17.5), y + 44, '17.50', { size: 13, weight: 700 });

// ---------------------------------------------------------------------------
// Plan des terrasses R+2
// ---------------------------------------------------------------------------
{
  const SVGH = 700, YF = 210, g = [];
  const { px, py, wm } = { px: (m) => +(X0 + m * S).toFixed(2), py: (d) => +(YF + d * S).toFixed(2), wm: (m) => +(m * S).toFixed(2) };
  // dalle de toiture du parking, pleine sur toute la largeur
  g.push(`<rect x="${px(0)}" y="${py(0)}" width="${wm(17.5)}" height="${wm(AVANCEE)}" fill="${C.dalle}"/>`);
  g.push(`<rect x="${px(VOID[0])}" y="${py(0)}" width="${wm(1.80)}" height="${wm(AVANCEE)}" fill="${C.bande}"/>`);
  for (let d = 0.18; d < AVANCEE; d += 0.30)
    g.push(`<line x1="${px(VOID[0])}" y1="${py(d)}" x2="${px(VOID[1])}" y2="${py(d - 0.30)}" stroke="${C.dim}" stroke-width="0.6" opacity="0.5"/>`);
  base(YF, 1.45, g);
  // garde-corps droits : trois cotes ouverts par terrasse, plus la bande centrale
  const gc = (x1, y1, x2, y2) => {
    g.push(`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${C.glass}" stroke-width="6" stroke-linecap="round"/>`);
    g.push(`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${C.inox}" stroke-width="1.6"/>`);
    const n = Math.max(2, Math.round(Math.hypot(x2 - x1, y2 - y1) / (1.35 * S)));
    for (let k = 0; k <= n; k++)
      g.push(`<circle cx="${x1 + (x2 - x1) * k / n}" cy="${y1 + (y2 - y1) * k / n}" r="3.4" fill="none" stroke="${C.inox}" stroke-width="2"/>`);
  };
  for (const [m1, m2] of BLOCS) {
    gc(px(m1), py(0.06), px(m1), py(AVANCEE - 0.06));
    gc(px(m2), py(0.06), px(m2), py(AVANCEE - 0.06));
    gc(px(m1), py(AVANCEE - 0.06), px(m2), py(AVANCEE - 0.06));
    g.push(txt(px((m1 + m2) / 2), py(AVANCEE / 2) - 8, 'TERRASSE', { size: 13, fill: C.dim, ls: '0.24em', weight: 700 }));
    g.push(txt(px((m1 + m2) / 2), py(AVANCEE / 2) + 14, '7.85 × 4.00 m — 31.4 m²', { size: 10.5, fill: C.dim, ls: '0.1em', weight: 600 }));
  }
  g.push(txt(0, 0, 'BANDE CENTRALE 1.80 — NON AFFECTEE', { size: 9, fill: C.ink, ls: '0.12em', weight: 700, transform: `translate(${px(8.75) + 4} ${py(2.0)}) rotate(90)` }));
  g.push(`<line x1="${px(0)}" y1="${py(AVANCEE)}" x2="${px(17.5)}" y2="${py(AVANCEE)}" stroke="${C.ink}" stroke-width="2.4"/>`);
  g.push(txt(px(0.15), py(AVANCEE) + 20, 'NU AVANT DU PARKING — LIMITE DE DALLE', { size: 9.5, fill: C.ink, ls: '0.1em', weight: 700, anchor: 'start' }));
  g.push(dimV(py(0), py(AVANCEE), px(-0.45), '4.00', { size: 11, weight: 700 }));
  g.push(chaine(px, py(AVANCEE) + 62));
  g.push(txt(px(3.925), py(-1.05), 'LOGEMENT', { size: 10, fill: C.dim, ls: '0.18em', weight: 700 }));
  g.push(txt(px(13.575), py(-1.05), 'LOGEMENT', { size: 10, fill: C.dim, ls: '0.18em', weight: 700 }));

  const body = `<div style="width: ${W}px; background: #F1EDE5">
${header({ w: W, kicker: 'Plan · niveau R+2, sur la toiture du parking', title: 'Terrasses',
  sub: 'Tracé relevé sur votre croquis : deux terrasses rectangulaires de 7,85 × 4,00 m, garde-corps droit sur les trois côtés ouverts, séparées par la bande centrale de 1,80 m fermée de chaque côté.',
  right: 'A3 PAYSAGE · ÉCHELLE 1:50<br>COTES EN MÈTRES<br>TRACÉ RETENU' })}
<svg viewBox="0 0 ${W} ${SVGH}" width="${W}" height="${SVGH}" xmlns="http://www.w3.org/2000/svg" style="display: block">${g.join('\n')}</svg>
</div>`;
  writeFileSync('Plan-Terrasse.dc.html', page({ body, props: JSON.stringify({ $preview: { width: W, height: SVGH + 200 } }) }));
  console.log('Plan-Terrasse.dc.html ok');
}

// ---------------------------------------------------------------------------
// Plan du RDC — parking
// ---------------------------------------------------------------------------
{
  const SVGH = 720, YF = 200, g = [];
  const px = (m) => +(X0 + m * S).toFixed(2), py = (d) => +(YF + d * S).toFixed(2), wm = (m) => +(m * S).toFixed(2);
  g.push(`<rect x="${px(0)}" y="${py(-1.90)}" width="${wm(17.5)}" height="${wm(1.90 + AVANCEE)}" fill="${C.dalle}"/>`);
  // murs : maconnerie pleine sur tout le pourtour
  g.push(`<rect x="${px(0)}" y="${py(AVANCEE - 0.30)}" width="${wm(17.5)}" height="${wm(0.30)}" fill="${C.beton}"/>`);
  g.push(`<rect x="${px(0)}" y="${py(-1.90)}" width="${wm(0.30)}" height="${wm(1.90 + AVANCEE)}" fill="${C.beton}"/>`);
  g.push(`<rect x="${px(17.2)}" y="${py(-1.90)}" width="${wm(0.30)}" height="${wm(1.90 + AVANCEE)}" fill="${C.beton}"/>`);
  for (const [a, b] of [XS.c1, XS.c2, XS.c3, XS.c4])
    g.push(`<rect x="${px(a)}" y="${py(-0.55)}" width="${wm(b - a)}" height="${wm(0.55)}" fill="${C.beton}"/>`);
  // portes de garage et hall
  for (const [a, b] of [[1.40, 6.60], [10.90, 16.10]]) {
    g.push(`<rect x="${px(a)}" y="${py(AVANCEE - 0.30)}" width="${wm(b - a)}" height="${wm(0.30)}" fill="#FFFFFF"/>`);
    g.push(`<rect x="${px(a)}" y="${py(AVANCEE - 0.22)}" width="${wm(b - a)}" height="${wm(0.08)}" fill="${C.accent}"/>`);
    g.push(txt(px((a + b) / 2), py(AVANCEE) + 20, `PORTE DE GARAGE ${(b - a).toFixed(2)} m`, { size: 9, fill: C.dim, ls: '0.1em', weight: 700 }));
  }
  g.push(`<rect x="${px(VOID[0])}" y="${py(-0.60)}" width="${wm(1.80)}" height="${wm(0.60 + AVANCEE)}" fill="#FFFFFF"/>`);
  g.push(`<rect x="${px(VOID[0])}" y="${py(-0.60)}" width="${wm(1.80)}" height="${wm(0.60 + AVANCEE)}" fill="none" stroke="${C.ink}" stroke-width="1.4"/>`);
  g.push(txt(0, 0, 'HALL D’ENTREE', { size: 10, fill: C.dim, ls: '0.16em', weight: 700, transform: `translate(${px(8.75) + 4} ${py(2.1)}) rotate(90)` }));
  // bande de ventilation, vue en projection haute
  for (const [a, b] of [[0.55, 1.40], [6.60, 7.30], [10.20, 10.90], [16.10, 16.95]]) {
    g.push(`<rect x="${px(a)}" y="${py(AVANCEE - 0.30)}" width="${wm(b - a)}" height="${wm(0.30)}" fill="none" stroke="${C.accent}" stroke-width="2.4" stroke-dasharray="8 4"/>`);
  }
  g.push(txt(px(3.5), py(AVANCEE) + 40, 'EN POINTILLE : BANDE DE BRISE-VUE ALU 0.80 m DE HAUT, EN PARTIE HAUTE DU MUR',
    { size: 9, fill: C.accent, ls: '0.09em', weight: 700, anchor: 'start' }));
  // vehicules
  const car = (x, y) => `<rect x="${px(x)}" y="${py(y)}" width="${wm(2.30)}" height="${wm(4.80)}" rx="6" fill="none" stroke="${C.dim}" stroke-width="1.1"/>`;
  for (const x of [1.60, 4.05, 11.10, 13.55]) g.push(car(x, 0.40));
  g.push(txt(px(4.0), py(-1.35), 'PARKING — STATIONNEMENT ET CIRCULATION', { size: 10, fill: C.dim, ls: '0.16em', weight: 700, anchor: 'start' }));
  // ligne de rupture arriere
  g.push(`<path d="M ${px(0)} ${py(-1.90)} L ${px(17.5)} ${py(-1.90)}" stroke="${C.ink}" stroke-width="1.2"/>`);
  g.push(txt(px(8.75), py(-1.90) - 10, 'COUPE PARTIELLE — PROFONDEUR DU BATIMENT A CONFIRMER', { size: 9, fill: C.dim, ls: '0.12em', weight: 700 }));
  g.push(dimV(py(0), py(AVANCEE), px(-0.45), '4.00', { size: 11, weight: 700 }));
  g.push(chaine(px, py(AVANCEE) + 78));

  const body = `<div style="width: ${W}px; background: #F1EDE5">
${header({ w: W, kicker: 'Plan · RDC, niveau parking', title: 'Socle parking',
  sub: 'Le parking avance de 4,00 m sur le nu de façade et occupe toute la largeur, bande centrale comprise. Façade en maçonnerie pleine, ventilée par une bande de brise-vue aluminium de 0,80 m en partie haute. Le R+1 reprend le même plan sans les portes de garage.',
  right: 'A3 PAYSAGE · ÉCHELLE 1:50<br>COTES EN MÈTRES<br>PLAN PARTIEL' })}
<svg viewBox="0 0 ${W} ${SVGH}" width="${W}" height="${SVGH}" xmlns="http://www.w3.org/2000/svg" style="display: block">${g.join('\n')}</svg>
</div>`;
  writeFileSync('Plan-RDC.dc.html', page({ body, props: JSON.stringify({ $preview: { width: W, height: SVGH + 220 } }) }));
  console.log('Plan-RDC.dc.html ok');
}
