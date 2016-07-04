import json
from bs4 import BeautifulSoup
import feedparser
import urllib2
import re
from time import sleep
import requests
from datetime import datetime, timedelta
from cookielib import CookieJar
from selenium import webdriver
import sys


def get_urls(driver, file_path, num_pages):
    urls = []
    for page in xrange(0, num_pages):
        search_url1 = """http://query.nytimes.com/search/sitesearch/?action=click&region=Masthead&pgtype=SectionFront&module=SearchSubmit&contentCollection=us&t=qry461#/*/30days/document_type%3A%22article%22/"""
        search_url2 = """/allauthors/newest/US/"""
        url = search_url1 + str(page) + search_url2
        driver.get(url)
        driver.implicitly_wait(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        result_urls = soup.find('div', {'class': 'searchResults'})
        x = result_urls.find_all('a')
        for item in x:
            urls.append(item.attrs['href'])
            print 'url: ', item.attrs['href']
        urls_s = list(set(urls))

        with open(file_path, 'a') as f:
            for row in urls_s:
                f.write(row.encode('utf8')+'\n')
        sleep(1)


if __name__ == '__main__':
    driver = webdriver.Firefox()
    url_file_path = sys.argv[1]
    num_pages = sys.argv[2]
    print 'getting urls'
    get_urls(driver,url_file_path,num_pages)
    print 'done!'
