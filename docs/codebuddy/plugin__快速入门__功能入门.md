# Codebuddy 插件

## VS Code

腾讯云代码助手主要提供两类功能：技术对话功能和代码补全功能。

### 技术对话功能

代码助手对话面板包括：左侧对话面板和编辑器内功能对话面板。

- 左侧对话面板。 和传统的聊天软件类似，但是开发者只能与代码助手进行对话，并且只能咨询有关编程技术的问题。左侧对话面板更适合咨询一些宽泛的问题，问题答案具有不确定性，不能保证百分之百回答正确，需要开发者多回合沟通才能得到最终答案，并且答案不一定有代码，可能是代码 \+ 文字说明等各种各样的形式。至于答案里面的代码部分是否需要复制或者插入到代码文件中，操作相对灵活自由，开发者自由选择。
- 编辑器内功能对话面板。 编辑器内功能对话面板是选中代码后进行交互，要求代码助手对选中的代码做处理，处理的方式可以通过自然语言交互。对选中的代码处理后的结果，是明确要求开发者选择是接受，还是取消。

面板的概览图如下所示：

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/cd3574e613b611f09fca52540099c741.png)

### 代码补全功能

目前支持的主流开发语言的补全，例如：C、C\+\+、C\#、CSS、Go、HTML、Java、JavaScript、Kotlin、TypeScript、React、Python、SQL、PHP、Objective\-C、Shell，System\-C、Verilog、MATLAB、Markdown 等。

只需要使用编辑器打开代码文件，编辑代码文件时候，代码助手会在合适时机和位置自动触发智能代码补全提示，如下图所示：

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/3abf7958ce3311efb1a552540099c741.png)

### 快捷键

默认快捷键如下：

| 操作 | macOS | Windows |
| --- | --- | --- |
| 进行代码解释 | ⌥ \+ ⇧ \+ X | Shift \+ Alt \+ X |
| 进行代码修复 | ⌥ \+ ⇧ \+ Y | Shift \+ Alt \+ Y |
| 进行代码注释 | ⌥ \+ ⇧ \+ M | Shift \+ Alt \+ M |
| 生成测试单元 | ⌥ \+ ⇧ \+ T | Shift \+ Alt \+ T |
| 询问 AI 问题 | ⌘ \+ ⌃ \+ I | Ctrl \+ Windows \+ I |
| 在代码区域打开技术对话 | ⌘ \+ ⌃ \+ N | Ctrl \+ Windows \+ N |

支持按下图操作，进行快捷键配置：单击插件菜单，选择**键盘快捷方式**，即可对快捷键进行自定义。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/64ca8284106011f0a9cd5254007c27c5.png)

### 对话快捷指令

在对话输入框中，输入 / 或 @ 调用预置的快捷指令：

- /clear：清空当前会话。
- /comments：为所选的代码添加文档注释。
- /new\-notebook：创建一个新的 Jupyter 笔记本。
- /explain：解释所选代码的工作原理。
- /fix：针对所选代码中的问题提出修复方案。
- /tests：为所选代码生成单元测试。
- /name\-var：变量命名。
- /cr：为所选代码和本地提交的 Diff 提出评审方案。
- /help：查看使用指南。
- @vscode：询问 VS Code。
- @terminal：询问如何在终端中执行某些操作。
- @workspace：询问您的工作空间，将自动引用当前代码。

## Visual Studio

具体详情请参见[Visual Studio 使用指引](https://cloud.tencent.com/document/product/1749/115713)。

## IDEA

### 技术对话功能

代码助手对话面板与传统的聊天软件类似，只是开发者只能与代码助手进行对话，并且只能咨询一些有关编程技术的问题。对话面板适合咨询一些比较宽泛的问题，一些复杂的问题，需要开发者多回合沟通才能得到最终答案，并且答案的形式是纯文字或者是代码 \+ 文字说明等形式。如下所示：

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/d08d4aa016aa11f09240525400bf7822.png)

### 代码补全功能

目前支持的主流开发语言的补全，例如：C、C\+\+、CSS、Go、HTML、Java、JavaScript、Kotlin、TypeScript、React、Python、SQL、Markdown 等。只需要使用编辑器打开代码文件，编辑代码文件时候，代码助手会在合适时机和位置自动触发智能代码补全提示，如下图所示：

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/7cfdf60bce3611ef97675254007c27c5.png)

### 快捷键

默认快捷键如下：

| 操作 | macOS | Windows |
| --- | --- | --- |
| 触发代码补全 | Enter | Enter |
| 采纳所有推荐代码 | Tab | Tab |
| 按行采纳推荐代码 | Ctrl \+ ⌘ \+ → | Ctrl \+ Alt \+ → |
| 按词采纳推荐代码 | ⌘ \+ → | Ctrl \+ → |
| 切换至下一个推荐结果 | ⌥ \+ ] | Alt \+ ] |
| 切换至上一个推荐结果 | ⌥ \+ \[ | Alt \+ \[ |
| 手动触发推荐 | ⌥ \+ \\ | Alt \+ \\ |
| 撤销当前推荐状态 | Esc | Esc |

1. 支持按下图操作，进行快捷键配置：单击插件菜单，选择**快捷键编辑。**![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/90362da713b711f0a63e5254005ef0f7.png)
2. 在弹出的设置弹窗中，选择**按键映射**，并在右侧找到“插件”文件夹。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/b872f14f106111f0a9cd5254007c27c5.png)
3. 在“插件”文件夹中，找到“Tencent Cloud CodeBuddy”，即可对快捷键进行自定义。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/d92a8eff106111f0aaa3525400e889b2.png)

### 对话快捷指令

在对话输入框中，输入 / 或 @ 调用预置的快捷指令：

- /comments：为所选的代码添加文档注释。
- /explain：解释所选代码的工作原理。
- /fix：针对所选代码中的问题提出修复方案。
- /tests：为所选代码生成单元测试。
- /clear：清空当前会话。
- /cr：AI 代码评审。
- /help：使用指南。
- @workspace：询问您的工作空间，将自动引用当前代码。
- @terminal：询问如何在终端中执行某些操作。

## Visual Studio 2022

在 Visual Studio 2022 中，目前腾讯云代码助手同样主要提供两类功能：技术对话和代码补全。

### 代码补全功能

在 Visual Studio 2022 代码编辑区内，可以通过正常编码停顿后自动触发腾讯云代码助手的代码补全功能，并会根据上下文智能生成准确的代码补全推荐。代码补全推荐可以包含注释、变量、函数等一应俱全的补全推荐内容。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/26049a1ae45d11efb98e525400e889b2.png)

### 技术对话功能

插件提供了多种语言和为各种框架提供了建议，在 Visual Studio 2022 上全面支持 C\#、C\+\+、TypeScript、ASP.NET 等方面的回答。当咨询复杂问题时，可以尝试与代码助手进行多轮对话，一步步接近想要的结果。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/155aab31106411f08c275254001c06ec.png)

### 对话快捷指令

在对话时也可以在对话框中调用 / 或 @ 指令，来进行对话，目前 Visual Studio 2022 支持的指令如下：

- /clear：清空当前会话。
- /comments：为所选代码添加文档注释。
- /explain：解释所选代码的工作原理。
- /fix：提出针对所选代码问题的修复方案。
- /tests：为所选代码生成单元测试。
- /nameVariable：智能命名变量。
- @workspace：自动引用当前工作空间代码。

## 微信开发者平台 IDE

目前，腾讯云代码助手在微信开发者平台中主要提供技术对话功能，包括左侧对话面板和编辑器内功能对话面板。

### 左侧对话面板

在左侧对话面板中，您可以在对话框中输入编程技术相关的问题，进行技术对话，当生成的结果不满意时，可以进行多轮对话，一步步生成您想要的结果。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/d783ea86106711f0a9cd5254007c27c5.png)

同时，目前代码助手也提供了如下指令，帮助您进行快捷对话：

- /clear：清空当前会话。
- /comments：为所选代码添加文档注释。
- /explain：解释所选代码的工作原理。
- /fix：提出针对所选代码问题的修复方案。
- /tests：为所选代码生成单元测试。
- /help：查看使用指南。
- @workspace：自动引用当前工作空间代码。
- @vscode：询问 VS Code。
- @terminal：询问如何在终端中执行某些操作。

### 编辑器内功能对话面板

编辑器内功能对话面板是选中代码后进行对话，目前暂时提供生成注释文档、解释代码、生成测试、修复代码功能。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/164d88e8106811f0a9cd5254007c27c5.png)