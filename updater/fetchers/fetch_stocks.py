"""Shipping stock quotes from Yahoo股市 quote pages -> stocks.json"""
import json,re,sys,time,urllib.request,datetime
UA={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36","Accept-Language":"zh-TW,zh;q=0.9"}
S=[("2603.TW","長榮","貨櫃","TW"),("2609.TW","陽明","貨櫃","TW"),("2615.TW","萬海","貨櫃","TW"),("2606.TW","裕民","散裝","TW"),("2637.TW","慧洋-KY","散裝","TW"),("2605.TW","新興","散裝/油輪","TW"),("5608.TW","四維航","散裝","TW"),("2612.TW","中航","散裝","TW"),("2617.TW","台航","散裝","TW"),("2613.TW","中櫃","港口/物流","TW"),("2208.TW","台船","造船","TW"),("2636.TW","台驊投控","物流","TW"),("6505.TW","台塑化","燃油/石化","TW"),
   ("MAERSK-B.CO","Maersk","貨櫃","DK"),("HLAG.DE","Hapag-Lloyd","貨櫃","DE"),("1919.HK","中遠海控","貨櫃","HK"),("2510.HK","德翔海運","貨櫃","HK"),("011200.KS","HMM","貨櫃","KR"),("9101.T","日本郵船 NYK","綜合","JP"),("9104.T","商船三井 MOL","綜合","JP"),("9107.T","川崎汽船 K Line","綜合","JP"),("1138.HK","中遠海能","油輪","HK"),("329180.KS","HD現代重工","造船","KR"),("042660.KS","韓華海洋","造船","KR"),("010140.KS","三星重工","造船","KR"),
   ("ZIM","ZIM 以星","貨櫃","US"),("MATX","Matson","貨櫃","US"),("DAC","Danaos","貨櫃船東","US"),("GSL","Global Ship Lease","貨櫃船東","US"),("CMRE","Costamare","貨櫃船東","US"),("FRO","Frontline","油輪","US"),("DHT","DHT","油輪","US"),("INSW","International Seaways","油輪","US"),("TNK","Teekay Tankers","油輪","US"),("STNG","Scorpio Tankers","油輪","US"),("SBLK","Star Bulk","散裝","US"),("GNK","Genco","散裝","US"),("FLNG","Flex LNG","LNG","US"),("LPG","Dorian LPG","LPG","US"),("BWLP","BW LPG","LPG","US")]
out=[]
def num(t,k):
    m=re.search(r'"%s":(-?[\d.]+)'%k,t); return float(m.group(1)) if m else None
for sym,zh,sec,mk in S:
    try: t=urllib.request.urlopen(urllib.request.Request(f"https://tw.stock.yahoo.com/quote/{sym}",headers=UA),timeout=30).read().decode("utf8","ignore")
    except Exception as e: print("fail",sym,e,file=sys.stderr); continue
    p=num(t,"regularMarketPrice"); pc=num(t,"chartPreviousClose") or num(t,"previousClose")
    tm=re.search(r'"regularMarketTime":(\d{9,})',t); cur=re.search(r'"currency":"([A-Z]{3})"',t)
    if p is None: print("noprice",sym,file=sys.stderr); continue
    ts=datetime.datetime.fromtimestamp(int(tm.group(1)),datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") if tm else None
    out.append(dict(sym=sym,zh=zh,sector=sec,market=mk,price=p,prev=pc,chg=round(p-pc,4) if pc else None,chg_pct=round((p/pc-1)*100,2) if pc else None,currency=cur.group(1) if cur else "",time=ts,url=f"https://tw.stock.yahoo.com/quote/{sym}"))
    time.sleep(0.6)
json.dump({"fetched":datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),"source":"Yahoo 股市","items":out},open(sys.argv[1],"w"),ensure_ascii=False)
print("stocks",len(out),[(o['zh'],o['price'],o['chg_pct'],o['time']) for o in out],file=sys.stderr)
