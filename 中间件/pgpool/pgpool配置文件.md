



```sh
su - postgres
mkdir ~/.ssh && chmod 700 ~/.ssh
ssh-keygen -t rsa -f ~/.ssh/id_rsa_pgpool


# id_rsa_pgpool.pub 文件的内容复制到 其他几台的 authorized_keys 中
```
**注意：postgres用户的家目录是 /var/lib/postgresql**
验证一下
```sh
ssh -p 22 postgres@x.x.x.x -i ~/.ssh/id_rsa_pgpool
```










## 配置文件修改


如果要启用 watchdog 设置，先判断下 arping 命令是否存在，如果没有则安装
```sh
apt install arping -y
```



```conf
backend_clustering_mode = 'streaming_replication'

# 设置 * 则同时监听 ipv4 和 ipv6 ，设置 0.0.0.0 则只监听 ipv4
listen_addresses = '0.0.0.0'
pcp_listen_addresses = '0.0.0.0'

# 设置两个后端
backend_hostname0 = 'host1'
backend_port0 = 5432
backend_weight0 = 1
backend_flag0 = 'ALLOW_TO_FAILOVER'
backend_application_name0 = 'server0'

backend_hostname1 = 'host2'
backend_port1 = 5433
backend_weight1 = 1
backend_flag1 = 'ALLOW_TO_FAILOVER'
backend_application_name1 = 'server1'


# 跳过pgpool的密码验证，直接让pgsql 来验证密码
allow_clear_text_frontend_auth = on     


# 健康检查
health_check_period = 30        # 健康检查间隔
health_check_user = 'xxx'
health_check_password = 'xxx'


# 流复制检查
sr_check_period = 10            # 检查流式复制延迟的时间间隔
sr_check_user = 'xxx'
sr_check_password = 'xxx'


# 看门狗，至少3个pgpool节点
use_watchdog = on
trusted_servers = 'xx,xx,xx'    # 填写 pgpool 节点的ip，用 , 分隔 

# 三个pgpool节点
hostname0 = 'x.x.x.x'
wd_port0 = 9000
pgpool_port0 = 9999
hostname1 = 'x.x.x.x'
wd_port1 = 9000
pgpool_port1 = 9999
hostname1 = 'x.x.x.x'
wd_port1 = 9000
pgpool_port1 = 9999


# 虚拟ip设置 , eth0 根据实际网卡修改
delegate_ip = 'x.x.x.x'
if_up_cmd = '/usr/bin/sudo /sbin/ip addr add $_IP_$/24 dev eth0 label eth0:0'
if_down_cmd = '/usr/bin/sudo /sbin/ip addr del $_IP_$/24 dev eth0'
arping_cmd = '/usr/bin/sudo /usr/sbin/arping -U $_IP_$ -w 1 -I eth0'
```




