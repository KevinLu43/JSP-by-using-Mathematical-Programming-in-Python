# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 15:20:11 2018

@author: Kevin Lu
"""

import pandas as pd
import numpy as np
import time
import pulp  

processing_time=pd.read_excel("C:/Users/Kevin Lu/Desktop/Jobshop.xlsx",
                              sheet_name="processing_time",
                              header = None)
machine_order=pd.read_excel("C:/Users/Kevin Lu/Desktop/Jobshop.xlsx",
                            sheet_name="machine_order",
                            header = None)

pt = processing_time.values
mo = machine_order.values

model = pulp.LpProblem("MIN_makespan", pulp.LpMinimize)

dv = pulp.LpVariable.dicts("start_time",
                                     ((i, j) for i in range(6) for j in range(6)),
                                     lowBound=0,
                                     cat='Continuous')
b =  pulp.LpVariable.dicts("binary_var",
                                     ((i, j,o) for i in range(6) for j in range(6) for o in range(6) if o!=j),
                                     lowBound=0,
                                     cat='Binary')

Cmax = pulp.LpVariable('Cmax',lowBound = 0, cat='Continuous')


model += Cmax

for j in range(6):
    for i in range(5):
       I = mo[j,i]
       K = mo[j,i+1]
       J = j
       model += (dv[K,J] - dv[I,J]) >= pt[I,J]
       
for j in range(6):
    for i in range(6):
       I = mo[j,i]
       J = j
       model += (Cmax - dv[I,J]) >= pt[I,J]
       
for i in range(6):
    for j in range(6):
        for l in range(6):
            if j!=l:
                I=i
                L = l
                J = j
                model += (dv[I,J] - dv[I,L]) >= (pt[I,L] - 100*(1-b[i,J,L]))
                model += (dv[I,L] - dv[I,J]) >= (pt[I,J] - 100*(b[i,J,L]))
       
start_time = time.time()
model.solve()
pulp.LpStatus[model.status]     

for var in dv:
    var_value = dv[var].varValue
    print( var[0],'-',var[1] ,var_value)

total_cost = pulp.value(model.objective)
print ('min cost:',total_cost)
print('the elapsed time:%s'% (time.time() - start_time))
