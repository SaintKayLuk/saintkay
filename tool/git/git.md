### git配置

#### version
~~~
git --version       查看git版本         
~~~



#### config

全局配置文件 ~/.gitconfig
仓库配置文件，根目录下 .git 目录下的 config 文件


~~~
git config          修改git配置
    --global        带此参数，修改的是全局配置，即修改的是 ~/.gitconfig 文件
    --list          查看所有配置

例：查看所有配置
git config --list
~~~

~~~
例：
git config user.name                        查看当前仓库 commit的name
git config user.name "your name"            设置当前仓库 commit的name
git config --global user.name               查看全局commit的name
git config --global user.name "your name"   设置全局commit的name
~~~


### Getting and Creating Projects

#### init
~~~
git init            创建一个空的git仓库或者重新初始化一个现有的仓库     
~~~
#### clone 
~~~
git clone           将存储库克隆到新目录
    --branch xxx    新建的HEAD指向 xxx 分支，默认指向 master 分支  
    --depth x       克隆深度，可以指定克隆深度，即最近的几次commit


例：克隆远程仓库 test 分支的一次深度
git clone --branch test --depth 1 https://xxx                  
~~~
 
### Basic Snapshotting

#### add
将文件添加到git 索引中，即暂存区中，即交给git来管理，被追踪文件
~~~
git add xxx
    -f 
      --force 强制添加被hu

例：添加当前目录下的所有没有被追踪的文件到 git 索引中，取决于执行 git 命令的所在目录
git add .
例：添加当前目录下的 abc 目录
git add abc/
~~~

#### status

通过 git status 查看git索引，哪些文件被暂存了(就是在你的Git索引中), 哪些文件被修改了但是没有暂存, 还有哪些文件没有被跟踪(untracked).
git status 不显示已经被commit的文件，而显示没有被追踪或者修改了没有提交的文件
~~~
git status
    -s 
      --short   短格式显示
    --ignored   显示忽略文件
~~~


~~~shell
例:
$ git status

On branch master
Your branch is up to date with 'origin/master'.

Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)

        new file:   abc

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

        modified:   bcd

Untracked files:
  (use "git add <file>..." to include in what will be committed)

        .idea/

On branch master:                   当前在master分支
Changes to be committed:            已经添加到暂存区的文件    
Untracked files:                    没有被追踪的文件，即不被git管理的文件
~~~


#### diff


#### commit


ff
f
f
f
ff
f
f
f
f
f
f
ff
fd

dsfg
dfg
dfs
gds
gfds
gdfs
gds
f
dfsgf
dsg
dfs
g
dfsg
s
dfg
dfs
gds
sdfg
dsf
#### git对象模型




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



#### git基本用法

提交代码流程
1. clone或者init一个仓库
2. git add，添加新文件或者修改内容到暂存区，(也可以是git索引中)，新增文件必须git add
3. git commit 将暂存区的修改内容，或者不在暂存区的修改内容提交到本地仓库
4. git push 将commit推送到远程仓库

~~~
git clone git://git.example.git   通过ssh克隆一个仓库
git clone http://example.git      通过http克隆一个仓库
git init                          初始化一个仓库，在当前目录下生成一个 .git 目录
~~~
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




##### 合并

~~~
git merge xxx         把 xxx 分支合并到当前分支
~~~


#### git历史

~~~
git log

~~~






























