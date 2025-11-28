


repmgr standby clone --force --dry-run


# 停止服务
systemctl stop postgresql

# 删除数据目录（确认无误后执行）
rm -rf /var/lib/pgsql/13/data

# 从 shmc-plm-app2 克隆
repmgr -h 192.168.35.64 -U repmgr -d repmgr standby clone --force

# 启动服务
systemctl start postgresql

# 重新注册节点
repmgr standby register
