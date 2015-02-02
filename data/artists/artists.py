import scraperwiki
import lxml.html
import urlparse
import json
import rdflib import Graph, URIRef
from SPARQLWrapper import SPARQLWrapper, JSON

artists = json.load(open('../../app/static/artist_101_names.json')) ## this is for query wikipedia
dump = {page.url:page.content for page in [wikipedia.page(artist) for artist in artists.values()]}

json.dump(dump, open("wiki_dump_101.json", "wb"))

## DBpedia for b and d dates
artists_url = [url.split('/')[-1] for url in json.load(open("wiki_dump_101.json")).keys()]
def unquote_uni(artist):
    return unidecode(urllib.unquote(artist.replace("_", " ").split('/')[-1].encode('utf-8')).decode("utf-8"))
info = {unquote_uni(artist):{"birthYear":None, "deathYear":None, "birthPlace":None, "lat":None, "lon":None} for artist in artists_url}  

def get_geo(place_url):
    try:
        html = scraperwiki.scrape(place_url)
        root = lxml.html.fromstring(html)
        try:
            lat = root.xpath("//span[@property='geo:lat']/text()")[0]
            lon = root.xpath("//span[@property='geo:long']/text()")[0]
            return {"lat":float(lat), "lon":float(lon)}
        except:
            return None
    except:
        return None

for artist in artists_url:
    un_artist = unquote_uni(artist)
    g = Graph()
    g.parse("http://dbpedia.org/resource/{0}".format(artist))
    # g.parse("http://dbpedia.org/resource/Andy_Warhol")
    # g.parse("http://dbpedia.org/resource/Johannes_Vermeer")

    for stmt in g.subject_objects(URIRef("http://dbpedia.org/ontology/birthDate")):
        info[un_artist]["birthYear"] = stmt[1][:4]
    for stmt in g.subject_objects(URIRef("http://dbpedia.org/ontology/deathDate")):
        info[un_artist]["deathYear"] = stmt[1][:4]
    place=[]
    for stmt in g.subject_objects(URIRef("http://dbpedia.org/ontology/birthPlace")):
        place.append(stmt[1])
        info[un_artist]["birthPlace"]= '; '.join([a.split('/')[-1] for a in place])
        for p in place:
            geo= get_geo(p)
            if geo:
                info[un_artist]["lat"]=geo["lat"]
                info[un_artist]["lon"]=geo["lon"]
                break
            else:
                continue
    print un_artist, info[un_artist]
                
len({k:v for k,v in zip(info.keys(), info.values()) if v["deathYear"]==None} )

json.dump(info, open("../../app/static/artist_101_info.json", "wb"))

## Wikipedia info box for BirthPlace and Picture
for url in json.load(open("wiki_dump_101.json")).keys():
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    print root.xpath("//span[@class='birthplace']/text()")


