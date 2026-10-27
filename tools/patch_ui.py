#!/usr/bin/env python3
"""Apply this repo's theme to a checkout of retropex/umbrel-electrs (the Electrs connection page).  patch_ui.py UPSTREAM_DIR
Adds overlay/ui/blake2b-theme.css (loaded after the app's own styles), the icon and favicon, and a new page title.
Anchors are exact; a missing one stops the build rather than shipping a half-themed page."""
import os, re, shutil, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = "apps/frontend/"


def main():
    if len(sys.argv) != 2:
        print(__doc__); return 2
    up = sys.argv[1]
    main_js = os.path.join(up, F + "src/main.js")
    html = os.path.join(up, F + "public/index.html")
    s = open(main_js, encoding="utf-8").read()
    h = open(html, encoding="utf-8").read()
    anchor = 'import store from "./store";'
    bad = []
    if "blake2b-theme.css" not in s and s.count(anchor) != 1:
        bad.append("src/main.js: expected exactly one %r" % anchor)
    if "<title>Electrs — Umbrel</title>" not in h and "<title>Electrs</title>" not in h:
        bad.append("public/index.html: title not found")
    # the connection page looks for the Electrum server on a fixed port 50001; Horizon's electrs listens on ELECTRUM_PORT (50004)
    el = os.path.join(up, "apps/backend/services/electrs.js")
    es = open(el, encoding="utf-8").read()
    old = 'new ElectrumClient(50001, ELECTRS_HOST, "tcp")'
    new = 'new ElectrumClient(Number(process.env.ELECTRUM_PORT) || 50001, ELECTRS_HOST, "tcp")'
    if new not in es and es.count(old) != 1:
        bad.append("services/electrs.js: expected exactly one %r" % old)
    # drop the "step-by-step instructions" link block (it points at Umbrel's own docs)
    ci = os.path.join(up, F + "src/components/ConnectionInformation.vue")
    cs = open(ci, encoding="utf-8").read()
    cs2 = re.sub(r'\n\s*<div\s+class="mt-12 border-t[^"]*"\s*>.*?Click here</a>\.\s*</p>\s*</div>', "", cs, count=1, flags=re.S)
    if cs2 == cs and "Click here" in cs:
        bad.append("ConnectionInformation.vue: help-link block not found")
    for b in bad:
        print("FAIL ", b)
    if bad:
        return 2
    if cs2 != cs:
        open(ci, "w", encoding="utf-8").write(cs2)
    if new not in es:
        open(el, "w", encoding="utf-8").write(es.replace(old, new))
    if "blake2b-theme.css" not in s:
        s = s.replace(anchor, anchor + '\nimport "./styles/blake2b-theme.css";')
        open(main_js, "w", encoding="utf-8").write(s)
    open(html, "w", encoding="utf-8").write(h.replace("<title>Electrs — Umbrel</title>", "<title>Electrs</title>"))
    ui = os.path.join(HERE, "overlay/ui")
    shutil.copy(os.path.join(ui, "blake2b-theme.css"), os.path.join(up, F + "src/styles/blake2b-theme.css"))
    shutil.copy(os.path.join(ui, "icon.svg"), os.path.join(up, F + "src/assets/icon.svg"))
    shutil.copy(os.path.join(ui, "icon.svg"), os.path.join(up, F + "src/assets/umbrel-qr-icon.svg"))  # the QR centre mark, no purple
    shutil.copy(os.path.join(ui, "favicon.png"), os.path.join(up, F + "public/favicon.png"))
    print("OK  themed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
