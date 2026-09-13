# Wrap the artifact build in real HTML boilerplate for self-hosting.
# The artifact platform injects <!doctype>/<html>/<head>; a static host does not.
import io, os, sys, shutil
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# The favicon lives in template.html so every build has it. These are
# link-preview tags, which only matter once the site is hosted at a URL.
DEPLOY_HEAD = (
    '<meta property="og:type" content="website">\n'
    '<meta property="og:site_name" content="Meridian Petroleum">\n'
    '<meta property="og:title" content="Meridian Petroleum">\n'
    '<meta property="og:description" content="An integrated oil and gas company '
    'operating across six Gulf countries, headquartered in Muscat.">\n'
    '<meta name="twitter:card" content="summary">\n'
)

src = io.open("meridian-petroleum.html", encoding="ascii").read()

# everything up to and including the single </style> belongs in <head>
cut = src.index("</style>") + len("</style>")
head, body = src[:cut].strip(), src[cut:].strip()

# charset is re-declared by us inside <head>, so drop the duplicate from the slice
head = head.replace('<meta charset="utf-8">\n', "", 1)

out = (
    "<!doctype html>\n"
    '<html lang="en">\n'
    "<head>\n"
    '<meta charset="utf-8">\n'
    + head + "\n"
    + DEPLOY_HEAD +
    "</head>\n"
    "<body>\n"
    + body + "\n"
    "</body>\n"
    "</html>\n"
)

# repo root is one level up from src/, so this works on any machine
DEST = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
os.makedirs(DEST, exist_ok=True)
io.open(os.path.join(DEST, "index.html"), "w", encoding="ascii", newline="\n").write(out)

# a tiny robots.txt so search engines are not guessing
io.open(os.path.join(DEST, "robots.txt"), "w", encoding="ascii", newline="\n").write(
    "User-agent: *\nAllow: /\n"
)

print("wrote %s" % DEST)
for f in sorted(os.listdir(DEST)):
    print("  %-12s %8.2f KB" % (f, os.path.getsize(os.path.join(DEST, f)) / 1024))

# sanity checks on the deploy file
d = io.open(os.path.join(DEST, "index.html"), encoding="ascii").read()
checks = [
    ("doctype",            d.startswith("<!doctype html>")),
    ("html lang",          '<html lang="en">' in d),
    ("single <head>",      d.count("<head>") == 1),
    ("single <body>",      d.count("<body>") == 1),
    ("closes html",        d.rstrip().endswith("</html>")),
    ("title in head",      d.index("<title>") < d.index("</head>")),
    ("style in head",      d.index("<style>") < d.index("</head>")),
    ("script in body",     d.index("<script>") > d.index("<body>")),
    ("viewport",           'name="viewport"' in d),
    ("favicon",            'rel="icon"' in d),
    ("no stray charset",   d.count('charset="utf-8"') == 1),
]
print()
for n, ok in checks:
    print("  [%s] %s" % ("PASS" if ok else "FAIL", n))
print("\n  total %.2f MB" % (len(d.encode()) / 1024 / 1024))
