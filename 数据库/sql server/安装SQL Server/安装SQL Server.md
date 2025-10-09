## 版本


* Developer
  * 开发版
  * 功能和企业版一样
  * 不可用于企业
* Standard
  * 标准版
  * 提供核心功能，但有限制（比如 CPU 核心数、内存使用上限）
* Enterprise
  * 企业版
  * 支持完整 AlwaysOn




## windows 中安装


1. 右键装载安装包(.iso文件)
2. 输入序列号（或默认“评估版”）
3. 功能选择（Feature Selection）
   * Database Engine Services(数据库引擎服务) **必选**
   * SQL Server Replication(复制) **可选，用于数据同步或分发**
   * Full-Text and Semantic Extractions for Search(全文搜索和语义提取) **可选（如你用全文检索）**
   * Analysis Services	(分析服务) **不选（除非你部署 BI）**
4. 实例配置
5. 服务配置（Server Configuration）
   * 服务账户：类似与linux中服务由哪个用户来启动，可以选择默认用户，也可以设置为 本机的 administrator 用户
6. 数据库引擎配置
   * Windows 身份验证（默认）：只能用windows的用户登录
   * 混合模式（推荐）：设置 sa 用户的密码
   * 还需要把当前用户(administrator)添加到sql server的管理员





