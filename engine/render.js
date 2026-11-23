// FIXED renderer. Usage: node render.js <build_dir>   (reads <build_dir>/deck.html, writes <build_dir>/deck.pdf)
// Waits for fonts and images, fails on any broken image, prints a 1280x720 page per <section>.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const dir = path.resolve(process.argv[2] || '.');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  await page.goto('file://' + path.join(dir, 'deck.html'), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(async () => {
    await Promise.all([...document.images].map(img => img.complete && img.naturalWidth ? null :
      new Promise((res, rej) => { img.onload = res; img.onerror = () => rej(new Error('img failed: ' + img.src)); })));
  });
  const broken = await page.evaluate(() => [...document.images].filter(i => !i.naturalWidth).map(i => i.src));
  if (broken.length) { console.error('broken images', broken); process.exit(1); }
  await page.pdf({ path: path.join(dir, 'deck.pdf'), printBackground: true, preferCSSPageSize: true });
  console.log('wrote', path.join(dir, 'deck.pdf'));
  await browser.close();
})();
