开发者可以与 AI 助手进行对话，并且咨询和编程技术相关的问题。通过多轮对话生成代码，或者由 AI 帮助解答编码过程中遇到的问题。

## VS Code

开发者可以在对话输入框中通过 **@** 和 **/** 发起对话场景的指令。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/4da4197b57fb11f0ba94525400454e06.png)

### Ask 和 Craft 模式切换

代码助手在对话输入框中支持 Ask 和 Craft 两种模式的切换，满足不同开发场景的需求。Ask 模式主要用于对话式技术问答，解决编码过程中的具体问题或快速生成片段代码；而 Craft 模式用于实现从自然语言需求到生成完整应用的复杂需求，实现“需求到交付”的自动化，属于项目级的软件开发智能体。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/9711afb6580911f0857a525400e889b2.png)

### 对话快捷指令

- 在对话输入框中，可输入`/`调用预置的快捷指令，以及自定义指令。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/e13fcc0257fd11f09c7652540044a08e.png)

	- **/doc**：为所选的代码添加文档注释。
	- **/explain**：解释所选代码的工作原理。
	- **/fix**：针对所选代码中的问题提出修复方案。
	- **/tests**：为所选代码生成单元测试。
	- **/cr**：可针对所选代码、文件或文件夹、文件变更，甚至是整个工程代码提出评审方案。
- 在对话输入框中，可输入 **@** 选择添加文件、知识库等资料作为对话上下文。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/7348a7e7580211f0b3f05254001c06ec.png)

	- **File \& Folders**：选择文件或文件夹作为对话上下文信息。
	- **Diff**：添加文件变更作为对话上下文信息。
	- **Docs**：选择添加知识库作为对话上下文信息，包括官方知识库和自定义知识库。
	- **Terminal**：添加终端最后执行的命令作为对话上下文信息。
	- **Agent**：选择自定义智能体。

### @ Add

单击 **@ Add** 可以选择添加文件、知识库等资料作为上下文，除了支持搜索文件之外，其它的与在对话输入框中输入 **@** 添加上下文一致。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/ad014c2b580211f0922d5254007c27c5.png)

### 模型配置

内置多种大模型，详情请参考 [模型配置](./模型配置)。

![](/docs/static/%E6%A8%A1%E5%9E%8B%E5%88%97%E8%A1%A8.sUqIwgkb.png)

### 对话管理

对话管理包括创建新对话和历史对话记录管理。

- 创建新对话。 如果您想重新开启对话或者开启一个新的技术话题，您可以单击**创建新对话**。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/9ab20260580611f094cd52540099c741.png)
- 历史对话记录管理。 单击进入**历史对话记录**后，在这里，您可以查看历史对话记录，并支持对历史对话进行编辑、导出和删除对话的操作。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/4819798d580711f0b3f05254001c06ec.png)

## JetBrains IDE

JetBrains IDE 的技术对话使用方式，与 VS Code 基本一致。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/a12439bc587711f0b3f05254001c06ec.png)

### Ask 和 Craft 模式切换

与 VS Code 相同，在 JetBrains IDEs 中，代码助手在对话输入框中同样支持 Ask 和 Craft 两种模式的切换，满足不同开发场景的需求。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/b0951b83587a11f0b3f05254001c06ec.png)

### 对话快捷指令

- 在对话输入框中，可输入 `/`调用预置的快捷指令以及自定义指令。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/904b1d7c587811f09fd0525400bf7822.png)

	- **/doc**：为所选的代码添加文档注释。
	- **/explain**：解释所选代码的工作原理。
	- **/fix**：针对所选代码中的问题提出修复方案。
	- **/tests**：为所选代码生成单元测试。
	- **/cr**：可针对所选代码、文件或文件夹、文件变更，甚至是整个工程代码提出评审方案。
- 在对话输入框中，可输入 `@`选择添加文件、知识库等资料作为对话上下文。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/df7fa9e9587811f0b3f05254001c06ec.png)

	- **File \& Folders**：选择文件或文件夹作为对话上下文信息。
	- **Diff**：添加文件变更作为对话上下文信息。
	- **Docs**：选择添加知识库作为对话上下文信息，包括官方知识库和自定义知识库。
	- **Terminal**：添加终端最后执行的命令作为对话上下文信息。
	- **Agent**：选择自定义智能体。

### @ Add

单击 \*\*@ Add **可以选择添加文件、知识库等资料作为上下文，除了支持搜索文件之外，其它的与在对话输入框中输入** @ \*\*添加上下文一致。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/2169d83d587911f094cd52540099c741.png)

### 模型切换

内置多种大模型，详情请参考 [模型配置](./模型配置)。

![](/docs/static/%E6%A8%A1%E5%9E%8B%E5%88%97%E8%A1%A8.sUqIwgkb.png)

### 对话管理

对话管理包括创建新对话和历史对话记录管理。

- 创建新对话。 如果您想重新开启对话或者开启一个新的技术话题，您可以单击**创建新对话**。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/80dac85a587911f0b3f05254001c06ec.png)
- 历史对话记录管理。 单击进入**历史对话记录**后，在这里，您可以查看历史对话记录，并右键历史对话，支持对历史对话进行编辑、导出和删除对话的操作。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/18c3f88b587a11f0857a525400e889b2.png)

## 微信开发者工具 IDE

微信开发者工具 IDE 的技术对话使用方式，与 VS Code 对齐。您可以在对话输入框中通过 `@`和 `/`符号发起对话场景的指令。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/c52c2d89740511f0bcac525400e889b2.png)

### Ask 和 Craft 模式切换

代码助手在对话输入框中支持 Ask 和 Craft 两种模式的切换，满足不同开发场景的需求。如果您希望解决编码过程中的具体问题或快速生成片段代码，可以选择 Ask 模式；如果您希望实现从自然语言到生成完整应用的复杂需求，实现“需求到交付”的自动化，可以选择 Craft 模式。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/11bde048740711f09e39525400454e06.png)

### 对话快捷指令

- 在对话输入框中，可输入 `/`调用预置的快捷指令。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/b5a02c8c740711f0bcac525400e889b2.png)

	- **/cr**：可针对所选代码、文件或文件夹、文件变更，甚至是整个工程代码提出评审方案。
	- **/tests**：为所选代码生成单元测试。
	- **/explain**：解释所选代码的工作原理。
	- **/fix**：针对所选代码中的问题提出修复方案。
	- **/doc**：为所选的代码添加文档注释。
- 在对话输入框中，可输入 **@** 选择添加文件、知识库等内容作为对话上下文。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/23fd67c4740911f09f3d52540099c741.png)

	- **File \& Folders**：选择文件或文件夹作为对话上下文信息。
	- **Diff**：添加文件变更作为对话上下文信息。
	- **Docs**：选择添加官方知识库作为对话上下文信息。
	- **Terminal**：添加终端最后执行的命令作为对话上下文信息。

### @ Add

在对话框中，单击 \*\*@ Add \*\*可以选择添加文件、知识库等内容作为上下文，除了支持搜索之外，其它的与在对话输入框中输入 **@** 添加上下文一致。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/25087fc3740a11f0bcac525400e889b2.png)

### 模型配置

内置多种模型，您可以根据实际需要自由切换。关于如何切换模型请参考 [模型配置](./模型配置)。

![](/docs/static/%E6%A8%A1%E5%9E%8B%E5%88%97%E8%A1%A8.sUqIwgkb.png)

### 对话管理

对话管理包括创建新对话和历史对话记录管理。

- 创建新对话 如果您想重新开启对话或者开启一个新的技术话题，您可以单击 **Start new chat**。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/d9ef8bd9742111f09e39525400454e06.png)
- 历史对话记录管理 单击进入 **Show chats** 后，在这里，您可以查看历史对话记录，并支持对历史对话进行编辑、导出和删除的操作。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/28c0862c742311f087e15254005ef0f7.png)