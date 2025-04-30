## instanceof

使用 instanceof 关键字判断一个对象是否为一个类（或接口、抽象类、父类）的实例

```java
public class A extends B {
    
    public static void main(String[] args) {
        
        //父类引用指向子类实例
        B b = new A();
        
        //判断实例b是否可以向下转型为A的实例
        if (b instanceof A){
            System.out.println("b可以向下转型为A");
            //可以强转为A的实例
            A a = (A) b;
        }
    }
}

```