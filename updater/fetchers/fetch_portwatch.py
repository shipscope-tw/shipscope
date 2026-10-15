"""IMF PortWatch daily chokepoint transits -> chokepoints.json (shared date axis, last N days, pre-war baseline)."""
import json, sys, urllib.request, urllib.parse, datetime, time, statistics
BASE="https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services/Daily_Chokepoints_Data/FeatureServer/0/query"
CPS=[("hormuz","Strait of Hormuz","荷姆茲海峽"),("bab","Bab el-Mandeb Strait","曼德海峽"),("suez","Suez Canal","蘇伊士運河"),("cape","Cape of Good Hope","好望角"),("panama","Panama Canal","巴拿馬運河"),("malacca","Malacca Strait","麻六甲海峽"),("taiwan","Taiwan Strait","台灣海峽"),("bosporus","Bosporus Strait","博斯普魯斯海峽")]
DAYS=int(sys.argv[2]) if len(sys.argv)>2 else 400
BASE_FROM,BASE_TO="2025-06-01","2026-02-27"   # pre-war window (war began 2026-02-28)
def q(en):
    p=urllib.parse.urlencode({"where":f"portname='{en}'","outFields":"date,n_total,n_tanker,n_container,n_dry_bulk,n_general_cargo,n_roro","orderByFields":"date DESC","resultRecordCount":DAYS,"f":"json"})
    for i in range(6):
        try: return [x["attributes"] for x in json.load(urllib.request.urlopen(BASE+"?"+p,timeout=60))["features"]]
        except Exception as e: print("retry",en,e,file=sys.stderr); time.sleep(5*(i+1))
    raise SystemExit("PortWatch unavailable")
data={k:{r["date"]:r for r in q(en)} for k,en,zh in CPS}
dates=sorted(set().union(*[set(v) for v in data.values()]))[-DAYS:]
out={"source":"IMF PortWatch（AIS 衛星/岸基船舶訊號）","source_url":"https://portwatch.imf.org/","fetched":datetime.date.today().isoformat(),"last_date":dates[-1],"baseline_window":[BASE_FROM,BASE_TO],"d":dates,"cps":{}}
for k,en,zh in CPS:
    rows=[data[k].get(d) for d in dates]
    g=lambda f:[(r[f] if r else None) for r in rows]
    other=[(r["n_general_cargo"]+r["n_roro"]) if r else None for r in rows]
    bt=[r["n_total"] for d,r in data[k].items() if BASE_FROM<=d<=BASE_TO]
    btk=[r["n_tanker"] for d,r in data[k].items() if BASE_FROM<=d<=BASE_TO]
    out["cps"][k]={"en":en,"zh":zh,"total":g("n_total"),"tanker":g("n_tanker"),"container":g("n_container"),"dry_bulk":g("n_dry_bulk"),"other":other,"base_total":round(statistics.mean(bt),1) if bt else None,"base_tanker":round(statistics.mean(btk),1) if btk else None}
    print(k,dates[-1],out["cps"][k]["total"][-1],out["cps"][k]["base_total"],file=sys.stderr)
json.dump(out,open(sys.argv[1],"w"),ensure_ascii=False,separators=(",",":"))
