创建其他项目来创建 kas的agent 和 gitlab-ci文件


## 设置kas

## 设置gitlab-ci.yml

如果在同一个gitlab里

这在当前项目配置ci文件路径为 my/path/.my-custom-file.yml@namespace/sub-group/another-project

格式为
项目内路径@组名/子组名/项目名

例如：另一个组 gitlab下的gitlab-ci项目，下的 wms/account/.gitlab-ci.yml
```
wms/account/.gitlab-ci.yml@gitlab/gitlab-ci
```