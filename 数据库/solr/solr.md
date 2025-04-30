# 运行环境

jre 1.8+

# 目录结构

* bin
    * solr 和 solr.cmd ：执行脚本，solr是linux下的脚本，solr.cmd 是windows下的脚本
    * post ：提供了用于发布内容到 Solr 的一个简单的命令行界面
    * solr.in.sh 和 solr.in.cmd ：配置文件
    * install_solr_services.sh : 用于linux将solr
* contrib ：包含 Solr 专用功能的附加插件
* dist ：包含一些 solr.jar 的jar包
* docs ：包括一个链接到在线 Javadocs 的 Solr
* example ：包括演示各种 Solr 功能的几种类型的示例
    * exampledocs ：这是一系列简单的 CSV、XML 和 JSON 文件，可以在首次使用 Solr 时使用bin/post
    * example-DIH ：此目录包含一些 DataImport Handler（DIH）示例，可帮助您开始在数据库、电子邮件服务器甚至 Atom 提要中导入结构化内容。每个示例将索引不同的数据集
    * files ：提供了一个基本的搜索 UI，可以用于文档（例如 Word 或 PDF）
    * films ：包含一组关于电影的强大数据，包括三种格式：CSV、XML 和 JSON
* licenses ： 包括了 Solr 使用的第三方库的所有许可证。
* server：
    * solr-webapp ：Solr 的 Admin UI
    * lib ：Jetty 库
    * logs ：日志文件
    * resources ：日志配置文件
    * server/solr/configsets ：示例配置


# solr脚本

启动
```sh
bin/solr start              启动solr，windows下使用solr.cmd
bin/solr start -cloud       以集群方式启动，可以简写为 -c
bin/solr start -d 目录      自定义目录，默认是 $SOLR_HOME/server，一般不会修改
bin/solr start -e           使用示例配置启动Solr，可用选项有
    cloud
    techproducts
    dih
    schemaless
bin/solr start -f           前台启动solr，使用-e得时候不能使用-f
bin/solr start -p 端口名     自定义端口，如果不指定，默认8983
bin/solr start -force


bin/solr restart        重启solr



```

```
./solr status           查看solr状态
./solr stop             停止solr，-p 指定关闭的端口，bin/solr stop -p 8983，-all停止所有
```


# solrCloud







