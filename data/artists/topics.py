from gensim import corpora, models, similarities, utils
from gensim.models import hdpmodel, ldamodel, lsimodel
from gensim.utils import lemmatize
import HTMLParser 
import urllib
from unidecode import unidecode
from collections import Counter
from itertools import izip
import json
import cPickle as pickle
import operator
import pprint as pp


## preparations
wiki_dump = json.load(open("wiki_dump.json"))
# wiki_dump_101 = json.load(open("wiki_dump_101.json"))
# wiki_dump.update(wiki_dump_101)
# json.dump(wiki_dump, open("wiki_dump.json", "wb"))
documents = wiki_dump.values()
artist_names = wiki_dump.keys()
artist_name_break = [map(lambda x: urllib.unquote(x.encode("utf-8")).decode("utf-8").lower(), a.split("/")[-1].split("_")) for a in artist_names]
artist_name_break = set(sum(artist_name_break, []))
stoplist = set('for a of the and to in'.split())
texts_with_tag = [[w for w in utils.lemmatize(document)] for document in documents] # lemmatize and taggings
pickle.dump(texts_with_tag, open("texts_with_tag.dump", "wb"))
texts = [[w.split('/')[0] for w in text] for text in texts_with_tag]

# all_tokens = sum(texts, [])
# tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)

filter_set = set.intersection(artist_name_break, stoplist, token_once)
## texts = [[word for word in text if word not in filter_set] for text in texts]
dictionary = corpora.Dictionary(texts)
bow = False
corpus_bow = [dictionary.doc2bow(text) for text in texts]
tfidf = models.TfidfModel(corpus_bow)
corpus_tfidf = tfidf[corpus_bow]

## LSA for 
lsi = lsimodel.LsiModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=50)
index = similarities.MatrixSimilarity(lsi[corpus_tfidf])

def word_to_artist(word, show_all=False):
    """
    associate artists with a word
    """
    artists_url = [url for url in json.load(open("wiki_dump_101.json")).keys()]
    sims = index[lsi[tfidf[dictionary.doc2bow([word])]]]
    if show_all:
        sims = {a:b for a, b in zip(artist_names, sims)}
    else:
        sims = {a:b for a, b in zip(artist_names, sims) if a in artists_url}
    sorted_sims = sorted(sims.items(), key=operator.itemgetter(1), reverse=True)
    # print "Artists related to " + str(len(sorted_sims)) + word
    # pp.pprint([[x[0].split('/')[-1], x[1]] for x in sorted_sims][:10])
    return [a[0] for a in [[x[0].split('/')[-1], x[1]] for x in sorted_sims][:5]]


texts_adj = [[w.split('/')[0] for w in text if w.split('/')[1]=="JJ" and w.split('/')[0] not in artist_name_break] for text in texts_with_tag]
dictionary_adj = corpora.Dictionary(texts_adj)
corpus_adj_bow = [dictionary.doc2bow(text) for text in texts_adj]
tfidf_adj = models.TfidfModel(corpus_adj_bow)

artists_url = [url for url in json.load(open("wiki_dump_101.json")).keys()]
artists_index = [artist_names.index(url) for url in artist_names if url in artists_url]
## corpus_adj_tfidf = tfidf_adj[corpus_adj_bow]
for url in artists_url:
    try:
        i = artist_names.index(url)
        print "\nThe 10 most common adj for " + artist_names[i].split('/')[-1] + ": "
        print [dictionary[j] for j in [a[0] for a in sorted(tfidf_adj[corpus_adj_bow[i]], key=lambda x: x[1], reverse=True)[:10]]]
    except:
        pass

keywords = {}
for url in artists_url:
    try:
        i = artist_names.index(url)
        keywords[unidecode.unidecode(urllib.unquote(artist_names[i].split('/')[-1].replace("_", " ").encode("utf-8")).decode("utf-8"))] = [unidecode.unidecode(dictionary[j]) for j in [a[0] for a in sorted(tfidf_adj[corpus_adj_bow[i]], key=lambda x: x[1], reverse=True)[:10]]]
    except:
        pass

keywords_artists = {keyword:[url_name_extract(a) for a in word_to_artist(keyword)] for keyword in list(set(sum(keywords.values(),[])))}

json.dump(keywords_artists, open("../../app/static/keywords_to_artists.json", "wb"))

json.dump(keywords, open("../../app/static/keywords_101.json", "wb"))

def ImpWords(i):
    return [dictionary[i] for i in [a[0] for a in sorted(tfidf_adj[corpus_adj_bow[i]], key=lambda x: x[1], reverse=True)[:20]]]


#artist_names_clean = json.load(open('../../app/static/artist_101_names_display.json'))
#artist_names_clean = [a[1] for a in sorted([[int(k),v] for k,v in zip(artist_names_clean.keys(), artist_names_clean.values())], key=lambda x: x[0])]
# artist_names_display = [unidecode(urllib.unquote(a.replace("_", " ").split('/')[-1].encode('utf-8')).decode("utf-8")) for a in artist_names]
# json.dump({k:v for k,v in zip(range(0,101), artist_names_display)}, open("../../app/static/artist_101_names_display.json", "wb"))
def url_name_extract(url):
    return unidecode(urllib.unquote(url.replace("_", " ").split('/')[-1].encode('utf-8')).decode("utf-8"))

dist_mat = {}
for artist in artists_url:
    num = artist_names.index(artist)
    sims = index[lsi[tfidf[corpus_bow[num]]]]
    sims = {url_name_extract(a):b for a, b in zip(artist_names, sims) if a in artists_url}
    sorted_sims = sorted(sims.items(), key=operator.itemgetter(1), reverse=True)
    sorted_sims = [list(a) for a in sorted_sims]
    dist_mat[url_name_extract(artist)] = (sorted_sims[1:]) # not including the artist herself

pickle.dump(dist_mat, open("../../app/static/dist_mat", 'wb'))


## Latent Dirichelt Allocation
num_topics = 100
if bow: # bag of words LDA
    lda = ldamodel.LdaModel(corpus=corpus_bow, id2word=dictionary, num_topics=num_topics, distributed=False, chunksize=500, passes=1, update_every=1)
else: # TFIDF LDA
    tfidf = models.TfidfModel(corpus_bow)
    corpus_tfidf = tfidf[corpus_bow]
    lda = ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=num_topics, distributed=False, chunksize=500, passes=1, update_every=1)

# inspect word distribution across topics
lda.print_topics(lda.num_topics)
def topic_inspector(artist):
    i = artist_names.index(artist)
    ##     print texts[i]
    ##    pdb.set_trace()
    topics_dist = sorted(lda[tfidf[corpus_bow[i]]], key=lambda x:x[1], reverse=True)
    for topic in topics_dist:
        print "prob " + str(topic[1])
        print lda.print_topic(topic[0])

topic_inspector("http://en.wikipedia.org/wiki/Johannes_Vermeer")
topic_inspector("http://en.wikipedia.org/wiki/Edward_Hopper")
topic_inspector("http://en.wikipedia.org/wiki/Claude_Monet")
topic_inspector("http://en.wikipedia.org/wiki/")

# inspect topics distribution across documents
topics_across_documents = []
for doc in lda[corpus_tfidf]:
    topic_dist = [0 for a in range(lda.num_topics)]
    for d in doc:
        topic_dist[d[0]] = d[1]
    topics_across_documents.append(topic_dist)

# ## Monet = 7, Vermeer = 42, Cezanne = 3, Matisse = 19, Renoir = 74, Chagall = 30, Vermeer = 42
# ## O'Keeffe = 96, Rothko = 18
# index = 74
# simi={name:0 for name in artist_names}
# for i in range(0,101):
#     if not (index == i):
#         simi[artist_names[i]]=sum([a*b for a, b in zip(topics_across_documents[index], topics_across_documents[i])])
# import operator
# sorted_simi = sorted(simi.items(), key=operator.itemgetter(1), reverse=True)
# print "\n\n20 most similar artists to " + artist_names[index] + " is:\n"
# pprint.pprint(sorted_simi[:20])

