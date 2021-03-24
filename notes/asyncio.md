asyncio通过事件循环驱动的协程实现并发

在函数定义前加上async语句，就创建了一个协程

```python
async def coro():
    print('this is a coroutine')
```

协程的优势在于可以轻量的切换，这是通过await实现的

```python
async def a():
    print('this is a')
    await asyncio.sleep(2)

async def b():
    await a
    print('this is b')

asyncio.run(b())
```

上面的代码中，b()在运行到await语句时，将控制交给a()，不过这种方式只实现了`调度`，与普通的函数调用没什么区别，b仍然要等a运行2秒后才能继续运行，没有实现并发

asyncio.run(b())等价于下面的代码，作用是将协程添加到`事件循环`中，并开启循环

```python
loop = asyncio.get_event_loop()
loop.run_until_complete(b())
loop.close()
```

为了实现并发，需要在将协程注册成一个`task`：

```python
async def a():
    print('this is a')
    await asyncio.sleep(3)
    print('a over')

async def b():
    print('this is b')
    await asyncio.sleep(2)
    print('b over')

async def c():
    asyncio.create_task(a())
    await b()

asyncio.run(c())
```

create_task()是asyncio内置的函数，用于将协程注册成Task对象，并且`自动调度`，此时a和b能够实现并发运行

注意:

- 1.每个协程里面必须有await语句，否则就相当于普通函数，因为只有运行到await，当前函数才会`交出控制权`，才能实现协程的调度

- 2.asyncio.sleep(2)为事件循环添加一个`2秒后的call_back()`，执行到asyncio.sleep(2)会`立即`执行事件循环中的下一个事件，在`2秒后`通过call_back再回到当前协程，继续执行当前协程剩下的内容

- 3.注册成task后，运行逻辑是：`先运行`本函数内的代码，直到运行到`await`、`yield`或`return`，本函数被挂起，然后按`注册顺序`运行task，而当本函数运行完毕就`直接返回`，没运行完的task也将被`终止`，所以上面代码的输出为(a没有运行完就结束了)：

```
this is b
this is a
b over
```

注册task除了使用create_task()还可以使用gather()或wait()