# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 11:58:21 2024

@author: amand
"""

from ortools.sat.python import cp_model
import ortools


""" PROBLEM 1 : Arrange rectangles into a strip """

# rectangle sizes
"""
A = [2, 3, 2, 3, 5] # height
B = [3, 4, 2, 4, 2] # width
"""

A = [2, 10, 4, 1, 4] # height
B = [4, 1, 2, 2, 5] # width

""" Maximization Problem -> the solver will arrange the rectangles so that we can fit the most 
rectangle sof the same height into the same strip. """

# define the model 
model = cp_model.CpModel()

strip_height = model.NewIntVar(1, 1000000000, "strip height") 
# I don't know what this value is, but I want the solver to choose it for me.  
# strip height = name of variable 

""" Next we need to tell the program whether we want to include a rectangle in a strip, 
and whether that strip will be rotated or not. We want the model to keep track of this 
information and return the most optimal configuration. """ 

# list that will keep track of all the chosen boolean variables. 
in_strip_vars = []
# keep track of whether the rectangle was rotated or not 
rotated_in_strip_vars = []

# 1) Define the constraints 

for i, a in enumerate(A):
    in_strip_vars.append(model.NewBoolVar("rectangle %d in strip" % i))
    rotated_in_strip_vars.append(model.NewBoolVar("rectangle %d rotated in strip" % i))
    model.Add(A[i]==strip_height).OnlyEnforceIf(in_strip_vars[i]) # only pick A as the height
    # if in_strip_vars is True for this rectangle -> constraint that is conditional depending 
    # on the value of a boolean variable 
    model.Add(B[i]==strip_height).OnlyEnforceIf(rotated_in_strip_vars[i]) # only pick B as the height 
    # if the rectangle is rotated 

# 2) Define the objective of the optimization problem   
""" We add up the sum of the booleans -> The higher the value then the more rectangles 
that have been chosen in the strip. """

# Don't stop searching until you find the absolute number of booleans that can be True. 
model.Maximize(sum(in_strip_vars + rotated_in_strip_vars)) # count the number of true booleans 

solver = cp_model.CpSolver() 
#solver.parameters.log_search_progress = True 
status = solver.Solve(model)


if status == cp_model.OPTIMAL:
    for i in range(len(A)):
        if solver.Value(in_strip_vars[i]):
            print("In strip: %d x %d" % (B[i], A[i]))
        elif solver.Value(rotated_in_strip_vars[i]):
            print("In strip rotated: %d x %d" % (A[i], B[i]))