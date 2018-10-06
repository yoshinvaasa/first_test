#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 22:50:08 2018

@author: haidin
"""

import numpy as np
import time
from selenium import webdriver
import pandas as pd
import pickle
import re

# Modifications done, data output is now in pandas dataframe type, 
# as a table

# Implementation is slightly different for the 2 read tables from the website
# corresponding to the next 10 and last 10 matches, due to 
# different original tables


def obtain_fixtures_tables(driver):
    # From the page "fixtures" the function reads the 2 tables (upcoming and past games)
    # and saves the in 2 variables, table and table2
    #
    # Inputs: driver, in the "fixtures" page
    # Outputs: table,table2, 2 dataframe variables with the upcoming 
    #          and past fixtures
    
    
    time.sleep(4)
    two_tables = driver.find_elements_by_class_name('horizontal_table')
    next_10_matches_table = two_tables[0]
    last_10_matches_table = two_tables[1]

    # Create tables
    table_pd = create_pd_table(next_10_matches_table,False)
    table_pd2 = create_pd_table(last_10_matches_table,True)
    
    
    return table_pd, table_pd2





def create_pd_table(original_table,past_10):
    # Function that takes original_table from the website and returns
    # a dataframe variable for that table
    # "past_10" is a boolean variable to idenfity if the input table
    # is for the next 10 matches (past_10 = False) or for the last 10 
    # matches (past_10 = True)
    
    x = original_table.text
    n_lines = x.count('\n')
    table_temp = [] # initialise a list
    
    # Extract first the lines
    
    for i in np.arange(0,n_lines):
        idx = x.find('\n')
        line = x[0:idx]
        table_temp.append(line)
        x = x[idx+1:]
    table_temp.append(x)
        
    
    # Extract the lines 1-by-1 to create a table (dataframe)
    n_columns = len(table_temp[0].split())
    table = [[] * n_columns] * n_lines
    table[0] = table_temp[0].split()
    column_names = table[0]
    
    time_format = re.compile('.{2}:.{2}')
    # initialise table as dataframe (pandas)
    table_pd = pd.DataFrame(columns = column_names)
    for i in np.arange(1,n_lines+1):
        
        line = table_temp[i].split()
        
        for j in np.arange(0,len(line)):
            if time_format.match(line[j]):
                # we found the time column
                j_time = j
                break
                
        # find the venue column index
        if 'Home' in line:
            j_venue = line.index('Home')
        elif 'Away' in line:
            j_venue = line.index('Away')
        else:
            raise ValueError('Cannot find the venue in the fixture table')
            
                
        time_column = line[0:j_time+1]
        opponent_column = line[j_time+1:j_venue]
        venue_column = line[j_venue]
        
        
        if past_10:
            result_column = line[j_venue+1]
            points_column = line[j_venue+2]
            tournament_column = line[j_venue+3:-1]
            line_dataframe = pd.DataFrame(data=[[time_column,opponent_column,
                            venue_column,result_column, points_column, 
                            tournament_column]],
                            columns = column_names)
            
        else:
            action_column = line[-1]
            tournament_column = line[j_venue+1:-1]
            line_dataframe = pd.DataFrame(data=[[time_column,opponent_column,
                            venue_column,tournament_column,action_column]],
                            columns = column_names)
            

        # Add info to the table
        table_pd = table_pd.append(line_dataframe) 
        
    # Table has been created :D
    return table_pd