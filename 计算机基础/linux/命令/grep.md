## grep

```
grep [选项] 参数 [file/stdin] 
    -w      完全匹配一个字符串

```


例子：grep -w 示例
```
cat abc.txt

123123 abc abccd
22abbba dfg2332
sdabcd a1122dd 44

grep "abc" abc.txt      --> 结果2行
grep -w "abc" abc.txt   --> 结果匹配1行。只有单独 abc 那行被匹配

```

### 执行状态

一般通过 $? 获取上一次执行的返回值，0是正确，返回其他即错误

grep返回状态
```
0   匹配了至少一行
1   没有匹配任何行
2   匹配过程发生了错误
```

在set -e的情况下，没有匹配到任何行即会退出，


### 配合if条件

```sh
if grep -q "username" home.txt
```
