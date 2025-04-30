## this


调用类的成员变量
```java
private String name;

public void setName(String name){
    this.name=name;
}
```

构造函数中调用构造函数，但只能放方法内第一行
```java
public class A {

    public A() {
    }
    
    public A(String s) {
        this();
    }

}
```