# Python 基础知识速查表

这是一份适合数学专业背景的 Python 速查表，随时查阅。

---

## 📌 数据类型速查

### 基本类型

```python
# 数字
x = 10              # int（整数）
y = 3.14            # float（浮点数）
z = 1 + 2j          # complex（复数）

# 字符串
s = "hello"         # str
s = 'hello'         # 单引号也可以
s = """多行
字符串"""

# 布尔值
b = True            # bool（注意大写）
b = False

# 空值
x = None            # NoneType
```

### 容器类型

```python
# 列表（可变）
lst = [1, 2, 3]
lst[0] = 10         # ✅ 可以修改

# 元组（不可变）
tup = (1, 2, 3)
tup[0] = 10         # ❌ 报错

# 字典
d = {"name": "张三", "age": 25}

# 集合
s = {1, 2, 3}       # 自动去重
```

---

## 📌 字符串操作

```python
s = "  Hello World  "

# 常用方法
s.strip()           # "Hello World"（去首尾空格）
s.lower()           # "  hello world  "
s.upper()           # "  HELLO WORLD  "
s.replace("World", "Python")  # "  Hello Python  "
s.split()           # ["Hello", "World"]
"|".join(["a", "b"]) # "a|b"

# 判断
"hello" in s        # False（大小写敏感）
s.startswith("  H") # True
s.endswith("  ")    # True

# f-string（推荐）
name = "张三"
age = 25
print(f"{name} 今年 {age} 岁")  # 张三 今年 25 岁
print(f"{3.14159:.2f}")         # 3.14（保留2位小数）
print(f"{0.756:.2%}")           # 75.60%（百分比）
```

---

## 📌 列表操作

```python
lst = [1, 2, 3, 4, 5]

# 索引（从0开始）
lst[0]              # 1（第一个）
lst[-1]             # 5（最后一个）
lst[1:3]            # [2, 3]（切片，不包含末尾）
lst[:3]             # [1, 2, 3]（前3个）
lst[2:]             # [3, 4, 5]（从第3个到最后）
lst[::2]            # [1, 3, 5]（每隔一个）

# 修改
lst.append(6)       # 末尾添加
lst.insert(0, 0)    # 在索引0插入
lst.remove(3)       # 删除第一个3
lst.pop()           # 删除并返回最后一个
len(lst)            # 长度

# 判断
3 in lst            # True

# 列表推导式
squares = [x**2 for x in range(10)]
evens = [x for x in range(10) if x % 2 == 0]
```

---

## 📌 字典操作

```python
d = {"name": "张三", "age": 25}

# 访问
d["name"]           # "张三"
d.get("name")       # "张三"（推荐）
d.get("phone")      # None（安全）
d.get("phone", "无") # "无"（默认值）

# 修改
d["age"] = 26       # 修改
d["city"] = "北京"   # 添加

# 遍历
for key in d:
    print(key, d[key])

for key, value in d.items():
    print(f"{key}: {value}")

# 常用方法
d.keys()            # dict_keys(['name', 'age'])
d.values()          # dict_values(['张三', 25])
"name" in d         # True
```

---

## 📌 集合操作

```python
a = {1, 2, 3}
b = {2, 3, 4}

# 集合运算
a & b               # {2, 3}（交集）
a | b               # {1, 2, 3, 4}（并集）
a - b               # {1}（差集）
a ^ b               # {1, 4}（对称差）

# 判断
2 in a              # True
a.issubset(b)       # False
```

---

## 📌 控制流

### if-elif-else

```python
score = 85

if score >= 90:
    print("优秀")
elif score >= 80:
    print("良好")
else:
    print("及格")

# 三元表达式
result = "及格" if score >= 60 else "不及格"
```

### for 循环

```python
# 遍历列表
for item in [1, 2, 3]:
    print(item)

# 遍历字典
for key, value in d.items():
    print(f"{key}: {value}")

# 遍历数字
for i in range(5):          # 0, 1, 2, 3, 4
    print(i)

for i in range(2, 10, 2):   # 2, 4, 6, 8
    print(i)

# 带索引遍历
for i, item in enumerate(["a", "b", "c"]):
    print(f"{i}: {item}")   # 0: a, 1: b, 2: c
```

### while 循环

```python
count = 0
while count < 5:
    print(count)
    count += 1
```

---

## 📌 函数

```python
# 基本定义
def greet(name):
    return f"Hello, {name}!"

# 默认参数
def greet(name, msg="Hello"):
    return f"{msg}, {name}!"

# 多个返回值
def get_stats():
    return 100, 0.73, 0.85  # 返回元组

total, auth, time = get_stats()  # 解包

# 可变参数
def sum_all(*args):
    return sum(args)

sum_all(1, 2, 3, 4)  # 10

# 关键字参数
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="张三", age=25)
```

---

## 📌 文件操作

```python
# 读文件
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()          # 读全部
    # 或
    lines = f.readlines()       # 读所有行
    # 或
    for line in f:              # 逐行读取
        print(line.strip())

# 写文件
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello\n")

# 追加
with open("output.txt", "a", encoding="utf-8") as f:
    f.write("World\n")
```

---

## 📌 路径处理

```python
from pathlib import Path

# 创建路径对象
p = Path("data/output.xlsx")

# 属性
p.name          # "output.xlsx"
p.stem          # "output"
p.suffix        # ".xlsx"
p.parent        # Path("data")
p.exists()      # True/False
p.is_file()     # True/False
p.is_dir()      # True/False

# 拼接路径
base = Path("data")
file_path = base / "output.xlsx"

# 创建目录
p.parent.mkdir(parents=True, exist_ok=True)
```

---

## 📌 异常处理

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("除数不能为0")
except FileNotFoundError:
    print("文件不存在")
except Exception as e:
    print(f"错误: {e}")
else:
    print("没有异常")
finally:
    print("无论如何都执行")
```

---

## 📌 Pandas 核心操作

```python
import pandas as pd

# 读取
df = pd.read_excel("data.xlsx")
df = pd.read_csv("data.csv", encoding="utf-8")

# 查看
df.head()           # 前5行
df.columns          # 列名
df.shape            # (行数, 列数)
df.info()           # 数据类型和空值信息

# 列操作
df["new_col"] = df["col1"] + df["col2"]
df["col"].fillna("")  # 填充空值
df["col"].astype(str)  # 转换类型

# 筛选
df[df["score"] > 0.5]               # 按条件筛选
df[df["name"].isin(["张三", "李四"])]  # 按列表筛选
df[~df["hash"].isin(existing)]      # 排除（~表示取反）

# 去重
df.drop_duplicates(subset=["hash"], keep="first")

# 分组
df.groupby("category")["score"].mean()

# apply（对每行应用函数）
df["hash"] = df.apply(lambda r: make_hash(r["col1"], r["col2"]), axis=1)
# axis=1: 按行; axis=0: 按列

# 写入
df.to_excel("output.xlsx", index=False)
```

---

## 📌 常用内置函数

```python
# 类型转换
int("123")          # 123
float("3.14")       # 3.14
str(123)            # "123"
list("abc")         # ["a", "b", "c"]

# 序列操作
len([1, 2, 3])      # 3
max([1, 5, 3])      # 5
min([1, 5, 3])      # 1
sum([1, 2, 3])      # 6
sorted([3, 1, 2])   # [1, 2, 3]

# 其他
range(5)            # 0, 1, 2, 3, 4
zip([1,2], ["a","b"])  # [(1,"a"), (2,"b")]
enumerate(["a","b"])   # [(0,"a"), (1,"b")]
```

---

## 📌 常见错误速查

| 错误 | 原因 | 解决 |
|------|------|------|
| `NameError: name 'x' is not defined` | 变量未定义 | 先赋值再使用 |
| `KeyError: 'name'` | 字典键不存在 | 用 `d.get("name")` |
| `IndexError: list index out of range` | 列表索引超出 | 检查列表长度 |
| `TypeError: 'str' object does not support item assignment` | 字符串不可变 | 创建新字符串 |
| `FileNotFoundError` | 文件不存在 | 检查路径 |
| `ValueError: invalid literal for int()` | 类型转换失败 | 检查数据格式 |
| `AttributeError: 'NoneType' object has no attribute 'xxx'` | 对None调用方法 | 检查是否为None |

---

## 📌 调试技巧

```python
# 查看类型
print(type(x))

# 查看对象的所有方法
print(dir(str))

# 查看函数文档
help(str.strip)

# 断点调试（打印变量）
print(f"x = {x}, type = {type(x)}")

# 检查是否为None
if x is None:
    print("x 是 None")

# 检查是否为空
if not x:  # 空字符串、空列表、0、None 都是 False
    print("x 是空的")
```

---

## 📌 你代码中的常用模式

### 1. 安全的字典访问

```python
# 不推荐
value = row["key"]  # 键不存在会报错

# 推荐
value = row.get("key", "")  # 键不存在返回空字符串
```

### 2. 列表推导式

```python
# 你的代码中常见
hashes = {row[0] for row in result}  # 集合推导式
scores = [auth_score(row) for _, row in df.iterrows()]  # 列表推导式
```

### 3. 防止除以0

```python
# 你的代码中常见
rate = a / b if b > 0 else 0
```

### 4. 字符串拼接计算hash

```python
# 你的代码中常见
s = "|".join([str(x or "") for x in [query, title, content]])
```

### 5. pandas fillna + astype

```python
# 你的代码中常见
df["col"] = df["col"].fillna("").astype(str)
```

---

随时回来查阅这份速查表！
