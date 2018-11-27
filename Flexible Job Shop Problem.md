*POLab*
<br>
*2018/12/01*
<br>
[【回到首頁】](https://github.com/KevinLu43/Job-Shop-Scheduling-with-Python)


## (一)問題描述
 
### ● 題目:
-
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
<img src=https://github.com/KevinLu43/Job-Shop-Scheduling-with-Python/blob/master/Picture/FJSP_Notation.JPG width="1000">

### ● 決策變數
<img src=https://github.com/KevinLu43/Job-Shop-Scheduling-with-Python/blob/master/Picture/FJSP_DV.JPG width="450">

```python
Cmax = pulp.LpVariable('Cmax',lowBound = 0, cat='Continuous')

Ci = pulp.LpVariable.dicts("start_time",
                           ((i) for i in range(1,6)),
                           lowBound=0,
                           cat='Continuous')
#i=job,j=operation,k=machine
st = pulp.LpVariable.dicts("start_time",
                           ((i, j, k) for i in range(1,6) for j in [ops[i-1][o] for o in range(1,5) if ops[i-1][o]!=0] for k in list(Processing_time.loc[(Processing_time['Operation']==j),'machine'])),
                           lowBound=0,
                           cat='Continuous')

ct = pulp.LpVariable.dicts("completed_time",
                           ((i, j, k) for i in range(1,6) for j in [ops[i-1][o] for o in range(1,5) if ops[i-1][o]!=0] for k in list(Processing_time.loc[(Processing_time['Operation']==j),'machine'])),
                           lowBound=0,
                           cat='Continuous')

x = pulp.LpVariable.dicts("X_binary_var",
                          ((i, j, k) for i in range(1,6) for j in [ops[i-1][o] for o in range(1,5) if ops[i-1][o]!=0] for k in list(Processing_time.loc[(Processing_time['Operation']==j),'machine'])),
                          lowBound=0,
                          cat='Binary')

y = pulp.LpVariable.dicts("Y_binary_var",
                          ((i, j, l, m,k) for i in range(1,6) for j in [ops[i-1][o] for o in range(1,5) if ops[i-1][o]!=0]  for l in range(1,6) for m in [ops[l-1][a] for a in range(1,5) if ops[l-1][a]!=0]  for k in list(set(list(Processing_time.loc[(Processing_time['Operation']==j),'machine']))&set(list(Processing_time.loc[(Processing_time['Operation']==m),'machine']))) if i < l ),
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
<img src=https://github.com/KevinLu43/Job-Shop-Scheduling-with-Python/blob/master/Picture/FJSP_CFirst.JPG  width="450">

<img src=https://github.com/KevinLu43/Job-Shop-Scheduling-with-Python/blob/master/Picture/FJSP_CFinal.JPG  width="650">




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

### ● 甘特圖


### ● Reference
Cemal Özgüven, Lale Özbakır, Yasemin Yavuz(Mathematical models for job-shop scheduling problems with routing and process plan flexibility)
