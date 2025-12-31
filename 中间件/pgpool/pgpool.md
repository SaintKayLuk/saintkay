



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


```conf
backend_clustering_mode = 'streaming_replication'
listen_addresses = '*'


# 配置多个后端地址
backend_hostname0 = 'host1'
backend_port0 = 5432
backend_weight0 = 1
#backend_data_directory0 = '/data/postgresql/15/main'
backend_flag0 = 'ALLOW_TO_FAILOVER'
backend_application_name0 = 'server0'

backend_hostname1 = 'host2'
backend_port1 = 5433
backend_weight1 = 1
#backend_data_directory1 = '/data/postgresql/15/main'
backend_flag1 = 'ALLOW_TO_FAILOVER'
backend_application_name1 = 'server1'


enable_pool_hba = on
pool_passwd = '/etc/pgpools2/pool_passwd'
allow_clear_text_frontend_auth = on      



sr_check_user = 'xxx'
sr_check_password = 'xxx'


health_check_period = 10
health_check_timeout = 20
health_check_user = 'xxx'
health_check_password = 'xxx'


```










