# Python+Pulp基本架構

### ● 在利用Python+Pulp建構數學規劃時，通常會依照此順序進行設定變數、目標函數、限制式等
<img src="https://github.com/jasonyoyo/python-pulp/blob/master/picture/pulp%20flow.png" >

### ● Import Module
python中一開始要先import Module才可以做使用，分為兩種方式:
 
 ```python
import pulp
```
```python
from pulp import*
```

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

## (二)常用的四大函數及屬性
### 1.四大函數
在建立一個數學規劃時，我們必須加入我們的決策變數、目標函數及限制式，以下是在設定這些變數及式子常用的四大函數的詳細內容介紹
<br>P.S. 在pulp中設定目標函數及限制式還有其他不一樣的方式，在此只介紹這四個函數的應用，若想要有更進一步的了解可至[pulp網站](https://pythonhosted.org/PuLP/pulp.html)內的查詢

### ● 定義問題(Formulate Problem)

<img src="https://github.com/jasonyoyo/python-pulp/blob/master/picture/%E5%AE%9A%E7%BE%A9%E5%95%8F%E9%A1%8C.png" width="600"><br>

### ● 決策變數函數(Create Decision Variables)

 變數預設的範圍上限為正無限，下限為負無限，變數型態為連續變數(continuous)<br>
 
<img src="https://github.com/jasonyoyo/python-pulp/blob/master/picture/%E8%AE%8A%E6%95%B8.png" width="700"><br>

### ● 目標函數(Add Objective Function)
<img src="https://github.com/jasonyoyo/python-pulp/blob/master/picture/%E7%9B%AE%E6%A8%99%E5%BC%8F.png" width="500"><br>

### ● 限制式函數(Add Constraints)
<img src="https://github.com/jasonyoyo/python-pulp/blob/master/picture/%E9%99%90%E5%88%B6%E5%BC%8F.png" width="500">


### 2.Pulp attributes
在pulp中，可以透過各種屬性來查詢或更改所建立數學規劃的內容，以下為常用的幾個屬性:
<br>P.S. 更多屬性查詢，可點擊[這裡](https://www.coin-or.org/PuLP/pulp.html)
### ● Model attributes:

|Attribute Name|Description|
|-----|-----|
|**slove()**|slove the problem|
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
