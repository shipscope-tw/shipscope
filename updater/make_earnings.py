"""Curated earnings folder data -> earnings.json (hand-maintained; refresh after each results season).
Each string field is [zh, en]. kpi: k=label, v=value text, yoy/qoq=% (number) or None, note=[zh,en] or None.
Figures are as reported by the company or quoted in the cited press reports; "推算/derived" marks arithmetic from reported totals."""
import json, sys

def K(kz, ke, vz, ve, yoy=None, qoq=None, nz=None, ne=None, d=False):
    return {"k": [kz, ke], "v": [vz, ve], "yoy": yoy, "qoq": qoq, "note": [nz, ne] if nz else None, "derived": d}
def L(*pairs): return [list(p) for p in pairs]
def S(t, u): return {"t": t, "u": u}

companies = []

# ---------------- Taiwan ----------------
companies.append({
 "id": "evergreen", "zh": "長榮海運", "en": "Evergreen Marine", "cc": "TW", "ticker": "2603.TW", "ccy": ["新台幣", "TWD"],
 "fleet": ["營運船隊約 200.6 萬 TEU，全球第 7（市占 5.9%）", "Operated fleet ~2.01m TEU, world No.7 (5.9% share)"],
 "ir": "https://www.evergreen-marine.com",
 "next": {"p": "2026Q3", "date": "2026-11-14", "approx": True, "note": ["法定公告期限 11/14，通常 11 月中公布", "Statutory deadline 14 Nov; usually mid-November"]},
 "periods": [
  {"p": "2026Q3", "kind": "flash", "date": "2026-10-09", "title": ["第三季營收快報（財報尚未公布）", "Q3 revenue flash (results not yet released)"],
   "kpis": [K("Q3 營收（7–9 月加總）", "Q3 revenue (Jul–Sep)", "1,467.8 億元", "NT$146.8bn", 51.4, 39.6, "依月營收加總；年增率以累計營收回推", "Sum of monthly revenue; YoY derived from YTD figures", True),
            K("9 月營收", "September revenue", "497.1 億元", "NT$49.7bn", 63.75),
            K("前 9 月累計營收", "Jan–Sep revenue", "3,384.5 億元", "NT$338.4bn", 15.36)],
   "hl": L(["7–9 月單月營收都在 480 億元以上，Q3 營收比 Q2 再多約四成，反映旺季與運價上漲。", "Monthly revenue held above NT$48bn in Jul–Sep; Q3 revenue was ~40% above Q2 on peak season and higher rates."],
           ["9 月營收年增 63.75%，是年增幅最大的月份；前 9 月累計已轉為年增 15.36%（上半年仍為年減 2.43%）。", "September revenue rose 63.75% YoY, the strongest month; Jan–Sep turned to +15.36% YoY (H1 was still −2.43%)."]),
   "gd": L(["獲利要等 11 月中第三季財報；營收成長不等於獲利同幅成長，需留意燃油與繞道成本。", "Profit awaits Q3 results in mid-November; revenue growth need not translate one-for-one into profit given fuel and diversion costs."]),
   "src": [S("Winvest 營收快訊（2026/10/09）", "https://winvest.tw/News/Detail/95592"), S("長榮 7 月營收（Winvest）", "https://winvest.tw/News/Detail/91802"), S("長榮 8 月營收（Winvest）", "https://winvest.tw/News/Detail/93916")]},
  {"p": "2026Q2", "date": "2026-08-13", "title": ["第二季財報", "Q2 results"],
   "kpis": [K("營收", "Revenue", "1,051.6 億元", "NT$105.2bn", 21.60),
            K("營業毛利率", "Gross margin", "22.80%", "22.80%", None, None, "Q1 為 15.47%", "Q1: 15.47%"),
            K("稅後淨利（歸屬母公司）", "Net profit to owners", "160.3 億元", "NT$16.0bn", 46.33),
            K("EPS", "EPS", "7.41 元", "NT$7.41", 46.44, 92.97),
            K("上半年 EPS", "H1 EPS", "11.24 元", "NT$11.24", None, None, "上半年淨利 243.4 億元，年減 36.48%", "H1 net NT$24.3bn, −36.48% YoY")],
   "hl": L(["第二季獲利主要受惠全球貿易需求有韌性，加上出貨旺季提前，帶動亞洲—北美、亞洲—歐洲主要航線的貨量與運價。", "Q2 profit was driven by resilient trade demand and an early peak season that lifted cargo and rates on Asia–North America and Asia–Europe."],
           ["毛利率由第一季 15.47% 回升至 22.80%，單季 EPS 7.41 元居貨櫃三雄之首。", "Gross margin recovered from 15.47% in Q1 to 22.80%; Q2 EPS of NT$7.41 was the highest of Taiwan's big three."],
           ["上半年仍較去年同期衰退（營收 −2.43%、淨利 −36.48%），主因是第一季運價偏低。", "H1 was still down YoY (revenue −2.43%, net −36.48%) because of weak Q1 rates."]),
   "gd": L(["公司表示下半年總體經濟與地緣風險仍有變數，會密切關注中東局勢、各區終端消費與全球運力供需，並調整航線布局與空櫃調度。", "Management sees macro and geopolitical uncertainty in H2 and will watch the Middle East, end demand and global capacity, adjusting routes and empty-container repositioning."],
           ["運力擴張：未來五年預計新增約 89 萬 TEU 運力。", "Fleet growth: about 890k TEU of new capacity planned over five years."]),
   "src": [S("航貿週刊（2026/08/14）", "https://shippingdigest.tw/news/20260814n1/"), S("時報資訊：貨櫃三雄 Q2 獲利", "https://www.chinatimes.com/realtimenews/20260814001046-260410"), S("今周刊（2026/08/24）", "https://www.businesstoday.com.tw/article/category/183009/post/202608240005/")]},
  {"p": "2026Q1", "date": "2026-05-14", "title": ["第一季財報", "Q1 results"],
   "kpis": [K("營收", "Revenue", "865.1 億元", "NT$86.5bn", -21.33),
            K("營業毛利率", "Gross margin", "15.47%", "15.47%"),
            K("稅後淨利（歸屬母公司）", "Net profit to owners", "83.0 億元", "NT$8.3bn", -69.65),
            K("EPS", "EPS", "3.84 元", "NT$3.84", -69.62)],
   "hl": L(["貨量較去年同期成長，但運價下滑，營收與獲利明顯衰退。", "Volumes grew YoY but lower freight rates cut revenue and profit sharply."]),
   "gd": L(["進入傳統旺季後，貨主提前備貨意願提高，有助出貨動能與運價。", "Shippers' earlier stocking ahead of peak season should support volumes and rates."],
           ["持續關注中東與紅海局勢；提升資產配置效率、加速低碳船隊轉型。", "Watching the Middle East and Red Sea; improving asset efficiency and accelerating the low-carbon fleet transition."]),
   "src": [S("經濟日報／中央社（2026/05/14）", "https://money.udn.com/money/story/5710/9503545")]}
 ]})

companies.append({
 "id": "yangming", "zh": "陽明海運", "en": "Yang Ming Marine", "cc": "TW", "ticker": "2609.TW", "ccy": ["新台幣", "TWD"],
 "fleet": ["營運船隊約 74.2 萬 TEU，全球第 9（市占 2.2%）；運費收入歐洲線 39%、美洲線 37%", "Fleet ~742k TEU, world No.9 (2.2%); freight revenue 39% Europe, 37% Americas"],
 "ir": "https://www.yangming.com",
 "next": {"p": "2026Q3", "date": "2026-11-14", "approx": True, "note": ["法定公告期限 11/14，通常 11 月中公布並舉行法說", "Deadline 14 Nov; results and investor call usually mid-November"]},
 "periods": [
  {"p": "2026Q3", "kind": "flash", "date": "2026-10-09", "title": ["第三季營收快報（財報尚未公布）", "Q3 revenue flash (results not yet released)"],
   "kpis": [K("Q3 營收（7–9 月加總）", "Q3 revenue (Jul–Sep)", "641.5 億元", "NT$64.1bn", 52.4, 39.7, "依累計營收回推", "Derived from YTD revenue", True),
            K("9 月營收", "September revenue", "217.0 億元", "NT$21.7bn", 69.94),
            K("前 9 月累計營收", "Jan–Sep revenue", "1,487.3 億元", "NT$148.7bn", 17.79)],
   "hl": L(["9 月營收年增近七成，公司說明主因是整體運價上漲；Q3 營收比 Q2 多約四成。", "September revenue rose ~70% YoY on higher overall rates; Q3 revenue was ~40% above Q2."],
           ["陽明以歐美長程線為主，運價彈性大：運價上漲時營收成長幅度通常高於以近洋為主的萬海。", "Yang Ming is weighted to long-haul Europe/US trades, so revenue reacts more strongly to rate moves."]),
   "gd": L(["獲利與法說將於 11 月中公布。", "Profit and investor call due mid-November."]),
   "src": [S("Winvest 營收快訊（2026/10/09）", "https://winvest.tw/News/Detail/96027")]},
  {"p": "2026Q2", "date": "2026-08-12", "title": ["第二季財報", "Q2 results"],
   "kpis": [K("營收", "Revenue", "459.2 億元", "NT$45.9bn", 18.78),
            K("營業利益", "Operating profit", "56.8 億元", "NT$5.7bn", 45.71),
            K("稅後淨利（歸屬母公司）", "Net profit to owners", "57.3 億元", "NT$5.7bn", 482.02),
            K("EPS", "EPS", "1.64 元", "NT$1.64", 485, 300),
            K("上半年 EPS", "H1 EPS", "2.05 元", "NT$2.05", None, None, "上半年淨利 71.7 億元，年減 18.17%", "H1 net NT$7.2bn, −18.17% YoY")],
   "hl": L(["單季營收創 6 個季度新高，淨利年增約 4.8 倍、季增約 3 倍。", "Quarterly revenue hit a six-quarter high; net profit rose ~4.8x YoY and ~3x QoQ."],
           ["第二季上海與歐洲主要碼頭塞港較嚴重，影響船期。", "Port congestion in Shanghai and major European terminals was heavy in Q2."]),
   "gd": L(["第三季歐美航線進入傳統旺季，出貨動能有助市場維持正向。", "Q3 peak season on Europe/US lanes should keep the market positive."],
           ["地緣政治與關稅政策仍將主導貨流與運力變化；公司將彈性調整船隊與航次、強化成本控管。", "Geopolitics and tariffs will keep driving cargo flows and capacity; the company will flex fleet deployment and control costs."],
           ["引用研究機構：2026 年全球運力成長約 4.2%–4.4%，需求成長約 2.1%–2.5%（Alphaliner、Drewry）。", "Cited forecasts: 2026 fleet growth ~4.2–4.4% vs demand ~2.1–2.5% (Alphaliner, Drewry)."],
           ["運能由 71.4 萬 TEU 增至 74.2 萬 TEU，已核准 24 艘新船於 2026–2030 年交付。", "Capacity up from 714k to 742k TEU; 24 newbuilds approved for 2026–2030 delivery."]),
   "src": [S("ETtoday（2026/08/12）", "https://finance.ettoday.net/news/3217942"), S("鉅亨網／優分析", "https://uanalyze.com.tw/articles/8823053268"), S("時報資訊：貨櫃三雄 Q2 獲利", "https://www.chinatimes.com/realtimenews/20260814001046-260410")]},
  {"p": "2026Q1", "date": "2026-05-13", "title": ["第一季財報", "Q1 results"],
   "kpis": [K("營收", "Revenue", "386.6 億元", "NT$38.7bn", -15.05),
            K("營業利益", "Operating profit", "約 7.5 億元", "~NT$0.75bn", None, None, "上半年 64.32 億減第二季 56.84 億推算", "H1 minus Q2", True),
            K("稅後淨利", "Net profit", "14.4 億元", "NT$1.4bn", -81.54),
            K("EPS", "EPS", "0.41 元", "NT$0.41", -81.61)],
   "hl": L(["平均運價較去年同期下降，加上船隊調配受中東戰事干擾，獲利大減約八成。", "Lower average rates and fleet disruption from the Middle East war cut profit by ~80%."]),
   "gd": L(["Alphaliner 預估 2026 年需求成長 2.5%、供給成長 3.8%（約 161 萬 TEU 新船），但繞道可吸收部分運能。", "Alphaliner: 2026 demand +2.5% vs supply +3.8% (~1.61m TEU deliveries), partly absorbed by diversions."],
           ["把握五一後出貨回溫與旺季商機，提升艙位利用率；啟動貨櫃汰舊換新。", "Targeting the post-May recovery and peak season; renewing its container fleet."]),
   "src": [S("旺得富（2026/05/14）", "https://wantrich.chinatimes.com/news/20260514900152-420101")]}
 ]})

companies.append({
 "id": "wanhai", "zh": "萬海航運", "en": "Wan Hai Lines", "cc": "TW", "ticker": "2615.TW", "ccy": ["新台幣", "TWD"],
 "fleet": ["2025 年底 116 艘、約 57.3 萬 TEU（全數自有）；亞洲近洋約占貨量 55%", "116 ships, ~573k TEU at end-2025 (all owned); intra-Asia ~55% of volume"],
 "ir": "https://www.wanhai.com",
 "next": {"p": "2026Q3", "date": "2026-11-14", "approx": True, "note": ["法定公告期限 11/14", "Statutory deadline 14 Nov"]},
 "periods": [
  {"p": "2026Q3", "kind": "flash", "date": "2026-10-09", "title": ["第三季營收快報（財報尚未公布）", "Q3 revenue flash (results not yet released)"],
   "kpis": [K("Q3 營收（7–9 月加總）", "Q3 revenue (Jul–Sep)", "596.2 億元", "NT$59.6bn", 70.2, 39.0, "依累計營收回推", "Derived from YTD revenue", True),
            K("9 月營收", "September revenue", "217.8 億元", "NT$21.8bn", 97.63),
            K("前 9 月累計營收", "Jan–Sep revenue", "1,361.6 億元", "NT$136.2bn", 27.28)],
   "hl": L(["9 月營收年增近一倍，為三雄中年增幅最大；7 月單月自結 EPS 2.17 元。", "September revenue nearly doubled YoY, the fastest of the big three; July self-reported EPS was NT$2.17."]),
   "gd": L(["獲利將於 11 月中公布；7 月自結數字未經查核，不宜直接乘三推估全季。", "Profit due mid-November; July's unaudited figure should not simply be tripled."]),
   "src": [S("Winvest 營收快訊（2026/10/09）", "https://winvest.tw/en/News/Detail/96031"), S("理財周刊（2026/09/04）", "https://www.moneyweekly.com.tw/_Article?AID=246905")]},
  {"p": "2026Q2", "date": "2026-08-13", "title": ["第二季財報", "Q2 results"],
   "kpis": [K("營收", "Revenue", "429.0 億元", "NT$42.9bn", 23),
            K("營業利益", "Operating profit", "111.3 億元", "NT$11.1bn", 28.5, None, "營益率 25.95%、毛利率 30.37%", "Op. margin 25.95%, gross 30.37%"),
            K("稅後淨利（歸屬母公司）", "Net profit to owners", "115.4 億元", "NT$11.5bn", 971, None, "去年同期 10.77 億元", "Q2 2025: NT$1.08bn"),
            K("EPS", "EPS", "4.11 元", "NT$4.11", 981, 50.55, "去年同期 0.38 元", "Q2 2025: NT$0.38"),
            K("上半年 EPS", "H1 EPS", "6.84 元", "NT$6.84", 95, None, "上半年淨利 192.1 億元，年增約 96%", "H1 net NT$19.2bn, ~+96% YoY")],
   "hl": L(["本業與業外同步改善：Q2 業外淨收益 49.79 億元（去年同期為損失 75.69 億元，主因匯損），EPS 年增約 10 倍。", "Both core and non-operating results improved: Q2 non-operating gain NT$4.98bn vs a NT$7.57bn loss a year earlier (FX), lifting EPS ~10x YoY."],
           ["以亞洲區間近洋線為主，第一季運價下跌時衰退幅度遠小於長榮、陽明。", "Its intra-Asia focus meant a much smaller Q1 decline than Evergreen and Yang Ming."]),
   "gd": L(["公司認為下半年供需結構仍相對健康；燃油成本雖升高，運價指數仍大幅高於年初，租船市場熱絡。", "Sees H2 supply-demand as relatively healthy; despite higher fuel costs, rate indices are well above the start of the year and the charter market is firm."],
           ["看好第四季節慶備貨與庫存回補需求。", "Expects Q4 holiday and restocking demand."],
           ["2026 年交付 7 艘新船（+4.88 萬 TEU）；2027–2030 年共 42 艘、約 47.5 萬 TEU，2027 年為交船高峰（+16.87 萬 TEU、資本支出約 18.61 億美元）。", "7 ships (+48.8k TEU) in 2026; 42 ships (~475k TEU) in 2027–2030, peaking in 2027 (+168.7k TEU, capex ~US$1.86bn)."]),
   "src": [S("理財周刊（2026/09/04）", "https://www.moneyweekly.com.tw/_Article?AID=246905"), S("鉅亨網／優分析（2026/08/14）", "https://uanalyze.com.tw/articles/8259753403"), S("時報資訊：貨櫃三雄 Q2 獲利", "https://www.chinatimes.com/realtimenews/20260814001046-260410")]},
  {"p": "2026Q1", "date": "2026-05", "title": ["第一季財報", "Q1 results"],
   "kpis": [K("營收", "Revenue", "約 336.4 億元", "~NT$33.6bn", None, None, "上半年減第二季推算", "H1 minus Q2", True),
            K("營業利益", "Operating profit", "約 58.3 億元", "~NT$5.8bn", None, None, "上半年減第二季推算", "H1 minus Q2", True),
            K("稅後淨利（歸屬母公司）", "Net profit to owners", "約 76.7 億元", "~NT$7.7bn", None, None, "上半年減第二季推算", "H1 minus Q2", True),
            K("EPS", "EPS", "2.73 元", "NT$2.73", -12.22, -23.53, None, None, True)],
   "hl": L(["近洋線運價波動較溫和，EPS 僅年減約 12%，抗跌性優於長程線為主的同業。", "Milder intra-Asia rate swings meant EPS fell only ~12% YoY, holding up better than long-haul peers."]),
   "gd": L(["萬海抗跌來自航線結構，不代表體質較佳；運價上漲時彈性也較小。", "Its resilience reflects route mix rather than stronger fundamentals; upside is also smaller when rates rise."]),
   "src": [S("今周刊（2026/08/24）", "https://www.businesstoday.com.tw/article/category/183009/post/202608240005/"), S("理財周刊（2026/08/29）", "https://www.moneyweekly.com.tw/_Article?AID=245637")]}
 ]})

# ---------------- Europe ----------------
companies.append({
 "id": "maersk", "zh": "馬士基", "en": "A.P. Moller-Maersk", "cc": "DK", "ticker": "MAERSK-B.CO", "ccy": ["美元", "USD"],
 "fleet": ["營運船隊約 472 萬 TEU，全球第 2（市占 13.8%）；與赫伯羅特組 Gemini 合作", "Fleet ~4.72m TEU, world No.2 (13.8%); Gemini cooperation with Hapag-Lloyd"],
 "ir": "https://investor.maersk.com/financials/financial-reports",
 "next": {"p": "2026Q3", "date": "2026-11-05", "approx": False, "note": ["第三季報告 11/5 公布", "Q3 interim report on 5 Nov"]},
 "periods": [
  {"p": "2026Q2", "date": "2026-08-13", "gdir": "up", "title": ["第二季報告", "Q2 interim report"],
   "kpis": [K("營收", "Revenue", "158 億美元", "US$15.8bn", 20),
            K("EBITDA", "EBITDA", "30 億美元", "US$3.0bn", 30, None, "去年同期 23 億美元", "Q2 2025: US$2.3bn"),
            K("EBIT", "EBIT", "16 億美元", "US$1.6bn", 89, None, "去年同期 8.45 億美元；EBIT 率 10.0%", "Q2 2025: US$845m; margin 10.0%"),
            K("海運 EBIT", "Ocean EBIT", "9.35 億美元", "US$935m", None, None, "Q1 為 −1.92 億美元", "Q1: −US$192m")],
   "hl": L(["海運營收年增 23%：裝載貨量 +4.1%、平均運價 +22%，船舶利用率 96%。", "Ocean revenue +23%: loaded volumes +4.1%, average loaded rate +22%, utilisation 96%."],
           ["荷姆茲海峽受阻，波灣進口貨改由其他港口與內陸轉運，受影響的運力調往其他航線；遠東（特別是中國）出口強勁。", "With Hormuz disrupted, Gulf-bound cargo was rerouted via other ports and inland; affected capacity was redeployed. Far East (especially China) exports were strong."],
           ["歐洲、中東、南美東岸、西非港口壅塞推升即期運價；物流 EBIT 2.17 億、碼頭 4.58 億美元。", "Congestion in Europe, the Middle East, ECSA and West Africa lifted spot rates; Logistics EBIT US$217m, Terminals US$458m."],
           ["執行長 Clerc：這一季再次說明航運進入「波動加劇的新時代」，瓶頸已成常態。", "CEO Clerc: the quarter shows a 'new era of heightened volatility'; bottlenecks are entrenched."]),
   "gd": L(["全年基礎 EBITDA 上修至 105–125 億美元（前次 80–100 億；5 月時為 45–70 億）。", "FY underlying EBITDA raised to US$10.5–12.5bn (prior US$8–10bn; May: US$4.5–7.0bn)."],
           ["全年基礎 EBIT 上修至 45–65 億美元（前次 20–40 億）；自由現金流 > 0（前次 ≥ −15 億）。", "FY underlying EBIT raised to US$4.5–6.5bn (prior US$2–4bn); free cash flow > 0 (prior ≥ −US$1.5bn)."],
           ["假設全球貨櫃需求成長約 4%；2025–26 與 2026–27 資本支出各 100–110 億美元。", "Assumes ~4% container demand growth; capex US$10–11bn for both 2025–26 and 2026–27."],
           ["敏感度：運價每 FFE ±100 美元，全年 EBIT ±7 億美元；10 億美元庫藏股持續執行。", "Sensitivity: ±US$100/FFE in rates = ±US$0.7bn FY EBIT; US$1bn buyback continues."]),
   "src": [S("Maersk 新聞稿（2026/08/13）", "https://www.maersk.com/news/articles/2026/08/13/maersk-delivers-strong-q2-and-raises-full-year-guidance"), S("Maersk 財報下載", "https://investor.maersk.com/financials/financial-reports")]},
  {"p": "2026Q1", "date": "2026-05-07", "gdir": "keep", "title": ["第一季報告", "Q1 interim report"],
   "kpis": [K("營收", "Revenue", "略低於去年同期", "Slightly below last year"),
            K("EBITDA", "EBITDA", "18 億美元", "US$1.8bn", -33, None, "去年同期 27 億美元", "Q1 2025: US$2.7bn"),
            K("EBIT", "EBIT", "3.4 億美元", "US$340m", -74, None, "去年同期 13 億美元；EBIT 率 2.6%", "Q1 2025: US$1.3bn; margin 2.6%"),
            K("海運 EBIT", "Ocean EBIT", "−1.92 億美元", "−US$192m")],
   "hl": L(["裝載貨量 +9.3%，但產業運力過剩壓低運價，海運部門虧損。", "Loaded volumes +9.3%, but industry overcapacity pressured rates and Ocean lost money."],
           ["儘管中東干擾，海運單位成本下降 7%；碼頭 EBIT 4.36 億、物流 1.73 億美元。", "Ocean unit cost fell 7% despite Middle East disruption; Terminals EBIT US$436m, Logistics US$173m."]),
   "gd": L(["維持全年指引：基礎 EBITDA 45–70 億、EBIT −15～10 億美元、自由現金流 ≥ −30 億美元（之後兩度上修）。", "Kept guidance: EBITDA US$4.5–7.0bn, EBIT −US$1.5–1.0bn, FCF ≥ −US$3.0bn (later raised twice)."]),
   "src": [S("Maersk 新聞稿（2026/05/07）", "https://www.maersk.com/news/articles/2026/05/07/maersk-delivered-volume-growth-across-all-businesses-in-q1")]}
 ]})

companies.append({
 "id": "hapag", "zh": "赫伯羅特", "en": "Hapag-Lloyd", "cc": "DE", "ticker": "HLAG.DE", "ccy": ["美元", "USD"],
 "fleet": ["營運船隊約 238 萬 TEU，全球第 5（市占 7.0%）；正在收購以色列 ZIM", "Fleet ~2.38m TEU, world No.5 (7.0%); acquiring Israel's ZIM"],
 "ir": "https://www.hapag-lloyd.com/en/ir/publications/financial-report.html",
 "next": {"p": "2026Q3", "date": "2026-11-12", "approx": False, "note": ["第三季報告 11/12（依市場行事曆）", "Q3 statement on 12 Nov (market calendar)"]},
 "periods": [
  {"p": "2026Q2", "date": "2026-08-13", "gdir": "up", "title": ["第二季報告", "Q2 results"],
   "kpis": [K("貨櫃航運營收", "Liner revenue", "57 億美元", "US$5.7bn"),
            K("EBITDA", "EBITDA", "8.29 億美元", "US$829m", None, None, "略高於去年同期", "Slightly above Q2 2025"),
            K("EBIT", "EBIT", "1.76 億美元", "US$176m", None, None, "低於去年同期", "Below Q2 2025"),
            K("淨利", "Group profit", "0.83 億美元", "US$83m", None, None, "Q1 虧損 2.56 億美元", "Q1: −US$256m"),
            K("平均運價", "Avg freight rate", "1,475 美元/TEU", "US$1,475/TEU", 9),
            K("貨量", "Volume", "350 萬 TEU", "3.5m TEU", 3)],
   "hl": L(["亞洲出口強勁、美國需求改善，即期運價與貨量明顯優於受干擾的第一季。", "Strong Asian exports and better US demand lifted spot rates and volumes from a disrupted Q1."],
           ["荷姆茲海峽封鎖在第二季造成約 6 億美元額外成本（燃油、保險、倉儲、改道、內陸運輸）。", "The Hormuz blockage added ~US$600m of Q2 costs (bunker, insurance, storage, rerouting, inland transport)."],
           ["碼頭與基礎設施部門營收 1.91 億、EBITDA 0.55 億美元，受惠首次全年合併 J M Baxi 貨櫃業務。", "Terminal & Infrastructure: revenue US$191m, EBITDA US$55m, helped by first full consolidation of J M Baxi's container business."]),
   "gd": L(["7/13 已上修全年：EBITDA 27–37 億美元、EBIT 1–11 億美元（原 11–31 億與 −15～5 億）。", "Raised on 13 Jul: FY EBITDA US$2.7–3.7bn, EBIT US$0.1–1.1bn (was US$1.1–3.1bn and −US$1.5–0.5bn)."],
           ["公司提醒指引仍受運價波動與中東衝突影響，不確定性高。", "Guidance remains highly uncertain given volatile rates and the Middle East conflict."],
           ["併購 ZIM：每股 35 美元現金，ZIM 股東已於 4/30 同意，目標 2026 年第四季完成，仍待以色列政府「黃金股」等監管核准。", "ZIM takeover at US$35/share cash; ZIM holders approved 30 Apr; targeted to close Q4 2026, pending approvals incl. Israel's golden share."]),
   "src": [S("Hapag-Lloyd H1 2026 投資人報告", "https://www.hapag-lloyd.com/content/dam/website/downloads/ir/HLAG_Investor_Report_H1_2026.pdf"), S("Hellenic Shipping News（2026/08/14）", "https://www.hellenicshippingnews.com/earnings-recovery-in-q2-despite-substantial-cost-headwinds/"), S("ZIM Q2 新聞稿（併購說明）", "https://s203.q4cdn.com/172866090/files/doc_financials/2026/q2/ZIM-Q2-2026-PR-Eng-19-8-2026-FINAL-new-template.pdf")]},
  {"p": "2026Q1", "date": "2026-05-13", "gdir": "keep", "title": ["第一季報告", "Q1 results"],
   "kpis": [K("貨櫃航運營收", "Liner revenue", "48 億美元", "US$4.8bn"),
            K("EBITDA", "EBITDA", "4.94 億美元", "US$494m"),
            K("EBIT", "EBIT", "−1.57 億美元", "−US$157m"),
            K("淨利", "Group profit", "−2.56 億美元", "−US$256m"),
            K("平均運價", "Avg freight rate", "1,330 美元/TEU", "US$1,330/TEU", -9.6, None, "去年同期 1,471 美元", "Q1 2025: US$1,471")],
   "hl": L(["公司自評「不滿意」：運價下跌、歐美嚴重天候干擾營運，加上荷姆茲海峽封鎖。", "Management called it unsatisfactory: lower rates, severe weather in Europe/North America and the Hormuz blockage."]),
   "gd": L(["維持全年 EBITDA 11–31 億美元、EBIT −15～5 億美元（7 月上修）。", "Kept FY EBITDA US$1.1–3.1bn and EBIT −US$1.5–0.5bn (raised in July)."]),
   "src": [S("HLAG Q1 2026 投資人報告", "https://www.hapag-lloyd.com/content/dam/website/downloads/ir/HLAG_Investor_Report_Q1_2026.pdf"), S("Container News（2026/05/13）", "https://container-news.com/hapag-lloyd-reports-unsatisfactory-first-quarter/")]}
 ]})

companies.append({
 "id": "msc", "zh": "地中海航運", "en": "MSC", "cc": "CH", "ticker": None, "ccy": ["—", "—"], "private": True,
 "fleet": ["全球最大貨櫃航商：營運船隊約 733 萬 TEU（市占 21.5%），手持訂單 134 艘", "World's largest carrier: ~7.33m TEU (21.5% share), 134 ships on order"],
 "ir": None,
 "privnote": ["MSC 為 Aponte 家族持有的未上市公司，不公布財報、也不舉行法說，因此沒有營收與獲利數字。可參考的是船隊與市占（Alphaliner），以及同業（馬士基、達飛）財報所反映的市場狀況。", "MSC is privately owned by the Aponte family and publishes no financial results or earnings calls. Fleet and market-share data (Alphaliner) and peers' results are the available proxies."],
 "periods": [],
 "src": [S("Container News：2026 上半年航商排名（Alphaliner）", "https://container-news.com/largest-container-shipping-companies-at-the-end-of-h1-2026/")]})

companies.append({
 "id": "cmacgm", "zh": "達飛海運", "en": "CMA CGM", "cc": "FR", "ticker": None, "ccy": ["美元", "USD"],
 "fleet": ["營運船隊約 437 萬 TEU，全球第 3（市占 12.8%）；未上市但每季公布財報", "Fleet ~4.37m TEU, world No.3 (12.8%); private but reports quarterly"],
 "ir": "https://www.cmacgm-group.com/en/finance",
 "next": {"p": "2026Q3", "date": "2026-11", "approx": True, "note": ["預計 11 月公布", "Expected in November"]},
 "periods": [
  {"p": "2026Q2", "date": "2026-07-28", "title": ["第二季財報", "Q2 results"],
   "kpis": [K("營收", "Revenue", "157 億美元", "US$15.7bn", 19.2),
            K("EBITDA", "EBITDA", "30 億美元", "US$3.0bn", 31, None, "EBITDA 率 19%", "Margin 19%"),
            K("淨利", "Net income", "7.7 億美元", "US$770m", 48, None, "去年同期 5.2 億美元", "Q2 2025: US$520m"),
            K("海運每 TEU 收入", "Shipping revenue/TEU", "1,575 美元", "US$1,575", 15.1),
            K("海運貨量", "Shipping volume", "630 萬 TEU", "6.3m TEU", 6)],
   "hl": L(["海運 EBITDA 23 億美元（去年同期 16 億），EBITDA 率 22.7%，主因貨量與運價同步改善。", "Shipping EBITDA US$2.3bn (vs US$1.6bn), margin 22.7%, on both volumes and rates."],
           ["物流（CEVA）營收 50 億美元、+8.5%，但 EBITDA 3.88 億、−15.4%：貨運代理承壓、汽車產業疲弱。", "Logistics (CEVA) revenue US$5.0bn (+8.5%) but EBITDA US$388m (−15.4%) on forwarding pressure and weak autos."],
           ["碼頭、航空貨運、媒體等其他業務營收 +47.6%、EBITDA +44.5%。", "Other activities (terminals, air cargo, media): revenue +47.6%, EBITDA +44.5%."],
           ["中東衝突成本：船隻受困波灣、保險費上升、進出該區的航線貨量下降，由較高運價抵銷。", "Middle East costs (ships trapped in the Gulf, higher insurance, lower volumes on Gulf services) were offset by firmer rates."]),
   "gd": L(["未提供數字指引；公司表示地緣環境仍高度不確定，中東緊張持續影響航線、運價與成本。", "No numeric guidance; geopolitics remain highly uncertain, with Middle East tensions affecting routes, rates and costs."],
           ["部分國家的關稅措施可能在未來幾個月影響貿易流向；將以「審慎但靈活」方式因應。", "Tariffs by some countries may shift trade flows in coming months; approach is 'prudent yet agile'."]),
   "src": [S("CMA CGM 新聞稿", "https://cmacgm-group.com/en/news-media/second-quarter-2026-financial-results"), S("FreightWaves（2026/07/28）", "https://www.freightwaves.com/news/geopolitics-helps-cma-cgm-shipping-profit-soar-42")]},
  {"p": "2026Q1", "date": "2026-05", "title": ["第一季財報", "Q1 results"],
   "kpis": [K("營收", "Revenue", "132 億美元", "US$13.2bn", -0.2),
            K("EBITDA", "EBITDA", "21 億美元", "US$2.1bn", -31.6, None, "EBITDA 率 16.0%", "Margin 16.0%"),
            K("海運每 TEU 收入", "Shipping revenue/TEU", "1,351 美元", "US$1,351", -9.8),
            K("海運貨量", "Shipping volume", "590 萬 TEU", "5.9m TEU", 1.5)],
   "hl": L(["海運營收 −8.5%、EBITDA 15 億美元（去年同期 25 億）；物流營收 +6.6% 但 EBITDA −17.2%。", "Shipping revenue −8.5%, EBITDA US$1.5bn (vs US$2.5bn); logistics revenue +6.6% but EBITDA −17.2%."]),
   "gd": L(["中東緊張持續影響航線、供需與營運成本（油價上升、運價波動）；公司將依靠業務多角化因應。", "Middle East tensions keep affecting routes, market balance and costs; the group relies on diversification."]),
   "src": [S("CMA CGM 新聞稿", "https://www.cmacgm-group.com/en/news-media/first-quarter-2026-financial-results")]}
 ]})

# ---------------- Asia (others) ----------------
companies.append({
 "id": "cosco", "zh": "中遠海控", "en": "COSCO Shipping Holdings", "cc": "CN", "ticker": "601919.SS / 1919.HK", "ccy": ["人民幣", "CNY"],
 "fleet": ["中遠海運集團船隊約 363 萬 TEU，全球第 4（市占 10.6%），含中遠海運集運與東方海外", "COSCO group fleet ~3.63m TEU, world No.4 (10.6%), incl. COSCO Shipping Lines and OOCL"],
 "ir": "https://hold.coscoshipping.com",
 "next": {"p": "2026Q3", "date": "2026-10-31", "approx": True, "note": ["A 股第三季報法定期限 10/31，通常 10 月底公布", "A-share Q3 deadline 31 Oct; usually end-October"]},
 "periods": [
  {"p": "2026Q2", "date": "2026-08-28", "title": ["2026 半年報（含第二季）", "2026 interim results (incl. Q2)"],
   "kpis": [K("Q2 營收", "Q2 revenue", "601.2 億元", "CNY60.1bn", 17.6),
            K("Q2 歸母淨利", "Q2 net profit to owners", "75.4 億元", "CNY7.5bn", 29.1),
            K("上半年營收", "H1 revenue", "1,119.2 億元", "CNY111.9bn", 2.6),
            K("上半年歸母淨利", "H1 net profit to owners", "134.2 億元", "CNY13.4bn", -23.5),
            K("上半年貨量", "H1 volume", "1,428 萬 TEU", "14.28m TEU", 8)],
   "hl": L(["第二季明顯好轉：單季營收年增 17.6%、淨利年增 29.1%，扭轉第一季頹勢。", "A clear Q2 turnaround: revenue +17.6% and net profit +29.1% YoY after a weak Q1."],
           ["上半年貨量 +8%，但單箱營業利潤由 197 降至 139 美元，營業利益率 12.5%（去年同期 17.9%）。", "H1 volume +8%, but operating profit per TEU fell from US$197 to US$139; margin 12.5% vs 17.9%."],
           ["中期股息每股 0.43 元（約 65.7 億元）；新訂 12 艘 22,000 TEU LNG 雙燃料船及 6 艘 3,200 TEU 船。", "Interim dividend CNY0.43/share (~CNY6.57bn); ordered 12×22,000 TEU LNG dual-fuel and 6×3,200 TEU ships."]),
   "gd": L(["預估全球貨櫃運輸需求成長約 2.5%–3.0%，運價「前低後高」；將優化航線與運力配置。", "Expects global container demand +2.5–3.0% with rates 'low first, higher later'; will optimise network and capacity."]),
   "src": [S("東方財富／財中社（2026/08/28）", "https://finance.eastmoney.com/a/202608283858728249.html"), S("Container News（2026/09/06）", "https://container-news.com/cosco-shipping-holdings-profit-falls-34-in-first-half-of-2026/"), S("FilingReader（股利與新船）", "https://filingreader.com/news-wire/shanghai/2026-08-29/cosco-shipping-posts-h1-profit-and-orders-new-vessels")]},
  {"p": "2026Q1", "date": "2026-04", "title": ["第一季", "Q1"],
   "kpis": [K("Q1 營收", "Q1 revenue", "約 518.0 億元", "~CNY51.8bn", None, None, "上半年減第二季推算", "H1 minus Q2", True),
            K("Q1 歸母淨利", "Q1 net profit to owners", "約 58.8 億元", "~CNY5.9bn", None, None, "上半年減第二季推算", "H1 minus Q2", True)],
   "hl": L(["第一季運價低迷，淨利僅約為第二季的八成；上半年淨利年減 23.5% 主要來自第一季。", "Weak Q1 rates; Q1 profit was ~80% of Q2's, and most of H1's 23.5% decline came from Q1."]),
   "gd": L(["詳見半年報展望。", "See interim outlook."]),
   "src": [S("東方財富／財中社（2026/08/28）", "https://finance.eastmoney.com/a/202608283858728249.html")]}
 ]})

companies.append({
 "id": "one", "zh": "海洋網聯（ONE）", "en": "Ocean Network Express", "cc": "JP", "ticker": None, "ccy": ["美元", "USD"],
 "fleet": ["日本郵船、商船三井、川崎汽船合資；船隊約 216 萬 TEU，全球第 6（市占 6.3%）。會計年度 4 月起算", "JV of NYK, MOL and K Line; ~2.16m TEU, world No.6 (6.3%). Fiscal year starts in April"],
 "ir": "https://www.one-line.com",
 "next": {"p": "2026Q3", "date": "2026-11", "approx": True, "note": ["FY2026 第二季（7–9 月），預計 10 月底～11 月初", "FY2026 Q2 (Jul–Sep), expected late Oct–early Nov"]},
 "periods": [
  {"p": "2026Q2", "date": "2026-07-31", "gdir": "up", "title": ["FY2026 第一季（2026 年 4–6 月）", "FY2026 Q1 (Apr–Jun 2026)"],
   "kpis": [K("營收", "Revenue", "45.4 億美元", "US$4.54bn", 12.1),
            K("EBITDA", "EBITDA", "7.07 億美元", "US$707m", 14.8),
            K("EBIT", "EBIT", "0.76 億美元", "US$76m", 100),
            K("淨利", "Net profit", "0.31 億美元", "US$31m", -64),
            K("裝載量", "Liftings", "326 萬 TEU", "3.26m TEU", 2.9)],
   "hl": L(["跨太平洋需求強勁，吸收了中東衝突帶來的成本上升，本業維持獲利。", "Strong transpacific demand absorbed the cost surge from the Middle East conflict, keeping operations profitable."],
           ["淨利年減主因去年同期基期較高與非營業項目；EBIT 已較去年同期倍增。", "Net profit fell YoY on a higher base and non-operating items, while EBIT doubled."]),
   "gd": L(["全年預測大幅上修：營收 194 億（原 185 億）、EBITDA 36 億（原 30 億）、EBIT 11 億（原 5 億）、淨利 9 億美元（原 3 億）。", "FY forecast raised: revenue US$19.4bn (was 18.5), EBITDA US$3.6bn (3.0), EBIT US$1.1bn (0.5), net US$900m (300m)."],
           ["預估上半年度淨利 7.5 億、下半年度 1.5 億美元：假設荷姆茲海峽 10 月恢復衝突前水準，船隻繼續繞行好望角。", "Expects H1 net US$750m and H2 US$150m, assuming Hormuz normalises in October and Cape routing continues."]),
   "src": [S("Container News（2026/08/04）", "https://container-news.com/one-announces-q1-fy2026-financial-results/"), S("FreightWaves：航商上修獲利預測", "https://www.freightwaves.com/news/strong-finish-ocean-lines-raise-profit-outlook-by-200")]}
 ]})

companies.append({
 "id": "hmm", "zh": "現代商船（HMM）", "en": "HMM", "cc": "KR", "ticker": "011200.KS", "ccy": ["韓元", "KRW"],
 "fleet": ["船隊約 103 萬 TEU，全球第 8（市占 3.0%）", "Fleet ~1.03m TEU, world No.8 (3.0%)"],
 "ir": "https://www.hmm21.com",
 "next": {"p": "2026Q3", "date": "2026-11", "approx": True, "note": ["預計 11 月中公布", "Expected mid-November"]},
 "periods": [
  {"p": "2026Q2", "date": "2026-08-13", "title": ["第二季財報", "Q2 results"],
   "kpis": [K("營收", "Revenue", "3.40 兆韓元", "KRW3.40tn", 30),
            K("營業利益", "Operating profit", "3,541 億韓元", "KRW354bn", 52),
            K("淨利", "Net profit", "4,110 億韓元", "KRW411bn"),
            K("上半年營業利益", "H1 operating profit", "6,232 億韓元", "KRW623bn", -26, None, "上半年營益率 10.2%；淨利 7,650 億、年減 37%", "H1 margin 10.2%; net KRW765bn, −37%")],
   "hl": L(["營收年增 30%、營業利益年增 52%，運價回升帶動；上半年 SCFI 平均 1,957 點，較去年同期高 15%。", "Revenue +30% and operating profit +52% on higher rates; SCFI averaged 1,957 in H1, 15% above a year earlier."],
           ["推動「軸輻式（Hub & Spoke）」航網，開發東南亞新貨源。", "Pursuing a hub-and-spoke network and new Southeast Asian demand."]),
   "gd": L(["預期第三季不確定性仍高：美國關稅、巴拿馬運河與主要港口壅塞、中東戰事。", "Expects high Q3 uncertainty: US tariffs, Panama Canal and port congestion, Middle East war."],
           ["過去 15 個月已投資 10 兆韓元，2030 中長期策略投資目標擴大至約 29 兆韓元；因應高油價優化燃油成本。", "Invested KRW10tn over 15 months; 2030 investment target raised to ~KRW29tn; optimising fuel costs."]),
   "src": [S("Herald Business（2026/08/13）", "https://biz.heraldcorp.com/article/10840595"), S("Container News（2026/08/13）", "https://container-news.com/hmm-maintains-profitability-in-h1-2026-despite-volatile-shipping-market/")]},
  {"p": "2026Q1", "date": "2026-05", "title": ["第一季", "Q1"],
   "kpis": [K("營收", "Revenue", "約 2.72 兆韓元", "~KRW2.72tn", None, None, "上半年減第二季推算", "H1 minus Q2", True),
            K("營業利益", "Operating profit", "約 2,691 億韓元", "~KRW269bn", None, None, "上半年減第二季推算", "H1 minus Q2", True),
            K("淨利", "Net profit", "約 3,540 億韓元", "~KRW354bn", None, None, "上半年減第二季推算", "H1 minus Q2", True)],
   "hl": L(["第一季運價偏低，營業利益明顯低於去年同期；上半年營業利益年減 26% 主要來自第一季。", "Low Q1 rates cut operating profit; most of H1's 26% decline came from Q1."]),
   "gd": L(["詳見第二季展望。", "See Q2 outlook."]),
   "src": [S("Container News（2026/08/13）", "https://container-news.com/hmm-maintains-profitability-in-h1-2026-despite-volatile-shipping-market/")]}
 ]})

companies.append({
 "id": "zim", "zh": "以星航運（ZIM）", "en": "ZIM", "cc": "IL", "ticker": "ZIM (NYSE)", "ccy": ["美元", "USD"],
 "fleet": ["船隊約 70 萬 TEU，全球第 10（市占 2.1%）；跨太平洋占比高，即將被赫伯羅特收購", "Fleet ~700k TEU, world No.10 (2.1%); transpacific-heavy; being acquired by Hapag-Lloyd"],
 "ir": "https://investors.zim.com",
 "next": {"p": "2026Q3", "date": "2026-11", "approx": True, "note": ["預計 11 月中；因併購案不舉行法說電話會議", "Expected mid-Nov; no call due to the pending merger"]},
 "periods": [
  {"p": "2026Q2", "date": "2026-08-19", "gdir": "set", "title": ["第二季財報", "Q2 results"],
   "kpis": [K("營收", "Revenue", "17.8 億美元", "US$1.78bn", 9),
            K("淨利", "Net income", "0.64 億美元", "US$64m", 170, None, "去年同期 0.24 億", "Q2 2025: US$24m"),
            K("調整後 EBITDA", "Adj. EBITDA", "4.91 億美元", "US$491m", 4),
            K("平均運價", "Avg freight rate", "1,590 美元/TEU", "US$1,590/TEU", 8),
            K("貨量", "Volume", "92.2 萬 TEU", "922k TEU", 3)],
   "hl": L(["受惠跨太平洋航線的領先地位與靈活的商業策略，第二季轉為獲利；上半年仍淨虧損 0.22 億美元。", "Its transpacific position and agile commercial approach returned Q2 to profit; H1 remained a US$22m net loss."]),
   "gd": L(["全年調整後 EBITDA 20–24 億美元、調整後 EBIT 7–11 億美元。", "FY adjusted EBITDA US$2.0–2.4bn; adjusted EBIT US$0.7–1.1bn."],
           ["董事會可能依第三季結果考慮配息；赫伯羅特以每股 35 美元現金收購，目標第四季完成。", "Board may consider a dividend on Q3 results; Hapag-Lloyd's US$35/share cash takeover targeted to close in Q4."]),
   "src": [S("ZIM Q2 2026 新聞稿", "https://s203.q4cdn.com/172866090/files/doc_financials/2026/q2/ZIM-Q2-2026-PR-Eng-19-8-2026-FINAL-new-template.pdf")]},
  {"p": "2026Q1", "date": "2026-05", "title": ["第一季", "Q1"],
   "kpis": [K("營收", "Revenue", "約 13.96 億美元", "~US$1.40bn", None, None, "上半年減第二季推算", "H1 minus Q2", True),
            K("淨利", "Net income", "約 −0.86 億美元", "~−US$86m", None, None, "上半年減第二季推算", "H1 minus Q2", True),
            K("調整後 EBITDA", "Adj. EBITDA", "約 3.13 億美元", "~US$313m", None, None, "上半年減第二季推算", "H1 minus Q2", True)],
   "hl": L(["運價與貨量下滑，第一季虧損；上半年營收 31.77 億美元（去年同期 36.42 億）。", "Lower rates and volumes led to a Q1 loss; H1 revenue US$3.18bn vs US$3.64bn."]),
   "gd": L(["詳見第二季展望。", "See Q2 outlook."]),
   "src": [S("ZIM Q2 2026 新聞稿", "https://s203.q4cdn.com/172866090/files/doc_financials/2026/q2/ZIM-Q2-2026-PR-Eng-19-8-2026-FINAL-new-template.pdf")]}
 ]})

out = {"updated": "2026-10-16",
       "note": ["數字取自公司公告或所列新聞報導；標「推算」者為依公布的累計數相減而得。台灣公司為新台幣，其他依各公司報告幣別。", "Figures are from company releases or the cited press reports; items marked 'derived' are arithmetic from reported totals. Each company in its reporting currency."],
       "groups": [["台灣貨櫃三雄", "Taiwan's big three", ["evergreen", "yangming", "wanhai"]], ["歐洲大型航商", "European majors", ["maersk", "msc", "cmacgm", "hapag"]], ["亞洲與其他", "Asia & others", ["cosco", "one", "hmm", "zim"]]],
       "companies": companies}
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("companies", len(companies), "periods", sum(len(c["periods"]) for c in companies))
