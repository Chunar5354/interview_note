## yield

包含yield语句的函数是一个`生成器`

生成器的作用是可以`延迟产生结果`，每当运行到yield语句，就会被`挂起`，并且将yield后面的值（如果没有就是None）传递出去（类似return）

可以通过next()和send()方法让生成器继续执行，其中send()方法可以给生成器传入值

一个例子：

```python
def gen():
    for i in range(5):
        n = yield i
        print('n is:', n)

g = gen()
next(g)  # 启动生成器，也可以用send(None)
print(g.send(999))
print(next(g))
print(g.send(888))
```

输出为：

```
n is: 999
1
n is: None
2
n is: 888
3
```

可以看到，除了启动生成器，后面的next()和send()方法都会接收生成器传出的值，send()还会传入一个值，next()默认传入None

### 通过生成器创建协程

```python
def consumer():
    send_to_p = ''
    while True:
        get_from_p = yield send_to_p
        print('consumer:', get_from_p)
        send_to_p = 'after: {}'.format(get_from_p)

def producer(c):
    c.send(None)
    for i in range(5):
        print('producer:', i)
        get_from_c = c.send(i)
        print(get_from_c)
    c.close()

c = consumer()
producer(c)
```

协程相比于普通函数的优势在于不同任务之间调度的`粒度更小`，而且不用像函数调用那样包含`大量的上下文`，比如上面的consumer生成器中，send_to_p等参数只是`局部变量`，仅仅保存在consumer的上下文中，这样在切换时能够节省资源

## yield from

yield from有两个作用，一个是接收生成器的`可迭代参数`，另一个是作为`委派生成器`，用作生成器和调用者之间的桥梁

### 接收可迭代参数

```python
def gen():
    yield from range(0, 5)

g = gen()
next(g)  # 启动生成器，也可以用send(None)
print(next(g))
print(next(g))
```

上面的函数将原来的gen生成器中带有循环的yield改写成了yield from一个可迭代对象，作用是相同的

区别在于使用yield from时，`不能通过send()`方法传值（可以send(None)启动）

### 委派生成器

在生成器调用者caller和生成器generator之间加入一个带有yield from语句的委派生成器，可以在caller与generator之间构建一个双向的传值通道，相比于直接调用（通过send()也可以传值），yield from处理了一些`默认的异常情况`，使得程序编写更加方便和简洁

比如下面的例子

```python
def averager():
    total = 0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total/count
    return (count, average)

def grouper(results, key):
    while True:
        results[key] = yield from averager()  # yield from 可以处理异常，直接得到生成器函数返回的结果

def caller(data):
    results = {}
    for key, values in data.items():
        group = grouper(results, key)
        next(group)
        for value in values:
            # 通过grouper送到了average()生成器的 term = yield 这里
            print(group.send(value))
        group.send(None)
    report(results)

def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(
            result[0], group, result[1], unit
        ))

data = { 'girls;kg': [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5], 
         'girls;m': [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43], 
         'boys;kg': [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3], 
         'boys;m': [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46], }

if __name__ == '__main__':
    caller(data)
```

caller()作为调用者，可以直接通过send()方法与生成器averager()进行值传递，传递的值grouper()完全不知情

注意当传入None时，averager()的循环结束，会抛出一个`StopIteration`异常，将return的值包含在StopIteration中，如果没有grouper()，就需要在caller()中`手动处理这个异常`，而通过yield from 语句就能够直接接收return的值