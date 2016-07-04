import json
import re
from time import sleep
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from time import sleep
import requests
import sys

def get_story_urls(url_file_path, end_date, num_days):
    story_urls = []
    story_docs = []
    archive_page_urls = []
    dayless = timedelta(days=1)
    new_date = end_date

    #get list of archive pages
    for i in xrange(num_days):
        day = new_date.day
        month = new_date.month
        url = "http://www.huffingtonpost.com/archive/2016-{}-{}".format( month , day)
        archive_page_urls.append(url)
        new_date = new_date-dayless

#get article urls
article_urls = []
for url in archive_page_urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    x = soup.find_all('a',{ "class" : "" })
    y = [link["href"] for link in x if "/2016/" in link["href"] ]
    article_urls.extend(y)
    sleep(1)

z = list(set(article_urls))
story_urls = [url for url in z if url.find('ir=Entertainment')==-1 and url.find('ir=Green')==-1]

with open(url_file_path,'w') as f:
    for row in story_urls:
        f.write(row.encode('utf8')+'\n')



if __name__ == '__main__':
    url_file_path = sys.argv[1]
    # end date in the format 'Jun 30 2016'
    end_date_str = sys.argv[2]
    datetime.strptime(end_date_str, '%b %d %Y')
    print 'login successful'
    print 'getting urls'
    get_story_urls(url_file_path, end_date, num_days)
    print 'done!'
