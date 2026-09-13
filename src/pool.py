# Build a pool of service-page photograph candidates from a short list of
# categories that are known to exist, paced so Commons does not rate-limit.
import json, urllib.parse, urllib.request, io, sys, re, base64, time
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
UA = {"User-Agent": "MeridianDemoSite/1.0 (educational demo site)"}
API = "https://commons.wikimedia.org/w/api.php"

CATS = [
 ("ep",  "Category:Oil platforms"),
 ("ep",  "Category:Jackup rigs"),
 ("ep",  "Category:Oil wells"),
 ("ep",  "Category:Petroleum industry in Oman"),
 ("ref", "Category:Oil refineries in Saudi Arabia"),
 ("ref", "Category:Oil refineries"),
 ("mid", "Category:Oil storage tanks"),
 ("mid", "Category:Oil tankers"),
 ("tr",  "Category:Photovoltaic power stations"),
 ("tr",  "Category:Solar thermal power stations"),
 ("gas", "Category:LNG terminals"),
]
OK_LIC = re.compile(r"(cc[ -]by|cc0|public domain)", re.I)
SKIP = re.compile(r"(map|diagram|logo|chart|graph|poster|schematic|icon|banner|seal|flag|model"
                  r"|drawing|plan|portrait|protest|damage|attack|explosion|spill|fire|wreck"
                  r"|navy|uss |sailor|marine|soldier|military|memorial|museum|abandoned|rust)", re.I)

def api(params, tries=5):
    params.update({"format": "json", "formatversion": "2"})
    url = API + "?" + urllib.parse.urlencode(params)
    for a in range(tries):
        try:
            return json.load(urllib.request.urlopen(
                urllib.request.Request(url, headers=UA), timeout=120))
        except Exception as e:
            if a == tries - 1: raise
            time.sleep(4 * (a + 1))

seen, pool = set(), []
for group, cat in CATS:
    try:
        d = api({"action": "query", "generator": "categorymembers", "gcmtitle": cat,
                 "gcmtype": "file", "gcmlimit": "45", "prop": "imageinfo",
                 "iiprop": "url|size|extmetadata", "iiurlwidth": "380"})
    except Exception as e:
        print("  ! %s: %s" % (cat, e)); continue
    pages = d.get("query", {}).get("pages", [])
    kept = 0
    for pg in pages:
        ii = (pg.get("imageinfo") or [{}])[0]
        t = pg.get("title", "")
        if t in seen or not ii.get("thumburl"): continue
        if not re.search(r"\.jpe?g$", t, re.I) or SKIP.search(t): continue
        w, h = ii.get("width", 0), ii.get("height", 1)
        if w < 1300 or w / h < 1.2: continue
        md = ii.get("extmetadata", {})
        lic = (md.get("LicenseShortName", {}) or {}).get("value", "")
        if not OK_LIC.search(lic): continue
        artist = re.sub("<[^>]+>", "", (md.get("Artist", {}) or {}).get("value", ""))[:60]
        seen.add(t); kept += 1
        pool.append({"group": group, "title": t[5:], "lic": lic, "artist": artist.strip(),
                     "thumb": ii["thumburl"], "w": w, "h": h})
    print("%-4s %-44s %2d of %2d" % (group, cat[9:53], kept, len(pages)))
    time.sleep(1.6)

json.dump(pool, open("pool.json", "w", encoding="utf-8"), ensure_ascii=False)
print("\n%d candidates" % len(pool))

cells = []
for i, c in enumerate(pool):
    try:
        im = Image.open(io.BytesIO(urllib.request.urlopen(
            urllib.request.Request(c["thumb"], headers=UA), timeout=45).read())).convert("RGB")
        im.thumbnail((290, 290), Image.LANCZOS)
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=56)
        b64 = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception:
        b64 = ""
    cells.append('<figure><img src="%s" alt=""><figcaption><b>%d %s</b> %s</figcaption></figure>'
                 % (b64, i, c["group"], c["title"][:34]))
io.open("../_pool.html", "w", encoding="utf-8").write(
  "<style>body{background:#111;margin:0;font:10px system-ui;color:#ccc}"
  "main{display:grid;grid-template-columns:repeat(6,1fr);gap:3px;padding:3px}"
  "figure{margin:0;background:#1c1c1c}img{width:100%;display:block;aspect-ratio:3/2;object-fit:cover}"
  "figcaption{padding:2px 3px;line-height:1.2}b{color:#f0b34a}</style><main>" + "".join(cells) + "</main>")
print("pool sheet: _pool.html")
