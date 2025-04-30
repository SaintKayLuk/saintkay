## import

导入其他包中的类，接口等
使用import之后可以直接使用类名或者方法名来使用，而不需要使用全路径

语法
```java
//直接指定需要导入的类
import java.util.List;
import java.util.Set;

//导入对应包下的所有类
import java.util.*;
```

注意：* 只能导入当前包目录下的，不能导入子包下的
```java
//没有指定到 java.util 则找不到 java.util 包下的 类
import java.*;
```



## import static

导入静态变量和方法
能直接使用，而不需要指定类名等

```java
//导入的时候直接指定到静态变量和方法
import static B.i;
import static B.method;
public class A {
    public static void main(String[] args) {
        //使用的时候不需要指定类名，直接使用变量和方法
        i
        method()
    }
}

    

public class B{
    static int i;
    public static void method() {
    }
}
```
