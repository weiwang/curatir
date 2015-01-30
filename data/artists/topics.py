from gensim import corpora, models, similarities, utils
from gensim.models import hdpmodel, ldamodel, lsimodel
from gensim.utils import lemmatize
import HTMLParser 
import urllib
import unidecode
from collections import Counter
from itertools import izip
import json
import cPickle as pickle
import operator
import pprint as pp

wiki_dump = json.load(open("wikipedia_text_dump.json"))
documents = wiki_dump.values()
artist_names = wiki_dump.keys()
artist_lastname = [unidecode.unidecode(urllib.unquote(a.split("/")[-1].split("_")[-1].encode("utf-8")).decode("utf-8")).lower() for a in artist_names]
texts_with_tag = [[w for w in utils.lemmatize(document)] for document in documents] # lemmatize and taggings
texts = [[w.split('/')[0] for w in text] for text in texts_with_tag]

dictionary = corpora.Dictionary(texts)


bow = False
corpus_bow = [dictionary.doc2bow(text) for text in texts]
texts_adj = [[w.split('/')[0] for w in text if w.split('/')[1]=="JJ" and w.split('/')[0] not in artist_lastname] for text in texts_with_tag]
dictionary_adj = corpora.Dictionary(texts_adj)
corpus_adj_bow = [dictionary.doc2bow(text) for text in texts_adj]

## Latent Semantic Analysis 
tfidf = models.TfidfModel(corpus_bow)
corpus_tfidf = tfidf[corpus_bow]
lsi = lsimodel.LsiModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=10)
index = similarities.MatrixSimilarity(lsi[corpus_tfidf])

tfidf_adj = models.TfidfModel(corpus_adj_bow)
## corpus_adj_tfidf = tfidf_adj[corpus_adj_bow]
for i in range(0, 101):
    print "\nThe 10 most common adj for " + artist_names[i].split('/')[-1] + ": "
    print [dictionary[j] for j in [a[0] for a in sorted(tfidf_adj[corpus_adj_bow[i]], key=lambda x: x[1], reverse=True)[:10]]]

keywords = {}
for i in range(0, 101):
    keywords[unidecode.unidecode(urllib.unquote(artist_names[i].split('/')[-1].replace("_", " ").encode("utf-8")).decode("utf-8"))] = [unidecode.unidecode(dictionary[j]) for j in [a[0] for a in sorted(tfidf_adj[corpus_adj_bow[i]], key=lambda x: x[1], reverse=True)[:10]]]

json.dump(keywords, open("../../app/static/keywords_101.json", "wb"))

def ImpWords(i):
    return [dictionary[i] for i in [a[0] for a in sorted(tfidf_adj[corpus_adj_bow[i]], key=lambda x: x[1], reverse=True)[:20]]]


def rec(num):
    sims = index[lsi[tfidf[corpus_bow[num]]]]
    sims = {a:b for a, b in zip(artist_names, sims)}
    sorted_sims = sorted(sims.items(), key=operator.itemgetter(1), reverse=True)
    print "Artists similar to " + artist_names[num].split('/')[-1]
    pp.pprint([x[0].split('/')[-1] for x in sorted_sims][1:6])


#artist_names_clean = json.load(open('../../app/static/artist_101_names_display.json'))
#artist_names_clean = [a[1] for a in sorted([[int(k),v] for k,v in zip(artist_names_clean.keys(), artist_names_clean.values())], key=lambda x: x[0])]
artist_names_display = [unidecode(urllib.unquote(a.replace("_", " ").split('/')[-1].encode('utf-8')).decode("utf-8")) for a in artist_names]
json.dump({k:v for k,v in zip(range(0,101), artist_names_display)}, open("../../app/static/artist_101_names_display.json", "wb"))
dist_mat = {}
for num in range(0, 101):
    sims = index[lsi[tfidf[corpus_bow[num]]]]
    sims = {a:b for a, b in zip(artist_names_display, sims)}
    sorted_sims = sorted(sims.items(), key=operator.itemgetter(1), reverse=True)
    sorted_sims = [list(a) for a in sorted_sims]
    dist_mat[artist_names_display[num]] = (sorted_sims[1:])

pickle.dump(dist_mat, open("../../app/static/dist_mat", 'wb'))

## LDA
# num_topics = 20
# if bow: # bag of words LDA
#     lda = ldamodel.LdaModel(corpus=corpus_bow, id2word=dictionary, num_topics=num_topics)
# else: # TFIDF LDA
#     tfidf = models.TfidfModel(corpus_bow)
#     corpus_tfidf = tfidf[corpus_bow]
#     lda = ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=num_topics)

# # inspect word distribution across topics
# lda.print_topics(lda.num_topics)

# # inspect topics distribution across documents
# topics_across_documents = []
# for doc in lda[corpus_tfidf]:
#     topic_dist = [0 for a in range(lda.num_topics)]
#     for d in doc:
#         topic_dist[d[0]] = d[1]
#     topics_across_documents.append(topic_dist)

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

