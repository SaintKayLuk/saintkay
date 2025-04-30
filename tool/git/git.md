

* 工作区
* 暂存区
* 本地仓库
* 远程仓库

修改和新增文件都会在工作区，通过git add 添加到暂存区
暂存区文件通过git commit 提交到本地仓库
本地仓库可以通过git push 把commit 推到远程仓库
一个本地仓库可以对应多个远程仓库

```
        git add          git commit           git push
工作区  ---------> 暂存区 -----------> 本地仓库 ---------> 远程仓库
        <--------                             
        git reset                                
```

### 配置文件

全局配置文件 ~/.gitconfig
仓库配置文件，根目录下 .git 目录下的 config 文件

### git命令

```sh
git --version       #查看git版本   
git init            #初始化一个本地仓库
git status          #查看git索引，即哪些文件被暂存了，哪些文件没有暂存，可以显示所有没有commit的文件
    -s/--short      #短格式显示
    --ignored       #显示忽略文件

git clone           #克隆一个远程仓库到本地
    --branch xxx    #克隆哪个分支，默认 master 分支  
    --depth x       #克隆深度，可以指定克隆深度，即最近的几次commit
#例：克隆远程仓库 test 分支的一次深度
git clone --branch test --depth 1 https://xxx     
```

git配置命令
```
git [--global] config [命令]                #git 配置文件   
git config user.name                        #查看当前仓库 commit的name
git config user.name "your name"            #设置当前仓库 commit的name
git config --global user.name               #查看全局commit的name
git config --global user.name "your name"   #设置全局commit的name
git config --global key value               #设置全局参数
git config --global --unset key             #取消全局参数
```


```sh
git add xxx         #添加文件或目录到暂存区
git commit xxx      #提交文件到仓库


git reset --hard HEAD~2         #撤销两个commit
git reset --hard <commit_id>    #回滚到指定commit
git push            #推送本地commit到远程仓库
```







#### git目录和工作目录


git目录为根目录下的 .git目录，为项目存储所有历史和元信息的目录

~~~
HEAD        当前项目处于哪个分支
config      项目配置信息，git config命令修改的就是此文件
description 项目描述信息   
index       索引文件
hooks/      系统默认钩子脚本目录    
logs/       各个refs的历史信息
objects/    Git本地仓库的所有对象 (commits, trees, blobs, tags)
refs/       标识项目里的每个分支指向了哪个提交(commit)
~~~

工作目录为根目录下除了 .git 其他文件，文件夹，即当前分支的文件，切换分支时，内容会变化，所有历史信息都保存在 git目录 中



~~~
git status          查看没有commit的文件的状态
git diff            查看没有添加到暂存区的修改内容
git diff --cached   查看暂存区中的修改的内容
~~~

##### 分支

~~~

git branch          查看分支，前面带 * 的是当前分支
    -a              查看所有分支，包括远程分支
    -d xxx          删除 xxx 分支
    -D xxx          强制 xxx 删除

git branch xxx      从当前分支创建新分支，分支名为 xxx
git checkout xxx    切换到 xxx 分支
~~~








cherry-pick 检出某个commit


























