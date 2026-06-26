## 代码补全

在 Visual Studio 代码编辑区内，可以通过正常编码停顿后自动触发补全场景，并会根据上下文智能生成准确的代码补全推荐。该场景具有如下特性：

- 支持多种编程语言的语法深度学习，提供全面的代码补全功能。
- 注释描述、变量、函数等补全一应俱全。
- 根据注释或函数声明智能生成代码块。
- 函数间补全，帮助您轻松实现新函数或完善现有函数。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/c9d8fc47cd6911efa2ff52540044a08e.gif)

## 技术对话

插件提供了多种语言和为各种框架提供了建议，在 Visual Studio 上全面支持 C\#、C\+\+、TypeScript、ASP.Net 等方面的回答。 登录后，可以通过**工具** \> \*\*CodeBuddy \*\* \> **打开对话**进行技术对话。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/974536db115011f0ae09525400bf7822.png)

在侧栏对话框，可以咨询技术问题，例如使用 C\# 写一段冒泡排序。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/88c50940147911f09fca52540099c741.gif)

## 对话模型切换

腾讯云代码助手除了内置腾讯自研的混元大模型之外，目前已经部署了官方 deepseek \-r1模型，默认是混元大模型。在左侧对话面板中，有一个模型选项可以支持您自由选择对话模型进行切换。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/e5139299115011f0ae09525400bf7822.png)

## 快捷指令问答

通过输入 / 或 @ 调用预置的快捷指令，或通过 \# 引用知识库，快速获取所需帮助：

- /clear：清空当前会话。
- /comments：为所选代码添加文档注释。
- /explain：解释所选代码的工作原理。
- /fix：提出针对所选代码问题的修复方案。
- /tests：为所选代码生成单元测试。
- /nameVariable：智能命名变量。
- @workspace：自动引用当前工作空间代码。
- 知识库：支持引用预置的知识库。

## 自动生成代码注释

通过指令 /comments，结合圈选的代码，可以快速生成代码注释。

- 根据代码功能快速生成清晰、易读的注释。
- 自动生成解释目录，降低理解成本。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/a61b54e5147a11f0aaa3525400e889b2.gif)

## 代码规范与错误修复

通过指令 /fix，可以快速提供对于圈选代码的修复方案。

- 选中代码即可进行规范检查和错误修复。
- 减少漏洞，提高代码质量。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/65f4a41e147b11f0ae09525400bf7822.gif)

## 总结与路线

腾讯云代码助手在 Visual Studio 的第一版中，支持了比较常用的场景，在接下来的版本中，我们会陆续支持企业版登录，加强对于代码生成的效果，支持查找历史对话和使用内联对话、评审等高级能力。