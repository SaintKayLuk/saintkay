# skill规范


## skill目录结构


```
my-skill/
├── SKILL.md            # 核心文件
│   ├── name            # (必须)，skill的名字，和文件夹名一致，建议使用 kebab-case 格式，例如 server-ops
│   └── description     # (必须)，描述，不只是介绍 Skill 干什么，还应该说明什么时候应该触发这个 Skill
│
├── references/         # (可选)，存放按需加载的参考文档
├── scripts/            # (可选)，存放可执行脚本
└── assets/             # (可选)，存放模板、静态资源
```

示例：一个 server-info 的skill目录结构示例
```
server-info/
│
├── SKILL.md
│
├── references/
│   ├── linux.md
│   └── windows.md
│
├── scripts/
│   ├── linux_info.sh
│   └── windows_info.ps1
│
└── assets/
    └── server-report-template.xlsx
```





## description 怎么写

```
description: [能力] + [适用对象/任务] + [触发场景] + [典型关键词]
```
例：做一个 Linux 运维 Skill
```
description: 检查和排查 Linux 服务器的 CPU、内存、磁盘、网络、端口和系统服务问题。当用户需要进行 Linux 服务器状态检查、资源异常分析、端口检查、服务故障排查或性能问题定位时使用。
```
