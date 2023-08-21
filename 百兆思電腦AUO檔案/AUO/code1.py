# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 15:31:08 2023

@author: Admin
"""

import random

def fun(raw_data):
    upper_limit=[1,1,1,1,1,1,1,1,1,1,1,1]
    lower_limit=[0,0,0,0,0,0,0,0,0,0,0,0]
    counter =0
    for i in range(len(raw_data)):
        if(raw_data[i]>upper_limit[i] or raw_data[i] < lower_limit[i]):
            counter+=1
    Anomaly=counter*5
    random_float = random.uniform(0.0, 100.0)
    rounded_float = round(random_float, 2)
    if(rounded_float>30.0 and rounded_float<35.0):
        return round(random.uniform(0.0,6.0), 0)
    else:
        return round(random.uniform(0.0,3.0), 0)