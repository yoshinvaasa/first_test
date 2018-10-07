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
from read_function import * 
from action_functions import *


# For downloading automatically
profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2) # custom location
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', '/home/haidin/Desktop/Test/first_test')
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/csv,text/csv')


# Create driver and give url address
driver = webdriver.Firefox(profile)
url= 'https://rockingsoccer.com/en/soccer'
driver.get(url)
assert "Rocking Soccer" in driver.title



# Log into the game
login(driver)

# Go to the matches section
time.sleep(3)
myMatches_elem = driver.find_element_by_id('menu-entry-friendlies')
myMatches_elem.send_keys(Keys.RETURN)

# Read next matches
table_upcoming , table_recent = obtain_fixtures_tables(driver)


# Select line-up ONLY for next match
#line_up_name = '1: first tactic'
#select_lineup_next_match(driver, line_up_name)

# Get free tickets
#myMatches_elem = driver.find_element_by_id('menu-entry-friendlies')
#myMatches_elem.send_keys(Keys.RETURN)
#get_free_tickets(driver)



######################### Read financial information
time.sleep(3)
finances_elem = driver.find_element_by_id('menu-entry-finances')
finances_elem.click()
balance_sheet_pd_table, account_table_pd = obtain_finance_tables(driver)


####################### Read players' information
time.sleep(3)
finances_elem = driver.find_element_by_id('menu-entry-players')
finances_elem.click()

# players_data = download_and_read_players_data(driver)
time.sleep(3)
cookie_accept_button = driver.find_element_by_css_selector('.cc-btn')
cookie_accept_button.click()
    
time.sleep(2)
export_to_csv = driver.find_elements_by_class_name('submit')
export_to_csv = export_to_csv[2]
export_to_csv.click()

# Read csv file
file_name = time.strftime('%Y_%m_%d') + '_players.csv'
players_data = pd.read_csv(file_name, sep=';')


# Logout and shutdown web browser
logout(driver)
shutdown(driver)


    
    
    

