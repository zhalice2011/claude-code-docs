## 插件端通用问题

### 插件下载安装问题

#### 插件市场无法搜到插件？

通过 [插件安装](./../快速入门/产品安装) 检查 IDE 类型及版本是否支持。

#### 通过官网或渠道下载的插件无法安装？

通过 [插件安装](./../快速入门/产品安装) 检查 IDE 类型及版本是否支持。

### 插件登录问题

#### 插件登录网络异常？

- 异常现象：网络通信异常，显示设备连不上代码助手域名。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/0197cfb4138311f0ae09525400bf7822.png)
- 解决办法：

	- 重启 IDE 重新登录。
	- 检查网络连接是否正常。
	
	
		- SaaS 测试：打开 [腾讯云\-华佗诊断](https://itango.tencent.com/app/data/huatuo) 或 [Itango\-网络诊断](https://itango.tencent.com/app/data/huatuo?app_version=3.29.21.412&app_sdk_id=0300000000&app_publish_channel=TencentInside&os_version=15.0.1&app_lang=zh-cn&os_name=Mac&c_district=0&app_instance_id=2)，输入域名：copilot.tencent.com 后进行检测。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032954869/dc3e5c47f3e811efb00452540044a08e.png) 查看结果： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032954869/dc4144c3f3e811ef920e5254005ef0f7.png)
		- 私有化测试：私有化地址沟通管理员获取。
		
		
			- Windows：`ping -n 100 -l 1400 copilot.tencent.com`（替换为私有化地址）。
			- Mac：`sudo ping -c 100 -i 0.2 -s 1400 copilot.tencent.com`（替换为私有化地址）。
			- Linux：`sudo ping -c 100 -f -s 1400 copilot.tencent.com`（替换为私有化地址）。
			
			
			```
			主要关注 ping 的丢包率和 RTT，如下图（有明显丢包）：
			
			```
			![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032954869/dc21cd35f3e811efa823525400e889b2.png)
- 检查是否有系统代理干扰。
- 检查防火墙连接是否正常。具体请参见 [防火墙配置](./../操作指南/防火墙配置)。
- 检查 host 配置是否正常，排查是否有异常 host 干扰代码助手地址。

### 插件使用问题

#### 功能使用异常，如对话功能使用异常？

- 重新触发功能。
- 检查网络连接问题。

#### 对话或补全生成效果异常？

- 补全生成效果异常：

	- 异常现象：补全重复、补全质量差，生成幻觉代码、补全代码存在安全风险（漏洞、敏感信息等）、补全代码存在括号异常问题。
	- 解决方法：模型问题，收集报错信息并反馈。根据不同端收集报错信息参考底部。
- 对话生成效果异常：

	- 异常现象。
	
	
		- 返回结果的代码未高亮：左上角标注“PlainText”，模型错误返回了伪代码，未指明代码格式。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032954869/02009addf3e911efb00452540044a08e.png)
		- 结果质量问题：对话结果不满意，不符合业务需求。
		- 安全问题：对话返回结果非编程类并出现一切与社会主义核心价值观相悖、危害国家社会和个人身心健康的有害内容；对话返回代码存在安全、合规风险。
		- 功能异常问题：侧栏对话框指令失效，对生成结果的复制、应用到代码、新建文件等功能失效。
	- 解决方法：模型问题，收集报错信息并反馈。请参见底部 [根据不同端收集报错信息](#不同端收集报错信息)。

### 插件升级问题

#### 插件未正常升级？

解决方法：

- 自动更新未生效，单击 IDE 内产品图标，手动单击**检查更新**触发手动升级。
- 检查其他功能是否正常使用，是否有网络问题或代理干扰。
- 低版本 JB\-IDE 插件无法自动升级，需要手动下载插件包更新。
- 检查是否对插件扩展全局禁用。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/6c1a355c138411f0ae09525400bf7822.png) 如果对插件扩展全局禁用，则选择**启用所有扩展**启动扩展。

#### 评审变更失败？

- 异常现象：使用代码评审变更功能时提示："**Git model not found**"。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/af7bb696256911f08caa5254005ef0f7.png)
- 解决方法：根据您使用的操作系统选择 [安装 Git](https://git-scm.com/downloads)，然后再重新尝试。

### 远端环境安装问题

#### 背景

对于需要使用 AnyDev 云研发的用户，需要在云研发环境中安装 CodeBuddy 插件，否则将不能正常使用 CodeBuddy 插件，例如：

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/0e6ececf78b711f08255525400e889b2.png)

CodeBuddy 分析工程扫描工作区目录时，扫描的是本地目录，而非远端机器目录，导致分析失败。

#### 远端插件安装

##### 前置条件

您需要在 AnyDev 云研发中开通**个人云服务器 CVM** 或 **开发容器。**

##### **安装**

- **方式一**：安装有 **JetBrains Gateway****Step1**：在开通的个人云服务器 CVM 或 开发容器的云研发环境中，选择对应的 IDE 进行连接。路径：**云研发** \> **选择开通的云研发环境** \> **单击选择对应的 IDE 连接**，会自动拉起 Gateway 在远程服务器中部署和连接 IDE 后端。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/9989d1f378dc11f09cab525400bf7822.png)**Step2**：插件同步到远端或远端路径下直接安装。

	- 连接 IDE 后端后，在 IDE 后端中直接安装。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/6da996fc78de11f0960452540044a08e.png)注意：在云研发中，这里插件的安装需要安装在 Client 端中。
	- 使用本地 VSCode 进入 AnyDev 云研发环境，在扩展页的云研发环境栏中，单击下图中的**下载**按钮，在弹出的插件菜单选项中选择 **Tencent Cloud CodeBuddy** 插件，即可将本地插件同步到云研发环境中。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/fff811e878df11f0960452540044a08e.png)
- **方式二：** 本地 VS Code 通过 SSH 连接方式 **Step1**：在本地 VS Code 中，新建远程使用 SSH 命令进行连接。命令格式：`ssh hello@microsoft.com -p port`，其中 hello 为远程服务器的用户名，microsoft.com 为远程服务器的域名，port 为端口号。您也可以在 iOA 中直接获取 SSH 连接命令。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/85d7ba7178e211f08c4552540099c741.png)**Step2：** 插件同步到远端或远端路径下直接安装，同**方式一**。

## VS Code 插件问题

### 插件登录问题

#### VS Code 登录插件无法唤起浏览器

- 预期现象：单击登录能提示打开外部网站 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032954869/1530f080f3ec11efb67252540099c741.png)
- 解决方法：

	- Visual Studio Code 内问题排查。
	
	
		- 在设置中搜索：`@id:workbench.externalBrowser`
		- 将默认浏览器设置为 Chrome。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/2139e52b138711f0a63e5254005ef0f7.png) 设置完成后重启 IDE，再重新登录。
	- 系统默认浏览器问题排查。
	
	
		- Windows：在设置中，搜索 HTTPS 类型的默认应用，设置为 Chrome 后重试。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032954869/155bca1af3ec11efbda7525400454e06.png)
		- Mac：在设置中，将默认网页浏览器，设置为 Chrome 后重试。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032954869/154aa3d9f3ec11ef9b7d525400bf7822.png)

#### 登录身份认证失败？

- 异常现象：登录时插件报错，提示：**timeout of 30000ms exceeded**. ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/bff9fe625d3611f0857a525400e889b2.png)
- 解决办法：

	1. 顶部搜索框输入 `>show out`，并选择**显示输出通道**。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/c02be9a45d3611f0ba94525400454e06.png)
	2. 然后选择输出通道为 **CodeBuddy**。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/bfc8d4035d3611f094cd52540099c741.png)
	3. 复制下图中相对位置的链接并在浏览器打开，进行扫码登录。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/d038be5d5d3611f0ba94525400454e06.png)

### MCP Server 安装问题

#### MCP 市场一键安装 MCP Server 失败？

- `npx` 或 `Node.js` 未安装。

	- 异常现象： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/d3d10a671b6b11f0b5c65254001c06ec.png)
	- 解决方法：先确保已准备好安装 `MCP Server` 的依赖环境，如下：
	
	
		- Windows：安装 `npx` 要求 `npm 5.2.0`及以上版本。可参考以下文档安装 `npx` 和 `uvx`：
		
		
			- npx：[nvm\-windows](https://github.com/coreybutler/nvm-windows)
			- uvx：[uv](https://github.com/astral-sh/uv)
		- Mac：可参考以下文档安装 `npx` 和 `uvx`：
		
		
			- npx：[nvm](https://github.com/nvm-sh/nvm)
			- uvx：[uv](https://github.com/astral-sh/uv) 安装好依赖环境后再尝试重新安装 `MCP Server`。
- `npx` 未正确安装或未配置环境变量

	- 异常现象：已安装 `Node.js` 和 `npx`，安装 `MCP Server` 时提示：`spawn npx ENOENT`。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/cc5b3e7e1e9011f0a7ba5254001c06ec.png)
	- 解决方法：重启 IDE，再重新尝试安装 `MCP Server`。

#### 安装 MCP Server 32000报错？

- 异常现象：安装 MCP Server 时提示 **MCP error \-32000: Connection closed**。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/6e578c754b7811f085275254001c06ec.png)
- 解决方法：

> **说明：** 以下解决方法只针对 howtocook\-mcp 这个例子，如果您在安装其它 MCP 时遇到同样报错问题，可参考以下方法尝试解决。

	1. 尝试在终端手动执行命令：`npx -y howtocook-mcp`。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/e7a74f354c0d11f0914c52540044a08e.png)
	2. 防止 VS Code 的环境变量没有识别到 npx，需要重启 VS Code。并升级 node 版本至更高版本后，尝试重新连接 MCP。 如果执行以上操作后依旧报错，可以继续尝试以下方法：
	3. 清理日志，并重新连接 MCP。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/99781af24c0f11f0930e525400bf7822.png)
	4. 复制以下配置内容并更换，然后在终端执行命令：`npm install -g howtocook-mcp` 后重新连接 MCP。
	
	bash
	```
	"howtocook": {
	 "command": "howtocook-mcp",
	 "args": []
	}
	```
	![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/709437844c1011f085275254001c06ec.png)

## JetBrains IDEs 插件问题

### 插件安装或升级问题

#### Windows 系统无法正常升级插件？

- 异常现象：升级插件时报错。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/e947f39d057411f08bc5525400454e06.png)
- 解决方法： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/c3dd6e58138711f08c275254001c06ec.png)**方案1**：当弹出此窗口时，不点立即重启，而是直接手动关闭 IDE，之后再手动打开。 **方案2**：暂时先不处理弹窗，打开**任务管理器**，单击**详细信息**，然后找到 language\-server\-win\-x64\.exe 这个进程右键结束任务，之后再单击立即重启。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032954869/38d3c29b088011f0890f52540099c741.png)

### 插件卸载问题

#### Windows 系统无法卸载插件？

- 解决方法： 方案1：先将插件禁用，并手动关闭 IDE，手动重启 IDE，然后保持禁用状态下，卸载插件，之后重启 IDE 即可。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/5367a417138911f09b3252540044a08e.png) 方案2：同更新场景，打开**任务管理器**，单击**详细信息**，然后找到 language\-server\-win\-x64\.exe 这个进程右键结束任务，之后在插件市场卸载即可。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032954869/d800393b088011f0890f52540099c741.png)

### 插件使用问题

#### 3\.1\.12 版本插件页面空白并提示正在初始化？

- 异常现象：登录后插件页面空白并提示初始化中。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/0d8c022b4b4411f085275254001c06ec.png)
- 解决方法：更新至 3\.1\.13 版本。

#### Craft 的模型输出乱码？

- 异常现象：使用 Craft 时模型输出乱码。 【现象一】 如下图所示： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/e424556f4c1111f0914c52540044a08e.png) 【现象二】 如下图所示： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/f9bd58d54c1111f08548525400454e06.png)
- 解决方法：将 **Editor › General › Console** 路径下的 **Default Encoding** 设置为 GBK。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/fbab96fd4c1511f08bfe5254005ef0f7.png)

## Android Studio 插件问题

### Craft 使用问题

对于 Android Studio 用户，您需要先手动安装 JCEF，才能体验 Craft 功能。您可以参考下面的操作进行安装。

1. 在 Android Studio 的搜索中选择\*\* Actions\*\*。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/4443bffd2fe211f0948f52540099c741.png)
2. 在输入框中输入并搜索 **choose boot java runtime for the IDE...**。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/62200ccd2fe211f08caa5254005ef0f7.png)
3. 选择和当前 IDE 匹配且带有 JCEF 的版本。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/c8b3b03d2fe211f09e67525400bf7822.png)
4. 重启 IDE，重新加载插件视窗即可正常使用，如下图。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/39e302c42fe311f0948f52540099c741.png)

## 微信开发者工具问题

### 插件下载安装问题

#### 微信 IDE 无法正常下载安装插件？

- 异常现象： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/e4418521138a11f0ae09525400bf7822.png)
- 解决方法：

	- 清除编辑器缓存。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/5cb09a41138b11f0aaa3525400e889b2.png) 清除编辑器缓存后，重新下载安装试试。
	- 清空缓存文件夹。
	
	
		1. 打开编辑器扩展目录。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/a410de3cef3411ef93475254005ef0f7.png)
		2. 回退两层文件夹到 Editor。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/f747e3c1ef3411ef9ac1525400454e06.png)
		3. 清空 CachedExtensionVSIXs 缓存文件夹。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/2a40a2a1ef3511efab2f5254007c27c5.png) 清空缓存文件夹后再重新试试。

### 插件使用问题

#### 插件页面空白或使用过程中提示扩展宿主意外终止？

- 异常现象：登录后插件页面空白或使用过程中提示扩展宿主意外终止。

	- 页面空白 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/454555cb4b4511f092f25254007c27c5.png)
	- 扩展宿主意外终止 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/6474e7384b4511f085275254001c06ec.png)
- 解决方法：

	1. 插件升级到最新版本。
	2. 重命名历史记录文件为 `craft_history.json.bak`。
	3. 重新加载编辑器。 历史记录文件地址： Win 32：`C:\Users\用户名\AppData\Local\craft\craft_history.json`。 Mac：`/Users/用户名/Library/Caches/craft/craft_history.json`。 其它：`/home/用户名/.local/share/craft/craft_history.json`。

## Xcode 插件问题

### 代码补全失效？

- 异常现象：触发代码补全后无反应，或者无提示，代码补全不生效。
- 解决方法：

	1. 按下快捷键 `Command + 空格`，输入活动监视器并打开，在活动监视器中搜索找到 "**language\-server\-macos\-arm64**"，终止掉该进程。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/141b3e624dbb11f09bf25254005ef0f7.png)
	2. 重启电脑后重试。
	3. 如果通过以上方法还未解决，请将系统设置当中的两个页面截图，并反馈，如下图： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/5d81d13d4dbb11f0a6ac525400bf7822.png)

## Web 端问题

### 登录异常？

访问页面不存在。

- 异常现象：登录地址返回404。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100025099277/8d2e29f3d89311ef9e13525400454e06.png)
- 解决方法：可以更换使用新地址：<https://copilot.tencent.com/admin>。

### 邀请异常？

- 异常现象：邀请链接打开异常。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/d9768e8c138b11f0a63e5254005ef0f7.png)
- 解决方法：直接在手机微信中打开。

### 数据异常？

- 异常现象：企业管理后台页面查看的数据异常（包括度量数据异常、活跃数据异常、授权数据异常等）。
- 解决方法：数据同步需要15分钟时间，确认是否因未同步造成异常。

## 不同端收集报错信息

系统环境信息：Mac/Windows/Linux。其它信息根据不同端参考如下：

### VS Code

#### 1\. IDE 环境及版本信息

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/2fb55aef138c11f0a9cd5254007c27c5.png)

#### 2\. 插件版本信息

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/637cbe18138c11f0854e525400454e06.png)

#### 3\. 用户 ID 信息

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/998b1f0d138c11f0854e525400454e06.png)

#### 4\. 报错日志信息

本地客户端日志获取：

1. 在底部状态栏中单击插件 logo，然后单击**查看日志**。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/80a0b597822611f0ac3c525400e889b2.png)
2. 在弹出的窗口中展示的 log 日志文件便是当前工程当日的插件日志。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/9f322d68822711f0840d525400454e06.png)

### JetBrains\-IDE（以 IDEA 为例）

#### 1\. IDE 环境及版本信息

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/9418740ed3bd11efa4a3525400bf7822.png)

#### 2\. 插件版本信息

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/3639c091138e11f0a63e5254005ef0f7.png)

#### 3\. 用户 ID 信息

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/aacf124d138e11f09b3252540044a08e.png)

#### 4\. 本地客户端报错日志获取

1. 在 JetBrains 顶部菜单的 \*\*Help \*\*找到 \*\*Collect Logs and Diagnostic Data \*\*项，并单击开始自动采集 IDE 日志。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/fdbb42d2d3d111ef81865254005ef0f7.png)
2. 采集完成后出现敏感数据的警告确认弹窗，此时选择 \*\*Show in Explorer(Win) or Show in Finder(Mac) \*\*在 Explorer or Finder 中定位已采集的日志文件。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/284fe98bd3d211ef81865254005ef0f7.png)
3. 在 Explorer or Finder 中被选中的 \*\*idea\-logs\-xxxxxx.zip \*\*即为插件日志 ，提供 idea.log。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032954869/8e8f06b0f4b611efa8355254001c06ec.png)

### Android Studio

#### 1\. 用户 ID 信息

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/aa7c9dc5139611f0a9cd5254007c27c5.png)

#### 2\. 本地客户端报错日志

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/cf0a9601138f11f0a63e5254005ef0f7.png)

### Visual Studio

#### 1\. IDE 环境及版本信息

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/35e919e7139011f0a9cd5254007c27c5.png)

#### 2\. 插件版本信息

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/68bb659d139011f09b3252540044a08e.png)

#### 3\. 本地客户端日志

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/6217a180139111f08c275254001c06ec.png)

### 微信开发者平台

#### 1\. IDE 环境及版本信息

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/93ef5600139111f09b3252540044a08e.png)

#### 2\. 插件版本信息

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/b2b374dd139111f0aaa3525400e889b2.png)

#### 3\. 用户 ID 信息

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/a901fd8b139211f08c275254001c06ec.png)

#### 4\. 本地客户端日志信息

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/72d77c9c139311f09b3252540044a08e.png)

> **说明：**

> 如果以上方法还不能解决您的问题，请通过 [联系我们](./../联系我们) 的方式联系我们。