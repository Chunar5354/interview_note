俗话说：“知己知彼，百战不殆”，在准备面试的过程中，大家基本都会在网上搜集前辈们的面经，借此来了解各个公司在面试过程中常常提问的问题，这样就能够针对性的做出准备

那你想不想知道，在某个领域，最常被提问到的知识点是什么呢？使用Python编程，通过爬虫+分词就能很容易的实现这一目标

## 1.爬取面经

以[牛客网](https://www.nowcoder.com/)为例

首先打开面经汇总页面

[![6m0o9g.png](https://s3.ax1x.com/2021/03/05/6m0o9g.png)](https://imgtu.com/i/6m0o9g)

找到自己感兴趣的领域或者公司，这里我选择了golang

[![6mD3QJ.md.png](https://s3.ax1x.com/2021/03/05/6mD3QJ.md.png)](https://imgtu.com/i/6mD3QJ)

点开之后发现面经内容相关的部分是通过Ajax加载的，如果直接爬取页面是得不到这些内容的

读取Ajax可以使用Python的[selenium](https://selenium-python.readthedocs.io/)库，通过`WebDriverWait`方法可以等待Ajax加载之后再读取内容

具体实现如下:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome(executable_path='C:/user/selenium/chromedriver.exe')  # 自己的chromedriver位置
driver.get('https://www.nowcoder.com/discuss/experience?tagId=2656')  # 对应的页面url

# 等待ajax内容加载
wait = WebDriverWait(driver, 10)
# 一直等到 class='js-nc-wrap-link'(对应页面的ajax部分)加载出来
wait.until(
    EC.presence_of_element_located((By.CLASS_NAME, 'js-nc-wrap-link'))
)
```

- 注意，由于selenium要调用浏览器，所以首先要下载对应浏览器的驱动，这部分在selenium官方文档中有详细说明

等Ajax加载完毕，就可以获得每一条面经对应的链接了，不过每次打开页面，默认只会显示20几条内容，需要向下刷新页面才能继续加载，所以为了一次性能所爬取一些内容，需要一个模拟页面下滑的函数：

```python
def scrollPage(timeout, times):
    for i in range(times):
        print('next')
        # 向下刷新一次内容
        driver.execute_script('window.scrollTo(0,Math.max(document.documentElement.scrollHeight,document.body.scrollHeight,document.documentElement.clientHeight));')
        time.sleep(timeout)
```

两个参数，timeout指的是隔多久向下刷新一次，times指的是一共刷新几次，可以按照自己的需要来改动

等到页面信息全加载出来，爬取的方式就很多了，我用的是[beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)，整个爬虫的代码如下：

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import time

BASE_URL = 'https://www.nowcoder.com'

driver = webdriver.Chrome(executable_path='P:/selenium/chromedriver.exe')
driver.get('https://www.nowcoder.com/discuss/experience?tagId=2656')  # 对应的页面

# 等待ajax内容加载
wait = WebDriverWait(driver, 10)
wait.until(
    EC.presence_of_element_located((By.CLASS_NAME, 'js-nc-wrap-link'))
)

def scrollPage(timeout, times):
    for i in range(times):
        print('next')
        # 向下刷新一次内容
        driver.execute_script('window.scrollTo(0,Math.max(document.documentElement.scrollHeight,document.body.scrollHeight,document.documentElement.clientHeight));')
        time.sleep(timeout)

# 以3秒的间隔向下刷新5次内容
scrollPage(3, 5)

# 带有 class='js-nc-wrap-link' 属性的标签都是面经的链接
items = driver.find_elements_by_class_name('js-nc-wrap-link')

with open('content.txt', 'w', encoding='utf-8') as f:
    # 逐个读取每一个链接中的文本，并写到文件里面
    for item in items:
        print(item.get_attribute('data-href'))
        response = requests.get(BASE_URL + item.get_attribute('data-href'))
        data = response.text
        soup = BeautifulSoup(data, 'html.parser')
        words = soup.find('div', {'class': 'post-topic-des nc-post-content'})
        f.write(words.get_text())
```

## 2.分词统计

在上一节中，我们爬取到了想要的面经内容，并以文本的形式保存到了文件中，有了这个文件，就可以统计其中的词频

我这里使用Python的[jieba](https://github.com/fxsjy/jieba)库来实现分词

```python
import jieba

# 读取文本内容
with open('content.txt', 'r', encoding='utf-8') as f:
    data = f.read()

# 分词
count = jieba.lcut(data)
word_count={}
for word in count:
    if len(word) == 1:  # 去掉标点符号等无意义的字符
        continue
    word_count[word] = word_count.get(word, 0) + 1

# 按词频对分词进行排序
items = list(word_count.items())
items.sort(key=lambda x: x[1], reverse=True)

# 将词频写入文件
with open('freq.txt', 'w', encoding='utf-8') as f:
    for item in items:
        f.write(str(item)+'\n')
        if item[1] <= 2:  # 出现2次以下的不写入
            break
```

于是就得到了词频统计文件`freq.txt`

[![6myBSU.png](https://s3.ax1x.com/2021/03/05/6myBSU.png)](https://imgtu.com/i/6myBSU)

可以看到对于golang来说，面试中最常出现的考点是“项目”、“算法”以及“进程”等等（没用的词语太多了，可以通过设置一些停用词来去掉诸如“什么”，“一个”这些没有意义的词语）

如果想美观一点还可以弄成表格或者词云图之类的