当对一个数据页进行更新时，如果数据页在内存中，可以直接更新，否则需要从磁盘中将这个数据页读到内存再更新，磁盘IO的开销比较大，所以innodb提供了change buffer机制

使用change buffer机制时，如果要更新的数据页不在内存中，innodb并不会从磁盘读取数据，而是将`更新操作`缓存在change buffer中，在`下次`需要访问这个数据页的时候，将数据页读入内存，然后执行change buffer中对于这个页的操作，这个过程称为`merge`

merge可以发生在下一次访问时，`后台`线程也会定期merge，`数据库关闭时`也会进行merge

change buffer是可以持久化的数据，能够被保存到磁盘上

change buffer的目的就是减少磁盘的`读`（相比于redo log主要是减少了磁盘的`随机写`）

change buffer所做的操作会记录到redo log中

## 唯一索引与普通索引

对于唯一索引，每次更新都要判断表中是否已经包含要插入的行，所以一定要将数据页读入内存才可以判断，所以`不会使用`到change buffer

change buffer只能在普通索引上使用，所以在不影响业务的前提下，最好使用普通索引来减少磁盘的读IO