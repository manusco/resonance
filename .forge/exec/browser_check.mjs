#!/usr/bin/env node
/*
 * Resonance execution surface - real browser grounding via Playwright.
 *
 * /design and /test can describe a UI, but they cannot SEE it. This opens a real
 * headless browser, loads a URL, and reports what actually rendered: the title,
 * console and page errors, whether required elements exist, and a screenshot on
 * disk. That turns "looks right" into "verified in a browser."
 *
 * Playwright is not a Resonance dependency (clone-and-go stays light). This uses
 * whatever Playwright the target PROJECT has. If it is absent, the check degrades
 * with a clear one-line install hint instead of crashing.
 *
 * Usage:
 *   node .forge/exec/browser_check.mjs <url> [--assert "css"]... [--shot out.png] [--json]
 * Exit: 0 healthy, 1 a problem rendered, 3 Playwright not available.
 */

function parseArgs(argv) {
  const a = { url: null, asserts: [], shot: null, json: false };
  for (let i = 0; i < argv.length; i++) {
    const t = argv[i];
    if (t === "--assert") a.asserts.push(argv[++i]);
    else if (t === "--shot") a.shot = argv[++i];
    else if (t === "--json") a.json = true;
    else if (!a.url) a.url = t;
  }
  return a;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.url) {
    console.error("usage: node browser_check.mjs <url> [--assert css]... [--shot out.png] [--json]");
    process.exit(2);
  }

  let pw;
  try {
    pw = await import("playwright");
  } catch {
    const msg = "Playwright is not installed in this project. Run: npm i -D playwright && npx playwright install chromium";
    console.log(args.json ? JSON.stringify({ ok: false, reason: msg }) : msg);
    process.exit(3);
  }

  const consoleErrors = [];
  let browser;
  try {
    browser = await pw.chromium.launch();
    const page = await browser.newPage();
    page.on("console", (m) => { if (m.type() === "error") consoleErrors.push(m.text()); });
    page.on("pageerror", (e) => consoleErrors.push(String(e)));

    const resp = await page.goto(args.url, { waitUntil: "load", timeout: 30000 });
    const status = resp ? resp.status() : null;            // file:// yields null
    const httpOk = resp ? resp.ok() : true;
    const title = await page.title();

    const assertions = [];
    for (const sel of args.asserts) {
      const found = (await page.locator(sel).count()) > 0;
      assertions.push({ selector: sel, found });
    }
    let screenshot = null;
    if (args.shot) { await page.screenshot({ path: args.shot, fullPage: true }); screenshot = args.shot; }

    const ok = httpOk && consoleErrors.length === 0 && assertions.every((a) => a.found);
    const result = { ok, url: args.url, status, title, consoleErrors, assertions, screenshot };

    if (args.json) {
      console.log(JSON.stringify(result, null, 2));
    } else {
      console.log(`browser check: ${args.url}`);
      console.log(`  ${ok ? "OK" : "PROBLEM"}  status=${status ?? "n/a"}  title=${JSON.stringify(title)}`);
      if (consoleErrors.length) console.log(`  console errors (${consoleErrors.length}): ${consoleErrors.slice(0, 3).join(" | ")}`);
      for (const a of assertions) console.log(`  ${a.found ? "found  " : "MISSING"} ${a.selector}`);
      if (screenshot) console.log(`  screenshot: ${screenshot}`);
    }
    process.exit(ok ? 0 : 1);
  } finally {
    if (browser) await browser.close();
  }
}

main().catch((e) => { console.error("browser_check error:", e.message); process.exit(1); });
