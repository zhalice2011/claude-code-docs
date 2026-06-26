## CodeBuddy 介绍

腾讯云 CodeBuddy（Tencent Cloud CodeBuddy，以下简称 CodeBuddy），由腾讯云自研的一款专为微信小程序开发设计的编程提效辅助工具，基于腾讯混元 \+ DeepSeek 双轮模型驱动，构建对微信开发者友好，好用易用的代码助手，为微信小程序开发者提供技术问答、Craft 小程序编码智能体、智能代码补全、单元测试、智能评审、代码修复等 Agent 智能体拓展能力，兼容 MCP 开放生态，辅助微信开发者提升编码效率和质量，助力微信小程序开发者。

## CodeBuddy 特性

### 编码智能体 Craft

输入指令，AI 深度理解，自主完成多文件代码生成和改写，自动生成可执行的微信小程序应用。

![Craft编码生成应用效果](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/da7700e878be11f0bda35254007c27c5.png)

### AI 技术对话

人工智能技术对话，将复杂问题轻松解决。

- 基于海量技术文档、微信开发文档、腾讯云API文档等进行训练，并支持团队自定义知识库管理，轻松问答。
- 支持灵活配置和切换多种模型，并支持第三方 DeepSeek 模型接入。
- 技术对话集成微信开发者工具，支持将对话代码内容一键插入编译区当中，快速问答。
- 支持框选或全选编译区代码内容，进行代码规范检查与错误修复。
- 智能生成代码注释，清晰解释既有代码，快速接手历史微信小程序项目。

![AI对话](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/a719c82778bf11f08c4552540099c741.png)

### 代码补全

智能补全，支持多种微信小程序开发语言和框架的生成；基于上下文理解以及开发者编辑行为，智能感知当前微信小程序编码环境，实时提供下一步代码编辑建议，并给出相应推荐，高效完成微信小程序编程工作。

![补全](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/31c4283378c011f09cab525400bf7822.png)

### 支持 MCP 协议

兼容 MCP 开放生态，推动 AI 与外部系统标准化连接，串联端到端的微信小程序开发全流程。

![Mcp](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/b310777078c011f0bd33525400454e06.png)

### 智能代码评审智能体

支持微信小程序代码批量评审，及时发现问题，并给出优化建议。

![代码评审和检查](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/dcc5153378c011f09a9a5254001c06ec.png)

自动生成 commit message，规范开发流程。

![代码评审和检查](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/fb170cca78c011f08c4552540099c741.png)

## 快速安装

下面将介绍如何对新版本的微信开发者工具 IDE 和 CodeBuddy 进行安装和使用。

1. 前往 [微信开发者平台 IDE](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html) 下载微信开发者工具，注意建议下载最新**开发版 Nightly Build**，请根据您的系统选择最新版本进行下载并安装。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/ab6f9a85768c11f0bcac525400e889b2.png)
2. 安装完成后，打开微信开发者工具，使用微信扫码登录微信开发者工具。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/fb00c00a768811f09f3d52540099c741.png)
3. 登录后，创建您所需的项目，或者选择您以前所创建的项目并打开。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/3dbad3bd768611f081ce52540044a08e.png)
4. 如果选择创建项目，则根据您的实际需求进行创建。如果没有 AppID，则可以单击注册按钮进行注册小程序账号；或者直接单击测试号，使用测试号作为AppID，但使用测试号时目前暂不支持选择微信云开发。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/04e6a5c0768711f09f3d52540099c741.png)

> **注意：**

> 这里所创建的项目属于演示的项目，并非固定，在实际开发项目中需要根据自己的实际情况填写/选择信息，创建属于自己的项目。

5. 单击**扩展区域**图标，展开热门或者在搜索栏中输入**腾讯云代码助手**或 **CodeBuddy**，单击腾讯云代码助手右边的**安装**，等待安装完成即可。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/132c6ff1768a11f081ce52540044a08e.png)

> **说明：**

> 腾讯云代码助手插件安装完成后，建议重启一下微信开发者工具。如果出现安装异常，例如下图，您可参考 [不同端功能常见问题](./../../常见问题/不同端功能常见问题#微信IDE无法正常下载安装插件) 进行解决。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/14c7bb01768c11f084fc525400bf7822.png)

## 开始体验

安装完成 CodeBuddy 后即可直接进行体验，下面将以一个案例进行演示。