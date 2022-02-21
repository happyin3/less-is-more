# Go Zero

# Raft in Go

## iota

iota是golang语言的常量计数器,只能在常量的表达式中使用。

iota在const关键字出现时将被重置为0(const内部的第一行之前)，const中每新增一行常量声明将使iota计数一次(iota可理解为const语句块中的行索引)。

使用iota能简化定义，在定义枚举时很有用。

### 参考文献

1. [Go iota 原理和源码剖析](https://www.lgolang.com/articles/74)

## sync.Mutex

## channel

## new, make

## struct{}, interface{}

## go

## defer

## Go构造函数

## time、time.NewTicker

## select