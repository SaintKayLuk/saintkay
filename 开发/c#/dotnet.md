# dotnet


dotnet是平台
C#是语言，在dotnet上运行的语言，

一个sln文件是一个解决方案，包含多个项目(csproj)


- 解决方案项目结构(sln)
  - MySolution.sln
  - ProjectA\ProjectA.csproj
  - ProjectB\ProjectB.csproj


项目结构
```
MyDotNetApp/
│
├── Controllers/            # 控制器文件夹，处理 HTTP 请求。
│   └── WeatherForecastController.cs
│
├── Models/                 # 数据模型文件夹，包含数据结构和 DTOs。
│   └── WeatherForecast.cs
│
├── Services/               # 服务层文件夹，包含业务逻辑代码。
│   └── WeatherService.cs
│
├── Program.cs              # 应用入口，.NET 6 使用简化的启动方式。
│
├── appsettings.json        # 应用配置文件（非环境相关）。
├── appsettings.Development.json  # 环境相关的配置文件（开发环境）。
│
├── MyDotNetApp.csproj      # 项目文件，定义项目依赖和构建设置。
│
├── Properties/             # 包含程序集信息的文件夹。
│   └── launchSettings.json # 本地开发和调试设置。
│
└── bin/ & obj/             # 编译输出和中间文件，通常被忽略（添加到 `.gitignore`）。

```




