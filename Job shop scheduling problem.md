## (一)問題描述
 
### ● 題目:
There are j jobs and m machines; each job comprises a set of tasks1 which must each be done on a different machine for different specified processing times, in a given job-dependent order. Table 1 shows a standard 6 x 6 benchmark problem (ie, j = 6; m = 6), from (Muth & Thompson 1963).
### ● 已知:
<img src=https://github.com/KevinLu43/Job-Shop-Scheduling-with-Python/blob/master/Picture/JSP_Data.JPG width="650">
### ● 目標:
- 最小化完工時間
 
### ● 限制:
<img src=https://github.com/KevinLu43/Job-Shop-Scheduling-with-Python/blob/master/Picture/JSP_Constraints.JPG  width="650">
## (二)數學模型

### ● 參數設定
### ● 決策變數
### ● 數學式
- 目標式 :
Min Cmax
- 限制式:

## (三)Python+Pulp
## Import pulp

```python
import pulp 
```

## Model
- 定義問題
```python
model = pulp.LpProblem("MIN_makespan", pulp.LpMinimize)
```

## Add decision variables
- 儲存決策變數
```python
dv = pulp.LpVariable.dicts("start_time",
                                     ((i, j) for i in range(6) for j in range(6)),
                                     lowBound=0,
                                     cat='Continuous')
b =  pulp.LpVariable.dicts("binary_var",
                                     ((i, j,o) for i in range(6) for j in range(6) for o in range(6) if o!=j),
                                     lowBound=0,
                                     cat='Binary')

Cmax = pulp.LpVariable('Cmax',lowBound = 0, cat='Continuous')
```



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
       

model.solve()
pulp.LpStatus[model.status]     

for var in dv:
    var_value = dv[var].varValue
    print( var[0],'-',var[1] ,var_value)

total_cost = pulp.value(model.objective)
print ('min cost:',total_cost)
```
