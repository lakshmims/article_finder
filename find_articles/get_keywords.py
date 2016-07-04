from __future__ import unicode_literals
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import NMF
import sys
import pickle
#from article_finder.models.src.get_data import process_text
from unidecode import unidecode
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tag import pos_tag
import re
import numpy as np
import urllib
import urllib2
import json

import httplib
import urllib
import base64
import os


def find_keywords(new_document,vectorizer,model):

    doc_tfif = vectorizer.transform([new_document])

    t = np.array(doc_tfif.todense())
    keyword_indexes = t[0].argsort()[:-5: -1]
    feature_names = vectorizer.get_feature_names()
    f_names = np.array(feature_names)

    tfif_keywords = f_names[keyword_indexes]

    new_transformed_doc = model.transform(doc_tfif)

    # keywords from topics
    topic_keywords = []
    x = new_transformed_doc[0].argsort()[:-3:-1]
    feature_names = vectorizer.get_feature_names()
    for row in model.components_[x, :]:
        topic_keywords.append( " ".join([feature_names[i] for i in row.argsort()[:-3:-1]]))

    return " ".join(tfif_keywords) + " " + " ".join(topic_keywords)


def process_text(content_list):

    content_list_new = []
    wl = WordNetLemmatizer()
    stop_words = stopwords.words('english')
    regex = re.compile('[^a-zA-Z]')

    for content in content_list:
        word_list_1 = content.split()
        word_list_2 = [word for word in word_list_1 if word not in stop_words]
        pos_to_drop = ['CC','IN','UH','WP','DT','WDT','PRP','VBD','PRP$','RB', 'VB','VBP']
        tagged_content = pos_tag(word_list_2)

        word_list_3 = []
        for word,pos in tagged_content:
            if pos not in pos_to_drop:
                word_list_3.append(word)

        word_list_4 = [regex.sub(" ",wl.lemmatize(word)) for word in word_list_3 ]

        content_list_new.append(" ".join(word_list_4))
    return content_list_new

def unpkl(file_name):
    with open(file_name, 'r') as f:
        unpkl_file = pickle.load(f)
    return unpkl_file

def search_docs(bing_api_key, key_words):
    similar_stories = []
    headers = {'Ocp-Apim-Subscription-Key': bing_api_key,}

    params = urllib.urlencode({
        # Request parameters
        'q': key_words,
        'count': '10',
        'offset': '0',
        'mkt': 'en-us',
        'safesearch': 'Moderate', })

    try:
        conn = httplib.HTTPSConnection('api.cognitive.microsoft.com')
        conn.request("GET", "/bing/v5.0/news/search?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    res = json.loads(data)
    for story in res['value']:
        source = story['provider'][0]['name']
        headline = story['name']
        url = story['url']
        similar_stories.append((headline,source, url))

    return similar_stories



if __name__ == '__main__':
    new_document_file = sys.argv[1]
    pkl_vectorizer_file = sys.argv[2]
    pkl_nmf_file = sys.argv[3]

    with open(new_document_file,'r') as f:
        new_document = f.read()

    vectorizer = unpkl(pkl_vectorizer_file)
    nmf = unpkl(pkl_nmf_file)

    key_words = find_keywords(new_document,vectorizer,nmf)

    #bing_api_key = os.environ['BING_API_KEY']
    bing_api_key = 'c705afe8bd8645aebb686f7a925ebb20'
    similar_stories = search_docs(bing_api_key, key_words)
    for x,y,z in similar_stories:
        print x,y , '\n'
