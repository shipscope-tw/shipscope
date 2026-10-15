"""IMF PortWatch daily chokepoint transits -> chokepoints.json.
Daily series for the last N days (shared date axis) + weekly averages since 2019-01-01 + pre-war baseline."""
import json, sys, urllib.request, urllib.parse, datetime, time, statistics
BASE="https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services/Daily_Chokepoints_Data/FeatureServer/0/query"
CPS=[("hormuz","Strait of Hormuz","荷姆茲海峽"),("bab","Bab el-Mandeb Strait","曼德海峽"),("suez","Suez Canal","蘇伊士運河"),("cape","Cape of Good Hope","好望角"),("panama","Panama Canal","巴拿馬運河"),("malacca","Malacca Strait","麻六甲海峽"),("taiwan","Taiwan Strait","台灣海峽"),("bosporus","Bosporus Strait","博斯普魯斯海峽")]
DAYS=int(sys.argv[2]) if len(sys.argv)>2 else 400
HIST_FROM="2019-01-01"
BASE_FROM,BASE_TO="2025-06-01","2026-02-27"   # pre-war window (war began 2026-02-28)
FIELDS="date,n_total,n_tanker,n_container,n_dry_bulk,n_general_cargo,n_roro"
def page(en,offset):
    p=urllib.parse.urlencode({"where":f"portname='{en}' AND date>='{HIST_FROM}'","outFields":FIELDS,"orderByFields":"date ASC","resultOffset":offset,"resultRecordCount":1000,"f":"json"})
    for i in range(6):
        try:
            j=json.load(urllib.request.urlopen(BASE+"?"+p,timeout=90))
            if "features" not in j: raise RuntimeError(str(j)[:200])
            return [x["attributes"] for x in j["features"]]
        except Exception as e: print("retry",en,offset,e,file=sys.stderr); time.sleep(5*(i+1))
    raise SystemExit("PortWatch unavailable")
def q(en):
    rows,off=[],0
    while True:
        b=page(en,off); rows+=b; off+=len(b)
        if len(b)<1000: return rows
data={k:{r["date"]:r for r in q(en)} for k,en,zh in CPS}
alld=sorted(set().union(*[set(v) for v in data.values()]))
dates=alld[-DAYS:]
def other(r): return (r["n_general_cargo"] or 0)+(r["n_roro"] or 0)
# weekly (Monday-start) averages since 2019
def wk(d): x=datetime.date.fromisoformat(d); return (x-datetime.timedelta(days=x.weekday())).isoformat()
weeks=sorted({wk(d) for d in alld})
last=datetime.date.fromisoformat(alld[-1])
if (last-datetime.date.fromisoformat(weeks[-1])).days<6: weeks=weeks[:-1]   # drop incomplete last week
out={"source":"IMF PortWatch（AIS 衛星/岸基船舶訊號）","source_url":"https://portwatch.imf.org/","fetched":datetime.date.today().isoformat(),"last_date":dates[-1],"baseline_window":[BASE_FROM,BASE_TO],"d":dates,"cps":{},"w":{"d":weeks,"from":HIST_FROM,"cps":{}}}
for k,en,zh in CPS:
    rows=[data[k].get(d) for d in dates]
    g=lambda f:[(r[f] if r else None) for r in rows]
    bt=[r["n_total"] for d,r in data[k].items() if BASE_FROM<=d<=BASE_TO]
    btk=[r["n_tanker"] for d,r in data[k].items() if BASE_FROM<=d<=BASE_TO]
    out["cps"][k]={"en":en,"zh":zh,"total":g("n_total"),"tanker":g("n_tanker"),"container":g("n_container"),"dry_bulk":g("n_dry_bulk"),"other":[(other(r) if r else None) for r in rows],"base_total":round(statistics.mean(bt),1) if bt else None,"base_tanker":round(statistics.mean(btk),1) if btk else None}
    acc={w:{"total":[],"tanker":[],"container":[],"dry_bulk":[],"other":[]} for w in weeks}
    for d,r in data[k].items():
        w=wk(d)
        if w in acc:
            for f in ("total","tanker","container","dry_bulk"): acc[w][f].append(r["n_"+f] or 0)
            acc[w]["other"].append(other(r))
    avg=lambda a: round(sum(a)/len(a),1) if a else None
    out["w"]["cps"][k]={f:[avg(acc[w][f]) for w in weeks] for f in ("total","tanker","container","dry_bulk","other")}
    print(k,dates[-1],out["cps"][k]["total"][-1],out["cps"][k]["base_total"],"weeks",len(weeks),file=sys.stderr)
json.dump(out,open(sys.argv[1],"w",encoding="utf-8"),ensure_ascii=False,separators=(",",":"))
