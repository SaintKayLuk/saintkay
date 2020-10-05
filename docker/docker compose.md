# 安装docker compose
方式一
~~~
curl -L https://github.com/docker/compose/releases/download/1.24.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose
~~~
方式二
~~~
yum -y install epel-release
yum -y install python-pip
pip install docker-compose
~~~
方式三
直接github下载文件
放 /usr/local/bin/下改名为docker-compose
chmod +x /usr/local/bin/docker-compose


https://docs.docker.com/compose/compose-file/

docker-compose.yml 例子

四个顶级键：必须有version和services，networks和volumes可选
version: 
services:
networks:
volumes:

stack模式下
configs:
secrets:

~~~yml
version: "3.7"                   #compose文件版本
services:                        #服务
  service_name:                  #服务名
    image: nginx:1.7             #镜像
    container_name: mynginx      #容器名字，stack方式下忽略此项
    hostname: foo                #容器的hostname
    
    logging:                     #容器日志
      driver: "json-file"        #
      options:                   #
        max-size: "200k"         #单个日志文件最大200k 
        max-file: "10"           #日志文件最多10个，超出后重新覆盖
    
    ports: 
      - target: 80               #容器内的端口
        published: 80            #公开端口
        protocol: tcp            #端口协议（tcp或udp）
        mode: host               #host(用于在每个节点上发布主机端口)/ingress使群集模式端口达到负载平衡
    
    config:                      #配置文件
      - source: my_config        #docker中创建的配置文件名称
        target: /etc/my_config   #容器内的配置文件
        mode: 0444               #服务的任务容器中装入的文件的权限，默认0444

    secrets:
      - source: my_secret        #docker中创建的secret名称
        target: my_secret        #secret在容器中的名称，/run/secret/my_secret
        mode: 0444               #服务的任务容器中装入的文件的权限，默认0444

    deploy:                      #docker stack deploy方式启动需要的参数
      mode: replicated           #global/replicated(默认)  global每个节点起一个容器，replicated指定数量
      endpoint_mode: vip         #vip/dnsrr 创建虚拟ip
      replicas: 5                #mode为replicated时候指定的容器数量
      
      restart_policy:            #重启策略
        condition: on-failure    #none/on-failure/any(默认) 
        delay: 5s                #重启等待时间，默认0
        max_attempts: 3          
        window: 120s                    
      
      rollback_config:           #更新失败的情况下回滚服务配置
        parallelism: 1           #一次要回滚的容器数。如果设置为0，则所有容器将同时回滚
        delay: 30s               #每个容器组回滚之间等待的时间（默认为0s）
        failure_action: pause    #如果回滚失败，该怎么办。continue/pause(默认)
        order: start-first       #回滚期间的操作顺序。stop-first/start-first
      
      update_config:             #更新服务-配置
        parallelism: 1           #一次更新的容器数
        delay: 30s               #更新一组容器之间等待的时间
        failure_action: rollback #跟新失败操作，continue/rollback/pause(默认)
        order: start-first       #更新期间的操作顺序,stop-first/start-first

      placement:                 #约束和首选项
        constraints:             #可以用==或者!=,多个条件全都满足的条件下的节点去部署
          - "node.role==worker"
          - "node.hostname!=123"
        max_replicas_per_node: 1 #每个节点上运行的最大副本任务数   
    



networks:
  some-network: 
    
volumes: 
  some-volumes: 

configs:
  my_config:
    file: ./my_config.txt        #当前路径下的my_config.txt文件
  my_other_config:
    external: true               #外部创建好的config










~~~


