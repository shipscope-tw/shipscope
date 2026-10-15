"""IMF PortWatch port calls for ~70 major ports -> ports.json
Monthly average port calls per day since 2019-01 (total, container, tanker, dry bulk) + same-month 2019 baseline."""
import json, sys, urllib.request, urllib.parse, datetime, time
B="https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services/"
PORTS=[("port1201","新加坡"),("port1188","上海"),("port824","寧波"),("port1189","深圳蛇口"),("port1414","深圳鹽田"),("port425","廣州南沙"),("port1069","青島"),("port1297","天津"),("port273","大連"),("port1404","廈門"),("port1072","秦皇島"),("port474","香港"),
 ("port1065","釜山"),("port1338","蔚山"),("port541","高雄"),("port1252","台中"),("port238","基隆"),("port1417","橫濱"),("port786","名古屋"),("port581","神戶"),
 ("port960","巴生港"),("port1269","丹戎帕拉帕斯"),("port514","雅加達（丹戎不碌）"),("port1291","胡志明市"),("port434","海防"),("port1197","林查班"),("port694","馬尼拉"),
 ("port254","可倫坡"),("port776","孟買（那瓦舍瓦）"),("port241","吉大港"),("port540","坎德拉"),
 ("port744","杰貝阿里"),("port362","富查伊拉"),("port1091","拉斯坦努拉"),("port518","吉達"),("port746","塞拉萊"),("port192","塞得港"),
 ("port1114","鹿特丹"),("port57","安特衛普"),("port446","漢堡"),("port168","不來梅港"),("port985","勒阿弗爾"),("port343","費利克斯托"),("port1348","瓦倫西亞"),("port31","阿爾赫西拉斯"),("port908","比雷埃夫斯"),("port380","格但斯克"),("port504","伊斯坦堡"),("port833","新羅西斯克"),
 ("port664","洛杉磯／長灘"),("port815","紐約／紐澤西"),("port1170","薩凡納"),("port481","休士頓"),("port264","科珀斯克里斯蒂"),("port2388","薩賓帕斯"),("port812","紐奧良"),("port1350","溫哥華"),("port699","曼薩尼約（墨西哥）"),("port700","曼薩尼約（巴拿馬）"),("port1160","桑托斯"),("port1045","卡亞俄"),
 ("port311","德班"),("port1099","理查茲灣"),("port626","拉哥斯"),("port757","蒙巴薩"),("port955","黑德蘭港"),("port276","丹皮爾"),("port816","紐卡索（澳洲）")]
FROM="2019-01-01"
def get(url,params):
    p=urllib.parse.urlencode(params)
    for i in range(6):
        try:
            j=json.load(urllib.request.urlopen(url+"?"+p,timeout=120))
            if "features" not in j: raise RuntimeError(str(j)[:200])
            return [x["attributes"] for x in j["features"]]
        except Exception as e: print("retry",e,file=sys.stderr); time.sleep(5*(i+1))
    raise SystemExit("PortWatch ports unavailable")
ids=[p for p,_ in PORTS]; zh=dict(PORTS)
inlist=lambda xs:"("+",".join(f"'{x}'" for x in xs)+")"
meta={r["portid"]:r for r in get(B+"PortWatch_ports_database/FeatureServer/0/query",{"where":f"portid IN {inlist(ids)}","outFields":"portid,portname,ISO3,country,lat,lon","resultRecordCount":200,"f":"json"})}
F=["portcalls","portcalls_container","portcalls_tanker","portcalls_dry_bulk","export_container","import_container"]
stats=json.dumps([{"statisticType":"sum","onStatisticField":f,"outStatisticFieldName":f} for f in F]+[{"statisticType":"count","onStatisticField":"portcalls","outStatisticFieldName":"ndays"}])
rows=[]
for i in range(0,len(ids),8):
    rows+=get(B+"Daily_Ports_Data/FeatureServer/0/query",{"where":f"portid IN {inlist(ids[i:i+8])} AND date>='{FROM}'","groupByFieldsForStatistics":"portid,year,month","outStatistics":stats,"resultRecordCount":2000,"f":"json"})
    print("ports batch",i,len(rows),file=sys.stderr)
cell={(r["portid"],f"{r['year']}-{r['month']:02d}"):r for r in rows}
months=sorted({m for _,m in cell})
# drop a trailing month with too few days of data
while months and max((cell.get((p,months[-1]),{}).get("ndays") or 0) for p in ids)<7: months.pop()
r1=lambda x: None if x is None else round(x,1)
nd_last=max((cell.get((p,months[-1]),{}).get("ndays") or 0) for p in ids) if months else 0
out={"source":"IMF PortWatch（AIS 到港艘次與貨量估算）","source_url":"https://portwatch.imf.org/","fetched":datetime.date.today().isoformat(),"months":months,"ndays_last":nd_last,"ports":[]}
for pid in ids:
    m=meta.get(pid)
    if not m: print("missing meta",pid,file=sys.stderr); continue
    ser={f:[] for f in F}
    for mo in months:
        c=cell.get((pid,mo)); nd=(c or {}).get("ndays") or 0
        for f in F: ser[f].append((r1(c[f]/nd) if not f.startswith(('export','import')) else c[f]/nd) if c and nd and c[f] is not None else None)
    base=[]
    for mm in range(1,13):
        c=cell.get((pid,f"2019-{mm:02d}")); nd=(c or {}).get("ndays") or 0
        base.append(r1(c["portcalls"]/nd) if c and nd else None)
    kt=lambda xs:[None if x is None else round(x/1000,1) for x in xs]   # tonnes/day -> thousand tonnes/day
    out["ports"].append({"id":pid,"zh":zh[pid],"en":m["portname"],"iso":m["ISO3"],"lat":round(m["lat"],3),"lon":round(m["lon"],3),"calls":ser["portcalls"],"ctr":ser["portcalls_container"],"tnk":ser["portcalls_tanker"],"blk":ser["portcalls_dry_bulk"],"exc":kt(ser["export_container"]),"imc":kt(ser["import_container"]),"base2019":base})
print("ports",len(out["ports"]),"months",months[0],months[-1],file=sys.stderr)
json.dump(out,open(sys.argv[1],"w",encoding="utf-8"),ensure_ascii=False,separators=(",",":"))
