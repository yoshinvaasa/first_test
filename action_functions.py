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

def login(driver):
    # Login function
    #
    # Input: driver, in the main page of rocking soccer
    
    username_elem = driver.find_element_by_name('username')
    password_elem = driver.find_element_by_name('password')
    #login_elem = driver.find_element_by_name('login')
    
    
    username,password = get_credentials()
    username_elem.send_keys(username)
    password_elem.send_keys(password)
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