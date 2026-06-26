腾讯云代码助手新增了管理端创建和管理提示词的功能，包括**自定义指令**和**全局提示词**。

> **说明：**

> 自定义指令和全局提示词目前仅支持企业账号使用。

## 自定义指令

### 自定义指令介绍

- 作用：支持自定义指令，满足编码场景中对自定义扩展指令的需求。
- 使用自定义指令的优势：

	- 提高工作效率：通过设置自定义指令，开发者可以快速调用常用的代码片段或函数，避免重复输入和查找。这不仅节省了时间，还能让开发者更专注于逻辑和创意的实现。
	- 个性化编程体验：每位开发者都有自己的编程风格和习惯。自定义指令功能允许用户根据自己的需求调整 AI 的响应方式，使其更符合个人的工作流程和思维方式。
	- 促进团队协作：在团队开发中，使用统一的自定义指令可以帮助团队成员保持一致的编码风格和规范。这有助于提高代码的可读性和可维护性，减少沟通成本。

### 创建自定义指令

1. 登录 [企业后台管理](https://copilot.tencent.com/admin)。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/7ca53d2a621611f0b30d5254007c27c5.png)
2. 左侧导航栏选择**自定义指令**，在**自定义指令**下单击**创建指令**。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/c2b3ce86621611f0ad0f5254005ef0f7.png)
3. 在创建自定义指令页面下，根据提示输入**指令名称**、**指令描述**、**提示词描述**，选择**上下文。**![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/92e75238621711f091585254001c06ec.png)

	- **上下文**中的**添加知识库。** 可以选择添加或不添加知识库，如果选择添加知识库，那么调用该自定义指令后即可关联知识库，增强生成质量。添加知识库可以按照如下2步进行：
	
	3\.1 勾选**添加知识库**后，功能启用，然后单击**选择**添加知识库。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/c6e4ff4a621711f0a64452540099c741.png)
	
	3\.2选择需要添加的知识库，可以选择官方知识库和自定义知识库。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/0486088e621811f0ad0f5254005ef0f7.png)
	
	
	> **说明：**
	
	
	> 如果没有自定义知识库，请参见 [知识库管理](./知识库管理) 创建自定义知识库。
- **上下文**中的**引用文件。**

如果选择开启**引用文件**功能，那么调用该自定义指令即可关联当前工程文件。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/43b14a43621811f0b30d5254007c27c5.png)
- CodeBase：功能启用后，调用指令会加入整个工程为上下文。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/83fa19fc621811f0a64452540099c741.png)
4. 输入完成后，单击**保存**。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/bcb0c517621911f0b324525400e889b2.png)
5. 返回上一层自定义指令面板，确认自定义指令已开启，默认为开启状态。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/e0bd0267621911f091585254001c06ec.png)

### 调用指令示例展示

#### VS Code

1. 在对话框直接输入`/`调用指令。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/60f5f8c9622811f0b30d5254007c27c5.png)

> **说明：**

> 如果调用时没有所创建的自定义指令，可以尝试重启 IDE 软件或者确保处于企业组织下。

2. 输出结果。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/9b3c79b4622811f0ad0f5254005ef0f7.png)

#### Jetbrains IDE

1. 在对话框直接输入`/`调用指令。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/3d302e2b622c11f0b30d5254007c27c5.png)
2. 输出结果。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/d111e1d962b911f097ec52540044a08e.png)

## 全局提示词

### 介绍

- 全局提示词的作用：允许企业团队添加全局提示词，代码助手会根据自定义的全局提示词生成代码的命名规则、注释标准、代码结构等内容。通过这些提示词，代码助手可以更好地理解我们的编码习惯，从而生成质量更高、更加一致的代码。
- 使用全局提示词，会应用到所有对话请求中，主要体现在：

	- 为所有的官方指令额外增加全局提示词，这里的官方指令例如： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/1437266f622911f0ad0f5254005ef0f7.png)
	- 为所有的自定义指令额外增加全局提示词，这里的自定义指令例如： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/2f1c1cd7622911f0b30d5254007c27c5.png)
	- 为普通对话添加额外的全局提示词。普通对话，即使用对话框中的对话。

### 添加全局提示词

1. 登录 [企业后台管理](https://copilot.tencent.com/admin)。
2. 左侧导航栏单击**自定义指令**，进入自定义指令面板，然后选择**全局提示词**。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/d3c9128b621b11f0b30d5254007c27c5.png)
3. 输入全局提示词描述，然后单击**保存**即可。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/578a4fd2621c11f0a64452540099c741.png)

### 示例展示

1. 添加下面的全局提示词。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/847810c0621c11f0ad0f5254005ef0f7.png)
2. 圈选代码后，在对话框中直接调用指令`/tests` 来生成单元测试。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/de91b5ea62d911f0bac1525400454e06.png)
3. 输出结果：

	- 添加全局提示词前的测试用例代码： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/b5aa004262da11f092fe525400bf7822.png)
	- 添加全局提示词后的测试用例代码： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/e8d4bf4262da11f0a64452540099c741.png)从上图的输出结果中可以对比看到，所添加的全局提示词已经被应用到对话中，增加了 SpringBootTest 来编写单元测试。