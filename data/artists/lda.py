from gensim import corpora, models, similarities, utils
from gensim.models import hdpmodel, ldamodel, lsimodel
from gensim.utils import lemmatize
from itertools import izip
import json
import pprint

documents = json.load(open("wikipedia_text_dump.json"))
artist_names = [document[:20] for document in documents]
texts = [[w.split('/')[0] for w in utils.lemmatize(document)] for document in documents] # lemmatize and no taggings

dictionary = corpora.Dictionary(texts)

## LDA

bow = False
corpus_bow = [dictionary.doc2bow(text) for text in texts]
num_topics = 20
if bow: # bag of words LDA
    lda = ldamodel.LdaModel(corpus=corpus_bow, id2word=dictionary, num_topics=num_topics)
else: # TFIDF LDA
    tfidf = models.TfidfModel(corpus_bow)
    corpus_tfidf = tfidf[corpus_bow]
    lda = ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=num_topics)

# inspect word distribution across topics
lda.print_topics(lda.num_topics)

# inspect topics distribution across documents
topics_across_documents = []
for doc in lda[corpus_tfidf]:
    topic_dist = [0 for a in range(lda.num_topics)]
    for d in doc:
        topic_dist[d[0]] = d[1]
    topics_across_documents.append(topic_dist)

## Monet = 7, Vermeer = 42, Cezanne = 3, Matisse = 19, Renoir = 74, Chagall = 30, Vermeer = 42
## O'Keeffe = 96, Rothko = 18
index = 74
simi={name:0 for name in artist_names}
for i in range(0,101):
    if not (index == i):
        simi[artist_names[i]]=sum([a*b for a, b in zip(topics_across_documents[index], topics_across_documents[i])])
import operator
sorted_simi = sorted(simi.items(), key=operator.itemgetter(1), reverse=True)
print "\n\n20 most similar artists to " + artist_names[index] + " is:\n"
pprint.pprint(sorted_simi[:20])

## Latent Semantic Analysis 
lsi = lsimodel.LsiModel(corpus=corpus_bow, id2word=dictionary, num_topics=10)
index = similarities.MatrixSimilarity(lsi[corpus_bow])

def rec(num):
    sims = index[lsi[corpus_bow[num]]]
    sims = {a:b for a, b in zip(artist_names, sims)}
    sorted_sims = sorted(sims.items(), key=operator.itemgetter(1), reverse=True)
    pp.pprint(sorted_sims[1:6])

