### Recursion and Tree Recursion
q3：确定奇偶，依次递归 
q4: 将每种分值作为一种等级，依次递减
q5: 要用逐次递增的面值来进行计算时，要考虑到最大面值时的情况，`next_larger_dollar`函数在处理面值100时返回自身，导致递归无法终止。当计算总金额为100时，程序进入无限递归，错误地累加方式数目。需要修改`next_larger_dollar`，使得面值100的下一个面值超过100，从而正确终止递归。
	
	def next_larger_dollar(bill):
    """Returns the next larger bill in order."""
    	if bill == 1:
        	return 5
    	elif bill == 5:
			return 10
		elif bill == 10:
			return 20
		elif bill == 20:
			return 50
		elif bill == 50:
			return 100
		elif bill==100:
			return 101
		return 101

需要计算用给定面值（1, 5, 10, 20, 50, 100 美元）凑出目标金额的所有组合方式，要求不使用循环，仅通过递归实现。面值列表按顺序分为两种遍历方向：

**递增方向**：从最小面值 1 开始，逐步尝试更大的面值（1→5→10→20→50→100）

**递减方向**：从最大面值 100 开始，逐步尝试更小的面值（100→50→20→10→5→1）

### 二、面值递增方案的边界错误分析

#### 1. 初始代码（错误版本）



```
def next\_larger\_dollar(bill):

	if bill == 1: return 5

	elif bill == 5: return 10

	elif bill == 10: return 20

	elif bill == 20: return 50

	elif bill == 50: return 100

	return 100  # 错误：100的下一个面值应为None，但返回了100

def count\_dollars\_upward(total):

	def helper(total, bill):

		if total == 0: return 1  # 凑出目标金额，一种方式

		if total < 0: return 0   # 金额不足，无解

		if bill > 100: return 0   # 错误：面值超过100时才终止，导致100面值未正确处理

		return helper(total - bill, bill) + helper(total, next\_larger\_dollar(bill))

	return helper(total, 1)
```

#### 2. 错误原因

**边界条件错误**：当`bill=100`时，`next_larger_dollar(100)`错误地返回 100（而非`None`），导致递归进入死循环（始终处理 100 面值）。

**终止条件缺失**：`if bill > 100: return 0`无法识别「无更大面值」的情况（100 已是最大面值），导致部分组合未被计算（如直接使用 100 面值时的边界情况）。

#### 3. 修正后的递增方案



```
def next\_larger\_dollar(bill):
	if bill == 1: return 5
	elif bill == 5: return 10
	elif bill == 10: return 20
	elif bill == 20: return 50
	elif bill == 50: return 100
	return None  # 100的下一个面值为None，表示无更大面值
	
def count\_dollars\_upward(total):
	def helper(total, bill):
		if total == 0: return 1
		if total < 0 or bill is None: return 0  # 新增bill为None时的终止条件
		return helper(total - bill, bill) + helper(total, next\_larger\_dollar(bill))
	return helper(total, 1)
```

**关键修复**：

当`bill=100`时，`next_larger_dollar`返回`None`，表示「无更大面值」，递归遇到`bill is None`时终止。

通过`bill is None`明确处理「面值用尽」的边界，避免无效递归。

### 三、面值递减方案的边界正确性分析

#### 1. 正确代码（递减方向）



```
def next\_smaller\_dollar(bill):
	if bill == 100: return 50
	elif bill == 50: return 20
	elif bill == 20: return 10
	elif bill == 10: return 5
	elif bill == 5: return 1
	# 当bill=1时，无更小面值，函数默认返回None（但递归中不会触发）

def count\_dollars(total):
	def helper(total, bill):
		if total == 0: return 1  # 凑出目标金额
		if total < 0: return 0   # 金额不足
		if bill == 1: return 1   # 最小面值：剩余金额只能用1美元，仅1种方式
		return helper(total - bill, bill) + helper(total, next\_smaller\_dollar(bill))
	return helper(total, 100)  # 从最大面值100开始尝试
```

#### 2. 无需检查`bill None`的原因

**递归终止逻辑**：当`bill`递减到 1 时，通过`if bill == 1: return 1`直接终止递归。此时，若剩余金额`total`为正，只能用 1 美元凑（只有 1 种方式）；若`total`为 0 或负数，由前两个条件处理。

**面值递减路径**：面值按`100→50→20→10→5→1`递减，当`bill=1`时，`next_smaller_dollar(1)`无匹配条件，返回`None`，但递归已在此前通过`bill == 1`的条件提前终止，不会执行到`next_smaller_dollar(1)`。

**边界覆盖完整**：最小面值 1 作为「兜底」条件，确保所有剩余金额的组合方式被唯一确定（只能用 1 美元，方式数为 1），无需额外处理`None`。

### 四、核心区别：递增 vs 递减的递归设计



| **特征**     | 面值递增方案（从 1 到 100）      | 面值递减方案（从 100 到 1）     |
| ---------- | ---------------------- | --------------------- |
| **递归方向**   | 从小面值开始，逐步尝试更大面值        | 从大面值开始，逐步尝试更小面值       |
| **终止条件**   | 需要检查`bill None`（无更大面值） | 通过`bill==1`终止（最小面值兜底） |
| **面值用尽处理** | 显式判断`bill是否存在`         | 隐式通过最小面值 1 的唯一性处理     |
| **递归子问题**  | `使用当前面值`或`尝试更大面值`      | `使用当前面值`或`尝试更小面值`     |


**覆盖所有边界**：

递增方案中，最大面值的下一个面值为`None`，需显式处理「无更大面值」的终止条件。

递减方案中，最小面值 1 是「原子解」（剩余金额只能用 1 美元，方式唯一），可作为递归终止的「保底条件」。

**避免无效递归**：通过条件判断（如`total < 0`或`bill无效`）及时终止无效路径，防止无限递归或错误计算。
