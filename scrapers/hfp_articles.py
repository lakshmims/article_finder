import json
from bs4 import BeautifulSoup
import urllib2
from time import sleep
import requests
import sys


def get_stories(url_file_path, story_file_path):
    urls = []
    with open(file_path,'r') as f:
        for line in f:
            urls.append(line.strip('\n'))

    for story_url in urls:

        story_file_name = ''
        story_text_all = ''
        try:
            response = requests.get(story_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            story_topic = soup.find_all("meta", { "property" : "article:section", "content" : "Politics"})

            #get stories from category "Politics"
            if len(story_topic) > 0:
                story_text_all = soup.find_all("div", { "class" : "content-list-component text" })[0].text
                story_file_name = story_url[story_url.rfind('/')+1:story_url.rfind('.html')]
                story_title = soup.find_all('title', {'class': ''})[0].string.strip()
                story_date = soup.find_all('span',{'class':'timestamp__date--published'})[0].text
                story_date = story_date[0:10].replace('/','')

            if len(story_file_name)>0 and len(story_text_all)>0:
                file_url = story_file_path + story_file_name
                file_content = { 'url':story_url, 'title':story_title, 'date':story_date, 'content':story_text_all}
                with open(file_url,'w') as f:
                    f.write(json.dumps(file_content))
        except:
            print 'error. could not get story', story_url

        sleep(1)


if __name__ == '__main__':
    print 'getting stories'
    file_path = sys.argv[1]
    get_stories(url_file_path, story_file_path)
    print 'done!'
