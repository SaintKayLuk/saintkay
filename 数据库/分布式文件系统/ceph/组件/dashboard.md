### dashboard
```sh
#添加用户，并指定角色，指定密码从文件
ceph dashboard ac-user-create <user_name> <role_name> -i password.txt

#查看所有用户
ceph dashboard ac-user-show
#查看用户admin的详细信息
ceph dashboard ac-user-show admin
#查看所有角色
ceph dashboard ac-role-show
#查看角色 administrator 的详细信息
ceph dashboard ac-role-show administrator
```