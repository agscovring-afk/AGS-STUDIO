import { writeFileSync } from 'node:fs';
import { XS, COL, PBW, RETRAIT, AXE, BV_EP, BALCON_NICHE, BALCON_NICHE_P, GCN, PBN, GC } from './geo.mjs';
import { page, header } from './page.mjs';
import { txt, dimH, dimV } from './svgkit.mjs';
import { D, PATTERNS, callout, nomenclature, detailTitle, axe } from './detailkit.mjs';

// ---------------------------------------------------------------------------
// Coupes horizontales de detail. Le plan de coupe passe a 1,50 m du sol fini,
// donc au droit des vantaux. Repere local : X = abscisse de facade (m),
// Y = profondeur, positive vers l'exterieur, 0 au nu de facade.
// ---------------------------------------------------------------------------
const W = 2244, SVGH = 1560, S = 377.95;          // 1:10
const g = [];
const mk = (ox, oy) => {
  const PX = (x) => +(ox + x * S).toFixed(2);
  const PY = (y) => +(oy - y * S).toFixed(2);     // exterieur vers le haut
  const R = (x1, x2, y1, y2, fill, extra = '') =>
    `<rect x="${PX(x1)}" y="${PY(y2)}" width="${((x2 - x1) * S).toFixed(2)}" height="${((y2 - y1) * S).toFixed(2)}" fill="${fill}" ${extra}/>`;
  const L = (x1, y1, x2, y2, c, w = 1) =>
    `<path d="M ${PX(x1)} ${PY(y1)} L ${PX(x2)} ${PY(y2)}" stroke="${c}" stroke-width="${w}" fill="none"/>`;
  return { PX, PY, R, L };
};
const STROKE = `stroke="${D.ink}" stroke-width="1.1"`;
const FIN = `stroke="${D.fine}" stroke-width="0.7"`;
const rupture = (y, x1, x2) => {
  const n = Math.max(3, Math.round((x2 - x1) / 26)), p = [`M ${x1} ${y}`];
  for (let i = 1; i <= n; i++) p.push(`L ${x1 + (x2 - x1) * (i - 0.5) / n} ${y + (i % 2 ? 8 : -8)}`);
  p.push(`L ${x2} ${y}`);
  return `<path d="${p.join(' ')}" fill="none" stroke="${D.dim}" stroke-width="1"/>`;
};
const rep = (n, x, y, dx, dy) => callout(n, x, y, x + dx, y + dy, '', { mid: x + dx * 0.55 });

// Un montant de menuiserie alu TPR 65 vu en coupe horizontale, largeur totale
// 0.065 m, avec sa rupture de pont thermique et le double vitrage 4/16/4.
const montant = (m, x, ep = 0.065, yIn = -0.02, yOut = 0.045) => {
  const { PX, PY, R } = m, o = [];
  o.push(R(x - ep / 2, x + ep / 2, yIn, yOut, 'url(#gAlu)', STROKE));
  o.push(R(x - ep / 2 + 0.012, x + ep / 2 - 0.012, yIn + 0.016, yOut - 0.016, '#8A8F93', FIN));
  return o.join('');
};
const vitrage = (m, x1, x2, y = 0.012) => {
  const { PX, PY, R, L } = m, o = [];
  o.push(R(x1, x2, y - 0.012, y + 0.012, 'url(#gVerre)', `stroke="${D.verreL}" stroke-width="0.9"`));
  o.push(L(x1, y, x2, y, D.verreL, 0.7));
  return o.join('');
};
// double cloison : brique 15 + lame d'air 5 + brique 10 + monocouche 15 mm
const mur = (m, x1, x2) => {
  const { R } = m;
  return [R(x1, x2, -0.30, -0.15, 'url(#pBrique)', STROKE),
          R(x1, x2, -0.15, -0.10, 'url(#pIsol)', FIN),
          R(x1, x2, -0.10, 0.0, 'url(#pBrique)', STROKE),
          R(x1, x2, 0.0, 0.015, 'url(#pMono)', STROKE)].join('');
};

// ===========================================================================
// H1 — POTEAU 55 cm ET TABLEAU DE BAIE
// ===========================================================================
{
  const M = mk(190 - 9.65 * S, 340);              // le poteau demarre a x = 190 px
  const { PX, PY, R, L } = M;
  const [c1, c2] = XS.c3;                         // poteau 9.65 .. 10.20
  g.push(R(c1, c2, -0.30, 0.0, 'url(#pBeton)', STROKE));            // poteau BA 55 x 30
  g.push(R(c1, c2, 0.0, 0.015, 'url(#pMono)', STROKE));
  g.push(mur(M, c2, c2 + 0.62));                                     // retour de mur
  g.push(R(c2 + 0.62, c2 + 0.90, -0.30, -0.10, 'url(#pBrique)', STROKE));  // tableau : retour
  g.push(R(c2 + 0.62, c2 + 0.90, -0.10, 0.0, 'url(#pIsol)', FIN));
  g.push(montant(M, c2 + 0.66));                                     // dormant lateral
  g.push(vitrage(M, c2 + 0.695, c2 + 1.30));
  g.push(R(c2 + 0.90, c2 + 1.30, 0.0, 0.015, 'url(#pMono)', FIN));
  g.push(R(c2 + 0.62, c2 + 0.695, 0.028, 0.045, 'url(#gAlu)', FIN));  // couvre-joint
  g.push(axe(PX((c1 + c2) / 2), PY(-0.40), PX((c1 + c2) / 2), PY(0.10)));
  g.push(rupture(PY(-0.30) + 0, PX(c2 + 1.30), PX(c2 + 1.30)));
  g.push(`<path d="M ${PX(c2 + 1.30)} ${PY(-0.32)} L ${PX(c2 + 1.30)} ${PY(0.05)}" stroke="${D.dim}" stroke-width="1" stroke-dasharray="7 5"/>`);
  g.push(dimH(PX(c1), PX(c2), PY(-0.44), COL.toFixed(2), { size: 9.5 }));
  g.push(dimH(PX(c2), PX(c2 + 0.66), PY(-0.44), '0.66', { size: 9.5 }));
  g.push(dimV(PY(0.015), PY(-0.30), PX(c1) - 30, '0.315', { size: 9 }));
  [[1, PX(9.92), PY(-0.16), -40, -46], [2, PX(10.50), PY(-0.22), 4, -52], [3, PX(10.50), PY(-0.125), 60, 40],
   [4, PX(10.86), PY(0.012), 46, -44], [5, PX(11.10), PY(0.012), 40, 46], [6, PX(10.79), PY(0.037), -34, -50]]
    .forEach(([n, x, y, dx, dy]) => g.push(rep(n, x, y, dx, dy)));
  g.push(detailTitle(170, 178, 'H1', 'POTEAU 55 cm ET TABLEAU DE BAIE', 'ÉCHELLE 1:10 · COUPE HORIZONTALE À +1,50'));
  g.push(nomenclature(170, 560, [
    ['1', 'Poteau BA 55 × 30 — c’est lui qui donne la trame de la façade'],
    ['2', 'Double cloison brique creuse 15 + lame d’air 5 + brique 10'],
    ['3', 'Retour de tableau : la brique intérieure vient buter sur le dormant,'],
    ['', 'la lame d’air est fermée par un about isolant'],
    ['4', 'Dormant latéral alu TPR 65 à rupture de pont thermique, RAL 7024'],
    ['5', 'Double vitrage 4/16/4, joint EPDM, calage périphérique'],
    ['6', 'Couvre-joint alu et mastic sur fond de joint, 8 mm'],
  ], { size: 8.6 }));
}

// ===========================================================================
// H2 — TRUMEAU ENTRE LES DEUX PORTES-BALCON, AVEC LE PROFIL LED VERTICAL
// ===========================================================================
{
  const M = mk(1030 - 12.55 * S, 340);
  const { PX, PY, R, L } = M;
  const a = 12.90, b = 14.25;                     // trumeau de 1.35 m entre les deux baies
  g.push(mur(M, a - 0.02, b + 0.02));
  g.push(montant(M, a - 0.03));
  g.push(montant(M, b + 0.03));
  g.push(vitrage(M, a - 0.60, a - 0.062));
  g.push(vitrage(M, b + 0.062, b + 0.60));
  // niche du profil LED vertical, 60 x 40 mm dans le monocouche
  const c = (a + b) / 2;
  g.push(R(c - 0.03, c + 0.03, -0.025, 0.015, '#FFFFFF', STROKE));
  g.push(R(c - 0.026, c + 0.026, -0.021, 0.006, 'url(#gAlu)', FIN));
  g.push(R(c - 0.019, c + 0.019, -0.006, 0.002, D.led, ''));
  g.push(`<path d="M ${PX(c)} ${PY(0.02)} l -26 -34 M ${PX(c)} ${PY(0.02)} l 26 -34 M ${PX(c)} ${PY(0.02)} l 0 -40" stroke="${D.led}" stroke-width="1.1" opacity="0.5" fill="none"/>`);
  g.push(`<path d="M ${PX(a - 0.60)} ${PY(-0.32)} L ${PX(a - 0.60)} ${PY(0.05)} M ${PX(b + 0.60)} ${PY(-0.32)} L ${PX(b + 0.60)} ${PY(0.05)}" stroke="${D.dim}" stroke-width="1" stroke-dasharray="7 5"/>`);
  g.push(dimH(PX(a), PX(b), PY(-0.44), '1.35', { size: 9.5 }));
  g.push(dimH(PX(c - 0.03), PX(c + 0.03), PY(0.12), '0.06', { size: 9 }));
  [[1, PX(a - 0.30), PY(-0.22), -10, -52], [2, PX(c), PY(-0.004), 0, 62], [3, PX(a - 0.03), PY(0.012), -46, 46],
   [4, PX(b + 0.30), PY(0.008), 40, -50]]
    .forEach(([n, x, y, dx, dy]) => g.push(rep(n, x, y, dx, dy)));
  g.push(detailTitle(1030, 178, 'H2', 'TRUMEAU ENTRE LES DEUX PORTES-BALCON', 'ÉCHELLE 1:10 · COUPE HORIZONTALE À +1,50'));
  g.push(nomenclature(1030, 560, [
    ['1', 'Trumeau de 1,35 m entre les deux porte-balcon d’un même balcon'],
    ['2', 'Profil LED vertical encastré 60 × 40 mm, hauteur 1,90 m, 3000 K,'],
    ['', 'diffuseur affleurant le monocouche — même circuit que la gorge de rive'],
    ['3', 'Montants alu TPR 65 des deux baies, RAL 7024'],
    ['4', 'Double vitrage 4/16/4 — porte-balcon 1,80 × 2,20 m'],
  ], { size: 8.6 }));
}

// ===========================================================================
// H3 — LE VIDE CENTRAL : deux balcons et le brise-vue entre eux
// ===========================================================================
{
  const M = mk(190 - 7.30 * S, 861);
  const { PX, PY, R, L } = M;
  const [n1, n2] = XS.vide;
  // les deux blocs de part et d'autre du vide
  g.push(mur(M, n1 - 0.55, n1));
  g.push(mur(M, n2, n2 + 0.55));
  g.push(R(n1 - 0.55, n1, -0.30, 0.015, 'none', STROKE));
  // flancs de la fente : ils sont en retrait de 1,50 m
  g.push(R(n1 - 0.30, n1, -RETRAIT, 0.0, 'url(#pBrique)', STROKE));
  g.push(R(n2, n2 + 0.30, -RETRAIT, 0.0, 'url(#pBrique)', STROKE));
  g.push(R(n1 - 0.30, n1, -RETRAIT, -RETRAIT + 0.0, 'none'));
  // refend de fond + portes-fenetres, une par logement
  for (const [h1, h2] of [[n1, AXE - BV_EP / 2], [AXE + BV_EP / 2, n2]]) {
    const c = (h1 + h2) / 2;
    g.push(R(h1, h2, -RETRAIT - 0.30, -RETRAIT, 'url(#pBrique)', STROKE));
    g.push(R(c - PBN / 2, c + PBN / 2, -RETRAIT - 0.30, -RETRAIT, D.paper, ''));
    g.push(montant(M, c - PBN / 2 + 0.033, 0.065, -RETRAIT - 0.05, -RETRAIT + 0.02));
    g.push(montant(M, c + PBN / 2 - 0.033, 0.065, -RETRAIT - 0.05, -RETRAIT + 0.02));
    g.push(vitrage(M, c - PBN / 2 + 0.066, c + PBN / 2 - 0.066, -RETRAIT - 0.015));
    // dalle du balcon, de la porte au garde-corps
    g.push(R(h1, h2, -RETRAIT, -GCN, D.carr, FIN));
    // garde-corps verre feuillete 8.8.4 + main courante inox
    g.push(R(h1 + 0.02, h2 - 0.02, -GCN - 0.009, -GCN + 0.009, 'url(#gVerre)', `stroke="${D.verreL}" stroke-width="1"`));
    for (const x of [h1 + 0.04, h2 - 0.04])
      g.push(`<circle cx="${PX(x)}" cy="${PY(-GCN)}" r="4.5" fill="${D.inox}" stroke="${D.inoxD}" stroke-width="0.9"/>`);
  }
  // le brise-vue : 40 cm, sur l'axe, du refend au garde-corps
  g.push(R(AXE - BV_EP / 2, AXE + BV_EP / 2, -RETRAIT - 0.30, -GCN, 'url(#gAlu)', STROKE));
  for (let y = -RETRAIT + 0.06; y < -GCN - 0.02; y += 0.09)
    g.push(L(AXE - BV_EP / 2, y, AXE + BV_EP / 2, y, '#7E858A', 1.4));
  g.push(R(AXE - BV_EP / 2 - 0.03, AXE + BV_EP / 2 + 0.03, -GCN - 0.03, -GCN, D.inox, FIN));
  g.push(axe(PX(AXE), PY(-RETRAIT - 0.42), PX(AXE), PY(0.16)));
  g.push(rupture(PY(-0.30), PX(n1 - 0.55), PX(n1 - 0.30)));
  g.push(rupture(PY(-0.30), PX(n2 + 0.30), PX(n2 + 0.55)));
  g.push(dimH(PX(n1), PX(AXE - BV_EP / 2), PY(0.16), BALCON_NICHE.toFixed(2), { size: 9.5 }));
  g.push(dimH(PX(AXE - BV_EP / 2), PX(AXE + BV_EP / 2), PY(0.16), BV_EP.toFixed(2), { size: 9.5 }));
  g.push(dimH(PX(AXE + BV_EP / 2), PX(n2), PY(0.16), BALCON_NICHE.toFixed(2), { size: 9.5 }));
  g.push(dimH(PX(n1), PX(n2), PY(0.34), '1.80', { size: 10 }));
  g.push(dimV(PY(0), PY(-GCN), PX(n2 + 0.42), GCN.toFixed(2), { size: 9 }));
  g.push(dimV(PY(-GCN), PY(-RETRAIT), PX(n2 + 0.42), BALCON_NICHE_P.toFixed(2), { size: 9 }));
  [[1, PX(8.20), PY(-1.10), -54, 34], [2, PX(AXE), PY(-1.05), 52, -34], [3, PX(8.20), PY(-GCN), -56, -30],
   [4, PX(9.30), PY(-1.52), 56, 34], [5, PX(n2 + 0.15), PY(-0.80), 56, -20]]
    .forEach(([n, x, y, dx, dy]) => g.push(rep(n, x, y, dx, dy)));
  g.push(detailTitle(170, 690, 'H3', 'LE VIDE CENTRAL — DEUX BALCONS, LE BRISE-VUE ENTRE EUX', 'ÉCHELLE 1:10 · COUPE HORIZONTALE À +1,50'));
  g.push(nomenclature(1400, 900, [
    ['1', 'Balcon du logement de gauche — 0,70 × 0,80 m'],
    ['2', 'Brise-vue aluminium RAL 7024, 40 cm de large, lames horizontales'],
    ['', 'sur ossature alu, du refend de fond jusqu’au garde-corps'],
    ['3', 'Garde-corps verre feuilleté 8.8.4, h 1,10 m, 2 pinces inox par panneau —'],
    ['', 'il s’arrête à 0,70 m en arrière du nu : la fente reste ouverte devant'],
    ['4', 'Porte-fenêtre 0,70 m depuis le logement, alu TPR 65 RAL 7024'],
    ['5', 'Flanc de la fente : brique + monocouche, retour de 1,50 m'],
  ], { size: 8.6 }));
}

g.unshift(PATTERNS(S));
const body = `<div style="width: ${W}px; background: #FFFFFF">
${header({ w: W, kicker: 'Carnet de détails · coupes horizontales',
  title: 'La façade coupée à hauteur d’homme',
  sub: 'Trois coupes horizontales au 1:10, plan de coupe à +1,50 m du sol fini : le poteau de 55 cm avec le tableau de la baie, le trumeau de 1,35 m qui porte le profil LED vertical, et le vide central avec ses deux balcons séparés par le brise-vue de 40 cm.',
  right: 'A2 PAYSAGE · ÉCHELLE 1:10<br>COTES EN MÈTRES<br>NIVEAU COURANT R+3 À R+8' })}
<svg viewBox="0 0 ${W} ${SVGH}" width="${W}" height="${SVGH}" xmlns="http://www.w3.org/2000/svg" style="display: block">${g.join('\n')}</svg>
</div>`;
writeFileSync('Details-Horizontaux.dc.html', page({ body, props: JSON.stringify({ $preview: { width: W, height: SVGH + 220 } }) }));
console.log('Details-Horizontaux.dc.html ok');
