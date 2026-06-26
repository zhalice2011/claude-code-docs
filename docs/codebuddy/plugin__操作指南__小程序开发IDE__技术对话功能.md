腾讯云代码助手的技术对话功能，与微信开发者 IDE 做了深度的融合，并享用和 VSCode 一致的交互操作。 我们在微信开发者平台 IDE 中，支持主流前端语言，小程序语言 Markdown、Json 等。 当成功登录后，您只需要单击右下角开启 AI 对话或切换到代码助手对话面板即可。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/15b7bdfc114811f0ae09525400bf7822.png)

## 输入框

您可以直接在输入框中输入需求，然后回车，我们会根据当前项目和代码的上下文，生成更接近您要的答案。这里可以是技术回答，也可以是代码生成。 我们提供了指令、@、和 \# 知识库能力。接下来详细介绍下各个模块的作用和使用方法。

### 指令

如上图所示，指令是帮助开发者给予一个提问前的**动作申明**，我们称之为指令，也是开发过程中最常用的场景。目前我们提供如下指令：

- /clear 清除当前会话内容。
- /comments 为圈选代码生成注释，如下图所示。 圈选代码后，在对话框中输入 `/comments` 回车，代码助手会为您快速生成代码注释。单击顶部菜单，可以一键插入。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/305f92ad114a11f0854e525400454e06.png)
- /explain 为圈选代码生成解释。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/79ff8c4a114a11f0ae09525400bf7822.png)
- /fix 修复圈选代码。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/b3be5096114a11f0ae09525400bf7822.png)
- /nameVariables AI 生成变量名。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/2992594d114d11f0ae09525400bf7822.png)
- /tests 为圈选代码生成对应的测试。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/6e9eea1a114d11f0854e525400454e06.png)

### @ Agent 能力

您可以在对话中 @ 不同需求的 AI 智能体。我们目前支持：

- @workspace ： 对当前工程询问的智能体。
- @terminal：对终端问题询问解答的智能体，如下图： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/cbd36ded114d11f0a63e5254005ef0f7.png)

命令展示：

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/ea55b1f5114d11f0aaa3525400e889b2.png)

### \# 上下文

您可以选择知识库，引入更多上下文可以加强对话生成内容。如下图所示，在输入框输入 \#TDesign 您的需求后，知识库会先找到 TDesign 小程序相关的上下文代码，并作为额外上下文，结合您的提问，生成对话结果。同时在对话中会列举几个最相关的召回的文档地址供用户查阅。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/54a5ffde114e11f09fca52540099c741.png)