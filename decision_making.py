#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 22:09:03 2018

@author: haidin
"""

import numpy as np
import pandas as pd

def analyse_improvement(building_name, current_level, account_table_pd, 
                        balance_sheet_pd_table):
    # Analyse if improvement can be supported within current budget and if
    # net weekly budget is > 0 after improvement
    #
    # Inputs:
    #       - building_name: name of the building to analyse improvement
    
    # Adjust for csv file if necessary
    if building_name in ['Catering','Fanshop','Museum','Office','Stadium']:
        building_filename = building_name + '.csv'
    else:
        building_filename = building_name
    
    
    ac_t_pd = account_table_pd
    
    weekly_income = ac_t_pd['Weekly (€)'][:-1].sum() #don't include total
    weekly_costs = ac_t_pd['Weekly_ (€)'][:-1].sum() #don't include total
    weekly_interest = ac_t_pd.loc[8, 'Weekly (€)']
    
    weekly_net = weekly_income - weekly_costs
    weekly_net_without_interest = weekly_net - weekly_interest
    
    # Import corresponding building information
    
    
    buildings = ['Catering.csv','Fanshop.csv','Health','Museum.csv','Office.csv'
                 ,'Scout\'s', 'Stadium.csv', 'Training', 'Youth']
    i = buildings.index(building_filename)
    
    building = buildings[i]
    
    bd = pd.read_csv('./Data files/' + building, sep=';') # building data
    # Make correction to the table
    if building in ['Training', 'Youth']:
    # 'Youth' or building == 'Training':
        bd.loc[np.arange(10,16), 'Level'] = np.arange(11,17)
    
    
    
    #################### Make decision
    # do we have positive net after improving a certain building
    
    next_level_weekly_cost = bd.loc[current_level, 'Weekly costs'] # current_level 
    #is correct, because of indexing
    
    updated_weekly_net = weekly_net - next_level_weekly_cost
    updated_weekly_net_without_interest = weekly_net_without_interest - next_level_weekly_cost
    
    balance = balance_sheet_pd_table.loc[2,'Value (€)'] # current balance 
    cost_improvement = bd.loc[current_level, 'Construction costs']
    updated_balance = balance - cost_improvement
    
    if updated_weekly_net_without_interest > 0 and updated_balance > 0:
        approved_improvement = True
        reason = []
    
    elif updated_balance < 0:
        approved_improvement = False
        reason = 'Not enough balance'
    
    elif updated_weekly_net_without_interest < 0:
        approved_improvement = False
        reason = 'Weekly net will be negative'    
    
    elif updated_weekly_net_without_interest < 0 and updated_balance < 0: 
        approved_improvement = False
        reason = 'Negative net and negative balance'
        
    
    return approved_improvement, reason, weekly_net, updated_weekly_net_without_interest
        
