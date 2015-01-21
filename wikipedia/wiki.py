# Standard packages for data analysis

import numpy as np
import matplotlib.pyplot as plt

# pandas handles tabular data
import pandas as pd

# networkx handles network data
import networkx as nx

# json handles reading and writing JSON data
import json

# To visualize webpages within this webpage
from IPython.display import HTML

# To run queries against MediaWiki APIs
from wikitools import wiki, api, page
import wikipedia 

# Some other helper functions
from collections import Counter
from operator import itemgetter

def wikipedia_query(query_params,site_url='http://en.wikipedia.org/w/api.php'):
    site = wiki.Wiki(url=site_url)
    request = api.APIRequest(site, query_params)
    result = request.query()
    return result[query_params['action']]

def get_article_links(article):
    query = {'action': 'query',
             'redirects': 'True',
             'prop': 'links|linkshere',
             'titles': article, # the article variable is passed into here
             'pllimit': '500',
             'plnamespace': '0',
             'lhlimit': '500',
             'lhnamespace': '0',
             'lhshow': '!redirect',
             'lhprop': 'title'}
    results = wikipedia_query(query) # do the query
    page_id = results['pages'].keys()[0] # get the page_id
    
    if 'links' in results['pages'][page_id].keys(): #sometimes there are no links
        outlist = [link['title'] for link in results['pages'][page_id]['links']] # clean up outlinks
    else:
        outlist = [] # return empty list if no outlinks
    
    if 'linkshere' in results['pages'][page_id].keys(): #sometimes there are no links
        inlist = [link['title'] for link in results['pages'][page_id]['linkshere']] # clean up inlinks
    else:
        inlist = [] # return empty list if no inlinks
    return len(outlist),len(inlist)

article = "Bill Clinton"
outd, ind = get_article_links(article)
print "There are {0} out links from and {1} in links to the ".format(outd,ind)
print article+" article"


PaulCezanne = wikipedia.page("Paul Cezanne")
PaulCezanne.content()


import urllib


artists = open()
params = { "format":"xml", "action":"parse", "prop":"revisions", "rvprop":"timestamp|user|comment|content" }
params["titles"] = "API|%s" % urllib.quote(title.encode("utf8"))
qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
url = "http://en.wikipedia.org/w/api.php?%s" % qs
urllib.urlopen(url).read()
