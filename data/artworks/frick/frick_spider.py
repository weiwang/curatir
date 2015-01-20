import scraperwiki
import lxml.html
import urlparse
import json

def scrape_page(root, material):    
    try:
        artist, title = root.xpath("//title/text()")[0].split(" : ")[0].split(" - ")
        image = root.xpath("//img[contains(@src, '/internal/media')]/@src")[0]
        ## material = [m.strip().split(" (")[0] for m in root.xpath("//div[text()='Object Type / Material']/following-sibling//text()").split(" (")]
        id = root.xpath("//a[@class='permalink']/@href")[0]
        onview = root.xpath("//div[@id='onview']/span//text()")[0]
        item = {
            'id' :  id,
            'title' : title,
            'artist' : artist,
            #'location' : displayLoc,
            'image' : base_url + image,
            'material' : material,
            'venue' : "The Frick Collection",
            'onview' : onview
            }
        
        if (onview == "Currently on View"):
            print item
            return item
        return None
        
    except:
        ## print 1
        pass

def spider(starting_url, material):
    html = scraperwiki.scrape(starting_url)
    root = lxml.html.fromstring(html)
    dump = []
    dump.append(scrape_page(root, material))
    
    next_link = root.xpath("//a[text()='Next']/@href")[0]

    while(next_link):
        html = scraperwiki.scrape(base_url + next_link)
        root = lxml.html.fromstring(html)
        dump.append(scrape_page(root, material))
        try:
            next_link = root.xpath("//a[text()='Next']/@href")[0]
        except:
            next_link = None
    json.dump(dump, open('frick_'+material+'_dump.json', "wb"))

    
starting_url_painting = 'http://collections.frick.org/view/objects/asitem/152/0/primaryMaker-asc/title-asc?t:state:flow=3435e5e4-1bb6-4551-93a9-54bd5a7348ee'
starting_url_sculpture = 'http://collections.frick.org/view/objects/asitem/126/0/primaryMaker-asc/title-asc?t:state:flow=b97f233f-91f7-4b80-9cf9-08cec00ec555'
base_url = "http://collections.frick.org/"

if __name__ == "__main__":
    spider(starting_url_painting, "painting")
    spider(starting_url_sculpture, "sculpture")
    
