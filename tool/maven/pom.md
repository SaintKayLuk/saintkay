## pom

POM代表“项目对象模型”。它是Maven项目保存在名为的文件中的XML表示形式pom.xml。当有Maven人士在场时，谈到一个项目就意味着一种哲学意义，而不仅仅是包含代码的文件集合。一个项目包含配置文件，以及所涉及的开发人员及其所扮演的角色，缺陷跟踪系统，组织和许可证，项目所在的URL，项目的依存关系以及所涉及的所有其他小部分玩以赋予代码生命。它是与该项目有关的所有事情的一站式服务。实际上，在Maven世界中，一个项目根本不需要包含任何代码，只需包含一个pom.xml。

~~~ xml
<project>
    <!-- 声明此POM符合哪个版本的项目描述符 (必须)-->
    <modelVersion>4.0.0</modelVersion>

    <!--基础 -->
    <groupId> ... </groupId>
    <artifactId> ... </artifactId>
    <version> ... </version>
    <packaging> ... </packaging>
    <parent> ... </parent>
    <dependencies> ... </dependencies>
    <dependencyManagement> ... </dependencyManagement>
    <modules> ... </modules>
    <properties> ... </properties>

    <!--构建设置-->
    <build> ... </build>
    <reporting> ... </reporting>

    <!--更多项目信息-->
    <name> ... </name>
    <description> ... </description>
    <url> ... </url>
    <inceptionYear> ... </inceptionYear>
    <licenses> ... </licenses>
    <organization> ... </organization>
    <developers> ... </developers>
    <contributors> ... </contributors>

    <!--环境设置-->
    <issueManagement> ... </issueManagement>
    <ciManagement> ... </ciManagement>
    <mailingLists> ... </mailingLists>
    <scm> ... </scm>
    <prerequisites> ... </prerequisites>
    <repositories> ... </repositories>
    <pluginRepositories> ... </pluginRepositories>
    <distributionManagement> ... </distributionManagement>
    <profiles> ... </profiles>
</project>
~~~

## 基础

### maven坐标

~~~ xml
<groupId> ... </groupId>
<artifactId> ... </artifactId>
<version> ... </version>
~~~

* **groupId** 一般为公司的倒写
* **artifactId** 通常是已知项目的名称
* **version** 项目版本

### 打包

~~~ xml
<packaging> ... </packaging>
~~~

打包方式，默认是jar, 可以pom，jar，maven-plugin，ejb，war，ear，rar
父工程打包方式是pom

### 依赖

~~~ xml
<dependencies>
    <dependency>
        <groupId>junit</groupId>
        <artifactId>junit</artifactId>
        <version>4.12</version>
        <type>jar</type>
        <scope>test</scope>
        <optional>true</optional>
    </dependency>
    ...
</dependencies>
~~~

* **groupId,artifactId,version** 此三位一体用于及时计算特定项目的Maven坐标
* **type** 对应于所选的依赖类型。默认为jar
* **scope** 此元素引用手头任务的类路径（编译和运行时，测试等），以及如何限制依赖项的可传递性。有五个作用域：
  * compile 这是默认范围，如果未指定则使用。编译依赖项在所有类路径中均可用。此外，这些依赖项会传播到相关项目。
  * provided 这很像编译，但是表明您希望JDK或容器在运行时提供它。它仅在编译和测试类路径上可用，并且不可传递。
  * runtime -此作用域指示依赖关系不是编译所必需的，而是执行所必需的。它在运行时和测试类路径中，但不在编译类路径中。
  * test 此范围表明该依赖关系对于正常使用该应用程序不是必需的，并且仅在测试编译和执行阶段可用。它不是可传递的。
  * system 此范围类似于，provided除了必须提供显式包含它的JAR之外。该工件始终可用，并且不会在存储库中查找。

* **optional** 当此项目本身是依赖项时，将依赖项标记为可选，当**optional**为true时候，依赖不会传递
* **system** 当scope为system时，maven pavkage是默认不会将打包此依赖，这里我们以springboot的打包方式为例子

~~~ xml
<plugin>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-maven-plugin</artifactId>
    <!--把scope为system的依赖打包进jar -->
    <configuration>
        <includeSystemScope>true</includeSystemScope>
    </configuration>
</plugin>
~~~

#### 排除依赖

~~~ xml
<dependency>
    <groupId>org.apache.maven</groupId>
    <artifactId>maven-embedder</artifactId>
    <version>2.0</version>
        <exclusions>
            <exclusion>
                <groupId>org.apache.maven</groupId>
                <artifactId>maven-core</artifactId>
            </exclusion>
        </exclusions>
    </dependency>
~~~

#### 依赖管理

父级除了继承某些顶级元素外，还具有为子POM和传递依赖项配置值的元素。这些元素之一是dependencyManagement。

~~~ xml
<dependencyManagement>
    <dependencies>
        <dependency>...</dependency>
    </dependencies>
</dependencyManagement>
~~~

OM使用它来帮助管理其所有子级中的依赖项信息。如果my-parent项目用于dependencyManagement定义上的依赖项junit:junit:4.12，那么从该继承项继承的POM可以仅设置groupId= junit和artifactId= 来设置其依赖项，junit而Maven将由version父项填充该集合。这种方法的好处是显而易见的。可以在一个中央位置设置依赖项详细信息，该位置会传播到所有继承的POM。
注意，从传递性依赖项合并的工件的版本和范围也由依赖项管理部分中的版本规范控制。这可能会导致意外的后果。考虑在你的项目中使用了两个相关性的情况下，dep1和dep2。dep2反过来也使用dep1，并且需要特定的最低版本才能运行。如果随后使用dependencyManagement来指定较旧的版本，dep2将被迫使用较旧的版本，并且会失败。因此，您必须小心检查整个依赖关系树，以免发生此问题。

### 继承

#### 父工程

当此工程是父工程时，maven的packaging为pom

~~~ xml
<groupId> org.codehaus.mojo </groupId>
<artifactId> myparent</artifactId>
<version> 2.0 </version>
<packaging> pom </packaging>
~~~

#### 子工程

当pom为子工程时

~~~ xml
<parent>
    <groupId> org.codehaus.mojo </groupId>
    <artifactId> myparent</artifactId>
    <version> 2.0 </version>
    <relativePath> ../my-parent </relativePath>
</parent>
~~~

* relativePath 父工程的pom文件路径，不是必需的，但可以用作Maven的指示符，然后先搜索该项目的父级的给定路径，然后再搜索本地和远程存储库。

### 属性

Maven属性是值占位符，就像Ant中的属性一样。在POM中的任何地方都可以使用符号${X}，在X属性中访问它们的值。或者它们可以被插件用作默认值，例如：

~~~ xml
<properties>
    <maven.compiler.source> 1.8 </maven.compiler.source>
    <maven.compiler.target> 1.8 </maven.compiler.target>
    <project.build.sourceEncoding> UTF-8 </project.build.sourceEncoding>
    <project.reporting.outputEncoding> UTF-8 </project.reporting.outputEncoding>
</properties>
~~~

#### 五种属性风格

* **env.x** 系统环境变量，我们可以通过${env.PATH}来读取系统的属性，PATH为大写

~~~ xml
${env.JAVA_HOME}
~~~

* **project.x** pom文件的属性，可以读取pom文件内的属性，

~~~ xml
${project.basedir}：表示当前项目的根目录，即当前pom.xml文件所在的位置，还可以简化的写法：${basedir}
${project.version}：表示当前项目的版本，可以简写为：${version}
${project.parent.version} 表示父项目的版本，在子项目中可以使用此属性，来确保版本号的一致性
~~~

* **settings.x** 表示的路径settings.xml中包含相应元素的值。

* **java.x** Java系统属性：所有可通过java.lang.System.getProperties()访问的属性都可以作为POM属性使用，例如${java.home}。

* **x** pom中自定义属性，可以在pom中的任何位置访问，

~~~ xml
<properties>
    <test.test123>123</test.test123>
</properties>
~~~

可以在pom中通过${test.test123}来替代"123"

## 构建设置

### Build

#### BaseBuild
~~~ xml
<build> 
    <defaultGoal>install</defaultGoal> 
    <directory>${basedir}/target</directory> 
    <finalName>${artifactId}-${version}</finalName> 
    <filters> 
        <filter>filters/filter1.properties</filter>
    </filters> 
    ... 
</build>
~~~

* **defaultGoal** 
* **directory** 打包后文件存放路径，默认是${basedir}/target
* **finalName** 打包后的文件名，默认${artifactId}-${version}

#### Resources
~~~ xml
<resources>
    <resource>
        <targetPath>META-INF/plexus</targetPath>
        <filtering>false</filtering>
        <directory>${basedir}/src/main/plexus</directory>
        <includes>
            <include>configuration.xml</include>
        </includes>
        <excludes>
            <exclude>**/*.properties</exclude>
        </excludes>
    </resource>
</resources>
~~~

