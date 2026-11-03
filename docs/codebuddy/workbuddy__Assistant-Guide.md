# 助理接入指南

助理支持通过微信、企业微信、QQ、飞书、钉钉等即时通讯平台，远程控制电脑上的 WorkBuddy。

推荐使用移动端 App

WorkBuddy 移动端（App）可以在手机上通过文字、语音、图片和文件下达任务，支持「云端工作」和「连接电脑」两种执行模式。登录与桌面端相同的账号即可使用，不需要创建机器人或配置应用凭证。

- [了解 WorkBuddy 移动端（App）并下载安装](./../workbuddyapp/Overview)
- [通过移动端 App 连接电脑，远程操控桌面端 WorkBuddy](./../workbuddyapp/features/Multidevice)
如果您需要通过即时通讯平台使用助理，请参考下方对应平台的接入指南。

## 微信助理接入指南

接入微信助理让您可以通过手机微信远程控制电脑上的 WorkBuddy。在微信中发送任务指令，WorkBuddy 在电脑上自动执行，并将结果同步回微信聊天窗口。所有项目、文件、凭证和工具均使用您电脑本地的环境，无需额外配置。

### 微信助理能做什么

绑定微信助理后，您可以在微信中完成以下操作：

- 启动新的任务，或继续助理板块中未完成的会话
- 发送后续指令、回答 WorkBuddy 的追问、指导进行中的工作
- 批准命令执行、文件修改等需要确认的操作
- 查看任务输出、差异对比
- 当 WorkBuddy 完成任务或需要您的关注时，在微信中收到通知

### 设置前的准备

在开始绑定之前，请确认满足以下条件：

| 要求 | 说明 |
| --- | --- |
| WorkBuddy 版本 | macOS / Windows 上安装 **WorkBuddy \>\= 4\.6\.4** |
| 微信版本 | 手机上已登录 **微信 \>\= 8\.0\.70** |
| 账号一致性 | WorkBuddy 和微信使用同一账号登录（或已关联） |
| 网络连接 | 电脑和手机均能正常访问互联网 |
| WorkBuddy 运行中 | WorkBuddy 必须保持运行状态 |

提示

微信助理接入无需填写 App ID、App Secret 等开发凭证，只需扫码即可完成绑定。

### 连接微信助理

#### 第一步：打开助理设置

1. 打开 WorkBuddy
2. 在左侧 **助理** 栏点击齿轮图标，进入「助理设置」

![助理栏的齿轮图标](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/1.m1V5GY4g.png)

3. 在集成列表中找到「微信助理集成」
4. 点击右侧的「配置」按钮

![微信助理集成的配置按钮](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/2.B3o7ZTse.png)

#### 第二步：生成绑定二维码

点击「配置」后，按钮会短暂显示为「绑定中...」，WorkBuddy 正在生成用于绑定的二维码。

#### 第三步：扫码完成绑定

二维码生成后会直接显示在卡片下方。打开手机微信，扫描该二维码即可完成绑定。

![微信助理绑定二维码](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/3.B4pImZpI.png)

注意

二维码有时效限制。如果二维码过期或扫码失败，请重新点击「配置」生成新的二维码。

#### 第四步：确认绑定状态

扫码完成后，卡片状态会变为「已绑定」。如果后续需要更换账号，可以点击「解绑」后重新绑定。

![微信助理已绑定状态](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/4.BsCR3lH2.png)

### 使用场景与连接方式

WorkBuddy 微信助理支持以下几种使用场景：

#### 日常办公电脑

连接您日常使用 WorkBuddy 的 Mac 或 Windows 电脑。当您离开工位时，可以通过微信远程访问相同的项目、文件和工作线程。

注意

如果电脑休眠、断网或关闭 WorkBuddy，远程访问将暂时中断。

**建议设置**：

- Mac 笔记本请保持打开并接通电源；如果合盖使用，建议外接显示器使电脑不休眠
- 可在 WorkBuddy 设置中开启**锁屏远程**，防止长时间任务被中断

#### 专属常开主机

如果您的项目需要长期运行的任务（如定时巡检、持续集成监控等），可以使用一台专用的 Mac 或 Windows 电脑，在上面安装项目依赖、凭证、插件和工具，保持 WorkBuddy 持续运行。即使您的主电脑离线，微信助理仍然可以访问这台常开主机。

### 跨设备接续工作

微信助理支持与 WorkBuddy 桌面端无缝衔接：

- 在微信中发起一个任务后，可以回到电脑上的 WorkBuddy 查看完整的执行过程和结果
- 当您回到电脑前时，WorkBuddy 会在助理中显示微信中发起的会话，无需手动查找
- 您可以在电脑上继续追问、细化任务，或在微信中随时查看进度

说明

当微信消息到达时，WorkBuddy 会自动切换到 **助理** 标签页并加载对应的会话，无需手动切换。

### 微信消息类型

通过微信与 WorkBuddy 交互支持以下方式：

- **文字消息**：发送自然语言任务指令
- **图片消息**：发送截图或文档照片，WorkBuddy 可识别图中内容
- **文件消息**：转发文件，WorkBuddy 可读取并分析
- **语音消息**：发送语音指令（需微信语音转文字功能）

### 什么来自本地电脑

当您通过微信向 WorkBuddy 发送任务时，处理过程发生在您的电脑上：

| 来源 | 说明 |
| --- | --- |
| 手机微信 | 仅发送指令、批准操作和后续消息 |
| 您的电脑 | 提供 WorkBuddy 执行任务所需的全部环境 |

具体来说，WorkBuddy 使用您电脑上的：

- **项目与文件**：所有仓库代码、本地文档均来自您的电脑
- **Shell 命令**：终端命令在您的电脑上执行，使用您本地的环境和依赖
- **凭证与权限**：已登录的网站、Git 仓库、云服务等均使用您电脑上的凭证
- **插件与工具**：已安装的插件、MCP 服务器、浏览器扩展、Computer Use 能力均可远程使用
- **安全策略**：沙箱设置、操作审批规则仍然适用于远程发起的会话

### 微信助理常见问题

#### 页面一直停留在「绑定中...」怎么办？

1. 确认电脑上的 WorkBuddy 正在运行，且网络连接正常
2. 关闭当前配置窗口后重新进入「微信助理集成」
3. 如果问题仍然存在，重启 WorkBuddy 后重新绑定

#### 扫码后没有显示「已绑定」怎么办？

1. 确认扫码使用的是您希望绑定的微信账号
2. 等待几秒钟让绑定状态同步
3. 如果二维码已经失效，请点击「重试」生成新的二维码后再次扫码

#### 微信里发消息没有响应怎么办？

1. 确认电脑上的 WorkBuddy 仍在运行，且**助理**服务未关闭
2. 返回「助理设置」检查微信助理集成状态是否仍为「已绑定」
3. 如有必要，可先解绑后重新扫码绑定

#### 微信助理和微信客服号有什么区别？

两者功能相同，都可以通过微信与 WorkBuddy 对话。微信助理是另一种绑定通道，绑定流程与微信客服号一致（扫码即可），您可以根据需要选择其中一种使用。

#### 多个微信账号可以绑定同一台电脑吗？

WorkBuddy 当前一对一绑定。如果您需要切换微信账号，请先在「助理设置」中解绑当前账号，再使用新账号扫码绑定。

## 微信客服号接入指南

微信客服号集成让您可以通过手机微信远程控制电脑上的 WorkBuddy。在微信中发送任务指令，WorkBuddy 在电脑上自动执行，并将结果同步回微信聊天窗口。

### 微信客服号能做什么

绑定微信客服号后，您可以在微信中完成以下操作：

- 启动新的任务，或继续助理板块中未完成的会话
- 发送后续指令、回答 WorkBuddy 的追问、指导进行中的工作
- 批准命令执行、文件修改等需要确认的操作
- 查看任务输出、差异对比
- 当 WorkBuddy 完成任务或需要您的关注时，在微信中收到通知

### 设置前的准备

在开始绑定之前，请确认满足以下条件：

| 要求 | 说明 |
| --- | --- |
| WorkBuddy 版本 | macOS / Windows 上安装并登录 **WorkBuddy \>\= 4\.6\.4** |
| 微信版本 | 手机上已登录一个可正常使用的**微信 \>\= 8\.0\.70** |
| 网络连接 | 电脑和手机均能正常访问互联网 |
| WorkBuddy 运行中 | 电脑保持开机并运行 WorkBuddy |

提示

微信客服号接入无需额外创建开放平台应用，也不需要填写 App ID、App Secret 等开发凭证。整个绑定流程都可以直接在 WorkBuddy 中完成。

### 连接微信客服号

#### 第一步：打开助理设置

1. 打开 WorkBuddy
2. 点击右上角头像，进入「助理设置」
3. 在集成列表中找到「微信客服号集成」
4. 点击右侧的「配置」按钮

![微信客服号集成的配置按钮](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/1.QOtyZZkt.png)

#### 第二步：等待绑定初始化

点击配置后，WorkBuddy 按钮会短暂显示为「绑定中...」，WorkBuddy 正在生成用于绑定的二维码。

#### 第三步：扫码完成绑定

初始化完成后，页面会展示一个二维码。使用手机微信扫描该二维码，即可将当前微信账号与 WorkBuddy 绑定。

![微信客服号绑定二维码](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/2.C4nBZYa3.png)

注意

二维码有时效限制。如果二维码过期或扫码失败，请重新点击「配置」生成新的二维码后再试。

#### 第四步：确认绑定状态

扫码完成后，WorkBuddy 会展示当前已绑定的微信头像和昵称，右侧状态会变为「已绑定」。如果后续需要更换账号，也可以在这里点击「解绑」后重新绑定。

![微信客服号已绑定状态](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/3.BXkDaLnV.png)

### 使用示例

绑定完成后，您就可以直接在微信里和 WorkBuddy 对话，例如：

- 帮我总结今天桌面上最新的会议记录
- 帮我检查这个项目最近改过的接口有没有明显问题
- 帮我生成一个登录页原型

WorkBuddy 会在电脑上自动执行任务，并把执行过程和最终结果同步回微信聊天窗口。

![在微信中与 WorkBuddy 对话](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/4.DxZSAsJc.png)

### 跨设备接续工作

微信客服号支持与 WorkBuddy 桌面端无缝衔接：

- 在微信中发起一个任务后，可以回到电脑上的 WorkBuddy 查看完整的执行过程和结果
- 在**助理**页面可查看远程任务的完整执行记录，包括思考过程、操作步骤、生成文件及最终结果
- 您可以在电脑上继续追问、细化任务，或在微信中随时查看进度

### 什么来自本地电脑

当您通过微信向 WorkBuddy 发送任务时，处理过程发生在您的电脑上：

| 来源 | 说明 |
| --- | --- |
| 手机微信 | 仅发送指令、批准操作和后续消息 |
| 您的电脑 | 提供 WorkBuddy 执行任务所需的全部环境 |

电脑上的 WorkBuddy 使用您本地的项目文件、Shell 环境、凭证权限、插件和工具来执行任务。也就是说，您电脑上能做的事，通过微信也能远程完成。

### 远程任务与普通任务的区别

| 对比项 | 普通任务 | 助理（远程任务） |
| --- | --- | --- |
| 工作目录 | 自由指定 | 固定使用**助理**专属文件夹 |
| 新建对话 | 支持多个并行任务 | 仅一个会话，所有远程指令集中处理 |
| 上下文管理 | 可清空历史重新开始 | 保留完整对话历史，不可清空 |

建议

本地操作优先使用主界面的普通任务；需要远程触发或统一查看记录时，再使用助理。

### 微信客服号常见问题

#### 页面一直停留在「绑定中...」怎么办？

1. 确认电脑上的 WorkBuddy 正在运行，且网络连接正常
2. 关闭当前配置窗口后重新进入「微信客服号集成」
3. 如果问题仍然存在，重启 WorkBuddy 后重新绑定

#### 扫码后没有显示「已绑定」怎么办？

1. 确认扫码使用的是您希望绑定的微信账号
2. 等待几秒钟让绑定状态同步
3. 如果二维码已经失效，请重新生成二维码后再次扫码

#### 微信里发消息没有响应怎么办？

1. 确认电脑上的 WorkBuddy 仍在运行，且**助理**服务未关闭
2. 返回「助理设置」检查微信客服号集成状态是否仍为「已绑定」
3. 如有必要，可先解绑后重新扫码绑定

#### 微信客服号和微信助理有什么区别？

两者功能相同，都可以通过微信与 WorkBuddy 对话。微信客服号是 WorkBuddy 提供的绑定通道之一，绑定流程为扫码即可完成；微信助理是另一种绑定通道，与微信客服号功能一致。您可以根据需要选择其中一种使用。

#### 多个微信账号可以绑定同一台电脑吗？

WorkBuddy 当前支持一对一绑定。如果您需要切换微信账号，请先在「助理设置」中解绑当前账号，再使用新账号扫码绑定。

## 企微助理接入指南

企微助理集成让您可以通过企业微信远程控制电脑上的 WorkBuddy。在企业微信中向智能机器人发送任务指令，WorkBuddy 在电脑上自动执行，并将结果同步回企业微信聊天窗口。

### 企微助理能做什么

绑定企微助理后，您可以在企业微信中完成以下操作：

- 在**群聊中 @机器人**下发团队协作任务，WorkBuddy 自动执行并返回结果
- **跟进任务进度**：直接向机器人发送任务指令，随时跟进执行进度
- 创建**专属任务群**，长期绑定 WorkBuddy 处理团队日常工作
- **发布通知**：任务完成后自动通知群聊相关人员
- **任务提醒**：将待办、验收、协作事项同步到企微群
- **流程打通**：连接 WorkBuddy 任务处理与团队现有工作流
- **确认操作**：批准命令执行、文件修改等需要确认的操作

### 设置前的准备

在开始配置之前，请确认满足以下条件：

| 要求 | 说明 |
| --- | --- |
| WorkBuddy | 已在电脑上安装 **WorkBuddy \>\= 4\.6\.4** |
| 企业微信账号 | 拥有一个可创建智能机器人的企业微信账号 |
| 网络连接 | 电脑和手机均能正常访问互联网 |
| WorkBuddy 运行中 | 电脑保持开机并运行 WorkBuddy |

提示

如果您还没有企业微信账号，可以前往 [企业微信官网](https://work.weixin.qq.com/wework_admin/register_wx) 免费注册一个企业。

### 连接企微助理

企业微信集成需要先在平台完成机器人创建和配置。请根据您的账号角色选择对应的操作指南。

#### 管理员操作

##### 第一步：进入管理后台创建机器人

打开浏览器，访问 [企业微信管理后台](https://work.weixin.qq.com/wework_admin/frame)，使用管理员账号登录后，依次点击「安全与管理」→「管理工具」→「智能机器人」→「创建机器人」。

![企业微信管理后台：智能机器人入口](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/wecom-guide-1.BEQ8dvDd.png)

![企业微信管理后台：创建机器人](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/wecom-guide-2.DlrX2Hk3.png)

如果先进入 AI 自动生成页面，请点击左下角的「手动创建」：

![AI 自动生成页面的手动创建入口](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/2.D9E3GsWy.png)

在创建页面直接选择「API 模式创建」：

![选择 API 模式创建](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/wecom-guide-3.oOi_9rH6.png)

##### 第二步：填写基本信息

进入 API 模式页面后，请先完成以下公共配置：

| 配置项 | 说明 |
| --- | --- |
| **机器人名称** | 建议填写容易识别的名字，如「WorkBuddy 助手」 |
| **可见范围** | 选择哪些员工、部门或标签可以使用这个机器人 |

点击「可见范围」后的「添加」，选择需要使用机器人的成员、部门或标签。

![设置机器人可见范围](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/visible-range.DG0MoWc3.png)

完成以上配置后，请先点击页面底部的「保存」，再在右侧「API 配置」区域选择「使用长连接」。

##### 第三步：获取凭证并完成绑定

进入[使用长连接方式接入](#使用长连接方式接入)完成后续步骤。

#### 普通成员操作

##### 第一步：在企业微信客户端创建机器人

打开企业微信客户端，进入「工作台」→「智能机器人应用」→「创建机器人」。

![企业微信客户端：创建机器人入口](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/1.DdHM-fev.png)

如果先进入 AI 自动生成页面，请点击左下角的「手动创建」，再选择「API 模式创建」：

![AI 自动生成页面的手动创建入口](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/2.D9E3GsWy.png)

![选择 API 模式创建](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/3.Ck217sUl.png)

##### 第二步：填写基本信息

进入 API 模式页面后，请先完成以下公共配置：

| 配置项 | 说明 |
| --- | --- |
| **机器人名称** | 建议填写容易识别的名字，如「WorkBuddy 助手」 |
| **可使用成员围** | 选择哪些员工、部门或标签可以使用这个机器人 |

点击「可使用成员」后的「修改」，选择需要使用机器人的成员、部门或标签。

![设置机器人可使用成员](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/4.BuvAHCYe.png)

完成以上配置后，再在下方「API 配置」区域选择「使用长连接」。

##### 第三步：获取凭证并完成绑定

进入[使用长连接方式接入](#使用长连接方式接入)完成后续步骤。

#### 使用长连接方式接入

两种角色在此步骤的操作一致。推荐优先使用长连接模式，配置步骤更少，也不需要回填 Webhook URL。

**在企业微信中获取 Bot ID 和 Secret**：

1. 在「API 配置」区域选择「使用长连接」
2. 复制 `Bot ID`
3. 点击 `点击获取` 获取 `Secret`，并妥善保存

![获取长连接 Bot ID 和 Secret](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/longlink-bot-credentials.CEJjnqsO.png)

提示

长连接模式不需要再填写 URL、Token 或 `Encoding-AESKey`。

#### 在 WorkBuddy 中完成绑定

1. 打开 WorkBuddy，点击左下角头像菜单中的「设置\-助理设置」
2. 在「集成（BETA）」区域找到「企微助理集成」，点击「配置」
3. 在弹窗中选择「WebSocket 长连接」后，有两种绑定方式可选：
	- 手动填写 `Bot ID` 和 `Secret`
	- 点击快捷绑定接入，使用企微扫码完成绑定
	- 填入刚才复制的 `Bot ID` 和 `Secret`后点击「注册」完成绑定

![企微助理集成的配置入口](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/5.qWDtiT-D.png)

![WebSocket 长连接注册弹窗](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/6.BZ55K463.png)

##### 私有化部署企业微信：填写自定义 WebSocket 地址

若您的企业采用**私有化部署的企业微信**，还需额外填写专属的 WebSocket 地址才能完成注册：

1. 在企业微信管理后台获取私有化部署的 WebSocket 地址，格式形如 `ws://<网关>:<端口>/im_openws?bizid=1`
2. 在「WebSocket 长连接」配置中，除 `Bot ID` 和 `Secret` 外，将该地址填入**自定义 WebSocket 地址**输入框
3. 点击「注册」完成绑定

填写要求

- 地址协议必须为 `ws://` 或 `wss://`，使用 `http://` 等其他协议会被拦截并给出提示
- 留空时自动回落到公有云默认地址，不影响常规（非私有化）部署的绑定
- 该输入框**仅在 WebSocket 长连接模式**下出现，URL 回调模式不涉及
配置保存后重启 WorkBuddy 会自动重连；若地址不可达，界面会显示明确的连接错误状态，便于排查网络或地址配置问题。

#### 关于 API 模式

企业微信 API 模式支持两种接入方式：

- **长连接模式（推荐）**：在 WorkBuddy 中填写 `Bot ID` 和 `Secret` 即可完成绑定，配置更简单，无需回填 Webhook URL。
- **URL 回调模式**：适用于需要 Webhook 回调的场景。需在 WorkBuddy 中填写 `Token` 和 `Encoding-AESKey`，生成 Webhook URL 后再回填到企业微信。

URL 回调模式配置指引见本节末尾「使用 URL 回调接入（备选方案）」。

### 企微助理开始使用

配置完成后，您就可以在企业微信中直接与机器人对话了。

#### 找到机器人

在企业微信通讯录的「企业创建的」分组下找到刚刚创建的机器人，点击「发消息」即可开始下发任务。

![在企业微信通讯录中找到机器人](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/wecom-guide-10.DGuEDc4B.png)

#### 联通后对话效果

发送一条简单消息（例如"你好"）进行联通测试。如果配置正确，WorkBuddy 会接收到消息并在企业微信中返回回复。

恭喜

如果机器人能够正常回复，说明您已成功完成 WorkBuddy 与企业微信的对接！

### 企微助理跨设备接续工作

企微助理支持与 WorkBuddy 桌面端无缝衔接：

- 在企业微信中发起一个任务后，可以回到电脑上的 WorkBuddy 查看完整的执行过程和结果
- 在**助理**页面可查看远程任务的完整执行记录，包括思考过程、操作步骤、生成文件及最终结果
- 您可以在电脑上继续追问、细化任务，或在企业微信中随时查看进度

### 企微助理：什么来自本地电脑

当您通过企业微信向 WorkBuddy 发送任务时，处理过程发生在您的电脑上：

| 来源 | 说明 |
| --- | --- |
| 企业微信 | 仅发送指令、批准操作和后续消息 |
| 您的电脑 | 提供 WorkBuddy 执行任务所需的全部环境 |

电脑上的 WorkBuddy 使用您本地的项目文件、Shell 环境、凭证权限、插件和工具来执行任务。也就是说，您电脑上能做的事，通过企业微信也能远程完成。

### 企微助理：远程任务与普通任务的区别

| 对比项 | 普通任务 | 助理（远程任务） |
| --- | --- | --- |
| 工作目录 | 自由指定 | 固定使用**助理**专属文件夹 |
| 新建对话 | 支持多个并行任务 | 仅一个会话，所有远程指令集中处理 |
| 上下文管理 | 可清空历史重新开始 | 保留完整对话历史，不可清空 |

建议

本地操作优先使用主界面的普通任务；需要远程触发或统一查看记录时，再使用助理。

### 使用 URL 回调接入（备选方案）

如果您已经在使用 Webhook 配置，或因网络、部署限制需要通过 URL 回调接入，可按以下步骤操作。

#### 在企业微信中生成回调凭据

1. 在「API 配置」区域选择「使用 URL 回调」
2. 点击 `Token` 和 `Encoding-AESKey` 输入框右侧的「随机获取」
3. 保存这两个参数，后续需要在 WorkBuddy 中使用

![随机获取 Token 和 Encoding-AESKey](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/wecom-guide-4.lB4uC-vS.png)

重要

请务必保存好 `Token` 和 `Encoding-AESKey`，否则后续无法完成注册。

#### 在 WorkBuddy 中生成 Webhook URL

1. 打开 WorkBuddy，进入「助理设置」→「企微 AIBot 集成」→「配置」
2. 在注册弹窗中切换到「使用 URL 回调」
3. 填入刚才获取的 `Token` 和 `Encoding-AESKey`，点击「注册」
4. 注册成功后，复制生成的 Webhook URL

![切换到 URL 回调并填入凭据](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/7.BaLtfLWf.png)

![复制生成的 Webhook URL](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/8.BRAyJKVS.png)

#### 回填 URL 并保存

回到企业微信的机器人创建页面：

1. 将刚才复制的 Webhook 地址粘贴到 `URL` 输入框
2. 点击「保存」完成配置

![回填 Webhook URL 并保存](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/wecom-guide-9.Jzv4lt7W.png)

### 企微助理常见问题

#### 机器人没有响应怎么办？

请按以下步骤排查：

1. **检查 WorkBuddy 状态**：确保电脑上的 WorkBuddy 正在运行，且**助理**服务已开启
2. **核对接入方式**：确认企业微信与 WorkBuddy 中选择的是同一种接入方式
3. **检查凭据**：长连接模式请核对 `Bot ID` 和 `Secret`；URL 回调模式请核对 `Token` 和 `Encoding-AESKey`
4. **检查网络连接**：确保电脑能够正常访问网络

#### URL 验证失败怎么办？

1. 确保 WorkBuddy 处于运行状态
2. 检查**助理**服务是否已正常启动
3. 重新复制 Webhook URL，确保没有遗漏或多余字符
4. 确认 `Token` 和 `Encoding-AESKey` 与 WorkBuddy 中配置的完全一致

#### 长连接注册失败怎么办？

1. 确认企业微信侧已选择「使用长连接」
2. 重新复制 `Bot ID` 和 `Secret`，避免带入多余空格
3. 如 `Secret` 已失效，可在企业微信后台重新获取后再次注册
4. **私有化部署场景**：核对自定义 WebSocket 地址的协议是否为 `ws://` 或 `wss://`、网关与端口是否正确，并确认该地址在当前电脑上可正常访问

## QQ 机器人接入指南

本指南将帮助您将 WorkBuddy 接入 QQ，让您可以通过 QQ 随时随地远程操控电脑上的 WorkBuddy 完成任务。

### 接入 QQ 能做什么

将 WorkBuddy 接入 QQ 后，你可以随时随地通过 QQ 与电脑上的 WorkBuddy 助理对话、派发任务：

| 能力 | 说明 |
| --- | --- |
| 远程操控完成任务 | 不在电脑前也能给 WorkBuddy 派活，让它读写文件、整理资料、生成文档 |
| 发送文件与图片 | 可直接在 QQ 中向机器人发送文件和图片，作为任务的输入材料 |
| 高危操作确认 | 远程执行删除文件等高风险操作前，WorkBuddy 会先在 QQ 中向你确认，经你同意后才会执行，远程使用也安全可控 |
| 私聊与群聊 | 支持与机器人一对一私聊，也支持拉入 QQ 群后 **@机器人** 使用，与团队成员共享任务 |

### 接入前准备

在开始之前，请确保您已满足以下条件：

- 已在电脑上安装 WorkBuddy，并开启了**助理**远程控制功能。
- 拥有一个已完成实名认证的 QQ 账号。

提示

QQ 开放平台要求账号完成实名认证。如未认证，请先在 QQ 中完成实名认证后再进行后续操作。

### 接入 QQ

#### 第一步：注册并登录 QQ 开放平台

打开浏览器，访问 [QQ 开放平台](https://q.qq.com/qqbot/openclaw/login.html)，使用QQ扫码登录。

![登录QQ开放平台](https://download.codebuddy.cn/web/docs/71c8722a08165ddedf566c5f1711bb0ec8ea991b/docs/static/qq-guide-1.BSmYTk4-.png)

#### 第二步：创建机器人

点击创建机器人：

![创建机器人](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/qq-guide-2.DdeZxWeY.png)

点击后会立刻成功，此时机器人会给你的QQ发一条成功消息，头像昵称可按喜好自定义编辑。

#### 第三步：获取并配置凭证

复制并保存机器人的 AppID 和 AppSecret 。

![复制AppID和AppSecret](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/qq-guide-3.B1fiLS6i.png)

重要提示

出于安全考虑，AppSecret不支持明文保存，二次查看将会强制重置，请自行妥善保存。

#### 第四步：在 WorkBuddy 中接入 QQ

1. 打开 WorkBuddy，点击助理的**设置**⚙️图标后进入**助理设置**页面。
2. 点击QQ机器人卡片右边的**连接**按钮。

![QQ机器人集成配置](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/qq-guide-5.CppvIKbu.png)

3. 选择一种方式连接已创建的 QQ 机器人
- **QQ 扫码**：扫码连接已创建的机器人。

![QQ 扫码连接](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/qq-guide-6.BqAWhxq9.png)

- **更多连接方式**：选择 WebSocket 长连接或使用 URL 回调，填入上方复制保存的 AppID 和 AppSecret ，点击**连接**按钮。

![更多连接方式](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/qq-guide-7.CsjQmu3T.png)

4. 连接成功后，在**助理**页面上方会显示 QQ 图标。

![助理QQ图标](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/qq-guide-9.2UbTr9Lp.png)

### QQ 机器人开始使用

接入成功后，即可通过 QQ 开始使用 WorkBuddy。

提示

QQ 机器人依赖电脑端的 WorkBuddy 运行。请保持电脑开机且 WorkBuddy 处于运行状态，否则机器人将无法响应消息。

#### 发起任务

- **私聊**：在 QQ 中找到已创建的机器人，直接发送消息。
- **群聊**：将机器人加入 QQ 群，在群聊中 **@机器人** 后发送需求。

使用自然语言描述需要完成的任务，例如：

- 「帮我把桌面上的发票按月份归类」
- 「统计一下本周的会议纪要里有哪些待办事项」

#### 发送文件和图片

直接在对话中发送文件或图片，WorkBuddy 会将其作为任务材料处理，也可以配合文字说明任务需求。

#### 确认高风险操作

当任务涉及删除文件、执行脚本等高风险操作时，WorkBuddy 会在 QQ 中发送确认消息。确认后才会继续执行；拒绝后则不会执行该操作。

### 取消 QQ 连接

如果不再需要 QQ 机器人服务，可进入**设置** \> **助理设置**页面，在 **QQ 机器人**卡片右侧点击**取消连接**。取消连接后将无法继续使用 QQ 集成服务，但不会影响已有会话记录。

### QQ 机器人声明

本节说明，构成[服务协议](https://rule.tencent.com/rule/202603180001)和[隐私保护](https://privacy.qq.com/document/preview/771d9a58551449e9a7e7445ebfe04966)指引的组成部分，具有同等法律效力。 如有不一致之处，以前述协议原文为准。

## 飞书接入指南

本指南将帮助您在飞书中配置 WorkBuddy 机器人，让您可以通过飞书随时随地远程操控电脑上的 WorkBuddy 完成编程任务。

### 飞书前提条件

在开始之前，请确保您已满足以下条件：

- 已在电脑上安装 WorkBuddy，并开启了 **助理** 远程控制功能
- 拥有一个飞书企业账号（需要有创建应用的权限）

### 创建飞书应用

#### 登录开发者后台

打开浏览器，访问 [飞书开放平台](https://open.feishu.cn/app)，使用企业账号登录后，点击「创建企业自建应用」。

![登录飞书开放平台](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/feishu-guide-1.DVtlT-_d.png)

#### 填写应用信息

在弹出的创建窗口中，填写以下信息：

| 配置项 | 说明 |
| --- | --- |
| **应用名称** | 给应用起一个名字，如「WorkBuddy 助手」 |
| **应用描述** | 简单描述应用的功能 |
| **应用图标** | 上传一个应用图标 |

![填写应用信息](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/feishu-guide-2.Bq35BkzN.png)

填写完成后，点击「创建」按钮。

#### 进入应用详情

应用创建成功后，会自动跳转到应用详情页面。

![应用详情页](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/feishu-guide-3.CquowSwv.png)

### 添加机器人能力

在应用详情页的「添加应用能力」区域，找到「机器人」卡片，点击「添加」按钮。

![添加机器人能力](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/feishu-guide-4.Bvf_VP1c.png)

### 配置应用权限

为了让机器人能够正常收发消息，需要为应用添加必要的权限。

#### 进入权限管理

在应用详情页左侧菜单中，点击「权限管理」，然后选择「批量导入 / 导出权限」。

![复制权限列表](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/feishu-guide-5.BMDln-1L.png)

#### 批量导入权限

在弹出的窗口中：

1. 清空输入框中的所有内容
2. 将下方的权限列表完整复制并粘贴进去
3. 点击「确定新增权限」

**需要导入的权限列表：**

json
```
{
  "scopes": {
    "tenant": [
      "contact:contact.base:readonly",
      "docx:document:readonly",
      "im:chat:read",
      "im:chat:update",
      "im:message.group_at_msg:readonly",
      "im:message.p2p_msg:readonly",
      "im:message.pins:read",
      "im:message.pins:write_only",
      "im:message.reactions:read",
      "im:message.reactions:write_only",
      "im:message:readonly",
      "im:message:recall",
      "im:message:send_as_bot",
      "im:message:send_multi_users",
      "im:message:send_sys_msg",
      "im:message:update",
      "im:resource",
      "application:application:self_manage",
      "cardkit:card:write",
      "cardkit:card:read"
    ],
    "user": [
      "contact:user.employee_id:readonly",
      "offline_access",
      "base:app:copy",
      "base:field:create",
      "base:field:delete",
      "base:field:read",
      "base:field:update",
      "base:record:create",
      "base:record:delete",
      "base:record:retrieve",
      "base:record:update",
      "base:table:create",
      "base:table:delete",
      "base:table:read",
      "base:table:update",
      "base:view:read",
      "base:view:write_only",
      "base:app:create",
      "base:app:update",
      "base:app:read",
      "board:whiteboard:node:create",
      "board:whiteboard:node:read",
      "calendar:calendar:read",
      "calendar:calendar.event:create",
      "calendar:calendar.event:delete",
      "calendar:calendar.event:read",
      "calendar:calendar.event:reply",
      "calendar:calendar.event:update",
      "calendar:calendar.free_busy:read",
      "contact:contact.base:readonly",
      "contact:user.base:readonly",
      "contact:user:search",
      "docs:document.comment:create",
      "docs:document.comment:read",
      "docs:document.comment:update",
      "docs:document.media:download",
      "docs:document:copy",
      "docx:document:create",
      "docx:document:readonly",
      "docx:document:write_only",
      "drive:drive.metadata:readonly",
      "drive:file:download",
      "drive:file:upload",
      "im:chat.members:read",
      "im:chat:read",
      "im:message",
      "im:message.group_msg:get_as_user",
      "im:message.p2p_msg:get_as_user",
      "im:message:readonly",
      "search:docs:read",
      "search:message",
      "space:document:delete",
      "space:document:move",
      "space:document:retrieve",
      "task:comment:read",
      "task:comment:write",
      "task:task:read",
      "task:task:write",
      "task:task:writeonly",
      "task:tasklist:read",
      "task:tasklist:write",
      "wiki:node:copy",
      "wiki:node:create",
      "wiki:node:move",
      "wiki:node:read",
      "wiki:node:retrieve",
      "wiki:space:read",
      "wiki:space:retrieve",
      "wiki:space:write_only"
    ]
  }
}
```
![粘贴权限列表](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/feishu-guide-6.CKT55pRC.png)

等待几秒钟，页面会显示权限已成功添加。

![权限添加成功](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/feishu-guide-7.DvbUEU9F.png)

### 获取应用凭证

#### 查看凭证信息

在应用详情页左侧菜单中，点击「凭证与基础信息」。

在页面中，您会看到两个重要的凭证信息：

- **App ID**：应用的唯一标识
- **App Secret**：应用的密钥（点击查看）

重要

请务必妥善保管 App Secret，不要泄露给他人！

![凭证与基础信息](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/feishu-guide-8.CpdvKWGY.png)

#### 获取 Encrypt Key 和 Verification Token

在应用详情页左侧菜单中，点击「事件与回调」，在右侧页面中选择加密策略。

您可以点击刷新按钮自动生成，或点击编辑按钮自定义您的 Encrypt Key 和 Verification Token。

![Encrypt Key 和 Verification Token](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/feishu-guide-8-1.DJzG3LOk.png)

重要

请务必妥善保管 Encrypt Key 和 Verification Token，不要泄露给他人！

### 在 WorkBuddy 中配置飞书

现在，我们需要将凭证配置到 WorkBuddy 中，让它能够与飞书通信。

#### 填写凭证

在 WorkBuddy 中，点击助理的**设置⚙️**图标后进入**助理设置**，找到**飞书集成**开始配置。

![飞书集成入口](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/feishu-guide-9.CN779x5z.png)

将刚才获取的 App ID、App Secret 以及 Encrypt Key 填入对应的输入框:

- **WebSocket 长连接**模式 适用于个人/家庭/办公室用户（没有公网 IP）。配置更简单，不需要公网地址，开箱即用。

![WebSocket长连接模式](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/feishu-guide-10.Crk-ilq8.png)

- **使用 URL 回调**模式 适用于有服务器、有公网 IP 的用户，需要额外在飞书开放平台填写生成的 Webhook 地址。

![URL回调模式](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/feishu-guide-11.DosshPS5.png)

#### 注册

- WebSocket 长连接：点击「注册」按钮完成配置，配置成功显示**已连接**：

![WebSocket已连接](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/feishu-guide-12.R_60TxIN.png)

- 使用 URL 回调：点击「注册」按钮系统会生成一个 Webhook 地址，点击复制保存：

![URL回调已注册](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/feishu-guide-13.Doll6xpa.png)

### 配置飞书事件回调

接下来，我们需要告诉飞书将消息发送到哪里。

#### 配置事件订阅

返回飞书开放平台，进入应用详情页；在左侧菜单中，点击「事件与回调」。

- WebSocket 长连接：在「订阅方式」中选择「使用长连接接收事件」，点击「验证」：

![使用长连接接收事件](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/feishu-guide-14.B_poTA-h.png)

配置成功显示「连接成功」：

![连接成功](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/feishu-guide-15.FMhd1iEo.png)

- 使用 URL 回调：在「订阅方式」中选择「将事件发送至开发者服务器」，将刚才复制的 Webhook 地址粘贴到输入框中并点击「保存」：

![将事件发送至开发者服务器](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/feishu-guide-16.BeXmFzec.png)

#### 添加消息接收事件

在「事件配置」区域，点击「添加事件」，搜索并添加「接收消息」事件。

![添加接收消息事件](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/feishu-guide-17.PEN-b6c0.png)

#### 配置卡片回调

1. 切换到「回调配置」页签
2. 搜索「卡片回传交互」
3. 点击「确认添加」

![卡片回传交互配置](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/feishu-guide-18.D7Us2LUf.png)

![确认添加卡片回调](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/feishu-guide-19.CBUtnaq6.png)

### 发布应用

应用必须发布后才能在飞书中使用。

#### 创建版本

点击页面上方的「创建版本」按钮。

![创建版本](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/feishu-create-release.DkAkt14R.png)

在弹出的窗口中填写：

| 配置项 | 示例 |
| --- | --- |
| **版本号** | 1\.0\.0 |
| **版本描述** | 首次发布，集成 WorkBuddy |

点击「确定」创建版本。

![发布版本](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/feishu-release.C_dxs14W.png)

#### 发布版本

创建成功后，点击版本右侧的「发布」按钮。

提示

如果您是企业管理员，应用通常会自动审批通过。如果需要审批，请联系您的企业管理员。

### 飞书开始使用

#### 找到机器人

在飞书的搜索框中，输入刚才创建的机器人名称进行搜索。

#### 开始对话

点击机器人进入对话窗口，或者点击「打开应用」开始使用。

![打开应用](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/feishu-guide-20.CBJCZq9g.png)

#### 发送任务

直接发送您的需求，比如「帮我写一个待办事项应用」。WorkBuddy 会在电脑上自动执行任务，并将结果返回给您。

![发送任务](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/feishu-guide-21.DB5sVp5U.png)

恭喜

您已成功将 WorkBuddy 接入飞书！现在可以通过飞书随时随地远程控制 WorkBuddy 完成各种编程任务了。

### 飞书常见问题

#### 机器人没有响应怎么办？

请按以下步骤排查：

1. **检查应用状态**：确认应用已成功发布
2. **检查 WorkBuddy**：确保电脑上的 WorkBuddy 正在运行，且 **助理** 服务已开启
3. **核对 Webhook**：确认 Webhook 地址配置正确
4. **检查权限**：确保所有权限都已正确导入

#### 收不到消息怎么办？

1. 确认已添加「接收消息」事件
2. 确认已配置「卡片回传交互」回调
3. 检查事件订阅中的 Webhook 地址是否正确

## 钉钉机器人接入指南

本指南将帮助您在钉钉中配置 WorkBuddy 机器人，让您可以通过钉钉随时随地远程操控电脑上的 WorkBuddy 完成编程任务。

### 钉钉前提条件

在开始之前，请确保您已满足以下条件：

- 已在电脑上安装 WorkBuddy，并开启了 **助理** 远程控制功能
- 拥有一个具有**企业管理员权限**的钉钉账号

提示

如果您还没有钉钉账号，请前往 [钉钉官网](https://www.dingtalk.com/download) 下载客户端并创建团队。

### 创建钉钉应用

#### 登录开发者后台

打开浏览器，访问 [钉钉开发者后台](https://open.dingtalk.com/)，使用管理员账号登录。

![登录开发者后台](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/login-developer-console.CLo2owy8.png)

首次使用

如果系统提示「该账号还未加入组织」，您可以创建一个个人企业，按需填写信息即可。

![创建个人企业](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/create-personal-org.CCdsgAJ_.png)

#### 创建应用

1. 在开发者后台首页，点击「应用开发」，并点击「创建应用」

![创建应用](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/create-app.BYp0m06K.png)

2. 在弹出的创建窗口中，填写以下信息：

| 配置项 | 填写内容（后续都可以随意修改） | 说明 |
| --- | --- | --- |
| 应用名称 | （内容随便写） | 自定义名称 |
| 应用描述 | （内容随便写） | 简单描述用途 |
| 应用类型 | 可以暂时不传 |  |

![填写应用信息](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/fill-app-info.BYBmvoBC.png)

3. 填写完成后，点击「保存」

#### 添加机器人能力

应用创建成功后，会自动跳转到「添加应用能力」页面：

1. 找到「机器人」选项，点击「添加机器人」

![添加机器人能力](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/add-robot-capability.CZkfvmyl.png)

2. 填写机器人的基本信息：
	- **机器人名称**：给机器人起一个名字
	- **机器人描述**：简单描述功能
	- **预览图**：上传一张机器人头像

![配置机器人信息](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/config-robot-info.DY4EBXm0.png)

3. 点击「确认发布」

![确认发布机器人](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/confirm-publish-robot.gisNfn0e.png)

### 配置钉钉应用权限

为了让机器人能够正常收发消息，需要开通以下权限：

1. 在应用详情页左侧菜单中，点击「权限管理」
2. 在搜索框中分别搜索以下权限，并点击「立即开通」：
	- `Card.Streaming.Write`
	- `Card.Instance.Write`
	- `qyapi_robot_sendmsg`

![添加权限](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/add-permissions.DF98JOdW.png)

### 获取钉钉应用凭证

#### 查看凭证信息

1. 在应用详情页左侧菜单中，点击「凭证与基础信息」
2. 在页面中找到以下两个重要信息：
	- **Client ID**（也叫 AppKey）
	- **Client Secret**（也叫 AppSecret）

重要

这两个凭证非常重要，请务必妥善保存，不要泄露给他人！

![获取凭证](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/get-credentials.GWm559Bt.png)

#### 获取 AES Key 和 Token

在应用详情页左侧菜单中，点击「开发配置 \- 事件订阅」，在「推送方式」中选择「HTTP推送」。

您可以点击刷新按钮自动生成您的 AES Key 和 Token。

![AES Key 和 Token](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/dingtalk-aes-token.C5mRmrgS.png)

重要

请务必妥善保管 AES Key 和 Token，不要泄露给他人！

### 在 WorkBuddy 中配置钉钉

#### 填写钉钉凭证

打开 WorkBuddy，点击助理的**设置⚙️**图标后进入**助理设置**，选择**钉钉集成**：

![钉钉集成入口](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/dingtalk-1.HLe1RdDx.png)

将刚才获取的 Client ID 和 Client Secret 填入对应输入框：

- **WebSocket 长连接**模式 适用于个人/家庭/办公室用户（没有公网 IP）。配置更简单，不需要公网地址，开箱即用。

![WebSocket长连接模式](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/dingtalk-2.BlZP-Yfa.png)

- **使用 URL 回调**模式 适用于有服务器、有公网 IP 的用户，需要额外在钉钉开发者后台填写生成的 Webhook 地址。

![URL回调模式](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/dingtalk-3.BWbUQV9Z.png)

#### 注册钉钉机器人

- WebSocket 长连接：点击「注册」配置成功后显示「已连接」：

![WebSocket已连接](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/dingtalk-4.B5dZu0o2.png)

- 使用 URL 回调：点击注册后显示「已注册」，系统会生成一个 Webhook 地址，点击复制保存：

![URL回调已注册](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/dingtalk-5.CfyUyl-J.png)

选择「使用 URL 回调」，还需要返回钉钉开发者后台，配置钉钉消息接收地址：

1. 进入机器人配置页面
2. 下滑到页面底部，找到消息接收配置
3. 将「Stream 模式」切换为「**HTTP 模式**」

![切换HTTP模式](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/switch-http-mode.BA2uojja.png)

4. 在「消息接收地址」中粘贴 Webhook 地址
5. **重要**：将地址中的 `http` 改为 `https`
6. 点击「发布」保存配置

![配置Webhook地址](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/config-webhook.UDh3FyeJ.png)

### 发布钉钉应用

应用必须发布后才能在钉钉中使用。

#### 创建钉钉应用版本

1. 点击页面上方的「查看版本详情」

![查看版本详情](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/view-version-details.0yAIXXq8.png)

2. 填写版本描述信息

![填写版本描述](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/fill-version-desc._FOw3HqW.png)

#### 提交发布

1. 点击「确认发布」提交审核

![确认发布版本](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/confirm-publish-version.nHnfEK4L.png)

2. 等待审核通过（通常会很快自动审批）

![审批通过](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/approval-passed.Cg9e4SLR.png)

### 钉钉开始使用

钉钉机器人支持两种使用方式：**群聊使用**和**单聊使用**。

#### 在群聊中使用

如果您想在群里使用机器人：

**第一步**：创建或选择一个群聊

创建群聊时，请确保群的「归属组织」与创建机器人时的组织相同。

**第二步**：添加机器人到群聊

1. 点击群右上角的设置按钮

![群聊设置](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/group-settings.Dnq0n7SX.png)

2. 选择「机器人」

![机器人设置](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/robot-settings.DLLx4rNs.png)

3. 点击「添加机器人」

![添加机器人到群聊](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/add-robot-to-group.hm8ha6Sf.png)

4. 搜索并选择您创建的机器人

![搜索机器人](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/search-robot-group.LpBU0LAt.png)

5. 确认添加

![确认添加机器人](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/confirm-add-robot.C3aLkqs-.png)

**第三步**：开始使用

在群里 @机器人 并发送您的需求，WorkBuddy 会自动执行任务并回复结果。

![群聊使用效果](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/chat-usage.BdwPRh3l.png)

#### 单聊使用

如果您想直接与机器人私聊：

1. 在钉钉顶部搜索框中，搜索机器人的名称

![搜索机器人私聊](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/search-robot-private.DzOR9AIx.png)

2. 点击机器人进入对话窗口，直接发送消息即可

![单聊使用效果](https://download.codebuddy.cn/web/docs/688347ea6a808d65a655fde345b5bc3170647b7c/docs/static/chat-usage.BdwPRh3l.png)

恭喜

您已成功将 WorkBuddy 接入钉钉！现在可以通过钉钉随时随地远程控制 WorkBuddy 完成各种编程任务了。

### 钉钉常见问题

#### 机器人没有响应怎么办？

请按以下步骤排查：

1. **检查应用状态**：确认应用已发布并通过审批
2. **检查 Webhook 配置**：确认地址正确，且使用的是 `https` 协议
3. **检查 WorkBuddy**：确保电脑上的 WorkBuddy 正在运行，且 **助理** 已开启
4. **检查权限**：确认三个权限都已正确开通

#### 在群里找不到机器人怎么办？

1. 确认机器人应用已发布
2. 确认群聊的「归属组织」与机器人所属组织相同
3. 尝试重启钉钉客户端

## 相关文档

- [助理功能说明](./From-Beginner-to-Expert-Guide/Function-Description/Assistant)
- [WorkBuddy 开启第一个任务](./FirstTask)