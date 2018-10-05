#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 22:50:08 2018

@author: haidin
"""

import numpy as np
import time
from selenium import webdriver

def obtain_fixtures_tables(driver):
    # From the page "fixtures" the function reads the 2 tables (upcoming and past games)
    # and saves the in 2 variables, table and table2
    #
    # Inputs: driver, in the "fixtures" page
    # Outputs: table,table2, 2 list variables with the upcoming and past fixtures
    
    
    time.sleep(4)
    two_tables = driver.find_elements_by_class_name('horizontal_table')
    next_10_matches_table = two_tables[0]
    last_10_matches_table = two_tables[1]

    x = next_10_matches_table.text
    n_lines = x.count('\n')
    table = list()
    
    for i in np.arange(0,n_lines):
        idx = x.find('\n')
        line = x[0:idx]
        table = [table , line]
        x = x[idx+1:]
        
    y = last_10_matches_table.text
    n_lines = y.count('\n')
    table2 = list()
    
    for i in np.arange(0,n_lines):
        idx = y.find('\n')
        line = y[0:idx]
        table2 = [table2 , line]
        y = y[idx+1:]
        
    return table,table2
