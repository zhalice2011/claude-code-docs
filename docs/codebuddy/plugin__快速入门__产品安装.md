# Codebuddy 插件

## 插件对主流 IDE 版本要求

| IDE | 最低版本要求 |
| --- | --- |
| Visual Studio Code | 1\.82 |
| Visual Studio | 17\.6（VS 2022） |
| IntelliJ IDEA | 2022\.2 |
| PyCharm | 2022\.2 |
| GoLand | 2022\.2 |
| CLion | 2022\.2 |
| PhpStorm | 2022\.2 |
| Android Studio | Flamingo \| 2022\.2\.1 |
| 微信开发者工具 IDE | 1\.06\.2409140 |
|  |  |

> **注意**：
> 
> - 其他更多 JetBrains 系列 IDE 版本要求请参见 [JetBrains 插件市场](https://plugins.jetbrains.com/plugin/24379-tencent-cloud-ai-code-assistant/versions/stable)。
> - 除市场版本外，JetBrains 另外提供低版本兼容插件，最低可兼容至2020\.3，您可点击 [此处](https://acc-1258344699.cos.accelerate.myqcloud.com/plugins/saas-lower/jetbrains/coding-copilot-latest.zip) 下载。受低版本 JetBrains 能力限制，此插件包无法体验最新的产品功能，建议尽量升级 JetBrains 版本，使用正式版本插件。

## VS Code

1. 安装 Visual Studio Code：建议安装版本 1\.82 及以上，[单击前往 VS Code 官网下载](https://code.visualstudio.com/Download)。
2. 安装插件：

	- **快速安装**：[单击一键安装腾讯云代码助手](https://write.woa.com/vscode:extension/Tencent-Cloud.coding-copilot)，即可快速跳转到腾讯云代码助手的安装界面。
	
	
	> **说明：**
	
	
	> 使用快速安装时，请保证已正确安装 Visual Studio Code，否则无法进行一键安装。
	- **从 IDE 插件市场安装**：您也可以在 VS Code 插件市场手动搜索**腾讯云代码助手**并下载安装。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/8fc1127f13a611f0854e525400454e06.png)
	- **下载安装包**：您也可以 [单击下载最新版本安装包](https://copilot.tencent.com/v2/plugin/download?platform=vscode&version=latest)，并前往 VS Code 手动安装。
	
	![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032954869/f7fdbeda119811ef9eec5254007bbd8c.png)

## Visual Studio

以 VS 2022 为例（VS 2026 安装操作相同），具体详情请参见 [Visual Studio 2022 安装](https://cloud.tencent.com/document/product/1749/115712)。

## JetBrains IDEs

1. 安装 JetBrains IDEs：[下载并安装任意 JetBrains 的 IDE 产品](https://www.jetbrains.com.cn/idea/)，例如 IntelliJ IDEA、WebStorm、PyCharm、PhpStorm、GoLand 等 IDE。
2. 安装插件：

	- **从 IDE 插件市场安装。** 打开插件市场：在右上角的设置中，单击 **插件** 。
	
	![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/1fa8dd5713a811f0854e525400454e06.png)搜索 **腾讯云代码助手**。
	
	![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/fd004b9813a711f0ae09525400bf7822.png)在搜索结果中单击 **安装**。
	
	![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/2310ef0c13a911f0a63e5254005ef0f7.png)
	- **下载安装包**：[单击下载最新版本安装包](https://copilot.tencent.com/v2/plugin/download?platform=jetbrains&version=latest)，并前往 JetBrains IDEs 手动安装。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/5064550513a911f0a63e5254005ef0f7.png)
	- 选择 **从磁盘安装插件**。
	
	![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/8732f9df13a911f0854e525400454e06.png)选择已下载的插件包。
	
	![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/05dba01113aa11f0a9cd5254007c27c5.png)

## 微信开发者工具 IDE

1. 前往 [微信开发者平台 IDE](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html) 下载微信开发者工具，注意需要下载最新**开发版 Nightly Build**。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/ab6f9a85768c11f0bcac525400e889b2.png)
2. 安装完成后，打开微信开发者工具，使用微信扫码登录微信开发者工具。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/fb00c00a768811f09f3d52540099c741.png)
3. 登录后，创建您所需的项目，或者选择您以前所创建的项目并打开。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/3dbad3bd768611f081ce52540044a08e.png)
4. 如果选择创建项目，则根据您的实际需求进行创建。如果没有 AppID，则可以单击注册按钮进行注册小程序账号；或者直接单击测试号，使用测试号作为AppID，但使用测试号时目前暂不支持选择微信云开发。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/04e6a5c0768711f09f3d52540099c741.png)

> **注意：**

> 这里所创建的项目属于演示的项目，并非固定，在实际开发项目中需要根据自己的实际情况填写/选择信息，创建属于自己的项目。
5. 单击**扩展区域**图标，展开热门或者在搜索栏中输入**腾讯云代码助手** 或 **CodeBuddy**，单击腾讯云代码助手右边的**安装**，等待安装完成即可。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/132c6ff1768a11f081ce52540044a08e.png)

> **说明：**

> 腾讯云代码助手插件安装完成后，建议重启一下微信开发者工具。如果出现安装异常，例如下图，您可参考 [不同端功能常见问题](https://cloud.tencent.com/document/product/1749/116012#06de3c55-437d-49fb-8b3f-af5daae004c6) 进行解决。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/14c7bb01768c11f084fc525400bf7822.png)