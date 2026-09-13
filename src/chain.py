# Rework the "How the chain works" row: bigger cards, less text, and a
# visual that actually reads as a chain rather than five equal boxes.
import io, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

p = "template.html"
s = io.open(p, encoding="utf-8").read()
E = []
def sub(a, b): E.append((a, b))

# ---- copy: six words a stage, and a lede half the length ---------------
sub('{ step:"01", h:"Explore", p:"Seismic, test wells and licences, close to fields we already run.", dur:"2 – 6 years" }',
    '{ step:"01", h:"Explore", p:"Seismic surveys, test wells, licence awards.", dur:"2 – 6 years" }')
sub('{ step:"02", h:"Produce", p:"Platforms and onshore wells lift it and separate oil, gas and water.", dur:"20 – 40 year field life" }',
    '{ step:"02", h:"Produce", p:"Wells and platforms lift it and separate it.", dur:"20 – 40 year field life" }')
sub('{ step:"03", h:"Move", p:"Pipelines, tanks and ports carry it to the plants and the ships.", dur:"Continuous" }',
    '{ step:"03", h:"Move", p:"Pipelines, tanks and ports carry it onward.", dur:"Continuous" }')
sub('{ step:"04", h:"Process", p:"Refineries and gas plants make fuels, plastics and liquefied gas.", dur:"Continuous" }',
    '{ step:"04", h:"Process", p:"Refineries and gas plants convert it.", dur:"Continuous" }')
sub('{ step:"05", h:"Market", p:"Sold on long contracts and in open markets, delivered by us.", dur:"1 – 20 year contracts" }',
    '{ step:"05", h:"Market", p:"Sold on contracts, delivered by us.", dur:"1 – 20 year contracts" }')

sub("'<p class=\"lede\">Owning the whole chain only counts for something if you genuinely run every link in it. These are the five stages Meridian handles itself rather than hiring out.</p>'+",
    "'<p class=\"lede\">Owning the chain only counts if you run every link. These five stages are ours.</p>'+")

# ---- markup: icon tile, ghost numeral, duration on its own rule --------
sub("""        '<ol class="seq">'+CHAIN.map(function(s){
          return '<li><span class="step">'+esc(s.step)+'</span><h3>'+esc(s.h)+'</h3><p>'+esc(s.p)+'</p><span class="dur">'+esc(s.dur)+'</span></li>';
        }).join("")+'</ol>'+""",
"""        '<ol class="seq">'+CHAIN.map(function(s,i){
          return '<li style="--i:'+i+'">'+
            '<span class="seq-n" aria-hidden="true">'+esc(s.step)+'</span>'+
            '<span class="seq-i" aria-hidden="true">'+CHAIN_ICON[i]+'</span>'+
            '<h3><span class="sr-step">Stage '+esc(s.step)+': </span>'+esc(s.h)+'</h3>'+
            '<p>'+esc(s.p)+'</p>'+
            '<span class="dur">'+esc(s.dur)+'</span></li>';
        }).join("")+'</ol>'+""")

# ---- the five icons, in the same stroked style as the rest of the site --
ICONS = [
 'M12 3 4.5 21M12 3l7.5 18M8.6 12h6.8M6.6 17h10.8',                       # derrick
 'M2.5 21h19M6 21v-8M18 21v-8M4.5 13h15M9 13V7.5h6V13M12 7.5V4',          # platform
 'M2 9h6.5a3.2 3.2 0 0 1 3.2 3.2 3.2 3.2 0 0 0 3.2 3.2H22M6.5 9V5.6M17.4 15.4V19',  # pipeline
 'M3 21V9.6l3.4-2.2V21M10.3 21V5.8L13.7 3.6V21M17.6 21v-7.4L21 11.4V21M1.6 21h20.8',  # towers
 'M2.6 16.6h18.8L19 21H5l-2.4-4.4ZM6.2 16.6V8.4h11.6v8.2M9.6 8.4V5.2h4.8v3.2M12 5.2V2.4',  # ship
]
ICO = "  var CHAIN_ICON = [\n" + "".join(
 "    '<svg width=\"23\" height=\"23\" viewBox=\"0 0 24 24\" fill=\"none\" aria-hidden=\"true\">"
 "<path d=\"%s\" stroke=\"currentColor\" stroke-width=\"1.5\" stroke-linecap=\"round\" "
 "stroke-linejoin=\"round\"/></svg>'%s\n" % (d, "," if i < 4 else "")
 for i, d in enumerate(ICONS)) + "  ];\n\n"
sub("  var CHAIN = [", ICO + "  var CHAIN = [")

# ---- styling -----------------------------------------------------------
OLD_CSS = """/* value chain */
.seq{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,196px),1fr));gap:1.1rem}
.seq li{position:relative;background:var(--raised);border:1px solid var(--line);border-radius:var(--r-lg);
  padding:1.45rem 1.3rem 1.35rem;display:flex;flex-direction:column;gap:.55rem;
  box-shadow:var(--e1),var(--edge);transition:box-shadow .25s ease,transform .25s ease,border-color .2s ease}
.seq li:hover{box-shadow:var(--e2),var(--edge);transform:translateY(-3px);border-color:var(--brass)}
/* the link between one stage and the next, drawn across the gap */
.seq li::after{content:"";position:absolute;top:2.35rem;right:calc(-1.1rem - 1px);width:1.1rem;height:2px;
  background:linear-gradient(90deg,var(--brass),var(--line));opacity:.55}
.seq li:last-child::after{display:none}
.seq .step{display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;
  border-radius:50%;background:var(--brass);color:var(--surface);font-family:var(--mono);font-size:var(--t2);
  font-weight:600;letter-spacing:0;flex:none}
.seq h3{font-size:var(--t5)}
.seq p{font-size:var(--t4)}
.seq .dur{font-family:var(--mono);font-size:var(--t1);color:var(--muted);margin-top:auto;padding-top:.7rem;
  border-top:1px solid var(--line-soft)}"""

NEW_CSS = """/* value chain - five stages, read left to right */
.seq{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,200px),1fr));gap:.9rem}
.seq li{position:relative;overflow:hidden;isolation:isolate;background:var(--raised);
  border:1px solid var(--line);border-radius:var(--r-lg);min-height:17rem;
  padding:1.7rem 1.35rem 1.25rem;display:flex;flex-direction:column;gap:.55rem;
  box-shadow:var(--e1),var(--edge);transition:box-shadow .25s ease,transform .25s ease,border-color .2s ease}
.seq li:hover{box-shadow:var(--e3),var(--edge);transform:translateY(-5px);border-color:var(--brass)}
/* brass rule that draws itself across the top on hover */
.seq li::before{content:"";position:absolute;inset:0 0 auto 0;height:3px;background:var(--brass);
  transform:scaleX(0);transform-origin:left;transition:transform .32s ease;z-index:2}
.seq li:hover::before{transform:scaleX(1)}
/* the stage number, set large and faint behind the text */
.seq-n{position:absolute;top:-.6rem;right:.5rem;z-index:-1;pointer-events:none;
  font-family:var(--disp);font-weight:700;letter-spacing:-.05em;line-height:1;
  font-size:clamp(3.3rem,2.2rem + 2.8vw,4.8rem);color:var(--ink);opacity:.055;
  transition:opacity .25s ease,color .25s ease}
.seq li:hover .seq-n{color:var(--brass);opacity:.14}
.seq-i{display:inline-flex;align-items:center;justify-content:center;width:46px;height:46px;flex:none;
  border-radius:13px;background:var(--brass-soft);color:var(--brass);border:1px solid var(--line);
  margin-bottom:.35rem;transition:background .25s ease,color .25s ease,border-color .25s ease}
.seq li:hover .seq-i{background:var(--brass);color:var(--surface);border-color:var(--brass)}
.seq h3{font-size:var(--t6)}
.seq p{font-size:var(--t4);color:var(--body)}
.sr-step{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
.seq .dur{font-family:var(--mono);font-size:var(--t1);letter-spacing:.09em;text-transform:uppercase;
  color:var(--muted);margin-top:auto;padding-top:.85rem;border-top:1px solid var(--line-soft)}
/* chevron in the gap: the flow between one stage and the next */
.seq li::after{content:"";position:absolute;top:2.85rem;right:-.78rem;width:9px;height:9px;z-index:3;
  border-top:2px solid var(--brass);border-right:2px solid var(--brass);transform:rotate(45deg);
  opacity:.35;animation:flow 3.4s ease-in-out infinite;animation-delay:calc(var(--i) * .34s)}
.seq li:last-child::after{display:none}
@keyframes flow{0%,62%,100%{opacity:.3}18%{opacity:1}}
[data-theme="dark"] .seq-n{opacity:.09}
[data-theme="dark"] .seq-i{border-color:var(--brass-soft)}
@media (max-width:820px){.seq li{min-height:0}.seq li::after{display:none}}
@media (prefers-reduced-motion:reduce){.seq li::after{animation:none}}"""

sub(OLD_CSS, NEW_CSS)

bad = [a[:60] for a, b in E if a not in s]
if bad:
    print("NOT FOUND:")
    for m in bad: print("   ", repr(m))
    sys.exit(1)
for a, b in E: s = s.replace(a, b, 1)
io.open(p, "w", encoding="utf-8").write(s)
print("chain section reworked - %d edits" % len(E))
