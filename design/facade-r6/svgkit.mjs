// Petites primitives de dessin technique partagees par les planches.
export const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

export function txt(x, y, s, o = {}) {
  const a = {
    'font-family': o.mono ? "'Archivo', 'Helvetica Neue', Arial, sans-serif" : "'Archivo', 'Helvetica Neue', Arial, sans-serif",
    'font-size': o.size ?? 11,
    'font-weight': o.weight ?? 400,
    fill: o.fill ?? '#5F594E',
    'text-anchor': o.anchor ?? 'middle',
    'letter-spacing': o.ls ?? '0.02em',
  };
  const extra = o.transform ? ` transform="${o.transform}"` : '';
  return `<text x="${x}" y="${y}" ${Object.entries(a).map(([k, v]) => `${k}="${v}"`).join(' ')}${extra}>${esc(s)}</text>`;
}

// Cote horizontale avec traits d'attache et fleches obliques
export function dimH(x1, x2, y, label, o = {}) {
  const c = o.color ?? '#8C8478';
  const t = o.tickUp ?? 6, b = o.tickDown ?? 6;
  const arrow = (x) => `<path d="M ${x - 4.5} ${y + 4.5} L ${x + 4.5} ${y - 4.5}" stroke="${c}" stroke-width="1"/>`;
  return `<g>
    <line x1="${x1}" y1="${y - t}" x2="${x1}" y2="${y + b}" stroke="${c}" stroke-width="0.7"/>
    <line x1="${x2}" y1="${y - t}" x2="${x2}" y2="${y + b}" stroke="${c}" stroke-width="0.7"/>
    <line x1="${x1}" y1="${y}" x2="${x2}" y2="${y}" stroke="${c}" stroke-width="0.7"/>
    ${arrow(x1)}${arrow(x2)}
    ${txt((x1 + x2) / 2, y - 6, label, { size: o.size ?? 11, fill: o.textFill ?? '#3A352E', weight: o.weight ?? 500 })}
  </g>`;
}

// Cote verticale
export function dimV(y1, y2, x, label, o = {}) {
  const c = o.color ?? '#8C8478';
  const arrow = (y) => `<path d="M ${x - 4.5} ${y + 4.5} L ${x + 4.5} ${y - 4.5}" stroke="${c}" stroke-width="1"/>`;
  return `<g>
    <line x1="${x - 6}" y1="${y1}" x2="${x + 6}" y2="${y1}" stroke="${c}" stroke-width="0.7"/>
    <line x1="${x - 6}" y1="${y2}" x2="${x + 6}" y2="${y2}" stroke="${c}" stroke-width="0.7"/>
    <line x1="${x}" y1="${y1}" x2="${x}" y2="${y2}" stroke="${c}" stroke-width="0.7"/>
    ${arrow(y1)}${arrow(y2)}
    ${txt(0, 0, label, { size: o.size ?? 11, fill: '#3A352E', weight: 500, transform: `translate(${x - 5} ${(y1 + y2) / 2}) rotate(-90)` })}
  </g>`;
}

// Reperage de niveau : triangle + altitude + intitule
export function levelMark(x, y, alt, label, o = {}) {
  const c = o.color ?? '#2B2724';
  const w = o.lead ?? 26;
  return `<g>
    <line x1="${x - w}" y1="${y}" x2="${x + 150}" y2="${y}" stroke="${c}" stroke-width="0.6" stroke-dasharray="1 3" opacity="0.55"/>
    <path d="M ${x} ${y} l 6 9 l -12 0 z" fill="${c}"/>
    ${txt(x + 14, y - 5, alt, { size: 11.5, weight: 600, fill: '#23211E', anchor: 'start' })}
    ${txt(x + 14, y + 11, label, { size: 9.5, weight: 500, fill: '#8C8478', anchor: 'start', ls: '0.08em' })}
  </g>`;
}

// Pastille numerotee de renvoi + ligne de rappel
export function callout(n, cx, cy, tx, ty, o = {}) {
  const c = o.color ?? '#23211E';
  return `<g>
    <line x1="${tx}" y1="${ty}" x2="${cx}" y2="${cy}" stroke="${c}" stroke-width="0.7"/>
    <circle cx="${tx}" cy="${ty}" r="2" fill="${c}"/>
    <circle cx="${cx}" cy="${cy}" r="10.5" fill="#FFFFFF" stroke="${c}" stroke-width="1"/>
    ${txt(cx, cy + 4, String(n), { size: 11, weight: 700, fill: c })}
  </g>`;
}

// Hachure de terrain
export function ground(x1, x2, y, o = {}) {
  const c = o.color ?? '#8C8478';
  let h = '';
  for (let x = x1; x <= x2; x += 11) h += `<line x1="${x}" y1="${y}" x2="${x - 9}" y2="${y + 11}" stroke="${c}" stroke-width="0.7" opacity="0.7"/>`;
  return `<g><line x1="${x1 - 14}" y1="${y}" x2="${x2 + 14}" y2="${y}" stroke="#2B2724" stroke-width="1.6"/>${h}</g>`;
}
