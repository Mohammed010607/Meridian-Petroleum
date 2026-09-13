import json,urllib.parse,urllib.request,io,base64,sys
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
UA={"User-Agent":"MeridianDemoSite/1.0 (educational demo site)"}
ME =json.load(open("cands_me.json",encoding="utf-8"))
REF=json.load(open("cands_ref.json",encoding="utf-8"))

# (id, source list, index, target w, h, quality, vertical crop bias)
PICK=[
 ("hero_upstream", ME,10,1760,990,72,.60),   # jack-up rig, Abu Dhabi
 ("hero_refining", REF,0,1760,990,72,.50),   # Ruwais refinery, golden hour
 ("hero_lng",      ME,12,1760,990,74,.45),   # QatarGas LNG carrier
 ("hero_terminal", ME,16,1760,990,74,.50),   # Ras Laffan LNG terminal
 ("hero_shipping", ME,28,1760,990,72,.48),   # Muscat harbour
 ("card_ep",       ME, 0, 880,570,74,.42),   # Gulf offshore oil platform
 ("card_gas",      ME,13, 880,570,74,.45),   # LNG carrier
 ("card_refining", REF,1, 880,570,74,.48),   # Ruwais petrochemical, dusk
 ("card_midstream",ME,34, 880,570,76,.45),   # desert pipelines, Jubail
 ("card_transition",ME,48,880,570,74,.45),   # Masdar City solar
 ("band_plant",    ME,14,1600,620,72,.45),   # LNG carrier at berth
]

def fetch(title,width):
    u="https://commons.wikimedia.org/wiki/Special:FilePath/"+urllib.parse.quote(title.replace(" ","_"))+"?width="+str(width)
    r=urllib.request.Request(u,headers=UA)
    return Image.open(io.BytesIO(urllib.request.urlopen(r,timeout=120).read())).convert("RGB")

def cover(im,W,H,bias):
    sw,sh=im.size; tr=W/H; sr=sw/sh
    if sr>tr:
        nw=int(sh*tr); x=(sw-nw)//2; im=im.crop((x,0,x+nw,sh))
    else:
        nh=int(sw/tr); y=int((sh-nh)*bias); im=im.crop((0,y,sw,y+nh))
    return im.resize((W,H),Image.LANCZOS)

out={}; credits=[]
for pid,src,idx,W,H,q,bias in PICK:
    it=src[idx]
    im=fetch(it["title"], max(W,1400)+400)
    im=cover(im,W,H,bias)
    buf=io.BytesIO(); im.save(buf,"JPEG",quality=q,optimize=True,progressive=True)
    b=buf.getvalue()
    out[pid]="data:image/jpeg;base64,"+base64.b64encode(b).decode()
    credits.append({"id":pid,"title":it["title"],"lic":it["lic"],"artist":it["artist"]})
    print(f"{pid:16s} {W}x{H} {len(b)/1024:7.1f}KB [{it['lic']:<15}] {it['title'][:52]}")

json.dump(out,open("imgs.json","w"),indent=0)
json.dump(credits,open("credits.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("\ntotal base64: %.2f MB" % (sum(len(v) for v in out.values())/1024/1024))
