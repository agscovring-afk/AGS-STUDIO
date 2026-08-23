// Page de présentation du projet — un artifact publiable.
// Les images sont embarquées en base64 : la page doit tenir toute seule.
import { readFileSync, writeFileSync } from 'node:fs';
import { ondeAt, BLOC, ONDE, developpe, gcSegmentsLocal, LV, W, COL, RETRAIT, AXE, BV_EP } from './geo.mjs';

const SP = process.env.SP;
const b64 = (f, mime) => `data:${mime};base64,` + readFileSync(`${SP}/web/${f}`).toString('base64');
const IMG = {
  rueVerre: b64('rue-verre.jpg', 'image/jpeg'),
  rueFer: b64('rue-fer.jpg', 'image/jpeg'),
  rueInox: b64('rue-inox.jpg', 'image/jpeg'),
  rueNuit: b64('rue-nuit.jpg', 'image/jpeg'),
  gcVerre: b64('gc-verre.jpg', 'image/jpeg'),
  gcFer: b64('gc-fer.jpg', 'image/jpeg'),
  gcInox: b64('gc-inox.jpg', 'image/jpeg'),
  elevation: b64('elevation.png', 'image/png'),
  plan: b64('plan.png', 'image/png'),
  detailGc: b64('detail-gc.png', 'image/png'),
  mat0: b64('mat-0.jpg','image/jpeg'), mat1: b64('mat-1.jpg','image/jpeg'),
  mat2: b64('mat-2.jpg','image/jpeg'), mat3: b64('mat-3.jpg','image/jpeg'),
};

// --- le tracé de l'onde, à plat, tel qu'il est construit -------------------
const N = 400, VW = 1000, VH = 300, PAD = 40;
const sx = (u) => PAD + (u / BLOC) * (VW - 2 * PAD);
const sy = (d) => PAD + (d / 1.80) * (VH - 2 * PAD);
let onde = '';
for (let i = 0; i <= N; i++) {
  const u = BLOC * i / N;
  onde += `${i ? 'L' : 'M'} ${sx(u).toFixed(1)} ${sy(ondeAt(u)).toFixed(1)} `;
}
const pts = ONDE.map(([u, d]) => ({ u, d, x: +sx(u).toFixed(1), y: +sy(d).toFixed(1) }));
const SEG = gcSegmentsLocal();
const DEV = developpe();

const H = (s) => s;
const html = H(`<title>L’onde de rive</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>
:root{
  --ground:#F2F1EE; --surface:#FFFFFF; --sunk:#E7E6E1;
  --ink:#1B1E21; --muted:#6E7278; --line:#D8D7D2; --hair:#C9C8C2;
  --led:#B8842B; --led-soft:#E9C87E; --stone:#B79E76; --graphite:#474B4E;
  --shadow:0 1px 2px rgba(24,28,32,.05), 0 12px 32px -12px rgba(24,28,32,.16);
}
@media (prefers-color-scheme:dark){ :root:not([data-theme="light"]){
  --ground:#15181B; --surface:#1E2226; --sunk:#101315;
  --ink:#ECEAE5; --muted:#969CA2; --line:#2E3338; --hair:#3A4046;
  --led:#E7B94F; --led-soft:#7A5F2A; --stone:#C9B695; --graphite:#AAB0B5;
  --shadow:0 1px 2px rgba(0,0,0,.4), 0 14px 40px -14px rgba(0,0,0,.6);
}}
:root[data-theme="dark"]{
  --ground:#15181B; --surface:#1E2226; --sunk:#101315;
  --ink:#ECEAE5; --muted:#969CA2; --line:#2E3338; --hair:#3A4046;
  --led:#E7B94F; --led-soft:#7A5F2A; --stone:#C9B695; --graphite:#AAB0B5;
  --shadow:0 1px 2px rgba(0,0,0,.4), 0 14px 40px -14px rgba(0,0,0,.6);
}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);
  font-family:'Archivo','Helvetica Neue',Arial,sans-serif;font-size:17px;line-height:1.6;
  -webkit-font-smoothing:antialiased}
h1,h2,h3{margin:0;font-weight:700;font-stretch:112%;letter-spacing:-.022em;text-wrap:balance;line-height:1.02}
p{margin:0}
img{max-width:100%;display:block}
.wrap{max-width:1180px;margin:0 auto;padding:0 28px}
.narrow{max-width:660px}
.mono{font-family:'IBM Plex Mono',ui-monospace,Menlo,monospace;font-variant-numeric:tabular-nums}
.eyebrow{font-family:'IBM Plex Mono',monospace;font-size:11.5px;letter-spacing:.20em;
  text-transform:uppercase;color:var(--muted)}
section{padding:112px 0;border-top:1px solid var(--line)}
section:first-of-type{border-top:0}
.lede{font-size:19px;color:var(--muted);max-width:62ch;margin-top:20px}

/* ---------- hero ---------- */
.hero{padding:96px 0 88px;border:0}
.hero h1{font-size:clamp(46px,8.4vw,116px);font-stretch:118%;font-weight:800}
.hero h1 em{font-style:normal;color:var(--led)}
.wavebox{margin:52px 0 12px;position:relative}
.wavebox svg{width:100%;height:auto;overflow:visible}
.trace{fill:none;stroke:var(--ink);stroke-width:3.4;stroke-linecap:round;
  stroke-dasharray:var(--len);stroke-dashoffset:var(--len)}
.drawn .trace{transition:stroke-dashoffset 2.4s cubic-bezier(.22,.61,.36,1);stroke-dashoffset:0}
.nu{stroke:var(--hair);stroke-width:1.4;stroke-dasharray:7 6}
.tick{stroke:var(--led);stroke-width:2}
.dot{fill:var(--led)}
.cote{font-family:'IBM Plex Mono',monospace;font-size:15px;fill:var(--ink);font-weight:600;
  paint-order:stroke;stroke:var(--ground);stroke-width:5px;stroke-linejoin:round}
.coteL{font-family:'IBM Plex Mono',monospace;font-size:11px;fill:var(--muted);letter-spacing:.12em}
.pt{opacity:0;transition:opacity .5s ease}
.drawn .pt{opacity:1}
.drawn .pt:nth-of-type(1){transition-delay:.7s}
.drawn .pt:nth-of-type(2){transition-delay:1.15s}
.drawn .pt:nth-of-type(3){transition-delay:1.6s}
.keyline{display:flex;flex-wrap:wrap;gap:38px 56px;margin-top:44px;
  padding-top:26px;border-top:1px solid var(--line)}
.kv b{display:block;font-family:'IBM Plex Mono',monospace;font-size:30px;font-weight:600;letter-spacing:-.02em}
.kv span{font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--muted)}

/* ---------- images ---------- */
figure{margin:0}
.shot{border:1px solid var(--line);background:var(--surface);box-shadow:var(--shadow);overflow:hidden}
figcaption{margin-top:14px;font-size:14px;color:var(--muted);max-width:58ch}
.duo{display:grid;grid-template-columns:1fr 1fr;gap:28px;align-items:start}
.rue{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:44px;align-items:end}

/* ---------- boutons ---------- */
.switch{display:inline-flex;gap:4px;padding:4px;border:1px solid var(--line);
  background:var(--surface);border-radius:2px}
.switch button{appearance:none;border:0;background:transparent;color:var(--muted);
  font-family:'IBM Plex Mono',monospace;font-size:12px;letter-spacing:.10em;text-transform:uppercase;
  padding:9px 15px;cursor:pointer;border-radius:1px;transition:background .18s,color .18s}
.switch button:hover{color:var(--ink)}
.switch button[aria-pressed="true"]{background:var(--ink);color:var(--ground)}
.switch button:focus-visible{outline:2px solid var(--led);outline-offset:2px}

/* ---------- matière ---------- */
.mats{display:grid;grid-template-columns:repeat(4,1fr);gap:22px;margin-top:44px}
.mat{border:1px solid var(--line);background:var(--surface)}
.mat .chip{height:112px;background-color:var(--sunk)}
.mat .txt{padding:16px 18px 20px}
.mat h3{font-size:15.5px;font-stretch:106%}
.mat p{font-size:13.5px;color:var(--muted);margin-top:7px;line-height:1.5}

/* ---------- listes ---------- */
.rows{margin-top:40px;border-top:1px solid var(--line)}
.row{display:grid;grid-template-columns:44px 1fr 168px;gap:24px;align-items:baseline;
  padding:22px 0;border-bottom:1px solid var(--line)}
.row .n{font-family:'IBM Plex Mono',monospace;font-size:12px;color:var(--led);letter-spacing:.1em}
.row h3{font-size:18px;font-stretch:106%}
.row p{font-size:15px;color:var(--muted);margin-top:6px;max-width:58ch}
.row .tag{font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--muted);text-align:right}
footer{padding:72px 0 96px;border-top:1px solid var(--line);color:var(--muted);font-size:14px}
footer b{color:var(--ink);font-weight:600}
@media (max-width:900px){
  section{padding:80px 0}
  .duo,.rue,.mats{grid-template-columns:1fr}
  .row{grid-template-columns:32px 1fr;gap:16px}
  .row .tag{grid-column:2;text-align:left;margin-top:8px}
}
@media (prefers-reduced-motion:reduce){
  .trace{stroke-dashoffset:0;transition:none}
  .pt{opacity:1;transition:none}
}
</style>

<div class="wrap hero">
  <div class="eyebrow">Immeuble R+8 · logements · Algérie</div>
  <h1>Une façade<br>qui tient dans<br><em>une seule ligne.</em></h1>
  <p class="lede">Tout le projet part de là : la rive du balcon quitte le poteau perpendiculairement au nu, creuse un grand lobe, revient, en creuse un second plus court, et rejoint le poteau d’en face. Le reste — la structure, le garde-corps, l’éclairage, le prix — découle de cette ligne.</p>

  <div class="wavebox" id="wavebox">
    <svg viewBox="0 0 ${VW} ${VH}" role="img" aria-label="Profil de l'onde de rive : 0 au poteau, 1,80 m au grand lobe, 0,79 m au creux médian, 1,45 m au petit lobe, retour à 0.">
      <line class="nu" x1="${PAD}" y1="${sy(0)}" x2="${VW - PAD}" y2="${sy(0)}"/>
      <text class="coteL" x="${PAD}" y="${sy(0) - 14}">NU DE FAÇADE</text>
      <path class="trace" d="${onde.trim()}"/>
      ${pts.slice(1, 4).map((p) => `<g class="pt">
        <line class="tick" x1="${p.x}" y1="${sy(0)}" x2="${p.x}" y2="${p.y}"/>
        <circle class="dot" cx="${p.x}" cy="${p.y}" r="5"/>
        <text class="cote" x="${p.x + 14}" y="${p.y + (p.d > 1 ? 26 : -14)}">${p.d.toFixed(2).replace('.', ',')} m</text>
      </g>`).join('')}
    </svg>
  </div>

  <div class="keyline">
    <div class="kv"><b>${DEV.toFixed(2).replace('.', ',')} ml</b><span>développé par balcon</span></div>
    <div class="kv"><b>12</b><span>balcons, 6 niveaux × 2 blocs</span></div>
    <div class="kv"><b>${W.toFixed(2).replace('.', ',')} m</b><span>largeur de façade</span></div>
    <div class="kv"><b>${SEG.length}</b><span>panneaux de garde-corps</span></div>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="eyebrow">La règle du tracé</div>
    <h2 style="font-size:clamp(28px,4vw,44px);margin-top:16px">Elle naît sur le poteau,<br>elle ne s’en écarte pas.</h2>
    <p class="lede">C’est le point qui a demandé trois tours de correction. Une courbe qui quitte le mur en douceur donne une rive molle ; une courbe qui en part <em>perpendiculairement</em> donne un lobe franc, comme un demi-cercle qui prend appui sur la façade. Les deux portées d’extrémité sont donc des quarts d’ellipse, les portées intérieures un raccord en cosinus — d’où des fonds de lobe et un creux bien plats.</p>
    <div class="duo" style="margin-top:52px">
      <figure><div class="shot"><img src="${IMG.plan}" alt="Plan du niveau courant : l'onde de rive des deux blocs, cotée."></div>
        <figcaption>Plan du niveau courant au 1:50. Le bloc gauche est le miroir exact du bloc droit. Rayon minimal rencontré : 0,77 m, à la crête et au creux.</figcaption></figure>
      <figure><div class="shot"><img src="${IMG.elevation}" alt="Élévation de la façade principale au 1:100."></div>
        <figcaption>Élévation au 1:100. Une élévation orthogonale ne peut pas montrer une courbe qui se développe en plan : ici elle se lit à l’ombre portée, proportionnelle au porte-à-faux.</figcaption></figure>
    </div>
  </div>
</section>

<section id="rue">
  <div class="wrap">
    <div class="rue">
      <div>
        <div class="eyebrow">Depuis la rue</div>
        <h2 style="font-size:clamp(28px,4vw,44px);margin-top:16px">Ce que voit le passant.</h2>
      </div>
      <div style="padding-bottom:6px">
        <div class="switch" role="group" aria-label="Heure de la vue">
          <button type="button" data-rue="jour" aria-pressed="true">Jour</button>
          <button type="button" data-rue="nuit" aria-pressed="false">Nuit</button>
        </div>
      </div>
    </div>
    <figure style="margin-top:36px">
      <div class="shot"><img id="rueImg" src="${IMG.rueVerre}" alt="Perspective de rue de l'immeuble, de jour."></div>
      <figcaption id="rueCap">Objectif à décentrement — les verticales restent verticales, comme en photo d’architecture. Soleil à 49° de hauteur, 32° à gauche de la normale : chaque ombre portée sur la façade est calculée depuis la géométrie du balcon qui la jette.</figcaption>
    </figure>
  </div>
</section>

<section id="gc">
  <div class="wrap">
    <div class="eyebrow">À trancher</div>
    <h2 style="font-size:clamp(28px,4vw,44px);margin-top:16px">Trois garde-corps<br>sur la même rive.</h2>
    <p class="lede">Le tracé, les fixations et la main courante ne changent pas. Ce qui change, c’est ce qu’on met entre le sol et la main courante — et ça change tout le caractère de l’immeuble. ${SEG.length} panneaux de ${(SEG[0].ml * 100).toFixed(0)} cm par balcon dans les trois cas.</p>
    <div style="margin-top:34px" class="switch" role="group" aria-label="Type de garde-corps">
      <button type="button" data-gc="verre" aria-pressed="true">Tout verre</button>
      <button type="button" data-gc="fer" aria-pressed="false">Fer forgé</button>
      <button type="button" data-gc="inox" aria-pressed="false">Tout inox</button>
    </div>
    <figure style="margin-top:28px">
      <div class="shot"><img id="gcImg" src="${IMG.gcVerre}" alt="Détail de façade avec garde-corps tout verre."></div>
      <figcaption id="gcCap">Verre feuilleté 8.8.4 sur pinces inox. Le plus discret : la courbe reste seule, rien ne la concurrence. Sur les deux zones les plus serrées un panneau plat s’écarte de la courbe théorique de 17 mm — il faut des pinces à rotule.</figcaption>
    </figure>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="eyebrow">La matière</div>
    <h2 style="font-size:clamp(28px,4vw,44px);margin-top:16px">Quatre matériaux, pas un de plus.</h2>
    <p class="lede">Les pastilles ci-dessous ne sont pas des aplats : chaque matière est construite d’après sa structure réelle, à l’échelle réelle. Les lits de sédimentation du travertin font 5 cm, ses pores 3 à 8 mm ; le grain du monocouche gratté fait 3 mm.</p>
    <div class="mats">
      <div class="mat"><div class="chip" style="background-image:url(${IMG.mat1});background-size:cover;background-position:center"></div>
        <div class="txt"><h3>Monocouche blanc</h3><p>Grain fin gratté, joint creux de 15 mm au droit de chaque plancher. C’est lui qui dessine la ligne d’étage.</p></div></div>
      <div class="mat"><div class="chip" style="background-image:url(${IMG.mat0});background-size:cover;background-position:center"></div>
        <div class="txt"><h3>Travertin</h3><p>Façade ventilée sur les quatre poteaux. Saillie 13 cm, lame d’air, panneaux de 1,20 m à joints creux ouverts.</p></div></div>
      <div class="mat"><div class="chip" style="background-image:url(${IMG.mat2});background-size:cover;background-position:center"></div>
        <div class="txt"><h3>Aluminium RAL 7024</h3><p>Menuiseries TPR 65 à rupture de pont thermique, cadrage des baies, brise-vue, couvertines.</p></div></div>
      <div class="mat"><div class="chip" style="background-image:url(${IMG.mat3});background-size:cover;background-position:center"></div>
        <div class="txt"><h3>Inox 316 brossé</h3><p>Main courante Ø 42 continue, pinces et platines. Brossé dans le sens de la pièce — le reflet glisse le long de la courbe.</p></div></div>
    </div>
    <div class="duo" style="margin-top:56px">
      <figure><div class="shot"><img src="${IMG.detailGc}" alt="Planche de détail du garde-corps aux échelles 1:20 et 1:5."></div>
        <figcaption>Le garde-corps développé à plat, plus les deux coupes types au 1:5. La planche dit franchement ce que coûte une corde de 40 cm sur cette courbe.</figcaption></figure>
      <div>
        <h3 style="font-size:20px">L’éclairage fait le travail de nuit</h3>
        <p style="color:var(--muted);margin-top:12px">Une gorge de 50 × 50 mm creusée en sous-face de chaque bandeau, ruban 3000 K IP65. Elle ne s’allume pas seule : elle lave la sous-face au-dessus d’elle et le mur en dessous. C’est ce halo, pas le trait lumineux, qui fait lire la courbe depuis la rue.</p>
        <p style="color:var(--muted);margin-top:14px">S’y ajoute un profil vertical de 60 × 40 mm encastré dans le trumeau entre les deux portes-balcon, sur 1,90 m de haut, sur le même circuit.</p>
        <div class="keyline" style="margin-top:30px">
          <div class="kv"><b>${(DEV * 12).toFixed(0)} ml</b><span>de gorge LED</span></div>
          <div class="kv"><b>3000 K</b><span>température</span></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap narrow">
    <div class="eyebrow">Avant d’aller plus loin</div>
    <h2 style="font-size:clamp(26px,3.6vw,38px);margin-top:16px">Trois décisions vous appartiennent.</h2>
    <div class="rows">
      <div class="row"><div class="n">01</div>
        <div><h3>Le garde-corps</h3><p>Tout verre, fer forgé, ou tout inox. Les trois sont rendus plus haut, sur la même rive et la même lumière.</p></div>
        <div class="tag">Bloque le dossier</div></div>
      <div class="row"><div class="n">02</div>
        <div><h3>Les « 7 m » de baie</h3><p>Entraxe des poteaux — l’hypothèse retenue, qui donne 6,75 m libre et 17,50 m au total — ou largeur libre ? Dans le second cas la façade passe à 18,00 m et toutes les cotes se décalent.</p></div>
        <div class="tag">Jamais tranché</div></div>
      <div class="row"><div class="n">03</div>
        <div><h3>Le vide central</h3><p>Le garde-corps des deux petits balcons s’arrête à 0,70 m en arrière du nu, ce qui laisse la fente ouverte devant eux. Ou bien on l’aligne sur la façade, et le creusement passe de 1,50 à 0,80 m.</p></div>
        <div class="tag">Une seule cote</div></div>
    </div>
  </div>
</section>

<footer><div class="wrap">
  <b>Immeuble R+8 — façade principale.</b> Dossier de 20 planches : élévation, plans, coupe, carnet de détails au 1:10 et 1:5, perspectives. Toutes les cotes de cette page sortent d’une seule source de géométrie — changer une valeur refait les vingt planches.
</div></footer>

<script>
(function(){
  var box = document.getElementById('wavebox');
  var path = box.querySelector('.trace');
  try { path.style.setProperty('--len', Math.ceil(path.getTotalLength())); } catch(e) {}
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e){ if (e.isIntersecting) { box.classList.add('drawn'); io.disconnect(); } });
    }, { threshold: .25 });
    io.observe(box);
  } else { box.classList.add('drawn'); }

  var GC = {
    verre: { src: ${JSON.stringify(IMG.gcVerre)}, alt: 'Détail de façade avec garde-corps tout verre.',
      cap: "Verre feuilleté 8.8.4 sur pinces inox. Le plus discret : la courbe reste seule, rien ne la concurrence. Sur les deux zones les plus serrées un panneau plat s’écarte de la courbe théorique de 17 mm — il faut des pinces à rotule." },
    fer: { src: ${JSON.stringify(IMG.gcFer)}, alt: 'Détail de façade avec garde-corps en fer forgé.',
      cap: "Barreaux plats au pas de 13 cm et un registre de volutes entre deux lisses. Le plus habité des trois, et celui qui se fabrique le plus facilement ici. Il épouse n’importe quel rayon, donc aucune contrainte de courbure." },
    inox: { src: ${JSON.stringify(IMG.gcInox)}, alt: 'Détail de façade avec garde-corps tout inox.',
      cap: "Barreaudage inox 316 Ø 16 au pas de 11 cm, deux lisses intermédiaires. Le plus technique : il suit la courbe exactement, chaque barreau étant un point sur la rive." }
  };
  var RUE = {
    jour: { src: ${JSON.stringify(IMG.rueVerre)}, alt: "Perspective de rue de l'immeuble, de jour.",
      cap: "Objectif à décentrement — les verticales restent verticales, comme en photo d’architecture. Soleil à 49° de hauteur, 32° à gauche de la normale : chaque ombre portée sur la façade est calculée depuis la géométrie du balcon qui la jette." },
    nuit: { src: ${JSON.stringify(IMG.rueNuit)}, alt: "Perspective de rue de l'immeuble, de nuit.",
      cap: "La nuit, la gorge LED lave la sous-face du bandeau et le mur au-dessous. La façade disparaît, l’onde reste." }
  };
  function bind(attr, data, img, cap){
    var imgEl = document.getElementById(img), capEl = document.getElementById(cap);
    document.querySelectorAll('[data-' + attr + ']').forEach(function(b){
      b.addEventListener('click', function(){
        var k = b.getAttribute('data-' + attr), d = data[k];
        if (!d) return;
        document.querySelectorAll('[data-' + attr + ']').forEach(function(o){
          o.setAttribute('aria-pressed', String(o === b));
        });
        imgEl.src = d.src; imgEl.alt = d.alt; capEl.textContent = d.cap;
      });
    });
  }
  bind('gc', GC, 'gcImg', 'gcCap');
  bind('rue', RUE, 'rueImg', 'rueCap');
})();
</script>`);

writeFileSync('site-facade.html', html);
console.log('site-facade.html —', (html.length / 1024 / 1024).toFixed(2), 'Mo');
