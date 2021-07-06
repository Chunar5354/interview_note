装饰器提供了一种方法，在函数和类定义语句结束时`插入自动运行的代码`

自动重绑定，在def结束的时候通过`另一个函数`来运行当前函数

以下两种形式是等价的：

```python
@decorator
def F(arg):
    ...
F(99)
```

与

```python
def F(arg):
    ...
F = decorator(F)
F(99)
```

在调用F的时候，自动调用`decorator返回的对象`

装饰器自身是一个`返回可调用对象`的可调用对象，并`以函数作为参数`，可以是函数或类

## 函数型装饰器

一个简单的装饰器示例：

```python
def decorator(F):
    print('this is a decorator')
    return F

@decorator
def f1(a, b):
    return a+b

print(f1(1, 2))
```

运行：

```
this is a decorator
3
```

## 类型装饰器

装饰器自身除了是函数也可以是类，当装饰器是类时可以接收被装饰函数的参数

```python
class Decorator:
    def __init__(self, func):
        self.func = func
    # 关于函数调用的内建 方法
    def __call__(self, *args):
        print('the arguments are:', *args)
        return self.func(*args)

@Decorator
def f1(a, b):
    return a+b

print(f1(1, 2))
```

运行：

```
the arguments are: 1 2
3
```