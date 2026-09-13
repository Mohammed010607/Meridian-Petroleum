# Meridian Petroleum

Corporate website for Meridian Petroleum SAOG — a Muscat-headquartered
integrated oil and gas company operating across six Gulf countries.

Demonstration site: the company is fictional and all figures are sample data.

---

## Viewing it

Open `index.html` in any browser. That is the whole site — no server, no build
step, no install. It also works straight off the filesystem (`file://`).

To serve it locally instead:

```bash
python -m http.server 8000
# then open http://localhost:8000
```

## Structure

```
index.html              the built site — this is what you deploy
robots.txt
src/
  template.html         THE SOURCE. Edit this, not index.html
  imgs.json             the 11 photographs, base64-encoded
  credits.json          photo attribution metadata
  cands_me.json         photo search results (Gulf region)
  cands_ref.json        photo search results (refineries)
  build.py              template.html + imgs.json -> meridian-petroleum.html
  asciify.py            escapes non-ASCII so encoding can never break it
  make_deploy.py        wraps the build in <!doctype>/<html>/<head> -> index.html
  build_imgs.py         re-fetches, crops and re-encodes the photographs
tools/
  type-options.html     typeface comparison tool — open it in a browser
```

`index.html` is generated. Any edit made directly to it is lost on the next
build. Change `src/template.html` instead.

## Building

Requires Python 3 (and Pillow only if you re-run `build_imgs.py`).

```bash
cd src
python build.py        # inject the photographs
python asciify.py      # make the output encoding-independent
python make_deploy.py  # wrap it and write ../index.html
```

`make_deploy.py` prints a checklist and writes to the repo root, so it works
from any clone on any machine.

## Replacing the photographs

Photo slots live in the `IMG` block near the top of the `<script>` in
`src/template.html`. Each value can be a filename (`"photo.jpg"`) or an inline
`data:` URI. Match the crop ratios:

| Slot | Size |
| --- | --- |
| `hero_upstream` `hero_refining` `hero_lng` `hero_terminal` `hero_shipping` | 1760 × 990 |
| `card_ep` `card_gas` `card_refining` `card_midstream` `card_transition` | 880 × 570 |
| `band_plant` | 1600 × 620 |

The current photographs are freely-licensed works, several under CC BY-SA.
The site carries no credits block, so **keep this repository private until they
are replaced with your own images.**

## How it works

- Single file. All CSS, JavaScript and imagery are inline; the only outbound
  request is to Google Fonts.
- Hash routing (`#/services`, `#/contact`). The path after `#` never reaches
  the server, so there are no rewrite rules and no 404 on refresh — it runs on
  any static host, or none.
- Responsive down to 320 px, with 44 px touch targets on phones and tablets.
- Light and dark themes follow the reader's system setting.
