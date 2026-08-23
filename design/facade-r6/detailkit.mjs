// Trames et primitives des planches de detail (1:10 et 1:5).
// Les hachures suivent la convention du dessin d'execution : le beton arme
// hachure a 45°, la brique creuse dessine ses alveoles, l'isolant se croise,
// l'aluminium est plein, le verre est un aplat clair a filet.

export const D = {
  ink: '#23211E', dim: '#8C8478', fine: '#B7AFA1',
  beton: '#D9D5CC', betonH: '#9A948A',
  brique: '#E3D3BE', briqueH: '#B79C7C',
  isol: '#F2EBDC', isolH: '#C9B58F',
  mono: '#FAF8F4', monoH: '#CFC8BA',
  alu: '#474B4E', aluD: '#31353A',
  verre: '#CFE0E4', verreL: '#8FA9AE',
  inox: '#AEB7BC', inoxD: '#7E888E',
  aqua: '#FFFFFF', aquaH: '#C8C2B6',
  etan: '#2A2724', mortier: '#E8E3D8',
  carr: '#EFEBE2', led: '#E7B94F',
  plot: '#6E6A62', bois: '#D8BE94', paper: '#FFFFFF',
};

// Trames SVG. Le pas est donne en px ecran, il est donc lie a l'echelle de la
// planche : PAT(S) rend les motifs a la bonne finesse pour le facteur S.
export function PATTERNS(S) {
  const u = (m) => +(m * S).toFixed(2);          // metres -> px
  const p = [];
  const pat = (id, w, h, body, bg) =>
    p.push(`<pattern id="${id}" width="${w}" height="${h}" patternUnits="userSpaceOnUse">${bg ? `<rect width="${w}" height="${h}" fill="${bg}"/>` : ''}${body}</pattern>`);

  const hb = u(0.028);                            // pas des hachures 45°, 2.8 cm
  pat('pBeton', hb, hb,
    `<path d="M 0 ${hb} L ${hb} 0 M ${-hb / 2} ${hb / 2} L ${hb / 2} ${-hb / 2} M ${hb / 2} ${hb * 1.5} L ${hb * 1.5} ${hb / 2}" stroke="${D.betonH}" stroke-width="0.8"/>`, D.beton);

  const bq = u(0.075);                            // alveoles de brique creuse
  pat('pBrique', bq, bq,
    `<rect x="${bq * 0.16}" y="${bq * 0.16}" width="${bq * 0.68}" height="${bq * 0.68}" fill="none" stroke="${D.briqueH}" stroke-width="0.9"/>`, D.brique);

  const iz = u(0.05);
  pat('pIsol', iz, iz,
    `<path d="M 0 0 L ${iz} ${iz} M ${iz} 0 L 0 ${iz}" stroke="${D.isolH}" stroke-width="0.7"/>`, D.isol);

  const mz = u(0.018);
  pat('pMono', mz, mz,
    `<circle cx="${mz / 2}" cy="${mz / 2}" r="0.7" fill="${D.monoH}"/>`, D.mono);

  const az = u(0.02);
  pat('pAqua', az, az * 1.6,
    `<circle cx="${az / 2}" cy="${az * 0.8}" r="0.6" fill="${D.aquaH}"/>`, D.aqua);

  const mo = u(0.024);
  pat('pMortier', mo, mo,
    `<circle cx="${mo * 0.3}" cy="${mo * 0.35}" r="0.9" fill="#BCB4A4"/><circle cx="${mo * 0.75}" cy="${mo * 0.8}" r="0.7" fill="#C8C0B0"/>`, D.mortier);

  const fz = u(0.03);                             // forme de pente / chape
  pat('pChape', fz, fz,
    `<path d="M 0 ${fz} L ${fz} 0" stroke="#C4BCAC" stroke-width="0.6"/>`, '#EDE8DE');

  p.push(`<linearGradient id="gVerre" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#DCEAEE"/><stop offset="1" stop-color="#BCD2D8"/></linearGradient>`);
  p.push(`<linearGradient id="gAlu" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#565B5F"/><stop offset="1" stop-color="${D.aluD}"/></linearGradient>`);
  return `<defs>${p.join('')}</defs>`;
}

// Reperage : bulle numerotee + ligne de rappel brisee vers le texte
export function callout(n, x, y, tx, ty, label, o = {}) {
  const col = o.color ?? D.ink;
  const mx = o.mid ?? (x + tx) / 2;
  return `<g>
    <path d="M ${x} ${y} L ${mx} ${y} L ${tx} ${ty}" fill="none" stroke="${col}" stroke-width="0.8" opacity="0.7"/>
    <circle cx="${x}" cy="${y}" r="2.6" fill="${col}"/>
    <circle cx="${tx}" cy="${ty}" r="9.5" fill="#FFFFFF" stroke="${col}" stroke-width="1.1"/>
    <text x="${tx}" y="${ty + 3.6}" text-anchor="middle" font-family="Archivo, Arial, sans-serif" font-size="10" font-weight="700" fill="${col}">${n}</text>
  </g>`;
}

// Nomenclature en pied de detail
export function nomenclature(x, y, rows, o = {}) {
  const w = o.w ?? 300, lh = o.lh ?? 14, size = o.size ?? 8.5;
  const out = [`<text x="${x}" y="${y}" font-family="Archivo, Arial, sans-serif" font-size="8.5" font-weight="700" letter-spacing="0.14em" fill="${D.ink}">${o.title ?? 'NOMENCLATURE'}</text>`];
  rows.forEach(([n, t], i) => {
    const yy = y + 18 + i * lh;
    if (n) {
      out.push(`<circle cx="${x + 5}" cy="${yy - 3.2}" r="6.4" fill="none" stroke="${D.dim}" stroke-width="0.9"/>`);
      out.push(`<text x="${x + 5}" y="${yy - 0.4}" text-anchor="middle" font-family="Archivo, Arial, sans-serif" font-size="7.5" font-weight="700" fill="${D.dim}">${n}</text>`);
    }
    out.push(`<text x="${x + 17}" y="${yy}" font-family="Archivo, Arial, sans-serif" font-size="${size}" fill="#4A453C">${t.replace(/&/g, '&amp;').replace(/</g, '&lt;')}</text>`);
  });
  return out.join('');
}

// Titre de detail + echelle
export function detailTitle(x, y, n, t, ech) {
  return `<g>
    <text x="${x}" y="${y}" font-family="Archivo, Arial, sans-serif" font-size="10.5" font-weight="700" letter-spacing="0.16em" fill="${D.ink}">${n} · ${t}</text>
    <text x="${x}" y="${y + 15}" font-family="Archivo, Arial, sans-serif" font-size="8.5" font-weight="600" letter-spacing="0.14em" fill="${D.dim}">${ech}</text>
  </g>`;
}

// Ligne de coupe / axe
export const axe = (x1, y1, x2, y2, c = D.dim) =>
  `<path d="M ${x1} ${y1} L ${x2} ${y2}" stroke="${c}" stroke-width="0.8" stroke-dasharray="14 4 3 4" fill="none"/>`;
