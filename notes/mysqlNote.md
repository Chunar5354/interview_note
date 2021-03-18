## having和where的区别

where是约束声明，在结果返回前起作用

having时过滤声明，在结果返回之后起作用

where在聚合语句（sum,min,max,avg,count）`之前`执行，having在`之后`执行

## union

可以将多个select查询的结果`组合`到一个结果集合中

可以使用`union all`返回所有结果集，包含重复数据，`union dinstinct`不包含重复数据（union默认除去了重复数据，所以可以不加dinstinct）

## 时间计算函数

timestampdiff()，接收三个参数，第一个是要格式化到的`精度`（比如year, month, day）， 第二个是`小时间`，第三个是`大时间`

如

```
timestampdiff(month, '2019-11-02', '2020-5-12')
```

计算的就是2019年11月2日和2020年5月12日之间相差几个月份

## JOIN联结

通用句式`join on`：

```
tableA join tableB on ...
```

几种join：

- `inner join`(join)，只会查询出在A和B中都出现的内容

- `left join`会将左边的表（A）中的全部结果查询出来，如果B中没有匹配的内容，就设为null

- `right join`与left join相反

- 要选出两个表的全部内容可以采取`A left join B unoin A right join B`的形式

- 选出只在其中一个表里存在的内容可以通过 where 条件语句来判断某个字段是否为null，注意null的判断要使用`is`或`is not`而不是等号，如：

```sql
select a.id, a.name, b.classID 
from student as a left join score as b 
on a.id = b.id 
where b.id is NULL;
```

就能筛选出只在student表中而不在score表中的内容

## 窗口函数

为符合条件的所有记录都执行一个函数，比如row_number()，会为每一行添加序号

通用句式

```
function_name() over(partition... orer by...) as alias
```

over()中的是窗口函数应用的范围，partition类似于group by分组

应用示例（根据每一科目的成绩对学生分别排名）：

```sql
select classID, id, score, row_number() over (partition by classID order by score desc) ranking from score;
```

- row_number(), rank()和dense_rank()的区别

row_number不会有重复序号，rank有重复序号且有间隙，dense_rank有重复序号且没有间隙

如(100, 100, 90)进行排序，row_number得到的结果是`(1, 2, 3)`，rank得到的结果是`(1, 1, 3)`，dense_rank得到的结果是`(1, 1, 2)`

## 一些小技巧

- 可以复制同一张表（student as a inner join student as b）

> 查询不同课程成绩相同的学生的学生编号、课程编号、学生成绩

- 先where后group by后having

> 查询两门及其以上不及格课程的同学的学号，姓名及其平均成绩

- 查询嵌套，select的结果可以作为一个临时表，如：

```
select a.id
    from (select ...from ...) as a
```

> 查询课程编号为“0001”的课程比“0002”的课程成绩高的所有学生的学号
