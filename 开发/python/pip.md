# pip

python的包管理器，相当于java的maven

## pip 管理python包
#### 安装/卸载 包
```sh
# 安装包，默认安装最新版本
pip install <package_name>
# 从指定地址下载包
pip install <package_name> -i <下载地址>
# 安装特定版本的包
pip install <package_name>==<version_number>

# 安装一个本地的包，把本地的一个包安装到环境里
pip install /path/package_name

# 卸载包
pip uninstall <package_name>
```

#### 升级包
```
pip install --upgrade <package_name>
```

#### 查看包
```sh
# 查看所有安装的包
pip list

# 查看包的详细信息
pip show <package_name>
```

#### 导出/导入 包
```sh
# 导出包和对应版本号到 requirements.txt 文件中
pip freeze > requirements.txt

# 从文件中安装指定的包
pip install -r requirements.txt
```

requirements文件格式
```
package_name==version_number
package_name==version_number
package_name==version_number
package_name==version_number
...
```



## 升级pip
```sh
python3 -m pip install --upgrade pip
```

#### 

更换源
```
pip config set global.index-url <url>
```

清理缓存
```
pip cache purge
```