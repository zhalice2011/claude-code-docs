# 无头模式 （Headless Mode)

> 以编程方式运行 CodeBuddy Code,无需交互式 UI

## 概述

无头模式允许您通过命令行脚本和自动化工具以编程方式运行 CodeBuddy Code,无需任何交互式 UI。

无头模式也支持定时任务相关能力。在脚本、SDK 或服务端集成场景中，可以使用 `CronCreate`、`CronList`、`CronDelete` 等工具来创建、查看和取消定时任务。

> **⚠️ 重要提示：** `-y` （或 `--dangerously-skip-permissions`) 是非交互模式的必需参数。在使用 `-p/--print` 参数进行非交互式执行时，必须添加此参数才能执行需要授权的操作（文件读写、命令执行、网络请求等）,否则这些操作会被阻止。仅 `-y` 时 HIGH/CRITICAL 危险命令仍可能要求确认；隔离沙箱里真正不询问请用 `export CODEBUDDY_IS_SANDBOX=1 && codebuddy -p -y ...`（高危，仅进程环境）。仅在受信任的环境和明确的任务场景下使用。详见 [CLI 参考](./cli-reference) 与 [沙箱 full pass（高危）](./env-vars#沙箱-full-pass-高危)。

## 基本用法

CodeBuddy Code 的主要命令行接口是 `codebuddy` （或 `cbc`) 命令。使用 `--print` （或 `-p`) 标志在非交互模式下运行并打印最终结果：

bash
```
codebuddy -p "暂存我的更改并为它们编写一组提交" \
  --allowedTools "Bash,Read" \
  --permission-mode acceptEdits
```
## 配置选项

无头模式利用 CodeBuddy Code 中所有可用的 CLI 选项。以下是用于自动化和脚本编写的关键选项：

| 标志 | 描述 | 示例 |
| --- | --- | --- |
| `--print`, `-p` | 在非交互模式下运行 | `codebuddy -p "查询"` |
| `--output-format` | 指定输出格式 （`text`, `json`, `stream-json`) | `codebuddy -p --output-format json` |
| `--resume`, `-r` | 通过会话 ID 恢复对话 | `codebuddy --resume abc123` |
| `--continue`, `-c` | 继续最近的对话 | `codebuddy --continue` |
| `--verbose` | 启用详细日志记录 | `codebuddy --verbose` |
| `--append-system-prompt` | 追加到系统提示词 （仅与 `--print` 配合使用） | `codebuddy --append-system-prompt "自定义指令"` |
| `--allowedTools` | 允许的工具列表,空格分隔或逗号分隔的字符串 | `codebuddy --allowedTools mcp__slack mcp__filesystem``codebuddy --allowedTools "Bash(npm install),mcp__filesystem"` |
| `--disallowedTools` | 拒绝的工具列表,空格分隔或逗号分隔的字符串 | `codebuddy --disallowedTools mcp__splunk mcp__github``codebuddy --disallowedTools "Bash(git commit),mcp__github"` |
| `--settings` | 从 JSON 文件或 JSON 字符串加载额外的设置配置 | `codebuddy -p --settings '{"model":"gpt-5"}' "查询"` |
| `--setting-sources` | 指定要加载的设置源（可选值: `user`, `project`, `local`） | `codebuddy -p --setting-sources project,local "查询"` |
| `--mcp-config` | 从 JSON 文件加载 MCP 服务器 | `codebuddy --mcp-config servers.json` |
| `--permission-prompt-tool` | 用于处理权限提示的 MCP 工具 （仅与 `--print` 配合使用） | ❌ 不支持 |

> **说明：** `--permission-prompt-tool` 功能当前不支持。

有关 CLI 选项和功能的完整列表，请参阅 [CLI 参考](./cli-reference) 文档。

## 多轮对话

对于多轮对话，您可以恢复对话或从最近的会话继续：

bash
```
# 继续最近的对话
codebuddy --continue "现在重构以提高性能"

# 通过会话 ID 恢复特定对话
codebuddy --resume 550e8400-e29b-41d4-a716-446655440000 "更新测试"

# 在非交互模式下恢复
codebuddy --resume 550e8400-e29b-41d4-a716-446655440000 "修复所有 linting 问题" -p
```
## 输出格式

### 文本输出 （默认）

bash
```
codebuddy -p "解释文件 src/components/Header.tsx"
# 输出： 这是一个 React 组件，显示...
```
### JSON 输出

返回包含元数据的结构化数据：

bash
```
codebuddy -p "数据层是如何工作的?" --output-format json
```
响应格式：

json
```
{
 ...
}
```
### 流式 JSON 输出

在收到每条消息时流式传输：

bash
```
codebuddy -p "构建一个应用程序" --output-format stream-json
```
每个对话都以初始 `init` 系统消息开始,然后是用户和助手消息列表,最后是包含统计信息的最终 `result` 系统消息。每条消息都作为单独的 JSON 对象发出。

### 后台任务事件（异步）

当模型用 `run_in_background: true` 启动后台命令（Bash / PowerShell）、后台工作流或**后台 Agent 子任务**时，CLI 会在 `stream-json` 输出流上为**每个任务**发出独立的 `system` 事件，携带唯一的 `task_id`（多任务并发时据此区分），`tool_use_id` 关联回发起该任务的 tool\_use：

- 任务启动 → `system` / `subtype: "task_started"`
- 任务进度（每完成一次 tool\_use，仅 sub\-agent/workflow 类）→ `system` / `subtype: "task_progress"`（带 `usage`）
- 任务状态变迁 → `system` / `subtype: "task_updated"`（带 `patch`）
- 任务完成/失败/被停止 → `system` / `subtype: "task_notification"`

jsonc
```
// 任务启动（进入运行态时立即推）
{"type":"system","subtype":"task_started","task_id":"agent-00f6","tool_use_id":"toolu_01","description":"bg agent","task_type":"Agent","uuid":"...","session_id":"..."}
// 进度（每完成一次 tool_use，携带累计 usage + 最近工具名；shell 任务不发）
{"type":"system","subtype":"task_progress","task_id":"agent-00f6","description":"bg agent","usage":{"total_tokens":320,"tool_uses":2,"duration_ms":157},"last_tool_name":"Bash","uuid":"...","session_id":"..."}
// 状态变迁（patch 携带变更字段；终态补 end_time）
{"type":"system","subtype":"task_updated","task_id":"agent-00f6","patch":{"status":"completed","end_time":1783945615966},"status":"completed","uuid":"...","session_id":"..."}
// 任务完成（可能在触发它的那轮 result 之后才到达；sub-agent 带 usage）
{"type":"system","subtype":"task_notification","task_id":"agent-00f6","tool_use_id":"toolu_01","status":"completed","summary":"Background agent \"bg agent\" completed","output_file":"/.../bg-tasks/agent-00f6.stdout.log","usage":{"total_tokens":480,"tool_uses":2,"duration_ms":250},"session_id":"..."}
```
字段说明：

| 字段 | 事件 | 说明 |
| --- | --- | --- |
| `task_id` | 全部 | 后台任务唯一 ID，贯穿 started → progress → updated → notification，用于区分并发任务、路由到 `TaskOutput` |
| `tool_use_id` | 多数（可选） | 关联回模型那次 tool\_use |
| `description` / `task_type` | started / progress | 任务命令描述 / 工具类型（`Bash` / `PowerShell` / `Workflow` / `Agent`） |
| `usage` | progress（必有）/ notification（sub\-agent 有，shell 省略） | `{ total_tokens, tool_uses, duration_ms }`（对齐 CC 的 `TaskUsage`） |
| `last_tool_name` | progress（可选） | 最近一次执行的工具名 |
| `patch` / `status` | updated | 本次变更字段（至少 `status`，终态补 `end_time`） |
| `status` | notification | `completed` / `failed` / `stopped`（`killed`/`cancelled` 归一为 `stopped`） |
| `summary` | notification | 人类可读的完成摘要 |
| `output_file` / `output_stderr_file` | notification（可选） | 后台任务输出落盘路径（文件模式），可据此读取完整输出 |

> **进度事件（`task_progress`）是事件驱动的**（每完成一次 tool\_use 推一条），不是定时轮询；后台 shell 任务（Bash/PowerShell）不发 progress，只有 sub\-agent / workflow 类任务发。
> 
> **终态可能只来 `task_updated`**：某些后台任务的终态只通过 `task_updated`（`patch.status` 为终态）到达而没有配套的 `task_notification`。跟踪"活跃任务"的消费方应对二者的终态 status（`completed` / `failed` / `stopped` / `killed`）一视同仁地清理。

> **重要（stdio 长连接场景）**：后台任务可能在**触发它的那一轮 `result` 之后**才完成。使用 `--input-format stream-json --output-format stream-json`（stdin 保持打开的长连接）时，CLI 会在任务真正结束后把 `task_notification` 主动推回到同一输出流——**无需**你再发新的输入。因此消费方应持续读取输出流，不要在收到第一个 `result` 后就停止读取，否则会错过后台完成事件。纯 `-p` 单发模式（进程随首个 `result` 结束）不支持后台任务，会返回明确错误。

> **禁用后台任务**：不支持/不需要后台任务的场景，设置环境变量 `CODEBUDDY_CODE_DISABLE_BACKGROUND_TASKS=1` 可禁用后台任务——Bash / PowerShell / Agent 的 `run_in_background` 参数会从工具 schema 中隐藏，即便模型仍下发也会被忽略/降级为前台执行，从而不产生任何后台 task 事件、也不会有跨轮回推。**SDK 的 `query()` 单发用法已自动注入该变量**（因为 `query()` 在首个 `result` 处停止、无法接收跨轮回推事件）；持续读取的 SDK 用法（JS `unstable_v2_createSession` / Python `CodeBuddySDKClient`）不受影响。

### 结构化 JSON 输出

要获得符合特定架构的输出，请使用 `--output-format json` 和 `--json-schema` 以及 [JSON Schema](https://json-schema.org/) 定义。响应包括关于请求的元数据（会话 ID、使用情况等），结构化输出在 `structured_output` 字段中。

此示例从 auth.py 中提取函数名称并将其作为字符串数组返回：

bash
```
codebuddy -p "提取 auth.py 中的主要函数名称" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'
```

> **提示**：使用 [jq](https://jqlang.github.io/jq/) 之类的工具来解析响应并提取特定字段：
> 
> bash
> ```
> # 提取文本结果
> codebuddy -p "总结这个项目" --output-format json | jq -r '.result'
> 
> # 提取结构化输出
> codebuddy -p "提取 auth.py 中的函数名称" \
>   --output-format json \
>   --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}' \
>   | jq '.structured_output'
> ```

## 输入格式

### 文本输入 （默认）

bash
```
# 直接参数
codebuddy -p "解释这段代码"

# 从 stdin
echo "解释这段代码" | codebuddy -p
```
### 流式 JSON 输入

通过 `stdin` 提供的消息流,其中每条消息代表一个用户轮次。这允许在不重新启动 `codebuddy` 二进制文件的情况下进行多轮对话，并允许在模型处理请求时向模型提供指导。

每条消息都是一个 JSON "用户消息" 对象,遵循与输出消息模式相同的格式。消息使用 [jsonl](https://jsonlines.org/) 格式进行格式化,其中每行输入都是一个完整的 JSON 对象。流式 JSON 输入需要 `-p` 和 `--output-format stream-json`。

bash
```
echo '{"type":"user","message":{"role":"user","content":[{"type":"text","text":"解释这段代码"}]}}' | \
  codebuddy -p --output-format=stream-json --input-format=stream-json --verbose

# 单条消息（包含图片）
echo '{"type":"user","message":{"role":"user","content":[{"type":"text","text":"文本提示词，如参考以下图片的文案"},{"type":"image","source":{"type":"base64","media_type":"image/png","data":"原始base64（不含协议前缀）"}}]}}' \
  | codebuddy -p --input-format stream-json --output-format stream-json

# 多轮对话（多行 JSON，对同一进程持续发送）
printf '%s\n' \
  '{"type":"user","message":{"role":"user","content":[{"type":"text","text":"第一问"}]}}' \
  '{"type":"user","message":{"role":"user","content":[{"type":"text","text":"第二问"}]}}' \
  | codebuddy -p --input-format stream-json --output-format stream-json --verbose
```
\#\#会话回退（Rewind）

回退能力让你把「工作区文件」和/或「对话历史」恢复到某条历史用户消息发送**之前**的状态。适用于自动化 Agent 在一次错误改动后重来、或 IDE/上游平台（如 CloudAgent）实现"撤销到某条消息"的场景。

对齐 Anthropic Claude Code v2\.1\.88 的命名与协议，并针对上游需求做了扩展。

### 命令行 flag（`--print` 家族启动时）

| Flag | 作用 | 约束 |
| --- | --- | --- |
| `--rewind-files <user-message-id>` | 把工作区文件恢复到该user 消息发送前的快照，然后**立即退出** | 需配合 `--resume`/`-c`；不能同时带 prompt |
| `--resume-session-at <message id>` | 恢复会话时，只保留到该消息（含）为止的历史（`slice(0, index+1)`），再继续对话 | 需配合 `--resume`/`-c` |
| `--dry-run` | 与 `--rewind-files` 组合，只预览要回退的文件差异，不改磁盘 | — |

bash
```
# 把文件回退到某条 user 消息之前的状态并退出
codebuddy -p --resume <sessionId> --rewind-files <userMessageUuid>

# 只预览（不改磁盘）
codebuddy -p --resume <sessionId> --rewind-files <userMessageUuid> --dry-run

# 恢复会话但把历史截断到某条消息，然后发新prompt
codebuddy -p --resume <sessionId> --resume-session-at <messageUuid> "换个方式重做这一步"
```
这三个 flag 是隐藏 flag（不出现在 `--help`），仅供 SDK / 上游平台脚本化调用。它们在所有 `--print` 变体（一次性、`--output-format json`、`--input-format stream-json` 长驻）启动时都生效。

### 流式 JSON 控制协议（长驻运行时）

在 `--input-format stream-json` 长驻模式下，可在**不重启进程**的情况下通过 `control_request` 触发回退。支持两个 subtype：

| subtype | 回退范围 | 说明 |
| --- | --- | --- |
| `rewind_files` | 仅**文件** | 对齐 Claude Code，只回退磁盘、不动对话历史 |
| `rewind` | 由 `scope` 决定 | cbc 扩展。`scope` 可选 `Code`（仅文件）/ `Conversation`（仅历史）/ `CodeAndConversation`（默认，文件\+历史）。文件回退失败**不阻塞**历史回退（部分成功语义） |

`rewind` 的 `scope` 取值：

| scope | 回退范围 |
| --- | --- |
| `CodeAndConversation`（默认） | 文件 \+ 对话历史一起（真实上游 CloudAgent 用法） |
| `Conversation` | 仅回退对话历史，保留磁盘文件 |
| `Code` | 仅回退磁盘文件 |

**请求：**

jsonc
```
// 仅回退文件（对齐 Claude Code）
{"type":"control_request","request_id":"r1","request":{"subtype":"rewind_files","user_message_id":"<uuid>","dry_run":false}}

// 文件 + 对话历史一起回退（scope 省略即默认 CodeAndConversation）
{"type":"control_request","request_id":"r2","request":{"subtype":"rewind","user_message_id":"<uuid>","dry_run":false}}

// 仅回退对话历史（保留磁盘文件）
{"type":"control_request","request_id":"r3","request":{"subtype":"rewind","user_message_id":"<uuid>","scope":"Conversation"}}
```
**响应（成功）：**

jsonc
```
// rewind_files（严格对齐 Claude schema，五字段）
{"type":"control_response","response":{"subtype":"success","request_id":"r1","response":{
  "canRewind":true,"filesChanged":["src/a.ts"],"insertions":12,"deletions":5}}}

// rewind（额外带 historyRewound；部分成功时带 fileRewindError）
{"type":"control_response","response":{"subtype":"success","request_id":"r2","response":{
  "canRewind":true,"filesChanged":["src/a.ts"],"insertions":12,"deletions":5,"historyRewound":true}}}
```
响应字段：

| 字段 | 类型 | 含义 |
| --- | --- | --- |
| `canRewind` | boolean | 是否成功回退（`rewind` 下历史成功即为 true） |
| `error` | string? | 失败原因（前置校验失败 / 历史回退失败） |
| `filesChanged` | string\[]? | 涉及的文件列表 |
| `insertions` / `deletions` | number? | 行级增删统计 |
| `historyRewound` | boolean? | （仅 `rewind`）对话历史是否已回退 |
| `fileRewindError` | string? | （仅 `rewind`）**部分成功**标志：`canRewind:true` 但文件回退失败，历史已回退——上游据此提示用户手动处理文件，但对话上下文已正确回到目标点 |

**关键语义（`rewind`）：文件回退失败不阻塞历史回退。** handler 先尽力回退文件（失败仅记录到 `fileRewindError`，不中断），再回退对话历史（必须成功）。因此即便工作区文件被占用/权限不足，会话上下文仍能正确回到目标点。

**`user_message_id` 的获取**：在 stream\-json 输出流里，`file-history-snapshot` 消息的 `snapshot.messageId` 即对应 user 消息的 id；也可直接用输出流中`type:"user"` 消息的 `uuid`。

**`dry_run: true`**：只计算并返回 `filesChanged`/`insertions`/`deletions` 预览，不改磁盘、不截断历史（`historyRewound:false`）。适合先弹窗给用户确认再真正回退。

### 与 Claude Code 的差异

| 能力 | Claude Code | cbc |
| --- | --- | --- |
| `rewind_files`（文件回退） | ✅ | ✅ 字段/语义严格对齐 |
| `--resume-session-at`（历史截断） | ✅ 仅 CLI flag | ✅ CLI flag |
| 运行时 `rewind`（文件 / 历史 / 两者，由 scope 选择） | ❌ 无 | ✅ cbc 扩展 |
| 运行时仅回退对话历史 | ❌ 无 | ✅ `rewind` \+ `scope:"Conversation"` |
| 文件回退失败不阻塞历史 | ❌ | ✅ `fileRewindError` 部分成功 |

### 在 SDK 中调用

TypeScript / Python SDK **无需新增专用方法**——rewind 是 SDK → CLI 方向的控制请求，直接复用 SDK 已有的通用 `control_request` 发送通道透传即可。请求/响应字段与上文一致。

**TypeScript SDK：**

ts
```
// query 为 SDK 的 Query 实例；transport.sendControlRequest 是既有通用通道
const resp = await query.transport.sendControlRequest<{
  canRewind: boolean;
  filesChanged?: string[];
  insertions?: number;
  deletions?: number;
  historyRewound?: boolean;
  fileRewindError?: string;
  error?: string;
}>({
  subtype: 'rewind',
  user_message_id: '<uuid>',
  scope: 'CodeAndConversation', // 省略即默认；可选 'Conversation' / 'Code'
});
if (resp.canRewind && resp.fileRewindError) {
  // 部分成功：历史已回退，文件回退失败——提示用户手动处理文件
}
```
**Python SDK：**

python
```
# query 为 SDK 的 Query 实例；_send_control_request 是既有通用通道
resp = await query._send_control_request({
    "subtype": "rewind",
    "user_message_id": "<uuid>",
    "scope": "Conversation",  # 仅回退对话历史
})
# resp: {"canRewind": True, "historyRewound": True, ...}
```

> 类型定义（`ControlRewindRequest` / `ControlRewindResponse` / `ControlRewindFilesRequest` / `ControlRewindFilesResponse`）已从 cbc 的 control\-signal 协议模块导出，TypeScript 消费方可直接 import 获得类型提示。

## Agent 集成示例

### SRE 事件响应机器人

bash
```
#!/bin/bash

# 自动化事件响应 agent
investigate_incident() {
    local incident_description="$1"
    local severity="${2:-medium}"

    codebuddy -p "事件: $incident_description (严重性: $severity)" \
      --append-system-prompt "你是一名 SRE 专家。诊断问题，评估影响，并提供即时行动项。" \
      --output-format json \
      --allowedTools "Bash,Read,WebSearch,mcp__datadog" \
      --mcp-config monitoring-tools.json
}

# 使用方式
investigate_incident "支付 API 返回 500 错误" "high"
```
### 自动化安全审查

bash
```
# PR 的安全审计 agent
audit_pr() {
    local pr_number="$1"

    gh pr diff "$pr_number" | codebuddy -p \
      --append-system-prompt "你是一名安全工程师。审查此 PR 的漏洞、不安全模式和合规问题。" \
      --output-format json \
      --allowedTools "Read,Grep,WebSearch"
}

# 使用并保存到文件
audit_pr 123 > security-report.json
```
### 多轮法律助手

bash
```
# 具有会话持久性的法律文档审查
session_id=$(codebuddy -p "开始法律审查会话" --output-format json | jq -r '.session_id')

# 分多个步骤审查合同
codebuddy -p --resume "$session_id" "审查 contract.pdf 的责任条款"
codebuddy -p --resume "$session_id" "检查 GDPR 要求的合规性"
codebuddy -p --resume "$session_id" "生成风险执行摘要"
```
## 最佳实践

- **使用 JSON 输出格式** 进行程序化解析响应：

bash
```
# 使用 jq 解析 JSON 响应
result=$(codebuddy -p "生成代码" --output-format json)
code=$(echo "$result" | jq -r '.result')
cost=$(echo "$result" | jq -r '.total_cost_usd')
```
- **优雅地处理错误** \- 检查退出代码和 stderr:

bash
```
if ! codebuddy -p "$prompt" 2>error.log; then
    echo "发生错误:" >&2
    cat error.log >&2
    exit 1
fi
```
- **使用会话管理** 在多轮对话中维护上下文
- **考虑超时** 对于长时间运行的操作：

bash
```
timeout 300 codebuddy -p "$complex_prompt" || echo "5 分钟后超时"
```
- **遵守速率限制** 在进行多个请求时，通过在调用之间添加延迟
- **使用 `-y`** 在非交互模式下执行需要授权的操作：

bash
```
# 非交互模式下的完整示例
codebuddy -p "分析代码并运行测试" \
  --output-format json \
  -y \
  --allowedTools "Bash,Read,Grep"
```

> **⚠️ 重要提示：** `-y` （或 `--dangerously-skip-permissions`) 是非交互模式的必需参数。在使用 `-p/--print` 参数进行非交互式执行时，必须添加此参数才能执行需要授权的操作（文件读写、命令执行、网络请求等）,否则这些操作会被阻止。仅 `-y` 时 HIGH/CRITICAL 危险命令仍可能要求确认；隔离沙箱里真正不询问请用 `export CODEBUDDY_IS_SANDBOX=1 && codebuddy -p -y ...`（高危，仅进程环境）。仅在受信任的环境和明确的任务场景下使用。详见 [CLI 参考](./cli-reference) 与 [沙箱 full pass（高危）](./env-vars#沙箱-full-pass-高危)。

## 相关资源

- [CLI 参考](./cli-reference) \- 完整的 CLI 文档
- [常见工作流](./common-workflows) \- 常见用例的分步指南
- [交互模式](./interactive-mode) \- 交互式会话功能
- [IAM 权限](./iam) \- 工具权限和访问控制

---

> **提示**：无头模式非常适合 CI/CD 管道、自动化脚本和 agent 集成。将其与 MCP 服务器结合使用以扩展功能。