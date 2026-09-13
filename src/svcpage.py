# Service detail pages: two photographs each, one capability fewer, and the
# glossary notes cut to a single sentence.
import io, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = "template.html"
s = io.open(p, encoding="utf-8").read()
E = []
def sub(a, b): E.append((a, b))

# --- picture slots on each service -------------------------------------
for slug, key in [("exploration-production", "ep"), ("gas-lng", "gas"),
                  ("refining-petrochemicals", "ref"), ("pipelines-terminals", "mid"),
                  ("energy-transition", "tr")]:
    sub('slug:"%s",' % slug,
        'slug:"%s", fig:["svc_%s_1","svc_%s_2"],' % (slug, key, key))

# --- layout ------------------------------------------------------------
sub("""          '<div class="block" id="sec-0"><div class="prose">'+s.intro.map(function(p){return '<p>'+esc(p)+'</p>';}).join("")+'</div></div>'+""",
"""          '<div class="block" id="sec-0"><div class="overview">'+
            '<div class="prose">'+s.intro.map(function(p){return '<p>'+esc(p)+'</p>';}).join("")+'</div>'+
            '<figure class="svcfig"><img src="'+IMG[s.fig[0]]+'" alt="" loading="lazy" decoding="async"></figure>'+
          '</div></div>'+""")
sub("""            '<div class="caps">'+s.capabilities.map(function(c){
              return '<article><h3>'+esc(c[0])+'</h3><p>'+esc(c[1])+'</p></article>';
            }).join("")+'</div></div>'+""",
"""            '<div class="caps">'+s.capabilities.map(function(c){
              return '<article><h3>'+esc(c[0])+'</h3><p>'+esc(c[1])+'</p></article>';
            }).join("")+'</div>'+
            '<figure class="svcfig svcfig--wide"><img src="'+IMG[s.fig[1]]+'" alt="" loading="lazy" decoding="async"></figure>'+
          '</div>'+""")

sub("/* capabilities as titled blocks, not a list */",
"""/* service page photography */
.overview{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:1.5rem;align-items:start}
.svcfig{margin:0;border-radius:var(--r-lg);overflow:hidden;border:1px solid var(--line);
  box-shadow:var(--e1),var(--edge);background:var(--surface-2)}
.svcfig img{display:block;width:100%;aspect-ratio:43/28;object-fit:cover}
.svcfig--wide{margin-top:1.5rem}
.svcfig--wide img{aspect-ratio:26/9}
@media (max-width:760px){.overview{grid-template-columns:1fr}.svcfig--wide img{aspect-ratio:16/9}}

/* capabilities as titled blocks, not a list */""")

# --- one capability fewer per service ----------------------------------
DROP = [
 "Extra wells in producing fields, on a rolling three-year rig schedule.",
 "Space held at two Gulf import terminals for summer demand.",
 "Each plant overhauled every five years, timed to the weakest margins.",
 "Robotic tools run the pipes on a published schedule, findings shared.",
 "Routine flaring ends across all operated sites, audited, by 2028.",
]

# --- glossary notes: keep the definition, drop the second sentence ------
NOTES = [
 ("A barrel of oil equivalent counts oil and gas together as one figure. Replacing more than 100% of what you produce means reserves are growing rather than running down.",
  "A barrel of oil equivalent counts oil and gas as one figure. Replacing more than 100% means reserves are growing, not running down."),
 ("A cargo is one shipload. Chilled to liquid, natural gas takes up about one six-hundredth of its normal volume, which is what makes shipping it possible.",
  "A cargo is one shipload. Chilled to liquid, gas takes about one six-hundredth of its normal volume."),
 ("The complexity rating runs from about 1 to 14 and describes how much processing a refinery can do. A higher number means it can handle cheaper, heavier crude.",
  "The complexity rating runs from about 1 to 14. A higher number means the refinery can take cheaper, heavier crude."),
 ("Throughput is the volume passing through the system. A berth is the place at a port where a ship ties up to load.",
  "Throughput is the volume passing through. A berth is where a ship ties up to load."),
 ("These cover emissions from our own operations and from the electricity we buy. A gigawatt is roughly the output of one large power station.",
  "These cover our own operations and the electricity we buy. A gigawatt is roughly one large power station."),
]
for a, b in NOTES: sub(a, b)

bad = [a[:56] for a, b in E if a not in s]
if bad:
    print("NOT FOUND:")
    for m in bad: print("   ", repr(m))
    sys.exit(1)
for a, b in E: s = s.replace(a, b, 1)

for text in DROP:
    pat = re.compile(r'\n *\["[^"]*","' + re.escape(text) + r'"\],?')
    if not pat.search(s):
        print("capability not found:", text[:50]); sys.exit(1)
    s = pat.sub("", s, count=1)

io.open(p, "w", encoding="utf-8").write(s)
print("service pages updated: %d edits, %d capabilities dropped" % (len(E), len(DROP)))
