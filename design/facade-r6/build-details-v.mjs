import { writeFileSync } from 'node:fs';
import { FASCIA, GC, PBH, DALLE, ACROTERE, HSP } from './geo.mjs';
import { page, header } from './page.mjs';
import { txt, dimH, dimV } from './svgkit.mjs';
import { D, PATTERNS, callout, nomenclature, detailTitle } from './detailkit.mjs';

// ---------------------------------------------------------------------------
// Coupes verticales de detail, 1:10. Repere local par detail :
// Y = distance au nu de reference (positif vers l'exterieur), Z = altitude.
// ---------------------------------------------------------------------------
const W = 2244, SVGH = 1010, S = 377.95;          // 1:10 a 96 dpi
const BASE = 745;                                  // ligne de pied commune
const g = [];
const mk = (ox, oy) => {
  const X = (y) => +(ox + y * S).toFixed(2);
  const Y = (z) => +(oy - z * S).toFixed(2);
  const R = (y1, y2, z1, z2, fill, extra = '') =>
    `<rect x="${X(y1)}" y="${Y(z2)}" width="${((y2 - y1) * S).toFixed(2)}" height="${((z2 - z1) * S).toFixed(2)}" fill="${fill}" ${extra}/>`;
  const L = (y1, z1, y2, z2, c, w = 1) =>
    `<path d="M ${X(y1)} ${Y(z1)} L ${X(y2)} ${Y(z2)}" stroke="${c}" stroke-width="${w}" fill="none"/>`;
  const P = (pts, fill, extra = '') =>
    `<path d="${pts.map(([y, z], i) => `${i ? 'L' : 'M'} ${X(y)} ${Y(z)}`).join(' ')} Z" fill="${fill}" ${extra}/>`;
  return { X, Y, R, L, P };
};
const STROKE = `stroke="${D.ink}" stroke-width="1.1"`;
const FIN = `stroke="${D.fine}" stroke-width="0.7"`;
const rupture = (x, y1, y2) => {
  const n = Math.max(3, Math.round((y2 - y1) / 26)), p = [`M ${x} ${y1}`];
  for (let i = 1; i <= n; i++) p.push(`L ${x + (i % 2 ? 8 : -8)} ${y1 + (y2 - y1) * (i - 0.5) / n}`);
  p.push(`L ${x} ${y2}`);
  return `<path d="${p.join(' ')}" fill="none" stroke="${D.dim}" stroke-width="1"/>`;
};
// bulle posee tout pres de l'element, leader court
const rep = (n, x, y, dx, dy) => callout(n, x, y, x + dx, y + dy, '', { mid: x + dx * 0.55 });

// ===========================================================================
// D1 — RIVE DE BALCON
// ===========================================================================
{
  const ox = 405, oy = BASE - 0.60 * S, m = mk(ox, oy);
  const { X, Y, R, L, P } = m;
  const Y1 = -0.62, Y2 = 0.20;
  g.push(R(Y1, 0, -0.26, -0.06, 'url(#pBeton)', STROKE));                 // dalle BA 20
  g.push(R(-0.10, 0, -0.06, 0.06, 'url(#pBeton)', STROKE));               // costiere
  g.push(P([[Y1, -0.06], [-0.10, -0.06], [-0.10, -0.028], [Y1, -0.012]], 'url(#pChape)', FIN));
  g.push(`<path d="M ${X(Y1)} ${Y(-0.012)} L ${X(-0.10)} ${Y(-0.028)} L ${X(-0.10)} ${Y(0.06)}" fill="none" stroke="${D.etan}" stroke-width="2.4"/>`);
  g.push(P([[Y1, -0.012], [-0.10, -0.028], [-0.10, 0.0], [Y1, 0.0]], D.carr, FIN));
  for (let y = Y1 + 0.12; y < -0.11; y += 0.22) g.push(L(y, 0.0, y, -0.02, D.fine, 0.7));
  g.push(R(0, Y2, -0.45, 0.06, 'url(#pAqua)', STROKE));                   // bandeau Aquapanel
  g.push(R(0.022, 0.052, -0.42, 0.02, D.inox, FIN));
  g.push(R(0.148, 0.178, -0.42, 0.02, D.inox, FIN));
  g.push(L(0.022, -0.19, 0.178, -0.19, D.inoxD, 1.5));
  g.push(L(0.022, -0.02, 0.178, -0.02, D.inoxD, 1.5));
  g.push(R(0.095, 0.145, -0.45, -0.40, '#FFFFFF', STROKE));               // gorge LED 50x50
  g.push(R(0.101, 0.139, -0.444, -0.414, D.alu, FIN));
  g.push(R(0.106, 0.134, -0.433, -0.421, D.led));
  g.push(`<path d="M ${X(0.12)} ${Y(-0.458)} l -20 30 M ${X(0.12)} ${Y(-0.458)} l 20 30 M ${X(0.12)} ${Y(-0.458)} l 0 34" stroke="${D.led}" stroke-width="1.1" opacity="0.5" fill="none"/>`);
  g.push(R(0.182, 0.20, -0.45, -0.428, D.paper, STROKE));                 // larmier
  const gy = -0.20;                                                       // garde-corps
  g.push(R(gy - 0.05, gy + 0.05, 0.0, 0.012, D.inox, FIN));
  g.push(R(gy - 0.009, gy + 0.009, 0.06, GC - 0.03, 'url(#gVerre)', `stroke="${D.verreL}" stroke-width="0.9"`));
  g.push(R(gy - 0.022, gy + 0.022, 0.012, 0.10, 'url(#gAlu)', `stroke="${D.inoxD}" stroke-width="0.8"`));
  g.push(`<circle cx="${X(gy)}" cy="${Y(GC)}" r="${(0.021 * S).toFixed(1)}" fill="${D.inox}" stroke="${D.inoxD}" stroke-width="1"/>`);
  g.push(`<circle cx="${X(gy)}" cy="${Y(0.006)}" r="3" fill="${D.inoxD}"/>`);
  g.push(dimV(Y(0), Y(GC), X(-0.50), '1.10', { size: 9.5 }));
  g.push(dimV(Y(-0.45), Y(0), X(0.30), FASCIA.toFixed(2), { size: 9.5 }));
  g.push(dimV(Y(-0.26), Y(-0.06), X(-0.74), DALLE.toFixed(2), { size: 9.5 }));
  g.push(dimH(X(0), X(Y2), Y(-0.56), '0.20', { size: 9.5 }));
  g.push(dimH(X(gy), X(0), Y(0.30), '0.20', { size: 9 }));
  g.push(rupture(X(Y1), Y(-0.28), Y(0.02)));
  [[1, X(-0.40), Y(-0.16), -52, 26], [2, X(-0.30), Y(-0.02), -52, -30], [3, X(0.075), Y(-0.24), 62, -18],
   [4, X(0.12), Y(-0.427), 66, 22], [5, X(gy), Y(0.62), -60, -22], [6, X(gy), Y(0.006), -58, 34],
   [7, X(-0.05), Y(0.03), -34, -56], [8, X(0.191), Y(-0.439), 56, 34]]
    .forEach(([n, x, y, dx, dy]) => g.push(rep(n, x, y, dx, dy)));
  g.push(detailTitle(170, 42, 'D1', 'RIVE DE BALCON — AU GRAND LOBE', 'ÉCHELLE 1:10'));
  g.push(nomenclature(170, 812, [
    ['1', 'Dalle BA 20 cm en porte-à-faux, coffrage cintré suivant l’onde'],
    ['2', 'Forme de pente 1,5 % + étanchéité SEL bicouche, relevé 12 cm'],
    ['3', 'Ossature acier galvanisé cintrée + Aquapanel Outdoor 12,5 mm,'],
    ['', 'enduit armé, monocouche blanc — habillage 20 cm au nu de la dalle'],
    ['4', 'Gorge 50 × 50 mm, profil alu + ruban LED 3000 K IP65'],
    ['5', 'Garde-corps h 1,10 m, cordes de 38 cm sur l’onde — tout verre 8.8.4,'],
    ['', 'tout inox Ø 16 ou fer forgé ; main courante Ø 42 continue'],
    ['6', 'Platine inox 100 × 100 × 8, 2 goujons M10 inox, manchette d’étanchéité'],
    ['7', 'Costière béton 10 × 12 cm en rive, support du relevé'],
    ['8', 'Larmier 18 mm en pied de bandeau'],
  ], { size: 8.6 }));
}

// ===========================================================================
// D2 — SEUIL DE PORTE-BALCON
// ===========================================================================
{
  const ox = 900, oy = BASE - 0.30 * S, m = mk(ox, oy);
  const { X, Y, R, L, P } = m;
  const IN = -0.58, OUT = 0.56, TOP = 1.24;
  g.push(R(IN, OUT, -0.26, -0.06, 'url(#pBeton)', STROKE));
  g.push(R(IN, 0, -0.06, -0.02, 'url(#pMortier)', FIN));
  g.push(R(IN, 0, -0.02, 0.0, D.carr, STROKE));
  g.push(R(IN, IN + 0.018, 0.0, 0.09, D.carr, FIN));
  g.push(P([[0.065, -0.06], [OUT, -0.06], [OUT, -0.042], [0.065, -0.028]], 'url(#pChape)', FIN));
  g.push(`<path d="M ${X(0.065)} ${Y(0.10)} L ${X(0.065)} ${Y(-0.028)} L ${X(OUT)} ${Y(-0.042)}" fill="none" stroke="${D.etan}" stroke-width="2.4"/>`);
  for (const y of [0.17, 0.35, 0.51]) g.push(R(y - 0.024, y + 0.024, -0.038, -0.016, D.plot, FIN));
  g.push(R(0.115, OUT, -0.016, 0.0, D.carr, STROKE));
  g.push(R(0.068, 0.112, -0.038, 0.0, '#FFFFFF', FIN));                   // caniveau
  for (let z = -0.034; z < -0.002; z += 0.009) g.push(L(0.070, z, 0.110, z, D.inox, 1.6));
  g.push(R(0.0, 0.065, 0.0, 0.10, 'url(#gAlu)', STROKE));                 // seuil alu
  g.push(R(0.027, 0.038, 0.014, 0.088, '#8A8F93', FIN));
  g.push(R(0.004, 0.061, 0.10, TOP, 'url(#gAlu)', STROKE));               // dormant + ouvrant
  g.push(R(0.027, 0.038, 0.112, TOP, '#8A8F93', FIN));
  g.push(R(0.019, 0.046, 0.17, TOP, 'url(#gVerre)', `stroke="${D.verreL}" stroke-width="0.9"`));
  g.push(L(0.0325, 0.17, 0.0325, TOP, D.verreL, 0.7));
  g.push(R(-0.016, 0.004, 0.10, TOP, 'url(#pMono)', FIN));
  g.push(`<rect x="${X(-0.007)}" y="${Y(0.104)}" width="${(0.014 * S).toFixed(2)}" height="7" fill="${D.alu}"/>`);
  g.push(rupture(X(IN), Y(-0.28), Y(0.11)));
  g.push(rupture(X(OUT), Y(-0.28), Y(0.02)));
  g.push(`<path d="M ${X(0.004)} ${Y(TOP)} L ${X(0.061)} ${Y(TOP)}" stroke="${D.dim}" stroke-width="1.2" stroke-dasharray="6 4"/>`);
  g.push(dimV(Y(-0.02), Y(0), X(OUT + 0.16), '0.02', { size: 9 }));
  g.push(dimV(Y(-0.26), Y(-0.06), X(IN - 0.12), DALLE.toFixed(2), { size: 9.5 }));
  g.push(dimH(X(0.004), X(0.061), Y(1.36), '0.065', { size: 9 }));
  [[1, X(-0.32), Y(-0.01), -34, -56], [2, X(0.33), Y(-0.008), 40, -56], [3, X(0.35), Y(-0.027), 58, 34],
   [4, X(0.09), Y(-0.02), -12, 62], [5, X(0.032), Y(0.05), -70, 30], [6, X(0.032), Y(0.72), 70, -26]]
    .forEach(([n, x, y, dx, dy]) => g.push(rep(n, x, y, dx, dy)));
  g.push(detailTitle(680, 42, 'D2', 'SEUIL DE PORTE-BALCON', 'ÉCHELLE 1:10'));
  g.push(nomenclature(680, 812, [
    ['1', 'Intérieur : carrelage sur chape, niveau fini de l’étage'],
    ['2', 'Balcon : grès cérame 60 × 60 sur plots réglables, 2 cm plus bas'],
    ['', 'que l’intérieur — la pluie ne remonte jamais dans le logement'],
    ['3', 'Plots PVC réglables, lame d’air ventilée sous le carrelage'],
    ['4', 'Caniveau de rive 45 mm, grille inox, raccordé à la descente EP'],
    ['5', 'Seuil aluminium à rupture de pont thermique, rejingot 10 cm,'],
    ['', 'relevé d’étanchéité 12 cm derrière le dormant'],
    ['6', 'Alu TPR série 65 RAL 7024, 2 vantaux coulissants, 4/16/4'],
  ], { size: 8.6 }));
}

// ===========================================================================
// D3 — JONCTION PLANCHER (repere local : 0 = tete de porte, a +2.20)
// ===========================================================================
{
  const ox = 1450, oy = BASE - 0.34 * S, m = mk(ox, oy);
  const { X, Y, R, L } = m;
  const IN = -0.55, zD = HSP - PBH, zT = zD + DALLE;
  g.push(R(IN, 0.02, 0, 0.30, 'url(#pBeton)', STROKE));                   // linteau BA 20x30
  g.push(R(IN, -0.10, 0.30, zD, 'url(#pBrique)', STROKE));                // brique 15
  g.push(R(-0.10, -0.05, 0.30, zD, 'url(#pIsol)', FIN));                  // lame d'air 5
  g.push(R(-0.05, 0.02, 0.30, zD, 'url(#pBrique)', STROKE));              // brique 10
  g.push(R(IN, 0.02, zD, zT, 'url(#pBeton)', STROKE));                    // plancher
  g.push(R(0.02, 0.32, zD, zT, 'url(#pBeton)', STROKE));                  // dalle de balcon au-dessus
  g.push(R(0.02, 0.037, -0.34, zT + 0.30, 'url(#pMono)', STROKE));        // monocouche 15 mm
  g.push(R(0.02, 0.037, zD + 0.025, zD + 0.055, D.dim, ''));              // joints creux 15x15
  g.push(R(0.02, 0.037, zT - 0.055, zT - 0.025, D.dim, ''));
  g.push(R(0.004, 0.061, -0.34, 0, 'url(#gAlu)', STROKE));                // dormant haut
  g.push(R(0.027, 0.038, -0.34, -0.012, '#8A8F93', FIN));
  g.push(R(0.019, 0.046, -0.34, -0.055, 'url(#gVerre)', `stroke="${D.verreL}" stroke-width="0.9"`));
  g.push(R(-0.016, 0.004, -0.34, 0, 'url(#pMono)', FIN));
  g.push(rupture(X(IN), Y(-0.02), Y(zT + 0.28)));
  g.push(rupture(X(0.32), Y(zD + 0.01), Y(zT - 0.01)));
  g.push(`<path d="M ${X(0.004)} ${Y(-0.34)} L ${X(0.061)} ${Y(-0.34)}" stroke="${D.dim}" stroke-width="1.2" stroke-dasharray="6 4"/>`);
  g.push(dimV(Y(zD), Y(zT), X(0.46), DALLE.toFixed(2), { size: 9.5 }));
  g.push(dimV(Y(0), Y(0.30), X(-0.68), '0.30', { size: 9 }));
  g.push(dimV(Y(0.30), Y(zD), X(-0.68), (zD - 0.30).toFixed(2), { size: 9 }));
  g.push(dimH(X(IN + 0.25), X(0.02), Y(-0.30), '0.30', { size: 9 }));
  [[1, X(-0.26), Y(0.15), -40, 44], [2, X(-0.26), Y(zD + 0.10), -46, -12], [3, X(-0.075), Y(0.60), 70, -20],
   [4, X(0.029), Y(zD + 0.04), 66, -22], [5, X(0.029), Y(0.95), 66, 24], [6, X(0.032), Y(-0.18), 70, 26]]
    .forEach(([n, x, y, dx, dy]) => g.push(rep(n, x, y, dx, dy)));
  g.push(detailTitle(1230, 42, 'D3', 'JONCTION PLANCHER · LINTEAU · ALLÈGE', 'ÉCHELLE 1:10'));
  g.push(nomenclature(1230, 812, [
    ['1', 'Linteau BA 20 × 30 au-dessus de la porte-balcon'],
    ['2', 'Plancher dalle pleine BA 20 cm — hauteur sous plafond 3,06 m,'],
    ['', 'hauteur d’étage 3,26 m'],
    ['3', 'Double cloison brique creuse 15 + lame d’air 5 + brique 10'],
    ['4', 'Joint creux 15 × 15 mm au droit de chaque plancher : il rattrape'],
    ['', 'le retrait du monocouche et dessine la ligne d’étage'],
    ['5', 'Monocouche blanc 15 mm, grain fin gratté, sur gobetis'],
    ['6', 'Dormant haut alu TPR 65, calfeutrement mousse + mastic'],
  ], { size: 8.6 }));
}

// ===========================================================================
// D4 — ACROTERE ET COUVERTINE
// ===========================================================================
{
  const ox = 1995, oy = BASE - 0.30 * S, m = mk(ox, oy);
  const { X, Y, R, L, P } = m;
  const IN = -0.55;
  g.push(R(IN, 0.02, -0.20, 0.0, 'url(#pBeton)', STROKE));
  g.push(P([[IN, 0.0], [-0.17, 0.0], [-0.17, 0.075], [IN, 0.045]], 'url(#pIsol)', FIN));
  g.push(P([[IN, 0.045], [-0.17, 0.075], [-0.17, 0.10], [IN, 0.07]], 'url(#pChape)', FIN));
  g.push(`<path d="M ${X(IN)} ${Y(0.07)} L ${X(-0.17)} ${Y(0.10)} L ${X(-0.17)} ${Y(ACROTERE - 0.28)}" fill="none" stroke="${D.etan}" stroke-width="2.6"/>`);
  for (let y = IN + 0.05; y < -0.19; y += 0.05)
    g.push(`<circle cx="${X(y)}" cy="${Y(0.088 + (y - IN) * 0.078)}" r="2.6" fill="#B7AFA1"/>`);
  g.push(R(-0.17, 0.02, 0.0, ACROTERE, 'url(#pBeton)', STROKE));
  g.push(R(0.02, 0.037, -0.20, ACROTERE, 'url(#pMono)', STROKE));
  g.push(R(-0.176, -0.17, 0.10, ACROTERE - 0.28, D.paper, FIN));
  g.push(R(-0.185, 0.037, ACROTERE - 0.305, ACROTERE - 0.275, D.alu, ''));
  g.push(P([[-0.215, ACROTERE + 0.055], [0.075, ACROTERE + 0.09], [0.075, ACROTERE + 0.055],
            [-0.215, ACROTERE + 0.02]], 'url(#gAlu)', STROKE));
  g.push(R(-0.222, -0.196, ACROTERE - 0.05, ACROTERE + 0.056, 'url(#gAlu)', STROKE));
  g.push(R(0.049, 0.075, ACROTERE - 0.05, ACROTERE + 0.092, 'url(#gAlu)', STROKE));
  g.push(P([[-0.222, ACROTERE - 0.05], [-0.196, ACROTERE - 0.05], [-0.196, ACROTERE - 0.075], [-0.209, ACROTERE - 0.082], [-0.222, ACROTERE - 0.075]], D.aluD, ''));
  g.push(P([[0.049, ACROTERE - 0.05], [0.075, ACROTERE - 0.05], [0.075, ACROTERE - 0.075], [0.062, ACROTERE - 0.082], [0.049, ACROTERE - 0.075]], D.aluD, ''));
  for (const y of [-0.11, 0.0]) g.push(R(y - 0.011, y + 0.011, ACROTERE, ACROTERE + 0.045, D.inox, FIN));
  g.push(rupture(X(IN), Y(-0.22), Y(0.08)));
  g.push(dimV(Y(0), Y(ACROTERE), X(0.34), ACROTERE.toFixed(2), { size: 9.5 }));
  g.push(dimV(Y(0.10), Y(ACROTERE - 0.28), X(-0.34), '0.72', { size: 9 }));
  g.push(dimH(X(-0.17), X(0.02), Y(-0.30), '0.17', { size: 9 }));
  [[1, X(-0.36), Y(0.02), -20, 52], [2, X(-0.32), Y(0.10), -46, -16], [3, X(-0.075), Y(0.55), 62, -18],
   [4, X(-0.07), Y(ACROTERE + 0.062), 62, -26], [5, X(0.062), Y(ACROTERE - 0.078), 66, 24],
   [6, X(-0.09), Y(ACROTERE - 0.29), -64, 26]]
    .forEach(([n, x, y, dx, dy]) => g.push(rep(n, x, y, dx, dy)));
  g.push(detailTitle(1790, 42, 'D4', 'ACROTÈRE ET COUVERTINE', 'ÉCHELLE 1:10'));
  g.push(nomenclature(1790, 812, [
    ['1', 'Toiture inaccessible : dalle BA 20, isolant en pente 1,5 %'],
    ['2', 'Étanchéité bicouche + protection gravillons roulés 4 cm'],
    ['3', 'Acrotère BA 17 cm, hauteur 1,00 m au-dessus du niveau fini'],
    ['4', 'Couvertine aluminium RAL 7024, pente vers l’intérieur,'],
    ['', 'éclisses et pattes de fixation tous les 1,20 m'],
    ['5', 'Goutte d’eau des deux côtés — elle décolle l’eau du monocouche :'],
    ['', 'c’est elle qui empêche les coulures noires sous le couronnement'],
    ['6', 'Relevé d’étanchéité 30 cm + bande solin en tête'],
  ], { size: 8.6 }));
}

g.unshift(PATTERNS(S));
const body = `<div style="width: ${W}px; background: #FFFFFF">
${header({ w: W, kicker: 'Carnet de détails · coupes verticales',
  title: 'Comment la façade est faite, de bas en haut',
  sub: 'Quatre coupes verticales au 1:10 : la rive du balcon avec son bandeau cintré et sa gorge LED, le seuil de la porte-balcon, la jonction du plancher avec le joint creux, et le couronnement. Cotes en mètres.',
  right: 'A2 PAYSAGE · ÉCHELLE 1:10<br>COTES EN MÈTRES<br>NIVEAU COURANT R+3 À R+8' })}
<svg viewBox="0 0 ${W} ${SVGH}" width="${W}" height="${SVGH}" xmlns="http://www.w3.org/2000/svg" style="display: block">${g.join('\n')}</svg>
</div>`;
writeFileSync('Details-Verticaux.dc.html', page({ body, props: JSON.stringify({ $preview: { width: W, height: SVGH + 220 } }) }));
console.log('Details-Verticaux.dc.html ok');
