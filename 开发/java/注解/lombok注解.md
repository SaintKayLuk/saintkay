# @Getter

为属性自动添加get方法

# @Setter

为属性自动添加set方法

# @ToString

重写 toString 方法

# @EqualsAndHashCode

重写 equals 和 hashCode 方法

# @NoArgsConstructor

生产一个无参构造方法

# @AllArgsConstructor

生成一个全部参数的构造方法

# @RequiredArgsConstructor

生成一个包含特定参数的构造方法
特定参数指 final 修饰的成员变量


# @Data

组合包，等同于下面这些注解的集合
* @Getter
* @Setter
* @ToString
* @EqualsAndHashCode
* @RequiredArgsConstructor


# @Value

组合包，等同于下面这些注解的集合
并且设置所有的成员变量为 final

* @Getter
* @ToString
* @EqualsAndHashCode
* @AllArgsConstructor



# @Builder

方便的实现建造者模式


示例用法：
```java
@Builder
public class A {
    
    String name;
    int age;

    void method(){
        A a = A.builder()
               .name("saintkay")
               .age(18)
               .build();
    }
}
```

## @Builder.Default

使用@Builder注解，构建的对象，不设置值，则属性为null，可以设置默认值、


例：如果age属性不添加 @Builder.Default 注解，那赋值 18 没有效果，如果在 method 方法中没有初始化 age 变量的值，则创建的 a 对象的 age 为null
```java
@Builder
public class A {

    String name;
    @Builder.Default
    int age = 18;

    void method() {
        A a = A.builder()
               .name("saintkay")
               .build();
    }
}
```

# @SuperBuilder

@build 注解 子类不能在builder()方法中构建父类的属性，可以通过 @SuperBuilder 来使用
父类和子类都需要添加 @SuperBuilder 注解

```java
@SuperBuilder
public class A {
    String name;
}

@SuperBuilder
class B extends A {
    int age;
    
    void method() {
        B b = builder().name("saintkay")
                       .age(18)
                       .build();
    }
}
```


# @Slf4j

自动生成该类的 log 静态常量

示例：
```java
@Slf4j
public class A {}    
```
等同于
```java
public class A {
    private static final Logger log= LoggerFactory.getLogger(A.class);
} 
    
```
