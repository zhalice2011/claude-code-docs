AI 辅助开发的大背景下，除了代码生成，在编辑器自带的终端模式下，同样需要 AI 相关的能力，从而可以帮助程序员在终端运行出现报错的场景下，可以快速查找到问题解决方案；也可以帮助程序员不需要记住太多的终端命令。本文旨在介绍腾讯云代码助手，如何与终端结合应用，为代码开发提供便利。

## 在对话中，面向终端 @terminal 提问

代码助手支持四种 agent 模式：

- @workspace：面向项目工程下的提问解答
- @vscode：面向 vscode 帮助文档的提问解答。
- @terminal：面向终端的提问解答。
- 拓展 agent，支持用户自行定义 agent，这里不做过多展开。

本部分将对 @terminal 面向终端的提问解答，进行实践演示。

### 获取终端中错误信息的相关帮助

当终端运行产生错误信息时，只需选中错误消息，右键单击，然后选择**腾讯云代码助手：解释代码**。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/55990bf2135911f09b3252540044a08e.png)

代码助手将为您提供错误描述和建议的修复方案。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/0d23d4c3148411f0aaa3525400e889b2.png)

当然您也可以直接在对话框中输入 @terminal，譬如，@terminal 安装 maven，如下图，他会找到和终端相关的答案。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/0ecbe1a2135b11f0854e525400454e06.png)