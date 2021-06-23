## mysql中explain各字段的解释

以下面这个查询为例：

```sql
explain select * from idx_study where a='1';
```

```
+------+-------------+-----------+------+---------------+-------+---------+-------+------+-----------------------+
| id   | select_type | table     | type | possible_keys | key   | key_len | ref   | rows | Extra                 |
+------+-------------+-----------+------+---------------+-------+---------+-------+------+-----------------------+
|    1 | SIMPLE      | idx_study | ref  | idx_a         | idx_a | 63      | const | 1    | Using index condition |
+------+-------------+-----------+------+---------------+-------+---------+-------+------+-----------------------+
```

### id

查询序号，id越大越先执行

### select_type

查询类型：

- SIMPLE，简单查询，不适用UNION或子查询

- PRIMARY，最外层的SELECT

- UNION，UNION查询中第二个及以后的查询

- DEPENDENT UNION，第二个或以后的查询取决于外层查询

- UNION RESULT，UNION的结果

- SUBQUERY，子查询的第一个SELECT

- DEPENDENT SUBQUERY，子查询的第一个SELECT，取决于外面的查询

- DERIVED，衍生表（FROM子句中的子查询）

- MATERIALIZED，物化子查询

### table

查询的表名

### type *

查询使用了哪种类型，可以判断查询的效率，很重要（从上到下效率依次变差）

- system，只有一行数据或空表（只能用于myisam和memory表）

- const，最多只有`一行`记录匹配，出现在联合主键或唯一索引的所有字段与`常量`比较时

- eq_ref，多表join时，对于前面表的每一行，在当前表中只能找到`一行`，当主键或唯一索引的`所有字段`都被join联结时使用

- ref，对于前面表的每一行，在当前表中匹配到`多行`，只用到索引的最左前缀或索引不是主键或唯一索引时使用

- fulltext，全文索引，全文索引的优先级很高，如果存在就会使用

- ref_or_null，在ref类型上增加了null值的比较

- index_merge，使用了两个或以上的索引，最后取交集或并集

- unique_subquery，用于where中的in形式子查询

- index_subquery，类似于unique_subquery，适用于非唯一索引

- range，索引`范围查询`，使用了不等号，BETWEEN，LIKE等

- index，索引`全表扫描`（如果是覆盖查询extra中会有using index）

- all，全表扫描

### possible_keys

查询可能用到的索引

### key

查询真正用到的索引

### key_len

查询用到的索引长度

### ref

- const，常数等值查询

- 使用联结查询时会显示关联字段

- func，使用了表达式或函数

### rows

mysql估算的需要扫描的行数，越小性能越好

### extra

- distinct，使用了distinct关键字

- using filesort，除了索引还使用了额外的排序操作，性能较差

- using index，覆盖索引

- using index condition，使用了ICP（Index Condition Pushdown），在存储引擎层用索引过滤数据，`减少二级索引回表次数`

- using where，查询的列未被索引覆盖，性能较差

- using temporary，使用了临时表，性能较差
