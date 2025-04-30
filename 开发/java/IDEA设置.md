### 显示形参名提示

```
File → Setting → Editor → Inlay Hints
```
根据文件类型，需要显示则打勾


### 编码设置

```
File → Setting → Editor → File Encodings
```

Global Encoding 设置为 UTF-8
Project Encoding 设置为 UTF-8

Default encoding for properties files 设置为 UTF-8 , 并且勾选 **Transparent native-to-ascii conversion**


### 提示区分大小写

```
File → Setting → Editor → General → Code Completion
```
取消勾选 **Match case** 则提示不区分大小写


### 优化 import

```
File → Setting → Editor → General → Auto Import
```
1. 自动导入明确的包: 勾选 **Add unambiguous imports on the fly** 
2. 自动去除没有引用的包: 勾选 **Optimize imports on the fly**    

### 代码默认折叠

```
File → Setting → Editor → General → Code Folding
```
自动折叠

取消勾选 **One-line methods** 



### 文档注释中使用渲染线（竖线样式）

```
File -> Settings -> Editor -> General -> Appearance
```

勾选 **Render documentation comments**


### 注解实现

例如lombok，mapstruct等

```
Settings -> Build, Execution, Deployment -> Compiler -> Annotation Processors -> 选中 Enable annotation processing 复选框 
左侧选择项目在 Maven default annotation processors profile 下 -> Store generated sources relative to:  -> 选择Module output directory
```