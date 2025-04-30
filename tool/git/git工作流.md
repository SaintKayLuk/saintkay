## git 工作流

* git flow
* github flow
* gitlab flow


### git flow

分支类型

* master
* develop
* feature
* hotfix
* release


分支合并流程图
```
master  ● -------------> ● --------------> ●
        ↓↘             ↗                  ↑
hotfix  ↓  ● --> ● --> ●  bugfix-xxx分支   ↑
        ↓              ↓                   ↑
release ↓              ↓        ● --> ● -- ● release-xxx分支
        ↘              ↓      ↗            ↓
develop   ● -------- > ● --> ● ----------> ●  
           ↘                 ↑
feature      ● ---> ● -----> ●  featrue-xxx分支
```

1. master 和 develop 长期存在，不会删除
2. master 存放对外发布的稳定代码
3. develop 存放开发的最新代码
4. feature 功能分支，从develop拉去，用于开发新功能，开发完合并进develop，一般命名为 feature-xxx
5. hotfix 从master拉去，用于线上bug紧急修复，修复完成合并进master和develop，一般命名为 bugfix-xxx
6. release 用于预发布，从develop 拉去，不再接受新功能，只提交bug修复，修复完合并进 master 和 develop，一般命名为 release-xxx



### github flow

分支类型
* master 
* 其他分支


分支合并流程图
```
其他分支    ● --> --> ● ----> ● (feature-xxx)
         ↗                    ↘
master  ● ---------------> ● --> ●
         ↘              ↗                 ↑
其他分支    ● --> ● --> ● (fixbug-xxx) 
```

1. master分支长期存在
2. 不区分补丁分支还是功能分支，需要自己命令
3. 发起 pull request 来合并分支进master，可以对此pull request发起讨论

### gitlab flow

分支类型
* master
* pre-production
* production


分支合并流程图
```
feature     ● --> ● --> ●
          ↗             ↘
master   ● --------------> ● 
                            ↘
pre-production ● -----------> ●   
                               ↘
production     ● --------------> ● 
```
1. 上游优先，只存在一个主分支master，是所有其他分支的上游，只有上游分支采纳的代码变化，才能应用到其他分支
2. 开发完成合并到master分支，自动ci到开发环境自测
3. 需要发布从master分支拉取release-xxx分支，部署到测试环境测试
4. 测试完 release-xxx 合并到 pre-production ，部署到预发布环境
5. 预发布环境测试完 合并到 production 分支，部署到生产环境
