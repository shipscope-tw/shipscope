"""Long price history for the KPI charts -> hist.json
Usage: python fetch_hist.py <out.json> [prev_hist.json] [indicators.json]
- Baltic indices (BDI/BCI/BPI/BSI/BHSI + avg T/C): HandyBulk monthly archive (daily, from 2025)
- Brent, WTI, Henry Hub, propane: FRED daily (5+ years); iron ore, Australian coal: FRED monthly (World Bank)
- every other indicator: accumulated from each day's indicators.json
Any source that fails is skipped and the previous history is kept."""
import json, re, sys, os, time, datetime, urllib.request, csv, io
UA={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36"}
out_p=sys.argv[1]; prev_p=sys.argv[2] if len(sys.argv)>2 else None; ind_p=sys.argv[3] if len(sys.argv)>3 else None
TODAY=datetime.date.today(); KEEP_FROM=(TODAY-datetime.timedelta(days=int(6.2*365))).isoformat()
def get(url,timeout=40):
    for i in range(3):
        try: return urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=timeout).read().decode("utf8","ignore")
        except Exception as e:
            if "404" in str(e): return ""
            err=e; time.sleep(2+2*i)
    print("FAIL",url[:90],err,file=sys.stderr); return ""
def load(p):
    try:
        d=json.load(open(p,encoding="utf-8"))
        return d.get("data",d) if isinstance(d,dict) and "series" not in d and "data" in d else d
    except Exception: return None
H=load(prev_p) if prev_p else None
H=H or {"series":{},"monthly":{},"src":{}}
H.setdefault("series",{}); H.setdefault("monthly",{}); H.setdefault("src",{})
def merge(kind,id_,pts):
    cur={d:v for d,v in H[kind].get(id_,[])}
    for d,v in pts:
        if v is not None and d>=KEEP_FROM: cur[d]=v
    H[kind][id_]=[[d,cur[d]] for d in sorted(cur)]
# ---------- Baltic (HandyBulk) ----------
MON={m:i for i,m in enumerate(["January","February","March","April","May","June","July","August","September","October","November","December"],1)}
NUM=r"([\d]{1,2},\d{3}|\d{3,6})"
LAB=[("bdi",r"Baltic Dry Index \(BDI\)"),("bci",r"Baltic Capesize Index \(BCI\)"),("bpi",r"Baltic Panamax Index \(BPI\)"),("bsi",r"Baltic Supramax Index \(BSI\)"),("bhsi",r"Baltic Handysize Index \(BHSI\)")]
TC=[("cape",r"capesize bulk carriers"),("pmx",r"panamax bulk carriers"),("smx",r"supramax bulk carriers"),("handy",r"handysize bulk carriers")]
STRICT=re.compile(r"The Baltic Dry Index \(BDI\)[^.]*?to (?:reach )?([\d,]+) points\. The Baltic Capesize Index \(BCI\)[^.]*?(?:to|at) ([\d,]+) points, [^.]*?capesize bulk carriers [^.]*?(?:to|at) \$([\d,]+)\. The Baltic Panamax Index \(BPI\)[^.]*?(?:to|at) ([\d,]+) points, [^.]*?panamax bulk carriers [^.]*?(?:to|at) \$([\d,]+)\. The Baltic Supramax Index \(BSI\)[^.]*?(?:to|at) ([\d,]+) points, [^.]*?supramax bulk carriers [^.]*?(?:to|at) \$([\d,]+)\. The Baltic Handysize Index \(BHSI\)[^.]*?(?:to|at) ([\d,]+) points, [^.]*?handysize bulk carriers [^.]*?(?:to|at) \$([\d,]+)")
def handy(t):
    s=re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",t)).replace("&rsquo;","'")
    parts=re.split(r"(\d{1,2}-(?:January|February|March|April|May|June|July|August|September|October|November|December)-\d{4})",s)
    rows={}
    for i in range(1,len(parts)-1,2):
        dd,mm,yy=parts[i].split("-"); key=f"{yy}-{MON[mm]:02d}-{int(dd):02d}"; body=parts[i+1][:2500]; rec={}
        m=STRICT.match(body.strip())
        if m:
            v=[int(x.replace(",","")) for x in m.groups()]
            rows[key]=dict(bdi=v[0],bci=v[1],cape=v[2],bpi=v[3],pmx=v[4],bsi=v[5],smx=v[6],bhsi=v[7],handy=v[8]); continue
        for k,lab in LAB:
            m=re.search(lab+r"[^.;]*?(?:\bto\b|\bat\b|reaching|reached|stood at|settled at|closed at)\s+(?:a\s+[\w\s-]{0,30}?of\s+)?"+NUM,body)
            if m: rec[k]=int(m.group(1).replace(",",""))
        for k,lab in TC:
            m=re.search(lab+r"[^.;]*?(?:\bto\b|\bat\b)\s+\$"+NUM,body)
            if m: rec[k]=int(m.group(1).replace(",",""))
        if 200<rec.get("bdi",0)<12000: rows[key]=rec
    return rows
full=not H["series"].get("bdi")
start=datetime.date(2025,1,1) if full else (TODAY.replace(day=1)-datetime.timedelta(days=62)).replace(day=1)
d=start; rows={}
while d<=TODAY:
    rows.update(handy(get(f"https://www.handybulk.com/baltic-dry-index/{d.year}/{d.strftime('%B').lower()}/"))); time.sleep(0.4)
    d=(d.replace(day=28)+datetime.timedelta(days=4)).replace(day=1)
rows.update(handy(get("https://www.handybulk.com/baltic-dry-index/")))
for k in [x for x,_ in LAB]+[x for x,_ in TC]:
    pts=[[d,r[k]] for d,r in rows.items() if k in r]
    if pts: merge("series",k,pts); H["src"][k]="Baltic Exchange（經 HandyBulk 彙整）"
print("handybulk days",len(rows),file=sys.stderr)
# ---------- FRED ----------
FRED_D=[("brent","DCOILBRENTEU","FRED（美國能源資訊署 EIA）"),("wti","DCOILWTICO","FRED（EIA）"),("hh","DHHNGSP","FRED（EIA）"),("propane","DPROPANEMBTX","FRED（EIA，Mont Belvieu）")]
FRED_M=[("ironore","PIORECRUSDM","FRED（世界銀行／IMF，月均）"),("coal","PCOALAUUSDM","FRED（世界銀行／IMF，澳洲動力煤月均）")]
cosd=(TODAY-datetime.timedelta(days=int(6*365))).isoformat()
for kind,lst in ((() if os.environ.get("SKIP_FRED") else (("series",FRED_D),("monthly",FRED_M)))):
    for id_,sid,src in lst:
        t=get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&cosd={cosd}",timeout=30)
        if not t or not t.lstrip().lower().startswith(("observation_date","date")): print("fred miss",sid,file=sys.stderr); continue
        pts=[]
        for r in csv.reader(io.StringIO(t)):
            if len(r)<2 or not re.match(r"\d{4}-\d\d-\d\d",r[0]): continue
            try: pts.append([r[0] if kind=="series" else r[0][:8]+"15",round(float(r[1]),3)])
            except ValueError: pass
        if pts: merge(kind,id_,pts); H["src"][id_]=src; print("fred",sid,len(pts),file=sys.stderr)
        time.sleep(0.5)
# ---------- accumulate today's indicators ----------
I=load(ind_p) if ind_p else None
for it in (I or {}).get("items",[]):
    pts=[[d,v] for d,v in (it.get("series") or [])]
    if it.get("date") and isinstance(it.get("value"),(int,float)): pts.append([it["date"],it["value"]])
    if pts:
        merge("series",it["id"],pts); H["src"].setdefault(it["id"],it.get("source",""))
H["updated"]=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
json.dump(H,open(out_p,"w",encoding="utf-8"),ensure_ascii=False,separators=(",",":"))
print("hist ids",{k:len(v) for k,v in H["series"].items()},"monthly",{k:len(v) for k,v in H["monthly"].items()},file=sys.stderr)
