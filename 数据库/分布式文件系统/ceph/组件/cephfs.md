### cephfs
```sh

#创建一个文件存储，名为 fs-test
ceph fs volume create fs-test

#创建一个文件存储，并指定 metadata的pool的名字 和 data的pool的名字
#需要事先创建好 metadata的pool 和 data 的 pool
ceph fs new cephfs cephfs_metadata cephfs_data
#查看文件存储
ceph fs ls

#删除文件存储，删除之前需要先停mds或者删除mds
ceph fs rm fs-test --yes-i-really-mean-it


#挂载
mount -t ceph 192.168.3.34:6789:/haha /mnt/haha -o name=admin,secret=AQBXXSFkL5ubOhAAnhYFnqWRtrwaJBmaCKL2+w==
# -t ceph   指定挂载类型
# -o 添加ceph的用户和密码

```