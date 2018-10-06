#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 21:38:57 2018

@author: haidin
"""

import pickle

# Quick demonstration on how to save variables in a file 


f = open('table.pckl','rb')
table = pickle.load(f)
f.close()

    
f = open('two_tables.pckl','wb')
pickle.dump(two_tables,f)
f.close()
#