腾讯云代码助手提供了**自定义知识库**的功能。知识库作为 RAG 技术的数据源，能够为 RAG 提供额外的信息输入，加上 RAG 技术先进的信息检索和自然语言处理能力，能够让生成的内容具备高度的准确性和相关性，显著提高回答的质量，增强大模型生成的能力。接下来，让我们借助腾讯云代码助手的**自定义知识库**的功能，为您详细解析 Swarm 的源代码，以便您迅速掌握其设计理念和实现细节，并可以快速基于此能力进行企业内的实战开发。

## 对 Swarm 的介绍

Swarm 是 OpenAI 发布的一个实验性的智能体开发框架，被设计为一个轻量级的多智能体开发框架，主要针对需要多个智能体协同工作的场景，例如复杂任务的分配和多智能体间的合作等。它具有轻量级、无状态运行、高度可控、易于测试和迭代等特点。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/71691acebdb511efa6b052540055f650.png)

## 对 Swarm 的应用

### 准备自定义知识库

对于首次使用的新用户，需要如下3步创建企业（对于已经创建了企业的用户，直接登录 [企业后台管理](https://copilot.tencent.com/admin/overview) 并跳到第3步即可）。

1. 按向导 [创建企业](https://copilot.tencent.com/admin/team/version)，此处以创建旗舰版为例，如需了解其他版本请参见 [版本说明](./../../产品简介/版本说明)。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100025099277/df6f8cc9cbff11ef97675254007c27c5.png)
2. 创建成功后，您就是企业管理员。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/9e6076d5120111f09fca52540099c741.png)
3. 接下来创建知识库：在左侧导航栏选择**知识库**，单击**新建知识库**，配置知识库的基本信息后，单击**确定**。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/d0b2afa3120111f08c275254001c06ec.png)
4. 腾讯云代码助手支持离线代码库，您可以在 Github 克隆并应用最新的 [Swarm 代码库](https://github.com/openai/swarm)，单击 **Code** ，在下列列表中选择 **Download ZIP** 进行克隆。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/fc583d50bdb911efa6b052540055f650.png)
5. 下载到本地后上传即可。  ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/4b3a27ec120211f0ae09525400bf7822.png) 最新版本提供了知识库设置功能，可以根据高级用法调整召回参数等。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/682fc4ba120211f0854e525400454e06.png)
6. 上传完成后稍等查看数据处理状态，检查是否索引完成。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/8df1b520120211f0aaa3525400e889b2.png)
7. 最后返回首页列表，并开启**应用**即可。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/a4efdf37120211f08c275254001c06ec.png)

### 应用 Swarm

1. 确保登录账号属于所创建知识库的企业账号下，如果不是，则按下面的步骤进行账号切换。

	1. 单击插件小图标，然后单击**切换账号**。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/998c33a4148011f09b3252540044a08e.png)
	2. 选择所创建知识库的企业账号。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/ceefb412148011f0854e525400454e06.png)
2. 输入 **\#Swarm** 选择对应的知识库后，即可进行提问。例如我们先问一下 Swarm 的项目整体情况，如下图： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/8d300dc6120311f09b3252540044a08e.png)
3. 让代码助手完成简单的代码工作。 在对话输入框中输入提示词：“在 Swarm 中，如何实现一个 Agent 将对话转交给另一个 Agent，并且同时更新上下文变量？”。输出如下图所示： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/efe2cb7f120311f0ae09525400bf7822.png)
4. 运行程序，结果如下： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/4858b931bdd411ef8a945254002693fd.png)
5. 让代码助手解释程序，输出如下： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/a8f7ca00bdd411ef928f525400d5f8ef.png)

### 深入调研代码

Swarm 的核心代码主要位于 Swarm 目录下的 init.py 和 core.py 文件中。让我们逐步分析这些文件的内容：

- 1. 在对话输入框输入提示词：“解释 Swarm 的核心实现，并分析其中的关键部分及其作用”向代码助手进行提问。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/7977972d120511f0a63e5254005ef0f7.png) 对话框的输出如下： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/a9829edb120611f0854e525400454e06.png) 从上面的回答中我们看到了 Swarm 的几个关键模块： **Swarm**：主要的 Swarm 类，用于管理整个系统。
	
	**Agent**：代表单个智能体。
	
	**ContextVariable**：上下文。 并给出了一个 Handoffs 的关键概念，这个概念也是作为轻量级多 Agent 框架的核心链路。
2. 让代码助手生成一个完整的示例，并生成流程图，以加深对 Swarm 的框架了解。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/46c7bef0120711f0ae09525400bf7822.png)

## 总结

在日新月异的技术变革下，自定义知识库可以帮助企业快速提升外部变化，从而在不需要微调模型的前提下，就可以让对话质量更好，更容易的帮助企业开发者提高开发效率。当遇到问题的时候，可以尝试用知识库 RAG 来解决问题。

腾讯云代码助手针对代码、技术文档做了深度的索引优化，对于召回出来的效果，和提升对话的生成质量，起到了关键作用。

欢迎体验腾讯云代码助手的全新能力，自定义知识库，我们支持代码、离线代码库和普通文档，例如 PDF、WORD 等文件。