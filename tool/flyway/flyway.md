# Flyway 配置

pom文件配置
```xml
<dependency>
    <groupId>org.flywaydb</groupId>
    <artifactId>flyway-core</artifactId>
    <!-- <version>xxx</version> 可以不指定版本，交由springboot来指定 -->
</dependency>
```


application.yml文件配置
```yml
spring:
  flyway:
    enabled: true                       # 默认开启
    locations: classpath:db/migration   # 默认迁移脚本目录 src/main/resources/db/migration
    baseline-on-migrate: true           # Flyway 会将数据库当前状态标记为 "baseline" 状态，意味着它认为当前数据库结构是第一个版本，从这个版本开始执行 Flyway 的后续迁移
```


迁移脚本的命名规则是 V<版本号>__<描述>.sql

