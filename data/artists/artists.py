import scraperwiki
import lxml.html
import urlparse
import json

url =  'http://www.theartwolf.com/articles/most-important-painters.htm'
root = lxml.html.fromstring(scraperwiki.scrape(url))
artists = root.xpath("//p/strong//text()")
json.dump(artist, open('artists_101.json', "wb"))



    
