# 定时任务

~~~sql
查看是否开启事件调度器
SHOW VARIABLES LIKE 'event_scheduler';

开启
SET GLOBAL event_scheduler = 1;
关闭
SET GLOBAL event_scheduler = 0;

查看任务
SHOW EVENTS;
~~~