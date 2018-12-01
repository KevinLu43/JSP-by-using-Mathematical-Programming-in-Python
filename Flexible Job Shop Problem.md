*POLab*
<br>
*2018/12/01*
<br>
[【回到首頁】](https://github.com/KevinLu43/Job-Shop-Scheduling-with-Python)


## (一)問題描述
 
### ● 題目:
- 加工順序
<img src=https://github.com/KevinLu43/JSP-by-using-Mathematical-Programming-in-Python/blob/master/Picture/FJSP_OS.JPG width="650">

- 加工時間

<img src=https://github.com/KevinLu43/JSP-by-using-Mathematical-Programming-in-Python/blob/master/Picture/FJSP_PT.JPG width="450">

### ● 目標:
- 最小化完工時間
 
### ● 限制:
- 每個工作必須遵守一定的順序
- 每個Operation有不同的機台可以選擇
- 每台機台一次只能做一個工作
### (二)數學模型

### ● Notation
<img src=https://github.com/KevinLu43/JSP-by-using-Mathematical-Programming-in-Python/blob/master/Picture/FJSP_Notation.JPG width="950">

### ● 決策變數
<img src=https://github.com/KevinLu43/JSP-by-using-Mathematical-Programming-in-Python/blob/master/Picture/FJSP_DV.JPG width="850">

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
<img src=https://github.com/KevinLu43/JSP-by-using-Mathematical-Programming-in-Python/blob/master/Picture/FJSP_C1.JPG width="250">

- 確保Operation只在一台機台被執行
<img src=https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/implementation%20with%20python/GA-jobshop/picture/4.png width="350">

```python
#加入限制式
###限制式###
for i in range(1,6):
    for j in [ops[i-1][o] for o in range(1,5) if ops[i-1][o]!=0]:
        ma_list=list(Processing_time.loc[(Processing_time['Operation']==j),'machine'])
        model += pulp.lpSum(x[i,j,ma] for ma in ma_list)==1
```

<img src=https://github.com/KevinLu43/JSP-by-using-Mathematical-Programming-in-Python/blob/master/Picture/FJSP_C2.JPG width="400">

<img src=https://github.com/KevinLu43/JSP-by-using-Mathematical-Programming-in-Python/blob/master/Picture/FJSP_C3.JPG width="500">

- 如果第i個Job的第j個Operation在Machine k上執行，那他的Operation結束時間要大於等於開始時間+作業時間，沒有被執行的Operation，開始與結束時間等於0

```python
for i in range(1,6):
    for j in [ops[i-1][o] for o in range(1,5) if ops[i-1][o]!=0]:
        ma_list=list(Processing_time.loc[(Processing_time['Operation']==j),'machine'])
        for k in ma_list:
            ptime=int(Processing_time.loc[(Processing_time['Operation']==j)&(Processing_time['machine']==k),['J%d'%i]].iloc[0])
            I = i
            J = j
            K = k
            model += st[I,J,K] + ct[I,J,K] <=x[I,J,K]*1000
            model += ct[I,J,K] >= st[I,J,K] +ptime-(1-x[I,J,K])*1000
```

<img src=https://github.com/KevinLu43/JSP-by-using-Mathematical-Programming-in-Python/blob/master/Picture/FJSP_C4.JPG width="500">

<img src=https://github.com/KevinLu43/JSP-by-using-Mathematical-Programming-in-Python/blob/master/Picture/FJSP_C5.JPG width="500">

- 如果兩個Operation要使用相同機台，確保他們不會同時執行

```python
for i in range(1,6):
    for l in range(1,6):
        if i<l:
            for o1 in [ops[i-1][o] for o in range(1,5) if ops[i-1][o]!=0]:
                ma1_list=list(Processing_time.loc[(Processing_time['Operation']==o1)&(Processing_time.loc[:]['J%d'%i]!=0),'machine'])
                for o2 in [ops[l-1][o] for o in range(1,5) if ops[l-1][o]!=0]:
                    ma2_list=list(Processing_time.loc[(Processing_time['Operation']==o2)&(Processing_time.loc[:]['J%d'%l]!=0),'machine'])
                    mach_set=list(set(ma1_list)&set(ma2_list))
                    if len(mach_set)>0:
                        for k in mach_set:
                            model += st[i,o1,k]>=ct[l,o2,k]-y[i,o1,l,o2,k]*1000
                            model += st[l,o2,k]>=ct[i,o1,k]-(1-y[i,o1,l,o2,k])*1000
```

<img src=https://github.com/KevinLu43/JSP-by-using-Mathematical-Programming-in-Python/blob/master/Picture/FJSP_C6.JPG width="300">

- 確保每一個Job的Operation的順序，一定要前一個完成才能進行下一個Operation

```python
for i in range(1,6):
    op_num=[ops[i-1][o] for o in range(1,5) if ops[i-1][o]!=0]
    print(op_num)
    for j in range(1,len(op_num)):
        print(i,j)
        preop_num=op_num[j-1]
        curop_num=op_num[j]
        print('pc')
        print(preop_num,curop_num)
        prema_list=list(Processing_time.loc[(Processing_time['Operation']==preop_num)&(Processing_time.loc[:]['J%d'%i]!=0),'machine'])
        curma_list=list(Processing_time.loc[(Processing_time['Operation']==curop_num)&(Processing_time.loc[:]['J%d'%i]!=0),'machine'])
        model += pulp.lpSum(st[i,curop_num,ma1] for ma1 in curma_list) >= pulp.lpSum(ct[i,preop_num,ma2] for ma2 in prema_list)
```

<img src=https://github.com/KevinLu43/JSP-by-using-Mathematical-Programming-in-Python/blob/master/Picture/FJSP_C7.JPG width="200">

- 確保每一個工作的最後完成時間是每一個工作最後一個Operation完成後的時間

```python
for i in range(1,6):
    op_list=[ops[i-1][o] for o in range(1,5) if ops[i-1][o]!=0]
    last_op=op_list[-1]
    model +=Ci[i]>=pulp.lpSum(ct[i,last_op,k] for k in list(Processing_time.loc[(Processing_time['Operation']==last_op),'machine']))
```

<img src=https://github.com/KevinLu43/JSP-by-using-Mathematical-Programming-in-Python/blob/master/Picture/FJSP_C8.JPG width="200">

- 定義Makespan

```python
    model += Cmax >= Ci[i]
```       

## 求解
```python
model.solve()
pulp.LpStatus[model.status]     
```
#印出解及目標值
```python
for var in ct:
    var_value = ct[var].varValue
    print( var[0],var[1],var[2] ,var_value)

total_cost = pulp.value(model.objective)
print ('min cost:',total_cost)
```
-min cost: 193.0
### ● 甘特圖
<img src=https://github.com/KevinLu43/Job-Shop-Scheduling-with-Python/blob/master/Picture/FJSP_G.JPG width="700">

### ● Reference
[Cemal Özgüven, Lale Özbakır, Yasemin Yavuz Mathematical models for job-shop scheduling problems with routing and process plan flexibility](https://www.sciencedirect.com/science/article/pii/S0307904X09002819)
