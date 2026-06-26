全新软件开发智能体 Craft，输入自然语言指令，支持文件多选，AI 深度理解，自主完成多文件代码生成和改写，即刻落地可执行应用。与 Ask 模式的对话智能体相比，跨文件上下文理解、批量代码生成与修改、智能代码优化与重构是 Craft 的核心功能，尤其是在生成代码工程中表现突出，能够显著提升开发者的效率。

> **说明：**
> 
> - Craft 支持的插件端：VS Code、JetBrains IDEs、微信开发者工具。
> - Craft 支持的语言：市面上主流的开发语言都支持，例如 C、C\+\+、C\#、CSS、Go、HTML、Java、JavaScript 等等。

## 使用方法

1. 打开 Craft 模式。在代码助手对话输入框下提供 Ask 和 Craft 两种模式切换的入口，您可以单击切换到 Craft 模式，或者使用快捷键（Windows 为 Alt \+ I ；macOS 为⌘ \+ I）快速切换。
- VS Code![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/3594cf7f588011f09c7652540044a08e.png)
- JetBrains IDEs![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/4e757fd2588011f09fd0525400bf7822.png)
- 微信开发者工具 IDE![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/1909f14e743911f084fc525400bf7822.png)
2. **模式设置**，包括生成计划（**Plan 模式**）、自动运行和自动修改文件，VS Code 和 JetBrains IDEs 、微信开发者工具 IDE 的模式设置入口一致，以 VS Code 为例，如下图。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/4be5939d588111f09fd0525400bf7822.png) 这三个设置默认为开启状态。
- **生成计划（Plan 模式）**：启用生成计划后，Craft 将根据需求进行拆解任务，制定计划并澄清需求。如果需求不明确 Craft 会进行询问，您只需回复直到需求清晰后，单击开始按钮或者回复请生成代码，即可开始执行计划。
- **自动运行**：启用自动运行后，Craft 会根据计划自动执行任务，减少人工操作。
- **自动修改文件**：启用自动修改文件后，Craft 能够对文件进行生成和改写。
3. **对话管理**。包括创建新对话和历史对话记录管理。

	- 创建新对话。您可以根据实际需求创建新对话。
	
	
		- VS Code![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/3b76c4e8588311f0b3f05254001c06ec.png)
		- JetBrains IDEs![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/560031d1588311f0922d5254007c27c5.png)
		- 微信开发者工具 IDE![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/8877e2ae743911f0bcac525400e889b2.png)
- 历史对话记录管理。在这里，您可以查看历史对话记录，并支持对历史对话记录进行导出、编辑和删除的操作 。

	- VS Code![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/9204304b588311f095485254005ef0f7.png)
	- JetBrains IDEs![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/a563429d588311f094cd52540099c741.png)
	- 微信开发者工具 IDE![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/cec66549743911f09e39525400454e06.png)
4. 在输入框中输入需求描述。
- VS Code![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/232cce3e588411f095485254005ef0f7.png)
- JetBrains IDEs![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/381539ff588411f0857a525400e889b2.png)
- 微信开发者工具 IDE![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/56a28222743a11f087e15254005ef0f7.png)
5. 可以选择**添加上下文**作为对话上下文。

	- 单击 **@ Add**，可以选择添加文件或文件夹、文件变更、知识库以及终端最后执行的命令作为对话上下文。
	
	
		- VS Code![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/6b418e5e588411f0857a525400e889b2.png)
		- JetBrains IDEs![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/85c918e3588411f0857a525400e889b2.png)
		- 微信开发者工具 IDE![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/8caddeeb743a11f084fc525400bf7822.png)**@File \& Folders**：选择文件或文件夹作为对话上下文信息。 **@Diff**：添加文件变更作为对话上下文信息。 **@Docs**：选择添加知识库作为对话上下文信息，包括官方知识库和自定义知识库。 **@Terminal**：添加终端最后执行的命令作为对话上下文信息。
- 或者在**资源管理器**的文件树中，右键单击文件或文件夹选择**腾讯云代码助手 CodeBuddy** \> **添加到对话。**

	- VS Code![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/17c21cd1588611f0ba94525400454e06.png)
	- JetBrains IDEs![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/4633156e588611f095485254005ef0f7.png)
	- 微信开发者工具 IDE![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/0bbefdef743b11f0b9a25254007c27c5.png)
- 或者在编辑区中，圈选代码后右键选择**腾讯云代码助手 CodeBuddy** \> **添加到对话**，或 **CodeBuddy** \> **添加到对话**。

	- VS Code![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/b1dcdd56588611f0ba94525400454e06.png)
	- JetBrains IDEs![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/fc977edc588611f0b3f05254001c06ec.png)
	- 微信开发者工具 IDE![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/5e87c1ad743b11f084fc525400bf7822.png)
6. 输入需求描述后，Craft 将自主完成多文件代码生成和改写，并以 diff 视图的形式进行分栏展示。此外，JetBrains IDEs 还支持在新窗口以 diff 的形式展示改写文件。
- VS Code![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/a6a5d8e7588811f0922d5254007c27c5.png)
- JetBrains IDEs![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/33b905f0476c11f0afa1525400bf7822.png)
- 微信开发者工具 IDE![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/e127ccde743b11f0bcac525400e889b2.png)
7. 对生成的代码可以进行**接受**/**拒绝**处理。

	- 可以对所有编辑文件进行**全部接受**或**全部拒绝**处理。
	
	
		- VS Code![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/04802833588a11f0b3f05254001c06ec.png)
		- JetBrains IDEs![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/84ef3df6476d11f0aeeb5254001c06ec.png)
		- 微信开发者工具 IDE![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/533bfe97743c11f09f3d52540099c741.png)
- 鼠标悬浮单个编辑文件可以对单个编辑进行接受或拒绝的处理。

	- VS Code![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/d5d83e32588911f095485254005ef0f7.png)
	- JetBrains IDEs![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/d7d917ad476d11f0a5a752540044a08e.png)
	- 微信开发者工具 IDE![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/7b38e475743c11f0bcac525400e889b2.png)
8. 在修改文件的操作条中，可以对修改文件进行操作，包括查看变更，以及接受或拒绝。
- VS Code![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/cbbf5c7c743c11f087e15254005ef0f7.png)
- 微信开发者工具 IDE![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/079b8057743d11f087e15254005ef0f7.png)
9. 对于对话生成的代码文件内容，单击蓝色显示的代码文件或方法或类或路径等，可直接跳转到对应内容进行查看。
- VS Code![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/2ae034c0743d11f09f3d52540099c741.png)
- 微信开发者工具 IDE![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/005f82d8743e11f081ce52540044a08e.png)
10. 版本化管理。Craft 支持版本管理能力，将鼠标悬浮在之前对话版本，您可以选择回退版本、重新编辑。如果想要回退版本，详情请参考 [Craft 撤回检查点](https://write.woa.com/document/177446544772448256)。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/b33bb5a7589f11f0857a525400e889b2.png)
11. 模型切换。Craft 预置了 **hunyuan** 和 **deepseek\-v3** 最新模型，默认（default）为 **hunyuan** 模型，支持您对模型进行切换，满足不同场景需求。
- VS Code![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/dac04caa588b11f094cd52540099c741.png)
- JetBrains IDEs![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/0d11ae72588c11f0922d5254007c27c5.png)
- 微信开发者工具 IDE![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/3b52f353743e11f09e39525400454e06.png)

## 实战场景示例

下面为您演示一个《打地鼠》游戏的开发，来体验一下 Craft 通过自然语言来生成代码工程的能力。

1. 在 Craft 对话框中输入提示词需求。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/a9138f111f2711f0aec7525400454e06.png)
2. Craft 的执行过程。 2\.1 在开始执行游戏开发任务前，Craft 会向您询问具体要求信息，以此来制定详细的开发执行计划。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/7bbbe2521f2911f0aec7525400454e06.png) 2\.2 开发计划制定完成后，请求您进行确认。如果不满意可以选择继续输入需求；如果满意，单击**开始**即可开始自动执行开发计划。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/7dc88bc41f2a11f081f552540099c741.png) 2\.3 先对需求进行分析，并创建了基本目录结构。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/58044d5e1f4511f0ac5352540044a08e.png) 2\.4 基于任务依次创建实现逻辑。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/7dac96b61f4511f08c8d525400bf7822.png) 2\.5 所有逻辑代码全部实现后，会对当前游戏运行环境进行检测。如果检测到 Python 或第三方库未安装时，会自动进行安装。环境安装完成后，会自动运行程序。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/9946aabe1f4911f0ac5352540044a08e.png) 2\.6 程序测试完成能够正常运行后，可以选择对程序进行优化。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/14b977e41f4b11f099e05254005ef0f7.png) 2\.7 游戏优化后，自动对所优化的需求进行游戏测试。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/0150491a1f4f11f08c8d525400bf7822.png)
3. 效果演示。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/14a7ab2b1f5111f099e05254005ef0f7.gif)