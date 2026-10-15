"""Fetch latest shipping/energy indicators with as-of dates -> indicators.json"""
import json, re, sys, html, urllib.request, datetime, time
UA={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36"}
def get(url):
    for i in range(3):
        try: return urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=40).read().decode("utf8","ignore")
        except Exception as e: err=e; time.sleep(3)
    print("FAIL",url,err,file=sys.stderr); return ""
MON={m:i for i,m in enumerate(["January","February","March","April","May","June","July","August","September","October","November","December"],1)}
def pdate(s):
    m=re.match(r"(\d{1,2})-([A-Za-z]+)-(\d{4})",s)
    if m: return f"{m.group(3)}-{MON[m.group(2)]:02d}-{int(m.group(1)):02d}"
    m=re.match(r"([A-Za-z]+) (\d{1,2}), (\d{4})",s)
    return f"{m.group(3)}-{MON[m.group(1)]:02d}-{int(m.group(2)):02d}"
out=[]
def add(**k): out.append(k)
# ---- Dry bulk: handybulk daily (current + archive months) ----
def handy(url):
    t=re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",get(url))); rows={}
    for m in re.finditer(r"(\d{1,2}-[A-Za-z]+-\d{4}) The Baltic Dry Index \(BDI\).*?to (?:reach )?([\d,]+) points\. The Baltic Capesize Index \(BCI\).*?(?:to|at) ([\d,]+) points, .*?capesize bulk carriers .*?(?:to|at) \$([\d,]+)\. The Baltic Panamax Index \(BPI\).*?(?:to|at) ([\d,]+) points, .*?panamax bulk carriers .*?(?:to|at) \$([\d,]+)\. The Baltic Supramax Index \(BSI\).*?(?:to|at) ([\d,]+) points, .*?supramax bulk carriers .*?(?:to|at) \$([\d,]+)\. The Baltic Handysize Index \(BHSI\).*?(?:to|at) ([\d,]+) points, .*?handysize bulk carriers .*?(?:to|at) \$([\d,]+)",t):
        v=[int(x.replace(",","")) for x in m.groups()[1:]]
        rows[pdate(m.group(1))]=dict(BDI=v[0],BCI=v[1],CAPE=v[2],BPI=v[3],PMX=v[4],BSI=v[5],SMX=v[6],BHSI=v[7],HANDY=v[8])
    return rows
today=datetime.date.today(); rows={}
for back in range(0,3):
    d=(today.replace(day=1)-datetime.timedelta(days=31*back)).replace(day=1)
    rows.update(handy(f"https://www.handybulk.com/baltic-dry-index/{d.year}/{d.strftime('%B').lower()}/"))
rows.update(handy("https://www.handybulk.com/baltic-dry-index/"))
ds=sorted(rows)
meta={"BDI":("BDI 波羅的海綜合指數","Baltic Dry Index","點","散裝"),"BCI":("BCI 海岬型指數","Capesize","點","散裝"),"BPI":("BPI 巴拿馬型指數","Panamax","點","散裝"),"BSI":("BSI 超輕便極限型指數","Supramax","點","散裝"),"BHSI":("BHSI 輕便型指數","Handysize","點","散裝"),"CAPE":("海岬型平均日租 (5TC)","Capesize avg T/C","US$/日","散裝"),"PMX":("巴拿馬型平均日租","Panamax avg T/C","US$/日","散裝"),"SMX":("超輕便極限型平均日租","Supramax avg T/C","US$/日","散裝"),"HANDY":("輕便型平均日租","Handysize avg T/C","US$/日","散裝")}
if ds:
    for k,(zh,en,u,sec) in meta.items():
        ser=[[d,rows[d][k]] for d in ds]
        last=ser[-1]; prev=ser[-2] if len(ser)>1 else None
        add(id=k.lower(),name=zh,en=en,sector=sec,value=last[1],unit=u,date=last[0],chg=(last[1]-prev[1]) if prev else None,chg_label="較前一交易日",series=ser[-60:],freq="日",source="Baltic Exchange（經 HandyBulk 彙整）",source_url="https://www.handybulk.com/baltic-dry-index/")
# ---- Containers: SSE SCFI / CCFI ----
for code,zh,en in [("scfi","SCFI 上海出口集裝箱運價指數","Shanghai Containerized Freight Index"),("ccfi","CCFI 中國出口集裝箱運價指數","China Containerized Freight Index")]:
    try:
        d=json.loads(get(f"https://en.sse.net.cn/currentIndex?indexName={code}"))["data"]; l=d["lineDataList"][0]
        add(id=code,name=zh,en=en,sector="貨櫃",value=round(l["currentContent"],2),unit="點",date=d["currentDate"],chg=round(l["absolute"],2),chg_label=f"較上期 ({d['lastDate']})",series=[[d["lastDate"],round(l["lastContent"],2)],[d["currentDate"],round(l["currentContent"],2)]],freq="週",source="上海航運交易所",source_url="https://en.sse.net.cn/indices/scfinew.jsp" if code=="scfi" else "https://en.sse.net.cn/indices/ccfinew.jsp")
    except Exception as e: print("SSE fail",code,e,file=sys.stderr)
# ---- Drewry WCI ----
t=get("https://www.drewry.co.uk/supply-chain-advisors/supply-chain-expertise/world-container-index-assessed-by-drewry")
s=re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",t)); dp=re.findall(r'datePublished"\s*:\s*"(\d{4}-\d\d-\d\d)',t)
m=re.search(r"WCI\), the benchmark[^.]*?(fell|rose|increased|decreased|remained stable|was stable)[^$]*?\$([\d,]+) per 40ft",s)
if m and dp:
    routes=re.findall(r"from (Shanghai) to ([A-Za-z ]+?) (?:fell|rose|increased|decreased|remained stable at|was stable at|declined|grew)[^$]*?\$([\d,]+) per 40ft",s) + re.findall(r"(Shanghai) to ([A-Za-z ]+?) (?:fell|rose|increased|decreased|remained stable at|declined|grew)[^$]*?\$([\d,]+) per 40ft",s)
    rt={}; [rt.setdefault(b.strip(),int(c.replace(",",""))) for a,b,c in routes]
    add(id="wci",name="Drewry WCI 世界貨櫃指數（綜合）",en="Drewry World Container Index",sector="貨櫃",value=int(m.group(2).replace(",","")),unit="US$/40呎櫃",date=dp[0],chg=None,chg_label="",note="；".join(f"上海→{k} ${v:,}" for k,v in rt.items()),series=[],freq="週",source="Drewry",source_url="https://www.drewry.co.uk/supply-chain-advisors/supply-chain-expertise/world-container-index-assessed-by-drewry")
# ---- Singapore VLSFO (Ship & Bunker) ----
t=get("https://shipandbunker.com/prices/apac/sea/sg-sin-singapore")
for fuel,zh in [("VLSFO","新加坡 VLSFO 極低硫燃油"),("MGO","新加坡 MGO 船用柴油")]:
    i=t.find(f'caption="{fuel} in Singapore"')
    if i>0:
        seg=re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",t[i:i+6000]))
        rr=re.findall(r"\b[A-Z]?\s?(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{1,2}) ([\d,.]+) ([+-][\d.]+|unch)",seg)
        if rr:
            ser=[]
            for mo,dd,v,c in rr:
                mi=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"].index(mo)+1
                y=today.year if mi<=today.month else today.year-1
                ser.append([f"{y}-{mi:02d}-{int(dd):02d}",float(v.replace(",",""))])
            ser.sort(); last=ser[-1]
            add(id=fuel.lower(),name=zh,en=f"Singapore {fuel}",sector="成本",value=last[1],unit="US$/公噸",date=last[0],chg=round(last[1]-ser[-2][1],2) if len(ser)>1 else None,chg_label="較前一日",series=ser,freq="日",source="Ship & Bunker",source_url="https://shipandbunker.com/prices/apac/sea/sg-sin-singapore")
# ---- Trading Economics (energy & raw materials) ----
TE=[("brent","brent-crude-oil","Brent 布蘭特原油","Brent crude","US$/桶","油輪"),("wti","crude-oil","WTI 原油","WTI crude","US$/桶","油輪"),("ttf","eu-natural-gas","TTF 歐洲天然氣","EU natural gas TTF","€/MWh","LNG"),("hh","natural-gas","Henry Hub 美國天然氣","US natural gas","US$/MMBtu","LNG"),("propane","propane","丙烷（Mont Belvieu）","Propane","US$/加侖","LPG"),("ironore","iron-ore","鐵礦砂 (62% Fe)","Iron ore","US$/公噸","散裝"),("coal","coal","Newcastle 煤炭","Coal","US$/公噸","散裝"),("soy","soybeans","黃豆","Soybeans","US¢/英斗","散裝"),("steel","steel","中國螺紋鋼","Steel rebar","CNY/公噸","散裝")]
for id_,slug,zh,en,u,sec in TE:
    t=html.unescape(get(f"https://tradingeconomics.com/commodity/{slug}"))
    md=re.search(r'name="description" content="([^"]*)"',t)
    if not md: print("TE miss",slug,file=sys.stderr); continue
    desc=md.group(1)
    m=re.search(r"(?:rose|fell|traded flat|increased|decreased|was unchanged)(?: to| at)? ([\d,.]+) \S+ on ([A-Z][a-z]+ \d{1,2}, \d{4})",desc)
    if not m: print("TE miss2",slug,file=sys.stderr); continue
    v=float(m.group(1).replace(",","")); d=pdate(m.group(2))
    a=re.search(r"(up|down) ([\d.]+)% from the previous day",desc); dd=((1 if a.group(1)=="up" else -1)*float(a.group(2))) if a else 0.0
    a=re.search(r"past month, .*? (risen|fallen|gained|lost|declined|increased|decreased) ([\d.]+)%",desc); m1=((1 if a.group(1) in("risen","gained","increased") else -1)*float(a.group(2))) if a else None
    a=re.search(r"([\d.]+)% (higher|lower) than a year ago",desc) 
    if a: y1=(1 if a.group(2)=="higher" else -1)*float(a.group(1))
    else:
        a=re.search(r"is (up|down) ([\d.]+)% compared to the same time last year",desc); y1=((1 if a.group(1)=="up" else -1)*float(a.group(2))) if a else None
    add(id=id_,name=zh,en=en,sector=sec,value=v,unit=u,date=d,chg_pct=dd,chg_label="日變動",m1_pct=m1,y1_pct=y1,series=[],freq="日",source="Trading Economics",source_url=f"https://tradingeconomics.com/commodity/{slug}")
    time.sleep(1)
json.dump({"fetched":datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),"items":out},open(sys.argv[1],"w"),ensure_ascii=False)
for o in out: print(o["id"],o["value"],o["unit"],o["date"],file=sys.stderr)
