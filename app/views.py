from flask import render_template, request
from app import app
import pymysql as mdb
import json
import os

db = mdb.connect(user="root", host="localhost", db="nyarts", charset='utf8')

@app.route('/')
            
@app.route('/index')
def index():
    return render_template("input.html")

@app.route('/input')
def input():
    return render_template("input.html")


@app.route('/output')
def output():
  #pull 'ID' from input field and store it
    artist = request.args.get('ID')
    #    artist.replace("'", "''")
    with db:
        cur = db.cursor()
        cur.execute("set @num := 0, @type := '';")
        cur.execute("select title, image_url, venue, @num := if(@type = venue, @num + 1, 1) as row_number, @type := venue as dummy from artworks WHERE ARTIST='{0}' group by venue, title having row_number <= 10;".format(artist))
        # cur.execute("SELECT TITLE, IMAGE_URL, VENUE FROM artworks WHERE ARTIST='%s' GROUP BY VENUE;" % artist)
        query_results = cur.fetchall()
        cur.execute("SELECT TITLE FROM artworks WHERE ARTIST='%s';" % artist)
        query_results_full = cur.fetchall()

    artworks = []    
    for result in query_results:
        code = {
            "The Frick Collection":"frick",
            "Metropolitan Museum of Arts":"met",
            "The Museum of Modern Art":"moma",
            "Whitney Museum of American Art":"whitney"
        }[result[2]]
        artworks.append(dict(title=result[0], image=result[1], venue=result[2], venue_code=code))
    
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static", "artist_101_names.json")
    s_artist = json.load(open(json_url))
    s_artist = [v for v in s_artist.values()][:5]
    #    s_artist = json.load(open("./static/artist_101_names.json"))[:5]

    return render_template("output.html", artworks = artworks, artist=artist, number=len(query_results_full), s_artist=s_artist)

