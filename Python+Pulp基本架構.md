*POLab*
<br>
*2018/12/01*
<br>
[【回到首頁】](https://github.com/KevinLu43/Job-Shop-Scheduling-with-Python)


# Python+Pulp基本架構

### ● 在利用Python+Pulp建構數學規劃時，通常會依照此順序進行設定變數、目標函數、限制式等
<img src="https://github.com/jasonyoyo/python-pulp/blob/master/picture/pulp%20flow.png" >

### ● Import Module
### python中一開始要先調用 Module才可以使用，調用方式常見的有兩種:
1. 
 ```python
import pulp
```
2.
```python
from pulp import*
```
較不推薦使用，容易造成衝突，並降低可讀性與維護性
更詳盡的說明請參考[這裡](https://medium.com/pyladies-taiwan/python-%E7%9A%84-import-%E9%99%B7%E9%98%B1-3538e74f57e3)

### ● 建模時常使用for迴圈及if條件句
-**for迴圈**
```python
for i in <some list>:
 <do something for each i here>
```
-**if條件句**
```python
if <condition>:
 <do something if condition is true here>
```

## 常用的函數及屬性
### 1.函數
在建立一個數學規劃時，我們必須加入我們的決策變數、目標函數及限制式，以下是在設定這些變數及式子常用的函數內容介紹，
在pulp中設定目標函數及限制式還有其他不一樣的方式，更進一步的了解請參考[pulp網站](https://pythonhosted.org/PuLP/pulp.html)內的查詢

### ● 定義問題(Formulate Problem)

Problem = pulp.LpProblem(name_str, sense)

sense ∈ {pulp.LpMinimize,pulp.LpMaximize}

- E.g. Maximization problem

```python
problem = pulp.LpProblem('Benefit',pulp.LpMaximize)
```

### ● 決策變數函數(Create Decision Variables)

變數預設的範圍上限為正無限，下限為負無限，變數型態為連續變數(continuous)<br>

Decision_Variable = pulp.LpVariable(name_str, lowbound, upbound, category)

category ∈ {Continuous, Integer, Binary}

E.g. x ∈ [0,∞]

```python
X = pulp.LpVariable('VarX', 0, None, cat='Continuous')
```

### ● 限制式函數(Add Constraints)

problem+=linear_constraint, constraint_name_str

E.g. Cost: 2X1 - 3X2 ≤100

```python
problem += 2*X1 – 3*X2 <= 100, 'Cost'
```

### 2.Pulp attributes
在pulp中，可以透過各種屬性來查詢或更改所建立數學規劃的內容，以下為常用的幾個屬性:
<br>P.S. 更多屬性查詢，可點擊[這裡](https://www.coin-or.org/PuLP/pulp.html)
### ● Model attributes:

|Attribute Name|Description|
|-----|-----|
|**solve()**|solve the problem|
```python
model.solve()
```


|Attribute Name|Description|
|-----|-----|
|**status**|The return status of the problem from the solver.|

|string value|numerical value|
|-----|-----|
|"Optimal"|1|
|"Not Solve"|0|
|"Infeasible"|-1|
|"Unbounded"|-2|
|"Undefined"|-3|

```python
model.status
```
```
1
```
```python
pulp.LpStatus[model.status]
```
```
'Optimal'
```


|Attribute Name|Description|
|-----|-----|
|**value(model.objective)**|objective value for current solution|
```python
total_cost = pulp.value(model.objective)
```


|Attribute Name|Description|
|-----|-----|
|**varValue**|Value in the current solution|
|**variables.name**|variable name|
```python
for v in prob.variables():
    print(v.name, "=", v.varValue)
```
