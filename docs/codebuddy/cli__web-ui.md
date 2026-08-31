# Web UI

CodeBuddy Code 提供内置的 Web UI，在浏览器中提供完整的交互界面。当您以 serve 模式启动或开启远程控制时，Web UI 自动可用。

## 概述

Web UI 提供与终端界面相同的核心能力，并针对浏览器进行了可视化布局优化：

- **对话**：发送消息、查看对话、实时监控工具执行
- **终端**：内嵌终端，支持分屏布局（最多 4 个面板）
- **Workers**：管理 CLI Worker 进程和 Daemon 守护进程
- **日志**：独立日志查看器，支持多种日志类型和关键词搜索
- **远程控制**：连接微信和企业微信渠道
- **监控**：系统资源指标和各 Worker 进程级内存/运行时间指标
- **任务**：浏览任务模版并创建定时任务
- **插件**：管理插件安装和插件市场
- **设置**：配置主题、语言、模型、权限模式和主 Agent（标准 / PTC / 极简 / 创造）
- **文档**：浏览 CLI 文档，支持全文搜索
- **API 文档**：查看交互式 Swagger UI，方便 HTTP API 探索

## 访问 Web UI

### 方式一：Serve 模式

使用 `--serve` 参数启动 CodeBuddy Code：

bash
```
codebuddy --serve --port 7890
# 新对话盖章进程默认（不写 settings.json）：
codebuddy --serve --agent ptc --permission-mode bypassPermissions
```
然后在浏览器中打开：

```
http://127.0.0.1:7890
```
标准模式请显式传 `--agent cli`，不要指望 `lastUsed` 或默认 chip。`minimal` 不要配 `--permission-mode plan`。

### 方式二：远程控制

在已有的 CodeBuddy Code 会话中启动 Gateway：

```
/gateway
```
终端会显示二维码和 URL。用手机扫码或在浏览器中打开 URL。详见[远程控制](./remote-control)文档。

## Serve 启动：模式与权限

进程默认，**不写 settings**。`--agent` 压过 chip `lastUsed`，以及续接会话上的 leftover 四模式 / `cli` 站立键。不抢自定义 `@agent`。

bash
```
codebuddy --serve --agent <模式> --permission-mode <权限>
```
本机调试常见写法（`--auth none` 只给本机 / CI，不要对公网这么开）：

bash
```
codebuddy --serve --agent ptc --permission-mode bypassPermissions --auth none --open
```
### `--agent` 四种 shipped

| 值 | 界面 | 对话层 | 说明 |
| --- | --- | --- | --- |
| `cli` | 标准模式 | 原生全工具（Bash / Read / Grep…） | **什么都不加**时的默认；要标准模式请显式传它 |
| `ptc` | PTC | 只有 `REPL`，沙箱里全量 | Code Mode |
| `minimal` | 极简 | 只有 `REPL`，沙箱 Bash / Edit / Skill（无 MCP） | 无 Read / Glob / MCP；prompt 与注入不教这些工具 |
| `create` | 创造模式 | 与标准同一套工具 | 多写自定义 agent 的提示 |

也可以是自定义 id（`.codebuddy/agents/<name>.md` 的 `name`）。

`multitask` **不是** `--serve` / Web UI 的启动值：入口守卫会拒，进程非 0。协调器在会话内用 `/multitask`（交互 TUI）或 [`session/set_multitask`](./acp#multitask-协调器sessionset_multitask)（ACP）。

### `--permission-mode`

help 写的是前 6 个；运行时还认 `fullAccess`。

| 值 | 含义 |
| --- | --- |
| `default` | 默认：按规则问 |
| `acceptEdits` | 编辑自动过，其它仍问 |
| `bypassPermissions` | 跳过权限确认 |
| `plan` | Plan 模式。**`minimal` \+ `plan` 会 400**，不要这么配 |
| `dontAsk` | 不问，该拒就拒 |
| `auto` | 自动分类 |
| `fullAccess` | 运行时允许，help 里没列；语义接近 `bypassPermissions` |

相关（一般不用）：

text
```
--permission-mode-before-plan <mode>   退出 plan 回到哪个权限
--subagent-permission-mode <mode>      子代理/队友权限，不继承主会话
```
完整语义见 [权限模式](./permission-modes)。

### 四模式 × 常用权限

bash
```
# 标准 + 默认权限
codebuddy --serve --agent cli --permission-mode default --auth none --open

# 标准 + 跳过权限
codebuddy --serve --agent cli --permission-mode bypassPermissions --auth none --open

# PTC + 跳过权限
codebuddy --serve --agent ptc --permission-mode bypassPermissions --auth none --open

# PTC + 默认权限
codebuddy --serve --agent ptc --permission-mode default --auth none --open

# 极简 + 跳过权限（不要加 --permission-mode plan）
codebuddy --serve --agent minimal --permission-mode bypassPermissions --auth none --open

# 创造 + 跳过权限
codebuddy --serve --agent create --permission-mode bypassPermissions --auth none --open
```
### 同条上的其它开关

| 旗标 | 取值 | 说明 |
| --- | --- | --- |
| `--serve` | 无参 | HTTP \+ Web UI |
| `--open` | 无参 | ACP 起来后再开浏览器 |
| `--auth` | `password`（默认）/ `none` | 本机调试用 `none` |
| `--host` | 默认 `127.0.0.1` | 绑全接口再显式 `--host 0.0.0.0` |
| `--port` | 数字 | 不写则自动选 |

## 认证方式

Web UI 支持两种认证模式：

| 模式 | 设置 | 说明 |
| --- | --- | --- |
| 密码认证（默认） | `--auth password` / `CODEBUDDY_GATEWAY_AUTH=password` | `--serve` 的默认行为，启动时终端打印密码和带密码的可点链接 |
| 免认证 | `--auth none` / `CODEBUDDY_GATEWAY_AUTH=none` | 显式关闭，启动时打印警告。同机任意进程可经此服务执行命令、读写文件，仅建议在隔离环境或 CI 中使用 |

认证方式（以下任一方式均可）：

- **URL 参数**：`?password=xxx` — 打开 Web UI 首页时自动登录并下发 Cookie（**仅首页有效，对 `/api/v1/*` 端点无效**）
- **登录页面**：输入终端显示的密码
- **Bearer Token**：`Authorization: Bearer <password>`，用于 API 访问
- **Cookie**：`gateway_session`，浏览器登录后自动携带，有效期 30 天

在 `~/.codebuddy/settings.json` 中配置：

json
```
{
  "gateway.auth": "none"
}
```
## 功能详解

### 对话视图

默认视图，用于与 Agent 交互。核心功能：

- **富文本消息渲染**：Markdown、语法高亮代码块、表格、图片
- **工具执行展示**：内联查看工具调用、参数和结果
- **权限管理**：在浏览器中直接批准或拒绝工具权限
- **问答面板**：回答 Agent 的多选问题
- **任务进度**：实时监控后台任务和 Team 进度
- **会话管理**：新建对话、浏览历史、切换会话
- **工作目录管理**：添加/移除附加工作目录，扩展 Agent 的文件访问范围。工作目录与智能体模式统一显示在输入卡片顶部；新会话可选择，会话开始后显示只读状态。
- **主 Agent**：空白会话可切换 `cli` / `ptc` / `minimal` / `create` 或自定义智能体。chip 选择写入 `codebuddy.mainAgent.lastUsed`，不改 `default`。进程 `--agent` 压过 lastUsed。已有历史的会话锁定当前 Agent。
- **右侧工作台**：资源管理器、文件搜索、源代码管理、文件编辑和终端使用独立工具标签，可一键全屏并拖拽调整宽度；窄面板会自动切换文件树与编辑区布局，并隐藏编辑器 minimap。对话中的文件路径支持跳转到指定行或行号范围；普通点击 URL 会在工作台安全预览，`Cmd/Ctrl` 点击会在浏览器新标签打开；本地 HTML 文件可在源码与安全预览之间切换。编辑器、预览和文件树可以把当前文件下载到本地。
- **目标**：输入 `/goal` 或从输入框进入目标模式，可设置进行中目标。暂停会立刻卸掉续跑并掐当前回合，目标条保留为已暂停；继续后按同一条件重新启动。垃圾桶清除目标并收起目标条。

### 终端视图

基于 xterm.js 的内嵌终端：

- **分屏布局**：支持水平和垂直分屏，最多 4 个面板
- **独立会话**：每个面板有独立的 PTY 会话
- **持久连接**：终端会话在页面刷新后保持
- **自适应调整**：窗口大小变化时面板自动调整

### 文档视图

在 Web UI 中直接浏览 CLI 文档：

- **全文搜索**：基于 MiniSearch 搜索所有文档
- **多语言**：自动跟随 UI 语言设置（中文/英文）
- **目录导航**：根据文档标题自动生成，带滚动追踪
- **内部跳转**：文档链接在查看器内导航（SPA 模式）
- **API 文档**：快速链接到 `/api/docs` 的交互式 Swagger UI

### 实例管理

管理多个 CodeBuddy Code 实例：

- **实例列表**：查看所有运行中的实例及其工作目录和状态
- **快速切换**：一键切换实例
- **手动添加**：通过 URL 添加远程实例
- **隧道支持**：通过 Cloudflare Tunnel 访问实例

### 后台会话

Web UI 的 Agent View 直接使用 `/api/v1/jobs` 管理后台 agent；外部 worker 由独立的 Workers 视图管理，不混入 jobs 列表。

- **项目列表**：按工作目录分组，支持置顶、项目分组、搜索和完成通知；运行中的 job 用动态指示，等待输入的 job 显示需要输入提示。
- **派发新会话**：可选择主 Agent（与对话栏同一份目录：内置四种模式 \+ 自定义）、模型、思考强度、启动权限、启动目录、自定义名称和 shell 模式，并支持图片与文件附件。请求体字段：`agent`、`model`、`effort`、`permissionMode`、`sourceSessionId`（继承受限上下文）、`bgIsolation`（`none` / `worktree`，省略时跟随全局设置）。`GET /api/v1/jobs/dispatch-context` 返回 `defaultAgentName`、`agents`、`permissionMode`（进程 `--permission-mode`）。`minimal` 不能与 `permissionMode=plan` 同用。
- **右键操作**：停止、重启、置顶/取消置顶、重命名、移出项目、复制会话 ID、复制工作目录和删除。
- **会话恢复**：重启 job 会恢复其 session；浏览器重新打开时，主 Web UI 使用持久化的 session ID 加载历史，失败后才回退到 continue 选择。打开已有子智能体时保持当前画面和输入框，不整页刷新；历史回放完成前继续显示上一屏。地址栏带会话 ID 时，短暂的 load 失败会重试，不会另开新会话。子智能体运行中改模型会记在该实例上，重启后沿用，不改主对话默认模型。
- **内嵌对话**：父网关同源 iframe 池化打开后台 agent。页面由父网关出 SPA，ACP / 目标 / internal API 经 `/api/v1/jobs/:id/frame/` 反代到该 job 的 loopback；storage、auth、jobs 仍由父网关处理。iframe `src` 不携带网关密码。各页输入框独立；恢复时只在卸帧瞬间搬草稿，不共用一份输入。
- **频道与私信**：频道回执按频道认，不画成「消息来自 user」；1:1 输入框 `@` 只做补全。用户在频道发言后，被叫醒的人头像马上显示在忙；默认 Agent 不进花名册、不吃 `@所有人` 未读。
- **对话数据**：`GET /api/v1/jobs/:id/transcript` 一次性返回最近最多 1000 行 ACP replay updates；`GET /api/v1/jobs/:id/stream` 先回放 transcript 尾部，再通过 SSE 尾随新输出。
- **生命周期**：支持 reply、stop、respawn 和 delete。删除可能因前台持有或 worktree 守卫返回 `{ deleted: false, reason }`，UI 会保留该 job 并提示原因。
- **实时更新**：列表通过 `/api/v1/jobs/events` 接收 `snapshot`、`added`、`changed`、`removed` 和 `keepalive` 事件，无需手动刷新。

完整端点、字段、错误码和 curl 示例见 [HTTP API — Jobs](./http-api)。

### 设置

- **主题**：浅色、深色或跟随系统（自动检测）
- **语言**：中文、英文或跟随系统（自动检测）
- **模型**：从可用选项中选择 AI 模型
- **权限模式**：默认、接受编辑、跳过权限或规划模式
- **主 Agent**：总闸 `codebuddy.mainAgent.enabled`（缺省开）；「允许未声明宿主」`allowUnopted`（缺省关，WorkBuddy 保持原生 `cli`）；管理页可设 `default`、用 AI 创建自定义智能体。chip 选择只写 `lastUsed`。

## API 文档

HTTP 服务运行时，可在以下地址访问交互式 API 探索器：

```
http://127.0.0.1:{PORT}/api/docs
```
Swagger UI 提供以下功能：

- 浏览所有可用的 REST API 端点
- 查看请求/响应 Schema
- 直接在浏览器中测试 API 调用
- 在 `/api/openapi.json` 下载 OpenAPI 3\.1 规范

完整的 API 参考请见 [HTTP API 文档](./http-api)。

## 移动端支持

Web UI 完全响应式，支持移动设备：

- **侧边栏**：小屏幕上折叠为滑出式抽屉
- **PWA 支持**：添加到主屏幕获得类原生应用体验
- **触控优化**：所有交互针对触摸操作优化
- **扫码访问**：终端扫码即可在手机上打开

## 快捷键

| 快捷键 | 操作 |
| --- | --- |
| `Enter` | 发送消息 |
| `Shift+Enter` | 输入换行 |
| `Escape` | 停止运行中的 Agent |

## 技术细节

- **框架**：React 18 \+ Zustand 状态管理
- **通信**：ACP 协议，基于 HTTP/SSE（非 WebSocket）
- **样式**：Tailwind CSS \+ CSS 变量主题
- **终端**：xterm.js \+ fit addon
- **搜索**：MiniSearch 客户端全文搜索
- **Markdown**：react\-markdown \+ remark\-gfm \+ 语法高亮

## 相关文档

- [远程控制](./remote-control) — 通过 Gateway 和 Tunnel 启动 Web UI
- [HTTP API](./http-api) — 完整的 REST API 文档
- [ACP 协议](./acp) — IDE 集成的 Agent Client Protocol
- [权限模式](./permission-modes) — `--permission-mode` 语义
- [CLI 参考](./cli-reference) — `--agent` / `--serve` 参数
- [设置](./settings) — 配置选项