/**
 * Embeds build-time env into static HTML.
 * VITE_/REACT_APP_ style: value must be present at `docker build` via --build-arg.
 */
const fs = require('fs');
const path = require('path');

const greeting = process.env.APP_GREETING || '(not set at build time)';
const clientId = process.env.CLIENT_ID || 'unknown';

const templatePath = path.join(__dirname, '..', 'public', 'index.template.html');
const outPath = path.join(__dirname, '..', 'public', 'index.html');

let html = fs.readFileSync(templatePath, 'utf8');
html = html
  .replaceAll('__APP_GREETING__', greeting)
  .replaceAll('__CLIENT_ID__', clientId);

fs.writeFileSync(outPath, html);
console.log('Built index.html with APP_GREETING=%s CLIENT_ID=%s', greeting, clientId);
