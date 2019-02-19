#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 18:47:54 2019

@author: johannes
"""

f = open("MissionPlan/Stage_1_Attack.txt");
line = f.readlines()[1]
waypoint = line.split(";")
del waypoint[-1] # delete last element with new line command        
print(waypoint)
        
f.close()