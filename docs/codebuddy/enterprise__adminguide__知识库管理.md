## 通过自定义知识库，定制企业私有 RAG

腾讯云代码助手允许企业创建专属的自定义知识库，并且支持的文件类型有单文档、多文档、文档压缩包、离线代码库等。企业管理员可以将企业知识库中上传的文档和文件等内容整合起来，便于企业开发者在回答问题时将其作为上下文参考，从而使代码助手的回答更贴合企业特点。

### 创建自定义知识库

创建自定义知识库只需要如下几步操作即可：

1. 创建知识库空间：

	- 输入名称（20个英文字符或10个中文字符） \-\- 必填。
	- 描述（30个英文字符或15个中文字符） \-\- 选填。
	- 可见范围：必选，默认是企业所有成员。可设置部分成员可见，支持输入搜索选择和在下拉选项列表中直接选择。 单击**确定**创建完成，整体截图如下： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/37ab7ea447ff11f092f25254007c27c5.png)
2. 上传文件： 为当前知识库添加文件，支持以下类型：
- 文档：支持 .md、 .markdown、.docx、.pdf 格式，每个文档不超过 30MB。
- 压缩包：支持 .zip、.tar、.tgz、.tar.gz、.gz、.gzip 格式，每个压缩包不超过 100 MB，解压后文件不超过 500 个。

	- 文件内容命名要遵循 utf\-8、gbk 编码，暂时不支持其它格式的编码。  
	![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/72e57b354a9811f0930e525400bf7822.png)
	
	单击**添加数据**，进入添加文件页面。支持**文件拖拽**和**单击选择文件**两种交互。
	
	![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/97cddc0c4a9811f08548525400454e06.png) 以这个 [GitHub](https://github.com/leaferjs/draw) 仓库为例： 单击并下载成 ZIP 包后，然后拖拽到当前页面后，单击确定后，会进行后端解压，如果遇到限制会给出失败原因。没有问题后则上传成功，并返回 到知识库的首页展示文件列表。每个文件都有直观的索引状态展示。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/b1fbe7544a9811f085275254001c06ec.png)

3. 等待索引完毕后开启知识库。

	- 数据处理状态：索引中、索引失败、已完成。
	- 索引中和索引失败的数据不可启用。
	- 索引完成的数据默认启用。  
	![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/cddd3ba04a9811f0b25352540099c741.png) 返回知识库首页，开启知识库。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/ea1a1b464a9811f08548525400454e06.png)

### 更新自定义知识库

通过以下两种方式修改知识库的基本信息，包括知识库的名称、描述；也可以对已经有的知识库进行文件的添加。

- 从知识库列表编辑：在知识库列表中选择对应知识库，单击**编辑**，即可进入知识库编辑模式。  
![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/0ce6bfe24a9911f08957525400e889b2.png)
- 知识库内页面编辑：进入对应知识库内，单击名称边上的按钮进行编辑，回车即完成保存。同时，也支持添加数据或对知识库进行设置。  
![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/214a71374a9911f08bfe5254005ef0f7.png)

### 使用自定义知识库

#### 适用版本

| **适用版本** | 腾讯云代码助手旗舰版、专享版、企业版。 |
| --- | --- |
| **插件版本** | 需要升级到最新版本 3\.1\.20。 |

#### VSCode 使用步骤

当前用户如果处于企业组织，且企业组织下有自定义知识库，那么 @ Docs 知识库下就会出现**自定义知识库**分类。如下：

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/7af69bf24a9911f0b25352540099c741.png)

您可以通过键盘或者鼠标的两种方式选中内置的知识库。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/8a4f6edd4a9911f08957525400e889b2.png)

接下来我们看看效果：

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/9dee24d04a9911f0930e525400bf7822.png)

#### JetBrains 使用步骤

当前用户如果处于企业组织，且企业组织下有自定义知识库，那么 @ Docs 知识库下就会出现**自定义知识库**分类。如下：

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/b158d6b54a9911f085275254001c06ec.png)

执行后的效果如下：

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/d06612a14a9911f0914c52540044a08e.png)