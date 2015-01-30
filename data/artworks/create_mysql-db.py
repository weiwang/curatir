import pymysql as mdb
import os
import json

files=os.popen("find . -type f -name '*.json'").read().strip().split('\n')            
#files = ['./frick/frick_painting_dump.json']
con = mdb.connect(host='localhost', user='root', passwd='', db='nyarts', use_unicode=True,charset="utf8") #host, user, password, #database

with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS artworks")
    cur.execute("CREATE TABLE artworks (Id INT PRIMARY KEY AUTO_INCREMENT,TITLE VARCHAR(50),ARTIST VARCHAR(50), MATERIAL VARCHAR(50), VENUE VARCHAR(50), URL VARCHAR(100), IMAGE_URL VARCHAR(100))")
    for file in files:
        museum = json.load(open(file))
        for record in museum:            
            if record:
                title =record['title'].replace("'", "''")
                artist = record['artist'].replace("'", "''")
                material = record['material'].replace("'", "''")
                venue = record['venue'].replace("'", "''")
                url = record['id']
                if type(url) is list:
                    url = url[0]
                image_url = record['image']
                if type(image_url) is list:
                    image_url = image_url[0]
                query = u"INSERT INTO artworks (TITLE, ARTIST, MATERIAL, VENUE, URL, IMAGE_URL) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(title, artist, material, venue, url, image_url)
                cur.execute(query)


