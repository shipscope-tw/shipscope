"""Extend earnings.json: sector categories, logos, ship photos, Taiwan bulk/tanker names, global bulk/tanker/gas peers,
and richer earnings-call notes for the Taiwan container lines. Usage: python3 earnings_extend.py <earnings.json> <images.json>"""
import json, sys
from make_earnings_lib import K, L, S

E = json.load(open(sys.argv[1], encoding="utf-8"))
IMG = json.load(open(sys.argv[2], encoding="utf-8"))
C = {c["id"]: c for c in E["companies"]}

def photo(key, generic=False, cap=None):
    m = IMG[key]
    return {"f": m["f"], "by": m["by"], "lic": m["lic"], "page": m["page"], "generic": generic, "cap": cap}

# ---------- categories, logos, photos for existing companies ----------
meta = {
 "evergreen": ("container", {"f": "Evergreen Line Logo.svg"}, photo("evergreen", cap=["長榮 Ever Given（2 萬 TEU 級）", "Evergreen's Ever Given (20,000 TEU class)"])),
 "yangming": ("container", None, photo("yangming", cap=["陽明 YM Inception", "Yang Ming's YM Inception"])),
 "wanhai": ("container", None, photo("wanhai", cap=["萬海 Wan Hai 503", "Wan Hai 503"])),
 "maersk": ("container", {"f": "Maersk Line Logo, July 2021.svg"}, photo("maersk", cap=["馬士基 3E 級 Mærsk Mc-Kinney Møller", "Maersk Triple-E Mærsk Mc-Kinney Møller"])),
 "msc": ("container", {"f": "Mediterranean Shipping Company logo.svg"}, photo("msc", cap=["MSC Irina（24,346 TEU）", "MSC Irina (24,346 TEU)"])),
 "cmacgm": ("container", {"f": "CMA CGM logo.svg"}, photo("cmacgm", cap=["達飛 CMA CGM Nevada", "CMA CGM Nevada"])),
 "hapag": ("container", {"f": "Hapag-Lloyd.svg"}, photo("hapag", cap=["赫伯羅特 Berlin Express", "Hapag-Lloyd's Berlin Express"])),
 "cosco": ("container", {"f": "COSCO Shipping Logo.svg"}, photo("cosco", cap=["中遠海運 COSCO Shipping Universe（21,237 TEU）", "COSCO Shipping Universe (21,237 TEU)"])),
 "one": ("container", {"f": "Ocean Network Express logo.svg"}, photo("one", cap=["ONE Apus（洋紅色船體）", "ONE Apus (magenta hull)"])),
 "hmm": ("container", {"f": "HMM Logo Basic Form.svg"}, photo("hmm", cap=["HMM Algeciras（23,964 TEU）", "HMM Algeciras (23,964 TEU)"])),
 "zim": ("container", {"f": "ZIM Logo.svg"}, photo("zim", cap=["以星 ZIM Alabama", "ZIM Alabama"])),
}
for cid, (cat, logo, ph) in meta.items():
    c = C[cid]; c["cats"] = [cat]; c["logo"] = logo; c["photo"] = ph

# ---------- richer notes: Evergreen ----------
ev = C["evergreen"]
ev["fleet"] = ["242 艘、約 204 萬 TEU，全球第 7（市占 5.9%）；規劃 2030 年約 290 艘、274 萬 TEU", "242 ships, ~2.04m TEU, world No.7 (5.9%); plans ~290 ships / 2.74m TEU by 2030"]
q3 = ev["periods"][0]
q3["title"] = ["第三季營收快報＋10/8 法說會（財報尚未公布）", "Q3 revenue flash + 8 Oct investor call (results pending)"]
q3["hl"] = L(
 ["法說會（10/8）：旺季提早且延續到 9 月，第三季運價走高；9 月營收年增 63.75%，受十一長假前出貨潮與天候改善帶動。", "Investor call (8 Oct): peak season came early and lasted into September, lifting Q3 rates; September revenue +63.75% YoY on pre-Golden Week shipments and better weather."],
 ["貨量：遠東—美國約 +5.1%、遠東—歐洲約 +12.2%；目前運價「美線強、歐線弱」，歐線 4 月因美伊衝突大漲、7 月後逐週緩跌。", "Volumes: Far East–US ~+5.1%, Far East–Europe ~+12.2%. Rates are 'strong on US lanes, weak on Europe'; Europe spiked in April on the US–Iran conflict and has eased weekly since July."],
 ["美國碼頭進口量創高、存貨偏低，主要美系客戶對需求看法正面；關稅調整後美國進口商可能獲約 1,600 億美元退稅，有望支撐進口。", "US ports are seeing record imports and low inventories; major US customers are positive. Tariff refunds of ~US$160bn to importers could support volumes."],
 ["全球塞港嚴重（例如新加坡碼頭使用率九成以上），吸收新增運力；歐洲航線多採「去程繞好望角、回程走蘇伊士」。", "Severe congestion (e.g. Singapore terminals >90% utilised) absorbs new capacity; Europe services often go out via the Cape and return via Suez."])
q3["gd"] = L(
 ["11 月前訂艙「非常樂觀」，12 月接春節前拉貨；第四季營收預估年增微幅成長。", "Bookings through November are 'very optimistic', with pre-Lunar New Year cargo in December; Q4 revenue expected to grow slightly YoY."],
 ["美國線「春節前看不出任何悲觀理由」；美國現貨價明顯高於去年第四季長約談判價，看好明年長約價格高於今年。", "US trade: 'no reason for pessimism before Lunar New Year'; spot is well above last Q4's contract level and 2027 contracts should price higher."],
 ["歐線第四季運價偏低但仍屬健康；歐地線長約比例低，價格仍比去年同期高。", "Europe Q4 rates are lower but healthy; few Europe/Med contracts, but priced above last year."],
 ["風險：美國若因通膨啟動升息、2028 年美西碼頭工人合約（明年下半年開始談）、紅海風險未根本解決；明年第二季能見度仍低。", "Risks: US rate hikes on inflation, the 2028 US West Coast dockworker contract (talks from H2 next year), unresolved Red Sea risk; low visibility on Q2 next year."],
 ["船隊：2030 年約 290 艘、274 萬 TEU，其中 55 艘雙燃料（約占運能 32.8%）；2025 年 11 月已訂 14 艘 1.4 萬 TEU LNG 雙燃料船（三星重工、廣船國際各 7 艘，總價 24.5–28.7 億美元）。", "Fleet plan: ~290 ships / 2.74m TEU by 2030, 55 dual-fuel (~32.8% of capacity); 14×14,000 TEU LNG dual-fuel ships ordered Nov 2025 (7 Samsung HI, 7 GSI; US$2.45–2.87bn)."],
 ["獲利將於 11 月中第三季財報公布。", "Q3 profit due mid-November."])
q3["src"] = [S("中央社：長榮法說（2026/10/08）", "https://cna.com.tw/news/afe/202610080235.aspx"), S("Winvest 營收快訊（2026/10/09）", "https://winvest.tw/News/Detail/95592"), S("Yahoo 新聞：長榮訂造 14 艘 LNG 雙燃料船", "https://tw.news.yahoo.com/%E9%95%B7%E6%A6%AE%E6%B5%B7%E9%81%8B%E6%96%A5%E8%B3%87990%E5%84%84%E5%85%83-%E8%B2%B7%E6%96%B0%E8%88%B9-%E6%96%B0%E6%AB%83-224738464.html")]

# ---------- Yang Ming: 9/22 investor call ----------
ym = C["yangming"]
ym["fleet"] = ["第三季 99 艘、約 77.3 萬 TEU，全球第 9（市占 2.2%）；運費收入歐洲線 39%、美國線 36%", "Q3: 99 ships, ~773k TEU, world No.9 (2.2%); freight revenue 39% Europe, 36% US"]
yq3 = ym["periods"][0]
yq3["title"] = ["第三季營收快報＋9/22 法說會（財報尚未公布）", "Q3 revenue flash + 22 Sep investor call (results pending)"]
yq3["hl"] = L(
 ["9 月營收年增近七成（整體運價上漲），第三季營收比第二季多約四成。", "September revenue up ~70% YoY on higher rates; Q3 revenue ~40% above Q2."],
 ["法說會（9/22）：上半年運量 223.6 萬 TEU、年增 3.9%（歐洲線 +10%、美國線 +7.8%）；營收比重歐洲 39%、美國 36%、亞洲 25%（中東與紅海停航使亞洲比重下降）。", "Investor call (22 Sep): H1 liftings 2.236m TEU, +3.9% (Europe +10%, US +7.8%); revenue mix Europe 39%, US 36%, Asia 25% (Asia share down on Middle East/Red Sea suspensions)."],
 ["第二季毛利率回升至 13%；亞洲、歐洲、南美東岸、中東主要港口普遍塞港 4–10 天，公司認為塞港可能成為常態。", "Q2 gross margin recovered to 13%; major ports in Asia, Europe, ECSA and the Middle East see 4–10 day delays, which may become the norm."])
yq3["gd"] = L(
 ["第四季歐美進入淡季，市況「緩步修正」：歐美線運價微幅修正；亞洲線進入旺季，運價有望優於第三季。", "Q4: Europe/US enter the slack season with a gradual correction; intra-Asia enters peak season and may beat Q3."],
 ["美東線因巴拿馬運河限制與亞洲塞港，艙位缺口可能持續、運價可望維持高檔；美西線不會與美東脫鉤。", "US East Coast: Panama limits and Asian congestion keep space tight and rates firm; West Coast won't decouple."],
 ["年底將簽的歐線長約，價格將高於去年。", "Europe contracts signed at year-end should price above last year."],
 ["新船：共 24 艘貨櫃輪與 4 艘散裝輪；其中 5 艘 1.5 萬 TEU LNG 雙燃料船 2026 年底前交完，其餘 2028–2030 年交付；2026 年採購 15 萬 TEU 自有櫃。", "Newbuilds: 24 container ships and 4 bulkers; five 15,000 TEU LNG dual-fuel ships delivered by end-2026, the rest in 2028–2030; buying 150k TEU of own boxes in 2026."],
 ["紅海未明朗前不考慮復航；2027 年運價走勢預計 2027 年第一季才較清楚，研究機構對供需預測分歧大。", "No Red Sea return until safe; 2027 rate direction clearer in Q1 2027, with wide divergence in supply-demand forecasts."])
yq3["src"] = [S("富果：陽明 9/22 法說摘要", "https://blog.fugle.tw/post/earnings-call-2609-2026-09-22"), S("陽明法說簡報（公開資訊觀測站）", "https://mopsov.twse.com.tw/nas/STR/260920260922M001.pdf"), S("Winvest 營收快訊（2026/10/09）", "https://winvest.tw/News/Detail/96027"), S("旺得富（2026/09/24）", "https://wantrich.chinatimes.com/news/20260924900003-420101")]

# ---------- Wan Hai: route mix and outlook ----------
wh = C["wanhai"]
wq2 = wh["periods"][1]
wq2["hl"] += L(
 ["航線結構（3/26 法說）：亞洲區間 29 條主要航線，占貨量 55%；中東與印度由 22% 升至 25%、北美 13%；營收比重中東與印度由 23% 升至 27%。", "Route mix (26 Mar call): 29 main intra-Asia loops = 55% of volume; Middle East & India up from 22% to 25%, North America 13%; ME & India revenue share up from 23% to 27%."],
 ["中東戰事讓波灣消費品庫存耗盡，貨改經吉達等港轉運，壅塞擴散到印度與新加坡，推升近洋與中東、印度航線運價（5/28 說明）。", "The war drained Gulf consumer-goods inventories; cargo rerouted via Jeddah and other ports, spreading congestion to India and Singapore and lifting intra-Asia, ME and India rates (28 May)."])
wq2["gd"] = L(
 ["總經理謝福隆：高運價可延續到第三季，市場自 5 月起「明顯轉旺」；2026 年北美長約價格一定高於 2025 年。", "President Hsieh: high rates should last through Q3, with the market 'clearly stronger' since May; 2026 North America contracts certainly above 2025."],
 ["下半年供需結構仍相對健康，燃油成本雖升，運價指數仍大幅高於年初；看好第四季節慶備貨與庫存回補。", "H2 supply-demand still relatively healthy; despite higher fuel, rate indices are well above the start of the year; Q4 holiday and restocking demand expected."],
 ["美國 232 條款對台灣汽車零組件等非半導體貨品給予優惠稅率，屬萬海承運範圍，可望受惠。", "US Section 232 preferential rates for Taiwanese non-semiconductor goods (e.g. auto parts) fall within Wan Hai's cargo base."],
 ["凱基投顧：近洋與北美線合計約占營收 68%，是本波運價上漲最大受惠者（法人觀點）。", "KGI (broker view): intra-Asia plus North America ~68% of revenue, the biggest beneficiary of the rate upswing."],
 ["新船：2026 年交 7 艘（+4.88 萬 TEU）；2027–2030 年共 42 艘、約 47.5 萬 TEU，2027 年為交船高峰（+16.87 萬 TEU、資本支出約 18.61 億美元）；自有櫃占 83%、平均櫃齡 5.2 年。", "Newbuilds: 7 ships (+48.8k TEU) in 2026; 42 ships (~475k TEU) in 2027–2030, peaking 2027 (+168.7k TEU, capex ~US$1.86bn); 83% owned boxes, average age 5.2 years."])
wq2["src"] += [S("聯合報：萬海法說（2026/03/26）", "https://udn.com/news/story/7252/9405030"), S("ETtoday：萬海看好高運價延續到第三季（2026/05/28）", "https://finance.ettoday.net/news/3173582"), S("旺得富：法人看貨櫃三雄（2026/09/24）", "https://wantrich.chinatimes.com/news/20260924900003-420101")]

# ---------- new companies ----------
G_BULK = photo("g_bulk", True, ["示意：海岬型散裝船（非該公司船舶）", "Illustrative capesize bulker (not this company's ship)"])
G_TANK = photo("g_tanker", True, ["示意：油輪甲板（非該公司船舶）", "Illustrative tanker deck (not this company's ship)"])
TW_NEXT = {"p": "2026Q3", "date": "2026-11-14", "approx": True, "note": ["法定公告期限 11/14", "Statutory deadline 14 Nov"]}
new = []
new.append({"id": "uming", "zh": "裕民航運", "en": "U-Ming Marine", "cc": "TW", "ticker": "2606.TW", "ccy": ["新台幣", "TWD"], "cats": ["bulk"],
 "fleet": ["營運 72 艘（自有 54、代管 7、合資 11），在建 14 艘；自有船平均 8.1 歲；以海岬型為主", "72 ships (54 owned, 7 managed, 11 JV), 14 on order; owned fleet avg 8.1 yrs; capesize-focused"],
 "ir": "https://mops.twse.com.tw", "next": TW_NEXT, "logo": None, "photo": G_BULK,
 "periods": [{"p": "2026Q2", "date": "2026-08", "title": ["第二季財報＋9/16 法說會", "Q2 results + 16 Sep investor call"],
   "kpis": [K("營收", "Revenue", "50.1 億元", "NT$5.0bn", 38.5, 28.8), K("營業利益", "Operating profit", "15.6 億元", "NT$1.56bn", None, None, "營益率 31.1%", "Margin 31.1%"),
            K("稅後淨利", "Net profit", "19.8 億元", "NT$1.98bn"), K("EPS", "EPS", "2.34 元", "NT$2.34"), K("上半年 EPS", "H1 EPS", "3.51 元", "NT$3.51", None, None, "上半年淨利 29.6 億元", "H1 net NT$2.96bn")],
   "hl": L(["BDI 現貨反彈帶動：第二季 BDI 平均 2,751 點，高於第一季 2,159 點與去年同期 1,118 點。", "Driven by the spot rebound: Q2 BDI averaged 2,751 vs 2,159 in Q1 and 1,118 a year earlier."],
           ["海岬型長約約 55%、現貨 45%；中小型船長約約 25%、現貨 75%。今年新簽海岬型長約日租約 3 萬美元以上（過去約 2.5–3 萬）。", "Capesize ~55% long-term / 45% spot; smaller ships ~25% / 75%. New capesize charters this year above US$30k/day (vs US$25–30k before)."],
           ["環保節能船占 94%；新船 2026 年交 1 艘、2027 年 6 艘、2028 年 5 艘、2030 年 2 艘。", "94% eco ships; newbuild deliveries: 1 in 2026, 6 in 2027, 5 in 2028, 2 in 2030."]),
   "gd": L(["下半年運價預期優於上半年及去年同期；現貨營收認列有 1–2 個月遞延，第四季營收有機會優於第三季。", "H2 rates expected above H1 and last year; with a 1–2 month lag in spot revenue, Q4 may beat Q3."],
           ["需求：延噸海浬成長約 3.8%，高於貨量成長 2.6%（巴西、幾內亞長程礦砂與鋁土礦）；西芒杜滿產可增加 100 艘以上海岬型船需求。", "Demand: tonne-miles ~+3.8% vs volumes +2.6% (long-haul Brazil/Guinea ore and bauxite); Simandou at full output could need 100+ extra capesizes."],
           ["供給：新船訂單僅占船隊 13.66%（歷史低檔），未來幾年供給成長約 3%–4%；降速航行使有效運力受限。", "Supply: orderbook only 13.66% of fleet (historic low), 3–4% annual supply growth; slow steaming limits effective capacity."],
           ["股利配發率維持 50% 以上；風險：荷姆茲、俄烏戰爭、印尼 2027 年 1 月煤炭出口新政（可能引發第四季搶運）、幾內亞鋁土礦出口限額。", "Payout ≥50%; risks: Hormuz, Russia–Ukraine, Indonesia's Jan 2027 coal export rule (possible Q4 rush), Guinea bauxite quotas."]),
   "src": [S("富果：裕民 9/16 法說摘要", "https://blog.fugle.tw/post/earnings-call-2606-2026-09-16")]}]})
new.append({"id": "wisdom", "zh": "慧洋-KY", "en": "Wisdom Marine", "cc": "TW", "ticker": "2637.TW", "ccy": ["新台幣", "TWD"], "cats": ["bulk"],
 "fleet": ["2026 年初 128 艘（巴拿馬型 35、超輕便極限型 29、輕便型 38、小型輕便型 23）；約 81–85 艘採指數連動租約", "128 ships at start-2026 (35 Panamax, 29 Supramax, 38 Handy, 23 small Handy); ~81–85 on index-linked charters"],
 "ir": "https://www.wisdomlines.com.tw", "next": TW_NEXT, "logo": {"fav": "wisdomlines.com.tw"}, "photo": G_BULK,
 "periods": [{"p": "2026Q2", "date": "2026-08", "title": ["第二季財報與自結數字", "Q2 results and monthly self-reported figures"],
   "kpis": [K("營收", "Revenue", "約 53.4 億元", "~NT$5.3bn", None, None, "上半年自結 96.8 億減第一季推算", "H1 self-reported minus Q1", True), K("EPS", "EPS", "2.49 元", "NT$2.49", None, 55.6),
            K("上半年營收", "H1 revenue", "96.8 億元", "NT$9.7bn", 32.32, None, "自結", "Self-reported"), K("1–8 月每股稅前盈餘", "Jan–Aug pre-tax EPS", "6.81 元", "NT$6.81", None, None, "自結；1–8 月營收 137.8 億、年增 35.38%", "Self-reported; Jan–Aug revenue NT$13.8bn, +35.38%")],
   "hl": L(["6 月營業利益率突破四成，為 2022 年以來新高；毛利率連季升至約 39%。", "June operating margin topped 40%, the highest since 2022; gross margin rose to ~39%."],
           ["新船 Paiwan Elegance（今治造船 4 萬噸輕便型，第三期環保船）6 月加入，已簽長期租約、毛利率約五成；9 月再交 Paiwan Hero。", "New 40k dwt Handy Paiwan Elegance (Imabari, eco design) joined in June on a long charter at ~50% gross margin; Paiwan Hero followed in September."],
           ["持續處分老船：今年已認列 5 艘處分收益，全年賣船目標「雙位數」；8 月處分兩艘約貢獻 1,200 萬美元。", "Selling older ships: gains on 5 so far, double-digit disposals targeted; two sold in August added ~US$12m."]),
   "gd": L(["下半年「審慎樂觀」：荷姆茲通航狀況反覆，美伊戰事走向待觀察；地緣風險降溫與戰後重建可帶動原物料運輸。", "Cautiously optimistic for H2: Hormuz access remains erratic; easing risk and post-war rebuilding could lift commodity shipping."],
           ["新船：2026 年 8 艘 4 萬噸輕便型、2027 年 4 艘（含 2 艘巴拿馬型）、2028 年 1 艘；環保法規（EEXI、CII、EU ETS）對年輕船隊有利。", "Newbuilds: eight 40k dwt Handys in 2026, four in 2027 (incl. 2 Panamax), one in 2028; tighter rules (EEXI, CII, EU ETS) favour young fleets."],
           ["資本支出下降、負債比降至約 40%，股利空間提高；今年配發現金股利 3.5 元。", "Lower capex and ~40% debt ratio leave more room for dividends; NT$3.5 cash dividend paid this year."]),
   "src": [S("理財周刊（2026/09/16）", "https://www.moneyweekly.com.tw/_Article?AID=248952"), S("ETtoday（2026/07/03）", "https://finance.ettoday.net/news/3194757"), S("富果：慧洋 6/9 法說摘要", "https://blog.fugle.tw/post/earnings-call-2637-2026-06-09")]}]})
new.append({"id": "taiwannav", "zh": "台灣航業", "en": "Taiwan Navigation", "cc": "TW", "ticker": "2617.TW", "ccy": ["新台幣", "TWD"], "cats": ["bulk"],
 "fleet": ["散裝船隊平均船齡約 6 歲；2 艘 6.4 萬噸新船 2028 年交付", "Dry bulk fleet averages ~6 years; two 64k dwt newbuilds due 2028"],
 "ir": "https://mops.twse.com.tw", "next": TW_NEXT, "logo": None, "photo": G_BULK,
 "periods": [{"p": "2026Q2", "date": "2026-08-06", "title": ["2026 上半年財報", "H1 2026 results"],
   "kpis": [K("上半年營收", "H1 revenue", "約 23.7 億元", "~NT$2.37bn", 16), K("毛利率", "Gross margin", "43%", "43%"),
            K("上半年淨利", "H1 net profit", "約 6.46 億元", "~NT$0.65bn"), K("上半年 EPS", "H1 EPS", "1.55 元", "NT$1.55", None, None, "第一季 0.71 元，推算第二季約 0.84 元", "Q1 NT$0.71, implying ~NT$0.84 in Q2")],
   "hl": L(["上半年乾散貨市場優於預期，海岬型運價創近年同期高點；截至 7 月平均運價較去年漲近一倍，中小型船日租年增四至六成。", "H1 dry bulk beat expectations; capesize rates hit multi-year seasonal highs; average rates through July nearly doubled YoY, smaller-ship hire up 40–60%."],
           ["驅動因素：長程貨載增加、有效運力偏緊、中東戰事拉長航程；2 艘 4 萬噸新船第二季交船營運。", "Drivers: more long-haul cargo, tight effective capacity, longer voyages from the Middle East war; two 40k dwt newbuilds delivered in Q2."]),
   "gd": L(["全年展望「樂觀」，散裝運價優於去年同期；將評估處分高齡船並研議新造船。", "Optimistic for the year with rates above last year; reviewing older-ship sales and new orders."],
           ["風險：地緣政治、主要經濟體貨幣政策、中國房地產與鋼鐵需求；歐盟碳稅與 FuelEU 罰款依合約由租家負擔。", "Risks: geopolitics, monetary policy, China property/steel demand; EU ETS and FuelEU costs borne by charterers."]),
   "src": [S("ETtoday（2026/08/06）", "https://finance.ettoday.net/news/3214731")]}]})
new.append({"id": "shihwei", "zh": "四維航", "en": "Shih Wei Navigation", "cc": "TW", "ticker": "5608.TW", "ccy": ["新台幣", "TWD"], "cats": ["bulk"],
 "fleet": ["以中小型散裝船為主", "Mainly small and mid-size bulk carriers"], "ir": "https://mops.twse.com.tw", "next": TW_NEXT, "logo": None, "photo": G_BULK,
 "periods": [{"p": "2026Q2", "date": "2026-08", "title": ["第二季財報", "Q2 results"],
   "kpis": [K("EPS", "EPS", "0.42 元", "NT$0.42", None, None, "第一季 −0.11 元", "Q1: −NT$0.11"), K("上半年 EPS", "H1 EPS", "0.32 元", "NT$0.32", None, None, "上半年轉虧為盈", "Back to profit in H1")],
   "hl": L(["第二季轉為獲利；第二季 BDI 平均 2,751 點，較去年同期大增 88%，各船型運價均較第一季與去年同期上升。", "Returned to profit in Q2; Q2 BDI averaged 2,751 (+88% YoY), with all segments above Q1 and last year."],
           ["供給偏緊：新船訂單約占船隊 13.8%、平均交期 4.28 年；2026 年超過 3,000 艘船進行特檢，每次進塢 3–4 週。", "Tight supply: orderbook ~13.8% of fleet with 4.28-year average lead time; 3,000+ ships face special surveys in 2026 (3–4 weeks in dock)."]),
   "gd": L(["法人認為下半年散裝市場佳，獲利可望穩健向上（法人觀點，公司未給數字指引）。", "Analysts expect a strong H2 dry bulk market (broker view; no company guidance)."]),
   "src": [S("經濟日報（2026/08/19）", "https://money.udn.com/money/amp/story/5607/9701018")]}]})
new.append({"id": "cmt", "zh": "中國航運", "en": "Chinese Maritime Transport", "cc": "TW", "ticker": "2612.TW", "ccy": ["新台幣", "TWD"], "cats": ["bulk"],
 "fleet": ["散裝與專用船隊", "Dry bulk and specialised fleet"], "ir": "https://mops.twse.com.tw", "next": TW_NEXT, "logo": None, "photo": G_BULK,
 "periods": [{"p": "2026Q2", "date": "2026-08", "title": ["第二季財報與月營收", "Q2 results and monthly revenue"],
   "kpis": [K("EPS", "EPS", "1.50 元", "NT$1.50", -18, 21), K("上半年 EPS", "H1 EPS", "2.74 元", "NT$2.74", -10),
            K("8 月營收", "August revenue", "5.13 億元", "NT$0.51bn", 27.16), K("1–8 月營收", "Jan–Aug revenue", "35.73 億元", "NT$3.57bn", 10.02)],
   "hl": L(["第二季 EPS 季增約兩成，但低於去年同期（去年同期有較多處分利益）；8 月營收年增 27%。", "Q2 EPS rose ~20% QoQ but was below last year; August revenue +27% YoY."]),
   "gd": L(["公司未提供數字指引。", "No numeric guidance."]),
   "src": [S("Winvest 營收快訊", "https://winvest.tw/News/Detail/94446")]}]})
new.append({"id": "sincere", "zh": "新興航運", "en": "Sincere Navigation", "cc": "TW", "ticker": "2605.TW", "ccy": ["新台幣", "TWD"], "cats": ["tanker", "bulk"],
 "fleet": ["VLCC 超大型油輪、VLOC 礦砂船、海岬型與 Kamsarmax 散裝船", "VLCC tankers, VLOC ore carriers, capesize and Kamsarmax bulkers"],
 "ir": "https://mops.twse.com.tw", "next": TW_NEXT, "logo": None, "photo": G_TANK,
 "periods": [{"p": "2026Q2", "date": "2026-08-11", "title": ["第二季財報", "Q2 results"],
   "kpis": [K("稅後淨利（歸屬母公司）", "Net profit to owners", "17.6 億元", "NT$1.76bn"), K("EPS", "EPS", "3.01 元", "NT$3.01", None, 356, "第一季 0.66 元", "Q1: NT$0.66"),
            K("上半年營收", "H1 revenue", "26.97 億元", "NT$2.70bn", 33.0), K("上半年營業利益", "H1 operating profit", "9.03 億元", "NT$0.90bn", 572), K("上半年 EPS", "H1 EPS", "3.67 元", "NT$3.67")],
   "hl": L(["第二季處分 VLCC 高登輪與海岬型青山輪，合計認列約 4,250 萬美元（約 13.4 億元）處分利益。", "Sold one VLCC and one capesize in Q2, booking ~US$42.5m (~NT$1.34bn) of gains."],
           ["上半年平均每日淨收入：VLCC 約 8.68 萬美元（年增 146%）、VLOC 3.22 萬（+56%）、Kamsarmax 1.6 萬（+31%）、海岬型 2.11 萬（+31%）。", "H1 average daily net earnings: VLCC ~US$86.8k (+146%), VLOC US$32.2k (+56%), Kamsarmax US$16k (+31%), capesize US$21.1k (+31%)."]),
   "gd": L(["另一艘 VLCC 美生輪預計明年 1–2 月交船，處分利益約 4,400 萬美元，約貢獻明年第一季稅前 EPS 2.37 元。", "Another VLCC sale delivers in Jan–Feb next year for ~US$44m gain, ~NT$2.37 pre-tax EPS in Q1 next year."],
           ["將靈活配置期租與現貨、評估汰舊換新，維持審慎財務與充足流動性（上半年現金約 104 億元）。", "Will balance time-charter and spot exposure, consider fleet renewal and keep ample liquidity (~NT$10.4bn cash)."]),
   "src": [S("ETtoday（2026/08/12）", "https://finance.ettoday.net/news/3217951")]}]})

new.append({"id": "starbulk", "zh": "Star Bulk", "en": "Star Bulk Carriers", "cc": "GR", "ticker": "SBLK (Nasdaq)", "ccy": ["美元", "USD"], "cats": ["bulk"],
 "fleet": ["135 艘（全數交付後 138 艘、1,380 萬載重噸），全球最大上市散裝船東之一", "135 vessels (138 / 13.8m dwt fully delivered), one of the largest listed dry bulk owners"],
 "ir": "https://www.starbulk.com", "next": {"p": "2026Q3", "date": "2026-11", "approx": True, "note": ["預計 11 月", "Expected November"]}, "logo": {"fav": "starbulk.com"}, "photo": photo("starbulk", cap=["Star Bulk 的 Star Crios", "Star Bulk's Star Crios"]),
 "periods": [{"p": "2026Q2", "date": "2026-08-05", "title": ["第二季財報", "Q2 results"],
   "kpis": [K("營收", "Revenue", "3.57 億美元", "US$357m", 44.5), K("淨利", "Net income", "1.45 億美元", "US$145m", None, None, "去年同期 4 萬美元", "Q2 2025: US$0.04m"),
            K("調整後 EBITDA", "Adj. EBITDA", "1.84 億美元", "US$184m", 167), K("平均日租（TCE）", "TCE/day", "24,486 美元", "US$24,486", 80), K("季配息", "Dividend", "每股 0.90 美元", "US$0.90/sh")],
   "hl": L(["2022 年第二季以來最好的一季；日均 TCE 年增約八成，營運成本每日 5,265 美元。", "Best quarter since Q2 2022; TCE up ~80% YoY with opex of US$5,265/day."],
           ["中東衝突升溫，燃油存貨出售帶來 2,100 萬美元收益。", "A US$21m gain on bunker sales came with the Middle East escalation."]),
   "gd": L(["執行長：支撐上半年的供需平衡仍在，展望「具建設性」，對今年剩餘時間樂觀。", "CEO: the supply-demand balance behind H1 is intact; outlook 'constructive' and optimistic for the rest of the year."]),
   "src": [S("Star Bulk Q2 2026 新聞稿", "https://www.starbulk.com/media/uploads_file/2026/08/05/p1jv9pap521j03bs21c7oivt1l669.pdf")]}]})
new.append({"id": "pacificbasin", "zh": "太平洋航運", "en": "Pacific Basin", "cc": "HK", "ticker": "2343.HK", "ccy": ["美元", "USD"], "cats": ["bulk"],
 "fleet": ["自有 106 艘輕便型、超輕便極限型與超靈便型散裝船，連同租入約 254 艘", "106 owned Handysize/Supramax/Ultramax bulkers, ~254 including chartered"],
 "ir": "https://www.pacificbasin.com", "next": {"p": "2026Q3", "date": "2026-10", "approx": True, "note": ["第三季營運更新，預計 10 月", "Q3 trading update, expected October"]}, "logo": None, "photo": photo("g_handy", cap=["Pacific Basin 的輕便型散裝船", "A Pacific Basin Handysize bulker"]),
 "periods": [{"p": "2026Q2", "date": "2026-08-06", "title": ["2026 上半年財報", "2026 interim results"],
   "kpis": [K("上半年營收", "H1 revenue", "11.1 億美元", "US$1.11bn", 8.8), K("上半年淨利", "H1 net profit", "1.05 億美元", "US$105m", 310, None, "去年同期 2,560 萬美元", "H1 2025: US$25.6m"),
            K("輕便型 TCE", "Handysize TCE", "14,150 美元/日", "US$14,150/day", None, None, "高於市場 1,950 美元", "US$1,950 above market"), K("超輕便極限型 TCE", "Supramax TCE", "16,550 美元/日", "US$16,550/day", None, None, "高於市場 2,370 美元", "US$2,370 above market")],
   "hl": L(["日租持續優於市場指數；營運活動每日利潤 1,060 美元、共 12,650 營運天。", "Continued to beat market indices; operating activity margin US$1,060/day over 12,650 days."],
           ["自有船隊市值 20.7 億美元，高於帳面 15.6 億美元；現金損益兩平低於每日 6,800 美元；期中股息提高至每股 15.5 港仙。", "Owned fleet worth US$2.07bn vs US$1.56bn book; cash breakeven below US$6,800/day; interim dividend raised to HK15.5¢."]),
   "gd": L(["執行長：地緣、總經、法規與天候因素將讓市況持續波動，同時帶來風險與機會。", "CEO: geopolitical, macro, regulatory and weather factors will keep markets volatile, creating risks and opportunities."]),
   "src": [S("Baird Maritime（2026/08/06）", "https://www.bairdmaritime.com/shipping/dry-cargo/bulkers/pacific-basin-reports-105m-h1-profit-as-freight-markets-strengthen"), S("Tiger 新聞：期中股息", "https://www.itiger.com/news/1105391406")]}]})
new.append({"id": "frontline", "zh": "Frontline", "en": "Frontline", "cc": "CY", "ticker": "FRO (NYSE)", "ccy": ["美元", "USD"], "cats": ["tanker"],
 "fleet": ["VLCC、Suezmax、LR2／Aframax 油輪船隊，全球最大上市油輪公司之一", "VLCC, Suezmax and LR2/Aframax fleet; one of the largest listed tanker owners"],
 "ir": "https://www.frontline.bm", "next": {"p": "2026Q3", "date": "2026-11", "approx": True, "note": ["預計 11 月", "Expected November"]}, "logo": {"fav": "frontline.bm"}, "photo": G_TANK,
 "periods": [{"p": "2026Q2", "date": "2026-08-28", "title": ["第二季財報", "Q2 results"],
   "kpis": [K("營收", "Revenue", "9.43 億美元", "US$943m", 96), K("淨利", "Net income", "6.59 億美元", "US$659m", 733, 18, "歷來最高單季；去年同期 7,910 萬", "Record quarter; Q2 2025: US$79.1m"),
            K("VLCC 日租", "VLCC TCE", "152,700 美元", "US$152,700"), K("Suezmax 日租", "Suezmax TCE", "111,500 美元", "US$111,500"), K("LR2 日租", "LR2 TCE", "92,400 美元", "US$92,400")],
   "hl": L(["創公司史上最高單季獲利；油輪三種船型日租都在 9 萬美元以上。", "Record quarterly profit; all three segments earned above US$90k/day."],
           ["胡塞再度攻擊紅海，更多 VLCC 改繞好望角，航程拉長。", "Renewed Houthi attacks pushed more VLCC volumes around the Cape, lengthening voyages."]),
   "gd": L(["第三季 VLCC 現貨已訂 86%、平均 156,900 美元/日；未來 12 個月損益兩平約 23,800 美元/日。", "Q3 VLCC spot 86% booked at US$156,900/day; 12-month breakeven ~US$23,800/day."],
           ["執行長：能源供應安全將主導戰略決策、改變貿易路線，對長期影響看法不變。", "CEO: energy security will increasingly drive strategy and reshape trade lanes; long-term conviction unchanged."]),
   "src": [S("Seatrade Maritime（2026/08/28）", "https://www.seatrade-maritime.com/tankers/record-profits-for-frontline-as-tanker-fundamentals-take-a-back-seat")]}]})
new.append({"id": "dht", "zh": "DHT", "en": "DHT Holdings", "cc": "BM", "ticker": "DHT (NYSE)", "ccy": ["美元", "USD"], "cats": ["tanker"],
 "fleet": ["專營 VLCC 超大型油輪", "Pure-play VLCC owner"], "ir": "https://www.dhtankers.com",
 "next": {"p": "2026Q3", "date": "2026-11", "approx": True, "note": ["預計 11 月初", "Expected early November"]}, "logo": {"fav": "dhtankers.com"}, "photo": G_TANK,
 "periods": [{"p": "2026Q2", "date": "2026-08-06", "title": ["第二季財報", "Q2 results"],
   "kpis": [K("營收", "Revenue", "2.85 億美元", "US$285m", 123), K("淨利", "Net income", "1.98 億美元", "US$198m", 254, None, "公司史上最強一季", "Strongest quarter in its history"),
            K("VLCC 現貨日租", "VLCC spot TCE", "162,600 美元", "US$162,600"), K("VLCC 期租日租", "VLCC time-charter TCE", "90,800 美元", "US$90,800"), K("季配息", "Dividend", "每股 1.22 美元", "US$1.22/sh", None, None, "連續第 66 季；配發 100% 一般淨利", "66th straight; 100% of ordinary net income")],
   "hl": L(["現貨 VLCC 日均 16.3 萬美元，綜合平均 12.7 萬美元；調整後營運毛利 2.31 億美元（去年同期 6,900 萬）。", "Spot VLCCs averaged US$162.6k/day, combined US$126.7k; adjusted gross operating profit US$231m (vs US$69m)."]),
   "gd": L(["中東衝突迫使航線拉長、提高延噸海浬並降低船隊效率；中國停止去庫存後，原油運輸需求可望明顯回升。", "Middle East hostilities force longer routes, lifting ton-miles and cutting fleet efficiency; China's crude demand should rebound sharply once destocking reverses."]),
   "src": [S("Baird Maritime（2026/08/06）", "https://www.bairdmaritime.com/shipping/tankers/more-than-three-fold-jump-in-q2-net-income-marks-dht-holdings-strongest-ever-quarter")]}]})
new.append({"id": "flexlng", "zh": "Flex LNG", "en": "Flex LNG", "cc": "BM", "ticker": "FLNG (NYSE)", "ccy": ["美元", "USD"], "cats": ["gas"],
 "fleet": ["新型 LNG 運輸船船隊，多數簽長期租約", "Modern LNG carrier fleet, mostly on long-term charters"], "ir": "https://www.flexlng.com",
 "next": {"p": "2026Q3", "date": "2026-11", "approx": True, "note": ["預計 11 月", "Expected November"]}, "logo": {"f": "Flex LNG logo.svg"}, "photo": photo("flexlng", cap=["Flex LNG 的 Flex Endeavour", "Flex LNG's Flex Endeavour"]),
 "periods": [{"p": "2026Q2", "date": "2026-08-19", "title": ["第二季財報", "Q2 results"],
   "kpis": [K("營收", "Revenue", "1.07 億美元", "US$107m", None, 32.7), K("平均日租（TCE）", "TCE/day", "86,119 美元", "US$86,119", None, 31.0),
            K("淨利", "Net income", "4,490 萬美元", "US$44.9m", None, 130), K("調整後 EBITDA", "Adj. EBITDA", "7,900 萬美元", "US$79.0m", None, 48.5), K("季配息", "Dividend", "每股 0.75 美元", "US$0.75/sh", None, None, "連續第 20 季", "20th in a row")],
   "hl": L(["日租較第一季大幅回升；今年剩餘時間約 89% 已有確定合約。", "TCE rebounded strongly from Q1; ~89% of remaining 2026 days are firmly contracted."],
           ["現金 3.97 億美元，2029 年前無債務到期。", "US$397m cash, no debt maturities before 2029."]),
   "gd": L(["維持全年指引：營收 3.45–3.70 億美元（不含 EUA）、日租 73,000–78,000 美元、調整後 EBITDA 2.55–2.80 億美元。", "Kept FY guidance: revenue US$345–370m (ex-EUAs), TCE US$73–78k/day, adj. EBITDA US$255–280m."],
           ["年底前還有 40–45 艘新船交付，運價仍將波動；歐洲儲氣偏低與卡達出口減少提供支撐。", "40–45 more newbuilds before year-end keep rates volatile; low European storage and reduced Qatari exports offer support."]),
   "src": [S("Flex LNG Q2 2026 新聞稿", "https://www.inderes.dk/releases/flex-lng-second-quarter-2026-earnings-release")]}]})
new.append({"id": "bwlpg", "zh": "BW LPG", "en": "BW LPG", "cc": "SG", "ticker": "BWLPG (Oslo/NYSE)", "ccy": ["美元", "USD"], "cats": ["gas"],
 "fleet": ["全球最大 VLGC（超大型液化石油氣船）船東之一，約 50 艘，其中 20 艘以上為 LPG 雙燃料", "One of the largest VLGC owners, ~50 ships incl. 20+ LPG dual-fuel"], "ir": "https://www.bwlpg.com",
 "next": {"p": "2026Q3", "date": "2026-11", "approx": True, "note": ["預計 11 月", "Expected November"]}, "logo": {"fav": "bwlpg.com"}, "photo": photo("bwlpg", cap=["BW LPG 的 BW Cedar 靠泊", "BW LPG's BW Cedar alongside"]),
 "periods": [{"p": "2026Q2", "date": "2026-08-28", "title": ["第二季財報", "Q2 results"],
   "kpis": [K("稅後淨利", "Net profit after tax", "1.38 億美元", "US$138m"), K("EPS", "EPS", "0.79 美元", "US$0.79"),
            K("航運日租（TCE）", "Shipping TCE/day", "74,000 美元", "US$74,000"), K("季配息", "Dividend", "每股 0.95 美元", "US$0.95/sh", None, None, "配發 100% 航運淨利", "100% of shipping NPAT")],
   "hl": L(["航運本業強勁；產品服務（LPG 貿易）已實現交易利益 1.27 億美元，但因 1.45 億美元未實現評價損失，帳上稅後虧損 3,100 萬美元。", "Strong shipping; product services realised US$127m trading gains but a US$145m unrealised mark-to-market loss left a US$31m after-tax loss."]),
   "gd": L(["第三季已鎖定約 92% 天數、平均約 88,000 美元/日。", "~92% of Q3 days fixed at ~US$88,000/day."],
           ["荷姆茲全面恢復通航可增加中東 LPG 出口，但會縮小美國—遠東價差；中東出口完全恢復需 12–36 個月，北美出口持續成長。", "A full Hormuz reopening would lift Middle East exports but narrow the US–Far East arbitrage; ME exports need 12–36 months to recover; North American exports keep growing."],
           ["產業手持 VLGC 訂單 155 艘、約占現有船隊 35%，供給壓力需留意。", "Industry VLGC orderbook of 155 ships (~35% of fleet) is a supply risk."]),
   "src": [S("BW LPG Q2 2026 公告", "https://www.inderes.dk/releases/bw-lpg-limited-financial-results-for-q2-2026")]}]})
for c in new:
    c.setdefault("privnote", None); E["companies"].append(c)
C = {c["id"]: c for c in E["companies"]}
C["msc"]["photo"] = photo("msc", cap=["MSC Irina（24,346 TEU）", "MSC Irina (24,346 TEU)"])

# tabs
E["tabs"] = [
 ["home", "首頁", "Home"], ["container", "貨櫃", "Containers"], ["bulk", "散裝", "Dry bulk"], ["tanker", "油輪", "Tankers"], ["gas", "LNG・LPG", "LNG・LPG"]]
E["groups"] = {
 "home": [["台灣・貨櫃", "Taiwan · containers", ["evergreen", "yangming", "wanhai"]], ["台灣・散裝", "Taiwan · dry bulk", ["uming", "wisdom", "taiwannav", "shihwei", "cmt"]], ["台灣・油輪", "Taiwan · tankers", ["sincere"]]],
 "container": [["台灣", "Taiwan", ["evergreen", "yangming", "wanhai"]], ["歐洲大型航商", "European majors", ["maersk", "msc", "cmacgm", "hapag"]], ["亞洲與其他", "Asia & others", ["cosco", "one", "hmm", "zim"]]],
 "bulk": [["台灣", "Taiwan", ["uming", "wisdom", "sincere", "taiwannav", "shihwei", "cmt"]], ["國際", "International", ["starbulk", "pacificbasin"]]],
 "tanker": [["台灣", "Taiwan", ["sincere"]], ["國際", "International", ["frontline", "dht"]]],
 "gas": [["國際", "International", ["flexlng", "bwlpg"]]]}
E["gnote"] = {"gas": ["台灣目前沒有以 LNG／LPG 船為主業的上市公司；台灣的 LNG 進口由中油與台電租用船隊運送。", "Taiwan has no listed LNG/LPG shipowner; its LNG imports move on ships chartered by CPC and Taipower."]}
E["photo_note"] = ["照片來自 Wikimedia Commons，依各圖授權標示作者；標「示意」者非該公司船舶。公司標誌僅供識別。", "Photos from Wikimedia Commons, credited per licence; 'illustrative' images are not the company's own ships. Logos shown for identification only."]
json.dump(E, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("companies", len(E["companies"]))
