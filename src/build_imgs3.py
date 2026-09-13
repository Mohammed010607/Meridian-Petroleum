# Final service-page photographs. Picks are given as "<set>:<index>" against
# the candidate lists, so the choice is auditable and easy to change.
import json, urllib.parse, urllib.request, io, base64, sys
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
UA = {"User-Agent": "MeridianDemoSite/1.0 (educational demo site)"}

SETS = {"me": json.load(open("cands_me.json", encoding="utf-8")),
        "ref": json.load(open("cands_ref.json", encoding="utf-8"))}
for tag, f in (("c2", "cands2.json"), ("p", "pool.json")):
    try:
        SETS[tag] = json.load(open(f, encoding="utf-8"))
    except Exception:
        SETS[tag] = []

# id, candidate, width, height, quality, vertical crop bias
PICK = [
 ("svc_ep_1",  "me:0",   760, 500, 70, .42),   # loading jetty and tanker, Gulf
 ("svc_ep_2",  "me:1",  1140, 400, 68, .46),   # the same terminal, wide
 ("svc_gas_1", "me:13",  760, 500, 70, .45),   # LNG carrier under way
 ("svc_gas_2", "me:14", 1140, 400, 68, .46),   # LNG carrier at her berth
 ("svc_ref_1", "p:65",   760, 500, 70, .48),   # Duqm refinery, Oman
 ("svc_ref_2", "ref:1", 1140, 400, 68, .50),   # Ruwais refining, golden hour
 ("svc_mid_1", "p:66",   760, 500, 70, .45),   # Ras Markaz storage park, Oman
 ("svc_mid_2", "me:27", 1140, 400, 68, .22),   # port cranes, Sohar - crop high
 ("svc_tr_1",  "me:48",  760, 500, 70, .45),   # solar array
 ("svc_tr_2",  "p:119", 1140, 400, 68, .45),   # desert photovoltaic plant
]

def fetch(title, width):
    u = ("https://commons.wikimedia.org/wiki/Special:FilePath/"
         + urllib.parse.quote(title.replace(" ", "_")) + "?width=" + str(width))
    return Image.open(io.BytesIO(urllib.request.urlopen(
        urllib.request.Request(u, headers=UA), timeout=180).read())).convert("RGB")

def cover(im, W, H, bias):
    sw, sh = im.size; tr = W / H; sr = sw / sh
    if sr > tr:
        nw = int(sh * tr); x = (sw - nw) // 2; im = im.crop((x, 0, x + nw, sh))
    else:
        nh = int(sw / tr); y = int((sh - nh) * bias); im = im.crop((0, y, sw, y + nh))
    return im.resize((W, H), Image.LANCZOS)

out = json.load(open("imgs.json"))
credits = json.load(open("credits.json", encoding="utf-8"))
for pid, ref, W, H, q, bias in PICK:
    tag, idx = ref.split(":"); it = SETS[tag][int(idx)]
    im = cover(fetch(it["title"], W + 600), W, H, bias)
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
    b = buf.getvalue()
    out[pid] = "data:image/jpeg;base64," + base64.b64encode(b).decode()
    credits = [c for c in credits if c["id"] != pid]
    credits.append({"id": pid, "title": it["title"], "lic": it["lic"],
                    "artist": it.get("artist", "")})
    print("%-11s %4dx%3d %6.1fKB  %s" % (pid, W, H, len(b) / 1024, it["title"][:50]))

json.dump(out, open("imgs.json", "w"), indent=0)
json.dump(credits, open("credits.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\nimgs.json %.2f MB" % (sum(len(v) for v in out.values()) / 1024 / 1024))

rows = "".join('<figure><img src="%s" alt=""><figcaption>%s</figcaption></figure>'
               % (out[p[0]], p[0]) for p in PICK)
io.open("../_check.html", "w", encoding="utf-8").write(
  "<style>body{background:#111;margin:0;font:12px system-ui;color:#eee}"
  "main{display:grid;grid-template-columns:repeat(2,1fr);gap:5px;padding:5px}"
  "figure{margin:0}img{width:100%;display:block}figcaption{padding:3px}</style><main>"
  + rows + "</main>")
print("check sheet: _check.html")
