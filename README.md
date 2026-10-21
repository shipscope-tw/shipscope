# 樹說航情 ShipScope

航運產業儀表板：貨櫃、散裝、油輪、LNG／LPG 指標，荷姆茲等 8 大海峽與運河通行量，國際航運新聞與航運股行情。

- 網站：https://shipscope-tw.github.io/shipscope/
- 自動更新：GitHub Actions 每天台北時間 07:45、12:45 執行 `updater/update_all.py`，抓取公開資料後重建 `index.html`。
- 手動更新：到 Actions → Update ShipScope → Run workflow。
- 資料來源：IMF PortWatch、上海航運交易所、Baltic Exchange（經 HandyBulk）、Drewry、Ship & Bunker、Trading Economics、Alphaliner、Yahoo 股市、UNCTADstat、IGU、各媒體 RSS。數值皆標註資料日與來源，僅供參考。
- 維護與交接：見 [CLAUDE.md](CLAUDE.md)（專案結構、常用指令、每季更新法說、來源改版時怎麼修）。
