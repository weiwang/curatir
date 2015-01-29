from flask import render_template, request
from app import app
import pymysql as mdb
import json
import cPickle as pickle
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
    pickle_url = os.path.join(SITE_ROOT, "static", "dist_mat")
    info_url = os.path.join(SITE_ROOT, "static", "artist_101_info.json")
    dist_mat = pickle.load(open(pickle_url))
    artist_names = json.load(open(json_url))
    artist_names = [x for (y,x)  in sorted(zip([int(k) for k in artist_names.keys()], artist_names.values()))]
    rec_artists = [a for a in dist_mat[artist]][:5]
    #    rec_path = ["/output?ID=" + a.replace(" ", "+") for a in rec_artists]

    ## geo
    info = json.load(open(info_url))
    artist_info = info[artist]
    rec_artists_info = [info[rec] for rec in [a[0] for a in rec_artists]]

    ## list of artworks by venue
    artworks_by_venue = []
    for venue in set([artwork['venue'] for artwork in artworks]):
        artworks_by_venue.append([artwork for artwork in artworks if artwork['venue']==venue])

    return render_template("output.html", artworks = artworks, artworks_by_venue = artworks_by_venue, artist=artist, rec_artists=rec_artists, artist_info=artist_info, rec_artists_info=rec_artists_info)

