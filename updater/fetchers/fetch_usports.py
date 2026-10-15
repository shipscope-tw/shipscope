"""IMF PortWatch daily port calls / exports for key US ports -> usports.json"""
import json,sys,urllib.request,urllib.parse,datetime,time,statistics
B="https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services/Daily_Ports_Data/FeatureServer/0/query"
PORTS=[("port481","休士頓","Houston, TX",29.72,-95.14,"原油・成品油・LPG 最大出口港"),("port264","科珀斯克里斯蒂","Corpus Christi, TX",27.84,-97.38,"美國最大原油出口港（二疊紀盆地）"),("port932","阿蘭瑟斯港／Ingleside","Port Aransas, TX",27.85,-97.07,"VLCC 原油裝載"),("port134","博蒙特","Beaumont, TX",30.03,-94.03,"原油・成品油"),("port933","亞瑟港","Port Arthur, TX",29.88,-93.93,"煉油・原油出口"),("port2388","賽濱隘口","Sabine Pass, LA",29.75,-93.89,"Cheniere LNG 出口"),("port629","查爾斯湖","Lake Charles, LA",30.19,-93.31,"Cameron LNG・煉油"),("port2480","卡爾克蘇隘口 LNG","Calcasieu Pass, LA",29.79,-93.33,"Venture Global LNG"),("port2329","普拉克明","Plaquemines, LA",29.62,-89.9,"Venture Global LNG"),("port1214","南路易斯安那","South Louisiana",30.12,-90.87,"穀物・原油・化學品"),("port812","紐奧良","New Orleans, LA",29.93,-90.13,"穀物・成品油"),("port358","自由港（德州）","Freeport, TX",28.94,-95.33,"Freeport LNG・化學品"),("port1285","德州城","Texas City, TX",29.38,-94.91,"煉油・成品油"),("port1241","瓦爾迪茲（阿拉斯加）","Valdez/Swanport, AK",61.08,-146.38,"阿拉斯加原油"),("port664","洛杉磯／長灘","Los Angeles-Long Beach",33.76,-118.24,"美國最大貨櫃港"),("port815","紐約／新澤西","New York-New Jersey",40.67,-74.15,"東岸最大貨櫃港"),("port1170","薩凡納","Savannah, GA",32.08,-81.09,"東岸貨櫃港")]
FROM=sys.argv[2] if len(sys.argv)>2 else (datetime.date.today()-datetime.timedelta(days=500)).isoformat()
BF,BT="2025-06-01","2026-02-27"
def q(pid):
    rows=[];off=0
    while True:
        p=urllib.parse.urlencode({"where":f"portid='{pid}' AND date>='{FROM}'","outFields":"date,portcalls,portcalls_tanker,portcalls_container,export_tanker,export,import","orderByFields":"date ASC","resultOffset":off,"resultRecordCount":1000,"f":"json"})
        for i in range(6):
            try: d=json.load(urllib.request.urlopen(B+"?"+p,timeout=90)); break
            except Exception as e: print("retry",pid,e,file=sys.stderr); time.sleep(5*(i+1))
        else: raise SystemExit("PortWatch ports unavailable")
        f=[x["attributes"] for x in d.get("features",[])]; rows+=f
        if len(f)<1000: return rows
        off+=1000
data={p[0]:{r["date"]:r for r in q(p[0])} for p in PORTS}
dates=sorted(set().union(*[set(v) for v in data.values()]))
out={"source":"IMF PortWatch（AIS 推估靠港與裝卸量）","source_url":"https://portwatch.imf.org/","fetched":datetime.date.today().isoformat(),"last_date":dates[-1],"baseline_window":[BF,BT],"d":dates,"ports":[]}
for pid,zh,en,lat,lon,role in PORTS:
    rr=[data[pid].get(d) for d in dates]
    calls=[r["portcalls"] if r else None for r in rr]; tk=[r["portcalls_tanker"] if r else None for r in rr]
    ext=[round(r["export_tanker"]/1000) if r else None for r in rr]; ctn=[r["portcalls_container"] if r else None for r in rr]
    base=[r for d,r in data[pid].items() if BF<=d<=BT]
    m=lambda k:round(statistics.mean([r[k] for r in base]),2) if base else None
    out["ports"].append(dict(id=pid,zh=zh,en=en,lat=lat,lon=lon,role=role,calls=calls,tanker=tk,container=ctn,exp_tanker_kt=ext,base_calls=m("portcalls"),base_tanker=m("portcalls_tanker"),base_container=m("portcalls_container"),base_exp_tanker_kt=round(statistics.mean([r["export_tanker"] for r in base])/1000,1) if base else None))
    print(zh,len(base),out["ports"][-1]["base_tanker"],file=sys.stderr)
json.dump(out,open(sys.argv[1],"w"),ensure_ascii=False,separators=(",",":"))
