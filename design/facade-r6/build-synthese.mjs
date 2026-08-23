import { writeFileSync } from 'node:fs';
import { page, header } from './page.mjs';
import { LV, ETAGES, BALCONS, HSP, HSP_RDC, DALLE, ACROTERE, AVANCEE, RETRAIT,
         DMIN, DCREUX, DMAX, PBW, PBH, MENUISERIE, developpe, XS } from './geo.mjs';

const W = 1587;
const dev = developpe();

const REL = 'relevé';        // donnee fournie par le client
const DED = 'déduit';        // calcule a partir d'une donnee fournie
const SUP = 'à confirmer';   // hypothese de ma part

const BLOCS_DATA = [
  ['Géométrie de façade', [
    ['Largeur totale', '17,50 m', REL],
    ['Poteaux', '0,55 m de large', REL],
    ['Ouverture libre par baie', '6,75 m (entraxe de poteaux 7,30 m)', DED],
    ['Niche centrale', '1,80 m de large', REL],
    ['Retrait de la niche', '1,50 m en arrière du nu, au-dessus des terrasses', REL],
    ['Bande centrale sous les terrasses', 'pleine, elle avance avec le parking', REL],
  ]],
  ['Niveaux', [
    ['RDC', `${HSP_RDC.toFixed(2)} m libre + ${DALLE.toFixed(2)} dalle = ${(HSP_RDC + DALLE).toFixed(2)} m — parking`, REL],
    ['Étages courants', `${HSP.toFixed(2)} m libre + ${DALLE.toFixed(2)} dalle = ${(HSP + DALLE).toFixed(2)} m`, REL],
    ['R+1', 'parking', REL],
    ['R+2', 'terrasses', REL],
    ['R+3 à R+8', `${BALCONS.length} niveaux de balcons ondulés`, REL],
    ['Toiture / acrotère', `+ ${LV.toit.toFixed(2)} m / + ${LV.acr.toFixed(2)} m (acrotère ${ACROTERE.toFixed(2)} m)`, SUP],
    ['Hauteur hors tout', `${LV.acr.toFixed(2)} m — immeuble R+8, 9 niveaux`, DED],
  ]],
  ['Socle parking', [
    ['Avancée sur le nu de façade', `${AVANCEE.toFixed(2)} m, sur RDC et R+1`, REL],
    ['Façade du parking', 'maçonnerie pleine', REL],
    ['Ventilation', 'bande de brise-vue aluminium de 0,80 m de haut', REL],
    ['Accès', '2 portes de garage + hall d’entrée au centre', SUP],
  ]],
  ['Onde de rive des balcons', [
    ['Tracé', 'relevé sur votre croquis du 23.08 — bloc droit', REL],
    ['Bloc gauche', 'miroir du bloc droit', REL],
    ['Profondeur aux bords de bloc', `${DMIN.toFixed(2)} m`, REL],
    ['Creux médian', `${DCREUX.toFixed(2)} m`, REL],
    ['Crêtes', `${DMAX.toFixed(2)} m et 1,40 m`, REL],
    ['Développé par balcon', `${dev.toFixed(2)} ml — votre relevé annonçait ~10 ml`, SUP],
    ['Total', `${BALCONS.length} niveaux × 2 blocs = ${BALCONS.length * 2} rives → ≈ ${(dev * BALCONS.length * 2).toFixed(0)} ml`, DED],
  ]],
  ['Terrasses du R+2', [
    ['Nombre', '2, une par logement', REL],
    ['Dimensions', '7,85 × 4,00 m chacune', REL],
    ['Garde-corps', 'droit sur les trois côtés ouverts, aucune ondulation', REL],
    ['Séparation', 'bande centrale de 1,80 m, fermée par un garde-corps de chaque côté', REL],
    ['Usage de cette bande', 'non affectée — à définir', SUP],
  ]],
  ['Menuiseries', [
    ['Portes-balcon', `${PBW.toFixed(2)} m de large × ${PBH.toFixed(2)} m de haut`, REL],
    ['Nombre par balcon', '2', REL],
    ['Profilé', 'aluminium TPR série 65, rupture de pont thermique', REL],
    ['Teinte', 'RAL 7024 gris graphite', REL],
    ['Vitrage', 'double vitrage 4/16/4', SUP],
    ['Niche centrale', '1 porte-balcon par logement, en vis-à-vis', SUP],
  ]],
  ['Matériaux et teintes', [
    ['Monocouche — fond', 'teinte latte', REL],
    ['Monocouche — poteaux et acrotères', 'blanc', REL],
    ['Bandeaux de rive ondulés', 'Aquapanel cintré, finition blanche', REL],
    ['Garde-corps — remplissage', 'verre feuilleté teinté NOIR', REL],
    ['Garde-corps — structure', 'barreaudage et main courante inox', REL],
    ['Brise-vue', 'lames aluminium RAL 7024', REL],
    ['Hauteur de garde-corps', '1,10 m', SUP],
  ]],
  ['Éclairage', [
    ['Sous-face des rives', 'gorge LED continue, profil aluminium', REL],
    ['Entre les deux portes-balcon', 'profil LED vertical, éclairage latéral', REL],
    ['Niche centrale', 'brise-vue rétroéclairé', SUP],
    ['Entrée et portes de garage', 'bandeau lumineux', SUP],
    ['Température de couleur', '3000 K, IP65', SUP],
  ]],
];

const QUESTIONS = [
  ['Vos « 7 m » d’ouverture de balcon', 'Je les ai lus comme l’entraxe des poteaux (7,30 m), ce qui donne 6,75 m d’ouverture libre et boucle exactement les 17,50 m. Si les 7,00 m sont l’ouverture libre, la façade fait 18,00 m et tout se décale.'],
  ['Développé de l’onde', `Votre tracé lissé donne ${dev.toFixed(2)} ml par balcon ; vous aviez annoncé ~10 ml. L’écart vient du lissage du trait à main levée. Si les 10 ml sont fermes, je creuse légèrement les lobes.`],
  ['Acrotère', 'J’ai pris 1,00 m au-dessus de la dalle de toiture. À confirmer.'],
  ['La bande centrale de 1,80 m au R+2', 'Sur votre croquis elle est fermée par un garde-corps de chaque côté, donc elle n’appartient à aucun des deux logements. Local technique ? Simple vide de ventilation ? Terrasse partagée ?'],
  ['Profondeur du bâtiment', 'Inconnue — la coupe est dessinée en coupe partielle. Donnez-la moi si vous voulez une coupe complète.'],
  ['Niche centrale', 'Vous avez dit 1,80 de large et 1,50 de creux. Combien de portes-balcon donnent dedans, et de quel côté ?'],
];

const tag = (t) => {
  const col = t === REL ? ['#2F4F3A', '#DDE8DE'] : t === DED ? ['#4A4433', '#E9E3D3'] : ['#6E3B2E', '#F0DDD6'];
  return `<span style="display: inline-block; font-size: 9px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; padding: 2px 7px; border-radius: 2px; color: ${col[0]}; background: ${col[1]}; white-space: nowrap">${t}</span>`;
};

const bloc = ([titre, lignes]) => `<div style="break-inside: avoid; margin-bottom: 22px">
  <div style="font-family: 'Space Grotesk', 'Helvetica Neue', Arial, sans-serif; font-size: 14px; font-weight: 600; padding-bottom: 7px; border-bottom: 1.5px solid #23211E">${titre}</div>
  ${lignes.map(([k, v, t]) => `<div style="display: flex; gap: 12px; align-items: baseline; padding: 6px 0; border-bottom: 1px solid #E2DACB">
    <div style="flex: 0 0 178px; font-size: 11.5px; color: #6E6659">${k}</div>
    <div style="flex: 1; font-size: 12px; color: #23211E; text-wrap: pretty">${v}</div>
    <div style="flex: 0 0 auto">${tag(t)}</div>
  </div>`).join('\n  ')}
</div>`;

const body = `<div style="width: ${W}px; background: #F1EDE5">
${header({ w: W, kicker: 'Immeuble R+8 · logements · Algérie',
  title: 'Données du projet — à valider',
  sub: 'Tout ce que vous m’avez donné, plus ce que j’en ai déduit. Corrigez ce qui est faux et je relance le dessin sur cette base ; rien n’est dessiné tant que cette page n’est pas validée.',
  right: 'SYNTHÈSE · 23.08.2026<br>AVANT DESSIN<br>COTES EN MÈTRES' })}
<div style="padding: 26px 44px 6px; column-count: 2; column-gap: 46px">
  ${BLOCS_DATA.map(bloc).join('\n  ')}
</div>
<div style="padding: 8px 44px 40px">
  <div class="rule" style="margin-bottom: 20px"></div>
  <div class="eyebrow" style="margin-bottom: 14px">Les six points qu’il me manque</div>
  <div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px 34px">
    ${QUESTIONS.map(([t, d], i) => `<div style="display: flex; gap: 11px; align-items: flex-start">
      <div style="flex: 0 0 auto; width: 21px; height: 21px; border: 1px solid #23211E; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; margin-top: 1px">${i + 1}</div>
      <div>
        <div style="font-family: 'Space Grotesk', 'Helvetica Neue', Arial, sans-serif; font-size: 12.5px; font-weight: 600">${t}</div>
        <div style="font-size: 11.5px; line-height: 1.55; color: #6E6659; margin-top: 4px; text-wrap: pretty">${d}</div>
      </div>
    </div>`).join('\n    ')}
  </div>
</div>
</div>`;

writeFileSync('Synthese.dc.html', page({ body, props: JSON.stringify({ $preview: { width: W, height: 1400 } }) }));
console.log('Synthese.dc.html ok');
