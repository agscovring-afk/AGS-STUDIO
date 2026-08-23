import { writeFileSync } from 'node:fs';
import { page, header } from './page.mjs';
import { developpe } from './geo.mjs';

const W = 940;
const dev = developpe();

const MAT = [
  { n: 'Monocouche gratté', t: 'Ivoire sablé', sw: ['#E8E0D2', '#DCD1BC'], ref: 'Enduit monocouche épaisseur 15 mm, finition grattée fin, sur maçonnerie et voiles béton',
    pts: ['Teinte ivoire sablé sur l’ensemble des voiles, allèges et acrotères',
          'Joint creux horizontal 15 × 15 mm au droit de chaque plancher',
          'Poteaux de 55 cm laissés en léger relief — nu extérieur +2 cm sur l’allège'] },
  { n: 'Aquapanel cintré', t: 'Blanc pur', sw: ['#FBF9F5', '#E3DCD0'], ref: 'Plaque ciment 12,5 mm cintrée sur ossature, enduit + peinture façade blanc mat',
    pts: [`Bandeaux de rive ondulés, développé ${dev.toFixed(2)} ml par balcon`,
          'Balcons R+3 à R+6 × 2 blocs = 8 rives → ' + (dev * 8).toFixed(0) + ' ml',
          'Acrotère de terrasse R+2, onde continue sur 17,50 m → 20 ml',
          'Soit ≈ 99 ml au total ; retombée 45 cm → ≈ ' + (99 * 0.45).toFixed(0) + ' m² développés, sous-face comprise',
          'Rayon de cintrage mini ≈ 0,60 m — compatible plaque cintrée à sec'] },
  { n: 'Garde-corps verre + inox', t: 'Verre clair / inox brossé', sw: ['#C3D0D2', '#B7BEC2'], ref: 'Verre feuilleté 8.8.4 clair, montants et main courante inox 304 brossé Ø 42 mm',
    pts: ['Hauteur 1,10 m au-dessus du sol fini',
          'Le garde-corps suit l’onde de rive, à 5 cm en retrait du nu',
          'Montants tous les 1,55 m, fixation sur platine dans la dalle',
          'Linéaire ≈ 99 ml, sur le même tracé que les bandeaux Aquapanel'] },
  { n: 'Brise-vue aluminium', t: 'Bronze anodisé', sw: ['#8A6E4C', '#5A4832'], ref: 'Lames aluminium anodisé bronze, ossature alu, fixation sur poteaux béton',
    pts: ['Vide central 1,80 m — lames verticales, du R+2 au niveau toiture (≈ 22 m²)',
          'Séparations d’intimité en bout de balcon, 1,30 m de haut',
          'Ventilation du parking R+1 — lames horizontales pare-vue (≈ 34 m²)'] },
  { n: 'Menuiseries aluminium', t: 'Bronze anodisé', sw: ['#8A6E4C', '#2C3234'], ref: 'Portes-balcon 2 vantaux coulissants à rupture de pont thermique, double vitrage 4/16/4',
    pts: ['1,80 m de large × 2,40 m de haut',
          '2 par balcon × 2 blocs × 5 niveaux = 20 unités en façade principale',
          '+ 2 par niveau côté vide central = 10 unités',
          'Couvertine alu bronze en tête d’acrotère et de poteau'] },
];

const NOTES = [
  ['Découpage retenu', '0,55 + 6,75 + 0,55 + 1,80 + 0,55 + 6,75 + 0,55 = 17,50 m. L’ouverture libre est prise à 6,75 m pour boucler exactement les 17,50 m relevés — soit 7,30 m d’entraxe de poteaux. À confirmer selon ce que couvrent vos ~7 m.'],
  ['Nombre de niveaux', 'RDC + R+1 en parking, R+2 à R+6 en logements. Cela donne 5 lignes ondulées en façade — l’acrotère de la terrasse R+2, puis les balcons du R+3 au R+6 — ce qui correspond aux photos. Hauteurs prises à 3,40 m au RDC et 3,06 m aux étages : à caler sur vos hauteurs réelles.'],
  ['Onde de rive', 'Deux ondes par balcon, profondeur 1,30 m au creux et 3,00 m à la crête. C’est cette amplitude qui donne les ~10 ml de développé annoncés. Si la console de 3,00 m est trop profonde, on rapproche les ondes plutôt que de les aplatir.'],
  ['Terrasse R+2', 'Elle occupe toute la toiture du parking, soit 4,00 m de profondeur sur 17,50 m. Son acrotère reprend la même onde que les balcons pour que la lecture soit continue.'],
];

const card = (m, wide) => `<div style="border: 1px solid #D3C9B7; background: #F7F4ED; padding: 20px 22px 22px${wide ? '; grid-column: span 2' : ''}">
  <div style="display: flex; gap: 14px; align-items: center">
    <div style="display: flex; gap: 0; flex: 0 0 auto">
      ${m.sw.map((c, i) => `<div style="width: 34px; height: 34px; background: ${c}; border: 1px solid rgba(35,33,30,.18); ${i ? 'margin-left: -1px' : ''}"></div>`).join('')}
    </div>
    <div>
      <div style="font-family: 'Space Grotesk', 'Helvetica Neue', Arial, sans-serif; font-size: 16px; font-weight: 600; letter-spacing: -0.012em">${m.n}</div>
      <div style="font-size: 11px; font-weight: 600; letter-spacing: .14em; color: #8C8478; text-transform: uppercase; margin-top: 3px">${m.t}</div>
    </div>
  </div>
  <div style="font-size: 12px; line-height: 1.55; color: #4C463C; margin-top: 14px; padding-top: 13px; border-top: 1px solid #E0D8C8; text-wrap: pretty">${m.ref}</div>
  <ul style="margin: 12px 0 0; padding-left: 16px; font-size: 12px; line-height: 1.6; color: #6E6659${wide ? '; columns: 2; column-gap: 34px' : ''}">
    ${m.pts.map((p) => `<li style="margin-top: 4px; text-wrap: pretty">${p}</li>`).join('')}
  </ul>
</div>`;

const body = `<div style="width: ${W}px; background: #F1EDE5">
${header({ w: W, kicker: 'Matériaux, finitions &amp; hypothèses', title: 'Palette de façade',
  sub: 'Les quatre matériaux demandés, leur mise en œuvre et les quantités qui en découlent — puis les hypothèses que j’ai prises et qu’il faut confirmer.',
  right: 'VARIANTE A<br>« IVOIRE &amp; BRONZE »<br>QUANTITÉS ESTIMATIVES' })}
<div style="padding: 28px 44px 8px; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px">
  ${MAT.map((m, i) => card(m, i === MAT.length - 1)).join('\n  ')}
</div>
<div style="padding: 26px 44px 44px">
  <div class="rule" style="margin-bottom: 22px"></div>
  <div class="eyebrow" style="margin-bottom: 16px">À confirmer avant de figer le dessin</div>
  <div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px 34px">
    ${NOTES.map(([t, d]) => `<div>
      <div style="font-family: 'Space Grotesk', 'Helvetica Neue', Arial, sans-serif; font-size: 13.5px; font-weight: 600">${t}</div>
      <div style="font-size: 12px; line-height: 1.6; color: #6E6659; margin-top: 5px; text-wrap: pretty">${d}</div>
    </div>`).join('\n    ')}
  </div>
</div>
</div>`;

writeFileSync('Materiaux.dc.html', page({ body, props: JSON.stringify({ $preview: { width: W, height: 1320 } }) }));
console.log('Materiaux.dc.html ok');
