"""Trade-flow evidence for the trade-lane page -> trade.json
Usage: python fetch_trade.py <out.json> [prev_trade.json]
- IMF IMTS (monthly bilateral goods trade, US$, since 2019): who ships to whom
- Trading Economics: latest-month headline (customs releases, faster than IMF)
- UN Comtrade (annual, HS 2-digit): what is being shipped
Any source that fails keeps the previous data."""
import json, re, sys, time, html, datetime, urllib.request
out_p=sys.argv[1]; prev_p=sys.argv[2] if len(sys.argv)>2 else None
def get(url,timeout=90,ua="Mozilla/5.0"):
    for i in range(3):
        try: return urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":ua}),timeout=timeout).read().decode("utf8","ignore")
        except Exception as e: err=e; time.sleep(3+3*i)
    print("FAIL",url[:100],err,file=sys.stderr); return ""
try: P=json.load(open(prev_p,encoding="utf-8")); P=P.get("data",P) if "flows" not in P else P
except Exception: P={}
O={"updated":datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),"flows":P.get("flows",{}),"months":P.get("months",[]),"latest":P.get("latest",[]),"hs":P.get("hs",{}),
   "src":{"imf":"IMF International Merchandise Trade Statistics (IMTS)","te":"Trading Economics（原始資料：各國海關／統計局）","hs":"UN Comtrade（HS 2 位碼，年資料）"}}
# ---------- IMF IMTS monthly ----------
ASEAN=["VNM","THA","IDN","MYS","SGP","PHL","KHM"]
FLOWS=[  # id, reporter, indicator, partner(s), zh, en
 ("cn_x_world","CHN","XG_FOB_USD",["G001"],"中國出口：全球","China exports: world"),
 ("cn_x_us","CHN","XG_FOB_USD",["USA"],"中國出口：美國","China exports: US"),
 ("cn_x_eu","CHN","XG_FOB_USD",["G998"],"中國出口：歐盟","China exports: EU"),
 ("cn_x_asean","CHN","XG_FOB_USD",ASEAN,"中國出口：東協（7 國）","China exports: ASEAN-7"),
 ("cn_x_vn","CHN","XG_FOB_USD",["VNM"],"中國出口：越南","China exports: Vietnam"),
 ("cn_x_in","CHN","XG_FOB_USD",["IND"],"中國出口：印度","China exports: India"),
 ("vn_m_cn","VNM","MG_CIF_USD",["CHN"],"越南進口：來自中國","Vietnam imports from China"),
 ("vn_x_us","VNM","XG_FOB_USD",["USA"],"越南出口：美國","Vietnam exports: US"),
 ("vn_x_world","VNM","XG_FOB_USD",["G001"],"越南出口：全球","Vietnam exports: world"),
 ("us_m_world","USA","MG_CIF_USD",["G001"],"美國進口：全球","US imports: world"),
 ("us_m_cn","USA","MG_CIF_USD",["CHN"],"美國進口：來自中國","US imports from China"),
 ("us_m_vn","USA","MG_CIF_USD",["VNM"],"美國進口：來自越南","US imports from Vietnam"),
 ("us_m_mx","USA","MG_CIF_USD",["MEX"],"美國進口：來自墨西哥","US imports from Mexico"),
 ("us_m_tw","USA","MG_CIF_USD",["TWN"],"美國進口：來自台灣","US imports from Taiwan"),
 ("in_m_cn","IND","MG_CIF_USD",["CHN"],"印度進口：來自中國","India imports from China"),
]
reps=sorted({f[1] for f in FLOWS}); inds=sorted({f[2] for f in FLOWS}); parts=sorted({p for f in FLOWS for p in f[3]})
x=get(f"https://api.imf.org/external/sdmx/2.1/data/IMF.STA,IMTS/{'+'.join(reps)}.{'+'.join(inds)}.{'+'.join(parts)}.M?startPeriod=2019-01",timeout=180)
cell={}
for m in re.finditer(r"<Series ([^>]*)>(.*?)</Series>",x,re.S):
    a=dict(re.findall(r'(\w+)="([^"]*)"',m.group(1)))
    for tp,v in re.findall(r'TIME_PERIOD="(\d{4}-M\d\d)" OBS_VALUE="([^"]+)"',m.group(2)):
        try: cell[(a["COUNTRY"],a["INDICATOR"],a["COUNTERPART_COUNTRY"],tp.replace("-M","-"))]=float(v)
        except ValueError: pass
if cell:
    months=sorted({k[3] for k in cell}); flows={}
    for id_,r,ind,ps,zh,en in FLOWS:
        ser=[]
        for mo in months:
            vs=[cell.get((r,ind,p,mo)) for p in ps]
            ser.append(round(sum(vs)/1e9,3) if all(v is not None for v in vs) else None)
        while ser and ser[-1] is None: ser.pop()
        if any(v is not None for v in ser): flows[id_]={"zh":zh,"en":en,"rep":r,"v":ser}
    # drop trailing months where most flows are still missing
    n=max(len(f["v"]) for f in flows.values()); months=months[:n]
    O["flows"]=flows; O["months"]=months
    print("imf months",months[0],months[-1],"flows",len(flows),file=sys.stderr)
else: print("IMF failed, keeping previous",file=sys.stderr)
# ---------- Trading Economics latest-month headlines ----------
TEP=[("cn_x","china/exports","中國出口","China exports"),("cn_m","china/imports","中國進口","China imports"),("vn_x","vietnam/exports","越南出口","Vietnam exports"),("vn_m","vietnam/imports","越南進口","Vietnam imports"),
     ("tw_x","taiwan/exports","台灣出口","Taiwan exports"),("kr_x","south-korea/exports","韓國出口","South Korea exports")]
PZ={"US":"美國","USA":"美國","United States":"美國","EU":"歐盟","European Union":"歐盟","ASEAN":"東協","ASEAN countries":"東協","Japan":"日本","South Korea":"韓國","Korea":"韓國","China":"中國","Taiwan":"台灣","Hong Kong":"香港","India":"印度","Vietnam":"越南","Russia":"俄羅斯","Africa":"非洲","Latin America":"拉丁美洲","Mexico":"墨西哥","Australia":"澳洲","UK":"英國","Germany":"德國","Singapore":"新加坡","Canada":"加拿大","Brazil":"巴西","Indonesia":"印尼","Thailand":"泰國","Malaysia":"馬來西亞"}
MV=r"(rose|rising|climbed|jumped|soared|surged|increased|grew|advanced|went up|fell|dropped|declined|decreased|slumped|plunged|tumbled|contracted|eased|slid)"
latest=[]
for id_,slug,zh,en in TEP:
    t=html.unescape(get(f"https://tradingeconomics.com/{slug}",timeout=40,ua="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"))
    m=re.search(r'id="description"[^>]*>(.*?)</h2>',t,re.S)
    if not m: print("TE trade no page",slug,len(t),file=sys.stderr); time.sleep(3); continue
    d=re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",m.group(1))).strip()
    h=re.search(MV+r"(?: by)? ([\d.]+)% (?:year-on-year|from a year earlier|yoy|on an annual basis|compared to)",d)
    v=re.search(r"(?:USD|US\$|\$) ?([\d,.]+) (billion|million)",d)
    mo=re.search(r"in (January|February|March|April|May|June|July|August|September|October|November|December) (\d{4})",d)
    yoy=None
    if h: yoy=(-1 if h.group(1) in("fell","dropped","declined","decreased","slumped","plunged","tumbled","contracted","eased","slid") else 1)*float(h.group(2))
    else:   # "... to USD 87.22 billion in September 2026 from USD 54.22 billion in the same month of the previous year"
        b=re.search(r"to (?:a record |an all-time high of )?(?:USD |US\$|\$)([\d.,]+) (billion|million) in [A-Z][a-z]+ \d{4},? (?:up |down )?from (?:USD |US\$|\$)([\d.,]+) (billion|million) in the same month",d)
        if b: yoy=round((float(b.group(1).replace(",",""))/float(b.group(3).replace(",",""))-1)*100,1)
    if yoy is None or not mo: print("TE trade miss",slug,d[:120],file=sys.stderr); continue
    MON=["January","February","March","April","May","June","July","August","September","October","November","December"]
    rec={"id":id_,"zh":zh,"en":en,"month":f"{mo.group(2)}-{MON.index(mo.group(1))+1:02d}","yoy":yoy,
         "value_bn":(float(v.group(1).replace(",",""))/(1000 if v.group(2)=="million" else 1)) if v else None,"url":f"https://tradingeconomics.com/{slug}","partners":[]}
    for pm in re.finditer(r"(?:[Ee]xports|[Ss]hipments|[Ss]ales|[Ii]mports|[Pp]urchases) (?:to|from) (?:the )?([A-Z][A-Za-z ]{1,24}?)(?: countries| nations)? (?:\w+ )?"+MV+r"(?: by)? ([\d.]+)%",d):
        p=pm.group(1).strip(); s=-1 if pm.group(2) in("fell","dropped","declined","decreased","slumped","plunged","tumbled","contracted","eased","slid") else 1
        if p in PZ and PZ[p] not in zh and not any(x["p"]==p for x in rec["partners"]): rec["partners"].append({"p":p,"zh":PZ[p],"yoy":s*float(pm.group(3))})
    latest.append(rec); time.sleep(2)
if latest: O["latest"]=latest
print("te latest",[(r["id"],r["month"],r["yoy"],len(r["partners"])) for r in latest],file=sys.stderr)
# ---------- UN Comtrade: what is shipped (HS 2-digit, annual) ----------
HSP=[("cn_vn","156","704","X","中國 → 越南（中國海關申報）","China → Vietnam (China-reported)"),("us_vn","842","704","M","越南 → 美國（美國海關申報）","Vietnam → US (US-reported)"),("us_cn","842","156","M","中國 → 美國（美國海關申報）","China → US (US-reported)")]
def ct(rep,part,flow,yr):
    t=get(f"https://comtradeapi.un.org/public/v1/preview/C/A/HS?reporterCode={rep}&period={yr}&partnerCode={part}&flowCode={flow}&cmdCode=AG2",timeout=60)
    try: return {r["cmdCode"]:r["primaryValue"] for r in json.loads(t).get("data",[]) if r.get("primaryValue")}
    except Exception: return {}
Y=datetime.date.today().year
for id_,rep,part,flow,zh,en in HSP:
    if O["hs"].get(id_,{}).get("year",0)>=Y-1: continue          # already have the latest year
    for yr in (Y-1,Y-2):
        cur=ct(rep,part,flow,yr); time.sleep(2)
        if len(cur)>20:
            prev=ct(rep,part,flow,yr-1); time.sleep(2)
            tot=sum(cur.values()); top=sorted(cur.items(),key=lambda kv:-kv[1])[:10]
            O["hs"][id_]={"zh":zh,"en":en,"year":yr,"total_bn":round(tot/1e9,1),"top":[{"hs":k,"bn":round(v/1e9,2),"share":round(v/tot*100,1),"yoy":(round((v/prev[k]-1)*100,1) if prev.get(k) else None)} for k,v in top],
                          "total_yoy":round((tot/sum(prev.values())-1)*100,1) if prev else None}
            print("comtrade",id_,yr,len(cur),file=sys.stderr); break
json.dump(O,open(out_p,"w",encoding="utf-8"),ensure_ascii=False,separators=(",",":"))
