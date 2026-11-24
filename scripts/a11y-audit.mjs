/**
 * Accessibility gate for a Vanderbilt FLH Learning Library course.
 * Bundled with the vu-course-builder skill. Copy it into the course as
 * tools/a11y-audit.mjs.
 *
 *   npm i -D playwright @axe-core/playwright
 *   npx playwright install chromium
 *   python3 -m http.server 8765        # from the course root
 *   node tools/a11y-audit.mjs
 *
 * Book mode shows one page at a time, so a single scan of the document only
 * sees page one. This script walks the pager through EVERY page of every
 * edition it finds, at 1440x900 and 320x640. It runs axe-core (WCAG 2.0/2.1/
 * 2.2 A and AA) on each page and also checks these:
 *   - no horizontal scroll at any width, plus a 200% zoom pass
 *   - no running animations with prefers-reduced-motion: reduce
 *   - no console errors (proxy, net:: and favicon noise ignored)
 * Any critical or serious axe violation fails the gate (exit 1).
 *
 * Env:
 *   BASE         server root (default http://localhost:8765)
 *   EDITIONS     comma list of name=path (default: self-paced=/,classroom=/classroom/,facilitator=/facilitator/)
 *                editions that return 404 are skipped, so a course without a
 *                classroom or facilitator edition still runs
 *   CHROME_PATH  use a specific Chromium binary (e.g. /opt/pw-browsers/chromium in the cloud image)
 */
import { chromium } from 'playwright';
import { AxeBuilder } from '@axe-core/playwright';

const BASE = (process.env.BASE || 'http://localhost:8765').replace(/\/$/, '');
const EDITIONS = (process.env.EDITIONS ||
  'self-paced=/,classroom=/classroom/,facilitator=/facilitator/')
  .split(',').map((s) => { const [name, path] = s.split('='); return { name, url: BASE + path }; });
const VIEWPORTS = [
  { name: '1440x900', width: 1440, height: 900 },
  { name: '320x640', width: 320, height: 640 },
];
const TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'];
const NOISE = /TUNNEL|net::|favicon/i;

const problems = [];
let scans = 0;

const launch = { args: ['--no-sandbox'] };
if (process.env.CHROME_PATH) launch.executablePath = process.env.CHROME_PATH;
const browser = await chromium.launch(launch);

async function reachable(url) {
  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  try {
    const r = await page.goto(url, { waitUntil: 'domcontentloaded' });
    return !!r && r.ok();
  } catch { return false; } finally { await ctx.close(); }
}

async function overflow(page) {
  return page.evaluate(() =>
    document.documentElement.scrollWidth - document.documentElement.clientWidth);
}

/* Every page the pager built, as { i, key, label }. Returns [] when the
   course has no pager (scroll layout), and the caller scans once. */
async function listPages(page) {
  return page.evaluate(() => {
    if (!window.chartPager || !document.documentElement.classList.contains('paged')) return [];
    return Array.from(document.querySelectorAll('#main > .page')).map((el, i) => ({
      i, key: el.getAttribute('data-sec') || '', label: el.getAttribute('data-label') || '',
    }));
  });
}

async function turnTo(page, i) {
  await page.evaluate((n) => window.chartPager.go(n), i);
  await page.waitForTimeout(450);   // page-turn animation is 420ms
}

async function axe(page, where) {
  scans++;
  const results = await new AxeBuilder({ page }).withTags(TAGS).analyze();
  for (const v of results.violations) {
    if (v.impact !== 'critical' && v.impact !== 'serious') continue;
    problems.push(`${where}: [${v.impact}] ${v.id} - ${v.help} (${v.nodes.length} node(s))\n      ${v.nodes[0]?.target?.join(' ')}`);
  }
}

const live = [];
for (const ed of EDITIONS) {
  if (await reachable(ed.url)) live.push(ed);
  else console.log(`skip ${ed.name}: ${ed.url} not reachable`);
}
if (!live.length) {
  console.log(`A11Y GATE FAILED: nothing reachable at ${BASE}. Start the server from the course root.`);
  process.exit(1);
}

for (const ed of live) {
  for (const vp of VIEWPORTS) {
    const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height } });
    const page = await ctx.newPage();
    const errors = [];
    page.on('console', (m) => { if (m.type() === 'error' && !NOISE.test(m.text())) errors.push(m.text()); });
    page.on('pageerror', (e) => errors.push('pageerror: ' + e.message));

    // start clean so a saved page or route from an earlier run does not skew it
    await page.goto(ed.url, { waitUntil: 'networkidle' });
    await page.evaluate(() => { try { localStorage.clear(); } catch {} });
    await page.goto(ed.url, { waitUntil: 'networkidle' });

    const pages = await listPages(page);
    if (!pages.length) {
      problems.push(`${ed.name} ${vp.name}: pager did not build (no #main > .page). Book mode is required; scanned the scroll layout only.`);
      await axe(page, `${ed.name} ${vp.name} (scroll)`);
    }
    for (const p of pages) {
      await turnTo(page, p.i);
      const where = `${ed.name} ${vp.name} #p/${p.key} "${p.label}"`;
      await axe(page, where);
      const o = await overflow(page);
      if (o > 1) problems.push(`${where}: page scrolls horizontally by ${o}px`);
    }
    if (errors.length) problems.push(`${ed.name} ${vp.name}: console errors -> ${errors.slice(0, 3).join(' | ')}`);
    await ctx.close();
  }
}

// facilitator printable guide is a document: one scan per viewport
if (live.some((e) => e.name === 'facilitator') && await reachable(`${BASE}/facilitator/guide.html`)) {
  for (const vp of VIEWPORTS) {
    const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height } });
    const page = await ctx.newPage();
    await page.goto(`${BASE}/facilitator/guide.html`, { waitUntil: 'networkidle' });
    await axe(page, `guide ${vp.name}`);
    await ctx.close();
  }
}

// 200% zoom: a half-width viewport at desktop height, every page of the first edition
{
  const ed = live[0];
  const ctx = await browser.newContext({ viewport: { width: 720, height: 450 } });
  const page = await ctx.newPage();
  await page.goto(ed.url, { waitUntil: 'networkidle' });
  for (const p of await listPages(page)) {
    await turnTo(page, p.i);
    const o = await overflow(page);
    if (o > 1) problems.push(`200% zoom #p/${p.key} "${p.label}": page scrolls horizontally by ${o}px`);
  }
  await ctx.close();
}

// reduced motion: nothing may keep animating (marquee, pulses, hero video, flips)
{
  const ed = live[0];
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' });
  const page = await ctx.newPage();
  await page.goto(ed.url, { waitUntil: 'networkidle' });
  for (const p of await listPages(page)) {
    await turnTo(page, p.i);
    const running = await page.evaluate(() => {
      const anims = document.getAnimations ? document.getAnimations() : [];
      const moving = anims.filter((a) => a.playState === 'running' &&
        (a.effect?.getTiming?.().iterations === Infinity || (a.effect?.getTiming?.().duration || 0) > 400));
      const vids = Array.from(document.querySelectorAll('video'))
        .filter((v) => !v.paused && getComputedStyle(v).display !== 'none');
      return moving.length + vids.length;
    });
    if (running) problems.push(`reduced motion #p/${p.key} "${p.label}": ${running} animation(s) or video(s) still running`);
  }
  await ctx.close();
}

await browser.close();

console.log(`axe scans run: ${scans} across ${live.map((e) => e.name).join(', ')}`);
if (problems.length) {
  console.log(`\nA11Y GATE FAILED: ${problems.length} problem(s)\n`);
  problems.forEach((p) => console.log('  - ' + p));
  process.exit(1);
}
console.log('A11Y GATE PASSED: zero critical or serious violations, no horizontal scroll, reduced motion respected.');
