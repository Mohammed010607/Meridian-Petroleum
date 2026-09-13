# Two problems, measured: ~1,556 words of prose, and 41 distinct font sizes
# with 24 declarations under 12px. This cuts the copy and collapses the type
# onto a six-step scale with a 12px floor.
import io, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

p = "template.html"
s = io.open(p, encoding="utf-8").read()
R = []
def sub(old, new): R.append((old, new))

# ── service intros: two paragraphs each become one ──────────────────────
INTROS = [
("""        "We run 21 oil and gas fields ourselves, and own a share of 14 more that other companies run. About half of what we produce comes from platforms offshore in the Gulf; the rest comes from fields inland in the desert. We prefer fields we operate ourselves, because then we control the costs rather than waiting on a partner to decide.",
        "We do very little exploring in untested places. Most of our money goes into drilling extra wells in fields we already run, and connecting new discoveries by pipeline back to platforms that are already built and paid for. A well like that starts producing within months instead of years."
""",
 """        "We run 21 fields ourselves and hold a share of 14 more. Half our output is offshore, half inland. We spend on extra wells and tiebacks around fields we already operate, so a new well produces in months rather than years."
"""),
("""        "Gas is the part of the business we are growing fastest. Our plant at Ras Meridian has three production lines that cool gas into liquid, and a fourth has been approved. We sell to the end customer ourselves rather than handing the gas over at the factory gate — so we also take on the shipping and the responsibility for arriving on time.",
        "About 70% of our gas is sold on contracts of five years or more, which keeps income predictable. The rest is sold one shipload at a time at whatever the market pays that week — most valuable in winter, when demand and prices spike."
""",
 """        "Our fastest-growing business. Ras Meridian runs three liquefaction lines with a fourth approved. We sell to the end customer rather than at the plant gate, so we carry the shipping too. Around 70% moves on contracts of five years or more."
"""),
("""        "Our three refineries process 640,000 barrels of crude a day. They carry extra processing units that simpler refineries do not have, and that is deliberate: it lets us buy the thick, high-sulphur crude that sells at a discount and still get a high proportion of diesel and jet fuel out of it.",
        "At Duqm the refinery is joined to a chemicals plant. Rather than selling one of the lighter products at fuel prices, we pipe it next door and turn it into plastic pellets, which are worth considerably more. That link adds around $3.10 of value to every barrel."
""",
 """        "Extra conversion units let us buy thick, high-sulphur crude at a discount and still yield mostly diesel and jet fuel. At Duqm the refinery feeds a chemicals plant next door, adding about $3.10 to every barrel."
"""),
("""        "This is the steadiest part of the company. About 80% of its income comes from fixed fees: customers pay to reserve space in our pipelines and tanks whether they end up using it or not. Because that income barely moves with the oil price, this business pays for its own expansion.",
        "One control room watches the whole network, with leak detection on every line and robotic inspection tools sent through the pipes on a published schedule. Just under half the volume we carry belongs to other companies — competitors included, who pay to use our pipes."
""",
 """        "The steadiest part of the company. Around 80% of income is fixed fees — customers reserve space whether they ship or not — so it barely follows the oil price. Just under half the volume we carry belongs to other companies."
"""),
("""        "We spend 18% of the company's total budget on lowering emissions, and we report it as a business in its own right, held to the same financial standards as everything else. None of it is paid for from a side account or left out of the main figures.",
        "We tackle it in a deliberate order. Stopping methane leaks comes first, because it is the cheapest way to remove a tonne of emissions and the technology to measure it is now reliable. Capturing carbon dioxide comes second, fitted to the plants that will still be running in 2040. Solar and wind come third, sized to cover the electricity our own sites buy from the grid."
""",
 """        "18% of group capital, reported as its own business and held to the same returns test as the rest. Methane leaks first, because it is the cheapest tonne. Then carbon capture. Then solar and wind, sized to our own demand."
"""),
]
for a, b in INTROS: sub(a, b)

# ── hero slides ─────────────────────────────────────────────────────────
HERO = [
("We produce the equivalent of 412,000 barrels of oil every day across six Gulf countries — and we run most of those fields ourselves.",
 "412,000 barrels of oil equivalent a day, across six Gulf countries. We operate most of it ourselves."),
("Natural gas has to be chilled into a liquid before it can cross an ocean. We do that, then ship it ourselves — 14.2 million tonnes a year on a fleet of eleven vessels.",
 "Gas must be chilled to liquid before it can cross an ocean. We do that, and ship it — 14.2 million tonnes a year."),
("Our three refineries turn 640,000 barrels a day into fuels and plastics — including the thick, high-sulphur crude that most refineries cannot process.",
 "640,000 barrels a day into fuels and plastics — including the heavy crude most refineries cannot take."),
("6,800 kilometres of pipeline and 31 million barrels of storage carry oil and gas to port, running 99.7% of the time.",
 "6,800 km of pipeline and 31 million barrels of storage, running 99.7% of the time."),
("We spend 18% of our budget on cutting emissions: capturing 2.5 million tonnes of carbon dioxide a year, and ending routine gas burning by 2028.",
 "18% of our budget cuts emissions: 2.5 million tonnes of CO₂ captured a year, routine flaring gone by 2028."),
]
for a, b in HERO: sub('p:"%s"' % a, 'p:"%s"' % b)

# ── ledes ───────────────────────────────────────────────────────────────
LEDE = [
("We find oil and gas, drill the wells and bring what comes out to the surface — inland in the desert and offshore in the Gulf.",
 "Finding and producing oil and gas, offshore in the Gulf and inland in the desert."),
("Gas cannot be shipped as a gas. We cool it until it turns liquid, carry it by sea, and sell it to the customer at the other end.",
 "We chill gas to liquid, carry it by sea, and sell it at the other end."),
("We turn crude oil into petrol, diesel, jet fuel and the raw material for plastics — including from cheaper, harder-to-process crude.",
 "Crude into petrol, diesel, jet fuel and plastics — including the cheaper, harder grades."),
("The pipes, tanks and ports that carry oil and gas from the well to the ship. The least glamorous business we run, and the steadiest.",
 "The pipes, tanks and ports between the well and the ship. Our least glamorous business, and our steadiest."),
("Cutting the emissions from our own operations, capturing the carbon we cannot avoid, and building solar and wind to power our sites.",
 "Cutting our own emissions, capturing what we cannot avoid, and powering our sites with solar and wind."),
]
for a, b in LEDE: sub('lede:"%s"' % a, 'lede:"%s"' % b)

# ── card blurbs ─────────────────────────────────────────────────────────
CARD = [
("Finding and producing oil and gas across Oman, the UAE, Saudi Arabia, Kuwait and Qatar.",
 "Production across Oman, the UAE, Saudi Arabia, Kuwait and Qatar."),
("Chilling natural gas into liquid in Oman, then shipping it to customers in Asia and around the Gulf.",
 "Liquefaction in Oman, then shipping to customers in Asia and the Gulf."),
("Three refineries turning crude oil into fuels, with a chemicals plant next door that makes plastics.",
 "Three refineries making fuels, with a chemicals plant alongside."),
("6,800 km of pipeline, 24 storage terminals and four deep-water ports, all run from one control room.",
 "6,800 km of pipeline, 24 terminals and four deep-water ports."),
("Cutting our own emissions: capturing carbon, stopping gas leaks, and 1.4 GW of solar and wind.",
 "Carbon capture, methane abatement and 1.4 GW of solar and wind."),
]
for a, b in CARD: sub('card:"%s"' % a, 'card:"%s"' % b)

# ── value chain ─────────────────────────────────────────────────────────
CHAIN = [
("Surveying the rock, drilling test wells and winning licences — mostly close to fields we already run.",
 "Seismic, test wells and licences, close to fields we already run."),
("Platforms and onshore wells bring the oil and gas up, then separate it into oil, gas and water.",
 "Platforms and onshore wells lift it and separate oil, gas and water."),
("Pipelines, storage tanks and ports carry it onward to the refineries and to waiting ships.",
 "Pipelines, tanks and ports carry it to the plants and the ships."),
("Refineries and gas plants turn it into petrol, diesel, plastics and liquefied gas.",
 "Refineries and gas plants make fuels, plastics and liquefied gas."),
("We sell it on long contracts and in open markets — and we are the ones responsible for delivering it.",
 "Sold on long contracts and in open markets, delivered by us."),
]
for a, b in CHAIN: sub('p:"%s"' % a, 'p:"%s"' % b)

# ── news ────────────────────────────────────────────────────────────────
NEWS = [
("The new line adds 5.2 million tonnes a year, taking the plant to 19.4 million in total. The first shipment is due in 2029, and 78% of it is already sold.",
 "The line adds 5.2 million tonnes a year, taking the plant to 19.4 million. First cargo is due in 2029, and 78% is already sold."),
("Four new wells were piped back to the existing Al Hadd platform and began producing eleven weeks early, adding 34,000 barrels a day at peak.",
 "Four wells piped back to the existing platform came on eleven weeks early, adding 34,000 barrels a day at peak."),
("The plant has now pumped 2.04 million tonnes of carbon dioxide underground since it opened, running at 96% of its design capacity this year.",
 "2.04 million tonnes stored since opening, with the plant running at 96% of design capacity."),
("The 42-day shutdown overhauled the main processing units, finished four days early, and passed without a single injury causing lost time.",
 "The 42-day shutdown overhauled the main units, finished four days early, and lost no time to injury."),
]
for a, b in NEWS: sub('body:"%s"' % a, 'body:"%s"' % b)

# ── capabilities: same meaning, roughly a third fewer words ─────────────
CAPS = [
("We are the operator on our shallow-water and onshore fields, including two floating production ships.",
 "Operator on our shallow-water and onshore fields, including two floating production ships."),
("New discoveries are piped back to platforms we already own, instead of building another one.",
 "New finds piped back to platforms we already own, rather than building another."),
("Extra wells drilled into fields already in production, planned on a rolling three-year schedule.",
 "Extra wells in producing fields, on a rolling three-year rig schedule."),
("Water and gas pumped back into older fields in Oman and the UAE to push out oil that would otherwise stay underground.",
 "Water and gas injected into older fields to recover oil that would otherwise stay down."),
("Safely dismantling fields at the end of their life, paid for from money set aside in advance.",
 "End-of-life fields dismantled safely, funded from money set aside in advance."),
("The gas field, the plant that liquefies it, the ship that carries it, and the contract with the buyer.",
 "The field, the plant, the ship and the contract with the buyer."),
("We charter and schedule the fleet ourselves, so sending a cargo to a better market is our decision to make.",
 "We charter and schedule the fleet, so diverting a cargo is our decision."),
("Multi-year supply agreements with buyers in Japan, Korea and India, and with neighbours in Kuwait and the UAE.",
 "Multi-year agreements with buyers in Japan, Korea, India and the Gulf."),
("Space reserved at two Gulf import terminals, where the liquid is warmed back into gas for local use in summer.",
 "Space held at two Gulf import terminals for summer demand."),
("Buyers can ask for a shipment whose emissions have been offset, with the certificates cancelled in their name.",
 "Cargoes can be offset, with the certificates cancelled in the buyer's name."),
("Extra processing units that break thick, high-sulphur crude down into clean diesel and jet fuel.",
 "Units that break thick, high-sulphur crude into clean diesel and jet fuel."),
("At Duqm the refinery feeds a chemicals plant next door, turning fuel-grade material into higher-value plastic.",
 "At Duqm the refinery feeds a chemicals plant, turning fuel into plastic."),
("Diesel and ship fuel that meet the strictest sulphur limits, including the global shipping standard.",
 "Diesel and marine fuel meeting the strictest sulphur limits."),
("Every five years each plant is shut down and overhauled, timed for when profits are seasonally weakest.",
 "Each plant overhauled every five years, timed to the weakest margins."),
("Plant-based oils processed alongside crude, currently 4% of everything we put through.",
 "Plant-based oils run alongside crude, currently 4% of throughput."),
("Customers pay a fixed fee to reserve capacity whether they ship or not, so income barely follows the oil price.",
 "Customers pay to reserve capacity whether they ship or not."),
("The whole network is watched from a single room, with leak detection and valves that can be shut remotely.",
 "One room watches the network, with leak detection and remote valves."),
("Robotic tools are sent through the pipes on a published schedule, and the findings are shared with customers.",
 "Robotic tools run the pipes on a published schedule, findings shared."),
("Different grades of crude are stored and blended separately, so each customer gets exactly what they paid for.",
 "Grades stored and blended separately, so customers get what they paid for."),
("Deep-water berths that take the biggest crude tankers afloat, with equipment that captures fumes during loading.",
 "Berths for the largest tankers afloat, with vapour capture on loading."),
("Every site we run is monitored continuously for methane leaks, cross-checked by satellite and drone surveys.",
 "Continuous methane monitoring, cross-checked by satellite and drone."),
("Carbon dioxide is captured at the Sohar refinery and the Ras Meridian gas plant, then stored deep underground.",
 "Captured at Sohar and Ras Meridian, then stored deep underground."),
("Solar and wind farms built to replace the grid electricity our own facilities would otherwise buy.",
 "Solar and wind sized to replace the grid power our sites buy."),
("Ending the routine burning-off of unwanted gas at our sites, with an audited deadline of 2028.",
 "Routine flaring ends across all operated sites, audited, by 2028."),
("Our emissions figures are audited by an independent firm, not simply reported by us.",
 "Emissions audited by an independent firm, not just reported by us."),
]
for a, b in CAPS: sub('","%s"]' % a, '","%s"]' % b)

missing = [o[:58] for o, n in R if o not in s]
if missing:
    print("NOT FOUND (%d):" % len(missing))
    for m in missing: print("   ", repr(m))
    sys.exit(1)
for old, new in R:
    s = s.replace(old, new, 1)

# ── type scale: six steps, nothing under 12px ───────────────────────────
# seven steps, nothing below 12px; the clamp() display sizes are left alone
SCALE = [(0.705, "var(--t1)"), (0.795, "var(--t2)"), (0.845, "var(--t3)"),
         (0.935, "var(--t4)"), (1.060, "var(--t5)"), (1.200, "var(--t6)"),
         (1.600, "var(--t7)")]
def snap(m):
    v = float(m.group(1))
    for ceiling, tok in SCALE:
        if v <= ceiling: return "font-size:" + tok
    return m.group(0)
head = s[:s.index("</style>")]
tail = s[s.index("</style>"):]
before = len(set(re.findall(r"font-size:\s*([0-9.]+)rem", head)))
head = re.sub(r"font-size:\s*([0-9.]+)rem", snap, head)
after = len(set(re.findall(r"font-size:\s*([0-9.]+)rem", head)))
head = head.replace("  --r:5px; --r-lg:10px; color-scheme:light;",
                    "  --r:5px; --r-lg:10px; color-scheme:light;\n"
                    "  /* type scale - floor 12px, every size on the page is one of these */\n"
                    "  --t1:.75rem; --t2:.8125rem; --t3:.875rem; --t4:.9375rem;\n"
                    "  --t5:1rem; --t6:1.15rem; --t7:1.4rem;")
s = head + tail
io.open(p, "w", encoding="utf-8").write(s)

print("applied %d copy edits" % len(R))
print("  distinct rem font-sizes: %d -> %d" % (before, after))

def words(t): return len(re.findall(r"[A-Za-z0-9']+", t))
tot = 0
for name, pat in [("hero", r'\n      p:"([^"]+)"'), ("lede", r'lede:"([^"]+)"'),
                  ("intro", r'intro:\[\s*\n\s*"([^"]+)"'), ("cap", r'\["[^"]{3,30}","([^"]{30,})"\]'),
                  ("card", r'card:"([^"]+)"'), ("news", r'body:"([^"]+)"'),
                  ("chain", r'\n    \{ step:"\d+", h:"[^"]+", p:"([^"]+)"'),
                  ("timeline", r'\["(?:19|20)\d\d","([^"]+)"')]:
    tot += sum(words(x) for x in re.findall(pat, s))
print("  prose words: 1556 -> %d  (%.0f%% cut)" % (tot, 100*(1556-tot)/1556))
