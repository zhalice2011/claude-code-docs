# 企业微信智能机器人接入指南

通过 `/remote-control` 命令，您可以将 CodeBuddy Code 快速接入企业微信智能机器人，实现远程消息驱动。采用 **WebSocket 长连接** 主动连接方式，无需公网 IP，配置最为简洁。

## 前置条件

- 已注册企业微信账户
- CodeBuddy Code 已安装：`codebuddy --version`
- 已完成登录认证：`codebuddy` 后执行 `/login`

---

## 1\. 创建企业微信智能机器人

### 1\.1 打开创建页面

1. 打开企业微信客户端，进入「工作台」
2. 点击「智能机器人」→ 点击「创建」→ 选择「手动创建」

> 如果在工作台中未找到「智能机器人」入口，请将企业微信更新到最新版本。

### 1\.2 填写基本信息

输入机器人名称、头像、应用简介等基本信息。

![填写基本信息](https://download.codebuddy.cn/web/docs/b8be01454d01231d2f211ac94f535f8b9a6712db/docs/static/wecom_create_bot_1.D5tSjnJQ.png)

### 1\.3 切换到 API 模式

在页面底部点击「API 模式创建」。

![切换 API 模式](https://download.codebuddy.cn/web/docs/b8be01454d01231d2f211ac94f535f8b9a6712db/docs/static/wecom_create_bot_2.D6BjqJJ6.png)

### 1\.4 选择长连接方式

在 API 模式创建页面，找到「API 配置」区域，将连接方式选择为「使用长连接」。

![API 模式创建页面](https://download.codebuddy.cn/web/docs/b8be01454d01231d2f211ac94f535f8b9a6712db/docs/static/wecom_create_bot_3.DRlXQpTS.png)

### 1\.5 获取 Bot ID 和 Secret

在「API 配置」区域中找到以下信息并妥善保存：

- **Bot ID**：机器人的唯一标识（示例：`aibVGv7I...`）
- **Secret**：点击「获取」或「点击获取」获取访问密钥

![API 配置 - 获取 Bot ID 和 Secret](https://download.codebuddy.cn/web/docs/b8be01454d01231d2f211ac94f535f8b9a6712db/docs/static/wecom_create_bot_4.mRGxr9uD.png)

> ⚠️ **重要**：Secret 仅显示一次。如丢失可在机器人详情页重新生成。

### 1\.6 保存机器人

确认 Bot ID 和 Secret 已记录后，点击「保存」完成创建。

---

## 2\. 接入方式

推荐在 `/remote-control` 里选 **Add WeCom Bot → Scan QR**，用企业微信扫终端或网页上的码。扫完会自动拿到 Bot ID / Secret 并连上长连接。

也可以继续手填（环境变量或 `~/.codebuddy/channels/wecom/instances.json`）：

## 2\.1 配置环境变量

在启动 CodeBuddy CLI 前，设置以下环境变量：

bash
```
export CODEBUDDY_WECOM_BOT_ID="<你的 Bot ID>"
export CODEBUDDY_WECOM_BOT_SECRET="<你的 Bot Secret>"
```
### 可选配置

| 环境变量 | 说明 | 默认值 |
| --- | --- | --- |
| `CODEBUDDY_WECOM_BOT_ID` | AI Bot ID（必填） | — |
| `CODEBUDDY_WECOM_BOT_SECRET` | AI Bot Secret（必填） | — |
| `CODEBUDDY_WECOM_BOT_WS_URL` | WebSocket 服务地址（私有化部署时使用） | `wss://openws.work.weixin.qq.com` |
| `CODEBUDDY_WECOM_STREAMING_DEFAULT` | 全局默认流式开关（`1`/`0`，或 `true`/`false`） | 未设置 → 开（与逐机器人默认一致） |
| `CODEBUDDY_WECOM_CARDS_DEFAULT` | 全局默认权限/建议卡片开关（`1`/`0`，或 `true`/`false`） | 未设置 → 开（与逐机器人默认一致） |

**优先级**：单个机器人在操作页里显式设置的流式/卡片开关 \> 上面两个全局默认 \> 内置默认（开）。多个机器人共享一套全局默认时，只需设置一次，无需逐个机器人配置。

### 持久化配置（可选）

将环境变量添加到 shell 启动文件中，每次启动时自动生效：

bash
```
# ~/.zshrc 或 ~/.bashrc
export CODEBUDDY_WECOM_BOT_ID="<你的 Bot ID>"
export CODEBUDDY_WECOM_BOT_SECRET="<你的 Bot Secret>"
```

---

## 3\. 启动 CodeBuddy 并连接

### 3\.1 启动交互模式

bash
```
codebuddy
```
### 3\.2 打开远程控制面板

```
/remote-control
```
此命令打开交互式面板，列出所有可用的连接客户端。

### 3\.3 连接 wecom\-bot

使用方向键选择企微条目，按 `Enter` 进入该机器人的操作页（连接 / 断开、流式开关、卡片开关）：

```
Remote Control

  • WeCom  [disconnected · stream]
  • Add WeCom Bot
  • Add WeChat Account
  ✖ Cancel
```
未配置凭证时会先出企业微信绑定二维码；也可以在添加时选择手填 Bot ID / Secret。连接成功后面板会自动关闭。

环境变量 `CODEBUDDY_WECOM_BOT_ID` / `CODEBUDDY_WECOM_BOT_SECRET` 拉起的 `default` 机器人同样可以进操作页改开关，选项会写入 `~/.codebuddy/channels/wecom/instances.json`。该实例不能从面板删除。

### 3\.4 查看连接状态

再次执行 `/remote-control` 可查看连接状态。企微条目会附带当前模式，例如 `[connected · stream]` 或 `[connected · reply · text]`。

状态说明：

- `disconnected` — 未连接
- `connecting` — 连接中，请稍候
- `connected` — 已连接
- `stream` / `reply` — 流式开 / 关（关则整段推送，不刷工具进度）
- `text` — 已关掉卡片交互，确认改回回复 `y` / `n` 或编号

Web UI 远程控制页也有同样的流式、卡片开关。

---

## 4\. 面板操作说明

| 操作 | 说明 |
| --- | --- |
| `↑` / `↓` | 选择客户端条目 |
| `j` / `k` | Vim 风格导航（等同于上下方向键） |
| `Enter` | 企微进入操作页（连接、流式、卡片）；其他默认实例直接连接或断开 |
| `Esc` | 返回上一层或退出面板 |

---

## 5\. 验证接入

连接建立后，可通过以下方式验证 Bot 是否正常工作。

### 方式一：直接对话

1. 打开企业微信客户端（桌面端或移动端）
2. 在消息列表中找到你创建的机器人
3. 发送测试消息（如「你好」），确认 Bot 有回复

### 方式二：群组对话

1. 将机器人添加到群聊
2. 在群组中通过 @机器人名称 发送消息
3. Bot 会响应被 @ 的消息

---

## 6\. 消息处理流程和状态指示

### 消息处理全流程

用户发送消息到 Bot 后的处理流程：

```
用户在企业微信发送消息
        ↓ WebSocket 长连接实时推送消息
CodeBuddy CLI 接收消息
        ↓ 5 秒内回复（满足企微回调超时要求）
流式开：立即建流（同一回调 req_id），边生成边全量替换当前气泡
流式关：整段生成完再推一条回复，不刷工具进度和子代理感知
        ↓
权限 / 提问 / 建议：默认竖排投票卡；关掉卡片后改回文字确认
        ↓
后续结论再开一条新气泡（流式）或再推一条文本（非流式）
```
### 流式回复机制

默认使用企微流式消息（`aibot_respond_msg` stream 类型）。可在 `/remote-control` 或 Web UI 为当前机器人关掉流式，改回整段 `WeComReply` 推送。

流式开启时：

1. **立即建流**：收到用户消息后马上用回调里的 `req_id` 建流，满足 5 秒回复要求
2. **原位替换**：同一 `stream.id` 的后续帧是全量内容，用来刷新当前这条气泡
3. **一段一条**：一段正文结束后 `finish=true`，下一句换新的 `stream.id`，避免一轮回复全挤在一起
4. **工具状态**：长工具和子代理执行时用单独状态条，不泄露命令、文件内容和任务 prompt
5. **交互卡片**：权限确认、提问、下一步建议走竖排投票卡（`vote_interaction`）；点选后提交，卡片按官方协议在 5 秒内置灰。发卡片失败或关掉卡片时，改用原来的文字回复（`y` / `n` / 编号）

> 参考：[智能机器人长连接文档](https://developer.work.weixin.qq.com/document/path/101463) —— `req_id` 关联同一次回调，`stream.id` 标识一条气泡，`stream.content` 为全量替换。

#### 用户看到的效果

| 阶段 | 聊天窗口显示 | 说明 |
| --- | --- | --- |
| 消息发送后（流式开） | 开始出现回复，并随生成更新 | 同一条气泡全量替换，不是追加 |
| 消息发送后（流式关） | 等整段完成后再出现一条回复 | 不刷工具进度和子代理感知 |
| 需要确认时（卡片开） | 竖排选项 \+ 提交，权限卡会带上命令摘要 | 超长命令会再跟一条原文 |
| 需要确认时（卡片关） | 纯文本，回复 `y` / `n` 或编号 | 与 2\.140\.0 一致 |
| 一段结束 | 该条气泡锁定，下一段新开一条 | 一轮内多段回复分条展示 |

### 超时处理

- **流式消息超时**：6 分钟（从首次发送 stream 开始计时）
- **安全超时**：5 分钟（预留 1 分钟余量）
- **超时回退**：如果 Agent 处理超过 5 分钟，自动回退到异步推送（`aibot_send_msg`，24 小时有效期）
- **回调超时**：收到消息回调后需在 5 秒内发送回复（流式占位消息满足此要求）

---

## 7\. 工作原理

```
企业微信用户发送消息
        ↓
企业微信服务器（WebSocket 连接池）
        ↓ WebSocket 长连接实时推送
CodeBuddy CLI（WecomBotClient）
        ↓
CodeBuddy Agent 处理消息，生成回复
        ↓
通过同一 WebSocket 连接回复消息
        ↓
企业微信用户收到 Bot 回复
```
### 关键特性

- **连接方式**：WebSocket 长连接（客户端主动连接，无需公网 IP）
- **认证机制**：启动时发送 `aibot_subscribe` 帧，携带 `bot_id` \+ `secret` 完成鉴权
- **消息接收**：企业微信服务器通过 `aibot_msg_callback` 帧实时推送用户消息
- **消息回复**：通过 `aibot_respond_msg` 帧以流式方式返回 Agent 回复
- **心跳保活**：每 30 秒发送一次 `ping` 帧保持连接活跃
- **自动重连**：连接断开后按指数退避策略自动重连，最长延迟 60 秒

---

## 8\. 常见问题

### 环境变量未配置

**症状**：在 `/remote-control` 面板中选择 `wecom-bot` 后显示错误

```
Error: WeChat Work AI Bot is not configured.
Missing environment variables: CODEBUDDY_WECOM_BOT_ID, CODEBUDDY_WECOM_BOT_SECRET
```
**解决方案**：

1. 确认已设置 `CODEBUDDY_WECOM_BOT_ID` 和 `CODEBUDDY_WECOM_BOT_SECRET`
2. 执行 `echo $CODEBUDDY_WECOM_BOT_ID` 验证环境变量是否生效
3. 重新启动 CodeBuddy CLI
4. 再次执行 `/remote-control` 尝试连接

### 连接失败

**可能原因及排查**：

1. **Bot ID 或 Secret 错误**

	- 确认从企业微信后台复制的值完全一致（注意末尾是否有空格）
	- 确认 AI Bot 应用状态正常，未被停用
2. **网络连接问题**

	- 检查是否能访问 `wss://openws.work.weixin.qq.com`
	- 如使用私有化部署，确认 `CODEBUDDY_WECOM_BOT_WS_URL` 设置正确
	- 尝试在浏览器中测试网络连接：`curl -v wss://openws.work.weixin.qq.com`
3. **CLI 日志查看**

	- 查看终端输出的错误日志
	- 执行 `codebuddy` 后保持在主界面，观察连接过程中的输出

### 连接后消息无响应

**排查步骤**：

1. 执行 `/remote-control` 确认 `wecom-bot` 状态为 `connected`
2. 如状态为 `disconnected`，重新连接
3. 检查 CLI 终端日志是否有错误信息
4. 确认 CodeBuddy CLI 进程仍在运行（未被中断或退出）

### CLI 重启后需要重新连接

`/remote-control` 连接状态是临时的，不会持久化。每次重启 CodeBuddy CLI 后，需要重新执行 `/remote-control` 并选择 `wecom-bot` 建立连接。

**自动连接方案**（如需每次启动自动连接）：

将以下内容添加到启动脚本或 shell 配置文件中：

bash
```
# ~/.zshrc 或 ~/.bashrc
export CODEBUDDY_WECOM_BOT_ID="<你的 Bot ID>"
export CODEBUDDY_WECOM_BOT_SECRET="<你的 Bot Secret>"

# 可选：创建别名快速启动并自动连接
alias cbc-wecom='codebuddy -c "/remote-control"'
```

> 其中 `-c` 参数表示启动时自动执行指定命令。

### 应用提示"Token 过期"或"Secret 无效"

这通常表示 Bot 的 Secret 已失效或被重新生成。解决方案：

1. 登录企业微信管理后台，进入 Bot 详情页
2. 在「API 配置」区域重新生成 Secret
3. 更新环境变量 `CODEBUDDY_WECOM_BOT_SECRET`
4. 重启 CodeBuddy CLI 并重新连接

---

## 相关文档

- [Remote Control（远程控制）](./remote-control) \- 了解 Remote Control 的完整功能和其他客户端
- [斜杠命令](./slash-commands) \- 掌握所有内置命令
- [设置配置](./settings) \- 了解 CodeBuddy 配置选项