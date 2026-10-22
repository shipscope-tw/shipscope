# 樹說航情 ShipScope — 維護說明（給接手的人與 AI 助手）

航運產業研究參考儀表板，網站：https://shipscope-tw.github.io/shipscope/
本檔是交接用的維護手冊。AI 助手（Claude 等）開啟本專案時請先讀完本檔再動手。

## 必守原則

1. **只用免費、公開的資料。** 不放任何需要付費訂閱或授權的報告、資料庫內容；新增來源前先確認對方網頁公開可讀。
2. **每個數字都要能追溯。** 指標資料要帶 `source`（來源名稱）、`source_url`（連結）、`date`（資料日）。不要自行估算或編造數字；推算值要標明「推算」。
3. **保留免責聲明。** `updater/template.html` 中的 `.site-disc` 段落與側欄說明不可刪除：
   「本網站為國泰世華銀行同仁自行整理之航運產業研究參考工具，非本行官方網站，內容不代表本行立場，亦不構成任何投資或授信建議。」
4. **Logo 只用 `updater/data/brand/` 裡的原始檔，** 不要重繪或改色。
5. **網站不收集任何使用者或行內資料，** 不加登入、表單、追蹤碼。
6. **本 repo 必須保持公開。** GitHub Actions 對公開 repo 免費不計分鐘，Pages 也需要公開。因此 repo 裡不能放任何非公開資訊、帳密或金鑰（目前也不需要任何金鑰）。
7. 每日更新只跑固定的 Python 程式，**不呼叫任何 AI API。** 不要加入會產生費用的服務。

## 專案結構

| 路徑 | 內容 |
| --- | --- |
| `index.html` | 對外網站本體（約 3 MB 單一檔），由程式自動產生，**不要手動修改** |
| `updater/update_all.py` | 主程式：依序執行各抓取程式、合併資料、產生 `index.html` |
| `updater/fetchers/fetch_*.py` | 每個資料來源一支抓取程式（見下表） |
| `updater/data/feeds/*.json` | 各類資料的最新結果；抓取失敗時保留上一次成功的版本 |
| `updater/data/feeds/hist.json` | 指標歷史序列（折線圖與下載用） |
| `updater/data/news/*.json` | 新聞，依地區分檔（tw、asia、me、eu、af、am、global） |
| `updater/data/brand/` | Logo 原檔 |
| `updater/template.html` | 網頁版面與前端程式（單一檔，函式庫已內嵌）；資料在建置時注入 `/*__SNAPSHOT__*/null` 標記處 |
| `updater/make_earnings.py`、`make_earnings_lib.py`、`earnings_extend.py`、`earnings_images.json` | 「法說・財報」頁的人工整理資料與產生程式 |
| `.github/workflows/update.yml` | 排程：每天台北 07:45、12:45 自動執行並 commit |

| 抓取程式 | 來源 | 產出 |
| --- | --- | --- |
| `fetch_indicators.py` | 上海航運交易所（SCFI/CCFI/SEAFI）、Drewry WCI、Baltic Exchange 經 HandyBulk（BDI 等）、Ship & Bunker（新加坡燃油）、Trading Economics（原物料） | `indicators.json` |
| `fetch_hist.py` | 上述來源的歷史值、Yahoo Finance 期貨（BZ=F、CL=F、NG=F 等）、FRED（丙烷） | `hist.json` |
| `fetch_portwatch.py` | IMF PortWatch 海峽／運河通行量 | `chokepoints.json` |
| `fetch_ports.py`、`fetch_usports.py` | IMF PortWatch 全球港口、美國港口 | `ports.json`、`usports.json` |
| `fetch_portwait.py` | GoComet 港口等待時間 | `portwait.json` |
| `fetch_trade.py` | IMF IMTS、Trading Economics、UN Comtrade 進出口 | `trade.json` |
| `fetch_carriers.py` | Alphaliner Top 100 公開版 | `carriers.json` |
| `fetch_stocks.py` | Yahoo 股市 | `stocks.json` |
| `fetch_news.py` | 航運媒體 RSS、Bing 新聞 | `data/news/*.json` |
| `fetch_unctad.py` | UNCTADstat 船隊（載重噸、艘數、船齡）、海運貿易量、港口貨櫃吞吐量、造船與拆船；LNG 數字取自 IGU World LNG Report（程式內手動維護，每年 IGU 發布新年報後更新） | `supply.json` |

「今日重點」（`brief.json`）由 `update_all.py` 的 `build_brief()` 依當天數字套模板產生，不是 AI 生成。

## 常用指令

只需要 Python 3.8 以上，不需要安裝任何套件。

```bash
python updater/update_all.py            # 完整更新：抓所有資料並產生網頁
python updater/update_all.py --quick    # 只更新新聞與股價
python updater/update_all.py --offline  # 不抓資料，只用現有資料重新產生網頁（改版面後用這個）
```

在 repo 根目錄執行時，請加 `SHIPSCOPE_OUT=index.html`，讓輸出直接覆蓋網站檔：

```bash
SHIPSCOPE_OUT=index.html python updater/update_all.py --offline
```

執行紀錄寫在 `updater/update_log.txt`（不 commit）。

## Git 注意事項

- 機器人每天會 commit 兩次資料更新，所以**推送前一定先 `git pull --rebase`**。
- 若 rebase 時 `index.html` 衝突：先 `git checkout --theirs index.html`，再跑 `--offline` 重新產生，`git add index.html` 後 `git rebase --continue`。
- 改動 `updater/fetchers/**` 或 `updater/update_all.py` 並推上去後，會自動觸發一次完整更新。

## 常見工作

### 某個指標或區塊不更新了

1. 先對照原始來源：很多時候是來源本身還沒更新。例如 IMF PortWatch 約每週才發布一批，落後 3–7 天，屬正常。
2. 到 GitHub → Actions → 最近一次「Update ShipScope」的執行紀錄，找出失敗的 `fetch_xxx`。
3. 多半是來源網頁改版。只修那一支抓取程式，維持輸出 JSON 的欄位格式不變；可在 `updater/` 下照 `update_all.py` 裡 `JOBS_FULL` 列出的參數單獨執行該程式測試，例如 `python fetchers/fetch_indicators.py test.json`。
4. 推上去後會自動重跑；也可在 Actions 頁按 Run workflow 手動執行。

### 每季更新「法說・財報」

台灣公司約在 2、5、8、11 月中公布財報，國際航商時間各異。

1. 依公司官網的法說簡報、財報新聞稿或公開資訊觀測站，修改 `updater/make_earnings.py` 中各公司的 `periods`（數字照公司公布，推算值設 `d=True`；附上來源連結 `S(標題, 網址)`）。
2. 產生資料並補上圖片與分類：
   ```bash
   python updater/make_earnings.py updater/data/feeds/earnings.json
   python updater/earnings_extend.py updater/data/feeds/earnings.json updater/earnings_images.json
   SHIPSCOPE_OUT=index.html python updater/update_all.py --offline
   ```
3. 開啟 `index.html` 確認「法說・財報」頁顯示正常後 commit、push。

### 每年更新 LNG 船隊與貿易數字

UNCTAD 不單獨統計 LNG 船，`fetch_unctad.py` 開頭的 `LNG` 常數取自 IGU（國際天然氣聯盟）World LNG Report，每年約 5–6 月出新年報後手動補上一年的貿易量、年底船隊艘數與交船數，並更新 `src` 連結。UNCTAD 的資料由程式自動抓取（需要 `7z` 指令，GitHub 的 Ubuntu 主機已內建；本機可改裝 `py7zr`）。

### 每季更新首頁「2027 航運展望」

首頁的展望卡片讀 `updater/data/feeds/outlook.json`（人工整理，不會自動更新）。BIMCO 約每季發布貨櫃、散裝、油輪展望，Clarksons 半年發布業績簡報，WTO 每年 4 月、10 月發布貿易預測；有新版時更新對應的數字、`why` 說明、`src` 連結與 `updated` 日期。

- 只引用機構**公開發布**的內容（新聞稿、公開簡報、媒體報導），不放付費報告的數字。
- `signal` 是本站觀點（由維護者判斷），綜合各機構公開預估：預期運力快於用船需求填 `weak`，需求快於運力填 `strong`，接近填 `neutral`，取決於情境（如荷姆茲）填 `mixed`。卡片上的數字一律引用公開來源並附連結；付費報告只能作為維護者自己判斷的參考，不可把其中的數字或圖表放上網站。
- 貨櫃卡片的 `lanes` 列出各航線觀點（目前為亞歐線、亞洲區間），格式同上。
- 「目前景氣位置」取自 `template.html` 內 `STATIC.sectors` 的 `stage`。
- 各產業頁上方的「2027 展望」卡片也讀同一份 `outlook.json`（`OL_BY_SEC` 決定每頁顯示哪些卡片：油輪頁顯示成品油輪與原油輪），所以首頁與產業頁一定一致；改觀點只要改這個檔案。產業頁下方「展望」段落若與觀點衝突，也要一併改 `STATIC.sectors` 的 `outlook`（油輪的中英文版本在 `template.html` 內以程式覆寫）。
- 進入 2027 年後，把展望年份改成 2028（標題、`rows` 文字與頁面上的「2027」字樣）。

### 專題「烏俄戰爭與歐洲柴油」

內容寫在 `template.html` 的 `RUWAR`（數字、說明）與 `RUWAR_SRC`（來源連結）常數，油輪頁的「柴油」卡片也用同一份資料。柴油裂解價差、各國進口占比等都是整理日當時的公開報導數字，不會自動更新；有重大變化（例如荷姆茲恢復、歐盟新禁令）時更新數字、來源與 `asof` 日期。

### 修改版面

- 直接編輯 `updater/template.html`，改完跑 `--offline` 產生 `index.html` 並在瀏覽器檢查。
- 左側選單：`NAV_GROUPS` 與 `VIEWS`；英文翻譯：`window.I18N` 字典（新增中文字串時一併補英文）。
- 圖片只用開放授權來源（Wikimedia Commons），並在 `GEO_IMG`、`SEC_IMG` 等設定中保留出處資訊。
- 不要移除免責聲明，不要加入追蹤碼或外部表單。

## 已知狀況

- **排程延遲**：GitHub 尖峰時段排程可能晚數十分鐘才執行，屬正常。
- **60 天無活動會停用排程**：GitHub 對公開 repo 的規定。`update.yml` 每次排程執行時會呼叫 API 重新啟用自己（「Keep schedule alive」步驟），正常情況不會被停。若仍被停用：Actions → Update ShipScope → Enable workflow。
- **抓取失敗不會清空資料**：網站會顯示上一次成功的數字與其資料日。
- **IMF PortWatch 與其他 AIS 追蹤網站的艘數口徑不同**，不可混在同一條序列中比較。

## 帳號與交接

- 專案屬於 GitHub 組織 `shipscope-tw`。交接時把接手者加為組織 Owner，組織至少保持兩位管理員。
- 沒有任何外部服務帳號、API 金鑰或付費訂閱需要移交。
