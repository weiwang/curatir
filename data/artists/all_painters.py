## retrieve all painters texts from kimonolabs
import json
import urllib
texts=dict()
for k in range(0, 15): # every call returns 2,500 rows and there are ~35,000 rows in total
    results = json.load(urllib.urlopen("https://www.kimonolabs.com/api/ehiwm3mm?apikey=RfvyCnmyi1lAyMcLBuufFFuZRbZ0drHr&kimoffset="+str(k*2500)+"&kimbypage=1"))
    texts.update({results['results'][i]['url']:" ".join(map(lambda x: x['property1']['text'], results['results'][i]['collection1'])) for i in range(0, len(results['results'])) if len(results['results'][i]['collection1'])>1})

json.dump(texts, open("wiki_dump.json", "wb"))


