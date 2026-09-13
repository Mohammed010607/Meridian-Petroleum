import json,re,sys,html
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
imgs=json.load(open("imgs.json"))
creds=json.load(open("credits.json",encoding="utf-8"))
tpl=open("template.html",encoding="utf-8").read()

def clean(t):
    t=re.sub(r"\.(jpe?g|JPG|JPEG)$","",t)
    t=re.sub(r"\s*\(\d{6,}\)$","",t).replace("_"," ").strip()
    t=re.sub(r"^[\d\s]+","",t)
    t=re.sub(r"\s+(\d{3,}|DSW|\d{2})$","",t).strip()
    t=re.sub(r"(?<=[a-z])(?=[A-Z])"," ",t) if " " not in t else t
    return t.strip(" -")
def artist(a):
    a=re.sub(r"\s+"," ",a).strip().rstrip(",")
    a=re.sub(r"^(Original uploader was|User:)\s*","",a,flags=re.I)
    a=re.sub(r"\s*at (en|de)\.wikipedia.*$","",a,flags=re.I)
    a=re.sub(r"/\s*www\..*$","",a)
    a=re.sub(r"\s*from (London|UK).*$","",a)
    a=re.sub(r"\s*\(talk\)","",a,flags=re.I)
    a=re.sub(r"\s*at (en|de)\.?$","",a,flags=re.I)
    a=re.sub(r"\s*/\s*AGA$","",a)
    return a.strip(" .,/") or "Wikimedia Commons contributor"

# short credit shown on the hero stage
cmap={c["id"]: f'Photo: {artist(c["artist"])}, {c["lic"]}' for c in creds}

# full credit block for the footer
items=[]
for c in creds:
    items.append('%s &#8212; %s, %s' % (html.escape(clean(c["title"])), html.escape(artist(c["artist"])), html.escape(c["lic"])))
block=('<p>All photographs are freely licensed works sourced from Wikimedia Commons and are used here to illustrate a '
       'fictional company. They do not depict facilities owned or operated by any "Meridian Petroleum". '
       'Licence terms: <a href="https://creativecommons.org/licenses/">creativecommons.org/licenses</a>.</p>'
       '<p style="margin-top:.5rem">'+' &#183; '.join(items)+'</p>')

out=tpl.replace("__IMGS__", json.dumps(imgs))
out=out.replace("__CREDITMAP__", json.dumps(cmap, ensure_ascii=False))
out=out.replace("__CREDITS__", block)

assert "__IMGS__" not in out and "__CREDITMAP__" not in out and "__CREDITS__" not in out
open("meridian-petroleum.html","w",encoding="utf-8").write(out)
print("built  %.2f MB" % (len(out.encode())/1024/1024))
for k,v in cmap.items(): print("  ",k,"->",v[:78])
