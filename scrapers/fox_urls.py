import re
import json
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver


def get_story_urls(driver, file_path, num_pages):
    article_pages = []
    for page in xrange(0,num_pages*10,10):
        url = 'http://www.foxnews.com/search-results/search?q=a&ss=fn&sort=latest&section.path=fnc/politics,fnc/us,fnc/world&start='
        url = url+str(page)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        article_pages.extend(soup.find_all('a',{'class':'ng-binding', 'ng-bind':'article.title'}))
        sleep(1)

    with open(file_path,'w') as f:
        for row in article_pages:
            f.write(row['href'].encode('utf8')+'\n')


if __name__ == '__main__':
    file_path = sys.argv[1]
    num_pages = sys.argv[2]
    driver = webdriver.Firefox()
    print 'getting urls'
    get_story_urls(driver, file_path, num_pages)
    print 'done!'
