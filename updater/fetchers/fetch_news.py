"""Collect shipping news by region from Bing News RSS + publisher RSS feeds -> news.json
Each item: id, region, sectors, source, title, summary, url, published (ISO UTC), lang"""
import json, re, sys, html, hashlib, urllib.request, urllib.parse, datetime, time, email.utils
import xml.etree.ElementTree as ET
UA={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36"}
DAYS=int(sys.argv[2]) if len(sys.argv)>2 else 10
NOW=datetime.datetime.now(datetime.timezone.utc); CUT=NOW-datetime.timedelta(days=DAYS)
def get(url):
    for i in range(3):
        try: return urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=30).read()
        except Exception as e: err=e; time.sleep(2+i*3)
    print("FAIL",url[:100],err,file=sys.stderr); return b""
# (region, query, lang)
Q=[
 ("台灣","長榮海運",'zh'),("台灣","陽明海運",'zh'),("台灣","萬海航運",'zh'),("台灣","貨櫃三雄 運價",'zh'),("台灣","散裝航運 BDI",'zh'),
 ("台灣","裕民 慧洋 散裝",'zh'),("台灣","高雄港 貨櫃",'zh'),("台灣","台灣 航運股",'zh'),("台灣","台灣 LNG 進口 中油",'zh'),("台灣","台灣 造船 台船",'zh'),
 ("亞洲","中遠海運",'zh'),("亞洲","中國 航運 集運",'zh'),("亞洲","新加坡港 船舶",'zh'),("亞洲","日本 韓國 造船 訂單",'zh'),("亞洲","印度 港口 航運",'zh'),
 ("亞洲","日本 海運 郵船 商船三井",'zh'),("亞洲","韓國 HMM 航運",'zh'),("亞洲","中國 港口 吞吐量",'zh'),("亞洲","東南亞 港口 越南 印尼",'zh'),("亞洲","中國 鐵礦砂 進口",'zh'),("亞洲","印度 原油 進口 油輪",'zh'),
 ("亞洲","China port throughput",'en'),("亞洲","Vietnam port container",'en'),("亞洲","Indonesia coal exports shipping",'en'),("亞洲","India shipping ports crude imports",'en'),("亞洲","China iron ore imports",'en'),("亞洲","Japan LNG imports",'en'),
 ("亞洲","COSCO shipping",'en'),("亞洲","Singapore port shipping",'en'),("亞洲","Korea shipbuilding orders",'en'),("亞洲","China shipping container freight",'en'),("亞洲","Japan shipping NYK MOL",'en'),
 ("中東","荷姆茲海峽",'zh'),("中東","霍爾木茲海峽 船隻",'zh'),("中東","紅海 胡塞 航運",'zh'),("中東","卡達 LNG",'zh'),
 ("中東","Strait of Hormuz shipping",'en'),("中東","Hormuz tanker",'en'),("中東","Red Sea shipping Houthi",'en'),("中東","Qatar LNG shipping",'en'),
 ("歐洲","馬士基",'zh'),("歐洲","赫伯羅特 達飛",'zh'),("歐洲","歐洲 航運 碳排",'zh'),
 ("歐洲","Maersk",'en'),("歐洲","Hapag-Lloyd",'en'),("歐洲","Rotterdam port",'en'),("歐洲","EU ETS shipping",'en'),("歐洲","Greek shipowners tankers",'en'),("歐洲","Europe LNG imports",'en'),
 ("非洲","幾內亞 鋁土礦",'zh'),("非洲","西芒杜 鐵礦",'zh'),("非洲","非洲 港口 中國",'zh'),
 ("非洲","Simandou iron ore",'en'),("非洲","Guinea bauxite",'en'),("非洲","Transnet port Durban",'en'),("非洲","Nigeria LNG shipping",'en'),("非洲","Africa port shipping",'en'),("非洲","Cape of Good Hope shipping diversion",'en'),
 ("台灣","中鋼運通 台塑海運",'zh'),("台灣","四維航 新興航運 台航",'zh'),("台灣","台灣港務 港口 貨櫃量",'zh'),("台灣","航運 法說會 長榮 陽明",'zh'),
 ("非洲","蘇伊士運河 通行",'zh'),("非洲","Suez Canal revenue transits",'en'),("非洲","Mozambique LNG",'en'),("非洲","Mombasa port",'en'),("非洲","Tanger Med port",'en'),("非洲","South Africa ports shipping",'en'),("非洲","West Africa shipping",'en'),("非洲","Guinea Simandou Winning Consortium",'en'),
 
 ("美洲","巴拿馬運河",'zh'),("美洲","美國 港口費 中國船",'zh'),("美洲","美國 LNG 出口",'zh'),
 ("美洲","Panama Canal transits",'en'),("美洲","USTR port fees Chinese ships",'en'),("美洲","US LNG exports",'en'),("美洲","Port of Los Angeles imports",'en'),("美洲","Brazil iron ore Vale shipments",'en'),("美洲","US crude exports tankers",'en'),
 ("全球","航運 運價",'zh'),("全球","油輪 運價 VLCC",'zh'),("全球","LNG 船 運價",'zh'),("全球","LPG 船",'zh'),
 ("全球","VLCC rates",'en'),("全球","LNG carrier rates",'en'),("全球","VLGC LPG shipping",'en'),("全球","dry bulk market capesize",'en'),("全球","container shipping rates",'en'),("全球","Clarksons shipping",'en'),
]
FEEDS=[("gCaptain","https://gcaptain.com/feed/"),("Splash247","https://splash247.com/feed/"),("Hellenic Shipping News","https://www.hellenicshippingnews.com/feed/"),("Seatrade Maritime","https://www.seatrade-maritime.com/rss.xml"),("FreightWaves","https://www.freightwaves.com/news/feed"),("The Loadstar","https://theloadstar.com/feed/"),("Offshore Energy","https://www.offshore-energy.biz/feed/")]
SECT=[("貨櫃",r"貨櫃|货柜|集裝箱|集装箱|container|SCFI|CCFI|TEU|長榮|陽明|萬海|Maersk|馬士基|MSC|CMA CGM|Hapag|赫伯羅特|COSCO|中遠|ONE\b|ZIM|HMM|運價|liner"),
      ("散裝",r"散裝|散货|乾散|BDI|capesize|海岬|panamax|巴拿馬型|supramax|dry bulk|bulk|鐵礦|铁矿|iron ore|bauxite|鋁土|铝土|Simandou|西芒|煤|coal|grain|穀物|裕民|慧洋|新興|四維|台航|中航"),
      ("油輪",r"油輪|油轮|tanker|VLCC|原油|crude|成品油|Suezmax|Aframax|TD3C|影子船隊|shadow fleet"),
      ("LNG",r"LNG|液化天然氣|液化天然气|天然氣|天然气|gas carrier"),("LPG",r"LPG|VLGC|液化石油氣|丙烷|propane"),
      ("造船",r"造船|shipbuild|shipyard|newbuild|訂單|orderbook|船廠"),("港口",r"港口|港務|port\b|ports\b|碼頭|terminal|運河|canal"),
      ("地緣",r"荷姆茲|霍爾木茲|霍尔木兹|Hormuz|紅海|红海|Red Sea|胡塞|Houthi|伊朗|Iran|制裁|sanction|襲擊|袭击|attack|war|戰")]
TOPICS=[("simandou",r"Simandou|西芒杜|西芒度|幾內亞|几内亚|(?<!Papua New )(?<!Equatorial )Guinea|bauxite|鋁土|铝土|Morebaya|Kamsar"),("usgulf",r"(US|U\.S\.|美國|美灣|Gulf Coast|Texas|Louisiana|Corpus Christi|Houston).{0,60}(export|出口|crude|原油|LNG|LPG|tanker|油輪)|(export|出口).{0,40}(US|U\.S\.|美國)"),("clarksons",r"Clarksons|克拉克森")]
SKIP=r"(?i)horoscope|lottery|celebrity|cruises?\b|樂透|星座|NBA|MLB|郵輪"
REG=[("台灣",r"台灣|臺灣|Taiwan|高雄|Kaohsiung|長榮|陽明|萬海|Evergreen|Yang Ming|Wan Hai"),("中東",r"Hormuz|荷姆茲|霍爾木茲|Red Sea|紅海|Houthi|Iran|伊朗|Qatar|卡達|Saudi|沙烏地|UAE|Gulf|波斯灣|Fujairah"),("非洲",r"Africa|非洲|Guinea|幾內亞|Simandou|Nigeria|Durban|Transnet|Kenya|Egypt|Suez|Cape of Good Hope|好望角|Mozambique"),("美洲",r"\bUS\b|U\.S\.|America|美國|Panama|巴拿馬|Brazil|巴西|Canada|Mexico|Los Angeles|Houston|Gulf of Mexico|USTR|Venezuela|Chile|Argentina"),("歐洲",r"Europe|歐洲|EU\b|Rotterdam|Hamburg|Antwerp|Greece|Greek|希臘|Norway|UK\b|Britain|German|Maersk|Hapag|CMA CGM|MSC\b|Baltic Sea|Russia|俄羅斯"),("亞洲",r"China|中國|Chinese|Japan|日本|Korea|韓國|Singapore|新加坡|India|印度|Vietnam|Malaysia|Indonesia|Philippines|COSCO|中遠|Hong Kong|香港|Shanghai|上海")]
items={}
def norm(t): return re.sub(r"[\W_]+","",t.lower())[:40]
def add(region,source,title,summary,url,pub,lang):
    cut=CUT-datetime.timedelta(days=11) if region in("非洲",) else CUT-datetime.timedelta(days=4) if region=="亞洲" else CUT
    if not url or not title or pub<cut or re.search(SKIP,title): return
    title=html.unescape(title).strip(); summary=html.unescape(re.sub(r"<[^>]+>"," ",summary or "")).strip()
    summary=re.sub(r"\s+"," ",summary)[:320]
    title=re.sub(r"\s+-\s+[^-]{2,30}$","",title) if source and title.endswith(source) else title
    key=norm(title)
    if key in items: 
        if region!="全球" and items[key]["region"]=="全球": items[key]["region"]=region
        return
    blob=title+" "+summary
    if region=="全球":
        for r,pat in REG:
            if re.search(pat,title): region=r; break
    sec=[s for s,p in SECT if re.search(p,blob,re.I)]
    sec_t=[s for s,p in SECT if re.search(p,title,re.I)]
    if not sec_t and (lang=="en" or len(sec)<2): return
    if re.search(r"(?i)amazon s3|travel weekly|stocktwits",source or ""): return
    # relevance: must touch shipping/energy-trade vocabulary
    if not sec: return
    tp=[k for k,pat in TOPICS if re.search(pat,blob,re.I)]
    items[key]=dict(topics=tp,id=hashlib.md5(url.encode()).hexdigest()[:12],region=region,sectors=sec,source=source.strip(),title=title,summary=summary,url=url,published=pub.strftime("%Y-%m-%dT%H:%M:%SZ"),lang=lang)
for region,q,lang in Q:
    p={"q":q,"format":"rss"}; p.update({"zh":{"setlang":"zh-hant","cc":"TW"},"zhcn":{"setlang":"zh-hans","cc":"CN"},"en":{"setlang":"en-us","cc":"US"}}[lang]); lang="zh" if lang.startswith("zh") else lang
    p["qft"]='sortbydate="1"'
    root=None
    for attempt in range(4):
        raw=get("https://www.bing.com/news/search?"+urllib.parse.urlencode(p))
        try: root=ET.fromstring(raw); break
        except ET.ParseError: time.sleep(2+attempt*2)
    if root is None: print("bing fail",q,file=sys.stderr); continue
    for it in root.iter("item"):
        link=it.findtext("link") or ""; u=urllib.parse.parse_qs(urllib.parse.urlparse(link).query).get("url",[link])[0]
        src=""
        for ch in it:
            if ch.tag.endswith("Source"): src=ch.text or ""
        try: pub=email.utils.parsedate_to_datetime(it.findtext("pubDate"))
        except Exception: continue
        add(region,src or urllib.parse.urlparse(u).netloc,it.findtext("title"),it.findtext("description"),u,pub,lang)
    time.sleep(0.6)
for name,url in FEEDS:
    raw=get(url)
    if not raw: continue
    try: root=ET.fromstring(raw)
    except ET.ParseError: print("parse fail",name,file=sys.stderr); continue
    for it in root.iter("item"):
        try: pub=email.utils.parsedate_to_datetime(it.findtext("pubDate"))
        except Exception: continue
        t=it.findtext("title") or ""; d=it.findtext("description") or ""
        reg="全球"
        for r,pat in REG:
            if re.search(pat,t+" "+d): reg=r; break
        add(reg,name,t,d,it.findtext("link"),pub,"en")
out=sorted(items.values(),key=lambda x:x["published"],reverse=True)
json.dump({"fetched":NOW.strftime("%Y-%m-%dT%H:%MZ"),"days":DAYS,"items":out},open(sys.argv[1],"w"),ensure_ascii=False)
from collections import Counter
print(len(out),Counter(i["region"] for i in out),Counter(i["lang"] for i in out),file=sys.stderr)
