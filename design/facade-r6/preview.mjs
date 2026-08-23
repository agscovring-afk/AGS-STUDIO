// Sort le contenu d'un .dc.html en HTML simple, pour controle visuel local.
import { readFileSync, writeFileSync } from 'node:fs';
const src = process.argv[2], out = process.argv[3];
let s = readFileSync(src, 'utf8');
const body = s.slice(s.indexOf('<x-dc>') + 6, s.indexOf('</x-dc>'));
const styleM = body.match(/<style>([\s\S]*?)<\/style>/);
let content = body.replace(/<helmet>[\s\S]*?<\/helmet>/, '');
content = content.replace(/\{\{wall\}\}/g, '#E8E0D2').replace(/\{\{accent\}\}/g, '#8A6E4C');
writeFileSync(out, `<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Archivo:wght@400;500;600;700&display=swap">
<style>${styleM ? styleM[1] : ''}</style></head><body>${content}</body></html>`);
console.log('->', out);
