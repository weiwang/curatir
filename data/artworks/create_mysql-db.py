import pymysql as mdb
import os
files= []
# for root, dirs, files in os.walk("."):
#     for file in files:
#         if file.endswith(".json"):
#             files.append(os.path.join(root, file)))
            
files = ['./frick/frick_painting_dump.json']
con = mdb.connect(host='localhost', user='root', passwd='', db='nyarts', use_unicode=True,charset="latin1") #host, user, password, #database

with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS artworks")
    cur.execute("CREATE TABLE artworks (Id INT PRIMARY KEY AUTO_INCREMENT,TITLE VARCHAR(25),ARTIST VARCHAR(25), MATERIAL VARCHAR(25), VENUE VARCHAR(25))")

    add_artwork = ("INSERT INTO artworks (TITLE, ARTIST, MATERIAL, VENUE) VALUES (%s, %s, %s, %s)")        
    
    for file in files:
        musuem = json.load(open(file))
        for record in museum:            
            if record:
                title =record['title'].replace("'", "''")
                artist = record['artist'].replace("'", "''")
                material = record['material'].replace("'", "''")
                venue = record['venue'].replace("'", "''")
                query = u"INSERT INTO artworks (TITLE, ARTIST, MATERIAL, VENUE) VALUES ('{0}', '{1}', '{2}', '{3}')".format(title, artist, material, venue)
                cur.execute(query)
                #cur.execute(add_artwork, artwork)


with con: 
    cur = con.cursor()
    cur.execute("SELECT * FROM artworks")
    rows = cur.fetchall()
    for row in rows:
        print row
                
cur.close()
con.close()
