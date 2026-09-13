# Build an SVG map of Meridian's Gulf operations from real country boundaries.
# Downloads Natural Earth 50m outlines, clips to the region, projects to SVG.
import json, io, sys, math, urllib.request
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

URL = ("https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/"
       "geojson/ne_50m_admin_0_countries.geojson")

OPERATE = ["Oman", "United Arab Emirates", "Saudi Arabia", "Qatar", "Kuwait", "Bahrain"]
CONTEXT = ["Iran", "Iraq", "Yemen", "Jordan", "Egypt", "Israel", "Syria", "Turkey", "Eritrea",
           "Djibouti", "Ethiopia", "Somalia", "Sudan", "Pakistan", "Afghanistan", "Kazakhstan",
           "Turkmenistan", "Uzbekistan", "Azerbaijan", "Armenia", "Georgia", "Cyprus", "Lebanon",
           "Kuwait", "India"]

# viewport in degrees
LON0, LON1 = 44.0, 62.5
LAT0, LAT1 = 14.5, 31.5
W = 900.0
MEANLAT = math.radians((LAT0 + LAT1) / 2)
SX = W / (LON1 - LON0)
SY = SX / math.cos(MEANLAT)          # equirectangular with latitude correction
H = (LAT1 - LAT0) * SY

def proj(lon, lat):
    return ((lon - LON0) * SX, (LAT1 - lat) * SY)

def ring_to_path(ring, tol=0.45):
    """project a ring, dropping points closer than tol px (cheap simplification)"""
    pts, last = [], None
    for lon, lat in ring:
        x, y = proj(lon, lat)
        if last is None or abs(x - last[0]) + abs(y - last[1]) > tol:
            pts.append((x, y)); last = (x, y)
    if len(pts) < 3:
        return ""
    d = "M%.1f %.1f" % pts[0] + "".join("L%.1f %.1f" % p for p in pts[1:]) + "Z"
    return d

def geom_paths(geom):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    out = []
    for poly in polys:
        # outer ring only; holes are invisible at this scale
        ring = poly[0]
        # skip polygons entirely outside the viewport
        lons = [p[0] for p in ring]; lats = [p[1] for p in ring]
        if max(lons) < LON0 - 4 or min(lons) > LON1 + 4: continue
        if max(lats) < LAT0 - 4 or min(lats) > LAT1 + 4: continue
        p = ring_to_path(ring)
        if p: out.append(p)
    return out

print("downloading boundaries ...")
req = urllib.request.Request(URL, headers={"User-Agent": "meridian-site/1.0"})
data = json.load(urllib.request.urlopen(req, timeout=180))
print("  %d features" % len(data["features"]))

operate, context, found = {}, [], set()
for f in data["features"]:
    pr = f["properties"]
    name = pr.get("NAME_EN") or pr.get("NAME") or pr.get("ADMIN") or ""
    admin = pr.get("ADMIN") or name
    paths = None
    if admin in OPERATE or name in OPERATE:
        key = admin if admin in OPERATE else name
        paths = geom_paths(f["geometry"])
        if paths:
            operate[key] = paths; found.add(key)
    elif admin in CONTEXT or name in CONTEXT:
        paths = geom_paths(f["geometry"])
        if paths: context.extend(paths)

print("  operating countries found: %d/%d" % (len(found), len(OPERATE)))
for c in OPERATE:
    print("     %-22s %s" % (c, "ok" if c in found else "MISSING"))

SITES = [
 # label,                 lon,   lat,  business slug,             side, label dy
 ("Ras Meridian LNG",    59.38, 22.60, "gas-lng",                 "r",   5),
 ("Masirah Deep",        59.55, 20.35, "exploration-production",  "r",   5),
 ("Duqm refinery",       57.70, 19.67, "refining-petrochemicals", "r",   5),
 ("Sohar refinery",      56.71, 24.34, "refining-petrochemicals", "r",   5),
 ("Ibri solar",          56.30, 23.25, "energy-transition",       "l",  16),
 ("Dhofar wind",         54.10, 17.20, "energy-transition",       "l",   5),
 ("Fujairah terminal",   56.33, 25.28, "pipelines-terminals",     "r",  -8),
 ("Al Hadd field",       54.10, 24.90, "exploration-production",  "l",   5),
 ("Umm Sadr refinery",   51.55, 25.95, "refining-petrochemicals", "r",  -9),
 ("Wadi Sahba gas",      49.00, 24.30, "exploration-production",  "l",  17),
 ("Jubail pipelines",    49.66, 27.01, "pipelines-terminals",     "l",   5),
 ("Mina Al Ahmadi",      48.15, 29.07, "gas-lng",                 "l",  17),
 ("Bahrain storage",     50.55, 26.10, "pipelines-terminals",     "l", -11),
]
sites = []
for label, lon, lat, slug, side, dy in SITES:
    x, y = proj(lon, lat)
    sites.append({"label": label, "x": round(x, 1), "y": round(y, 1),
                  "slug": slug, "side": side, "dy": dy})

# country label anchors
LABELS = [("Saudi Arabia",46.0,22.4),("Oman",56.9,21.0),("U.A.E.",54.9,23.35),
          ("Qatar",51.25,24.75),("Kuwait",46.5,30.1),
          ("Iran",55.0,29.6),("Iraq",45.0,31.0),("Yemen",46.5,15.6)]
labels=[]
for n,lon,lat in LABELS:
    x,y = proj(lon,lat)
    labels.append({"n":n,"x":round(x,1),"y":round(y,1),
                   "op": n not in ("Iran","Iraq","Yemen")})

out = {"w": round(W), "h": round(H),
       "operate": {k: v for k, v in operate.items()},
       "context": context, "sites": sites, "labels": labels}
io.open("map.json", "w", encoding="ascii").write(json.dumps(out, separators=(",", ":")))
print("\nmap.json written  viewBox 0 0 %d %d   %.0f KB"
      % (out["w"], out["h"], len(json.dumps(out)) / 1024))
