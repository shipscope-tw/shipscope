"""Fleet supply vs seaborne demand (annual) -> supply.json

UNCTADstat bulk downloads (free, 7z-compressed CSV):
  US.MerchantFleet       world fleet by ship type, dwt / number / average age, as of 1 January each year
  US.SeaborneTrade       world seaborne trade loaded by cargo type, metric tons
  US.ContPortThroughput  world container port throughput, TEU
  US.ShipBuilding        world ship deliveries, gross tonnage
  US.ShipScrapping       world ship demolition, gross tonnage
LNG (not split out by UNCTAD) comes from the IGU World LNG Report, entered by hand below; update it each year when IGU
publishes a new report (usually May/June).

Needs the `7z` command (preinstalled on GitHub's Ubuntu runners) or the py7zr package to unpack the downloads.
"""
import csv, io, json, os, shutil, subprocess, sys, tempfile, time, urllib.request

UA = {"User-Agent": "ShipScope/1.0 (+https://shipscope-tw.github.io/shipscope/)"}
API = "https://unctadstat-api.unctad.org/bulkdownload/{r}/{f}"
REPORTS = ["US.MerchantFleet", "US.SeaborneTrade", "US.ContPortThroughput", "US.ShipBuilding", "US.ShipScrapping"]

# IGU World LNG Report: global trade (million tonnes), active carrier fleet at year end (incl. FSRU/FSU), deliveries in the year
LNG = {
    "trade": [[2023, 401.42], [2024, 411.24], [2025, 436.98]],
    "fleet": [[2024, 742], [2025, 804]],
    "deliveries": [[2024, 64], [2025, 79]],
    "src": [
        {"t": "IGU World LNG Report 2025", "u": "https://igu.org/press-releases/2025-world-lng-report-press-release"},
        {"t": "IGU World LNG Report 2026（IIR 摘要）", "u": "https://iifiir.org/en/news/world-lng-report-2026-north-american-exports-drive-record-growth-for-global-lng-trade"},
    ],
    "note": ["2023 年貿易量取自 2025 年報表 3.2 出口合計；船隊含浮式儲存再氣化船（FSRU）與浮式儲存船（FSU）。",
             "2023 trade is the export total in Table 3.2 of the 2025 report; the fleet includes FSRUs and FSUs."],
}


def download(rep):
    url = API.format(r=rep, f=rep.replace(".", "_"))
    for i in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()
        except Exception as e:
            err = e
            time.sleep(5)
    raise RuntimeError(f"{rep}: {err}")


def unpack(blob):
    """Return the CSV text inside a 7z archive."""
    tmp = tempfile.mkdtemp()
    try:
        arc = os.path.join(tmp, "a.7z")
        open(arc, "wb").write(blob)
        exe = shutil.which("7z") or shutil.which("7za") or shutil.which("7zr")
        if exe:
            subprocess.run([exe, "x", "-y", "-o" + tmp, arc], check=True, capture_output=True)
        else:
            import py7zr  # optional fallback
            with py7zr.SevenZipFile(arc) as z:
                z.extractall(tmp)
        name = next(f for f in os.listdir(tmp) if f.lower().endswith(".csv"))
        return open(os.path.join(tmp, name), encoding="utf-8-sig").read()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def world_rows(text):
    return [r for r in csv.DictReader(io.StringIO(text)) if r.get("Economy") == "0000"]


def num(s, scale=1.0, nd=1):
    try:
        return round(float(s) * scale, nd)
    except (TypeError, ValueError):
        return None


def main(out):
    raw = {}
    for rep in REPORTS:
        raw[rep] = world_rows(unpack(download(rep)))

    # fleet by ship type (dwt thousands -> million dwt)
    TYPES = {"0": "total", "1": "tanker", "2": "bulk", "3": "general", "4": "container", "5": "other"}
    rows = raw["US.MerchantFleet"]
    years = sorted({int(r["Year"]) for r in rows})
    fleet = {"years": years}
    for code, key in TYPES.items():
        by = {int(r["Year"]): r for r in rows if r["ShipType"] == code}
        fleet[key] = {
            "dwt": [num(by[y]["Dead weight tons in thousands"], 1e-3) if y in by else None for y in years],
            "n": [num(by[y]["Number of ships"], 1, 0) if y in by else None for y in years],
            "age": [num(by[y].get("Average age of vessels (years)"), 1, 1) if y in by else None for y in years],
        }

    # seaborne trade, goods loaded (thousand t -> million t)
    rows = raw["US.SeaborneTrade"]
    CARGO = {"10": "total", "11": "crude", "12": "other_tanker", "13": "dry"}
    ty = sorted({int(r["Year"]) for r in rows if r["CargoType"] in CARGO})
    trade = {"years": ty}
    for code, key in CARGO.items():
        by = {int(r["Year"]): r for r in rows if r["CargoType"] == code}
        trade[key] = [num(by[y]["Metric tons in thousands"], 1e-3) if y in by else None for y in ty]

    # container port throughput (TEU -> million TEU)
    rows = raw["US.ContPortThroughput"]
    col = next(k for k in rows[0] if k.startswith("TEU") and "Footnote" not in k and "Missing" not in k)
    teu = {"years": [int(r["Year"]) for r in rows], "v": [num(r[col], 1e-6) for r in rows]}

    def gt(rep):
        rs = sorted(raw[rep], key=lambda r: int(r["Year"]))
        return {"years": [int(r["Year"]) for r in rs], "v": [num(r["Gross Tonnage"], 1e-6) for r in rs]}

    d = {
        "source": "UNCTADstat（聯合國貿易和發展會議）；LNG：IGU World LNG Report",
        "source_url": "https://unctadstat.unctad.org/datacentre/",
        "fetched": time.strftime("%Y-%m-%d"),
        "fleet": fleet,
        "trade": trade,
        "teu": teu,
        "build": gt("US.ShipBuilding"),
        "scrap": gt("US.ShipScrapping"),
        "lng": LNG,
        "notes": {
            "fleet": ["船隊為每年 1 月 1 日的載重噸（DWT），100 總噸以上商船。",
                      "Fleet is deadweight tonnage on 1 January each year, merchant ships of 100 GT and above."],
            "trade": ["海運貿易量為各國裝貨量合計；「乾貨」包含鐵礦砂、煤、穀物等主要散貨，也包含貨櫃與其他雜貨。",
                      "Seaborne trade is goods loaded; 'dry cargo' covers the main bulks (iron ore, coal, grain) as well as containerised and other general cargo."],
        },
    }
    if len(fleet["years"]) < 10 or not trade["years"] or not teu["years"]:
        raise SystemExit("UNCTAD data looks incomplete")
    json.dump(d, open(out, "w", encoding="utf-8"), ensure_ascii=False)
    print("fleet", years[0], "-", years[-1], "trade", ty[0], "-", ty[-1], "teu", teu["years"][-1])


if __name__ == "__main__":
    main(sys.argv[1])
