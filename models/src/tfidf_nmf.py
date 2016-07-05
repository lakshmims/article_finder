from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF,LatentDirichletAllocation
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
import sys


import pickle

def model_nmf(content_list,max_df, min_df, max_features, n_topics):
    #vectorizer = TfidfVectorizer(max_df=max_df, min_df=min_df, max_features=max_features, binary=False, ngram_range=(1, 2))
    tfidf = vectorizer.fit_transform(content_list)
    nmf = NMF(n_components=n_topics, random_state=1, alpha=.1, l1_ratio=.5)
    transformed_docs = nmf.fit_transform(tfidf)
    feature_names = vectorizer.get_feature_names()
    n_top_words = 10
    for topic_idx, topic in enumerate(nmf.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    return vectorizer, nmf


def pkl(content,file_name):
    pkl_file = pickle.dumps(content)
    with open(file_name, 'w') as f:
        f.write(pkl_file)

def unpkl(file_name):
    with open(file_name, 'r') as f:
        unpkl_file = pickle.load(f)
    return unpkl_file

if __name__ == '__main__':
    data_file = sys.argv[1]
    max_df = sys.argv[2]
    min_df = int(sys.argv[3])
    max_features = int(sys.argv[4])
    n_topics = int(sys.argv[5])
    df = unpkl(data_file)
    content_list = df['text_p'].values
    print df['text_p'].head()
    vectorizer, nmf = model_nmf(content_list, max_df, min_df, max_features, n_topics)
    pkl(vectorizer,'vectorizer')
    pkl(nmf,'nmf')
