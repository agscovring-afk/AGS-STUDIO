export const FONTS = `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Archivo:wght@400;500;600;700&display=swap">`;

export const BASE_CSS = `
  body { margin: 0; background: #F1EDE5; color: #23211E;
         font-family: 'Archivo', 'Helvetica Neue', Arial, sans-serif;
         -webkit-font-smoothing: antialiased; }
  a { color: #8A6E4C; text-decoration: none; }
  a:hover { color: #5A4832; }
  h1, h2, h3 { margin: 0; font-family: 'Space Grotesk', 'Helvetica Neue', Arial, sans-serif; font-weight: 600; }
  .eyebrow { font-size: 10px; font-weight: 600; letter-spacing: .28em; color: #8C8478; text-transform: uppercase; }
  .rule { height: 1px; background: #D3C9B7; }
`;

export function page({ body, props, css = '' }) {
  const script = props
    ? `\n<script data-dc-script data-props='${props}'>\nclass Component extends DCLogic {${props.includes('"editor"') ? `
  renderVals() {
    return {
      wall: this.props.wall ?? '#E8E0D2',
      accent: this.props.accent ?? '#8A6E4C',
    };
  }` : ''}}\n</script>`
    : '';
  return `<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  ${FONTS}
  <style>${BASE_CSS}${css}</style>
</helmet>
${body}
</x-dc>${script}
</body>
</html>
`;
}

// Bandeau de titre commun a toutes les planches
export function header({ w, kicker, title, sub, right }) {
  return `<div style="display: flex; align-items: flex-end; justify-content: space-between; gap: 40px; padding: 36px 44px 20px;">
  <div style="max-width: ${Math.round(w * 0.62)}px">
    <div class="eyebrow">${kicker}</div>
    <h1 style="font-size: 34px; line-height: 1.04; letter-spacing: -0.018em; margin-top: 13px">${title}</h1>
    <div style="font-size: 13.5px; line-height: 1.5; color: #6E6659; margin-top: 9px">${sub}</div>
  </div>
  <div style="text-align: right; font-size: 10px; font-weight: 600; letter-spacing: .16em; color: #8C8478; line-height: 2.1; white-space: nowrap">${right}</div>
</div>
<div class="rule" style="margin: 0 44px"></div>`;
}
