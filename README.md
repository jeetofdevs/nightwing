# $NIGHTWING — Nightwing Doge on NEAR

Static memecoin site + X/Twitter header. Narrative: the doge who became Batman's partner, then went solo on NEAR.

- `index.html`, `style.css`, `script.js` — the website (no build step; open `index.html` or deploy the folder to any static host such as GitHub Pages, Vercel or Netlify).
- `assets/twitter-banner.png` — X header, 1500×500. `assets/twitter-banner@2x.png` is 3000×1000.
- `tools/make_banner.py` — regenerates the header (`python3 tools/make_banner.py`, needs Pillow).

Before launch, edit the `CONFIG` block at the top of `script.js`: set `launched: true` to switch on the buy buttons (they show "Coming Soon" until then), point `links.buy` at the DEX pair page, and add the contract address. X is set to https://x.com/NightwingOnNear.
Tokenomics numbers in `index.html` are placeholders — change them to match the real token.
