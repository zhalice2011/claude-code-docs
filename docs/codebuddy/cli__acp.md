# ACP 协议集成

> ACP (Agent Client Protocol) 是 Zed 编辑器推出的一种通用智能体协议，使智能体的核心功能（服务端）和用户界面（客户端）解耦，允许用户自由选择不同的智能体服务端和客户端进行搭配使用。

CodeBuddy Code 原生支持 ACP 协议，可以作为智能体服务端与支持 ACP 的编辑器无缝集成。

## 快速开始

### 启动 ACP 模式

使用 `--acp` 参数启动 CodeBuddy Code 的 ACP 服务器：

bash
```
codebuddy --acp
```
## Zed 编辑器集成

### 配置步骤

打开 Zed 配置文件（`~/.config/zed/settings.json`），添加以下配置：

json
```
{
  "agent_servers": {
    "CodeBuddy Code": {
      "command": "codebuddy",
      "args": ["--acp"],
      "env": {}
    }
  }
}
```
随后即可在 Zed 侧边栏创建 CodeBuddy Code Thread，开始使用。

### 配置说明

- **command**：指定 CodeBuddy Code 的命令路径（确保 `codebuddy` 在 PATH 中可用）
- **args**：使用 `["--acp"]` 启用 ACP 协议模式
- **env**：可选的环境变量配置，例如：

json
```
{
  "env": {
    "CODEBUDDY_API_KEY": "your-api-key",
    "CODEBUDDY_INTERNET_ENVIRONMENT": "internal"
  }
}
```

> **注意**：使用 `CODEBUDDY_API_KEY` 时，必须根据版本正确配置 `CODEBUDDY_INTERNET_ENVIRONMENT`：
> 
> 
> 	- 海外版：不设置（默认）
> 	- 中国版：`internal`
> 	- iOA 版：`ioa`详见 [身份和访问管理文档](./iam#个人用户-获取-api-key)。

## ACP 协议特性

### 客户端轮次 ID

客户端可以在 `session/prompt` 请求的 `_meta` 中提供本轮 `conversationRequestId`：

json
```
{
  "_meta": {
    "codebuddy.ai/conversationRequestId": "0198a1b2c3d47e5f8a9b0c1d2e3f4a5b"
  }
}
```
该值必须是小写、无连字符的 32 位 UUIDv7 十六进制字符串；省略时由 CLI 生成。CLI 不扫描会话历史做碰撞检测，调用方负责保证唯一性。普通 prompt 真正进入 history 后，相同值会写入本轮 `PromptResponse._meta`、语义消息的 `SessionUpdate._meta`、JSONL `providerData.conversationRequestId` 和模型请求头 `X-Conversation-Request-ID`。`/clear`、`/compact` 等短路命令或在 history 前被拒绝的 prompt 不保证产生这些输出。现有 `_meta['codebuddy.ai/requestId']` 语义保持不变。

### 认证信息扩展

CodeBuddy Code 在 `authenticate` 响应的 `_meta` 字段中返回用户信息：

json
```
{
  "_meta": {
    "codebuddy.ai/userinfo": {
      "userId": "用户 ID",
      "userName": "用户名",
      "userNickname": "用户昵称"
    }
  }
}
```
客户端可以利用这些信息提供更好的用户体验，例如显示当前登录用户、个性化界面等。

### 工具代理机制

ACP 协议支持客户端代理部分工具操作，提升性能和安全性：

- **文件操作代理**：基于客户端的 `fs.readTextFile` 和 `fs.writeTextFile` 能力
- **终端操作代理**：基于客户端的 `terminal` 能力

当客户端声明支持这些能力时，CodeBuddy Code 会自动将相关工具调用代理给客户端执行。

### 命令列表推送

CodeBuddy Code 会在创建新会话时自动向客户端推送可用的 Slash 命令列表（`available_commands_update`），让客户端能够：

- 提供命令自动补全功能
- 显示命令提示和帮助信息
- 动态更新可用命令

命令列表会包含当前可调用的项目级、用户级和插件 Skill，并在 Skill 加载完成或可见性配置变化后自动刷新。列表会过滤掉本地命令（如 `/clear`、`/exit`）和客户端专属命令（如 `/theme`、`/config`），只推送适用于 ACP 模式的命令。

### 上下文窗口档位配置

CodeBuddy Code 通过 `getConfigOptions` / `setSessionConfigOption` 的 `context_window` 配置项支持会话级上下文预算档位选择（如 200K / 1M）：

- **下发条件**：仅当当前模型配置了多档上下文预算（`contextWindow.supportedLengths` 不少于 2 档）时，`getConfigOptions` 才返回该配置项；单档或无配置的模型不会出现选择器。
- **档位校验**：`setSessionConfigOption('context_window', value)` 只接受当前模型已声明的档位，非法值会被拒绝。
- **生效范围**：档位是会话级临时配置，进程内有效；切换会话时保持，重启进程后回落模型默认档。
- **分母联动**：选择档位后，上下文环（`usage_update.size`）与压缩阈值均按该档位计算。

### Agent Teams 协议扩展

CodeBuddy Code 通过 `session_info_update` 的 `_meta` 字段扩展 ACP 协议，支持 Agent Teams 多智能体协作的实时状态推送。

#### Team 状态事件

通过 `_meta['codebuddy.ai/teamUpdate']` 推送以下事件类型：

**成员状态变化** (`member_status_change`)：

json
```
{
  "sessionUpdate": "session_info_update",
  "_meta": {
    "codebuddy.ai/teamUpdate": {
      "type": "member_status_change",
      "teamName": "my-team",
      "isAutoTeam": false,
      "members": [
        {
          "name": "ux-designer",
          "color": "blue",
          "description": "用户体验设计分析",
          "status": "running",
          "taskId": "agent-abc123",
          "sessionId": "session-xyz",
          "tokenUsage": { "inputTokens": 1000, "outputTokens": 500, "lastContextWindow": 42000 },
          "toolCallCount": 5
        }
      ]
    }
  }
}
```
**Team 创建** (`team_created`) / **删除** (`team_deleted`)：

json
```
{
  "sessionUpdate": "session_info_update",
  "_meta": {
    "codebuddy.ai/teamUpdate": {
      "type": "team_created",
      "teamName": "my-team"
    }
  }
}
```
#### 成员流式消息

成员的实时消息（文本、工具调用）通过标准 ACP 事件推送，附加 `_meta['codebuddy.ai/memberEvent']` 标记来标识消息来源：

json
```
{
  "sessionUpdate": "agent_message_chunk",
  "content": { "type": "text", "text": "正在分析架构方案..." },
  "_meta": {
    "codebuddy.ai/memberEvent": "tech-architect"
  }
}
```
客户端收到带 `memberEvent` 标记的事件后，应将其路由到对应成员的对话时间线，而非主对话区。

#### 页面刷新恢复

页面刷新后，`loadSession` 的 `replayHistory` 完成后会自动推送当前 Team 状态（`member_status_change` 事件），客户端无需单独请求。`AcpTeamBridge` 在订阅成员 session 时会自动重放其完整历史，因此成员的对话数据也通过 ACP SSE 完整恢复，无需额外 HTTP API。

## 其他编辑器支持

ACP 是开放协议，理论上任何支持 ACP 的编辑器都可以集成 CodeBuddy Code。配置方式与 Zed 类似：

json
```
{
  "agent_servers": {
    "CodeBuddy": {
      "command": "codebuddy",
      "args": ["--acp"]
    }
  }
}
```
## Multitask 协调器

ACP / `--serve` **不要**加 `--agent multitask` 或 `--multitask`（入口守卫会拒，进程非 0）。Multitask 是会话级 **overlay**，不是 Scene Mode，也不是 `permissionMode`。盖章不改 `agentName` / `permissionMode`，也不走 `session/set_mode`。与 `mainAgentSupport` 独立：未 opt\-in 的宿主仍可发现并写入这条标准 boolean 配置。

### 1\. 发现能力位

`initialize` 响应：

json
```
{ "agentCapabilities": { "multitaskSupport": true } }
```
只认 `multitaskSupport === true`。字段缺失或 `false` 都不要画开关（例如 `CODEBUDDY_CODE_DISABLE_BACKGROUND_TASKS`）。Helper：`isMultitaskSupportAdvertised`。

### 2\. 发现配置项

`session/new`、`session/load`、`session/resume` 的 `configOptions` 里按 **`id === 'multitask'`** 查找。`category` 是元数据（当前为 `_codebuddy.ai/multitask`），**不是主键**。

json
```
{
  "type": "boolean",
  "id": "multitask",
  "name": "Multitask",
  "description": "Coordinate detached workers while keeping the current agent mode",
  "category": "_codebuddy.ai/multitask",
  "currentValue": false
}
```
没有这一项：本会话不能开（极简站立、worker / 子会话、后台任务禁用）。客户端必须能消化未知 category；正确性只依赖 `id`、`type`、`currentValue`。

### 3\. 标准写入（推荐）

```
session/set_config_option
```
json
```
{
  "sessionId": "<id>",
  "configId": "multitask",
  "type": "boolean",
  "value": true
}
```
`value` 必须是 JSON boolean。`"true"` / `1` 会被拒，不会静默 toggle。成功返回更新后的 `{ "configOptions": [...] }`；`currentValue` 以这次返回和随后的 `session/update`（`sessionUpdate: config_option_update`，全量 `configOptions`）为准。两条写入路径共用 live\-session 解析、连接归属、落盘和 `config_option_update`。业务拒绝（Minimal / worker / 后台禁用）走 JSON\-RPC `-32602`，详细原因在 `error.data.details`，不要只读 `error.message`（常为 `Invalid params`）。

ts
```
const response = await connection.setSessionConfigOption({
    sessionId,
    configId: 'multitask',
    type: 'boolean',
    value: true,
});

const option = response.configOptions.find(item => item.id === 'multitask');
const enabled = option?.type === 'boolean' && option.currentValue === true;
```
只认本连接的 `acpConnectionId`。调用方缺 id fail\-closed；会话无 owner 时允许已识别连接认领；其他 owner 一律拒绝。

### 4\. CodeBuddy 方言：`session/set_multitask`（兼容）

旧客户端仍可经 `extMethod` 使用。新客户端走上一节的标准写入。方言保留 toggle 和结构化 `{ ok, on, already, agentName, message }`。

|  |  |
| --- | --- |
| 方法名 | `session/set_multitask`（`ACP_METHOD_SESSION_SET_MULTITASK`） |
| 参数 | `{ sessionId, enabled?: boolean }`：`true` 进入，`false` 退出，省略 toggle |
| 响应 | `{ ok, on, already, agentName, message }` |
| 约束 | 非空白可切；worker / 子会话 / 极简站立 / 后台禁用返回 `ok: false` |
| 归属 / 校验 | 与标准写入相同；`enabled` 出现但不是布尔 → `invalidParams` |

ts
```
import {
    ACP_METHOD_SESSION_SET_MULTITASK,
    buildSetMultitaskParams,
    isMultitaskSupportAdvertised,
} from '@genie/agent-client-protocol';

if (isMultitaskSupportAdvertised(init.agentCapabilities)) {
    await conn.extMethod(ACP_METHOD_SESSION_SET_MULTITASK, buildSetMultitaskParams(sessionId, true));
}
```
TUI `/multitask` 复用同一套盖章语义。

### 5\. 非用户发起的 drain 轮

worker 完成后，协调器会在父会话 **idle**、且客户端没有再发 `session/prompt` 的情况下再跑一轮汇总。这一轮没有用户气泡，requestId 由 CLI 分配。

开轮时先推一条标准 `session_info_update`，再发内容帧；收口仍是既有 `session_end`：

json
```
{
  "sessionUpdate": "session_info_update",
  "_meta": {
    "codebuddy.ai/unsolicitedTurn": {
      "requestId": "cli-hex-request-id",
      "reason": "background_drain"
    },
    "codebuddy.ai/requestId": "cli-hex-request-id"
  }
}
```
客户端应按 `requestId` 立刻开一轮空 user 的 Request，不要等 `user_message_chunk`，也不要把 idle 之后的陌生 requestId 当僵尸帧丢掉。后续同 requestId 的 `tool_call` / `agent_message_chunk` 归入这一轮；`session_end` 收口。

Helper：`buildUnsolicitedTurnUpdate` / `readUnsolicitedTurn`（`ACP_META_UNSOLICITED_TURN`）。未知 `_meta` 必须忽略，不能当协议错误。

假模型端到端：`packages/agent-cli/src/e2e/multitask-wakeup.spec.ts`（需先 `pnpm run bundle`）。

### 6\. 子 worker 提问跨父轮

协调器派工后 `end_turn`、父会话 idle 是预期行为。活着的 detached worker 的 `AskUserQuestion` / `ExitPlanMode` 仍走父会话的 `requestPermission`。宿主**不要**因为父轮 `session_end` 把这些提问标成已取消。只有用户停止该 worker，或关闭父会话，才收口。

## 故障排除

### 连接失败

**问题**: Zed 无法连接到 CodeBuddy

**解决方法**:

1. 确认 `codebuddy` 命令可用：

bash
```
which codebuddy
```
2. 测试 ACP 模式启动：

bash
```
codebuddy --acp
```
3. 检查配置文件 JSON 格式是否正确

### 工具调用失败

**问题**：文件操作或命令执行报错

**解决方法**:

1. 检查工作目录权限
2. 查看 CodeBuddy 日志

## 相关链接

- [CLI 参考手册](./cli-reference) \- 查看所有命令行参数（含 `--multitask`）
- [斜杠命令](./slash-commands) \- `/multitask`
- [IDE 集成说明](./ide-integrations) \- 更多编辑器集成方式
- [ACP 协议规范](https://github.com/agentclientprotocol/agent-client-protocol) \- 协议详细文档

---

*通过 ACP 协议，让 CodeBuddy Code 融入您喜爱的编辑器 🚀*