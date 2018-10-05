#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 21:32:10 2018

@author: haidin
"""

""" Creating bot using selenium. Login, logout and shutdown functionalities 
    operative. Creating reading functions to access the data in the website, 
    and to structure the data into readable format. """

import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from read_function import obtain_fixtures_tables
from action_functions import *

# Create driver and give url address
driver = webdriver.Firefox()
url= 'https://rockingsoccer.com/en/soccer'
driver.get(url)
assert "Rocking Soccer" in driver.title


# Log into the game
login(driver)


# Go to next match
time.sleep(1.5)
myMatches_elem = driver.find_element_by_id('menu-entry-friendlies')
myMatches_elem.send_keys(Keys.RETURN)
#next_game_elem = driver.find_element_by_class_name('lineup-link')
#next_game_elem.send_keys(Keys.RETURN)


# Read next matches
table,table2 = obtain_fixtures_tables(driver)


# Logout and shutdown web browser
logout(driver)
shutdown(driver)















# Python function syntax 
#def function_name(arguments):
#    
#    
#    return outputs