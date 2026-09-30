# WorkBuddy 接入 QQ 指南

本指南将帮助您将 WorkBuddy 接入 QQ，让您可以通过 QQ 随时随地远程操控电脑上的 WorkBuddy 完成任务。

## 接入 QQ 能做什么

将 WorkBuddy 接入 QQ 后，你可以随时随地通过 QQ 与电脑上的 WorkBuddy 助理对话、派发任务：

| 能力 | 说明 |
| --- | --- |
| 远程操控完成任务 | 不在电脑前也能给 WorkBuddy 派活，让它读写文件、整理资料、生成文档 |
| 发送文件与图片 | 可直接在 QQ 中向机器人发送文件和图片，作为任务的输入材料 |
| 高危操作确认 | 远程执行删除文件等高风险操作前，WorkBuddy 会先在 QQ 中向你确认，经你同意后才会执行，远程使用也安全可控 |
| 私聊与群聊 | 支持与机器人一对一私聊，也支持拉入 QQ 群后 **@机器人** 使用，与团队成员共享任务 |

## 接入前准备

在开始之前，请确保您已满足以下条件：

- 已在电脑上安装 WorkBuddy，并开启了**助理**远程控制功能。
- 拥有一个已完成实名认证的 QQ 账号。

提示

QQ 开放平台要求账号完成实名认证。如未认证，请先在 QQ 中完成实名认证后再进行后续操作。

## 接入 QQ

### 第一步：注册并登录 QQ 开放平台

打开浏览器，访问 [QQ 开放平台](https://q.qq.com/qqbot/openclaw/login.html)，使用QQ扫码登录。

![登录QQ开放平台](https://download.codebuddy.cn/web/docs/71c8722a08165ddedf566c5f1711bb0ec8ea991b/docs/static/qq-guide-1.BSmYTk4-.png)

### 第二步：创建机器人

点击创建机器人：

![创建机器人](https://download.codebuddy.cn/web/docs/59627aa83a521ce15e8397f23b45ea83b3a15b19/docs/static/qq-guide-2.DdeZxWeY.png)

点击后会立刻成功，此时机器人会给你的QQ发一条成功消息，头像昵称可按喜好自定义编辑。

### 第三步：获取并配置凭证

复制并保存机器人的 AppID 和 AppSecret 。

![复制AppID和AppSecret](https://download.codebuddy.cn/web/docs/59627aa83a521ce15e8397f23b45ea83b3a15b19/docs/static/qq-guide-3.B1fiLS6i.png)

重要提示

出于安全考虑，AppSecret不支持明文保存，二次查看将会强制重置，请自行妥善保存。

### 第四步：在 WorkBuddy 中接入 QQ

1. 打开 WorkBuddy，点击助理的**设置**⚙️图标后进入**助理设置**页面。
2. 点击QQ机器人卡片右边的**连接**按钮。

![QQ机器人集成配置](https://download.codebuddy.cn/web/docs/59627aa83a521ce15e8397f23b45ea83b3a15b19/docs/static/qq-guide-5.CppvIKbu.png)

3. 选择一种方式连接已创建的 QQ 机器人
- **QQ 扫码**：扫码连接已创建的机器人。

![QQ 扫码连接](https://download.codebuddy.cn/web/docs/59627aa83a521ce15e8397f23b45ea83b3a15b19/docs/static/qq-guide-6.BqAWhxq9.png)

- **更多连接方式**：选择 WebSocket 长连接或使用 URL 回调，填入上方复制保存的 AppID 和 AppSecret ，点击**连接**按钮。

![更多连接方式](https://download.codebuddy.cn/web/docs/59627aa83a521ce15e8397f23b45ea83b3a15b19/docs/static/qq-guide-7.CsjQmu3T.png)

4. 连接成功后，在**助理**页面上方会显示 QQ 图标。

![助理QQ图标](https://download.codebuddy.cn/web/docs/59627aa83a521ce15e8397f23b45ea83b3a15b19/docs/static/qq-guide-9.2UbTr9Lp.png)

## 开始使用

接入成功后，即可通过 QQ 开始使用 WorkBuddy。

提示

QQ 机器人依赖电脑端的 WorkBuddy 运行。请保持电脑开机且 WorkBuddy 处于运行状态，否则机器人将无法响应消息。

### 发起任务

- **私聊**：在 QQ 中找到已创建的机器人，直接发送消息。
- **群聊**：将机器人加入 QQ 群，在群聊中 **@机器人** 后发送需求。

使用自然语言描述需要完成的任务，例如：

- 「帮我把桌面上的发票按月份归类」
- 「统计一下本周的会议纪要里有哪些待办事项」

### 发送文件和图片

直接在对话中发送文件或图片，WorkBuddy 会将其作为任务材料处理，也可以配合文字说明任务需求。

### 确认高风险操作

当任务涉及删除文件、执行脚本等高风险操作时，WorkBuddy 会在 QQ 中发送确认消息。确认后才会继续执行；拒绝后则不会执行该操作。

## 取消 QQ 连接

如果不再需要 QQ 机器人服务，可进入**设置** \> **助理设置**页面，在 **QQ 机器人**卡片右侧点击**取消连接**。取消连接后将无法继续使用 QQ 集成服务，但不会影响已有会话记录。

## 声明

本节说明，构成[服务协议](https://rule.tencent.com/rule/202603180001)和[隐私保护](https://privacy.qq.com/document/preview/771d9a58551449e9a7e7445ebfe04966)指引的组成部分，具有同等法律效力。 如有不一致之处，以前述协议原文为准。