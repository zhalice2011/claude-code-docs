腾讯云代码助手推出**智能评审辅助**的新功能。这项功能旨在为 VS Code 和 JetBrains IDEs 上的开发者们提供全面支持，包括 **AI 辅助自评审**和 **AI 提交信息生成**两大核心功能。通过这些功能，开发者能够在项目开发过程中及时发现并解决本地代码变更可能引入的问题，从而提高代码质量，加速开发流程。

## AI 辅助自评审

AI 辅助自评审功能，旨在提高 IDE 下的代码自我审查的效率和质量。在 Chat 模式中使用，可以通过`/cr`指令直接触发本地自动化代码审查（AICR）。

### 触发评审

腾讯云代码助手支持三种评审范围：**评审文件或文件夹 （指定单个或多个文件或文件夹）**、**评审变更（当前暂存区代码变更）**、**评审编辑区（指定编辑区内容）**。

#### 评审编辑区

在打开的代码文件编辑区中，可以通过圈选代码区域触发 **IDE 编辑区范围内**的代码作为评审内容。

> **说明：**

> 如果在编辑区进行了划词圈选操作，触发评审功能后会将划词圈选部分的代码作为评审范围。如果未进行划词圈选，触发评审功能后会将整个工程文件的代码作为评审范围。

- 圈选代码区域后，将鼠标悬浮在所选代码区域上会出现功能面板，可以选择**代码评审**触发CR 自动评审功能。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/5be93c6657b911f09c7652540044a08e.png)
- 圈选代码区域后，也可以右键选择 **腾讯云代码助手 CodeBuddy** \> **代码评审**来触发评审功能。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/d1d2930657bb11f0b3f05254001c06ec.png)
- 圈选代码区域后，也可以单击代码操作的**小灯泡**来触发评审功能\*\*。\*\* ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/b50a090410fb11f0a9cd5254007c27c5.png)
- 对于方法级评审，可以直接单击方法上方的**代码评审**来触发评审功能。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/596f1b6d57bc11f0ba94525400454e06.png)

#### 评审文件或文件夹

代码助手支持将文件或文件夹作为评审范围，支持在功能面板的对话输入框或文件树中进行评审触发。

- 在对话输入框中，直接输入 `/cr`，然后单击 `@ Add` 按钮，选择 `File & Folders`；或者输入 `/`，选择 `cr`，接着选择文件或文件夹即可。选择时支持输入搜索。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/f9318f1e57be11f0ba94525400454e06.png)
- 在文件树中，鼠标单击文件或文件夹右键选择**腾讯云代码助手 CodeBuddy** \> **代码评审**。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/5329bc4457bf11f095485254005ef0f7.png)

#### 评审变更

在对话输入框中输入 `/cr`，然后选择 **Diff**，将评审 IDE 内暂存区的所有文件。**本指令将评审暂存区文件的变更部分，非变更部分将不评审。**

目前将**最多评审暂存区的三十个文件**。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/9327e1ee57c011f094cd52540099c741.png)

### 评审执行

您可以根据自己的需求，选择评审范围。例如：选择评审文件或文件夹进行评审时，通过 `/cr` 指令选择评审文件或文件夹后回车，将直接触发对所选文件或文件夹的评审。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/912e4a9957c111f09fd0525400bf7822.png)

### 查看评审结果

代码评审结束后，在对话面板内将直接返回评审结果，评审结果中将包含总体评价和问题列表，在问题列表中支持显示并单击蓝色位置区域跳转至问题所在文件代码片段进行查看。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/f7b636bf57d611f0922d5254007c27c5.png)

### 代码修复

评审返回评审结果后，您可以针对代码助手给出的评审意见进行修复。

- 单个问题修复 。您可以在问题列表中针对单个问题进行修复，例如选择**应用代码**时，将自动切换至 Craft 模式自动修复问题。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/a339c05457d711f094cd52540099c741.png)
- 多个问题修复。您可以基于问题列表中的所有问题一次性进行修复。手动切换至 Craft 模式（可以单击对话输入框左下方模式切换按钮进行切换，也可以通过快捷键 **Alt \+ I** 进行切换），然后输入**开始修复问题**即可，Craft将自动帮您将问题列表中的问题进行修复。在修复的过程中，将以 Diff 的形式进行展示，最后修复完成后 ，检查如果没问题选择**接受**即可。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/7a650de057d911f09fd0525400bf7822.png)

### AI 评审限制

为保证响应，目前对于评审大小有一定的限制，限制条件如下：

- 变更文件应包含新增行（\+），所在完整函数不应超过100行。
- 单个文件大小应小于**1M。**
- 符合前2个条件的有效变更文件，文件数最大应不超过1000个，变更行数不超过10000行。
- 文件黑名单检查（常见的配置文件、二进制文件、无后缀文件等），以及当前黑名单列表（可能有动态调整，目前更新到2024\.10月）如下：

> **注意：**

> **不支持评审的文件类型**：

> "go.mod", "go.sum", "\_test.go", "Test.java", "test.cpp", ".test", ".yaml", ".yml", ".ini", ".json", ".proto", ".md", ".txt", "mock", "\_mock", ".md", ".gradle", "pom.xml", "package.json", ".gitignore", ".gitmodules", ".npmignore", ".yarnignore", ".babelrc", ".eslintrc", ".stylelintrc", ".jshintrc", ".editorconfig", ".env", ".swp", ".cache", ".log", ".gem", ".lock", ".min.js", ".min.css", ".map", ".bundle.js", "bundle.css", ".d.ts", ".service\-worker.js", ".pb.go", ".pb.cc", ".pb", ".designer.cs", ".pyc", ".pyd", ".pyo", ".whl", ".luac", ".toc", "wire\_gen.go", ".svg", ".cmake"

## AI 提交信息生成

在本地 IDE 中提交代码变更时，支持一键唤起 AI，自动基于提交变更生成代码提交信息。该信息默认遵守 Conventional 提交信息规范，支持设置生成的语言、风格。借助 AI 快速生成规范化的提交信息，帮助开发者提升效率。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100027869939/a0b6785c87e711ef8631525400a9236a.png)

### 设置风格、语言

#### 设置 AI 提交信息语言

进入到插件设置里，在 **Commit Message Language** 中，配置 AI 提交信息语言，目前支持中文（默认）、英文。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100027869939/e824b90787e711ef8631525400a9236a.png)

#### 设置 AI 提交信息风格

进入到插件设置里，在 **Commit Message Style** 中，选择配置 AI 提交信息生成的风格，如下图。

- 风格1：生成变更摘要。
- 风格2：根据 Conventional 社区规范。
- 风格3：参考仓库历史提交。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100027869939/44c823e987e811ef82535254002693fd.png)