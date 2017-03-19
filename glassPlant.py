# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 13:57:00 2017

@author: Hope
"""

m = Model("PC")
m.ModelSense = GRB. MINIMIZE
m.setParam('TimeLimit', 7200)    #sets a time limit on eucaion to some number of seconds


trans_cost_per_ton = [[24.92,30.36,34.9,39.3,31.78,28.89,44.49,34.99,30.4,30.79,33.31,29.42,34.62,36.18,41.88],
                      [35.57,21.7,36.79,43.38,31.42,40.79,30.96,29.92,29.62,25.74,41.77,32.04,40.69,43.05,30.46],
                      [44.57,22.94,23.97,40.35,26.31,27.98,35,38.77,29.88,25.47,38.02,33.53,41.75,27.88,37.74],
                      [36.38,36.78,38.07,26.37,29.46,32.75,26.71,30.67,30.15,30.96,39.77,37.08,30.97,37.2,29.04],
                      [43.06,39.52,28.24,39.64,21.02,32.27,39.11,26.87,39.3,36.78,34.29,27.8,40.69,39.36,26.62],
                      [40,40.78,30.37,29.06,36.83,23.3,27.66,34.1,25.21,35.97,33.24,43.08,34.48,25.04,27.67],
                      [42.78,40.26,30.13,30.07,38.74,25.42,26.52,22.9,30.33,31.91,31.21,41.51,30.11,27.16,42.24],
                      [28.51,37.04,33.64,40.15,31.57,31.21,38.05,20.55,40.37,37.04,39.44,40.03,41.89,40.68,28.46],
                      [32.68,41.09,31.26,31.12,36.6,42.88,28.38,33.22,25.05,29.22,33.83,36,38.53,34.74,37.84],
                      [32.83,31.23,39.85,29.23,21.06,35.46,44.64,37.5,31.33,21.34,42.79,41.56,37.13,42,31.39],
                      [39.44,22.16,39.22,34.29,37.82,33.98,43.78,26.06,44.11,26.37,26.82,40.44,34.71,42.37,42.86],
                      [34.41,39.82,27.01,33.52,28.79,29.19,42.17,28.96,39.16,39.48,39.45,26.71,24.97,35.39,41.33],
                      [27.51,35.59,26.86,45.97,32.64,34.21,45.88,36.42,32.76,28.71,36.66,36.66,23.18,26.14,26.42],
                      [29.01,40.13,28.84,43.7,32.75,29.23,33.11,32.37,25.1,22.92,34.16,27.38,26.28,24.67,39.63],
                      [26.07,28.96,33.83,36.53,32.95,28.25,32.21,36.24,29.18,22.37,30.78,26.84,36.74,30.18,26.33]]
#all prices for plants 1-15
mine_purchase_price = [9355730,4652163,9908390,8379730,6946479,4760629,4880341,9804748,6100783,7224557,7756098,4015446,10580870,8088620,10866700]
m.update()

#Set up decision variables
mp_p=[]
for i in range(len(trans_cost_per_ton)):
    newdvars=[]
    for j in range(len(trans_cost_per_ton[i])):
        newdvars.append(m.addVar(vtype=GRB.BINARY, name="mp_a" +str(j) +"_" +str(i)))
    mp_p.append(newdvars) 
                

mp_s=[]
for i in range(len(trans_cost_per_ton)):
    newdvars=[]
    for j in range(len(trans_cost_per_ton[i])):
        newdvars.append(m.addVar(vtype=GRB.INTEGER, name="mp_b" +str(j) +"_" +str(i)))
    mp_s.append(newdvars)
    
#Set the number for the mine 0-14
mine_var=[]
for j in range(len(mine_purchase_price)):
    mine_var.append(m.addVar(vtype=GRB.BINARY,name='m_'+str(j)))       
#Update the model

m.update()

#Set up constraints:

for i in range(len(trans_cost_per_ton)):
    for j in range(len(trans_cost_per_ton[i])):
       m.addConstr(mp_p[i][j], GRB.LESS_EQUAL, mine_var[j])
       
for i in range(len(trans_cost_per_ton)):
    m.addConstr(quicksum(mp_s[i][j] for j in range(len(trans_cost_per_ton[i]))), GRB.GREATER_EQUAL, 153300)
  
                
for i in range(len(trans_cost_per_ton)):
    for j in range(len(trans_cost_per_ton[i])):
        m.addConstr(mp_s[i][j], GRB.LESS_EQUAL, mp_p[i][j]*100000000) #Set large number so it wouldnt be minimal solution
        


#objective function
m.setObjective(quicksum(trans_cost_per_ton[i][j] * mp_s[i][j] for i in range(len(trans_cost_per_ton)) for j in range(len(mine_purchase_price)))+ 
quicksum(mine_purchase_price[j] * mine_var[j] for j in range(len(trans_cost_per_ton[j]))))


m.update()
m.optimize()


#Print output values

print "The optimal objective function value is: $", m.ObjVal 
print "The optimal decision variables are:"
for var in mine_var:
    if var.x>0 :
        print '\t',var.varName

print "Which mine serves which plant:"
for line in mp_s:
    for var in line:
        if var.x > 0:
            print '\t', var.VarName, var.x
    print
        
                





