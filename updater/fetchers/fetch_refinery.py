"""US refinery utilisation and distillate (diesel) balance, weekly -> refinery.json

Source: US Energy Information Administration (EIA), Weekly Petroleum Status Report, published every Wednesday
(data for the week ending the previous Friday). Free and official; the same figures that Bloomberg/Reuters report.
Series (EIA codes):
  WPULEUS3  refinery utilisation, % of operable capacity
  WGIRIUS2  refinery gross input, thousand barrels/day
  WDISTUS1  distillate fuel oil stocks, thousand barrels
  WDIEXUS2  distillate fuel oil exports, thousand barrels/day
"""
import json, re, sys, time, urllib.request, datetime

UA = {"User-Agent": "Mozilla/5.0 (ShipScope research dashboard)"}
URL = "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s={s}&f=W"
SERIES = {"util": "WPULEUS3", "inputs": "WGIRIUS2", "dist_stock": "WDISTUS1", "dist_exp": "WDIEXUS2"}
MON = {m: i for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}


def get(url):
    for i in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read().decode("utf-8", "ignore")
        except Exception as e:
            err = e
            time.sleep(5)
    raise RuntimeError(f"{url}: {err}")


def parse(html):
    out = []
    for row in re.findall(r"<tr>(.*?)</tr>", html, re.S):
        m = re.search(r"class='B6'>[\s&nbsp;]*(\d{4})-([A-Za-z]{3})", row)
        if not m:
            continue
        y, rm = int(m.group(1)), MON.get(m.group(2))
        cells = re.findall(r"class='B5'>([\d/]*)&nbsp;</td>\s*<td class='B3'>([^<]*)</td>", row)
        for md, v in cells:
            v = v.replace("&nbsp;", "").replace(",", "").strip()
            if not md or not re.match(r"^-?[\d.]+$", v):
                continue
            mm, dd = int(md[:2]), int(md[3:5])
            yy = y + 1 if (rm == 12 and mm == 1) else (y - 1 if (rm == 1 and mm == 12) else y)
            out.append([f"{yy}-{mm:02d}-{dd:02d}", float(v)])
    out.sort()
    return out


def five_year(series, date):
    """Average of the same week in the previous five years (±3 days), as EIA does in its weekly report."""
    d = datetime.date.fromisoformat(date)
    vals = []
    for k in range(1, 6):
        t = d.replace(year=d.year - k)
        near = [v for s, v in series if abs((datetime.date.fromisoformat(s) - t).days) <= 3]
        if near:
            vals.append(near[0])
    return round(sum(vals) / len(vals), 1) if len(vals) >= 3 else None


def main(out):
    d = {"source": "U.S. Energy Information Administration（EIA）每週石油報告", "source_url": "https://www.eia.gov/petroleum/supply/weekly/",
         "fetched": time.strftime("%Y-%m-%d"), "series": {}, "latest": {}}
    for k, code in SERIES.items():
        s = parse(get(URL.format(s=code)))
        if len(s) < 100:
            raise SystemExit(f"{code}: only {len(s)} rows")
        cut = (datetime.date.fromisoformat(s[-1][0]) - datetime.timedelta(days=365 * 7)).isoformat()
        s = [r for r in s if r[0] >= cut]
        d["series"][k] = s
        last, prev = s[-1], s[-2]
        yago = [r for r in s if r[0] <= (datetime.date.fromisoformat(last[0]) - datetime.timedelta(days=364)).isoformat()]
        d["latest"][k] = {"date": last[0], "value": last[1], "prev": prev[1], "year_ago": yago[-1][1] if yago else None,
                          "avg5": five_year(s, last[0]), "code": code}
        time.sleep(1)
    json.dump(d, open(out, "w", encoding="utf-8"), ensure_ascii=False)
    L = d["latest"]
    print("util", L["util"]["date"], L["util"]["value"], "dist_stock", L["dist_stock"]["value"], "avg5", L["dist_stock"]["avg5"], "exp", L["dist_exp"]["value"])


if __name__ == "__main__":
    main(sys.argv[1])
