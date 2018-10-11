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
from read_function import read_players_info, read_facilities
#from read_function import * 
#from action_functions import *
from action_functions import read_and_get_help_tables, get_free_tickets, login
from action_functions import select_lineup_next_match, logout, shutdown
from action_functions import get_players_info
from decision_making import analyse_improvement



####################################################### Start the browser
# For downloading automatically
profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2) # custom location
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', '/home/haidin/Desktop/Test/first_test/Data files')
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
        'Get player\'s info?' : False, # need to read players info in case it doesnt exist
        'Read player\'s info?' : False, 
        'Read facilities page?' : False,
        'Export help files?' :  False, 
        'Logout?' : False, 
        'Shutdown browser?' : False ,
        'Approve building improvement?' : False
        }

x = action_items['Approve building improvement?']
y = action_items['Read financial info?']
z = action_items['Read facilities page?']


if  x == True and  (y == False or  z == False):
      print('Warning: to approve a building improvement we MUST analyse' \
             ' the financial records and read current facilities information. ' 
             '\nUpdating the action items list.' )
      print('...')
      action_items['Read financial info?'] = True
      action_items['Read facilities page?'] = True
      print('Action item list updated.')
      
time.sleep(3)
    

######################################################### Read matches
if action_items['Read matches?']:
    # Read next matches
    table_upcoming , table_recent = obtain_fixtures_tables(driver)


######################################################### Set lineup
if action_items['Select lineup?']:
    # Select line-up ONLY for next match
    line_up_name = '1: first tactic'
    select_lineup_next_match(driver, line_up_name)


######################################################### Get free tickets
if action_items['Get free tickets?']:
    # Get free tickets
    get_free_tickets(driver)



################################################ Read financial information
if action_items['Read financial info?']:
    balance_sheet_pd_table, account_table_pd = obtain_finance_tables(driver)
    
    
######################################### Get (download) players' information
# need to delete already existing file
if action_items['Get player\'s info?']:     
    get_players_info(driver)
    

################################################ Read players' information
if action_items['Read player\'s info?']:
    players_data = read_players_info(driver)
    
    
########## TEST FOR OTHER FACILITIES JUST DONE FOR STADIUM
######################################################## Read Facilities page        
if action_items['Read facilities page?']:
    facilities_table_pd = read_facilities(driver)
    
    
    
######################################################## Export help files
# Export files from help page help/facilities 
if action_items['Export help files?']:
    # Access tables and download them
    read_and_get_help_tables(driver)


############################################ Make decision for improvement
if action_items['Approve building improvement?']:
# Analyse if if we have budget to improve a certain building and if 
# weekly net budget is > 0 (without interest)
    building_name = 'Training'    
        
    current_level = facilities_table_pd[facilities_table_pd['Building Type']==building_name]['Level']
    
    if len(current_level) == 0: # such building does not exist
        current_level = 0
    elif len(current_level) > 0: 
        current_level = current_level[0]
        
    
    approved_improvement, reason, week_net, updt_w_net = analyse_improvement(
                                                    building_name, 
                                                       current_level,
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


    
    
    

