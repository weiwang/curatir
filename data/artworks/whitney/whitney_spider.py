import scraperwiki
import lxml.html
import urlparse
import json

def scrape_page(url):    
    print(url.split("/")[-1])
    try:
        root = lxml.html.fromstring(scraperwiki.scrape(url))
        material = root.xpath("//div[@class='detail object-medium']/p[@class='info']//text()")[0]
        if any([word in material.lower() for word in ['oil', 'canvas', 'painting']]):
            artist, title = root.xpath("//title//text()")[0].split(": ")[1:]
            image = root.xpath("//img[@class='artwork']/@src")[0]            
            item = {
                'id' :  url,
                'title' : title,
                'artist' : artist,
                'image' : image,
                'material' : material,
                'venue' : 'Whitney Museum of American Art'
            }        
            return item
        else:
            return None
        
    except:
        return None


if __name__ == "__main__":
    base_url = "http://collection.whitney.org/object/"
    N = 20000
    dump = [scrape_page(url) for url in [base_url+str(a) for a in range(1, N)]]
    dump = [d for d in dump if d]
    json.dump(dump, open('whitney_dump.json', "wb"))
    
    
    
    
