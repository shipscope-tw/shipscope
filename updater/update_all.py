# -*- coding: utf-8 -*-
"""
樹說航情 Cathay ShipScope — HTML 版更新程式
------------------------------------------------
用法：
    python update_all.py            # 完整更新（新聞、股價、指標、荷姆茲、美國港口、航商市佔）
    python update_all.py --quick    # 只更新新聞與股價（較快，約 1–3 分鐘）
    python update_all.py --offline  # 不抓資料，只用 data/ 現有資料重新產生 HTML

產出：與 updater 資料夾同層的「樹說航情_ShipScope.html」（可放到內網或共用磁碟）。
只需要 Python 3.8 以上，不需要安裝任何套件。
若行內需經 proxy 上網，請先設定環境變數 HTTPS_PROXY / HTTP_PROXY（見 README）。
任何一項抓取失敗時，會保留上一次成功的資料，網頁仍會正常產生。
"""
import base64, datetime, glob, json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
WORK = os.path.join(HERE, "work")
FETCH = os.path.join(HERE, "fetchers")
OUT = os.environ.get("SHIPSCOPE_OUT") or os.path.join(os.path.dirname(HERE), "樹說航情_ShipScope.html")
LOG = os.path.join(HERE, "update_log.txt")

REGIONS = {"台灣": "tw", "亞洲": "asia", "中東": "me", "歐洲": "eu", "非洲": "af", "美洲": "am", "全球": "global"}
JOBS_FULL = [
    ("news", ["fetch_news.py", "news.json", "10"], 900),
    ("stocks", ["fetch_stocks.py", "stocks.json"], 600),
    ("indicators", ["fetch_indicators.py", "indicators.json"], 600),
    ("chokepoints", ["fetch_portwatch.py", "chokepoints.json", "500"], 900),
    ("usports", ["fetch_usports.py", "usports.json"], 900),
    ("carriers", ["fetch_carriers.py", "carriers.json"], 300),
    ("ports", ["fetch_ports.py", "ports.json"], 900),
    ("trade", ["fetch_trade.py", "trade.json", os.path.join(DATA, "feeds", "trade.json")], 900),
    ("portwait", ["fetch_portwait.py", "portwait.json", os.path.join(DATA, "feeds", "portwait.json")], 300),
]
JOBS_QUICK = [j for j in JOBS_FULL if j[0] in ("news", "stocks")]


def now_utc():
    return datetime.datetime.now(datetime.timezone.utc)


def log(msg):
    line = "[%s] %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg)
    print(line, flush=True)
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def rj(path, default=None):
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        # 相容從 Claude 版匯出的 {"data": {...}} 格式
        if isinstance(d, dict) and set(d.keys()) >= {"data"} and isinstance(d["data"], dict) and len(d) <= 3:
            return d["data"]
        return d
    except Exception:
        return default


def wj(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))
    os.replace(tmp, path)


def run_fetchers(jobs):
    os.makedirs(WORK, exist_ok=True)
    ok = {}
    for name, args, timeout in jobs:
        out = os.path.join(WORK, args[1])
        if os.path.exists(out):
            os.remove(out)
        cmd = [sys.executable, os.path.join(FETCH, args[0]), out] + args[2:]
        log("抓取 %s ..." % name)
        try:
            env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")  # Windows 預設 cp950，強制 UTF-8
            r = subprocess.run(cmd, cwd=WORK, timeout=timeout, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
            d = rj(out)
            good = r.returncode == 0 and d is not None and (not isinstance(d, dict) or d.get("items") or d.get("cps") or d.get("carriers") or d.get("ports") or len(d) > 2)
            if good:
                ok[name] = d
                log("  %s 完成" % name)
            else:
                log("  %s 失敗，沿用上一版資料。%s" % (name, (r.stderr or r.stdout or "")[-400:].strip()))
        except subprocess.TimeoutExpired:
            log("  %s 逾時，沿用上一版資料" % name)
        except Exception as e:
            log("  %s 錯誤：%s，沿用上一版資料" % (name, e))
    return ok


def save_news(news):
    by = {k: [] for k in REGIONS.values()}
    for it in news.get("items", []):
        rk = REGIONS.get(it.get("region"), "global")
        x = {k: it.get(k) for k in ("id", "source", "title", "summary", "url", "published", "lang", "sectors", "topics")}
        x["summary"] = (x.get("summary") or "")[:240]
        by[rk].append(x)
    for rk, items in by.items():
        items = sorted(items, key=lambda x: x.get("published") or "", reverse=True)[:120]
        if not items:  # 該地區這次沒抓到，保留舊資料
            continue
        wj(os.path.join(DATA, "news", rk + ".json"), {"region": rk, "updated": news.get("fetched"), "items": items})


def merge_indicators(cur):
    prev = rj(os.path.join(DATA, "feeds", "indicators.json"), {}) or {}
    pmap = {i["id"]: i for i in prev.get("items", [])}
    seen = set()
    for it in cur.get("items", []):
        seen.add(it["id"])
        old = pmap.get(it["id"], {}).get("series", []) or []
        ser = {d: v for d, v in old}
        ser.update({d: v for d, v in (it.get("series") or [])})
        if it.get("date") and it.get("value") is not None:
            ser[it["date"]] = it["value"]
        it["series"] = [[d, ser[d]] for d in sorted(ser)][-260:]
    # 這次沒抓到的指標保留舊值
    for k, v in pmap.items():
        if k not in seen:
            cur.setdefault("items", []).append(v)
    return cur


# ---------------- 規則式「今日重點摘要」（HTML 版不使用 AI） ----------------
def _ind(I, k):
    for it in (I or {}).get("items", []):
        if it.get("id") == k:
            return it
    return None


def _num(v):
    try:
        return float(str(v).replace(",", "").replace("$", ""))
    except Exception:
        return None


def _m1(it):
    """近一個月變動 %（用歷史序列，若無則用 m1_pct 欄位）"""
    if it is None:
        return None
    if it.get("m1_pct") is not None:
        return it["m1_pct"]
    ser = it.get("series") or []
    v = _num(it.get("value"))
    if not ser or v is None:
        return None
    try:
        d0 = datetime.date.fromisoformat(it["date"]) - datetime.timedelta(days=30)
    except Exception:
        return None
    base = None
    for d, x in ser:
        if d <= d0.isoformat():
            base = x
    if not base:
        return None
    return (v / base - 1) * 100


def _md(d):
    try:
        x = datetime.date.fromisoformat(d[:10])
        return "%d/%d" % (x.month, x.day)
    except Exception:
        return d or ""


def _fmt(v, nd=0):
    v = _num(v)
    if v is None:
        return "—"
    return ("{:,.%df}" % nd).format(v)


def _dir(chg, zh=True):
    if chg is None:
        return ""
    if abs(chg) < 1e-9:
        return "持平" if zh else "flat"
    return ("上漲" if chg > 0 else "下跌") if zh else ("up" if chg > 0 else "down")


def build_brief(I, C):
    B = []
    # 1 荷姆茲
    try:
        h = C["cps"]["hormuz"]
        t = [x for x in h["total"] if x is not None]
        avg7 = sum(t[-7:]) / len(t[-7:])
        base = h.get("base_total") or 0
        pct = (avg7 / base - 1) * 100 if base else 0
        lvl = "嚴重受阻" if base and avg7 / base < 0.4 else ("明顯低於常態" if base and avg7 / base < 0.8 else "接近常態")
        lvl_en = "severely disrupted" if base and avg7 / base < 0.4 else ("well below normal" if base and avg7 / base < 0.8 else "near normal")
        B.append({
            "text": "荷姆茲：AIS 統計 7 日平均 %.1f 艘/日，較戰前 %.0f 艘 %+.0f%%（資料至 %s），通行%s；油輪與 LNG/LPG 運價的地緣溢價須持續觀察。" % (avg7, base, pct, _md(C.get("last_date")), lvl),
            "text_en": "Hormuz: AIS 7-day average of %.1f transits/day, %+.0f%% vs the pre-war %.0f (data to %s); traffic is %s. Keep watching the geopolitical premium in tanker and LNG/LPG rates." % (avg7, pct, base, _md(C.get("last_date")), lvl_en),
            "url": C.get("source_url") or "https://portwatch.imf.org/"})
    except Exception:
        pass
    # 2 貨櫃
    s, w = _ind(I, "scfi"), _ind(I, "wci")
    if s:
        chg = _num(s.get("chg"))
        txt = "貨櫃：SCFI %s 點（%s），%s %s 點" % (_fmt(s["value"], 0), _md(s.get("date")), _dir(chg), _fmt(abs(chg) if chg is not None else None, 1))
        en = "Containers: SCFI at %s (%s), %s %s" % (_fmt(s["value"], 0), _md(s.get("date")), _dir(chg, False), _fmt(abs(chg) if chg is not None else None, 1))
        if w:
            txt += "；Drewry WCI US$%s/FEU（%s）" % (_fmt(w["value"]), _md(w.get("date")))
            en += "; Drewry WCI US$%s/FEU (%s)" % (_fmt(w["value"]), _md(w.get("date")))
        B.append({"text": txt + "。", "text_en": en + ".", "url": s.get("source_url")})
    # 3 散裝
    b = _ind(I, "bdi")
    if b:
        chg, m1 = _num(b.get("chg")), _m1(b)
        cape = _ind(I, "cape")
        txt = "散裝：BDI %s 點（%s），日變動 %s" % (_fmt(b["value"]), _md(b.get("date")), ("%+d" % chg) if chg is not None else "—")
        en = "Dry bulk: BDI at %s (%s), daily change %s" % (_fmt(b["value"]), _md(b.get("date")), ("%+d" % chg) if chg is not None else "—")
        if m1 is not None:
            txt += "、近一月 %+.0f%%" % m1
            en += ", %+.0f%% over the past month" % m1
        if cape:
            txt += "；海岬型 5TC US$%s/日" % _fmt(cape["value"])
            en += "; Capesize 5TC US$%s/day" % _fmt(cape["value"])
        B.append({"text": txt + "。", "text_en": en + ".", "url": b.get("source_url")})
    # 4 能源
    br, ttf = _ind(I, "brent"), _ind(I, "ttf")
    if br:
        txt = "能源：Brent US$%s/桶（%s）" % (_fmt(br["value"], 2), _md(br.get("date")))
        en = "Energy: Brent at US$%s/bbl (%s)" % (_fmt(br["value"], 2), _md(br.get("date")))
        if br.get("y1_pct") is not None:
            txt += "，年增 %+.0f%%" % br["y1_pct"]
            en += ", %+.0f%% y/y" % br["y1_pct"]
        if ttf:
            txt += "；歐洲 TTF 天然氣 €%s/MWh" % _fmt(ttf["value"], 2)
            en += "; European TTF gas at €%s/MWh" % _fmt(ttf["value"], 2)
        B.append({"text": txt + "；油價與氣價水準影響油輪、LNG 船需求與船東燃油成本。", "text_en": en + "; oil and gas prices drive tanker and LNG carrier demand and owners' fuel costs.", "url": br.get("source_url")})
    # 5 燃油成本
    v = _ind(I, "vlsfo")
    if v:
        chg = _num(v.get("chg"))
        B.append({
            "text": "成本：新加坡 VLSFO US$%s/公噸（%s），%s；燃油約占航次成本四到六成，留意航商轉嫁（BAF）能力。" % (_fmt(v["value"]), _md(v.get("date")), (("較前日 %+.1f" % chg) if chg is not None else "")),
            "text_en": "Costs: Singapore VLSFO at US$%s/t (%s)%s; bunkers are roughly 40-60%% of voyage costs, so watch carriers' ability to pass them on via BAF." % (_fmt(v["value"]), _md(v.get("date")), ((", %+.1f d/d" % chg) if chg is not None else "")),
            "url": v.get("source_url")})
    tw = now_utc() + datetime.timedelta(hours=8)
    return {"date": tw.date().isoformat(), "generated": now_utc().strftime("%Y-%m-%dT%H:%M:%SZ"), "auto": True, "bullets": B[:5]}


# ---------------- 產生 HTML ----------------
def build_html():
    feeds = {}
    for p in glob.glob(os.path.join(DATA, "feeds", "*.json")):
        d = rj(p)
        if d is not None:
            feeds[os.path.splitext(os.path.basename(p))[0]] = d
    news = {}
    for p in glob.glob(os.path.join(DATA, "news", "*.json")):
        d = rj(p)
        if d is not None:
            news[os.path.splitext(os.path.basename(p))[0]] = d
    research = {}
    for p in sorted(glob.glob(os.path.join(DATA, "research", "*.json"))):
        d = rj(p)
        if isinstance(d, dict):
            d.pop("file_id", None)
            research[os.path.splitext(os.path.basename(p))[0]] = d
    settings = {}
    logo = None
    for ext, mime in (("png", "image/png"), ("jpg", "image/jpeg"), ("jpeg", "image/jpeg"), ("svg", "image/svg+xml"), ("webp", "image/webp")):
        lp = os.path.join(DATA, "brand", "logo." + ext)
        if os.path.exists(lp):
            with open(lp, "rb") as f:
                logo = "data:%s;base64,%s" % (mime, base64.b64encode(f.read()).decode())
            break
    if logo:
        settings["brand"] = {"logo_src": logo}
    snap = {"feeds": feeds, "news": news, "research": research, "settings": settings}
    js = json.dumps(snap, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029").replace("\ufffd", "")
    with open(os.path.join(HERE, "template.html"), encoding="utf-8") as f:
        tpl = f.read()
    mark = "/*__SNAPSHOT__*/null"
    if mark not in tpl:
        raise SystemExit("template.html 缺少 SNAPSHOT 標記")
    html = tpl.replace(mark, js, 1)
    tmp = OUT + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(html)
    os.replace(tmp, OUT)
    log("已產生 %s（%.1f MB）" % (OUT, os.path.getsize(OUT) / 1e6))


def main():
    try:
        sys.stdout.reconfigure(errors="replace")
    except Exception:
        pass
    args = set(sys.argv[1:])
    os.makedirs(os.path.join(DATA, "feeds"), exist_ok=True)
    os.makedirs(os.path.join(DATA, "news"), exist_ok=True)
    os.makedirs(os.path.join(DATA, "research"), exist_ok=True)
    if "--offline" not in args:
        jobs = JOBS_QUICK if "--quick" in args else JOBS_FULL
        got = run_fetchers(jobs)
        stamp = now_utc().strftime("%Y-%m-%dT%H:%M:%SZ")
        meta = rj(os.path.join(DATA, "feeds", "meta.json"), {}) or {}
        if "news" in got:
            save_news(got["news"])
            meta.update({"news_updated": stamp, "news_days": got["news"].get("days", 10), "news_count": len(got["news"].get("items", []))})
        if "indicators" in got:
            wj(os.path.join(DATA, "feeds", "indicators.json"), merge_indicators(got["indicators"]))
        for k in ("stocks", "chokepoints", "usports", "carriers", "ports", "trade", "portwait"):
            if k in got:
                wj(os.path.join(DATA, "feeds", k + ".json"), got[k])
        if "--quick" not in args:
            meta["updated"] = stamp
        meta["standalone"] = True
        wj(os.path.join(DATA, "feeds", "meta.json"), meta)
        if "--quick" not in args or "indicators" in got:
            I = rj(os.path.join(DATA, "feeds", "indicators.json"), {})
            C = rj(os.path.join(DATA, "feeds", "chokepoints.json"), {})
            br = build_brief(I, C)
            if br["bullets"]:
                wj(os.path.join(DATA, "feeds", "brief.json"), br)
        if "--quick" not in args:
            hp = os.path.join(DATA, "feeds", "hist.json"); tmp = os.path.join(WORK, "hist_new.json")
            os.makedirs(WORK, exist_ok=True)
            env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
            log("抓取 hist（走勢圖歷史）...")
            try:
                r = subprocess.run([sys.executable, os.path.join(FETCH, "fetch_hist.py"), tmp, hp, os.path.join(DATA, "feeds", "indicators.json")], cwd=WORK, timeout=1800, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
                if r.returncode == 0 and rj(tmp):
                    os.replace(tmp, hp); log("  hist 完成 " + (r.stderr or "").strip().splitlines()[-1][:200] if (r.stderr or "").strip() else "  hist 完成")
                else:
                    log("  hist 失敗，沿用上一版資料。" + (r.stderr or "")[-300:])
            except Exception as e:
                log("  hist 錯誤：%s，沿用上一版資料" % e)
        shutil.rmtree(WORK, ignore_errors=True)
    build_html()


if __name__ == "__main__":
    main()
