import { writeFileSync } from 'node:fs';
import { elevation, PALETTE_A } from './elevation.mjs';
import { page, header } from './page.mjs';
import { ground, txt } from './svgkit.mjs';

const W = 820, SVGH = 806, S = 27, X0 = 174, Y0 = 712;

const V = {
  B: {
    file: 'VarianteB.dc.html', label: 'Variante B', name: 'Graphite &amp; Verre',
    kicker: 'Direction écartée · B — pour mémoire',
    sub: 'Corps de bâtiment en monocouche blanc cassé, ossature verticale et vide central en graphite. Le contraste fait lire la trame des poteaux et transforme le vide en faille sombre — plus contrasté que la variante A, qui reste dans un seul registre.',
    tradeoff: 'Ce qu’elle apportait : une trame de poteaux très lisible de loin, et une teinte sombre où la salissure se voit moins. Pourquoi elle n’est pas retenue : le graphite chauffe au soleil sur une façade déjà exposée, et il exige une pose de brise-vue parfaitement régulière — le moindre défaut d’alignement se lit sur toute la hauteur.',
    P: { ...PALETTE_A, paper: '#EEECE8', wall: '#F5F3EE', wallDeep: '#DBD7CE', pier: '#33383A', plinth: '#262B2D',
      aqua: '#FFFFFF', aquaSh: '#E7E7E3', accent: '#5A6265', accentDark: '#2C3134', dark: '#1C2022',
      glass: '#9FB2B8', glassHi: '#DAE4E6', inox: '#C9CED1', ink: '#1C2022', dim: '#8A8880' },
    opts: {},
  },
  C: {
    file: 'VarianteC.dc.html', label: 'Variante C', name: 'Rubans continus',
    kicker: 'Direction écartée · C — pour mémoire',
    sub: 'Le fond de façade passe en teinte sombre et les bandeaux Aquapanel deviennent des rubans clairs qui traversent toute la largeur, vide central compris. L’onde devient le sujet ; poteaux et menuiseries disparaissent dans l’ombre.',
    tradeoff: 'Ce qu’elle apportait : c’est la variante qui met le plus en valeur les ~10 ml de courbe déjà coulés — l’onde devient le seul sujet de la façade. Pourquoi elle n’est pas retenue : le ruban continu impose de franchir le vide central, soit un ouvrage en porte-à-faux de 1,80 m à créer de toutes pièces, sur un fond sombre plus exigeant en entretien.',
    P: { ...PALETTE_A, paper: '#EFEBE3', wall: '#4A443B', wallDeep: '#3A352E', pier: '#544D42', plinth: '#33302A',
      aqua: '#F8F3E7', aquaSh: '#DCD3C0', accent: '#C08A3E', accentDark: '#87611F', dark: '#221F1A',
      glass: '#8FA3A8', glassHi: '#CFDBDC', inox: '#B9BFC2', ink: '#221F1A', dim: '#8C8478' },
    opts: { ribbon: true, fascia: 0.62 },
  },
};

for (const key of ['B', 'C']) {
  const v = V[key];
  const E = elevation(v.P, { scale: S, x0: X0, y0: Y0, ...v.opts });
  const svg = `<svg viewBox="0 0 ${W} ${SVGH}" width="${W}" height="${SVGH}" xmlns="http://www.w3.org/2000/svg" style="display: block">
  ${E.svg}
  ${ground(E.px(-1.4), E.px(18.9), E.py(0))}
  ${txt(E.px(8.75), E.py(0) + 44, '17.50 m · MEMES COTES, MEME GEOMETRIE QUE LA VARIANTE A', { size: 9, fill: v.P.dim, ls: '0.16em', weight: 600 })}
  </svg>`;
  const body = `<div style="width: ${W}px; background: #FFFFFF">
${header({ w: W, kicker: v.kicker, title: v.name, sub: v.sub, right: `${v.label.toUpperCase()} — NON RETENUE<br>ÉLÉVATION NON COTÉE<br>ÉCHELLE 1:150` })}
${svg}
<div style="padding: 0 44px 40px">
  <div class="rule" style="margin-bottom: 18px"></div>
  <div style="font-size: 12.5px; line-height: 1.62; color: #4C463C; text-wrap: pretty">${v.tradeoff}</div>
</div>
</div>`;
  writeFileSync(v.file, page({ body, props: JSON.stringify({ $preview: { width: W, height: SVGH + 290 } }) }));
  console.log(v.file, 'ok');
}
