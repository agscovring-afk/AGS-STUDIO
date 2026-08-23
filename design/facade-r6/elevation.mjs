import { XS, LV, BALCONS, ETAGES, NIVEAUX_LOGEMENT, HET, HSP, FASCIA, GC, PBH, RETRAIT, DMAX,
         AXE, BV_EP, JOUE, PBN, doors, gcSegments, depthAt, BLOCS } from './geo.mjs';
import { txt, dimH, dimV, levelMark, callout, ground } from './svgkit.mjs';

export const PALETTE_A = {
  name: 'Blanc & Graphite', paper: '#FFFFFF',
  wall: '#F4F2ED', wallDeep: '#E0DDD5',       // monocouche blanc, fonds de baie en retrait
  pier: '#FCFBF8', plinth: '#D8D4CA',
  aqua: '#FFFFFF', aquaSh: '#E9E6DE',
  accent: '#474B4E', accentDark: '#31353A',   // aluminium RAL 7024
  dark: '#22262A', glass: '#1E2224', glassHi: '#5A6468', inox: '#C6CCD0',
  led: '#F0D9A6',
  ink: '#23211E', dim: '#8C8478',
};

export function elevation(P, o = {}) {
  const S = o.scale ?? 42, X0 = o.x0 ?? 215, Y0 = o.y0 ?? 1092;
  const px = (m) => +(X0 + m * S).toFixed(2);
  const py = (h) => +(Y0 - h * S).toFixed(2);
  const wm = (m) => +(m * S).toFixed(2);
  const R = (x1, x2, h1, h2, fill, extra = '') =>
    `<rect x="${px(x1)}" y="${py(h2)}" width="${wm(x2 - x1)}" height="${wm(h2 - h1)}" fill="${fill}" ${extra}/>`;

  const FA = o.fascia ?? FASCIA;
  const piers = [XS.c1, XS.c2, XS.c3, XS.c4];
  const bays = [XS.bayA, XS.bayB];
  // les deux blocs de part et d'autre du vide (ou un ruban continu en variante C)
  const blocks = o.ribbon ? [[0, 17.50]] : [[0, XS.c2[1]], [XS.c3[0], 17.50]];
  const doorLevels = NIVEAUX_LOGEMENT;
  const g = [];

  // ---- defs -------------------------------------------------------------
  g.push(`<defs>
    <linearGradient id="gl" x1="0" y1="0" x2="0.32" y2="1">
      <stop offset="0" stop-color="${P.glassHi}" stop-opacity="0.92"/>
      <stop offset="0.30" stop-color="${P.glass}" stop-opacity="0.90"/>
      <stop offset="1" stop-color="${P.glass}" stop-opacity="0.96"/>
    </linearGradient>
    <linearGradient id="aq" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="${P.aqua}"/>
      <stop offset="0.62" stop-color="${P.aqua}"/>
      <stop offset="1" stop-color="${P.aquaSh}"/>
    </linearGradient>
    <linearGradient id="pane" x1="0" y1="0" x2="0.4" y2="1">
      <stop offset="0" stop-color="#4E5A5C"/><stop offset="0.5" stop-color="#33393B"/><stop offset="1" stop-color="#242A2C"/>
    </linearGradient>
    <linearGradient id="shdO" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0" stop-color="${P.dark}" stop-opacity="0.34"/>
      <stop offset="1" stop-color="${P.dark}" stop-opacity="0.06"/>
    </linearGradient>
    <linearGradient id="shd" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="${P.dark}" stop-opacity="0.20"/>
      <stop offset="1" stop-color="${P.dark}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="${P.paper}" stop-opacity="0"/>
      <stop offset="1" stop-color="${P.dim}" stop-opacity="0.10"/>
    </linearGradient>
  </defs>`);

  // ---- fond ------------------------------------------------------------
  g.push(`<rect x="${px(-1.2)}" y="${py(LV.acr) - 46}" width="${wm(19.9)}" height="${py(0) - py(LV.acr) + 46}" fill="url(#sky)"/>`);

  // ---- volume tour (nu de facade, en retrait) ---------------------------
  g.push(R(0, 17.50, 0, LV.acr, P.wall));
  // joints creux horizontaux au droit de chaque plancher
  for (const h of [...BALCONS, LV.toit])
    g.push(`<line x1="${px(0)}" y1="${py(h)}" x2="${px(17.5)}" y2="${py(h)}" stroke="${P.dim}" stroke-width="0.8" opacity="0.35"/>`);

  // ---- baies en retrait + menuiseries -----------------------------------
  for (const h of doorLevels) {
    for (const bay of bays) {
      g.push(R(bay[0], bay[1], h, h + HSP, P.wallDeep));
      g.push(R(bay[0], bay[1], h + HSP - 0.95, h + HSP, 'url(#shd)'));
      for (const [a, b] of doors(bay)) {
        g.push(R(a, b, h, h + PBH, 'url(#pane)'));
        g.push(R(a, b, h, h + PBH, 'none', `stroke="${P.accent}" stroke-width="2"`));
        g.push(`<line x1="${px((a + b) / 2)}" y1="${py(h)}" x2="${px((a + b) / 2)}" y2="${py(h + PBH)}" stroke="${P.accent}" stroke-width="1.6"/>`);
        g.push(`<line x1="${px(a + 0.06)}" y1="${py(h + PBH - 0.12)}" x2="${px(b - 0.06)}" y2="${py(h + PBH - 0.12)}" stroke="${P.glassHi}" stroke-width="1" opacity="0.35"/>`);
        // poignees
        g.push(`<rect x="${px((a + b) / 2 - 0.10)}" y="${py(h + 1.15)}" width="${wm(0.06)}" height="${wm(0.34)}" fill="${P.inox}"/>`);
        g.push(`<rect x="${px((a + b) / 2 + 0.04)}" y="${py(h + 1.15)}" width="${wm(0.06)}" height="${wm(0.34)}" fill="${P.inox}"/>`);
      }
      // profil LED vertical dans le trumeau central, entre les deux portes
      {
        const d = doors(bay), xm = (d[0][1] + d[1][0]) / 2;
        g.push(R(xm - 0.04, xm + 0.04, h + 0.30, h + 2.20, P.dark));
        g.push(R(xm - 0.025, xm + 0.025, h + 0.32, h + 2.18, P.led));
      }
      // brise-vue vertical d'intimite en bout de balcon (cote vide central)
      const bx = bay === XS.bayA ? bay[1] - 0.14 : bay[0];
      g.push(R(bx, bx + 0.14, h, h + HSP, P.accentDark));
      for (let k = 0.06; k < HET - FASCIA; k += 0.14)
        g.push(`<line x1="${px(bx)}" y1="${py(h + k)}" x2="${px(bx + 0.14)}" y2="${py(h + k)}" stroke="${P.accent}" stroke-width="1" opacity="0.55"/>`);
    }
  }

  // ---- poteaux / raidisseurs 55 cm --------------------------------------
  for (const [a, b] of piers) {
    g.push(R(a, b, LV.r2, LV.acr + 0.50, P.pier));
    g.push(R(a, a + 0.05, LV.r2, LV.acr + 0.50, '#FFFFFF', 'opacity="0.55"'));
    g.push(R(b - 0.09, b, LV.r2, LV.acr + 0.50, P.dark, 'opacity="0.22"'));
    g.push(R(b, b + 0.09, LV.r2, LV.acr + 0.40, P.dark, 'opacity="0.10"'));
    g.push(R(a, b, LV.acr + 0.40, LV.acr + 0.50, P.accent));      // couvertine alu
  }

  // ---- balcons ondules : bandeau Aquapanel + garde-corps -----------------
  // Garde-corps mixte au pas de 40 cm : un panneau de verre feuillete plat de
  // 40 cm, puis 40 cm de barreaudage inox, et ainsi de suite sur tout le
  // developpe. A 40 cm la fleche d'un plat reste invisible sur n'importe quel
  // rayon de la rive : c'est ce qui rend le verre posable sur la courbe.
  // garde-corps droit : terrasses du R+2, aucune courbure donc verre continu
  const gcDroit = (x1, x2, h) => {
    const s = [];
    s.push(`<rect x="${px(x1)}" y="${py(h) + 1}" width="${wm(x2 - x1)}" height="${wm(0.16)}" fill="${P.dark}" opacity="0.16"/>`);
    s.push(R(x1 + 0.04, x2 - 0.04, h + 0.17, h + GC - 0.10, 'url(#gl)'));
    s.push(R(x1 + 0.04, x2 - 0.04, h + 0.17, h + GC - 0.10, 'none', `stroke="${P.inox}" stroke-width="0.7" opacity="0.85"`));
    s.push(R(x1, x2, h + 0.08, h + 0.17, P.inox));
    const n = Math.max(2, Math.round((x2 - x1) / 1.35));
    for (let k = 0; k <= n; k++) {
      const x = x1 + (x2 - x1) * k / n;
      s.push(`<line x1="${px(x)}" y1="${py(h + 0.08)}" x2="${px(x)}" y2="${py(h + GC)}" stroke="${P.inox}" stroke-width="2.4"/>`);
    }
    s.push(R(x1, x2, h + GC - 0.09, h + GC, P.inox));
    s.push(R(x1, x2, h + GC - 0.09, h + GC - 0.062, '#FFFFFF', 'opacity="0.72"'));
    return s.join('');
  };

  const gcParts = (x1, x2, h, b) => {
    const s = [];
    s.push(`<rect x="${px(x1)}" y="${py(h) + 1}" width="${wm(x2 - x1)}" height="${wm(0.16)}" fill="${P.dark}" opacity="0.16"/>`);
    for (const seg of gcSegments(b)) {
      if (seg.kind === 'verre') {
        s.push(R(seg.x1 + 0.03, seg.x2 - 0.03, h + 0.17, h + GC - 0.10, 'url(#gl)'));
        s.push(R(seg.x1 + 0.03, seg.x2 - 0.03, h + 0.17, h + GC - 0.10, 'none', `stroke="${P.inox}" stroke-width="0.7" opacity="0.85"`));
        s.push(R(seg.x1, seg.x2, h + 0.08, h + 0.17, P.inox));                     // profil U inox en pied
      } else {
        s.push(R(seg.x1, seg.x2, h + 0.08, h + 0.15, P.inox));                     // lisse basse
        for (let x = seg.x1 + 0.055; x < seg.x2 - 0.03; x += 0.11)
          s.push(`<line x1="${px(x)}" y1="${py(h + 0.10)}" x2="${px(x)}" y2="${py(h + GC - 0.09)}" stroke="${P.inox}" stroke-width="1.5"/>`);
      }
      s.push(`<line x1="${px(seg.x2)}" y1="${py(h + 0.08)}" x2="${px(seg.x2)}" y2="${py(h + GC)}" stroke="${P.inox}" stroke-width="2.4"/>`);
    }
    s.push(`<line x1="${px(x1)}" y1="${py(h + 0.08)}" x2="${px(x1)}" y2="${py(h + GC)}" stroke="${P.inox}" stroke-width="2.4"/>`);
    s.push(R(x1, x2, h + GC - 0.09, h + GC, P.inox));                              // main courante continue
    s.push(R(x1, x2, h + GC - 0.09, h + GC - 0.062, '#FFFFFF', 'opacity="0.72"'));
    return s.join('');
  };

  const SUN = 0.92;                     // longueur d'ombre par metre de porte-a-faux
  const ombreOndee = (bi, h) => {
    const [x1, x2] = BLOCS[bi], N = 140, top = [], bot = [];
    for (let i = 0; i <= N; i++) {
      const m = x1 + (x2 - x1) * i / N, d = depthAt(m, bi);
      top.push(`${i ? 'L' : 'M'} ${px(m)} ${py(h - FA)}`);
      bot.push([px(m), py(h - FA - d * SUN)]);
    }
    const back = bot.slice().reverse().map(([x, y], i) => `${i ? 'L' : 'L'} ${x} ${y}`).join(' ');
    return `<path d="${top.join(' ')} ${back} Z" fill="url(#shdO)"/>`
      + `<path d="${bot.map(([x, y], i) => `${i ? 'L' : 'M'} ${x} ${y}`).join(' ')}" fill="none" stroke="${P.dark}" stroke-width="0.9" opacity="0.5"/>`;
  };
  for (const h of BALCONS) {
    for (let bi = 0; bi < blocks.length; bi++) {
      const [x1, x2] = blocks[bi];
      if (!o.ribbon) g.push(ombreOndee(bi, h));
      g.push(`<rect x="${px(x1)}" y="${py(h - FA) + 1}" width="${wm(x2 - x1)}" height="${wm(0.30)}" fill="${P.dark}" opacity="0.13"/>`);
      g.push(R(x1, x2, h - FA, h, 'url(#aq)'));                   // bandeau courbe Aquapanel
      g.push(R(x1, x2, h - 0.035, h, P.aquaSh, 'opacity="0.7"'));
      g.push(R(x1, x2, h - FA, h - FA + 0.05, P.dark, 'opacity="0.55"'));   // gorge LED en sous-face
      if (!o.ribbon) {
        const N = 140, pts = [];
        for (let i = 0; i <= N; i++) {
          const m = x1 + (x2 - x1) * i / N;
          pts.push(`${i ? 'L' : 'M'} ${px(m)} ${py(h - FA + 0.06 + (depthAt(m, bi) / DMAX) * (FA - 0.14))}`);
        }
        g.push(`<path d="${pts.join(' ')}" fill="none" stroke="${P.dim}" stroke-width="1.1" stroke-dasharray="4 3" opacity="0.85"/>`);
      }
      g.push(gcParts(x1, x2, h, o.ribbon ? 1 : bi));
    }
  }

  // ---- vide central : deux balcons, le brise-vue ENTRE eux ---------------
  // Corrige le 23.08 : le brise-vue n'est pas un panneau tendu en facade, c'est
  // le separateur des deux balcons, sur l'axe. En elevation on n'en voit donc
  // que la tranche de 12 cm ; le reste du vide s'ouvre sur les deux balcons et
  // sur le fond de niche, 1,50 m en arriere du nu.
  {
    const [n1, n2] = XS.vide, hb = [[n1, AXE - BV_EP / 2], [AXE + BV_EP / 2, n2]];
    g.push(R(n1, n2, LV.r2, LV.toit, P.wallDeep));                        // fond de fente, a 1,50 m
    g.push(R(n1, n2, LV.r2, LV.toit, '#000000', 'opacity="0.30"'));       // la fente est dans l'ombre
    g.push(R(n1, n1 + 0.22, LV.r2, LV.toit, '#000000', 'opacity="0.20"')); // flancs des deux blocs
    g.push(R(n2 - 0.22, n2, LV.r2, LV.toit, '#000000', 'opacity="0.14"'));
    for (const h of BALCONS) {
      // portes-fenetres au fond de la niche, une par logement
      for (const [a, b] of hb) {
        const c = (a + b) / 2;
        g.push(R(c - PBN / 2, c + PBN / 2, h + 0.02, h + PBH, P.glass));
        g.push(R(c - PBN / 2, c + PBN / 2, h + 0.02, h + PBH, 'none', `stroke="${P.accentDark}" stroke-width="1"`));
      }
      // dalle de chaque balcon, 0,80 m de profondeur, 0,70 m en arriere du nu
      g.push(R(n1, n2, h - 0.20, h, P.wall, 'opacity="0.88"'));
      g.push(R(n1, n2, h - 0.30, h - 0.20, '#000000', 'opacity="0.22"'));
      // garde-corps au nu, un par balcon
      for (const [a, b] of hb) g.push(gcDroit(a + 0.03, b - 0.03, h));
    }
    // le brise-vue : 40 cm sur l'axe, entre les deux balcons, du R+2 a la toiture
    g.push(R(AXE - BV_EP / 2, AXE + BV_EP / 2, LV.r2, LV.toit, P.accent));
    for (let x = AXE - BV_EP / 2 + 0.05; x < AXE + BV_EP / 2 - 0.02; x += 0.10)
      g.push(`<line x1="${px(x)}" y1="${py(LV.r2)}" x2="${px(x)}" y2="${py(LV.toit)}" stroke="${P.accentDark}" stroke-width="1.6" opacity="0.85"/>`);
    g.push(R(n1, n2, LV.r2, LV.toit, 'none', `stroke="${P.accentDark}" stroke-width="1.2"`));
  }

  // ---- socle parking : RDC + R+1, en avancee de 4.00 m ------------------
  g.push(`<rect x="${px(0)}" y="${py(LV.r2)}" width="${wm(17.5)}" height="${wm(LV.r2)}" fill="${P.wall}"/>`);
  g.push(R(0, 17.50, LV.r2 - 0.06, LV.r2, P.dark, 'opacity="0.10"'));
  g.push(R(0, 17.50, 0, 0.35, P.plinth));
  g.push(`<line x1="${px(0)}" y1="${py(LV.r1)}" x2="${px(17.5)}" y2="${py(LV.r1)}" stroke="${P.dim}" stroke-width="1.1" opacity="0.5"/>`);

  // RDC : deux portes de garage + hall d'entree
  const garages = [[1.40, 6.60], [10.90, 16.10]];
  for (const [a, b] of garages) {
    g.push(R(a, b, 0.20, 2.30, P.accentDark));
    for (let y = 0.20 + 0.38; y < 2.30; y += 0.38)
      g.push(`<line x1="${px(a)}" y1="${py(y)}" x2="${px(b)}" y2="${py(y)}" stroke="${P.accent}" stroke-width="1.2" opacity="0.75"/>`);
    g.push(R(a, b, 0.20, 2.30, 'none', `stroke="${P.accent}" stroke-width="1.8"`));
  }
  g.push(R(XS.vide[0] - 0.25, XS.vide[1] + 0.25, 0, 2.42, P.dark));
  g.push(R(XS.vide[0] - 0.25, XS.vide[1] + 0.25, 0, 2.42, 'none', `stroke="${P.accent}" stroke-width="2.2"`));
  g.push(R(XS.vide[0] - 0.05, XS.vide[1] + 0.05, 0, 2.00, 'url(#pane)'));
  g.push(txt(px((XS.vide[0] + XS.vide[1]) / 2), py(2.18), 'ENTREE', { size: 9, weight: 700, fill: P.accent, ls: '0.22em' }));
  g.push(R(0, 17.50, 2.44, 2.58, P.accent, 'opacity="0.85"'));   // auvent / bandeau alu

  // Parking maconne plein, ventile par une bande de brise-vue alu de 0,80 m
  const VENT = 0.80;
  const bandeVent = (a, b, y0) => {
    g.push(R(a, b, y0, y0 + VENT, P.dark));
    for (let y = y0 + 0.09; y < y0 + VENT; y += 0.14) {
      g.push(`<line x1="${px(a)}" y1="${py(y)}" x2="${px(b)}" y2="${py(y)}" stroke="${P.accent}" stroke-width="2.4" opacity="0.92"/>`);
      g.push(`<line x1="${px(a)}" y1="${py(y - 0.04)}" x2="${px(b)}" y2="${py(y - 0.04)}" stroke="${P.accentDark}" stroke-width="1" opacity="0.85"/>`);
    }
    g.push(R(a, b, y0, y0 + VENT, 'none', `stroke="${P.accentDark}" stroke-width="1.2"`));
  };
  for (const [a, b] of [[0.55, 7.30], [XS.vide[0], XS.vide[1]], [10.20, 16.95]])
    bandeVent(a, b, LV.r1 + 1.55);
  for (const [a, b] of [[0.55, 1.40], [6.60, 7.30], [XS.vide[0], XS.vide[1]], [10.20, 10.90], [16.10, 16.95]])
    bandeVent(a, b, 1.35);
  for (const [a, b] of [XS.c1, XS.c2, XS.c3, XS.c4])
    g.push(R(a, b, 2.58, LV.r2, P.pier, 'opacity="0.75"'));

  // ---- terrasse R+2 sur toiture parking ---------------------------------
  for (const [x1, x2] of BLOCS) {
    g.push(`<rect x="${px(x1)}" y="${py(LV.r2 + FA) + 1}" width="${wm(x2 - x1)}" height="${wm(0.22)}" fill="${P.dark}" opacity="0.12"/>`);
    g.push(R(x1, x2, LV.r2, LV.r2 + FA, 'url(#aq)'));
    g.push(R(x1, x2, LV.r2, LV.r2 + 0.05, P.dark, 'opacity="0.55"'));       // gorge LED
    g.push(gcDroit(x1, x2, LV.r2 + FA));
  }

  // ---- acrotere ---------------------------------------------------------
  g.push(R(0, 17.50, LV.toit, LV.acr, P.wall));
  g.push(`<line x1="${px(0)}" y1="${py(LV.toit)}" x2="${px(17.5)}" y2="${py(LV.toit)}" stroke="${P.dim}" stroke-width="0.9" opacity="0.45"/>`);
  g.push(R(0, 17.50, LV.acr - 0.10, LV.acr, P.accent));
  g.push(R(0, 17.50, 0, LV.acr, 'none', `stroke="${P.ink}" stroke-width="1.4"`));

  return { svg: g.join('\n'), px, py, wm, S, X0, Y0 };
}

// Habillage technique : cotes, niveaux, renvois — planche principale seulement
export function annotations(P, E) {
  const { px, py } = E;
  const a = [];
  a.push(ground(px(-1.6), px(19.1), py(0)));

  // chaine de cotes horizontale
  const yc = py(0) + 40;
  const chain = [[0, 0.55], [0.55, 7.30], [7.30, 7.85], [7.85, 9.65], [9.65, 10.20], [10.20, 16.95], [16.95, 17.50]];
  const lbl = ['0.55', '6.75', '0.55', '1.80', '0.55', '6.75', '0.55'];
  chain.forEach(([x1, x2], i) => a.push(dimH(px(x1), px(x2), yc, lbl[i], { size: 10.5 })));
  a.push(dimH(px(0), px(17.5), yc + 58, '17.50', { size: 14, weight: 700 }));
  a.push(txt(px(8.75), yc + 80, 'LARGEUR TOTALE DE FACADE', { size: 9, fill: P.dim, ls: '0.18em', weight: 600 }));
  a.push(txt(px(3.925), yc + 27, 'BAIE BALCON A', { size: 8.5, fill: P.dim, ls: '0.14em', weight: 600 }));
  a.push(txt(px(13.575), yc + 27, 'BAIE BALCON B', { size: 8.5, fill: P.dim, ls: '0.14em', weight: 600 }));
  a.push(txt(px(8.75), yc + 27, 'VIDE', { size: 8.5, fill: P.dim, ls: '0.14em', weight: 600 }));

  // chaine de cotes verticale
  const xv = px(0) - 92;
  for (let i = 0; i < ETAGES.length - 1; i++) {
    const h1 = ETAGES[i][0], h2 = ETAGES[i + 1][0];
    a.push(dimV(py(h1), py(h2), xv, (h2 - h1).toFixed(2), { size: 10 }));
  }
  a.push(dimV(py(0), py(LV.acr), xv - 44, LV.acr.toFixed(2), { size: 13, weight: 700 }));

  // reperes de niveau
  ETAGES.forEach(([h, alt, t]) => a.push(levelMark(px(17.5) + 34, py(h), alt, t)));

  // renvois materiaux
  const C = [
    [1, px(1.55), py(23.15), px(0.28), py(23.15)],
    [2, px(2.30), py(18.90), px(0.90), py(18.90)],
    [3, px(5.60), py(19.80), px(4.20), py(19.80)],
    [4, px(8.75), py(27.45), px(8.75), py(26.25)],
    [5, px(12.35), py(11.15), px(12.00), py(10.45)],
    [6, px(14.40), py(8.10), px(15.60), py(6.80)],
    [7, px(6.20), py(5.20), px(4.50), py(4.50)],
    [8, px(15.10), py(28.15), px(16.30), py(29.83)],
    [9, px(13.50), py(11.60), px(13.20), py(12.16)],
    [10, px(10.65), py(24.15), px(8.90), py(24.15)],
  ];
  C.forEach(([n, cx, cy, tx, ty]) => a.push(callout(n, cx, cy, tx, ty, { color: P.ink })));

  // notes de tete de planche : ce que l'elevation orthogonale ne peut pas montrer
  const wave = (x, y, w, amp) => {
    let d = `M ${x} ${y}`;
    for (let i = 1; i <= 60; i++) {
      const t = i / 60;
      d += ` L ${(x + t * w).toFixed(2)} ${(y + amp * Math.cos(2 * Math.PI * 2 * t) - amp).toFixed(2)}`;
    }
    return `<path d="${d}" fill="none" stroke="${P.ink}" stroke-width="1.4" stroke-linecap="round"/>`;
  };
  const nx = px(0), ny = 26;
  a.push(wave(nx, ny + 4, 74, 5));
  a.push(txt(nx + 86, ny + 8, 'ONDE DE RIVE : L OMBRE PORTEE ET LE TRAIT POINTILLE DONNENT LA PROFONDEUR — GRAND LOBE 1.80 m, CREUX 0.79 m, PETIT LOBE 1.10 m',
    { size: 9.5, anchor: 'start', fill: P.dim, weight: 600, ls: '0.09em' }));
  a.push(`<path d="M ${nx} ${ny + 32} l 0 12 M ${nx} ${ny + 38} l 74 0 M ${nx + 74} ${ny + 38} l -6 -3.5 M ${nx + 74} ${ny + 38} l -6 3.5" fill="none" stroke="${P.ink}" stroke-width="1.4"/>`);
  a.push(txt(nx + 86, ny + 42, 'SOCLE PARKING RDC + R+1 EN AVANCEE DE 4.00 m SUR LE NU DE FACADE · VOIR PLANCHE « COUPE A-A »',
    { size: 9.5, anchor: 'start', fill: P.dim, weight: 600, ls: '0.09em' }));
  a.push(`<path d="M ${nx} ${ny + 66} l 30 0 M ${nx + 44} ${ny + 66} l 30 0 M ${nx + 30} ${ny + 60} l 0 12 M ${nx + 44} ${ny + 60} l 0 12" fill="none" stroke="${P.ink}" stroke-width="1.4"/>`);
  a.push(txt(nx + 86, ny + 70, 'TERRASSES R+2 : GARDE-CORPS DROIT, SEPAREES PAR LA BANDE CENTRALE DE 1.80 m',
    { size: 9.5, anchor: 'start', fill: P.dim, weight: 600, ls: '0.09em' }));

  return a.join('\n');
}
