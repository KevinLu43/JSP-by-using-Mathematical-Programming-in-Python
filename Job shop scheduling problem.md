*POLab*
<br>
*2018/12/01*
<br>
[【回到首頁】](https://github.com/KevinLu43/Job-Shop-Scheduling-with-Python)


## (一)問題描述
 
### ● 題目:
There are j jobs and m machines; each job comprises a set of tasks1 which must each be done on a different machine for different specified processing times, in a given job-dependent order. Table 1 shows a standard 6 x 6 benchmark problem (ie, j = 6; m = 6), from (Muth & Thompson 1963).
### ● 已知:
<img src=https://github.com/KevinLu43/Job-Shop-Scheduling-with-Python/blob/master/Picture/JSP_Data.JPG width="650">

### ● 目標:
- 最小化完工時間
 
### ● 限制:
- 每台機台一次只能做一個工作
- 每個工作必須遵守一定的順序

### (二)數學規劃
### ● Notation
- i = machine 
- j = job 
- p_ij = processing time
### ● 決策變數
```python
import pulp 
```

- y_ij : starting time of operation(i,j)
```python
dv = pulp.LpVariable.dicts("start_time",
                                     ((i, j) for i in range(6) for j in range(6)),
                                     lowBound=0,
                                     cat='Continuous')
```
- Cmax : makespan
```python
Cmax = pulp.LpVariable('Cmax',lowBound = 0, cat='Continuous')
```
- b : binary
```python
b =  pulp.LpVariable.dicts("binary_var",
                                     ((i, j,o) for i in range(6) for j in range(6) for o in range(6) if j<o),
                                     lowBound=0,
                                     cat='Binary')
```

### ● 數學式
- 目標式 :
Min Cmax
```python
model = pulp.LpProblem("MIN_makespan", pulp.LpMinimize)
model += Cmax
```
- 限制式:
<img src=https://github.com/KevinLu43/Job-Shop-Scheduling-with-Python/blob/master/Picture/JSP_Constraints.JPG  width="650">


```python
#加入限制式
#確保工作的Operation順序，必須前一站完成才能排下一站
for j in range(6):
    for i in range(5):
       I = mo[j,i]
       K = mo[j,i+1]
       J = j
       model += (dv[K,J] - dv[I,J]) >= pt[I,J]
#定義makespan       
for j in range(6):
    for i in range(6):
       I = mo[j,i]
       J = j
       model += (Cmax - dv[I,J]) >= pt[I,J]
#確保一台機台一次只能有一個工作進行       
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
## 求解
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
#min cost:55

### ● 甘特圖
<img src=https://github.com/KevinLu43/Job-Shop-Scheduling-with-Python/blob/master/Picture/G.jpg width="800">

### Reference
Michael L.Pinedo [SchedulingTheory, Algorithms, and Systems Fourth Edition](https://wp.nyu.edu/michaelpinedo/)

J.F.Muth & G.L.Thompson(1963). Industrial Scheduling. Prentice Hall, Englewood Cliffs, New Jersey,1963.
