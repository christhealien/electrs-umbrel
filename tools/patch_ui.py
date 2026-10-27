#!/usr/bin/env python3
"""Apply this repo's theme to a checkout of retropex/umbrel-electrs (the Electrs connection page).  patch_ui.py UPSTREAM_DIR
Adds overlay/ui/blake2b-theme.css (loaded after the app's own styles), the icon and favicon, and a new page title.
Anchors are exact; a missing one stops the build rather than shipping a half-themed page."""
import os, shutil, sys

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
    for b in bad:
        print("FAIL ", b)
    if bad:
        return 2
    if "blake2b-theme.css" not in s:
        s = s.replace(anchor, anchor + '\nimport "./styles/blake2b-theme.css";')
        open(main_js, "w", encoding="utf-8").write(s)
    open(html, "w", encoding="utf-8").write(h.replace("<title>Electrs — Umbrel</title>", "<title>Electrs</title>"))
    ui = os.path.join(HERE, "overlay/ui")
    shutil.copy(os.path.join(ui, "blake2b-theme.css"), os.path.join(up, F + "src/styles/blake2b-theme.css"))
    shutil.copy(os.path.join(ui, "icon.svg"), os.path.join(up, F + "src/assets/icon.svg"))
    shutil.copy(os.path.join(ui, "favicon.png"), os.path.join(up, F + "public/favicon.png"))
    print("OK  themed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
