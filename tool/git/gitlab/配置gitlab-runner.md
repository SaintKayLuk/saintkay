# 配置 gitlab-runner


```sh
kubectl create secret generic s3access --from-literal=accesskey="YourAccessKey" --from-literal=secretkey="YourSecretKey"
```

```yaml
runners:
  config: |
    [[runners]]
      [runners.kubernetes]
        image = "ubuntu:22.04"
        allowed_pull_policies = ["always", "if-not-present", "never"]  # 允许的策略
      [runners.cache]
        Type = "s3"
        Path = "runner"
        Shared = true
        [runners.cache.s3]
          ServerAddress = "s3.amazonaws.com"
          BucketName = "my_bucket_name"
          BucketLocation = "eu-west-1"
          Insecure = false
          AuthenticationType = "access-key"

  cache:
      secretName: s3access

extraEnvFrom: {}
  CACHE_S3_ACCESS_KEY:
    secretKeyRef:
      name: s3access
      key: accesskey
  CACHE_S3_SECRET_KEY:
    secretKeyRef:
      name: s3access
      key: secretkey

resources: 
  limits:
    cpu: "1"
    memory: "2Gi"
  requests:
    cpu: "500m"
    memory: "1Gi"
```

