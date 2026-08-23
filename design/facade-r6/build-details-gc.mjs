import { writeFileSync } from 'node:fs';
import { GC, GC_PAS, BLOC, ondeAt, gcSegmentsLocal, developpe } from './geo.mjs';
import { page, header } from './page.mjs';
import { txt, dimH, dimV } from './svgkit.mjs';
import { D, PATTERNS, callout, nomenclature, detailTitle } from './detailkit.mjs';

// ---------------------------------------------------------------------------
// Le garde-corps mixte, a plat. La rive est courbe, le garde-corps la suit par
// une suite de cordes de 40 cm : un panneau de verre feuillete plat, puis
// 40 cm de barreaudage inox, et ainsi de suite. Cette planche donne le rythme
// developpe, les deux coupes types et l'angle a rattraper d'un panneau au
// suivant.
// ---------------------------------------------------------------------------
const W = 2244, SVGH = 1880;
const g = [];
const SEG = gcSegmentsLocal(), L = developpe(), PAS = SEG[0].ml;

// --- angles entre cordes successives : c'est ce que la pince doit rattraper --
const chords = SEG.map((s) => {
  const dy = ondeAt(s.x2) - ondeAt(s.x1), dx = s.x2 - s.x1;
  return Math.atan2(dy, dx);
});
const devi = chords.slice(1).map((a, i) => Math.abs(a - chords[i]) * 180 / Math.PI);
const devMax = Math.max(...devi), devMoy = devi.reduce((a, b) => a + b, 0) / devi.length;
// fleche d'une corde de 40 cm sur le plus petit rayon rencontre
const fleche = SEG.map((s) => {
  const n = 24; let f = 0;
  const x1 = s.x1, y1 = ondeAt(s.x1), x2 = s.x2, y2 = ondeAt(s.x2);
  const len = Math.hypot(x2 - x1, y2 - y1);
  for (let i = 1; i < n; i++) {
    const t = i / n, xx = x1 + (x2 - x1) * t, yy = ondeAt(xx);
    f = Math.max(f, Math.abs((y2 - y1) * (xx - x1) - (x2 - x1) * (yy - y1)) / len);
  }
  return f;
});
const flMax = Math.max(...fleche);
// Ce qui compte vraiment : la fleche des seuls panneaux de VERRE. Le barreaudage
// inox suit n'importe quel rayon, chaque barreau etant un point sur la courbe.
const iVerre = SEG.map((s, k) => (s.kind === 'verre' ? k : -1)).filter((k) => k >= 0);
const flVerre = Math.max(...iVerre.map((k) => fleche[k]));
const kPire = iVerre.reduce((a, k) => (fleche[k] > fleche[a] ? k : a), iVerre[0]);
const devVerre = Math.max(...iVerre.map((k) => devi[k] ?? 0));

// ===========================================================================
// G0 — ELEVATION DEVELOPPEE, 1:20
// ===========================================================================
{
  const S = 188.98, ox = 150, oy = 430;            // 1:20
  const X = (s) => +(ox + s * S).toFixed(2);
  const Y = (z) => +(oy - z * S).toFixed(2);
  const R = (s1, s2, z1, z2, fill, extra = '') =>
    `<rect x="${X(s1)}" y="${Y(z2)}" width="${((s2 - s1) * S).toFixed(2)}" height="${((z2 - z1) * S).toFixed(2)}" fill="${fill}" ${extra}/>`;
  g.push(R(0, L, -0.05, 0, '#EDEAE2', `stroke="${D.fine}" stroke-width="0.8"`));   // dalle, a plat
  SEG.forEach((s, k) => {
    const a = k * PAS, b = (k + 1) * PAS;
    if (s.kind === 'verre') {
      g.push(R(a + 0.015, b - 0.015, 0.10, GC - 0.035, 'url(#gVerre)', `stroke="${D.verreL}" stroke-width="1.6"`));
      g.push(R(a + 0.015, b - 0.015, 0.10, 0.14, D.inoxD, `stroke="${D.inoxD}" stroke-width="0.8"`));
      g.push(R(a + 0.015, b - 0.015, GC - 0.075, GC - 0.035, D.inoxD, `stroke="${D.inoxD}" stroke-width="0.8"`));
    } else {
      for (let x = a + 0.05; x < b - 0.02; x += 0.11)
        g.push(`<line x1="${X(x)}" y1="${Y(0.075)}" x2="${X(x)}" y2="${Y(GC - 0.035)}" stroke="${D.inoxD}" stroke-width="4"/>`);
      g.push(R(a, b, 0.045, 0.075, D.inoxD, `stroke="${D.inoxD}" stroke-width="0.8"`));
    }
    // platine a chaque joint
    g.push(R(a - 0.05, a + 0.05, 0, 0.03, D.inox, `stroke="${D.inoxD}" stroke-width="0.8"`));
  });
  g.push(R(0, L, GC - 0.035, GC + 0.007, D.inox, `stroke="${D.inoxD}" stroke-width="1.1"`)); // main courante O42
  g.push(dimV(Y(0), Y(GC), X(-0.14), '1.10', { size: 10 }));
  // chaine de cotes : un pas sur deux
  for (let k = 0; k < SEG.length; k += 1) {
    if (k % 4) continue;
    g.push(dimH(X(k * PAS), X((k + 1) * PAS), Y(-0.30), '0.40', { size: 8 }));
  }
  g.push(dimH(X(0), X(L), Y(-0.62), ' ', { size: 10.5 }));
  g.push(txt(X(L / 2), Y(-0.75), `${L.toFixed(2)} ml développés — ${SEG.length} panneaux de ${(PAS * 100).toFixed(0)} cm : 12 de verre, 12 d’inox`, { size: 11, fill: D.ink, weight: 600, ls: '0.04em' }));
  SEG.slice(0, 4).forEach((sg, k) => g.push(txt(X((k + 0.5) * PAS), Y(GC + 0.10),
    sg.kind === 'verre' ? 'VERRE' : 'INOX', { size: 8, fill: sg.kind === 'verre' ? D.verreL : D.inoxD, ls: '0.14em', weight: 700 })));
  g.push(detailTitle(150, 178, 'G0', 'GARDE-CORPS MIXTE — ÉLÉVATION DÉVELOPPÉE D’UN BALCON', 'ÉCHELLE 1:20 · DÉVELOPPÉ MIS À PLAT'));
}

// ===========================================================================
// G1 / G2 — COUPES VERTICALES TYPES, 1:5
// ===========================================================================
const coupeGC = (ox, oy, kind) => {
  const S = 755.91;                                 // 1:5
  const X = (y) => +(ox + y * S).toFixed(2);
  const Y = (z) => +(oy - z * S).toFixed(2);
  const R = (y1, y2, z1, z2, fill, extra = '') =>
    `<rect x="${X(y1)}" y="${Y(z2)}" width="${((y2 - y1) * S).toFixed(2)}" height="${((z2 - z1) * S).toFixed(2)}" fill="${fill}" ${extra}/>`;
  const o = [];
  const ST = `stroke="${D.ink}" stroke-width="1.1"`, FI = `stroke="${D.fine}" stroke-width="0.7"`;
  o.push(R(-0.13, 0.13, -0.09, -0.02, 'url(#pBeton)', ST));          // dalle
  o.push(R(-0.13, 0.13, -0.02, 0, D.carr, FI));                       // carrelage
  o.push(R(-0.055, 0.055, 0, 0.010, D.inox, FI));                     // platine 110 x 10
  o.push(`<circle cx="${X(-0.035)}" cy="${Y(0.005)}" r="3.4" fill="${D.inoxD}"/>`);
  o.push(`<circle cx="${X(0.035)}" cy="${Y(0.005)}" r="3.4" fill="${D.inoxD}"/>`);
  o.push(`<path d="M ${X(-0.035)} ${Y(0)} L ${X(-0.035)} ${Y(-0.075)} M ${X(0.035)} ${Y(0)} L ${X(0.035)} ${Y(-0.075)}" stroke="${D.inoxD}" stroke-width="2.4"/>`);
  if (kind === 'verre') {
    o.push(R(-0.030, 0.030, 0.010, 0.075, 'url(#gAlu)', `stroke="${D.inoxD}" stroke-width="0.9"`));  // pince basse
    o.push(R(-0.0088, 0.0088, 0.045, GC - 0.035, 'url(#gVerre)', `stroke="${D.verreL}" stroke-width="1"`));
    o.push(R(-0.026, 0.026, GC - 0.075, GC - 0.035, 'url(#gAlu)', `stroke="${D.inoxD}" stroke-width="0.9"`)); // pince haute
    o.push(R(-0.014, 0.014, 0.052, 0.070, '#8A8F93', FI));
  } else {
    o.push(R(-0.030, 0.030, 0.010, 0.045, D.inox, `stroke="${D.inoxD}" stroke-width="0.9"`));
    o.push(R(-0.012, 0.012, 0.045, GC - 0.035, D.inox, `stroke="${D.inoxD}" stroke-width="1"`));    // barreau O16 vu de face
    o.push(R(-0.055, 0.055, 0.045, 0.070, D.inox, `stroke="${D.inoxD}" stroke-width="0.9"`));       // lisse basse
    for (const dy of [-0.075, 0.075])
      o.push(R(dy - 0.008, dy + 0.008, 0.070, GC - 0.035, D.inox, `stroke="${D.inoxD}" stroke-width="0.8"`));
  }
  o.push(`<circle cx="${X(0)}" cy="${Y(GC - 0.014)}" r="${(0.021 * S).toFixed(1)}" fill="${D.inox}" stroke="${D.inoxD}" stroke-width="1.2"/>`);
  o.push(`<circle cx="${X(0)}" cy="${Y(GC - 0.014)}" r="${(0.013 * S).toFixed(1)}" fill="none" stroke="${D.inoxD}" stroke-width="0.8"/>`);
  o.push(dimV(Y(0), Y(GC), X(-0.20), '1.10', { size: 9.5 }));
  o.push(dimH(X(-0.055), X(0.055), Y(0.20), '0.11', { size: 9 }));
  return o.join('');
};
{
  const oy = 1620;
  g.push(coupeGC(400, oy, 'verre'));
  g.push(detailTitle(210, 726, 'G1', 'PANNEAU DE VERRE — COUPE VERTICALE', 'ÉCHELLE 1:5'));
  g.push(nomenclature(210, 1740, [
    ['1', 'Verre feuilleté 8.8.4 (17,5 mm), panneau plat de 40 cm'],
    ['2', 'Pinces inox 316 haute et basse, cale EPDM, serrage à la clé dynamo.'],
    ['3', 'Platine inox 110 × 110 × 10, 2 goujons M10 inox scellés dans la dalle'],
    ['4', 'Main courante inox Ø 42 × 2 mm, brossée grain 240, continue'],
  ], { size: 8.6 }));

  g.push(coupeGC(1060, oy, 'inox'));
  g.push(detailTitle(870, 726, 'G2', 'BARREAUDAGE INOX — COUPE VERTICALE', 'ÉCHELLE 1:5'));
  g.push(nomenclature(870, 1740, [
    ['1', 'Barreaux inox 316 Ø 16, entraxe 11 cm — moins de 11 cm entre nus'],
    ['2', 'Lisse basse inox 110 × 25, soudée sur les montants'],
    ['3', 'Montants inox Ø 42 aux deux extrémités de chaque section de 40 cm'],
    ['4', 'Même platine et même main courante que le panneau de verre'],
  ], { size: 8.6 }));
}

// ===========================================================================
// G3 — CE QUE COUTE UNE CORDE DE 40 cm : le pire panneau de verre, agrandi
// ===========================================================================
{
  const seg = SEG[kPire], u1 = seg.x1, u2 = seg.x2;
  const S = 1150, ox = 1620, oy = 1080;
  const yMid = (ondeAt(u1) + ondeAt(u2)) / 2;
  const X = (u) => +(ox + (u - (u1 + u2) / 2) * S).toFixed(2);
  const Y = (d) => +(oy - (d - yMid) * S).toFixed(2);
  const pad = 0.14, pts = [];
  for (let i = 0; i <= 200; i++) { const u = u1 - pad + (u2 - u1 + 2 * pad) * i / 200; pts.push([X(u), Y(ondeAt(u))]); }
  g.push(`<path d="${pts.map(([x, y], i) => `${i ? 'L' : 'M'} ${x} ${y}`).join(' ')}" fill="none" stroke="${D.ink}" stroke-width="2.4"/>`);
  g.push(txt(X(u2 + pad), Y(ondeAt(u2 + pad)) - 14, 'RIVE THÉORIQUE', { size: 8, fill: D.ink, ls: '0.12em', weight: 700, anchor: 'end' }));
  // la corde : le panneau plat
  g.push(`<path d="M ${X(u1)} ${Y(ondeAt(u1))} L ${X(u2)} ${Y(ondeAt(u2))}" stroke="${D.verreL}" stroke-width="9" stroke-linecap="butt" opacity="0.95"/>`);
  g.push(txt((X(u1) + X(u2)) / 2, (Y(ondeAt(u1)) + Y(ondeAt(u2))) / 2 - 22, 'PANNEAU DE VERRE PLAT — 40 cm', { size: 9, fill: '#5E7A80', ls: '0.1em', weight: 700 }));
  // la fleche, au point le plus ecarte
  let best = null;
  for (let i = 1; i < 200; i++) {
    const t = i / 200, uu = u1 + (u2 - u1) * t, dd = ondeAt(uu);
    const num = Math.abs((ondeAt(u2) - ondeAt(u1)) * (uu - u1) - (u2 - u1) * (dd - ondeAt(u1)));
    const f = num / Math.hypot(u2 - u1, ondeAt(u2) - ondeAt(u1));
    if (!best || f > best.f) best = { f, uu, dd, t };
  }
  const cu = u1 + (u2 - u1) * best.t, cd = ondeAt(u1) + (ondeAt(u2) - ondeAt(u1)) * best.t;
  g.push(`<path d="M ${X(best.uu)} ${Y(best.dd)} L ${X(cu)} ${Y(cd)}" stroke="#B4392F" stroke-width="2.4"/>`);
  g.push(`<circle cx="${X(best.uu)}" cy="${Y(best.dd)}" r="4" fill="#B4392F"/>`);
  g.push(txt(X(best.uu) + 14, Y(best.dd) + 26, `FLÈCHE ${(best.f * 1000).toFixed(0)} mm`, { size: 12, fill: '#B4392F', weight: 700, anchor: 'start' }));
  for (const u of [u1, u2]) g.push(`<circle cx="${X(u)}" cy="${Y(ondeAt(u))}" r="6" fill="#FFFFFF" stroke="${D.ink}" stroke-width="1.8"/>`);
  g.push(detailTitle(1450, 726, 'G3', 'CE QUE COÛTE UNE CORDE DE 40 cm', `AGRANDISSEMENT · PANNEAU LE PLUS DÉFAVORABLE, AU CREUX MÉDIAN`));
  g.push(nomenclature(1450, 1360, [
    ['', `Un panneau plat de 40 cm posé sur la rive s’écarte au maximum de ${(flVerre * 1000).toFixed(0)} mm`],
    ['', `de la courbe théorique — et seulement dans les deux zones les plus`],
    ['', `serrées (rayon 0,77 m à la crête et au creux). Ailleurs c’est 5 à 10 mm.`],
    ['', ''],
    ['', `Rotation d’un panneau de verre au suivant : ${devVerre.toFixed(0)}° au plus défavorable.`],
    ['', 'Elle demande des pinces à rotule, pas des pinces droites — à vérifier'],
    ['', 'avec le fournisseur avant commande.'],
    ['', ''],
    ['', 'SI VOUS VOULEZ LA COURBE PLUS FRANCHE : passer les panneaux à 20 cm'],
    ['', `dans les deux zones serrées ramène la flèche à 6 mm et la rotation à 9°.`],
    ['', 'Le rythme 40/40 reste lisible partout ailleurs.'],
  ], { size: 9 }));
}

g.unshift(PATTERNS(755.91));
const body = `<div style="width: ${W}px; background: #FFFFFF">
${header({ w: W, kicker: 'Carnet de détails · garde-corps',
  title: 'Le garde-corps, panneau par panneau',
  sub: `Le garde-corps suit la rive par une suite de cordes de 40 cm : un panneau de verre feuilleté plat, puis 40 cm de barreaudage inox, en alternance sur les ${L.toFixed(2)} ml développés — ${SEG.length} panneaux par balcon. Le barreaudage épouse n’importe quel rayon ; le verre, plat, s’écarte de la courbe de 5 à 10 mm sur la plus grande partie de la rive et de ${(flVerre * 1000).toFixed(0)} mm au plus défavorable. Voir G3.`,
  right: 'A2 PAYSAGE · ÉCHELLES 1:20 ET 1:5<br>COTES EN MÈTRES<br>NIVEAU COURANT R+3 À R+8' })}
<svg viewBox="0 0 ${W} ${SVGH}" width="${W}" height="${SVGH}" xmlns="http://www.w3.org/2000/svg" style="display: block">${g.join('\n')}</svg>
</div>`;
writeFileSync('Detail-Garde-Corps.dc.html', page({ body, props: JSON.stringify({ $preview: { width: W, height: SVGH + 220 } }) }));
console.log('Detail-Garde-Corps.dc.html ok — fleche max', (flMax * 1000).toFixed(2), 'mm · rotation max', devMax.toFixed(2), 'deg');
