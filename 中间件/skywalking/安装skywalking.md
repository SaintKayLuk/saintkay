# 安装 skywalking



## 通过 helm 在 kubernetes 中安装
```
helm install skywalking  oci://registry-1.docker.io/apache/skywalking-helm -n base --version 4.7.0 \
	--set oap.storageType=elasticsearch  \
	--set elasticsearch.enabled=true \
	--set ui.enabled=true \
	--set telemetry.enabled=false \
	--set alarm.enabled=false \
	--set ui.image.tag=9.7.0 \
	--set oap.image.tag=9.7.0
```