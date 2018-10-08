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
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from read_function import obtain_finance_tables, obtain_fixtures_tables
#from read_function import * 
#from action_functions import *
from action_functions import read_and_get_help_tables, get_free_tickets, login
from action_functions import select_lineup_next_match, logout, shutdown
from decision_making import analyse_improvement



####################################################### Start the browser
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


################################################### Confirm the cookie alert
time.sleep(6)
cookie_accept_button = driver.find_element_by_css_selector('.cc-btn')
cookie_accept_button.click()
time.sleep(2)


########################################################## Log into the game
login(driver)



##############################################################################
##############################################################################
################          To-do list          ################################
##############################################################################
##############################################################################

action_items = {'Read matches?' : False, 
        'Select lineup?' : False, 
        'Get free tickets?' : False, 
        'Read financial info?' : False, 
        'Get player\'s info?' : False,
        'Read player\'s info?' : False, 
        'Read facilities page?' : True,
        'Export help files?' :  False, 
        'Logout?' : False, 
        'Shutdown browser?' : False ,
        'Approve building improvement?' : False
        }

if action_items['Approve building improvement?'] == True and \
   action_items['Read financial info?'] == False:
      print('Warning: to approve a building improvement we MUST analyse' \
             ' the financial records. \nUpdating the action items list.')
      print('...')
      action_items['Read financial info?'] = True
      print('Action item list updated.')
    

######################################################### Read matches
if action_items['Read matches?']:
    # Go to the matches section
    time.sleep(3)
    myMatches_elem = driver.find_element_by_id('menu-entry-friendlies')
    myMatches_elem.send_keys(Keys.RETURN)
    
    # Read next matches
    table_upcoming , table_recent = obtain_fixtures_tables(driver)


######################################################### Set lineup
if action_items['Select lineup?']:
    # Go to the matches section
    time.sleep(3)
    myMatches_elem = driver.find_element_by_id('menu-entry-friendlies')
    myMatches_elem.send_keys(Keys.RETURN)
    # Select line-up ONLY for next match
    line_up_name = '1: first tactic'
    select_lineup_next_match(driver, line_up_name)


######################################################### Get free tickets
if action_items['Get free tickets?']:
    time.sleep(3)
    myMatches_elem = driver.find_element_by_id('menu-entry-friendlies')
    myMatches_elem.send_keys(Keys.RETURN)
    get_free_tickets(driver)



################################################ Read financial information
if action_items['Read financial info?']:
    time.sleep(3)
    finances_elem = driver.find_element_by_id('menu-entry-finances')
    finances_elem.click()
    balance_sheet_pd_table, account_table_pd = obtain_finance_tables(driver)
    
    
######################################### Get (download) players' information
if action_items['Get player\'s info?']:        
    time.sleep(3)
    players_elem = driver.find_element_by_id('menu-entry-players')
    players_elem.click()
    
    time.sleep(2)
    export_to_csv = driver.find_elements_by_class_name('submit')
    export_to_csv = export_to_csv[2]
    export_to_csv.click()


################################################ Read players' information
if action_items['Read player\'s info?']:
    time.sleep(3)

    ## Read csv file
    file_name = time.strftime('%Y_%m_%d') + '_players.csv'
    file_name = '2018_10_07_players.csv'
    try:
        players_data = pd.read_csv(file_name, sep=';')
    except FileNotFoundError:
        print('Player\'s file was not downloaded or not updated to today!' \
              ' Get player\'s information!')


########## NEEDS TO BE FINISHED FOR OTHER FACILITIES JUST DONE FOR STADIUM
######################################################## Read Facilities page        
if action_items['Read facilities page?']:
    time.sleep(3)
    facilities_elem = driver.find_element_by_id('menu-entry-facilities')
    facilities_elem.click()
    time.sleep(3)
    table = driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[2]/div' \
                                         '/div/div[4]/table/tbody')
    x = table.text
    n_lines = x.count('\n')
    table_lst = []
    for i in np.arange(0,n_lines):
        idx = x.find('\n')
        line = x[0:idx]
        line = line.split()
        table_lst.append([line[0],line[1],line[2]+line[3],line[-1]])
    
    facilities_table_pd = pd.DataFrame(data=table_lst, columns=['Building Type'
                                    , 'Level', 'Weekly Costs', 'State'])

    
    
######################################################## Export help files
# Export files from help page help/facilities 
if action_items['Export help files?']:
    time.sleep(3)
    help_elem = driver.find_element_by_id('menu-entry-help')
    help_elem.click()
    time.sleep(2)
    # Go to help/facilities
    facilities_help = driver.find_element_by_css_selector('ul.menu:nth-child(2) > li:nth-child(2) > a:nth-child(1)' )
    facilities_help.click()
    
    # Access tables and download them
    read_and_get_help_tables(driver)


############################################ Make decision for improvement
if action_items['Approve building improvement?']:
# Analyse if if we have budget to improve a certain building and if 
# weekly net budget is > 0 (without interest)
    time.sleep(3)
    building_name = 'Stadium.csv' # building's improvement
    approved_improvement, reason = analyse_improvement(building_name, 
                                                       account_table_pd, 
                                                       balance_sheet_pd_table)



############################################################### Logout 
if action_items['Logout?']:
    time.sleep(4)
    logout(driver)


###################################################### Shutdown web browser
if action_items['Shutdown browser?']:
    time.sleep(4)
    shutdown(driver)


    
    
    

