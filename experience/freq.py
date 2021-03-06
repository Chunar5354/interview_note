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
        if item[1] <= 2:  # 出现次数小于2的不写入
            break