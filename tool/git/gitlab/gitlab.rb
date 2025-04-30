# 配置gitlab网址
external_url  'http://gitlab.saintkay.com'


#时区
gitlab_rails['time_zone'] = 'Asia/Shanghai'
# 用户默认可以创建group
gitlab_rails['gitlab_default_can_create_group'] = false
# 可以修改用户名
gitlab_rails['gitlab_username_changing_enabled'] = false



### 备份设置

# 备份文件保存目录
gitlab_rails['backup_path'] = "/var/opt/gitlab/backups"

# 备份保留时长，秒，为0则永久保留
gitlab_rails['backup_keep_time'] = 604800











# 开启邮件
gitlab_rails['gitlab_email_enabled'] = true
gitlab_rails['gitlab_email_from'] = 'example@example.com'

# 邮件SMTP设置，下面是阿里云邮箱的SMTP设置
gitlab_rails['smtp_enable'] = true
gitlab_rails['smtp_address'] = "smtp.qiye.aliyun.com"
gitlab_rails['smtp_port'] = 465
gitlab_rails['smtp_user_name'] = "你的邮箱"
gitlab_rails['smtp_password'] = "邮箱密码"
gitlab_rails['smtp_domain'] = "邮箱的域"
gitlab_rails['smtp_authentication'] = "login"
gitlab_rails['smtp_enable_starttls_auto'] = false
gitlab_rails['smtp_tls'] = true

# ssh端口
gitlab_rails['gitlab_shell_ssh_port'] = 22

# 进程数,默认CPU核心数加一,最小为2,不能为1,为1会卡死
unicorn['worker_processes'] = 2

# http端口,包括web页面和项目http的url,修改此项记得在external_url后面也加上端口号
nginx['listen_port'] = 80




# 启用 容器镜像库
registry_external_url 'https://registry.example.com'