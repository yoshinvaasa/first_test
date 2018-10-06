#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 22:54:13 2018

@author: haidin
"""

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from credentials import get_credentials


def get_free_tickets(driver):
    time.sleep(3)
    free_tickets_elem = driver.find_element_by_class_name("tickets-link")
    free_tickets_elem.send_keys(Keys.RETURN)
    
    # Identify buy button (to get the free ticket) and select it


def select_lineup_next_match(driver, line_up_name):
    # Function takes the driver and selects next line-up from a set 
    # of given line-ups
    # Only does if the next match lineup hasn't been selected
    
    # 1 things need to corrected: 
    # 2. in the case that there are no matches to select the lineup
    
    next_selected_lineup = False;
    
    time.sleep(1.5)
    myMatches_elem = driver.find_element_by_id('menu-entry-friendlies')
    myMatches_elem.send_keys(Keys.RETURN)
    
    # Check whether lineup for next match is set or not
    next_game_elem = driver.find_element_by_class_name('lineup-link')
    img_next_game = next_game_elem.find_elements_by_xpath(".//*")[0] # get the icon
    x = img_next_game.get_property('src')    
    if 'lineup-done' in x:
        next_selected_lineup = True
    
    
    
    # Select line-up for next match, in case not yet selected
    # Go to "matches" section
    if next_selected_lineup == False:
        
        
        # Select next match
        next_game_elem = driver.find_element_by_class_name('lineup-link')
        next_game_elem.send_keys(Keys.RETURN)
        
        time.sleep(2)
        
#        load_lineup_elem = driver.find_element_by_name('load_lineup') # not necessary anymore
        load_lineup_elem2 = driver.find_elements_by_tag_name('option')
        for option in load_lineup_elem2:
            if option.text == line_up_name:
                print('found it!!!')
                option.click()
                break
        
        time.sleep(1)
        submit_chosen_lineup_elem = driver.find_element_by_class_name('submit')
        submit_chosen_lineup_elem.click()
        
        
        
        
def login(driver):
    # Login function
    #
    # Input: driver, in the main page of rocking soccer
    time.sleep(1)
    username_elem = driver.find_element_by_name('username')
    password_elem = driver.find_element_by_name('password')
    #login_elem = driver.find_element_by_name('login')
    
    
    username,password = get_credentials()
    username_elem.send_keys(username)
    time.sleep(1)
    password_elem.send_keys(password)
    time.sleep(1)
    password_elem.send_keys(Keys.RETURN)


# Logout of the game
def logout(driver):
    # Logout function
    #
    # Input: driver in whatever page, it can logout automatically
    
    time.sleep(3)
    logout_elem = driver.find_element_by_class_name('logout')
    logout_elem.send_keys(Keys.RETURN)


# Shutdown the driver
def shutdown(driver):
    # Close the web driver
    time.sleep(1)
    driver.quit()