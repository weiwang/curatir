import scraperwiki
import lxml.html
import urlparse
import json

def scrape_page(url):    
    print(url.split("/")[-1])
    try:
        root = lxml.html.fromstring(scraperwiki.scrape(url))
        artist, title = root.xpath("//title//text()")[0].split(": ")[1:]
        image = root.xpath("//img[@class='artwork']/@src")[0]
        material = root.xpath("//div[@class='detail object-medium']/p[@class='info']//text()")[0]
        item = {
            'id' :  url,
            'title' : title,
            'artist' : artist,
            #'location' : displayLoc,
            'image' : image,
            'material' : material,
            'venue' : 'Whitney Museum of American Art'
            }        
        ## print item
        return item
        
    except:
        return None


if __name__ == "__main__":
    base_url = "http://collection.whitney.org/object/"
    N = 20000
    dump = [scrape_page(url) for url in [base_url+str(a) for a in range(1, N)]]
    json.dump(dump, open('whitney_dump.json', "wb"))
    
    
    
    
