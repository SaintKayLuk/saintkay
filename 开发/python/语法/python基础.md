## python基础


* 2.x和3.x两个版本，互不兼容
* 末尾不需要分号


## 命名规范

* 模块名(文件名)：都用小写字母，多个单词之间用下划线拼接，例如 my_module
* 类名：驼峰原则，且首字母大写，例 MyClass
* 方法名：同模块名一样，例如 my_method
* 变量名：同模块名一样，例如 my_variable
* 常量名：全都大写，多个单词之间用下划线拼接，例如  MY_CONSTANT

类，方法，变量前都可以加下划线，来标识是否私有，当然只是标识，不强制

## 模块、包

```py
#引入模块
import test_module

#引入模块，并取个别名
import test_module as test

#引起模块中的a变量
from test_modele import a

# from 包名，然后引入模块xxx
# abc.bcd 是包路径， xxx 则是bcd下的模块
from abc.bcd import xxx
```

python包相当于目录，但是包路径下默认有一个
```
__init__.py
```








