## (一)問題描述
 
### ● 題目:

### ● 已知:
<img src=https://github.com/KevinLu43/Job-Shop-Scheduling-with-Python/blob/master/Picture/FJSP_Data.JPG width="1500">

### ● 目標:
- 最小化完工時間
 
### ● 限制:
- 每個工作必須遵守一定的順序
- 每個Operation有不同的機台可以選擇
- 每台機台一次只能做一個工作
### (二)數學模型

### ● Notation

### ● 決策變數

### ● 數學式
- 目標式 :
Min Cmax
- 限制式:
<img src=https://github.com/KevinLu43/Job-Shop-Scheduling-with-Python/blob/master/Picture/JSP_Constraints.JPG  width="650">

### (二)數學模型
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

## Add objective function

```python
#加入目標式
model += Cmax
```
## Add constraints

```python
#加入限制式
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
```       
## solve
```python
model.solve()
pulp.LpStatus[model.status]     
```
#印出解及目標值
```python
for var in dv:
    var_value = dv[var].varValue
    print( var[0],'-',var[1] ,var_value)

total_cost = pulp.value(model.objective)
print ('min cost:',total_cost)
```
min cost:55

### ● 甘特圖
