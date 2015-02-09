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

@app.route('/slides')
def input():
    return render_template("slides.html")


@app.route('/output')
def output():
  #pull 'ID' from input field and store it
    artist = request.args.get('ID')
    if artist:
        with db:
            cur = db.cursor()
            cur.execute("set @num := 0, @type := '';")
            artist_sql = artist.replace("'", "''")
            cur.execute("select title, image_url, venue, @num := if(@type = venue, @num + 1, 1) as row_number, @type := venue as dummy from artworks WHERE ARTIST='{0}' group by venue, title having row_number <= 36;".format(artist_sql))        
            # cur.execute("SELECT TITLE, IMAGE_URL, VENUE FROM artworks WHERE ARTIST='%s' GROUP BY VENUE;" % artist)
            query_results = cur.fetchall()
            # cur.execute("SELECT TITLE FROM artworks WHERE ARTIST='%s';" % artist_sql)
            # query_results_full = cur.fetchall()
        artworks = []    
        for result in query_results:
            code = {
                "The Frick Collection":"frick",
                "Metropolitan Museum of Art":"met",
                "The Museum of Modern Art":"moma",
                "Whitney Museum of American Art":"whitney"
            }[result[2]]
            artworks.append(dict(title=result[0], image=result[1], venue=result[2], venue_code=code))

        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT, "static", "artist_101_names.json")
        pickle_url = os.path.join(SITE_ROOT, "static", "dist_mat")
        info_url = os.path.join(SITE_ROOT, "static", "artist_101_info.json")
        keywords_url = os.path.join(SITE_ROOT, "static", "keywords_101.json")
        keywords_to_artists_url = os.path.join(SITE_ROOT, "static", "keywords_to_artists.json")
        dist_mat = pickle.load(open(pickle_url))
        artist_names = json.load(open(json_url))
        artist_names = [x for (y,x)  in sorted(zip([int(k) for k in artist_names.keys()], artist_names.values()))]
        try:
            rec_artists = [a for a in dist_mat[artist]][:5]
        #    rec_path = ["/output?ID=" + a.replace(" ", "+") for a in rec_artists]
        except:
            return render_template("input_var.html")
        ## geo
        info = json.load(open(info_url))
        artist_info = info[artist]
        rec_artists_info = [info[rec] for rec in [a[0] for a in rec_artists]]

        ## list of artworks by venue
        artworks_by_venue = []
        for venue in set([artwork['venue'] for artwork in artworks]):
            artworks_by_venue.append([artwork for artwork in artworks if artwork['venue']==venue])
        venue_links = {"Metropolitan Museum of Art":"http://www.metmuseum.org/visit", "The Museum of Modern Art":"http://www.moma.org/visit/index", 'The Frick Collection':'http://www.frick.org/visit', 'Whitney Museum of American Art':'http://whitney.org/Visit'}

        ## keywords
        all_keywords = json.load(open(keywords_url))
        rec_keywords = [all_keywords[a[0]] for a in rec_artists]
        artist_keywords = all_keywords[artist]

        keywords_to_artists = json.load(open(keywords_to_artists_url))
        keywords_to_artist = {k:keywords_to_artists[k] for k in artist_keywords}

        return render_template("output.html", artworks = artworks, artworks_by_venue = artworks_by_venue, artist=artist, artist_keywords=artist_keywords,  rec_artists=rec_artists, artist_info=artist_info, rec_artists_info=rec_artists_info, rec_keywords = rec_keywords, keywords_to_artist=keywords_to_artist, venue_links=venue_links)

    else:
        return render_template("input_var.html")
