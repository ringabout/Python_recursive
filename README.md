关注微信公众号：Python高效编程，了解更多 Python 实战知识

### 通过例子学递归

#### 思考问题

在文章正式开始之前，大家先思考一个问题：给定 1 元、2 元、5 元、10 元 四种纸币，如何通过组合（不限制单张纸币的使用次数）购买 12 元的商品？如果不考虑排序次序，有多少种组合方式？如果考虑排列次序，又有多少种可能的组合？例如十张一元的纸币。大家可以尝试使用 Python 解决此类问题，在文章的结尾处，我会提供自己的思考结果。

#### 耳熟能详的例子

生活中，有不少递归的例子，我们学习递归的时候，要善于把生活中的例子转化为编程语言实现。这样既锻炼了编程思维，又加深了自己对于概念的理解。

比如大家都听过这个故事吧：从前有座山，山上有座庙，庙里有个老和尚，老和尚在讲故事给小和尚听：从前有座山，山上有座庙，庙里有个老和尚，老和尚在讲故事给小和尚听：从前座山，山上有座庙，庙里有个老和尚，老和尚在讲故事给小和尚听.........

这就是一个无限递归的故事。那么我们应该如何使用 Python 描述呢？

首先我们来看什么是递归函数：一个函数在其内部调用函数本身，这个函数就被称为递归函数。很容易我们可以写出下面的代码：

```python
story = '从前有座山，山上有座庙，庙里有个老和尚，老和尚在讲故事给小和尚听:'
def recursive(story=story):
    return story + recursive(story)
```

这样做显然是不可以的。函数会无限递归下去，直到栈溢出，编译器报错： maximum recursion depth exceeded。因为我们缺少了停止条件，即何时 recursive 函数可以获得返回值，而不是继续调用自身。

```python
story = '从前有座山，山上有座庙，庙里有个老和尚，老和尚在讲故事给小和尚听:'
count = 0
def recursive(story=story):
    global count
    # 停止条件
    if count == 120:
        return story
    count += 1
    return story + recursive(story)
```

这次我们设置停止条件：count = 120，也就是说，函数每调用一次自身，count 值加 1。当 count 值为 120 的时候，停止调用自身，并返回 story。最后我们得到了 121 个 story 字符串相加的结果。

这样做虽然可以，但是我们并不希望打印出全部的字符串，而且我们不希望使用全局变量 count。所以把函数改写成 class：

```python
class Template:
    def __init__(self):
        self.string = '从前有座山，山上有座庙，庙里有个老和尚，老和尚在讲故事给小和尚听:'
     
    def _recursive(self, s):
        # 停止条件
        if self.count == 120:
            return s
        self.count += 1
        return s + self._recursive(s)
    
    @MyRepr
    def recursive(self):
        # 清零
        self.count = 0
        return self._recursive(self.string)
   
    def __repr__(self):
        return self.recursive()
```

MyRepr 装饰器是对于标准库 reprlib.Repr 类的重写：

```python
from functools import partial

class MyRepr(Repr):
    def __init__(self, cls):
        super().__init__()
        # 设定字符串最大长度
        self.maxstring = 100
        self.cls = cls      
        
    def __call__(self, *args, **kwargs):
        text = self.cls(*args, **kwargs)
        return self.repr(text)
      
    def __get__(self, instance, cls):
        return partial(self, instance)
```

这样输出的字符串长度就由 self.maxstring 接管，MyRepr 限定字符串长度为 100，并在字符串中间补上省略号,输出样式如下：

```
'从前有座山，山上有座庙，庙里有个老和尚，老和尚在讲故事给小和尚听:从前有座山，山上有座庙，庙里...尚，老和尚在讲故事给小和尚听:从前有座山，山上有座庙，庙里有个老和尚，老和尚在讲故事给小和尚听:'
```

#### Python 中的递归

递归是一把双刃剑。它比循环简单易懂，逻辑清晰，却会耗费大量系统资源。而 Python 也对递归层数有所限制，并且不支持尾递归优化。

但是使用递归可以快速解决问题，尤其是一些对资源要求不是很大的问题。递归也可以帮我们梳理思路，然后再使用循环重写递归。尤其有些复杂的问题，很难找到递归之外的解决方式。

在 Python 交互模式下，如果你想看到系统支持的递归层数，可以输入：

```python
>>> import sys
>>> sys.getrecursionlimit()
3000
```

#### 练手小例子

大家可以自己拿下面的小例子,使用递归实现来练练手。我写的代码仅供参考，并不一定是最优解法。如果大家有更好的解法，可以在留言小程序中贴上去。

- 阶乘
n! = n x (n−1) x (n−2) x (n−3) ⋅⋅⋅⋅ x 3 x 2 x 1!
- 求序列和
seq = [1, 5, 7]  sum = 1 + 5 + 7
- 求序列最大值
seq = [1, 5, 2, 7, 8]   max = 8 
- 递归版快速排序
```python
>>> seq = [9, 8, 7, 6, 5, 4, 3]
>>> random.shuffle(seq)
>>>seq
[6, 4, 9, 3, 8, 5, 7]
>>> quicksort(seq)
>>> [3, 4, 5, 6, 7, 8, 9]
```
- 斐波那契函数
Fn = Fn-1 + Fn-2

**阶乘**

n! = n x (n−1) x (n−2) x (n−3) ⋅⋅⋅⋅ x 3 x 2 x 1!

停止条件：n < 2

```python
def factor(n):
    # assert n >= 0
    if n < 2:
        return 1
    return n * factor(n-1)
```

精简版：

```python
# 阶乘 n >= 0
def factor(n):
    return 1 if n < 2 else n * factor(n-1)
```

**序列和**

seq = [1, 5, 7]  sum = 1 + 5 + 7

停止条件：序列为空

```python
# 和
def naive_sum(seq):
    if not seq:
        return 0
    else:
        return seq[0] + naive_sum(seq[1:])
```

**求序列最大值**

seq = [1, 5, 2, 7, 8]   max = 8 

停止条件：序列为空

```python
# 最大值
count = 1
def naive_max(seq):
    global count
    global max_num
    if count:
        max_num = seq[0]
        count = 0
    if not seq:
        count = 1
        return max_num
    else:
        if seq[0] > max_num:
            seq[0], max_num = max_num, seq[0]
        return naive_max(seq[1:])
```

**快速排序**
首先要打乱序列顺序 ，以防算法陷入最坏时间复杂度。快速排序使用“分而治之”的方法。对于一串序列，首先从中选取一个数，凡是小于这个数的值就被放在左边一摞，凡是大于这个数的值就被放在右边一摞。然后，继续对左右两摞进行快速排序。直到进行快速排序的序列长度小于 2 （即序列中只有一个值或者空值）。

注意：递归版的快排比较消耗资源。

```python
# quicksort
import random
def quicksort(seq):
    if len(seq) < 2:
        return seq
    else:
        base = seq[0]
        left = [elem for elem in seq[1:] if elem < base]
        right = [elem for elem in seq[1:] if elem > base]
        return quicksort(left) + [base] + quicksort(right)
seq = [9, 8, 7, 6, 5, 4, 3]
random.shuffle(seq)
# seq：[6, 4, 9, 3, 8, 5, 7]
print(quicksort(seq))
# 输出：[3, 4, 5, 6, 7, 8, 9]
```

##### 斐波那契函数：

Fn = Fn-1 + Fn-2

停止条件：n < 2

这里我们使用了 lru_cache 对结果进行缓存，lru_cache 会保存调用函数的结果到字典中，每次调用函数前，都会首先查询字典中是否已经有调用的结果了。如果有，函数就不必继续递归，而是返回这个结果。maxsize 为 None，表示缓存集合大小没有上限。

比如说 fibonacci(20) 会逐级递归，以至于调用很多次 fibonacci(1)，fibonacci(2)……，我们把这些结果保存起来，使得我们不必重复计算相同的函数，使得递归可以处理更多的数据。

```python
from functools import lru_cache

@lru_cache(maxsize=None)  
def fibonacci(n:int) -> int:
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### 开头的问题

再回到开篇的问题：给定 1 元、2 元、5 元、10 元 四种纸币，如何通过组合（不限制单张纸币的使用次数）购买 12 元的商品？

使用标准库 doctest 测试的内容如下：第一个 len 对应考虑排列次序对结果的影响，第二个 len 对应不考虑排列次序对结果的影响。第一种方式，共有 377 种可能的组合；而第二种方式，共有 11 种可能的组合。

```python
>>> currency = {1, 2, 5, 10}
>>> value = 12
>>> len(equal(currency, value))
377
>>> len(equal(currency, value, dup=True))
11
```

首先确定停止条件 1，当纸币的总额达到 12 元的时候，递归就应该停止，并返回可能的组合方式。停止条件 2，当纸币的总额超过 12 元的时候，递归也应该停止，并返回一个空列表。

我们循环纸币列表 currency，每次从中取一张纸币，并计算当前纸币面值总和以及可能的组合方式。然后调用自身，并判断是否满足停止条件。如果不满足，会继续从 currency 中取出一张纸币，并执行上述操作。如果满足停止条件，程序就会回到上一层继续执行，我们就可以得到 result 的值。如果 result 不为空，就保存这种组合方式。然后再从子列表中删除一个数，因为这种可能已经得到了处理。然后继续 for 循环，尝试下一种组合方式。

由于我们使用set 保存纸币，所以纸币的面值是非重的。也就是说，对于长度相同的组合，不考虑次序的话，它们就是同一种组合方式。我们同样使用 set 来保存独一无二的数值。

```python
# 完整代码，文末获取
def _equal(num:int, sub_list:list):
    # 停止条件 1
    # 当前总和等于给定值
    if num == value:
        return sub_list       
    
    for elem in currency:
        # 当前总和
        total_num = num + elem
        # 子列表增加元素
        sub_list.append(elem)
        # 停止条件 2
        # 当前总和大于给定值
        if num > value:
            return []
        # 副本
        result = _equal(total_num, sub_list.copy())
        # 去重模式
        # 若排序长度相同，则为重复值
        if dup:
            length = len(result)
            if length not in unique_set:
                unique_set.add(length)
            else:
                result = []
                
        # 如果返回值不为空
        # 将结果保存至列表中
        if result:
            total_list.append(result)
        # 子列表删除这个元素
        sub_list.pop()
      
    return []
```
