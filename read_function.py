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


def obtain_finance_tables(driver):
    # Function that given a driver in the "finances" page 
    # goes reads both tables given there and returns dataframe tables
    # for those 2 tables
    
    tables = driver.find_elements_by_tag_name('table')
    balance_sheet_table = tables[0].text
    account_table = tables[1].text
    
    ############################### Read 1st table, "Balance Sheet" table
    # Read the data and Create the structure
    table_temp = []
    n_lines = balance_sheet_table.count('\n')
    for i in np.arange(0,n_lines):
        idx = balance_sheet_table.find('\n')
        line = balance_sheet_table[0:idx]
        table_temp.append(line)
        balance_sheet_table = balance_sheet_table[idx+1:]
    
    table_temp.append(balance_sheet_table)
    
    balance_sheet_pd_table = pd.DataFrame()    
    data1_1 = table_temp[1][0:20]
    data1_2 = table_temp[1][21:]
    data2_1 = table_temp[2][0:11]
    data2_2 = table_temp[2][12:]
    data3_1 = table_temp[3][0:15]
    data3_2 = table_temp[3][16:]
    line1 = pd.DataFrame(data=[[data1_1,data1_2],[data2_1,data2_2],[data3_1,data3_2]])
    balance_sheet_pd_table = balance_sheet_pd_table.append(line1)
    
    # Make it nicer looking, with integer variables for the values
    x = pd.Series(data=balance_sheet_pd_table[1])

    for i in np.arange(0,len(x)):
        y = x[i]
        y = y[2:]
        y = y.replace(" ","")
        x[i] = int(y)
    
    balance_sheet_pd_table[1] = x
    balance_sheet_pd_table.columns = ['Type','Value (€)']

    
    
    ##################################### Read 2nd table, "Accounts" table
    # Read the data and Create the structure
    n_lines = account_table.count('\n')+1
    table_temp = []
    for i in np.arange(0,n_lines):
        idx = account_table.find('\n')
        line = account_table[0:idx]
        table_temp.append(line)
        account_table = account_table[idx+1:]
        
    line1_data = [table_temp[0],'','','']
    line2_data = [table_temp[1].split()[0] , '', table_temp[1].split()[1], '']
    
    account_table_pd = pd.DataFrame(data=[line1_data])
    account_table_pd = account_table_pd.append(pd.DataFrame(data=[line2_data]))
    
    for i in np.arange(2,n_lines):
        line = table_temp[i]
        idx_euro_sign = line.find('€')
        col1 = line[0:idx_euro_sign-1]
        line_without_1st_column = line[idx_euro_sign:]
        #line_without_1st_column = line_without_1st_column.split()
        
        for j in np.arange(0,len(line_without_1st_column)):
            if line_without_1st_column[j].isupper():
                idx_upper_case = j
                break
        
        col2 = line_without_1st_column[0:idx_upper_case]
        
        line_last_2_cols = line_without_1st_column[idx_upper_case:] 
        idx_euro_sign2 = line_last_2_cols.find('€')
        col3 = line_last_2_cols[0:idx_euro_sign2]
        col4 = line_last_2_cols[idx_euro_sign2:]
        
        line_pd_data = pd.DataFrame(data=[[col1,col2,col3,col4]])
        account_table_pd = account_table_pd.append(line_pd_data)
        
        
    x = account_table_pd 
    x.index = np.arange(0,10)
    x.columns = ['Type', 'Amount ()', 'Type2', 'Amount2 ()']
    col2_3 = pd.DataFrame( x['Amount ()'].str.split('(',1).tolist() )
    col5_6 = pd.DataFrame(x['Amount2 ()'].str.split('(',1).tolist())
    x = pd.concat([x['Type'],col2_3, x['Type2'],col5_6],axis=1)
    x.columns = ['Income', 'Amount (€)','Weekly (€)', 
                 'Expense', 'Amount2 (€)','Weekly_ (€)']
    
    y = x[x.columns[1]]
    for i in np.arange(0,len(y)):
        if len(y[i]) > 0:
            y[i] = y[i].replace(' ','')
            y[i] = y[i].replace('€','')
            y[i] = int(y[i])
            
    
    y = x[x.columns[4]]
    for i in np.arange(0,len(y)):
        if len(y[i]) > 0:
            y[i] = y[i].replace(' ','')
            y[i] = y[i].replace('€','')
            y[i] = int(y[i])
    
    y = x[x.columns[-1]]
    for i in np.arange(0,len(y)):
        if y[i] is not None:
            y[i] = y[i].replace(')','')
            y[i] = y[i].replace('€','')
            y[i] = y[i].replace(' ','')
            y[i] = int(y[i])
    
    
    y = x[x.columns[2]]
    for i in np.arange(0,len(y)):
        if y[i] is not None:
            y[i] = y[i].replace(')','')
            y[i] = y[i].replace('€','')
            y[i] = y[i].replace(' ','')
            y[i] = int(y[i])

    account_table_pd = x
    
    return balance_sheet_pd_table, account_table_pd






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