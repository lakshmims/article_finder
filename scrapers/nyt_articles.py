import json
from bs4 import BeautifulSoup
import feedparser
import urllib2
import re
from time import sleep
import requests
from datetime import datetime, timedelta
from cookielib import CookieJar

def get_stories(url_file_path,story_file_path):
    urls = []
    with open(url_file_path,'r') as f:
        for line in f:
            if ("/2016/" in line) and ("/politics/"  in line) and ("www.nytimes.com/" in line):
                urls.append(line.strip('\n'))

    cj = CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    for story_url in urls:
        story_file_name = ''
        story_text_all = ''
        try:
            page = opener.open(story_url)
            story = page.read()
            soup = BeautifulSoup(story,'html.parser')
            story_title = soup.find_all('title', {'class': ''})[0].string.strip()
            story_title = story_title.rstrip(' - The New York Times')
            story_date = soup.find_all('meta',{'name':'pdate'})[0].attrs['content']
            story_body = soup.find_all("p", { "class" : "story-body-text story-content" })
            story_text = []
            for snippet in story_body:
                html = str(snippet)
                soup_s = BeautifulSoup(html,'html.parser')
                story_text.append(soup_s.getText().encode("UTF-8"))
            story_text_all = ''.join(story_text)
            story_file_name = story_url[story_url.rfind('/')+1:-5]

            if len(story_file_name)>0 and len(story_text_all)>0:
                file_url =  story_file_path + story_file_name
                file_content = { 'url':story_url, 'title':story_title, 'date':story_date, 'content':story_text_all}
                with open(file_url,'w') as f:
                    f.write(json.dumps(file_content))
        except:
            print 'error. could not get story:',story_url

        sleep(1)

if __name__ == '__main__':
    url_file_path = sys.argv[1]
    story_file_path = sys.argv[2]
    print 'getting stories'
    get_stories(url_file_path,story_file_path)
    print 'done!'
