# minikube




--driver=none时报错，
~~~
minikube start --driver=none
* Centos 7.7.1908 上的 minikube v1.9.2
* 根据用户配置使用 none 驱动程序
X Sorry, Kubernetes v1.18.0 requires conntrack to be installed in root's path
~~~
需要安装conntrack
~~~
yum install -y conntrack
~~~

--driver=virtualbox需要安装VirtualBox



minikube start --image-repository='registry.cn-hangzhou.aliyuncs.com/google_containers'
~~~
minikube start
minikube status
minikube stop
minikube delete
~~~