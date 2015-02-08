import scraperwiki
import lxml.html
import urlparse
import urllib
import json
from rdflib import Graph, URIRef
from unidecode import unidecode
from geopy.geocoders import Nominatim

## Dbpedia for b and d dates
artists_url = [url.split('/')[-1] for url in json.load(open("wiki_dump.json")).keys()]
def unquote_uni(artist):
    return unidecode(urllib.unquote(artist.replace("_", " ").split('/')[-1].encode('utf-8')).decode("utf-8"))
wiki_prefix = "https://en.wikipedia.org/wiki/"
info = {unquote_uni(artist):{"birthYear":'????', "deathYear":'????', "birthPlace":'Not available', "birthAddress":'Not available' ,"lat":'Not available', "lon":'Not available', "wiki":wiki_prefix+artist} for artist in artists_url}  
geolocator = Nominatim()

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

counter = 0
for artist in artists_url:
    un_artist = unquote_uni(artist)
    g = Graph()
    try:
        g.parse("http://dbpedia.org/resource/{0}".format(artist))
    except:
        continue;
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
                # info[un_artist]["birthAddress"] = geolocator.reverse([geo['lat'], geo['lon']]).address
                break
            else:
                continue
    counter = counter + 1
    print counter

# find how many artists have no deathyear                
len({k:v for k,v in zip(info.keys(), info.values()) if v["deathYear"]==None} )


# def remove_None(x):
#     if x["birthYear"] is None:
#         x["birthYear"]="????";
#     if x["deathYear"] is None:
#         x["deathYear"]="????";
#     if x["birthPlace"] is None:
#         x["deathYear"]="????";
#     return x;

# def add_born_country(x):
#     geolocator = Nominatim()
#     if x["lat"] is not None:
#         x["birthAddress"] = geolocator.reverse([x['lat'], x['lon']]).address
#     else:
#         x["lat"] = 'Not available'
#         x["lon"] = 'Not available'
#         x["birthAddress"] = 'Not available'
#     return x

# values = map(remove_None, values)

# values = map(add_born_country, values)
# new_info = {key:value for key, value in zip(info.keys(), values)}


json.dump(info, open("../../app/static/artist_info.json", "wb"))
