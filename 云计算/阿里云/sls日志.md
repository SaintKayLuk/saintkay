## dotnet应用使用sls日志




dotnet服务部署在阿里云ack上，使用阿里云的sls来收集日志，因为dotnet默认打的日志带  ANSI 转义序列，而显示的时候不能识别，加上多行日志的区分

所以需要需要行首匹配和 字符串替换处理

日志格式，带ansi颜色
```sh
# info
^[[40m^[[32minfo^[[39m^[[22m^[[49m
#warn
^[[40m^[[1m^[[33mwarn^[[39m^[[22m^[[49m
```

1. 多行日志设置行首匹配正则
行首匹配正则
```
匹配前面部分
^(\x1b\[[0-9;]*m)*(dbug|info|warn|fail)

或者，完整匹配

^(\x1b\[[0-9;]*m)*(dbug|info|warn|fail)\x1b\[39m\x1b\[22m\x1b\[49m
```


2. 处理模式添加字符串替换

例：如下，如果有其他级别，再添加，比如warn等
```
原始字段        content
匹配方式        正则表达式匹配
匹配内容        ^(\x1b\[[0-9;]*m)*info\x1b\[39m\x1b\[22m\x1b\[49m
替换内容        INFO
```

处理插件需要按顺序，字符串替换的时候需要勾选
<div style="border: 1px solid black; padding: 5px; display: inline-block; font-size: 10px;">✓</div> 原始字段缺失报错<br/>
<div style="border: 1px solid black; padding: 5px; display: inline-block; font-size: 10px;">✓</div> 正则不匹配报错<br/>
<div style="border: 1px solid black; padding: 5px; display: inline-block; font-size: 10px;">✓</div> 保留原始字段<br/>
<div style="border: 1px solid black; padding: 5px; display: inline-block; font-size: 10px;">✓</div> 解析失败保留原始字段<br/>



3. 处理模式添加提取字段，按顺序添加在最后
```
原始字段    content
正则表达式  ^(DEBUG|INFO|WARN|ERROR)
结果字段    log_level
```






## ram用户只查看某个logstore的权限，先创建个ram用户，然后添加自定义权限，权限策略如下，替换 project_name 和 logstore_name

模板为添加2个 logstore 的
```yaml
{
  "Version": "1",
  "Statement": [
    {
      "Action": [
        "log:ListProject"
      ],
      "Resource": "acs:log:*:*:project/*",
      "Effect": "Allow"
    },
    {
      "Action": [
        "log:List*"
      ],
      "Resource": [
        "acs:log:*:*:project/${project_name}/logstore/*",
        "acs:log:*:*:project/${project_name}/logstore/*"
      ],
      "Effect": "Allow"
    },
    {
      "Action": [
        "log:Get*",
        "log:List*"
      ],
      "Resource": [
        "acs:log:*:*:project/${project_name}/logstore/${logstore_name}",
        "acs:log:*:*:project/${project_name}/logstore/${logstore_name}",
        "acs:log:*:*:project/${project_name}/logstore/${logstore_name}",
        "acs:log:*:*:project/${project_name}/logstore/${logstore_name}"
      ],
      "Effect": "Allow"
    },
    {
      "Action": [
        "log:Get*",
        "log:List*"
      ],
      "Resource": [
        "acs:log:*:*:project/${project_name}/dashboard",
        "acs:log:*:*:project/${project_name}/dashboard",
        "acs:log:*:*:project/${project_name}/dashboard/*",
        "acs:log:*:*:project/${project_name}/dashboard/*"
      ],
      "Effect": "Allow"
    },
    {
      "Action": [
        "log:Get*",
        "log:List*"
      ],
      "Resource": [
        "acs:log:*:*:project/${project_name}/savedsearch",
        "acs:log:*:*:project/${project_name}/savedsearch",
        "acs:log:*:*:project/${project_name}/savedsearch/*",
        "acs:log:*:*:project/${project_name}/savedsearch/*"
      ],
      "Effect": "Allow"
    }
  ]
}
```