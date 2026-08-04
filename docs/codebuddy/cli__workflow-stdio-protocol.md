# Workflow stdio 协议（stream\-json）

本文档规定 CodeBuddy CLI（`cbc` / `codebuddy`）在 stdio `stream-json` 通道上如何暴露 **Dynamic Workflow** 的进度与生命周期，以及该协议与 Claude Code 2\.1\.220 的对齐关系。目标是让任何按 Claude Code 官方 stream\-json 协议实现的 SDK / daemon / CI 都能不改代码地消费 cbc 的 workflow 事件。

> 适用于：`cbc --input-format stream-json --output-format stream-json`（即 headless stdio）。同一线上格式也用于 `-p` / `--print` 且 `--output-format=stream-json` 的场景。

## 1\. 与 Claude Code 2\.1\.220 的对齐关系

Claude Code 通过既有的 `system/task_*` 消息族承载 Dynamic Workflow 的进度，**不**新增独立的顶层 `type`。cbc 采用同样的约定：

| 关注点 | 线上形态（Claude Code 2\.1\.220 与 cbc 一致） |
| --- | --- |
| Workflow run 声明 | `{"type":"system","subtype":"task_started","task_type":"local_workflow","workflow_name":"...", ...}` |
| Phase / sub\-agent 进度 | `{"type":"system","subtype":"task_progress","workflow_progress":[{"type":"workflow_phase",...}, {"type":"workflow_agent",...}], ...}` |
| 状态变迁 | `{"type":"system","subtype":"task_updated","patch":{"status":"running|completed|failed|killed", ...}}` |
| 终态 | `{"type":"system","subtype":"task_notification","status":"completed|failed|stopped", ...}` |
| 中断 / 取消 | `{"type":"control_request","request":{"subtype":"interrupt", ...}}`（会话级） |

**不存在** cbc 独有的顶层 `type:"workflow"` 事件。任何说 Claude Code stream\-json 协议方言的消费者，都能无缝驱动并观测 cbc 的 workflow。

## 2\. 传输层

- **分帧**：newline\-delimited JSON（ndjson）。每行一个事件，以 `\n` 结束。**不是** SSE。
- **方向**：
	- **stdin**：`control_request` \+ `user` 消息。
	- **stdout**：`system`（含 subtype）、`assistant`、`user`、`result`、`control_response`。
- **编码**：UTF\-8。
- **顺序**：事件按产生顺序发出。见 §6 的时序保证。

## 3\. 功能总开关

Workflow 功能是全局开关（不按传输通道细分）：

| 触发条件 | 含义 |
| --- | --- |
| `CODEBUDDY_DISABLE_WORKFLOWS=1`（env） | 禁用整个 Workflow 功能。 |
| `settings.json: { "disableWorkflows": true }` | 同上，按用户 / 项目粒度关闭。 |

被禁用时，`Workflow` 工具不会注册，也不会产生 workflow 形状的 `task_started` / `task_progress` 事件；下游消费者只会看到其他后台任务的普通 `system/task_*` 消息。

## 4\. 从 stdin 驱动 workflow

控制通道与任何其它 stdio 会话一致：

jsonc
```
// 1. initialize
{"type":"control_request","request_id":"init","request":{"subtype":"initialize","hooks":{},"capabilities":{},"hasPrompt":true}}

// 2. 让 agent 起一次 workflow（模型将调用 `Workflow` 工具）
{"type":"user","message":{"role":"user","content":"run /deep-research topic=foo"}}

// 3. 全部停下（同时中止 workflow 与所有 sub-agent）
{"type":"control_request","request_id":"stop-1","request":{"subtype":"interrupt","session_id":"<sessionId>","reason":"user cancel"}}
```
注意：

- `interrupt` 的 `session_id` 取自更早的 stdout `system/init` 事件。
- `interrupt` 会同时中止 workflow **和**在飞的 sub\-agent 模型流。

## 4\.1 中止正在运行的 workflow

stdio 协议上停止 workflow **只有一条路**：从 stdin 发一条 `control_request` \+ `subtype: "interrupt"`。没有 "取消单个 workflow" 的命令 —— `interrupt` 中止整个会话，这也是 CLI 端到端实际执行的语义。

### 报文格式

jsonc
```
{
  "type": "control_request",
  "request_id": "<客户端自选字符串>",
  "request": {
    "subtype": "interrupt",
    "session_id": "<sessionId>",
    "reason": "user cancel"
  }
}
```
规则：

- 每次运行只发一条 interrupt；对同一 session 的重复 interrupt 是幂等的。
- 只在 run 还活着时才有意义。收到该 workflow task 的 `task_notification` 之后，interrupt 对 workflow 状态就是 no\-op。
- `session_id` 是会话级的；中止一个 session 不会影响同进程里其它 session。
- **不要**用关闭 stdin 替代 interrupt。

### stdout 上会依次看到什么

interrupt 送达之后，按顺序会出现：

1. **`control_response`** —— 一次性 ACK：

json
```
{"type":"control_response","response":{"subtype":"success","request_id":"stop-1"}}
```
ACK 只代表 "CLI 收到了 interrupt"，**不**意味着 workflow 已经收尾。
2. **`system/task_updated`** —— workflow task 的 `patch.status` 翻到 `"killed"`，`patch.end_time` 填上时间戳：

json
```
{"type":"system","subtype":"task_updated","task_id":"<workflowTaskId>","patch":{"status":"killed","end_time":1785...}}
```
3. **`system/task_notification`** —— 只发一条，`status:"stopped"`（内部 `killed` / `cancelled` 均映射到该值，见 §5\.4）：

json
```
{"type":"system","subtype":"task_notification","task_id":"<workflowTaskId>","status":"stopped","summary":"...","output_file":"..."}
```
4. **迟到的 `system/task_progress` 事件**（cbc 相对 Claude Code 的超集）—— 每个 sub\-agent 收尾时，其在 `task_progress.workflow_progress[]` 里的 `workflow_agent` 条目会把 `state` 从 `"start"` 翻到 `"error"`，并携带 `error: "subagent aborted: ..."`。Claude Code 不保证这一步；cbc 为了可观测性额外发出。只依赖 Claude Code 保证事件的消费者应把 `task_notification.status="stopped"` 作为唯一权威终态。

### 参考实现（interrupt \+ 优雅 drain）

js
```
import { spawn } from 'node:child_process';

const cbc = spawn('cbc', [
  '--input-format', 'stream-json',
  '--output-format', 'stream-json',
  '--permission-mode', 'bypassPermissions',
], { stdio: ['pipe', 'pipe', 'pipe'] });

const send = obj => cbc.stdin.write(JSON.stringify(obj) + '\n');

let buf = '';
let sessionId;
const tasks = new Map(); // task_id -> { workflow_progress, status, notified }

cbc.stdout.on('data', chunk => {
  buf += chunk;
  const lines = buf.split('\n'); buf = lines.pop();
  for (const line of lines) {
    if (!line.trim()) continue;
    let msg; try { msg = JSON.parse(line); } catch { continue; }

    if (msg.type === 'system' && msg.subtype === 'init') sessionId = msg.session_id;
    if (msg.type !== 'system') continue;

    if (msg.subtype === 'task_started' && msg.task_type === 'local_workflow') {
      tasks.set(msg.task_id, { workflow_progress: [], status: 'running', notified: false });
    }
    if (msg.subtype === 'task_progress' && Array.isArray(msg.workflow_progress)) {
      const t = tasks.get(msg.task_id);
      if (t) t.workflow_progress = msg.workflow_progress; // 权威快照
    }
    if (msg.subtype === 'task_updated') {
      const t = tasks.get(msg.task_id);
      if (t && msg.patch?.status) t.status = msg.patch.status;
    }
    if (msg.subtype === 'task_notification') {
      const t = tasks.get(msg.task_id);
      if (t) { t.status = msg.status; t.notified = true; }
    }
  }
});

send({ type: 'control_request', request_id: 'init',
  request: { subtype: 'initialize', hooks: {}, capabilities: {}, hasPrompt: true } });
send({ type: 'user', message: { role: 'user', content: '/deep-research topic=foo' } });

async function cancel() {
  if (!sessionId) return;
  send({ type: 'control_request', request_id: 'stop-' + Date.now(),
    request: { subtype: 'interrupt', session_id: sessionId, reason: 'user cancel' } });
  await new Promise(resolve => {
    const check = () => {
      const stillRunning = [...tasks.values()].some(t => !t.notified);
      if (!stillRunning) resolve();
      else setTimeout(check, 200);
    };
    check();
  });
}
```
上述代码里的关键点：

- 用 `system/init` 里的 `session_id` 作为 interrupt 的目标。
- 用 `task_notification`（而不是 `control_response` ACK）作为 "run 完事了" 的判据。
- 把 `task_progress.workflow_progress` 视作**权威快照**：后到的 `task_progress` 覆盖同 `task_id` 的先前状态。

## 5\. 消息参考

### 5\.1 `task_started`

jsonc
```
{
  "type": "system",
  "subtype": "task_started",
  "task_id": "<uuid>",
  "tool_use_id": "<toolUseId>",
  "task_type": "local_workflow",          // ← workflow 任务的判别器
  "workflow_name": "path:simple.workflow.js",
  "description": "<workflow description>",
  "uuid": "<messageUuid>",
  "session_id": "<sessionId>"
}
```
- `task_type: "local_workflow"` 标识 workflow 任务；其它后台任务保留 `"Agent"` / `"Bash"` / `"PowerShell"` 等值。
- `workflow_name` 对应 workflow 声明的 `meta.name`（脚本按路径起时回退为 `path:<basename>`）。Claude Code 会额外在 `prompt` 字段带上完整 workflow JS 源码；cbc 一般省略 `prompt`。

### 5\.2 `task_progress`（workflow 形态）

每次 workflow 的 phase / sub\-agent 时间线发生变化时会发一条。消费方应把 payload 视作**权威快照** —— 该 `task_id` 上最新的 `workflow_progress` 会覆盖之前的。

jsonc
```
{
  "type": "system",
  "subtype": "task_progress",
  "task_id": "<uuid>",
  "tool_use_id": "<toolUseId>",
  "description": "<workflow description>",
  "usage": { "total_tokens": 0, "tool_uses": 0, "duration_ms": 0 },
  "workflow_progress": [
    { "type": "workflow_phase", "index": 1, "title": "Gather" },
    { "type": "workflow_agent", "index": 1, "agentId": "v2:<hash>",
      "state": "start", "startedAt": 178547..., "label": "child-1",
      "phaseTitle": "Gather", "phaseIndex": 1 }
  ],
  "uuid": "<messageUuid>",
  "session_id": "<sessionId>"
}
```
Timeline 条目形态（与 Claude Code 2\.1\.220 对齐）：

- **`workflow_phase`**：`{ type, index, title }` —— workflow 脚本声明的 phase。
- **`workflow_agent`**：`{ type, index, agentId, state, startedAt, endedAt?, label?, phaseIndex?, phaseTitle?, tokens?, resultPreview? }`
	- `state`：`"start"` → `"done"` \| `"error"` \| `"cached"`。
	- `agentId`：内容寻址 key `v<schema>:<sha256>`；跨重跑稳定，方便消费方去重或映射到缓存产物。

### 5\.3 `task_updated`

Workflow 任务每次状态变迁都会发一条；用 `patch` 观察增量。

jsonc
```
{"type":"system","subtype":"task_updated","task_id":"<id>","patch":{"status":"completed","end_time":178547...}}
```
`status` 取值：`pending`、`running`、`paused`、`completed`、`failed`、`killed`。

### 5\.4 `task_notification`

Workflow 任务每次进入终态发一条。

jsonc
```
{"type":"system","subtype":"task_notification","task_id":"<id>",
 "status":"completed",             // 或 "failed" / "stopped"
 "summary":"<summary>","output_file":"...","usage":{...}}
```
`status` 映射自内部 task 状态：`killed` / `cancelled` 都收敛为 `"stopped"`。这是**权威**终态信号 —— 完成判定不要从其它事件推导。

## 6\. 时序保证

- `task_started` / `task_updated` / `task_notification` 是**关键事件**：一定按发生顺序到达，任务终态前不会漏。
- Workflow 类的 `task_progress` 事件对 phase / sub\-agent 生命周期变化有**投递保证**：workflow 任务进入终态之前，每个非缓存 sub\-agent 的 `workflow_agent` 条目都会至少出现一次终态（`done` / `error` / `cached`）。
- **中断下的顺序**（cbc 相对 Claude Code 的超集）：中断路径下 sub\-agent 异步收尾，部分 `task_progress` 事件（典型是把 `workflow_agent.state` 翻到 `"error"`）可能**晚于** `task_notification` 到达。消费方应把 `task_notification.status="stopped"` 视作终态**状态**信号，但把 `task_id` 保留一段短 grace window（推荐 5 秒），以捕获迟到的 `task_progress` 更新。
- **快照替换语义**：同一 `task_id` 上后到的 `task_progress` 覆盖先前的 `workflow_progress` 快照。消费方无需累积 diff，直接以最新 payload 为准即可。

## 7\. 与 Claude Code 的兼容性

**cbc 保证字节级完全等价于 Claude Code 2\.1\.220 的部分**：

- `system/task_started` 形态（`task_id`、`tool_use_id`、`task_type: "local_workflow"`、`workflow_name`、`description`、`uuid`、`session_id` 全部一致）。
- `system/task_progress.workflow_progress[]` 元素形态：`workflow_phase` 与 `workflow_agent`，字段名（`agentId`、`state`、`startedAt`、`endedAt`、`phaseIndex`、`phaseTitle`、`label`、`tokens`、`resultPreview`）与 state 枚举（`start` / `done` / `error` / `cached`）一致。
- `system/task_updated.patch` 与 `system/task_notification.status` 语义。

**cbc 相对 Claude Code 已声明的超集**（不违反 Claude Code schema，对 Claude Code 原生消费者安全）：

- 中断路径下，cbc 会额外发 `task_progress` 消息把在飞 sub\-agent 的 `workflow_agent.state` 从 `"start"` 翻到 `"error"`；Claude Code 不保证这一步。
- cbc 的 `workflow_name` 在脚本按路径起时用 `path:<basename>`（Claude Code 用 workflow 源码里的 `meta.name`）。

**消费方 MUST 忽略无法识别的字段** —— cbc 保留在不做 major 版本升级的前提下追加新 timeline 条目类型和可选字段的权利（见 §8）。

## 8\. 版本约定

本协议是加性演进的：

- `workflow_progress` 下可能新增 timeline 条目 `type` 值；消费方 MUST 忽略无法识别的 type。
- 现有字段在 major 版本内不会重命名或删除。
- 每个 workflow 任务确保只发一条 `task_notification`；消费方可以把它作为终态信号。

## 9\. 安全与隐私

- `initialize` 的 `control_response` 里含 `account.token`（Keycloak JWT）、企业 id、邮箱。**不要**未过滤地留档或公开分享 stdout dump。
- `task_started.workflow_name`、`task_progress.workflow_progress[].label`、`task_progress.workflow_progress[].resultPreview` 可能含用户输入或 sub\-agent 输出片段 —— 下游渲染时视为**不可信**。
- Workflow 事件 payload 本身不包含完整 prompt 或完整模型输出，只有 id、计数和短预览。