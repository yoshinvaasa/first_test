#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 21:30:07 2018

@author: haidin
"""

# FUNCTION WAS IMPLEMENTED SUCCESFULLY, THIS TEST FUNCTION IS NO LONGER 
# NECESSARY
# Test function for reading table and creating a dataframe for it


import pickle
import re
import pandas as pd
import numpy as np


##########################  Test
table_temp = table
n_lines = 6


# Process the "table_temp" variable
n_columns = len(table_temp[0].split())
table = [[] * n_columns] * n_lines
table[0] = table_temp[0].split()
column_names = table[0]

time_format = re.compile('.{2}:.{2}')
# initialise table as dataframe (pandas)
table_pd = pd.DataFrame(columns = column_names)
for i in np.arange(1,n_lines):
    
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
    tournament_column = line[j_venue+1:-1]
    action_column = line[-1]
    
    line_dataframe = pd.DataFrame(data=[[time_column,opponent_column,
                        venue_column,tournament_column,action_column]],
                        columns = column_names)

    # Add info to the table
    table_pd = table_pd.append(line_dataframe)

    
    
    
    
    
    
    