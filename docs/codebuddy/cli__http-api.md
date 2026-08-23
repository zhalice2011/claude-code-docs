# CodeBuddy Code HTTP API Beta

> **Beta**: 此 API 处于 Beta 阶段，接口可能会有调整。欢迎反馈意见。

CodeBuddy Code 提供两套公开接口，面向开发者构建 Agent 应用：

- **REST API** (`/api/v1/*`) — 无状态 HTTP 请求/响应，适合 Webhook 接入、管理操作、简单查询
- **ACP** (`/api/v1/acp`) — 有状态流式协议（JSON\-RPC over SSE），适合构建完整 Agent 客户端应用

## 快速开始

### 启动 HTTP 服务

bash
```
codebuddy --serve --port 8080 --session-id my-session
```
### API 文档（Swagger UI）

服务启动后访问：

- **交互式文档**: `http://127.0.0.1:8080/api/docs`
- **OpenAPI 规范**: `http://127.0.0.1:8080/api/openapi.json`

Swagger UI 提供所有公开端点的交互式测试界面。

### 验证服务正常

bash
```
curl http://127.0.0.1:8080/api/v1/health
# {"data":{"status":"ok","uptime":12.3,"platforms":["generic","wecom","wechat-kf"]}}
```
## API 分层

| 层级 | 路由前缀 | 兼容性承诺 | 说明 |
| --- | --- | --- | --- |
| **公开 REST API** | `/api/v1/*` | 语义化版本，不做破坏性变更 | 本文档覆盖的内容 |
| **公开 ACP 协议** | `/api/v1/acp` | 遵循 ACP 规范 | 完整对话能力，参见 [ACP 文档](https://agentclientprotocol.com) |
| **内部 RPC** | `/internal/*` | 不保证兼容性 | CLI 内部使用，不对外开放 |

## 安全

### 自定义请求头

所有 API 请求（除[豁免路径](#豁免路径)外）必须携带自定义请求头：

```
X-CodeBuddy-Request: 1
```
**原理**：自定义请求头会使浏览器的跨域请求变为"非简单请求"，强制触发 CORS preflight。配合 CORS 白名单，非法源的请求会被拦截。即使攻击者使用 `fetch(url, { mode: 'no-cors' })`，浏览器也不允许在 no\-cors 模式下发送自定义头，请求会因缺少该头而被服务端拒绝（403）。

#### 豁免路径

以下路径不需要携带 `X-CodeBuddy-Request` 头：

| 路径 | 说明 |
| --- | --- |
| `GET /` | SPA 入口页 |
| `GET /assets/*` | 静态资源 |
| `GET /docs/*` | API 文档页 |
| `GET /manifest.webmanifest` | PWA 清单 |
| `GET /api/v1/auth/status` | 认证状态检查 |
| `POST /api/v1/auth/login` | 登录 |
| `*/api/v1/webhooks/*` | Webhook（有平台签名验证） |
| `GET /api/openapi.json` | OpenAPI 规范 |
| `GET /api/docs*` | Swagger UI |

可通过环境变量 `CODEBUDDY_DISABLE_REQUEST_VALIDATION=1` 关闭此校验。

### CORS 白名单

跨域请求的 `Origin` 会与服务端 CORS 白名单匹配，不在白名单中的来源会被拒绝（预检返回无 CORS 头的 204，实际请求返回 403 `Origin not allowed`）。白名单来源：

- 本地端点自身的回环变体（`localhost` / `127.0.0.1` / `[::1]`，**仅限服务实际监听的端口**）
- Tunnel URL（如启用）
- 配置项 `gateway.corsOrigins`
- 环境变量 `CODEBUDDY_CODE_CORS_ORIGINS`（逗号分隔，支持精确 origin、`*.domain` 子域通配和 `*` 全开）

> ⚠️ **回环来源不再被无条件放行。** 早期实现允许任意 `localhost` / `127.0.0.1` 来源（不论端口），这使用户浏览器中任何占用本地端口的页面（如恶意页运行在 `http://localhost:3000`）都能跨源调用本服务的执行进程 / 文件读写接口。Cookie 的 `SameSite=Strict` 无法防护此场景 —— 端口不属于 "site" 的组成部分，`localhost:3000` 与 `localhost:8321` 属同 site 不同 origin，浏览器会照常携带会话 Cookie。
> 
> **本地开发**（Vite dev server 5173 → 后端 8321 属跨源）需显式声明来源：
> 
> bash
> ```
> CODEBUDDY_CODE_CORS_ORIGINS=http://localhost:5173 codebuddy --serve
> ```
> 被拒绝时，服务端日志与 403 响应体的 `hint` 字段都会提示该配置方式。

绑定 `0.0.0.0` 时（如 `--host 0.0.0.0`，常见于云虚拟机 / 局域网暴露场景），若未显式设置 `CODEBUDDY_CODE_CORS_ORIGINS`，服务端会**自动允许所有来源**（等价于配置 `*`），无需额外配置即可通过任意 IP 或域名访问 Web UI；显式设置该环境变量时以用户配置为准。此场景下认证为强制开启（见下），凭据仍是必需的。

### 认证

`--serve` **默认开启密码认证**。首次启动会生成随机密码并写入 `~/.codebuddy/settings.json`，同时在终端打印一条带密码的可点链接：

```
  Endpoint    http://127.0.0.1:8321
  Web UI      http://127.0.0.1:8321/?password=<生成的密码>

  Password    <生成的密码>
  Config      ~/.codebuddy/settings.json
```
点击该链接即可登录 Web UI（服务端会下发有效期 30 天的 `gateway_session` Cookie，后续直接访问端点即可，无需重复输入）。

认证模式优先级（高 → 低）：

| 来源 | 取值 | 说明 |
| --- | --- | --- |
| 环境变量 `CODEBUDDY_GATEWAY_AUTH` | `password` / `none` | 优先级最高，适合 CI |
| 绑定非回环地址（如 `--host 0.0.0.0`） | 强制 `password` | 对外暴露时不允许关闭 |
| 命令行 `--auth <mode>` | `password` / `none` |  |
| 配置项 `gateway.auth` | `password` / `none` |  |
| 默认值 | `password` | `--serve` 的兜底模式 |

> **安全说明**：这组端点包含执行进程（`/api/v1/process/*`）、读写任意文件（`/api/v1/files/*`、`/api/v1/fs/*`）和交互式终端（`/api/v1/pty/*`）等敏感能力。因此默认强制认证（secure by default，与 [E2B Secured Access](https://e2b.dev/docs/sandbox/secured-access) 的默认行为一致）。**关闭认证意味着同机任意进程都能通过该服务执行命令、读写文件**，仅建议在隔离环境（容器 / 一次性沙箱）或 CI 中使用。

关闭认证（仅在明确知晓风险时使用，启动时会打印警告）：

bash
```
codebuddy --serve --auth none
# 或
CODEBUDDY_GATEWAY_AUTH=none codebuddy --serve
```
#### 携带凭据的方式

**API 请求（`/api/v1/*`）只接受请求头或 Cookie**：

bash
```
# 1) Bearer Token（推荐，同时携带安全头）
curl -H "X-CodeBuddy-Request: 1" \
     -H "Authorization: Bearer YOUR_PASSWORD" \
     http://host:port/api/v1/sessions

# 2) X-Access-Token（与 Bearer 等价，对齐 E2B envd 的凭据头习惯）
curl -H "X-CodeBuddy-Request: 1" \
     -H "X-Access-Token: YOUR_PASSWORD" \
     http://host:port/api/v1/sessions

# 3) Cookie（浏览器登录后自动携带）
curl -H "X-CodeBuddy-Request: 1" \
     -H "Cookie: gateway_session=<sha256(password)>" \
     http://host:port/api/v1/sessions
```

> ⚠️ **`?password=` 仅对 `GET /` 与 `POST /api/v1/auth/login` 有效，对其他 `/api/v1/*` 端点无效**（会返回 401）。这是有意设计：URL 会被记录到浏览器历史、服务端访问日志，并在用户复制分享链接时泄露，因此密码不出现在 API 请求的网址中。`?password=` 的唯一用途是首次进门换取 `gateway_session` Cookie。
> 
> 用 `?password=` 测 API 会得到 401，这**不是**认证实现有问题。

## 响应格式

所有 `/api/v1/*` 端点使用统一的信封格式：

jsonc
```
// 成功
{
    "data": { ... }
}

// 错误
{
    "error": {
        "code": "AUTH_REQUIRED",      // 机器可读错误码
        "message": "Authentication required"  // 人类可读描述
    }
}
```
## 端点概览

### 系统

| 方法 | 端点 | 说明 |
| --- | --- | --- |
| GET | `/api/v1/health` | 健康检查 |
| GET | `/api/v1/info` | 环境信息（版本、OS、CWD 等） |
| GET | `/api/v1/metrics` | 系统资源指标 \+ 实例进程指标 |
| GET | `/api/v1/envs` | 环境变量（对齐 E2B envd） |

### 认证

| 方法 | 端点 | 说明 |
| --- | --- | --- |
| GET | `/api/v1/auth/status` | 获取认证状态 |
| POST | `/api/v1/auth/login` | 密码登录，返回 token |

### Runs（Agent 执行）

| 方法 | 端点 | 说明 |
| --- | --- | --- |
| POST | `/api/v1/runs` | 发起 Agent 执行（异步，返回 runId） |
| GET | `/api/v1/runs/:runId` | 查询执行状态 |
| GET | `/api/v1/runs/:runId/stream` | SSE 流式获取执行结果 |
| POST | `/api/v1/runs/:runId/cancel` | 取消执行 |

### Webhooks（第三方平台接入）

| 方法 | 端点 | 说明 |
| --- | --- | --- |
| GET | `/api/v1/webhooks/:platform` | 平台 URL 验证（企微等） |
| POST | `/api/v1/webhooks/:platform` | 平台消息 Webhook 入口 |

支持的平台：`generic`、`wecom`（企业微信）、`wechat-kf`（微信客服）

### 会话

| 方法 | 端点 | 说明 |
| --- | --- | --- |
| GET | `/api/v1/sessions` | 获取会话列表（支持 cwd 查询参数） |
| DELETE | `/api/v1/sessions/:id` | 删除会话 |
| POST | `/api/v1/sessions/:id/rename` | 重命名会话 |
| GET | `/api/v1/sessions/across-projects` | ⚠️ 已废弃，使用 `GET /api/v1/sessions?cwd=*` 代替 |
| GET | `/api/v1/sessions/workspaces` | ⚠️ 已废弃 |

### PTY（终端）

| 方法 | 端点 | 说明 |
| --- | --- | --- |
| POST | `/api/v1/pty` | 创建 PTY 会话 |
| GET | `/api/v1/pty` | 列出 PTY 会话 |
| GET | `/api/v1/pty/:id` | 查询 PTY 会话 |
| DELETE | `/api/v1/pty/:id` | 销毁 PTY 会话 |
| GET | `/api/v1/pty/:id/output` | SSE 流式获取 PTY 输出（替代 WebSocket） |
| POST | `/api/v1/pty/:id/input/send` | 发送 PTY 输入（对齐 E2B Process.SendInput） |
| POST | `/api/v1/pty/:id/resize` | 调整 PTY 大小（对齐 E2B Process.Update） |
| WebSocket | `/api/v1/pty/:id/ws` | PTY 双向数据传输（兼容保留） |

### Workers \& Daemon

Worker 是运行中的 CLI 进程（interactive / bg / daemon），通过 PID 文件注册表管理。

| 方法 | 端点 | 说明 |
| --- | --- | --- |
| GET | `/api/v1/workers` | 获取所有活跃 Worker 列表 |
| POST | `/api/v1/workers` | 手动添加远程 Worker |
| GET | `/api/v1/workers/:id` | 获取 Worker 详情（按 PID 或名称） |
| GET | `/api/v1/workers/:id/logs` | 获取 Worker 日志（支持多类型） |
| DELETE | `/api/v1/workers/:id` | 终止 Worker 进程 |
| GET | `/api/v1/daemon/status` | 查询 Daemon 状态 |
| POST | `/api/v1/daemon/start` | 启动 Daemon |
| POST | `/api/v1/daemon/stop` | 停止 Daemon |
| POST | `/api/v1/daemon/restart` | 重启 Daemon |

**Workers 查询参数**:

- `?kind=bg` — 按类型过滤（interactive / bg / daemon / daemon\-worker）
- `?local=true` — 仅返回本地 Worker（远程代理调用时使用）

**日志类型参数** (`GET /api/v1/workers/:id/logs`):

- `?type=telemetry` — 遥测日志（`~/.codebuddy/logs/{date}/`）
- `?type=process` — 进程 stdout/stderr（bg/daemon 日志）
- `?type=debug` — 调试日志（`~/.codebuddy/debug/`，需 `--debug`）
- `?type=transcript` — 对话历史摘要
- `?tail=200` — 只返回最后 N 行
- 不传 type 时自动选择最佳来源（telemetry \> process \> debug \> transcript）

### Jobs（后台智能体实例）

Jobs 是由 `/bg`、左箭头转后台或 `codebuddy agents` 派发出的后台智能体实例。它们与 CLI agent\-view / TUI 共用 JobStore 和生命周期语义。

| 方法 | 端点 | 说明 |
| --- | --- | --- |
| GET | `/api/v1/jobs` | 获取实例列表；支持 `all=1` 和 `cwd` 过滤 |
| POST | `/api/v1/jobs` | 派发后台智能体或 shell job |
| GET | `/api/v1/jobs/events` | SSE 订阅 `snapshot` / `added` / `changed` / `removed` / `keepalive` |
| GET | `/api/v1/jobs/prefs` | 获取置顶与项目分组偏好 |
| PUT | `/api/v1/jobs/prefs` | 批量更新置顶与项目分组偏好 |
| GET | `/api/v1/jobs/dispatch-context` | 获取启动目录、Agent 目录（内置四种模式 \+ 自定义，与主对话选择器同源）与仓库目标；响应含 `defaultAgentName`、`agents`、`permissionMode`（进程 `--permission-mode`） |
| GET | `/api/v1/jobs/resumable` | 获取可恢复的历史会话；支持 `cwd`、`includeAttached=1` |
| POST | `/api/v1/jobs/resume` | 从历史会话恢复为独立 job |
| GET | `/api/v1/jobs/:id` | 获取 job 详情；id 支持稳定 ID、short ID 或 sessionId |
| PATCH | `/api/v1/jobs/:id/name` | 重命名 job |
| POST | `/api/v1/jobs/:id/reply` | 回复等待输入的 job |
| POST | `/api/v1/jobs/:id/stop` | 停止 job |
| POST | `/api/v1/jobs/:id/respawn` | 重启 job 并恢复对话 |
| DELETE | `/api/v1/jobs/:id` | 删除 job 记录 |
| GET | `/api/v1/jobs/:id/stream` | SSE 回放 transcript 尾部并尾随新输出 |
| GET | `/api/v1/jobs/:id/transcript` | 一次性返回最近最多 1000 行 ACP replay updates |

**派发请求体** (`POST /api/v1/jobs`):

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `prompt` | string | 是 | 初始指令；`bash=true` 时为 shell 命令 |
| `cwd` | string | 否 | 启动目录，默认当前工作目录 |
| `model` | string | 否 | 指定模型，缺省按常规模型解析规则 |
| `effort` | string | 否 | `minimal` / `low` / `medium` / `high` / `xhigh` / `max` |
| `permissionMode` | string | 否 | `default` / `acceptEdits` / `plan` / `auto` / `dontAsk` / `bypassPermissions`。进程 `--permission-mode` 作为 Web 派发框默认，仍可被本次请求覆盖 |
| `agent` | string | 否 | 主 Agent：`cli` / `ptc` / `minimal` / `create` 或自定义 agent 名。省略时：进程 `--agent` \> `lastUsed` \> `default` \> 产品 `cli`。总闸关闭时忽略 shipped 模式名。`minimal` 与 `permissionMode=plan` 同传返回 `400 BAD_REQUEST` |
| `name` | string | 否 | 列表显示名称 |
| `bash` | boolean | 否 | 派发一次性 shell job |
| `sourceSessionId` | string | 否 | 继承受限上下文；新 job 仍使用独立会话 |
| `bgIsolation` | string | 否 | `none` / `worktree`；省略时跟随全局后台写隔离设置 |

`effort`、`permissionMode`、`bgIsolation` 按白名单校验，非法值返回 `400 BAD_REQUEST`。请求省略可选字段时不覆盖会话、全局或进程默认值。

`GET /api/v1/jobs/dispatch-context` 响应字段：

| 字段 | 说明 |
| --- | --- |
| `cwd` | 当前工作目录 |
| `defaultAgentName` | 派发框默认主 Agent：进程 `--agent` 优先，否则 `lastUsed` / `default` / 产品默认 |
| `agents` | 与主对话 chip 同一份目录（`built-in` 含 cli/ptc/minimal/create，外加自定义） |
| `permissionMode` | 进程 `--permission-mode`；有值时前端压过 lastUsed 权限 chip |
| `repoTargets` | 可派发的子仓 / worktree / 已有 job 仓根 |

**生命周期字段**:

- `state`: `working` / `blocked` / `done` / `failed` / `stopped`
- `status`: 存活进程的即时状态 `busy` / `waiting` / `idle` / `stopped`
- `tempo`: `active` / `idle` / `blocked`
- `alive` 与 `settled` 独立；`settled=true && alive=false` 表示已结束历史
- `foregroundHeld=true` 表示仍被前台终端持有，暂时不能 attach
- `webUrl` 仅在 job worker 存活并监听 loopback HTTP(S) 时返回，否则为 `null`

**对话与错误**:

- `/transcript` 一次性返回 `{ sessionId, updates }`，最多包含最近 1000 行转换后的 ACP replay updates。
- `/stream` 返回 `text/event-stream`；先回放最多 1000 行，再每秒尾随新增 JSONL 记录；shell job 返回空流。
- 不存在的 job 返回 `404 JOB_NOT_FOUND`。
- 删除若被 worktree 或前台持有守卫拒绝，仍返回 HTTP 200，但 body 为 `{ "deleted": false, "reason": "..." }`。

bash
```
# 派发后台智能体
curl -H "X-CodeBuddy-Request: 1" \
  -H "Authorization: Bearer $PASSWORD" \
  -H 'Content-Type: application/json' \
  -X POST http://127.0.0.1:8080/api/v1/jobs \
  -d '{"prompt":"检查当前仓库的测试状态","cwd":"/repo/app"}'

# 订阅 job 列表变化
curl -N -H "X-CodeBuddy-Request: 1" \
  -H "Authorization: Bearer $PASSWORD" \
  http://127.0.0.1:8080/api/v1/jobs/events
```
### Channels（远程控制）

| 方法 | 端点 | 说明 |
| --- | --- | --- |
| GET | `/api/v1/channels` | 获取客户端列表 |
| POST | `/api/v1/channels/:type/:id/start` | 启动客户端 |
| POST | `/api/v1/channels/:type/:id/stop` | 停止客户端 |
| POST | `/api/v1/channels/wechat` | 创建微信实例 |
| POST | `/api/v1/channels/wecom` | 创建企微实例 |

### 文件系统（E2B 兼容）

文件内容操作（对齐 E2B envd HTTP 端点）：

| 方法 | 端点 | 说明 |
| --- | --- | --- |
| GET | `/api/v1/files/download?path=...` | 下载文件（对齐 E2B envd GET /files） |
| POST | `/api/v1/files/upload?path=...` | 上传文件（对齐 E2B envd POST /files） |
| POST | `/api/v1/files/compose` | 合并多文件（对齐 E2B envd POST /files/compose） |

文件操作（对齐 E2B filesystem.proto）：

| 方法 | 端点 | 说明 |
| --- | --- | --- |
| POST | `/api/v1/fs/stat` | 获取文件/目录信息（对齐 Filesystem.Stat） |
| POST | `/api/v1/fs/list` | 列出目录内容（对齐 Filesystem.ListDir） |
| POST | `/api/v1/fs/mkdir` | 创建目录（对齐 Filesystem.MakeDir） |
| POST | `/api/v1/fs/remove` | 删除文件/目录（对齐 Filesystem.Remove） |
| POST | `/api/v1/fs/move` | 移动/重命名（对齐 Filesystem.Move） |

文件监听（对齐 E2B filesystem.proto）：

| 方法 | 端点 | 说明 |
| --- | --- | --- |
| POST | `/api/v1/fs/watch` | 流式目录监听 SSE（对齐 Filesystem.WatchDir） |
| POST | `/api/v1/fs/watcher/create` | 创建监听器（对齐 Filesystem.CreateWatcher） |
| POST | `/api/v1/fs/watcher/events` | 获取监听事件（对齐 Filesystem.GetWatcherEvents） |
| POST | `/api/v1/fs/watcher/remove` | 删除监听器（对齐 Filesystem.RemoveWatcher） |

CBC 增强：

| 方法 | 端点 | 说明 |
| --- | --- | --- |
| GET | `/api/v1/fs/search?query=...` | 文件模糊搜索（基于 ripgrep，E2B 无对应接口） |

### 进程管理（E2B 兼容）

对齐 E2B process.proto，将 gRPC 方法映射为 REST 端点：

| 方法 | 端点 | 说明 |
| --- | --- | --- |
| POST | `/api/v1/process/start` | 启动进程（对齐 Process.Start，支持 SSE/JSON） |
| GET | `/api/v1/process/list` | 列出运行中进程（对齐 Process.List） |
| POST | `/api/v1/process/connect` | 连接到进程 SSE 流（对齐 Process.Connect） |
| POST | `/api/v1/process/input/send` | 发送 stdin（对齐 Process.SendInput） |
| POST | `/api/v1/process/input/stream` | 流式发送 stdin（对齐 Process.StreamInput） |
| POST | `/api/v1/process/signal/send` | 发送信号（对齐 Process.SendSignal） |
| POST | `/api/v1/process/stdin/close` | 关闭 stdin（对齐 Process.CloseStdin） |
| POST | `/api/v1/process/update` | 更新进程配置如 PTY resize（对齐 Process.Update） |

### ACP（Agent Client Protocol）

| 方法 | 端点 | 说明 |
| --- | --- | --- |
| POST | `/api/v1/acp/connect` | 建立 ACP 连接，返回 connectionId 和 sessionToken |
| GET | `/api/v1/acp` | SSE 通知订阅（需要 acp\-connection\-id Header） |
| POST | `/api/v1/acp` | 发送 JSON\-RPC 请求（newSession、prompt、cancelRun 等） |
| DELETE | `/api/v1/acp` | 断开连接 |

### 文件变更（Checkpoint）— Internal

| 方法 | 端点 | 说明 |
| --- | --- | --- |
| POST | `/internal/file-changes/diff` | 获取单个文件的 diff 内容 |
| POST | `/internal/file-changes/checkpoints` | 列出可回退的 checkpoint |
| POST | `/internal/file-changes/revert` | 撤回文件变更或回退到 checkpoint |

> **注意**：这些是内部端点，无稳定性保证，仅供 Web UI 消费。

### 插件管理

| 方法 | 端点 | 说明 |
| --- | --- | --- |
| GET | `/api/v1/plugins` | 列出已安装插件（可选 `includeBuiltin=false` 过滤内置插件） |
| POST | `/api/v1/plugins` | 安装插件 |
| POST | `/api/v1/plugins/validate` | 验证插件/市场清单文件 |
| POST | `/api/v1/plugins/enable` | 启用插件 |
| POST | `/api/v1/plugins/disable` | 禁用插件 |
| POST | `/api/v1/plugins/uninstall` | 卸载插件 |
| POST | `/api/v1/plugins/update` | 更新插件到最新版本 |
| GET | `/api/v1/plugins/marketplaces` | 列出已配置的插件市场（可选 `includeBuiltin=false` 过滤内置市场） |
| POST | `/api/v1/plugins/marketplaces` | 添加插件市场（可选 `autoUpdate` 添加时即开启自动更新） |
| POST | `/api/v1/plugins/marketplaces/browse` | 浏览市场中的可用插件 |
| POST | `/api/v1/plugins/marketplaces/update` | 更新市场（同步远端仓库内容） |
| POST | `/api/v1/plugins/marketplaces/auto-update` | 开启/关闭市场自动更新 |
| DELETE | `/api/v1/plugins/marketplaces/:name` | 删除插件市场 |

### 配置管理

| 方法 | 端点 | 说明 |
| --- | --- | --- |
| GET | `/api/v1/settings` | 列出所有配置 |
| GET | `/api/v1/settings/:key` | 获取单个配置值 |
| PUT | `/api/v1/settings/:key` | 设置配置值 |
| POST | `/api/v1/settings/:key/items` | 向数组类配置追加值 |
| POST | `/api/v1/settings/:key/remove` | 从数组类配置移除值 |

### 工作目录

| 方法 | 端点 | 说明 |
| --- | --- | --- |
| GET | `/api/v1/workspace-dirs` | 列出当前附加工作目录 |
| POST | `/api/v1/workspace-dirs` | 添加单个工作目录 |
| DELETE | `/api/v1/workspace-dirs?path=` | 移除单个工作目录 |
| PUT | `/api/v1/workspace-dirs/sync` | 全量同步工作目录列表 |

### 任务模板

| 方法 | 端点 | 说明 |
| --- | --- | --- |
| GET | `/api/v1/tasks/templates` | 获取任务模板 |
| POST | `/api/v1/tasks/templates/refresh` | 刷新（触发 AI 推荐） |

### 使用统计

| 方法 | 端点 | 说明 |
| --- | --- | --- |
| GET | `/api/v1/stats` | 历史使用统计（跨所有项目） |
| GET | `/api/v1/stats/session` | 当前会话实时统计 |

### 链路追踪

| 方法 | 端点 | 说明 |
| --- | --- | --- |
| GET | `/api/v1/traces` | 获取 trace 列表（支持分页和过滤） |
| GET | `/api/v1/traces/:traceId` | 获取 trace 详情（含 spans） |
| DELETE | `/api/v1/traces` | 清空所有 traces |

**Traces 查询参数**:

- `?offset=0&limit=50` — 分页（limit 上限 200）
- `?session_id=xxx` — 按会话 ID 过滤
- `?worker_pid=12345` — 指定 Worker 实例（支持远程代理）
- `?worker_pid=all` — 扫描所有实例

### 定时任务

| 方法 | 端点 | 说明 |
| --- | --- | --- |
| GET | `/api/v1/scheduled-tasks` | 获取定时任务列表 |
| POST | `/api/v1/scheduled-tasks` | 创建定时任务 |
| DELETE | `/api/v1/scheduled-tasks/:id` | 删除定时任务 |

**定时任务查询参数**:

- `?sessionId=xxx` — 会话 ID（必需，不传则使用当前活跃会话）

## 使用示例

> 以下示例为突出各端点自身的参数而省略了公共请求头。实际调用 `/api/v1/*` 时需要补上：
> 
> 
> ```
> -H "X-CodeBuddy-Request: 1" -H "Authorization: Bearer $PASSWORD"
> ```
> 其中 `$PASSWORD` 是 `--serve` 启动时打印的密码（见[认证](#认证)）。缺少安全头会得到 403 `Missing required header`，缺少凭据会得到 401 `AUTH_REQUIRED`。仅 `/api/v1/health`、`/api/v1/auth/status` 等豁免端点可直接访问。

### 健康检查

bash
```
curl http://127.0.0.1:8080/api/v1/health
```
### 发起 Agent 执行

bash
```
# 发送消息（body 为 Gateway Protocol 格式，id/type 必填）
curl -X POST http://127.0.0.1:8080/api/v1/runs \
  -H "Content-Type: application/json" \
  -H "X-CodeBuddy-Request: 1" \
  -d '{
    "id": "run-1",
    "type": "message",
    "source": {"platform": "generic", "sender": {"id": "dev", "name": "Developer"}, "conversation": {"id": "run-1", "type": "direct"}},
    "payload": {"text": "帮我分析代码性能"}
  }'

# 响应: {"data": {"runId": "uuid-xxx", "status": "accepted"}}

# 通过 SSE 流获取结果（同样需携带 X-CodeBuddy-Request 头）
curl -H "X-CodeBuddy-Request: 1" http://127.0.0.1:8080/api/v1/runs/uuid-xxx/stream
```
#### 请求体字段（Gateway Protocol）

`POST /api/v1/runs` 的请求体为 Gateway Protocol 入站消息格式：

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `id` | ✅ | string | 消息唯一 ID，由调用方生成，用于去重与追踪 |
| `type` | ✅ | `"message"` \| `"action"` | 消息类型。`message` 发起对话，`action` 发送控制指令 |
| `payload.text` | — | string | prompt 文本（也兼容顶层 `text` / `prompt`） |
| `payload.attachments` | — | array | 附件列表，元素含 `type`（`image`/`voice`/`video`/`file`）、`url`、`urlType`（`local-path`/`url`）等 |
| `version` | — | string | 协议版本，默认 `"1.0"` |
| `source.platform` | — | string | 来源平台，默认 `"generic"` |
| `source.sender.id` | — | string | 发送者 ID，用于限流；缺省为 `"unknown"` |
| `source.sender.name` | — | string | 发送者名称 |
| `source.conversation.id` | — | string | 会话 ID，缺省取 `id` |
| `source.conversation.type` | — | `"direct"` \| `"group"` | 会话类型，默认 `"direct"` |
| `action` | — | `"cancel"` \| `"status"` | 仅 `type="action"` 时使用的控制动作 |
| `callback.url` | — | string | 异步回传结果的回调地址（模式 B） |
| `callback.headers` | — | object | 回调请求附加的自定义头 |
| `timeoutMs` | — | number | 单次执行超时（毫秒），优先级高于 `settings.gateway.runTimeoutMs`；也可用请求头 `X-Codebuddy-Run-Timeout`。设为 0 或负数关闭超时保护 |

> 权威定义见源码 `src/node/remote-gateway/gateway-protocol.ts` 的 `GatewayInboundMessage`。

### PTY 终端管理

bash
```
# 创建终端
curl -X POST http://127.0.0.1:8080/api/v1/pty \
  -H "Content-Type: application/json" \
  -d '{"cols": 120, "rows": 40}'

# 列出终端
curl http://127.0.0.1:8080/api/v1/pty

# SSE 流式获取输出（替代 WebSocket）
curl http://127.0.0.1:8080/api/v1/pty/SESSION_ID/output

# 发送输入
curl -X POST http://127.0.0.1:8080/api/v1/pty/SESSION_ID/input/send \
  -H "Content-Type: application/json" \
  -d '{"data": "ls -la\n"}'

# 调整大小
curl -X POST http://127.0.0.1:8080/api/v1/pty/SESSION_ID/resize \
  -H "Content-Type: application/json" \
  -d '{"cols": 200, "rows": 50}'

# 销毁终端
curl -X DELETE http://127.0.0.1:8080/api/v1/pty/SESSION_ID
```
### 文件系统操作（E2B 兼容）

bash
```
# 下载文件
curl "http://127.0.0.1:8080/api/v1/files/download?path=/tmp/test.txt"

# 上传文件
curl -X POST "http://127.0.0.1:8080/api/v1/files/upload?path=/tmp/upload.txt" \
  -H "Content-Type: application/octet-stream" \
  --data-binary @local-file.txt

# 获取文件信息
curl -X POST http://127.0.0.1:8080/api/v1/fs/stat \
  -H "Content-Type: application/json" \
  -d '{"path": "/tmp"}'

# 列出目录
curl -X POST http://127.0.0.1:8080/api/v1/fs/list \
  -H "Content-Type: application/json" \
  -d '{"path": "/tmp", "depth": 2}'

# 创建目录
curl -X POST http://127.0.0.1:8080/api/v1/fs/mkdir \
  -H "Content-Type: application/json" \
  -d '{"path": "/tmp/new-dir"}'

# 文件模糊搜索（CBC 增强）
curl "http://127.0.0.1:8080/api/v1/fs/search?query=component&limit=10"
```
### 进程管理（E2B 兼容）

bash
```
# 启动进程（JSON 模式）
curl -X POST http://127.0.0.1:8080/api/v1/process/start \
  -H "Content-Type: application/json" \
  -d '{"process": {"cmd": "python3", "args": ["script.py"]}, "tag": "my-script"}'

# 启动进程（SSE 流式输出）
curl -X POST http://127.0.0.1:8080/api/v1/process/start \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{"process": {"cmd": "python3", "args": ["script.py"]}}'

# 列出运行中进程
curl http://127.0.0.1:8080/api/v1/process/list

# 发送 stdin
curl -X POST http://127.0.0.1:8080/api/v1/process/input/send \
  -H "Content-Type: application/json" \
  -d '{"process": {"pid": 12345}, "input": {"stdin": "hello\n"}}'

# 发送信号（SIGTERM）
curl -X POST http://127.0.0.1:8080/api/v1/process/signal/send \
  -H "Content-Type: application/json" \
  -d '{"process": {"tag": "my-script"}, "signal": 15}'

# 系统指标 + 实例进程指标
curl http://127.0.0.1:8080/api/v1/metrics
# 响应: { data: { ts, cpuCount, cpuUsedPct, memTotalMib, memUsedMib, diskUsed, diskTotal, instances: [{ id, cwd, pid, rssMib, heapUsedMib, heapTotalMib, uptimeSeconds, ... }] } }
```
### 会话管理

bash
```
# 获取当前工作空间的会话列表
curl http://127.0.0.1:8080/api/v1/sessions

# 获取所有工作空间的会话列表
curl http://127.0.0.1:8080/api/v1/sessions?cwd=*

# 获取指定工作目录的会话列表
curl http://127.0.0.1:8080/api/v1/sessions?cwd=/path/to/workspace

# 获取指定项目的会话列表（按压缩工作目录名过滤）
curl http://127.0.0.1:8080/api/v1/sessions?cwd=*&projectId=workspace-hash

# 重命名会话
curl -X POST http://127.0.0.1:8080/api/v1/sessions/SESSION_ID/rename \
  -H "Content-Type: application/json" \
  -d '{"name": "性能优化讨论"}'
```
**cwd 查询参数说明**:

| cwd 值 | 说明 |
| --- | --- |
| 不传 | 返回当前工作空间的会话 |
| `*` | 返回所有工作空间的会话 |
| `/path/to/workspace` | 返回指定工作目录的会话 |

### 文件变更管理（Internal）

bash
```
# 获取文件 diff（需要文件在 checkpoint 中被跟踪）
curl -X POST http://127.0.0.1:8080/internal/file-changes/diff \
  -H "Content-Type: application/json" \
  -d '{"path": "/path/to/file.ts"}'
# 响应: {"data": {"path": "/path/to/file.ts", "oldText": "...", "newText": "..."}}

# 列出可回退的 checkpoint
curl -X POST http://127.0.0.1:8080/internal/file-changes/checkpoints \
  -H "Content-Type: application/json" \
  -d '{}'
# 响应: {"data": {"checkpoints": [{"id": "xxx", "label": "...", "createdAt": 1234567890, "files": [...], "additions": 5, "deletions": 2}]}}

# 按文件撤回变更
curl -X POST http://127.0.0.1:8080/internal/file-changes/revert \
  -H "Content-Type: application/json" \
  -d '{"paths": ["/path/to/file.ts"]}'
# 响应: {"data": {"success": true, "revertedFiles": ["/path/to/file.ts"]}}

# 回退到指定 checkpoint
curl -X POST http://127.0.0.1:8080/internal/file-changes/revert \
  -H "Content-Type: application/json" \
  -d '{"checkpointId": "checkpoint-uuid", "scope": "CodeAndConversation"}'
# scope 可选值: "Code"（仅回退文件）, "Conversation"（仅回退对话）, "CodeAndConversation"（全部回退）

# 撤回全部变更（回退到最早的 checkpoint）
curl -X POST http://127.0.0.1:8080/internal/file-changes/revert \
  -H "Content-Type: application/json" \
  -d '{}'
```
### 插件管理

bash
```
# 列出已安装插件（每项带 isBuiltIn 布尔字段，标识是否属于内置市场）
curl http://127.0.0.1:8080/api/v1/plugins

# 只列出用户自行安装的插件，过滤掉内置市场下的插件
curl "http://127.0.0.1:8080/api/v1/plugins?includeBuiltin=false"

# 安装插件（"name@marketplace" 格式）
curl -X POST http://127.0.0.1:8080/api/v1/plugins \
  -H "Content-Type: application/json" \
  -d '{"plugin": "my-plugin@my-marketplace"}'

# 启用插件
curl -X POST http://127.0.0.1:8080/api/v1/plugins/enable \
  -H "Content-Type: application/json" \
  -d '{"plugin": "my-plugin@my-marketplace"}'

# 禁用插件
curl -X POST http://127.0.0.1:8080/api/v1/plugins/disable \
  -H "Content-Type: application/json" \
  -d '{"plugin": "my-plugin@my-marketplace"}'

# 卸载插件
curl -X POST http://127.0.0.1:8080/api/v1/plugins/uninstall \
  -H "Content-Type: application/json" \
  -d '{"plugin": "my-plugin@my-marketplace"}'

# 更新插件到最新版本（传 waitForApply=true 可等待重建生效后再返回）
curl -X POST http://127.0.0.1:8080/api/v1/plugins/update \
  -H "Content-Type: application/json" \
  -d '{"plugin": "my-plugin@my-marketplace"}'

# 列出插件市场（每项带 isBuiltIn 布尔字段）
curl http://127.0.0.1:8080/api/v1/plugins/marketplaces

# 只列出用户自行添加的市场，过滤掉内置市场
curl "http://127.0.0.1:8080/api/v1/plugins/marketplaces?includeBuiltin=false"

# 添加插件市场
curl -X POST http://127.0.0.1:8080/api/v1/plugins/marketplaces \
  -H "Content-Type: application/json" \
  -d '{"source": "https://example.com/marketplace", "name": "my-marketplace"}'

# 添加插件市场并默认开启自动更新（等价于添加后再调一次 marketplaces/auto-update）
curl -X POST http://127.0.0.1:8080/api/v1/plugins/marketplaces \
  -H "Content-Type: application/json" \
  -d '{"source": "https://example.com/marketplace", "name": "my-marketplace", "autoUpdate": true}'

# 浏览市场中的插件
curl -X POST http://127.0.0.1:8080/api/v1/plugins/marketplaces/browse \
  -H "Content-Type: application/json" \
  -d '{"marketplace": "my-marketplace"}'

# 更新市场（真正从远端拉取最新内容）
curl -X POST http://127.0.0.1:8080/api/v1/plugins/marketplaces/update \
  -H "Content-Type: application/json" \
  -d '{"marketplace": "my-marketplace"}'

# 开启/关闭市场自动更新（开启后后台周期性同步并升级已安装插件）
curl -X POST http://127.0.0.1:8080/api/v1/plugins/marketplaces/auto-update \
  -H "Content-Type: application/json" \
  -d '{"marketplace": "my-marketplace", "autoUpdate": true}'

# 删除插件市场
curl -X DELETE http://127.0.0.1:8080/api/v1/plugins/marketplaces/my-marketplace
```
### 配置管理

bash
```
# 列出所有配置
curl http://127.0.0.1:8080/api/v1/settings

# 按作用域列出配置
curl "http://127.0.0.1:8080/api/v1/settings?scope=user"

# 获取单个配置
curl http://127.0.0.1:8080/api/v1/settings/model

# 设置配置值
curl -X PUT http://127.0.0.1:8080/api/v1/settings/theme \
  -H "Content-Type: application/json" \
  -d '{"value": "dark"}'

# 向数组类配置追加值
curl -X POST http://127.0.0.1:8080/api/v1/settings/permissions/items \
  -H "Content-Type: application/json" \
  -d '{"values": ["Allow: Read(**)"]}'

# 从数组类配置移除值
curl -X POST http://127.0.0.1:8080/api/v1/settings/permissions/remove \
  -H "Content-Type: application/json" \
  -d '{"values": ["Allow: Read(**)"]}'
```
### 工作目录

管理附加工作目录，使权限系统放行这些目录下的文件操作（与 `/add-dir` 命令效果一致）。

bash
```
# 列出当前附加工作目录
curl http://127.0.0.1:8080/api/v1/workspace-dirs

# 添加工作目录
curl -X POST http://127.0.0.1:8080/api/v1/workspace-dirs \
  -H "Content-Type: application/json" \
  -d '{"path": "/Users/me/other-project"}'

# 移除工作目录
curl -X DELETE "http://127.0.0.1:8080/api/v1/workspace-dirs?path=/Users/me/other-project"

# 全量同步（页面刷新恢复后调用）
curl -X PUT http://127.0.0.1:8080/api/v1/workspace-dirs/sync \
  -H "Content-Type: application/json" \
  -d '{"dirs": ["/Users/me/project-a", "/Users/me/project-b"]}'
```
**说明**：

- 添加的目录存储在 CLI scope（进程内存），实例关闭后失效
- 前端通过 Web UI 的 workspace storage 持久化，页面刷新后自动同步到后端
- 添加后，Agent 工具（Read/Write/Glob/Grep/Bash）可免询问访问这些目录

### 使用统计

bash
```
# 获取历史使用统计（活动热力图、模型/工具使用排行、连续活跃天数等）
curl http://127.0.0.1:8080/api/v1/stats

# 获取当前会话的实时成本统计
curl http://127.0.0.1:8080/api/v1/stats/session
```
### 链路追踪

bash
```
# 获取 trace 列表（分页）
curl "http://127.0.0.1:8080/api/v1/traces?offset=0&limit=20"

# 按会话 ID 过滤
curl "http://127.0.0.1:8080/api/v1/traces?session_id=SESSION_ID"

# 获取 trace 详情（含所有 spans）
curl http://127.0.0.1:8080/api/v1/traces/TRACE_ID

# 从远程 Worker 获取 traces
curl "http://127.0.0.1:8080/api/v1/traces?worker_pid=12345"

# 清空所有 traces
curl -X DELETE http://127.0.0.1:8080/api/v1/traces
```
### 定时任务管理

bash
```
# 获取定时任务列表
curl "http://127.0.0.1:8080/api/v1/scheduled-tasks?sessionId=SESSION_ID"

# 创建定时任务（每 5 分钟执行）
curl -X POST http://127.0.0.1:8080/api/v1/scheduled-tasks \
  -H "Content-Type: application/json" \
  -d '{"cron": "*/5 * * * *", "prompt": "检查构建状态", "sessionId": "SESSION_ID"}'

# 创建一次性任务（每周一上午 9 点）
curl -X POST http://127.0.0.1:8080/api/v1/scheduled-tasks \
  -H "Content-Type: application/json" \
  -d '{"cron": "0 9 * * 1", "prompt": "生成周报", "recurring": false, "sessionId": "SESSION_ID"}'

# 创建持久化任务（重启后仍保留）
curl -X POST http://127.0.0.1:8080/api/v1/scheduled-tasks \
  -H "Content-Type: application/json" \
  -d '{"cron": "0 0 * * *", "prompt": "每日清理", "durable": true, "sessionId": "SESSION_ID"}'

# 删除定时任务
curl -X DELETE "http://127.0.0.1:8080/api/v1/scheduled-tasks/TASK_ID?sessionId=SESSION_ID"
```
## 错误码

| 错误码 | HTTP 状态 | 说明 |
| --- | --- | --- |
| `AUTH_REQUIRED` | 401 | 需要认证 |
| `AUTH_INVALID` | 401 | 认证无效 |
| `AUTH_RATE_LIMITED` | 429 | 登录尝试过多 |
| `NOT_FOUND` | 404 | 资源不存在 |
| `BAD_REQUEST` | 400 | 请求参数错误 |
| `RATE_LIMITED` | 429 | 请求频率过高 |
| `INTERNAL_ERROR` | 500 | 服务器内部错误 |
| `SESSION_NOT_FOUND` | 404 | 会话不存在 |
| `JOB_NOT_FOUND` | 404 | Jobs 实例不存在 |
| `SESSION_DELETE_CURRENT` | 400 | 不能删除当前会话 |
| `TERMINAL_NOT_FOUND` | 404 | PTY 不存在 |
| `PROCESS_NOT_FOUND` | 404 | 进程不存在 |
| `PATH_REQUIRED` | 400 | 缺少 path 参数 |
| `PATH_NOT_DIRECTORY` | 400 | 路径不是目录 |
| `INSUFFICIENT_STORAGE` | 507 | 磁盘空间不足 |
| `RUN_NOT_FOUND` | 404 | 执行不存在 |
| `PLATFORM_UNSUPPORTED` | 400 | 不支持的 Webhook 平台 |
| `SIGNATURE_INVALID` | 403 | 签名验证失败 |