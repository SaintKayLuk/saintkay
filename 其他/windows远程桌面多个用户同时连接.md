远程桌面连接默认只有一个用户可远程，当另一个用户通过远程连接登陆时，会挤掉前一个用户

---
1. 允许远程连接到此计算机，并选择可以远程到此计算机的用户
 控制面板 --> 系统和安全 --> 系统 --> 远程设置 --> 远程桌面 --> 允许远程连接到此计算机
再选择用户，把需要远程连接的用户添加进来
---
2. 打开组策略，修改RD连接数量
win + r 输入 gpedit.msc 打开组策略，并依次打开 计算机配置 --> 管理模板 --> Windows组件 --> 远程桌面服务 --> 远程桌面会话主机 --> 连接 --> 限制连接的数量
选择已启用，并在允许 RD 的最大链接数输入需要同时远程连接的数量，输个5个就够用
---
3. win10系统默认只能单用户远程桌面，需要修改termsrv.dll文件
termsrv.dll 位于 C:\Windows\System32 下
打开 powershell (管理员) ，然后键入一下命令

* 将文件所有者从TrustedInstaller更改为本地管理员组
```
takeown /F c:\Windows\System32\termsrv.dll /A
```
* 授予本地管理员组对termsrv.dll文件的“完全控制”权限
```
icacls c:\Windows\System32\termsrv.dll /grant Administrators:F
```
* 关闭远程桌面服务
```
net stop TermService
```
* 修改 termsrv.dll 文件
将文件拷贝出来，并且备份一份，通过命令 winver 查看系统版本，
Windows 10 x64 1909 39 81 3C 06 00 00 0F 84 D9 51 01 00
Windows 10 x64 1909 39 81 3C 06 00 00 0F 84 5D 61 01 00
Windows 10 x64 1909 39 81 3C 06 00 00 0F 84 5D 61 01 00
Windows 10 x64 1903 39 81 3C 06 00 00 0F 84 5D 61 01 00
Windows 10 x64 1809 39 81 3C 06 00 00 0F 84 3B 2B 01 00
Windows 10 x64 1803 8B 99 3C 06 00 00 8B B9 38 06 00 00
Windows 10 x64 1709 39 81 3C 06 00 00 0F 84 B1 7D 02 00

用Tiny Hexer打开文件，根据对应版本 找到匹配项，有可能后几位不一致，也不用管
替换为： B8 00 01 00 00 89 81 38 06 00 00 90 

修改完之后复制到原路径下 c:\Windows\System32\termsrv.dll 替换原文件

* 开启远程桌面服务
```
net start TermService
```

---
windows server版本只需要1，2步就可以同时多用户远程了
win10 版本需要1，2，3步才可以同时多用户远程
