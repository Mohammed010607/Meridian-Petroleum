# Candidate colour schemes for the site, with a WCAG contrast check on every
# text/ground pair that actually occurs in the layout.
import io, sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

S = {}
def scheme(key, name, tag, desc, **kw): S[key] = dict(name=name, tag=tag, desc=desc, **kw)

scheme("meridian","Meridian","In use now",
 "Deep petroleum slate with a brass accent. Warm, industrial and deliberately understated.",
 deep="#0D181D",deep2="#16262D",deepLine="#2B3C44",onDeep="#F2F0EB",onDeepMuted="#A5B1B5",accentBright="#D99B2E",
 paper="#F6F5F2",surface="#FFFFFF",surface2="#EDEAE3",ink="#111E23",body="#3C484D",muted="#6C787C",
 line="#DBD7CF",lineSoft="#E6E2DA",accent="#A96C12",second="#1C5C69")

scheme("graphite","Graphite","Industrial",
 "Near-black charcoal with safety orange. The hardest, most plant-floor option here.",
 deep="#131313",deep2="#1F1F1F",deepLine="#343434",onDeep="#F2F2F0",onDeepMuted="#AAAAA7",accentBright="#FF8A3D",
 paper="#F5F4F2",surface="#FFFFFF",surface2="#EAE8E5",ink="#17171A",body="#414144",muted="#6E6E71",
 line="#D9D7D3",lineSoft="#E6E4E1",accent="#B54A06",second="#4A5B66")

scheme("navy","Navy","Maritime",
 "Deep navy with warm gold. The most conventionally corporate, and the most shipping-adjacent.",
 deep="#0A1B2E",deep2="#12283F",deepLine="#244056",onDeep="#EFF2F6",onDeepMuted="#A3B3C2",accentBright="#E4AE42",
 paper="#F5F6F8",surface="#FFFFFF",surface2="#E8ECF1",ink="#0E1E30",body="#3A4A5C",muted="#6B7A8A",
 line="#D5DCE4",lineSoft="#E4E9EF",accent="#8A5D07",second="#1F5E7A")

scheme("forest","Forest","Transition",
 "Deep green-black with copper. Leans on the energy-transition side of the business.",
 deep="#0C1A14",deep2="#14281F",deepLine="#254036",onDeep="#EFF3F0",onDeepMuted="#A5B7AD",accentBright="#E0915A",
 paper="#F4F6F3",surface="#FFFFFF",surface2="#E7EBE5",ink="#101F18",body="#3B4A42",muted="#697870",
 line="#D6DDD6",lineSoft="#E5EAE4",accent="#9B5118",second="#2C6B52")

scheme("sand","Sand","Desert",
 "Dark umber with pale gold. The most regional of the set, drawn from desert rather than steel.",
 deep="#1A140D",deep2="#271E14",deepLine="#3E3222",onDeep="#F5F0E7",onDeepMuted="#B9AC98",accentBright="#EDC069",
 paper="#F8F4EC",surface="#FFFDF8",surface2="#EEE7D9",ink="#1E1710",body="#4A4034",muted="#7A6E5E",
 line="#DED4C2",lineSoft="#EBE3D5",accent="#7E5A0C",second="#6A5A2E")

scheme("steel","Steel","Technical",
 "Cool blue-grey with a bright cyan. Reads as instrumentation and control rooms.",
 deep="#101820",deep2="#1B2733",deepLine="#2E3E4D",onDeep="#EEF3F7",onDeepMuted="#A2B2C0",accentBright="#45CBE6",
 paper="#F4F6F8",surface="#FFFFFF",surface2="#E7ECF0",ink="#131C25",body="#3C4854",muted="#6B7885",
 line="#D6DDE3",lineSoft="#E5EAEE",accent="#0B6A82",second="#3D5A73")

scheme("oxblood","Oxblood","Heritage",
 "Deep maroon with brass. Older and more formal, like a company with a long charter.",
 deep="#1B0E11",deep2="#2A171B",deepLine="#43262C",onDeep="#F4EEEF",onDeepMuted="#BAA2A6",accentBright="#DDA945",
 paper="#F7F4F3",surface="#FFFFFF",surface2="#EDE5E4",ink="#1F1113",body="#46383A",muted="#756466",
 line="#DDD2D1",lineSoft="#E9E1E0",accent="#8E2F3A",second="#5C4A3C")

scheme("ink","Ink","Editorial",
 "True near-black and white with one red. The most stripped-back and the most newspaper-like.",
 deep="#0A0A0B",deep2="#171719",deepLine="#2C2C30",onDeep="#F4F4F5",onDeepMuted="#A7A7AC",accentBright="#FF5B4E",
 paper="#F7F7F6",surface="#FFFFFF",surface2="#ECECEA",ink="#121214",body="#3E3E42",muted="#6C6C71",
 line="#D8D8D5",lineSoft="#E6E6E3",accent="#BC2A1F",second="#4B4B52")

scheme("lagoon","Lagoon","Coastal",
 "Deep teal with coral. The freshest of the set, and the least oil-and-gas by convention.",
 deep="#07201F",deep2="#0F2F2D",deepLine="#1E4745",onDeep="#EDF4F3",onDeepMuted="#9FB9B6",accentBright="#F58F66",
 paper="#F3F7F6",surface="#FFFFFF",surface2="#E4EDEB",ink="#0B2220",body="#384B49",muted="#667B78",
 line="#D2DEDC",lineSoft="#E2EBE9",accent="#A8411B",second="#1D6B66")

scheme("dune","Dune","Warm dark",
 "Dark plum-brown with apricot. Softer and dustier than the slate, without going pale.",
 deep="#1A1218",deep2="#281C25",deepLine="#402E3A",onDeep="#F4EFF2",onDeepMuted="#B7A4B0",accentBright="#F3AE70",
 paper="#F8F5F6",surface="#FFFFFF",surface2="#EEE7EA",ink="#1E141A",body="#473B42",muted="#76666E",
 line="#DED2D8",lineSoft="#EAE1E5",accent="#8F5416",second="#6A4A5C")

def lum(h):
    h = h.lstrip("#")
    c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    c = [(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4) for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

def ratio(a, b):
    la, lb = lum(a), lum(b)
    if la < lb: la, lb = lb, la
    return (la + 0.05) / (lb + 0.05)

# (label, fg, bg, minimum) — minimums follow WCAG: 4.5 body text, 3.0 large/UI
PAIRS = [
    ("ink on paper",        "ink",        "paper",   7.0),
    ("body on paper",       "body",       "paper",   4.5),
    ("muted on paper",      "muted",      "paper",   4.5),
    ("accent on paper",     "accent",     "paper",   4.5),
    ("ink on surface",      "ink",        "surface", 7.0),
    ("body on surface",     "body",       "surface", 4.5),
    ("accent on surface",   "accent",     "surface", 4.5),
    ("onDeep on deep",      "onDeep",     "deep",    7.0),
    ("onDeepMuted on deep", "onDeepMuted","deep",    4.5),
    ("accentBright on deep","accentBright","deep",   4.5),
    ("onDeep on deep2",     "onDeep",     "deep2",   7.0),
    ("accentBright on deep2","accentBright","deep2", 4.5),
]

bad = 0
for k, sc in S.items():
    fails = []
    for label, fg, bg, mn in PAIRS:
        r = ratio(sc[fg], sc[bg])
        if r < mn:
            fails.append("%s %.2f (need %.1f)" % (label, r, mn))
    status = "OK" if not fails else "FAIL"
    if fails: bad += 1
    print("%-10s %-12s %s" % (k, sc["tag"], status))
    for f in fails:
        print("      ! " + f)

print("\n%d of %d schemes fully pass" % (len(S) - bad, len(S)))
io.open("schemes.json", "w", encoding="ascii").write(json.dumps(S, separators=(",", ":")))
print("schemes.json written")
