# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 13:53:54 2017

@author: Hope
"""

from gurobipy import *
m = Model("Problem1")
m.ModelSense = GRB.MINIMIZE

constraint_coeff = [[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,1],
                    [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,1],
                    [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,1],
                    [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,1],
                    [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,1],
                    [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,1],
                    [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0],
                    [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0],
                    [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0],
                    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0],
                    [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,1],
                    [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,1],
                    [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0]]
#loop through to set the contraint that you need at least one in each row
cost = [5,5,5,5,5,5,21,25,15,17,27,32,14,17,89,95,52,30,37,29,50,30,55,39,200,135,85,82,275,155]
# for each i in row sum the entire row = 1
m.update()

num_tools = len(constraint_coeff) #rows
cost_constr = len(constraint_coeff[0]) #cols
m.update()
dvars = []
for k in range(len(cost)):
    dvars.append(m.addVar(vtype=GRB.BINARY,name='q'+str(k), lb=0.0, ub=1.0)) 
    #Set lb = 0.0 to insure that there are no negative values
m.update()
# for each i in row sum the entire row = 1
for i in range(len(constraint_coeff)):
    m.addConstr(quicksum((constraint_coeff[i][j] * dvars[j] for j in range(len(constraint_coeff[i])))), GRB.EQUAL, 1)

#cost times variables  
m.setObjective(quicksum(dvars[i] * cost[i] for i in range(len(constraint_coeff[i]))))  
m.update()
m.optimize()

print "The optimal objective function value is: $", m.ObjVal 
print
print "The optimal decision variables are:"
for i in range(len(dvars)):
    if dvars[i].x == 1:
        print dvars[i].VarName, dvars[i].Obj, dvars[i].x

