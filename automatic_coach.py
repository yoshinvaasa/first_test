#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 21:39:11 2018

@author: haidin
"""

""" Abandoned: problem with login with post method using 
               requests library """

import requests
import time
from lxml import html
import urllib
from bs4 import BeautifulSoup as soup
from credentials import get_credentials

url = "https://rockingsoccer.com/en/soccer/"
url2 = "https://rockingsoccer.com/en/soccer/facilities"
#
#username = 'yashar2'
#password = 'em94p2B*"K,B"9F#I.p3g1H('
#
#response = requests.get(url, auth=(username, password), verify=False)
#
#page = soup(response.text)
#
#txt = page.find('textarea', id="text").string

#login = s.get(url)

#time.sleep(2)

username, password = get_credentials()

payload = {'username': username, 
          'password': password,
          'persistent': '1'  # remember me
          }


session = requests.session()
r = requests.post(url, data=payload)
print(r.cookies)

time.sleep(1)
          
page = session.get(url2)


print(page.text)

##r1 = requests.get(url, params=values)
#
#tree = html.fromstring(r1.content)
#
##time.sleep(2)
#
#
#r = requests.post(url,data=payload)

#print(r.text)



#tree2 = html.fromstring(r.content)


# Use 'with' to ensure the session context is closed after use.
#with requests.Session() as s:
#    p = s.post(url, data=payload)
#    # print the html returned or something more intelligent to see if it's a successful login page.
#    print(p.text)
#
#    # An authorised request.
#    r = s.get(url)
#    #print(r.text)
#        # etc...


#r1 = requests.get(url)


#url = 'https://www.coursera.org/?authMode=login'




#values = {'username': 'liverpool23', 
#          'password': 'ion24nbweiw'}


#

# dir(r)

#print(r.text)

#page_soup = soup(r.content)

#print(page_soup.text)

