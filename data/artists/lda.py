from gensim import corpora, models, similarities, utils
from gensim.models import hdpmodel, ldamodel
from gensim.utils import lemmatize
from itertools import izip
import json

documents = json.load(open("wikipedia_text_dump.json"))
texts = [[w.split('/')[0] for w in utils.lemmatize(document)] for document in documents] # lemmatize and no taggings

dictionary = corpora.Dictionary(texts)

bow = False
corpus_bow = [dictionary.doc2bow(text) for text in texts]
if bow: # bag of words LDA
    lda = ldamodel.LdaModel(corpus=corpus_bow, id2word=dictionary, num_topics=50, update_every=1, chunksize=101, passes=1)
else: # TFIDF LDA
    tfidf = models.TfidfModel(corpus_bow)
    corpus_tfidf = tfidf[corpus_bow]
    lda = ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=50, update_every=1, chunksize=101, passes=1)

# inspect word distribution across topics
lda.print_topics(lda.num_topics)

# inspect topics distribution across documents
for doc in lda[corpus_tfidf]:
    print doc
