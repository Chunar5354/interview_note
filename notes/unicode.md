## Unicode

Unicode是一种字符集，用以消除全世界不同地区的字符编码差异

Unicode定长为`2字节`，可以表示65536个字符

Unicode有一个问题是可能造成空间浪费，如小于127号的ASCII字符，它们的`高八位全都是0`

## UTF-8

UTF-8是Unicode字符集的一种编码方式，它的优点是`可变长度`的编码方式

```
0xxxxxxx                             runes 0-127    (ASCII)
110xxxxx 10xxxxxx                    128-2047       (values <128 unused)
1110xxxx 10xxxxxx 10xxxxxx           2048-65535     (values <2048 unused)
11110xxx 10xxxxxx 10xxxxxx 10xxxxxx  65536-0x10ffff (other values unused)
```

对于0~127号的ASCII字符，只用一个字节就可以表示

而且`首字节的高位`决定了编码该字符所用的字节数，除了首字节的其他字节`最高2位固定是10`，这样就可以区分开来