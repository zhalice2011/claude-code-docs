## RAG 功能简介

RAG（Retrieval\-Augmented Generation），这一检索增强生成技术，与腾讯云代码助手的结合，为用户带来了前所未有的智能体验。它不仅基于大语言模型的海量知识，还随时能接入专业打造的“百科全书”级知识库。这使得腾讯云代码助手在提供研发问答和智能编码服务时，更加精准、全面，有效避免了模型幻觉，助力开发者高效解决问题，提升编码效率。接下来介绍一下使用流程。

## 基于预置知识库，快速体验 RAG

### 代码助手中的 @ Docs

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/d1bf5f20480011f0914c52540044a08e.png)

代码助手中的 **@ Docs** 是指更多类型的上下文，Extra Context Info。我们对 **@ Docs** 的触发位置没有要求，您可以把 **@ Docs** 知识库放在对话描述的任意位置。

在对话输入框中，单击 **@ Add** 然后选择 **Docs** ，或者输入 **@** 然后选择 **Docs** 调用预置的知识库。 知识库涵盖主流的代码仓库集合：

- 腾讯云实时音视频：实时音视频接口文档、辅助迁移文档。
- UnrealEngine 4\.5：UnrealEngine 4\.5版本知识库。
- TDesign：TDesign 组件 API 知识库 。
- Spring Boot：Spring 开发框架。
- Spring AI：基于 Spring 的 AI 应用框架。
- LangChain：基于 Langchain 的 AI 应用工具包。
- React：前端开发框架。
- Vue：前端开发框架。
- 腾讯云 API：腾讯云 API 开发知识库。
- LeaferJS：前端 Canvas 2D 引擎。
- 微信支付：微信支付开发知识库。
- 微信小程序：微信小程序开发知识库。
- 微信小游戏：微信小游戏开发知识库。
- 微信云开发：微信云开发\+云托管。
- 云原生构建：CNB 知识库。 如果您有更好的仓库或知识库期望预置，可以 [联系我们](https://cloud.tencent.com/document/product/1749/104249) 提出建议。

### VSCode 使用步骤

打开侧栏腾讯云代码助手，并在如下的输入框里选中上述内置的知识库。我们提供两种快速输入方式：

【通过键盘输入】

1. 直接输入 **@ 知识库名字**。为追求体验，当您输入的过程我们就启动过滤知识库。可以通过键盘上下键，选中后回车即可。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/08f9cbaa4a9611f08548525400454e06.png)
2. 选择知识库后，在输入框上方的操作条中会展示所添加的知识库，接下来输入问题描述即可引用知识库作为上下文，例如下图所示。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/3c6a94314a9611f0930e525400bf7822.png)

【通过鼠标单击】

1. 鼠标单击 **@ Add**，选择 **Docs**，然后再选择您需要的知识库。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/923a5876480a11f0914c52540044a08e.png)
2. 选择**知识库**的数据类型后，我们会列出所有内置的知识库。这里的知识库，是一系列相关的仓库的合集，包括官方知识库和自定义知识库。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/3e7406b6480b11f092f25254007c27c5.png)

### JetBrains 使用步骤

同 VSCode 的操作一样，您可以通过键盘或者鼠标的两种方式选中内置的知识库。

【通过键盘输入】

1. 输入 **@** **知识库名字**，然后通过键盘上下键，选中知识库后回车即可，如下图。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/962f3c164a9311f0b25352540099c741.png)
2. 选择知识库之后，在输入框上方的操作条中会展示所添加的知识库，接下来输入问题描述即可，例如下图所示。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/d418cc584a9511f0914c52540044a08e.png)

【通过鼠标输入】

1. 鼠标单击 **@ Add**，选择 **Docs**，然后再选择您需要的知识库。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/a771c0674a8811f0b25352540099c741.png)
2. 选择知识库的数据类型后，会列出所有的知识库，包括官方知识库和自定义知识库。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/0306241b4a8911f08548525400454e06.png)

### 执行过程

您可以在对话框中的任意位置选择所需的知识库，以基于 RAG 技术加强本次提问的结果。回车后，腾讯云代码助手会根据提问和选定的知识库首先检索与问题相关的资料作为参考，然后将这些资料和提问内容一同提交给大模型，从而生成比之前更精确的答案。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/88e1cb614a8911f08957525400e889b2.png)

#### VSCode 的效果

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/9b1fd63f4a8a11f0b25352540099c741.png)

#### JetBrains 的效果

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/0ec63a764a8b11f092f25254007c27c5.png)

### 支持多个知识库同时选择

您还可以选择多个知识库。例如可以引入前后端知识库，并提问如下图所示，腾讯云代码助手会结合知识库的召回作为参考，并生成前端部分和后端部分。

- 前端： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/f23f20d04a8b11f08548525400454e06.png)
- 后端： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/11e672c14a8c11f08bfe5254005ef0f7.png)

## 通过自定义知识库，定制企业私有 RAG

腾讯云代码助手允许企业创建专属的自定义知识库，并且支持的文件类型有单文档、多文档、文档压缩包、离线代码库等。企业管理员可以将企业知识库中上传的文档和文件等内容整合起来，便于企业开发者在回答问题时将其作为上下文参考，从而使代码助手的回答更贴合企业特点。

### 创建自定义知识库

创建自定义知识库只需要如下几步操作即可：

1. 创建知识库空间：

	- 输入名称（20个英文字符或10个中文字符） \-\- 必填。
	- 描述（30个英文字符或15个中文字符） \-\- 选填。
	- 可见范围：必选，默认是企业所有成员。可设置部分成员可见，支持输入搜索选择和在下拉选项列表中直接选择。 单击**确定**创建完成，整体截图如下： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/658b88d74a8f11f085275254001c06ec.png)
2. 上传文件： 为当前知识库添加文件，支持以下类型：
- 文档：支持 .md、 .markdown、.docx、.pdf 格式，每个文档不超过30MB。
- 压缩包：支持 .zip、.tar、.tgz、.tar.gz、.gz、.gzip 格式，每个压缩包不超过100MB，解压后文件不超过500个。

	- 文件内容命名要遵循 utf\-8、GBK 编码，暂时不支持其它格式的编码。 注意：限免期类型有限，会在近期新版本中逐步放开文件大小和类型的限制。 ![4de15f504a8e11f0b25352540099c741](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/4de15f504a8e11f0b25352540099c741.png)

单击**添加数据**，进入添加文件页面。支持**文件拖拽**和单击**选择文件**两种交互。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/33b95e2d4a8e11f0b25352540099c741.png) 以这个 [GitHub](https://github.com/leaferjs/draw) 仓库为例： 单击并下载成 ZIP 包后，然后拖拽到当前页面后，单击**确定**后，会进行后端解压，如果遇到限制会给出失败原因。没有问题后则上传成功，并返回到知识库的首页展示文件列表。每个文件都有直观的索引状态展示。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/851c96b34a8e11f08bfe5254005ef0f7.png)

3. 等待索引完毕后开启知识库。

	- 数据处理状态：索引中、索引失败、已完成。
	- 索引中和索引失败的数据不可启用。
	- 索引完成的数据默认启用。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/b1a6f0c44a8e11f08957525400e889b2.png) 返回知识库首页，开启知识库。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/4f1255574a8f11f08957525400e889b2.png)

### 更新自定义知识库

通过以下两种方式修改知识库的基本信息，包括知识库的名称、描述；也可以对已经有的知识库进行文件的添加。

- 从知识库列表编辑：在知识库列表中选择对应知识库，单击**编辑**，即可进入知识库编辑模式。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/a67fd6974a8f11f08548525400454e06.png)
- 知识库内页面编辑：进入对应知识库内，单击名称边上的按钮进行编辑，回车即完成保存。同时，也可以添加数据或对知识库进行设置。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/e7b9ff694a8f11f08957525400e889b2.png)

### 使用自定义知识库

#### 版本要求

- **适用版本**：腾讯云代码助手旗舰版、专享版、企业版。
- **插件版本**：需要升级到最新版本。

#### VSCode 使用步骤

1. 当前用户如果处于企业组织，且企业组织下有自定义知识库，那么 @ Docs 知识库下就会出现**自定义知识库**。如下： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/dbbcbf934a9111f0930e525400bf7822.png)
2. 您可以通过键盘或者鼠标的两种方式选中内置的知识库。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/d22c311c4a9611f0914c52540044a08e.png)
3. 接下来我们看看效果。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/4aa03d364a9711f08548525400454e06.png)

#### JetBrains 使用步骤

1. 当前用户如果处于企业组织，且企业组织下有自定义知识库，那么 **@ Docs** 知识库下就会出现**自定义知识库**分类。如下： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/722e63db4a9711f08957525400e889b2.png)
2. 执行后的效果如下： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/ba0948a74a9711f0b25352540099c741.png)