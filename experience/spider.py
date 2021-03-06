from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import time

BASE_URL = 'https://www.nowcoder.com'

driver = webdriver.Chrome(executable_path="P:/selenium/chromedriver.exe")
driver.get('https://www.nowcoder.com/discuss/experience?tagId=2656')  # 对应的页面

# 等待ajax内容加载
wait = WebDriverWait(driver, 10)
wait.until(
    EC.presence_of_element_located((By.CLASS_NAME, "js-nc-wrap-link"))
)

def scrollPage(timeout, times):
    for i in range(times):
        print('next')
        # 向下刷新一次内容
        driver.execute_script("window.scrollTo(0,Math.max(document.documentElement.scrollHeight,document.body.scrollHeight,document.documentElement.clientHeight));")
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

