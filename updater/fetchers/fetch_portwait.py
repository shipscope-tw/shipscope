"""Port delay / waiting time for ~60 major ports -> portwait.json
Usage: python fetch_portwait.py <out.json> [prev_portwait.json]
Source: GoComet public port-congestion page (delay in days, estimated from its shipment/vessel tracking).
Keeps a daily history of the headline delay so trends build up over time."""
import json, re, sys, time, datetime, urllib.request
out_p=sys.argv[1]; prev_p=sys.argv[2] if len(sys.argv)>2 else None
URL="https://www.gocomet.com/real-time-port-congestion"
ZH={"CNSHG":"上海","CNNBO":"寧波","CNSHK":"深圳蛇口","CNYTN":"深圳鹽田","CNNSA":"廣州南沙","CNTXG":"天津新港","CNDLC":"大連","CNQDG":"青島","CNTAO":"青島","CNXMN":"廈門","HKHKG":"香港",
    "TWKHH":"高雄","TWTXG":"台中","TWKEL":"基隆","KRPUS":"釜山","JPTYO":"東京","JPYOK":"橫濱","JPNGO":"名古屋","JPUKB":"神戶",
    "SGSIN":"新加坡","MYPKG":"巴生港","MYTPP":"丹戎帕拉帕斯","IDJKT":"雅加達","IDTPP":"雅加達（丹戎不碌）","VNSGN":"胡志明市（西貢港）","VNCMT":"蓋梅","VNVUT":"頭頓","VNHPH":"海防","THLCH":"林查班","PHMNL":"馬尼拉",
    "LKCMB":"可倫坡","INNSA":"孟買（那瓦舍瓦）","INMUN":"蒙德拉","AEJEA":"杰貝阿里","OMSLL":"塞拉萊","SAJED":"吉達","EGPSD":"塞得港",
    "NLRTM":"鹿特丹","BEANR":"安特衛普","DEHAM":"漢堡","DEBRV":"不來梅港","FRLEH":"勒阿弗爾","GBFXT":"費利克斯托","ESVLC":"瓦倫西亞","ESALG":"阿爾赫西拉斯","GRPIR":"比雷埃夫斯",
    "USLAX":"洛杉磯","USLGB":"長灘","USNYC":"紐約／紐澤西","USSAV":"薩凡納","USHOU":"休士頓","CAVAN":"溫哥華","MXZLO":"曼薩尼約（墨西哥）","PAMIT":"曼薩尼約（巴拿馬）",
    "BRSSZ":"桑托斯","ZADUR":"德班","KEMBA":"蒙巴薩","NGLOS":"拉哥斯"}
EN={"CAVAN": "Vancouver", "NGLOS": "Lagos (Apapa)", "INNSA": "Nhava Sheva (JNPT)", "TWKEL": "Keelung", "CNTXG": "Tianjin Xingang", "VNSGN": "Ho Chi Minh City", "PAMIT": "Manzanillo (Panama)", "MXZLO": "Manzanillo (Mexico)"}
REG={"CN":"東北亞","HK":"東北亞","TW":"東北亞","KR":"東北亞","JP":"東北亞","SG":"東南亞","MY":"東南亞","ID":"東南亞","VN":"東南亞","TH":"東南亞","PH":"東南亞",
     "LK":"南亞・中東","IN":"南亞・中東","AE":"南亞・中東","OM":"南亞・中東","SA":"南亞・中東","EG":"南亞・中東","NL":"歐洲","BE":"歐洲","DE":"歐洲","FR":"歐洲","GB":"歐洲","ES":"歐洲","GR":"歐洲",
     "US":"美洲","CA":"美洲","MX":"美洲","PA":"美洲","BR":"美洲","ZA":"非洲","KE":"非洲","NG":"非洲"}
try: P=json.load(open(prev_p,encoding="utf-8")); P=P.get("data",P) if "ports" not in P else P
except Exception: P={}
t=""
for i in range(3):
    try: t=urllib.request.urlopen(urllib.request.Request(URL,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"}),timeout=60).read().decode("utf8","ignore"); break
    except Exception as e: print("retry",e,file=sys.stderr); time.sleep(5)
m=re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>',t,re.S)
rows=[]
if m:
    try: rows=json.loads(m.group(1))["props"]["pageProps"]["ssrCongestionData"]
    except Exception as e: print("parse fail",e,file=sys.stderr)
if not rows:
    print("GoComet unavailable, keeping previous",file=sys.stderr); json.dump(P or {"ports":[],"hist":{}},open(out_p,"w",encoding="utf-8"),ensure_ascii=False,separators=(",",":")); sys.exit(0)
today=datetime.date.today().isoformat(); seen=set(); ports=[]
for r in rows:
    p=r.get("port") or {}; c=p.get("code")
    if c not in ZH or c in seen: continue          # first entry per UN/LOCODE = main terminal
    seen.add(c)
    ports.append({"code":c,"zh":ZH[c],"en":EN.get(c) or (p.get("display_name") or "").split(",")[0],"cc":(p.get("country_code") or "").upper(),"reg":REG.get(c[:2],"其他"),"lat":p.get("lat"),"lon":p.get("lon"),
                  "d":p.get("delay"),"w":r.get("weekly_median_delay"),"wmax":r.get("weekly_max_delay"),"f":r.get("fortnightly_median_delay"),"m":r.get("monthly_median_delay"),"lvl":p.get("delayLevel")})
hist=P.get("hist",{}); cut=(datetime.date.today()-datetime.timedelta(days=800)).isoformat()
for p in ports:
    if p["d"] is None: continue
    h=[x for x in hist.get(p["code"],[]) if x[0]>=cut and x[0]!=today]; h.append([today,p["d"]]); hist[p["code"]]=h
json.dump({"source":"GoComet Port Congestion（依其平台的貨櫃追蹤、船期與 AIS 推估）","source_url":URL,"fetched":today,"ports":ports,"hist":hist},open(out_p,"w",encoding="utf-8"),ensure_ascii=False,separators=(",",":"))
print("portwait",len(ports),"ports",file=sys.stderr)
