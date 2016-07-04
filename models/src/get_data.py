from __future__ import unicode_literals
import os
import re
import nltk
import json
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tag import pos_tag
import sys
import pickle

def load_data(folder, sub_dirs):
    files = []
    for subdir in subdirs:
        for file in os.listdir(folder + '/' + subdir + '/'):
            file_path = folder + '/' + subdir+'/' + file
            with open(file_path, 'r') as f:
                for line in f:
                    try:
                        row = json.loads(line)
                        row['source'] = subdir
                        files.append(row)
                    except:
                        print 'error could not load file' , file_path

        df =  pd.DataFrame(files)
        df['title'] = df['title'].astype(unicode)
        df['text'] = df['title'].astype(unicode) + df['content'].astype(unicode)
        df['pub_date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        df['text_p'] = process_text(df['text'])
        return df

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

def pkl(content,file_name):
    pkl_file = pickle.dumps(content)
    with open(file_name, 'w') as f:
        f.write(pkl_file)


if __name__ == '__main__':
    folder = sys.argv[1]
    sub_dirs = sys.argv[2]
    file_name = sys.argv[3]
    df = load_data(folder, sub_dirs)
    pkl(df,file_name)
