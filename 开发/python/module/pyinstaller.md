

pyinstaller xxx.spec

```
# 从从指定的包或模块中收集所有子模块
  --collect-submodules module_name
```                     


```
pyinstaller.exe -F -w --collect-submodules=pydicom -i .\dcm\braineuroo.ico main.py

-F 打包成一个文件
-w 不出现黑窗口
-i xxx 指定exe的图标
```