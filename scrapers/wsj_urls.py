import os
import sys
import re
import json
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver

def wsj_login(username,password):
    url = 'https://id.wsj.com/access/pages/wsj/us/signin.html?url=http%3A%2F%2Fwww.wsj.com&mg=id-wsj'
    driver = webdriver.Firefox()
    driver.get(url)

    user = driver.find_element_by_name('username')
    user.click()
    user.send_keys(username)

    pwrd = driver.find_element_by_name('password')
    pwrd.click()
    pwrd.send_keys(password)

    driver.find_element_by_id('submitButton').click()
    sleep(10)
    return driver

def get_story_urls(driver,file_path, num_pages):
    article_urls = []
    #search for all stories in the last 30 days
    search_url = 'http://www.wsj.com/search/term.html?KEYWORDS=a&min-date=2016/06/01&max-date=2016/06/30&isAdvanced=true&daysback=90d&andor=AND&sort=date-desc&source=wsjarticle&page='

    for page in xrange(0,num_pages):
        try:
            search_url = search_url+str(page)
            driver.get(search_url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            x = soup.find_all(re.compile('a.*\:a'),{"class":""})
            y = [item['href'] for item in x]

            #get stories only, ignore videos and slideshows
            z = ["www.wsj.com"+(link) for link in y if "/articles/" in link]
            article_urls.extend(z)
            sleep(1)
        except:
            print "error. could not get page{}".format(page) , search_url


    # save urls to file
    with open(file_path,'w') as f:
        for row in z:
            f.write(row.encode('utf8')+'\n')


if __name__ == '__main__':
    username = os.environ['WSJ_USER_ID']
    password = os.environ['WSJ_PASSWORD']
    file_path = sys.argv[1]
    num_pages = sys.argv[2]
    driver = wsj_login(username,password)
    print 'login successful'
    print 'getting urls'
    get_story_urls(driver, file_path,num_pages)
    print 'done!'
