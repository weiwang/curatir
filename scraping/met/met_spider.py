import scraperwiki
import lxml.html
import urlparse
import json

def scrape_page(root, material):
    
    try:
        # for p in root.xpath("//div[@id='omniture_caption']/h3//text()"):
        #     title = p

        # for p in root.xpath("//h4[text()='Works: ']/following-sibling::div/a[@href]//text()"):
        #     artist = p

        # for p in root.xpath("//h4[text()='Classification: ']/following-sibling::div/a[@href]//text()"):
        #     material = p

        # for p in root.xpath("//h4[text()='Permalink: ']/following-sibling::div/a[@href]/@href"):
        #     id = p

        # for p in root.xpath("//p[@id='mainImage']//@src"):
        #     image = p
        artist, title = root.xpath("//title/text()")[0].split(" | ")[:2]
        image = root.xpath("//div[@id='inner-image-container']/img/@src")
        ## material = [m.strip().split(" (")[0] for m in root.xpath("//div[text()='Object Type / Material']/following-sibling//text()").split(" (")]
        id = root.xpath("//a[@class='permalink']/@href")[0]
        item = {
            'id' :  "http://metmuseum.org/" + id,
            'title' : title,
            'artist' : artist,
            #'location' : displayLoc,
            'image' : image,
            'material' : material,
            'venue' : "Metropolitan Museum of Arts"
            }
        print item
        return item
        
    except:
        ## print 1
        pass

# def scrape_and_look_for_next_link(url):
#     html = scraperwiki.scrape(url)
#     ## print html
#     root = lxml.html.fromstring(html)
#     material = url.split("_")[-1]
#     scrape_page(root, material)

#     ## next_link = root.cssselect("a.next")      

#     next_link = root.xpath("//a[@class='next']/@href")[0]
    
#     ## print next_link
#     if next_link:
#         ## print next_url
#         scrape_and_look_for_next_link(base_url+next_link)

def spider(starting_url, material):
    i = 0;
    html = scraperwiki.scrape(starting_url)
    root = lxml.html.fromstring(html)
    dump = []
    dump.append(scrape_page(root, material))
    
    next_link = root.xpath("//a[@class='next']/@href")[0]

    while(next_link):
        html = scraperwiki.scrape(base_url + next_link)
        root = lxml.html.fromstring(html)
        dump.append(scrape_page(root, material))
        next_link = root.xpath("//a[@class='next']/@href")[0]
        i = i+1
    json.dump(dump, open('met_'+material+'_dump.json', "wb"))

    
starting_url_painting = 'http://metmuseum.org/collection/the-collection-online/search/435809?rpp=30&pg=1&od=on&ao=on&ft=painting&pos=1'
starting_url_sculpture = 'http://metmuseum.org/collection/the-collection-online/search/312429?rpp=30&pg=1&od=on&ao=on&ft=sculpture&pos=1'
base_url = "http://metmuseum.org"

if __name__ == "__main__":
    spider(starting_url_painting, "painting")
    spider(starting_url_sculpture, "sculpture")
    
