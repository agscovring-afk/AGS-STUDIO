// Bibliothèque de matières procédurales.
//
// Le premier jeu de filtres se contentait d'un feTurbulence par matériau : ça
// donne du bruit, pas de la matière. Une matière a une STRUCTURE, et c'est
// elle qu'il faut modéliser.
//   . le travertin est un calcaire de source : il se dépose en lits
//     horizontaux, et les bulles de gaz piégées à la sédimentation donnent des
//     pores étirés dans le sens du lit. Donc : bandes + pores allongés + veines.
//   . le monocouche gratté est un mortier chargé d'un granulat fin que le
//     grattage arrache : grain isotrope serré, très peu de relief.
//   . l'inox brossé est anisotrope : des stries dans un seul sens, et un
//     reflet qui glisse perpendiculairement aux stries.
//   . le laqué RAL 7024 n'a presque pas de texture — juste un micro-grain qui
//     casse l'aplat, sinon il sonne plastique.

export function FILTRES({ ech = 1 } = {}) {
  // ech : px par metre, pour que la finesse du grain suive l'echelle du dessin
  const f = (m) => +(1 / (m * ech)).toFixed(4);      // frequence d'un motif de m metres

  return `
  <!-- TRAVERTIN : lits horizontaux + pores fins etires + veines
       Echelle reelle : un pore de travertin fait 2 a 8 mm, pas 7 cm. C'est
       le LIT qui se voit de loin, pas le pore — le pore ne se lit qu'au nez
       du parement. Les deux doivent donc etre a leur vraie taille, sinon la
       pierre tourne au bois. -->
  <filter id="mTravertin" x="0%" y="0%" width="100%" height="100%">
    <!-- 1. les lits de sedimentation : tres etales en X, serres en Y -->
    <feTurbulence type="fractalNoise" baseFrequency="${f(1.8)} ${f(0.048)}"
                  numOctaves="4" seed="21" result="lits"/>
    <!-- 2. les pores : 3 a 8 mm, etires dans le sens du lit, et rares -->
    <feTurbulence type="fractalNoise" baseFrequency="${f(0.008)} ${f(0.0035)}"
                  numOctaves="2" seed="5" result="p0"/>
    <feColorMatrix in="p0" type="matrix" result="pores"
      values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 16 0 -8.9"/>
    <!-- 3. les veines : longues, presque horizontales, tres douces -->
    <feTurbulence type="turbulence" baseFrequency="${f(2.6)} ${f(0.16)}"
                  numOctaves="2" seed="13" result="v0"/>
    <feColorMatrix in="v0" type="matrix" result="veines"
      values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  1.15 0 0 0 -0.42"/>
    <!-- 4. relief : le lit porte la forme, le pore creuse a peine -->
    <feComposite in="lits" in2="pores" operator="arithmetic"
                 k1="0" k2="1" k3="-0.32" k4="0.06" result="hauteur"/>
    <feDiffuseLighting in="hauteur" lighting-color="#ffffff" surfaceScale="1.25"
                       diffuseConstant="1" result="lum">
      <feDistantLight azimuth="212" elevation="48"/>
    </feDiffuseLighting>
    <feComposite in="lum" in2="SourceGraphic" operator="arithmetic"
                 k1="1.16" k2="0" k3="0" k4="-0.055" result="pierre"/>
    <!-- 5. les veines assombrissent legerement, sans relief -->
    <feComposite in="veines" in2="pierre" operator="arithmetic"
                 k1="-0.085" k2="0" k3="1" k4="0" result="out"/>
  </filter>

  <!-- MONOCOUCHE GRATTE : grain fin serre, relief tres faible -->
  <filter id="mMonocouche" x="0%" y="0%" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="${f(0.0032)}" numOctaves="3" seed="7" result="grain"/>
    <feTurbulence type="fractalNoise" baseFrequency="${f(0.9)} ${f(1.6)}" numOctaves="2" seed="31" result="nuage"/>
    <feComposite in="grain" in2="nuage" operator="arithmetic" k1="0" k2="1" k3="0.22" k4="-0.06" result="h"/>
    <feDiffuseLighting in="h" lighting-color="#ffffff" surfaceScale="0.95" result="lum">
      <feDistantLight azimuth="215" elevation="58"/>
    </feDiffuseLighting>
    <feComposite in="lum" in2="SourceGraphic" operator="arithmetic" k1="1.16" k2="0" k3="0" k4="-0.022"/>
  </filter>

  <!-- BETON LISSE (banche) : nuages larges + bulles rares -->
  <filter id="mBeton" x="0%" y="0%" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="${f(0.55)} ${f(0.40)}" numOctaves="4" seed="11" result="n"/>
    <feTurbulence type="fractalNoise" baseFrequency="${f(0.035)}" numOctaves="1" seed="44" result="b0"/>
    <feColorMatrix in="b0" type="matrix" result="bulles"
      values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 9 0 -4.9"/>
    <feComposite in="n" in2="bulles" operator="arithmetic" k1="0" k2="1" k3="-0.5" k4="0.08" result="h"/>
    <feDiffuseLighting in="h" lighting-color="#ffffff" surfaceScale="1.1" result="lum">
      <feDistantLight azimuth="215" elevation="55"/>
    </feDiffuseLighting>
    <feComposite in="lum" in2="SourceGraphic" operator="arithmetic" k1="1.06" k2="0" k3="0" k4="-0.05"/>
  </filter>

  <!-- INOX BROSSE : stries dans un seul sens -->
  <filter id="mInox" x="0%" y="0%" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="${f(0.6)} ${f(0.0016)}" numOctaves="2" seed="3" result="stries"/>
    <feDiffuseLighting in="stries" lighting-color="#ffffff" surfaceScale="1.5" result="lum">
      <feDistantLight azimuth="0" elevation="46"/>
    </feDiffuseLighting>
    <feComposite in="lum" in2="SourceGraphic" operator="arithmetic" k1="1.12" k2="0" k3="0" k4="-0.10"/>
  </filter>

  <!-- LAQUE RAL 7024 : micro-grain, presque rien, mais pas un aplat -->
  <filter id="mLaque" x="0%" y="0%" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="${f(0.0022)}" numOctaves="2" seed="17" result="g"/>
    <feDiffuseLighting in="g" lighting-color="#ffffff" surfaceScale="0.35" result="lum">
      <feDistantLight azimuth="215" elevation="66"/>
    </feDiffuseLighting>
    <feComposite in="lum" in2="SourceGraphic" operator="arithmetic" k1="1.02" k2="0" k3="0" k4="-0.018"/>
  </filter>

  <!-- BITUME : granulat grossier, relief marque -->
  <filter id="mBitume" x="0%" y="0%" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="${f(0.012)} ${f(0.008)}" numOctaves="4" seed="19" result="n"/>
    <feDiffuseLighting in="n" lighting-color="#ffffff" surfaceScale="1.3" result="lum">
      <feDistantLight azimuth="215" elevation="50"/>
    </feDiffuseLighting>
    <feComposite in="lum" in2="SourceGraphic" operator="arithmetic" k1="1.10" k2="0" k3="0" k4="-0.085"/>
  </filter>`;
}

// Teintes de base, avant eclairement
export const TEINTE = {
  travertin: '#CFBC9C', travertinFonce: '#B9A483',
  monocouche: '#F4F1EA', beton: '#D6D2C8',
  inox: '#BFC6CB', laque7024: '#474B4E', bitume: '#7B7B76',
};
