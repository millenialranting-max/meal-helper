#!/usr/bin/env python3
"""Render an HTML file to an A4 PDF and PNG previews of every page.

Usage: python render_pdf.py tutorial.html Output.pdf
Tries Node Playwright, then Python Playwright, then a headless Chromium/Chrome binary.
Prints the page count; writes Output-p1.png, -p2.png … (if pypdfium2 is available) to check layout.
"""
import os, shutil, subprocess, sys, glob, tempfile

html, pdf = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])

NODE = """
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://%s', { waitUntil: 'networkidle' });
  await p.pdf({ path: '%s', format: 'A4', printBackground: true, preferCSSPageSize: true });
  await b.close(); })();
"""

def node_playwright():
    if not shutil.which("node"):
        return False
    npm_root = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
        f.write(NODE % (html, pdf))
    env = dict(os.environ, NODE_PATH=npm_root)
    return subprocess.run(["node", f.name], env=env, capture_output=True).returncode == 0 and os.path.exists(pdf)

def py_playwright():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return False
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(); pg = b.new_page()
            pg.goto("file://" + html, wait_until="networkidle")
            pg.pdf(path=pdf, format="A4", print_background=True, prefer_css_page_size=True); b.close()
        return os.path.exists(pdf)
    except Exception:
        return False

def chrome_binary():
    cands = [shutil.which(x) for x in ["chromium", "chromium-browser", "google-chrome", "chrome"]]
    cands += glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome")
    cands += ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
    for c in [c for c in cands if c and os.path.exists(c)]:
        r = subprocess.run([c, "--headless", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer",
                            f"--print-to-pdf={pdf}", "file://" + html], capture_output=True)
        if os.path.exists(pdf):
            return True
    return False

for fn in (node_playwright, py_playwright, chrome_binary):
    if fn():
        break
else:
    sys.exit("Could not render: install Playwright (npm i -g playwright or pip install playwright) or Chrome.")

try:
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(pdf)
    print(f"Pages: {len(doc)}")
    base = pdf[:-4]
    for i in range(len(doc)):
        doc[i].render(scale=1).to_pil().save(f"{base}-p{i+1}.png")
    print(f"Previews: {base}-p1.png …")
except Exception:
    print(f"PDF written: {pdf} (install pypdfium2 + pillow for page previews)")
