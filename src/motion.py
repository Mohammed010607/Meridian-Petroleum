# Two changes: redraw the value-chain marks as engineering symbols rather
# than pictograms, and add scroll-in motion across the site.
import io, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = "template.html"
s = io.open(p, encoding="utf-8").read()
E = []
def sub(a, b): E.append((a, b))

# ---------------------------------------------------------------- icons
# The tinted rounded tile was most of what made these read as app icons.
sub(""".seq-i{display:inline-flex;align-items:center;justify-content:center;width:50px;height:50px;flex:none;
  border-radius:14px;background:var(--brass-soft);color:var(--brass);border:1px solid var(--line);
  margin-bottom:.35rem;transition:background .25s ease,color .25s ease,border-color .25s ease}
.seq li:hover .seq-i{background:var(--brass);color:var(--surface);border-color:var(--brass)}""",
""".seq-i{display:block;color:var(--brass);opacity:.88;margin-bottom:.75rem;
  transition:opacity .25s ease,transform .3s ease}
.seq li:hover .seq-i{opacity:1;transform:translateY(-2px)}""")
sub('[data-theme="dark"] .seq-i{border-color:var(--brass-soft)}\n', "")
sub('<svg width="26" height="26" viewBox="0 0 24 24"', '<svg width="30" height="30" viewBox="0 0 24 24"')
sub('stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    'stroke="currentColor" stroke-width="1.15" stroke-linecap="round" stroke-linejoin="round"/></svg>')

ICONS = [
 # seismic source over three wavefronts
 ('M9 3.4h6M9 3.4 5.4 20.6M15 3.4l3.6 17.2M3.6 20.6h16.8M7.6 14.2h8.8M8.5 9.4h7',
  'M8.4 4.4h7.2v2.8H8.4zM12 7.2v2.1M6.2 12.9a7.6 7.6 0 0 0 11.6 0'
  'M8.3 16.6a4.7 4.7 0 0 0 7.4 0M10.2 20.2a2.2 2.2 0 0 0 3.6 0'),
 # wellhead with a side outlet
 ('M2.5 21h19M6 21v-8M18 21v-8M4.5 13h15M9 13V7.5h6V13M12 7.5V4',
  'M3.4 20.6h17.2M12 20.6v-9.2M9.4 11.4h5.2V7.8H9.4zM12 7.8V5.2M14.6 9.6h4.8M19.4 9.6v3.4'),
 # gate valve on a line
 ('M2.4 12h6.2M15.4 12h6.2M7.2 9.1v5.8M16.8 9.1v5.8'
  'M12 14.4a2.4 2.4 0 1 1 0-4.8 2.4 2.4 0 1 1 0 4.8M12 9.6V6.9M10.1 6.9h3.8',
  'M2.4 12h5.4M16.2 12h5.4M7.8 8.5l8.4 7V8.5l-8.4 7zM12 12V6.3M9.9 6.3h4.2'),
 # distillation column with trays, feed in, draw off
 ('M2 20.8h20M3.6 20.8V10a2.6 2.6 0 0 1 5.2 0v10.8M3.6 14.2h5.2M3.6 17.5h5.2'
  'M12.4 20.8v-8.4a2 2 0 0 1 4 0v8.4M19.2 20.8v-6.2a1.4 1.4 0 0 1 2.8 0v6.2',
  'M9 20.6V7.9a3 3 0 0 1 6 0v12.7zM9.4 11.6h5.2M9.4 14.9h5.2M9.4 18.2h5.2'
  'M9 10.2H4.9M4.9 10.2v3.2M15 17.4h4.1M19.1 17.4v-3.2'),
 # terminal, and the cargo leaving it
 ('M2.6 16.6h18.8L19 21H5l-2.4-4.4ZM6.2 16.6V8.4h11.6v8.2M9.6 8.4V5.2h4.8v3.2M12 5.2V2.4',
  'M2.8 8.2h5.2v7.6H2.8zM8 12h11.3M16.3 9 19.5 12l-3.2 3'),
]
for a, b in ICONS: sub(a, b)

# --------------------------------------------------------------- motion
sub("/* full-bleed feature band */",
"""/* ---------- motion ----------
   Opt-in only: script adds .anim once it has confirmed the observer really
   fires, so nothing can be left permanently hidden. */
html.anim [data-rise]{opacity:0;transform:translateY(15px)}
html.anim [data-rise].shown{opacity:1;transform:none;
  transition:opacity .6s cubic-bezier(.22,.61,.36,1),transform .6s cubic-bezier(.22,.61,.36,1);
  transition-delay:calc(var(--d,0) * 70ms)}
/* bars grow from their axis, the reported line draws itself, the forecast
   fades in behind it */
html.anim .chart .bar{transform-box:fill-box;transform-origin:left center;transform:scaleX(0)}
html.anim .chart.shown .bar{animation:barIn .8s cubic-bezier(.22,.61,.36,1) both;
  animation-delay:calc(var(--b,0) * 75ms)}
@keyframes barIn{to{transform:scaleX(1)}}
html.anim .chart .ln{stroke-dasharray:780;stroke-dashoffset:780}
html.anim .chart.shown .ln{animation:draw 1.1s ease-out .12s both}
@keyframes draw{to{stroke-dashoffset:0}}
html.anim .chart .ln-p,html.anim .chart .dot{opacity:0}
html.anim .chart.shown .ln-p{animation:fadeIn .5s ease-out 1s both}
html.anim .chart.shown .dot{animation:fadeIn .4s ease-out both;
  animation-delay:calc(.25s + var(--b,0) * 110ms)}
@keyframes fadeIn{to{opacity:1}}
html.anim .gulfmap .pin-h{animation:halo 4s ease-in-out infinite;
  animation-delay:calc(var(--p,0) * .21s)}
@keyframes halo{0%,72%,100%{opacity:.32}36%{opacity:.85}}
.btn .arrow{transition:transform .25s ease}
.btn:hover .arrow{transform:translateX(3px)}
@media (prefers-reduced-motion:reduce){
  html.anim [data-rise]{opacity:1;transform:none}
  html.anim .chart .bar{transform:none}
  html.anim .chart .ln{stroke-dasharray:none;stroke-dashoffset:0}
  html.anim .chart .ln-p,html.anim .chart .dot{opacity:1}
  html.anim .gulfmap .pin-h{animation:none}
}

/* full-bleed feature band */""")

# chart hooks: an index per bar and per dot, and classes on the two lines
sub("""bars+='<text class="cat" x="'+(padL-10)+'" y="'+(y+16)+'" text-anchor="end">'+esc(d[0])+'</text>'+
            '<rect class="bar" x="'+padL+'" y="'+(y+5)+'" width="'+w+'" height="15" rx="4"/>'+""",
    """bars+='<text class="cat" x="'+(padL-10)+'" y="'+(y+16)+'" text-anchor="end">'+esc(d[0])+'</text>'+
            '<rect class="bar" style="--b:'+i+'" x="'+padL+'" y="'+(y+5)+'" width="'+w+'" height="15" rx="4"/>'+""")
sub("""      return '<circle cx="'+X(i)+'" cy="'+Y(d[1])+'" r="3.4" fill="var(--c1)" stroke="var(--surface)" stroke-width="2"/>';""",
    """      return '<circle class="dot" style="--b:'+i+'" cx="'+X(i)+'" cy="'+Y(d[1])+'" r="3.4" fill="var(--c1)" stroke="var(--surface)" stroke-width="2"/>';""")
sub("""'<path d="'+actual+'" fill="none" stroke="var(--c1)" stroke-width="2.4" stroke-linejoin="round"/>'+
      '<path d="'+proj+'" fill="none" stroke="var(--c2)" stroke-width="2.4" stroke-dasharray="5 5"/>'+""",
    """'<path class="ln" d="'+actual+'" fill="none" stroke="var(--c1)" stroke-width="2.4" stroke-linejoin="round"/>'+
      '<path class="ln-p" d="'+proj+'" fill="none" stroke="var(--c2)" stroke-width="2.4" stroke-dasharray="5 5"/>'+""")
sub("""    var pins = m.sites.map(function(st){""",
    """    var pins = m.sites.map(function(st,pi){""")
sub("""'<circle class="pin-h" cx="'+st.x+'" cy="'+st.y+'" r="11"/>'+""",
    """'<circle class="pin-h" style="--p:'+pi+'" cx="'+st.x+'" cy="'+st.y+'" r="11"/>'+""")

# --------------------------------------------------------------- script
sub("""  /* In-page index: jump on click, highlight the section being read.""",
"""  /* Bring blocks in as they are scrolled to. The hidden state is applied
     from script, and dropped again if the observer turns out not to fire,
     so the page can never be left with invisible content. */
  var revealObs = null;
  function initReveal(root){
    if (revealObs) { revealObs.disconnect(); revealObs = null; }
    var html = document.documentElement;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches ||
        !("IntersectionObserver" in window)) { html.classList.remove("anim"); return; }
    var SEL = ".sechead,.svc-card,.seq li,.caps article,.news article,.panel,.chart," +
              ".mapwrap,.mapkey,.kpis > div,.regwrap,.specs,.prose,.tl li,.svcfig";
    var els = [].slice.call(root.querySelectorAll(SEL));
    if (!els.length) { html.classList.remove("anim"); return; }
    html.classList.add("anim");
    els.forEach(function(el){
      el.setAttribute("data-rise","");
      var sibs = el.parentNode.children, n = 0;
      for (var i=0;i<sibs.length && sibs[i]!==el;i++){
        if (sibs[i].hasAttribute && sibs[i].hasAttribute("data-rise")) n++;
      }
      el.style.setProperty("--d", String(Math.min(n,6)));
    });
    var fired = false;
    revealObs = new IntersectionObserver(function(entries){
      fired = true;
      entries.forEach(function(e){
        if (!e.isIntersecting) return;
        revealObs.unobserve(e.target);
        e.target.classList.add("shown");
      });
    }, {rootMargin:"0px 0px -6% 0px", threshold:0.04});
    els.forEach(function(el){ revealObs.observe(el); });
    setTimeout(function(){ if (!fired) html.classList.remove("anim"); }, 1200);
  }

  /* In-page index: jump on click, highlight the section being read.""")
sub("closeNav(); bindForm(); initStage(); initCounters(app); initTOC(app); window.scrollTo(0,0);",
    "closeNav(); bindForm(); initStage(); initReveal(app); initCounters(app); initTOC(app);\n    window.scrollTo(0,0);")

bad = [a[:58] for a, b in E if a not in s]
if bad:
    print("NOT FOUND:")
    for m in bad: print("   ", repr(m))
    sys.exit(1)
for a, b in E: s = s.replace(a, b, 1)
io.open(p, "w", encoding="utf-8").write(s)
print("icons + motion applied (%d edits)" % len(E))
