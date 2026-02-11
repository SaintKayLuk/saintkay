

默认用户名密码 Admin/zabbix

## 添加监控的主机




## 报警发送到钉钉机器人

#### 添加媒介

管理 - 媒介 - 创建媒介类型

```
名称：      DingTalk
类型：      脚本
脚本名称：  dingding.py

脚本参数
{ALERT.SENDTO}
{ALERT.SUBJECT} 
{ALERT.MESSAGE}
```
**脚本存放路径，默认 /usr/lib/zabbix/alertscripts**

#### 用户绑定媒介

管理 - 用户 - 点进用户"Admin" - 报警媒介

添加报警媒介
```
类型：      选择刚刚创建的 DingTalk
收件人：    随意填写
```

#### 配置 触发器动作

配置 - 动作 - 触发器动作 - 创建动作


**配置动作：**
```
名称：  Send To DingTalk
条件：  触发器示警度 - 大于等于 - 一般严重 （测试的话可以选择所有）
```

**配置操作：**

1. 添加操作：
```
操作：          发送消息
发送给用户：    选择绑定媒介的用户，例如前面操作的Admin
仅送到：        DingTalk
自定义消息内容  ✅
```

主题
```
🚨 {TRIGGER.SEVERITY} | {EVENT.NAME}
```
消息
```
### 🚨 Zabbix 告警通知

**主机**：{HOST.NAME}  
**IP**：{HOST.IP}  
**告警级别**：{TRIGGER.SEVERITY}  
**触发器**：{TRIGGER.NAME}

<font color=#FF0000>**当前值**：{ITEM.NAME} = {ITEM.LASTVALUE}</font>

**触发时间**：{EVENT.DATE} {EVENT.TIME}
```



2. 添加恢复操作：
```
操作：          发送消息
发送给用户：    选择绑定媒介的用户，例如前面操作的Admin
仅送到：        DingTalk
自定义消息内容  ✅
```

主题
```
✅ 已恢复 | {EVENT.NAME}
```

消息
```
### ✅ Zabbix 告警恢复

**主机**：{HOST.NAME}  
**触发器**：{TRIGGER.NAME}

**恢复时间**：{EVENT.RECOVERY.DATE} {EVENT.RECOVERY.TIME}
```




