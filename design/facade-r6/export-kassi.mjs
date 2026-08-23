// Exporte chaque planche en PDF a l'echelle vraie (1 px CSS = 1/96 pouce) et en
// PNG 2x, dans un dossier KASSI pret a etre depose sur le bureau.
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
const CH = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const TMP = process.env.SP;
const mm = (px) => +(px / 96 * 25.4).toFixed(2);
const canvas = JSON.parse(readFileSync('canvas.json', 'utf8'));
const ORDER = [
  ['01', 'Synthese', 'Donnees du projet a valider'],
  ['02', 'Main', 'Facade principale 1-100'],
  ['03', 'Plan-Balcon', 'Plan niveau courant - onde de rive 1-50'],
  ['04', 'Plan-Terrasse', 'Plan terrasses R+2 1-50'],
  ['05', 'Plan-RDC', 'Plan RDC parking 1-50'],
  ['06', 'Coupe', 'Coupe A-A 1-100'],
  ['07', 'Detail-Balcon', 'Detail balcon - les quatre vues 1-25'],
  ['08', 'Details-Verticaux', 'Details coupes verticales 1-10'],
  ['09', 'Details-Horizontaux', 'Details coupes horizontales 1-10'],
  ['10', 'Detail-Garde-Corps', 'Detail garde-corps 1-20 et 1-5'],
  ['11', 'Materiaux', 'Materiaux et finitions'],
  ['12', 'Vue', 'Ambiance - rives ondulees jour'],
  ['13', 'Vue-Nuit', 'Ambiance - la courbe allumee nuit'],
  ['14', 'Vue-Haut', 'Ambiance - vue plongeante terrasse et balcon'],
  ['15', 'Gabarit-Onde', 'Gabarit onde de rive'],
  ['16', 'Gabarit-Terrasse', 'Gabarit terrasses'],
];
mkdirSync('KASSI/PDF', { recursive: true });
mkdirSync('KASSI/PNG', { recursive: true });

const strip = (src) => {
  const s = readFileSync(src, 'utf8');
  const body = s.slice(s.indexOf('<x-dc>') + 6, s.indexOf('</x-dc>'));
  const st = body.match(/<style>([\s\S]*?)<\/style>/);
  const content = body.replace(/<helmet>[\s\S]*?<\/helmet>/, '');
  return { css: st ? st[1] : '', content };
};

const lignes = [];
for (const [no, name, titre] of ORDER) {
  const ab = canvas.artboards.find((a) => a.file === name + '.dc.html');
  if (!ab) { console.error('manque', name); continue; }
  const { css, content } = strip(name + '.dc.html');
  const W = ab.w, H = ab.h;
  const html = `<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Archivo:wght@400;500;600;700&display=swap">
<style>@page{size:${mm(W)}mm ${mm(H)}mm;margin:0}
html,body{margin:0;padding:0;background:#fff;-webkit-print-color-adjust:exact;print-color-adjust:exact}
#sheet{width:${W}px;height:${H}px;overflow:hidden;background:#fff}
${css}</style></head><body><div id="sheet">${content}</div></body></html>`;
  const f = `${TMP}/k_${name}.html`;
  writeFileSync(f, html);
  const pdf = `KASSI/PDF/${no} - ${titre}.pdf`;
  execFileSync(CH, ['--headless', '--disable-gpu', '--no-sandbox', '--no-pdf-header-footer',
    '--virtual-time-budget=6000', `--print-to-pdf=${pdf}`, 'file://' + f], { stdio: 'ignore' });
  const png = `KASSI/PNG/${no} - ${titre}.png`;
  execFileSync(CH, ['--headless', '--disable-gpu', '--no-sandbox', '--hide-scrollbars',
    '--force-device-scale-factor=2', `--window-size=${W},${H}`, '--virtual-time-budget=5000',
    '--default-background-color=FFFFFFFF', `--screenshot=${png}`, 'file://' + f], { stdio: 'ignore' });
  lignes.push(`${no}  ${titre.padEnd(48)} ${mm(W)} x ${mm(H)} mm`);
  console.log(no, name, '->', mm(W) + 'x' + mm(H), 'mm');
}
writeFileSync('KASSI/LISEZ-MOI.txt',
`IMMEUBLE R+8 — FACADE PRINCIPALE
Dossier KASSI — ${new Date().toISOString().slice(0, 10)}

PDF/   les planches a l'echelle vraie. Imprimer a 100 %, sans "ajuster a la page",
       sinon les cotes ne sont plus justes. Le format de chaque feuille est
       indique ci-dessous.
PNG/   les memes planches en image 2x, pour lire a l'ecran ou envoyer.

${lignes.join('\n')}

GEOMETRIE ARRETEE
  Largeur totale de facade      17.50 m       Poteaux 0.55 m
  Baie de balcon                6.75 m libre  Vide central 1.80 m
  Hauteur d'etage               3.26 m        dont dalle 0.20 m
  RDC                           2.60 m sous plafond
  Niveaux                       RDC et R+1 parking, R+2 terrasses,
                                R+3 a R+8 balcons, acrotere +29.88

  ONDE DE RIVE (bloc droit ; bloc gauche en miroir)
  Elle part du poteau perpendiculairement au nu.
  Grand lobe 1.80 m a 1.96 m du poteau
  Creux median 0.79 m a 3.92 m
  Petit lobe 1.10 m a 5.64 m
  Developpe 9.63 ml par balcon, 12 balcons

  GARDE-CORPS
  Alternance 40 cm de verre feuillete 8.8.4 et 40 cm de barreaudage inox O16,
  24 panneaux par balcon, main courante inox O42 a 1.10 m.
  Voir planche 10 : la fleche d'un panneau plat atteint 23 mm dans les deux
  zones les plus serrees.

  VIDE CENTRAL
  Fente de 1.80 m creusee de 1.50 m. Au fond, deux balcons de 0.70 x 0.80 m,
  un par logement, porte-fenetre de 0.70 m depuis le logement.
  Brise-vue aluminium RAL 7024 de 40 cm sur l'axe, entre les deux.
  Garde-corps verre a 0.70 m en arriere du nu.

  MATERIAUX
  Monocouche blanc, grain fin gratte, joint creux 15x15 a chaque plancher
  Bandeaux de rive Aquapanel Outdoor 12.5 mm sur ossature cintree, retombee 0.45
  Gorge LED 50x50 en sous-face de chaque bandeau, 3000 K IP65
  Menuiseries aluminium TPR serie 65 a rupture de pont thermique, RAL 7024
  Brise-vue et couvertines aluminium RAL 7024
  Garde-corps verre feuillete teinte noir et inox 316 brosse

RESTE A CONFIRMER
  Vos 7 m de baie : entraxe des poteaux (retenu, donne 6.75 libre et 17.50
  au total) ou largeur libre (la facade passerait a 18.00) ?
`);
console.log('LISEZ-MOI ok');
