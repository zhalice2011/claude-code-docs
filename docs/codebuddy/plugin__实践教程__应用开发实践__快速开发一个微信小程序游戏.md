腾讯云代码助手已经支持在微信开发者工具 IDE 下的编码辅助，在代码辅助的效率上有很大提升，通过自然语言描述就可以完成最终应用。并且，支持了全新软件开发智能体 Craft，输入自然语言指令，支持文件多选，AI 深度理解代码工程，自主完成工程多文件代码生成和改写，快速落地可执行应用。现在，为您介绍如何利用软件开发智能体 Craft 来快速开发一个微信小程序游戏—**五子棋**。

## 准备工作

1. 请前往 [微信开发者工具下载网址](https://developers.weixin.qq.com/miniprogram/dev/devtools/stable.html)下载微信开发者工具并安装，建议下载最新稳定版即可，例如现在的最新稳定版是 **1\.06\.2503310**。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/a3e17a8f4fe011f08a7252540099c741.png)
2. 想要了解更多开发资料的可前往 [小程序开发微信官网文档](https://developers.weixin.qq.com/miniprogram/dev/framework/) 查看相关参考文档。
3. 安装完微信开发者工具后，打开进行微信扫码登录。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/cca9e8d34fe111f0a6ac525400bf7822.png)
4. 创建小程序项目，单击左侧导航栏中的**小程序**，出现如下页面，填写信息创建小程序项目。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/dcfeed644fe211f08bba5254001c06ec.png)

	- 项目名称：可自定义。
	- 目录：可自定义。
	- AppID：如果没有注册小程序账号可以单击**注册**前往进行注册；或者直接单击**测试号**使用测试员来创建。
	- 后端服务：因为小程序游戏还不需要后端，所以这里选择了不使用云服务。
	- 开发模式：选择**小程序**。
	- 初始化：选择**模板**来创建。
	- 模板选择：选择**TS\-基础模板**即可。 填写完信息后单击**创建**即可。
5. 创建完小程序项目后，在**扩展**中，输入**腾讯云代码助手**或 \*\*CodeBuddy \*\*安装腾讯云代码助手插件。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/126f9ffc4fe411f0a6ac525400bf7822.png)

> **说明：**

> 安装插件完成后，建议重启一下微信开发者工具；如果出现安装异常，例如下图所示，可参考[不同端功能常见问题](https://cloud.tencent.com/document/product/1749/116012#06de3c55-437d-49fb-8b3f-af5daae004c6)进行解决。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/acbe53994ffb11f0ada05254007c27c5.png)
6. 单击腾讯云代码助手 icon，或底部右下方区域的\*\* AI 问答\*\*，即可进入全新软件开发智能体 Craft 模式，开启编码之旅。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/d90e44694fe411f09d0a525400454e06.png)

## 开始开发

### 应用 Craft 开发智能体进行开发

1. 先对 Craft 进行设置。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/bca683b44ffc11f0ada05254007c27c5.png)这三个设置默认为关闭状态。
- 自动运行：启用自动运行后，Craft 会根据计划自动执行任务，减少人工操作。
- 自动修改文件：启用自动修改文件后，Craft 能够对文件进行生成和改写。
- 确认计划：启用确认计划后，Craft 将根据需求进行拆解任务，制定计划并澄清需求。如果需求不明确 Craft 会进行询问，您只需回复直到需求清晰后，单击开始按钮或者回复请生成代码，即可开始执行计划。
2. 输入描述需求提示词。可参考下面的提示词。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/e2813ec84ffe11f08a7252540099c741.png)
3. 在输入需求描述后，如果您开启了**确认计划**，那么 Craft 在开始之前会先了解当前项目情况，并仔细分析需求。当有不明确的需求时会向您询问，您只需要一直回复即可。确认需求后，Craft 开始基于需求生成一份完整的执行计划。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/2f8f611f500011f09bf25254005ef0f7.png)
4. 确认需求后，Craft 生成一份完整的执行计划。如果满意，单击**开始**即可。如果不满意，您可以继续提需求，Craft 会基于最终的确认需求生成一份完整的计划。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/5457190a500211f0a6ac525400bf7822.png)
5. 开始执行计划。当 Craft 执行一段时间后，会询问您是否继续或有无新的需求。如果没有新需求，单击**继续**即可。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/96b01a1f500411f0a6ac525400bf7822.png)
6. Craft 根据执行计划 ，完成了小程序游戏的开发工作。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/900032f9500511f08bba5254001c06ec.png)
7. 接下来，运行程序，验证程序是否有编译错误。当输入运行程序的需求后，Craft 会向您询问是否运行。这里有两种模式可以选择：**每次询问**和**自动运行**，如果不需要每次向您询问，可以选择设置成**自动运行**，设置后将全局生效，后续的对话将自动运行。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/04b4704f500611f08bba5254001c06ec.png)
8. 编译运行程序后，发现无法精准落子，此时可以继续输入问题与 Craft 进行对话，让 Craft 继续优化代码。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/dd7ea028501811f0a97752540044a08e.png)
9. 重新编译运行程序，可以看到五子棋的微信小程序游戏可以精准落子，功能正常。您还可以继续基于实际需求进行版本迭代。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/3e7d04cc52ff11f095fc5254001c06ec.png)

### 优化代码的艺术

最后，我们来把项目工程优化一下，然后把核心逻辑解读并重构一下。

1. 生成文档注释。 腾讯云代码助手贴心的给出了三种方法生成文档注释：
- 方法一：通过圈选核心代码，右键，选择 **CodeBuddy** \> **生成文档**，如下： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/79371769530311f0a63e525400e889b2.png)
- 方法二：进入插件的高级设置（下图圈1），开启③和④。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/cdfd279f530411f0abce52540099c741.png) 返回代码后，可以在函数头或者鼠标悬浮后出现蓝色提示，单击**生成文档**，如下图： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/2fbae296530511f090d5525400bf7822.png)
- 方法三：直接使用快捷键，如下：

```
  | 系统      | 快捷键         |
  | ------- | ----------- |
  | Mac     | Opt+D       |
  | Windows | Shift+Alt+M |

```
我们看看生成的文档效果如下，满意的话单击**采纳**就可以直接应用：![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/1583b052122b11f0a63e5254005ef0f7.png)
2. 重构代码。 无论是语法错误，还是逻辑问题，或者是代码需要重构，一个 /fix 就可以帮我们 AI 检查。我们可以在对话框中使用 /fix 进行提问。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/2d722aa5530611f09a935254007c27c5.png)输出如下，我们可以选择应用代码。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/cea99252530611f095fc5254001c06ec.png)代码助手提供了智能插入的方法，通过大模型为其生成合并的 Diff View 预览效果，如下图，清晰很多了。代码助手在如下视图下可以选择部分采纳或者全部采纳：![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/2f264fd9530711f090d5525400bf7822.png)
3. 运行错误查询原因。我们在开发中有时会发现如下图的错误，我们可以鼠标右键单击错误信息，选择 **CodeBuddy：优化代码**，它能正确的给我结合当前工程代码进行分析，给出正确的解决方案。如下图，发现错误后，给出优化建议和代码，通过选择对话代码区域的 **Apply** 运行后，右边出现了 Diff View 预览，全部采纳后，问题解决。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/ce4cddf7530711f0bf84525400454e06.png)

## 总结

本文通过腾讯云代码助手来帮助开发五子棋的微信小程序游戏。可以发现，代码助手能够极大地帮助我们通过自然语言描述需求来生成工程代码，尤其是 **Craft** 智能体的支持，让小白也能快速实现自己的个人应用，做自己的产品经理。还可以帮助优化代码、生成代码注释等，是一个非常强大的编程辅助工具。同时，我们在与代码助手的对话过程中，注意要学会提示词的编写，良好的提示词能够让代码助手更容易理解需求，起到一个事半功倍的效果。