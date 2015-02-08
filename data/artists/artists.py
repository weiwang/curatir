import scraperwiki
import lxml.html
import urlparse
import urllib
import json
from rdflib import Graph, URIRef
from unidecode import unidecode
from geopy.geocoders import Nominatim

# artists = json.load(open('../../app/static/artist_101_names.json')) ## this is for query wikipedia
# dump = {page.url:page.content for page in [wikipedia.page(artist) for artist in artists.values()]}

# json.dump(dump, open("wiki_dump_101.json", "wb"))

## DBpedia for b and d dates
artists_url = [url.split('/')[-1] for url in json.load(open("wiki_dump_101.json")).keys()]
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
    g.parse("http://dbpedia.org/resource/{0}".format(artist))

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
                info[un_artist]["birthAddress"] = unidecode(geolocator.reverse([geo['lat'], geo['lon']]).address).split(", ")[-1]
                break
            else:
                continue
    counter = counter + 1
    print counter

def normalize(artist):
    artist['birthAddress'] = artist['birthAddress'].replace('Belgie - Belgique - Belgien', 'Belgium')
    artist['birthAddress'] = artist['birthAddress'].replace('Espana', 'Spain')
    artist['birthAddress'] = artist['birthAddress'].replace( 'Ellada','Greece')
    artist['birthAddress'] = artist['birthAddress'].replace('Deutschland', 'Germany')
    artist['birthAddress'] = artist['birthAddress'].replace('Estados Unidos Mexicanos', 'Mexico')
    artist['birthAddress'] = artist['birthAddress'].replace('Italia', 'Italy')
    artist['birthAddress'] = artist['birthAddress'].replace('Nederland', 'Netherlands')
    artist['birthAddress'] = artist['birthAddress'].replace('Norge', 'Norway')
    artist['birthAddress'] = artist['birthAddress'].replace('Osterreich', 'Austria')
    artist['birthAddress'] = artist['birthAddress'].replace('Rossiia', 'Russia')
    artist['birthAddress'] = artist['birthAddress'].replace('Svizra', 'Switzerland')
    artist['birthAddress'] = artist['birthAddress'].replace("Belarus'", "Belarus")
    return artist;

info = {k:normalize(v) for k,v in zip(info.keys(), info.values())}
    

# find how many artists have no deathyear                
len({k:v for k,v in zip(info.keys(), info.values()) if v["deathYear"]=='????'} )

json.dump(info, open("../../app/static/artist_101_info.json", "wb"))


