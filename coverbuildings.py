# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 14:10:47 2024

@author: amand
"""

from ortools.sat.python import cp_model
import ortools

""" Problem 3 : Given N rectangular buildings of width 1, find the minimum total area
of two banners that cover all the buildings. """


# Question: What is the width of the first banner?


model = cp_model.CpModel()

heights = [3, 1, 4] 
banner1_width = model.NewIntVar(1, len(heights), "banner 1 width")
banner1_height = model.NewIntVar(1, max(heights), "banner 1 height")
banner2_width = model.NewIntVar(0, len(heights), "banner 2 width")
model.Add(banner2_width == len(heights)-banner1_width) 
banner2_height = model.NewIntVar(0, max_height, "banner 2 height")                         