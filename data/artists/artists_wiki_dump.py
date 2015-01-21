import json
import wikipedia

artists = json.load(open('artists_101.json'))
dump=[]
for artist in artists:
    dump.append(wikipedia.page(artist).content)

json.dump(dump, open("wikipedia_text_dump.json", "wb"))
