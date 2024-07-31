# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 13:21:57 2024

@author: amand
"""

from ortools.sat.python import cp_model
import ortools

""" Problem 2 : Given a set of points on a cartesian place, find the maximum 
distance between some pair of them to maximise another metric. The objective is to
find the largest possible distance d that allows them to spread out within overlapping 
each other. """

# x-y positions of the sheep
xs = [0, 0, 10, 10]
ys = [0, 10, 0 , 10]

    
""" 
Constraints: 
1) N is an integer within the range [2 ... 100,000]
2) Each element of arrays X,Y is an integer within the range [0..100,000]
3) No two sheep are standing in the same position
"""


# create the model
model = cp_model.CpModel()

# start = center - d, end = center + d, width = 2*d 
d = model.NewIntVar(0, 100000, "d") # distance 
twice_d = model.NewIntVar(0, 200000, "2xd")
model.Add(twice_d == 2*d) # forces this to be true -> the system needs a 
# variable in the NewIntervalVar, cannot be a formula 

# save the intervals 
width_intervals = []
height_intervals = []

for i in range(len(xs)):
    
    # left and right
    left = model.NewIntVar(-100000, 100000, "left")
    right = model.NewIntVar(-100000, 100000, "right")
    model.Add(left == xs[i] - d)
    model.Add(right == xs[i] + d)

    # NewIntervalVar -> cannot accept a formula e.g 2*d
    width_iv = model.NewIntervalVar(left, twice_d, right, "width_iv for shade %d" % i)
    width_intervals.append(width_iv)
    
    # top and bottom 
    top = model.NewIntVar(-100000, 100000, "top")
    bottom = model.NewIntVar(-100000, 100000, "bottom")     
    model.Add(top == ys[i] + d)
    model.Add(bottom == ys[i] - d)
    
    height_iv = model.NewIntervalVar(bottom, twice_d, top, "height_iv for shade %d" % i)
    height_intervals.append(height_iv)
    
# Constraint for no overlapping
model.AddNoOverlap2D(width_intervals, height_intervals)

# Goal of problem:
model.Maximize(d)

# Solve the problem 
solver = cp_model.CpSolver()
#solver.parameters.log_search_progress = True 
status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    print("D = %d" % solver.Value(d))