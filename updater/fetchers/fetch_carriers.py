"""Alphaliner public Top 100 -> carriers.json"""
import json,sys,urllib.request,datetime
req=urllib.request.Request("https://alphaliner.axsmarine.com/PublicTop100/rooter.php",data=json.dumps([{"action":"top100","method":"getTop100Table","data":None,"type":"rpc","tid":1}]).encode(),headers={"Content-Type":"application/json","X-Requested-With":"XMLHttpRequest","Referer":"https://alphaliner.axsmarine.com/PublicTop100/","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36"})
r=[x for x in json.load(urllib.request.urlopen(req,timeout=60))[0]['result'] if 'rank' in x]
top=[dict(rank=x['rank'],name=x['comp_name'],teu=x['totalTeu'],ships=x['totalShips'],share=x['percent'],chartered=x['chartProcent'],order_teu=x['orderTeu'],order_pct=x['orderProcents'],flag=x['carrier_flag'][-6:-4]) for x in r[:30]]
json.dump({"date":datetime.date.today().isoformat(),"source":"Alphaliner Top 100","source_url":"https://alphaliner.axsmarine.com/PublicTop100/","world_teu":round(r[0]['totalTeu']/r[0]['percent']*100),"carriers":top},open(sys.argv[1],'w'),ensure_ascii=False)
print("carriers",len(top),file=sys.stderr)
