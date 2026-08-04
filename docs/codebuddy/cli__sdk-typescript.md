# TypeScript SDK 参考

> **版本要求**：本文档针对 CodeBuddy Agent SDK v0\.1\.0 及以上版本。

本文档提供 TypeScript SDK 的完整 API 参考。有关快速入门和使用示例，请参阅 [SDK 概览](./sdk)。

## Requirements

| 依赖 | 版本要求 |
| --- | --- |
| Node.js | \>\= 18\.0\.0 |
| TypeScript | \>\= 5\.0\.0（推荐） |

**运行时支持**：

- Node.js（推荐）
- Bun
- Deno

## Installation

bash
```
npm install @tencent-ai/agent-sdk
```
或使用其他包管理器：

bash
```
yarn add @tencent-ai/agent-sdk
pnpm add @tencent-ai/agent-sdk
```
### 环境变量

| 变量名 | 说明 | 必需 |
| --- | --- | --- |
| `CODEBUDDY_CODE_PATH` | CodeBuddy CLI 可执行文件路径 | 可选 |

### 认证配置

SDK 支持使用已有登录凭据、API Key 或 OAuth Client Credentials 认证，详见 [SDK 概览 \- 认证配置](./sdk#认证配置)。

## Functions

### query()

主要 API 入口，创建一个查询并返回消息流。

typescript
```
function query(params: {
  prompt: string | AsyncIterable<UserMessage>;
  options?: Options;
}): Query;
```
**参数**：

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `prompt` | `string | AsyncIterable<UserMessage>` | 查询提示词或用户消息流 |
| `options` | `Options` | 配置选项（可选） |

**返回值**：`Query` \- 扩展了 `AsyncGenerator<Message, void>` 的接口

### Query 接口

typescript
```
interface Query extends AsyncGenerator<Message, void> {
  // 中断当前执行
  interrupt(): Promise<void>;

  // 动态修改权限模式
  setPermissionMode(mode: PermissionMode): Promise<void>;

  // 动态修改模型
  setModel(model?: string): Promise<void>;

  // 设置最大思考 token 数
  setMaxThinkingTokens(tokens: number | null): Promise<void>;

  // 获取可用权限模式列表
  getAvailableModes(): Promise<ModeInfo[]>;

  // 获取可用模型列表
  getAvailableModels(): Promise<ModelInfo[]>;

  // 获取支持的斜杠命令
  supportedCommands(): Promise<SlashCommand[]>;

  // 获取支持的模型列表
  supportedModels(): Promise<ModelInfo[]>;

  // 获取 MCP 服务器状态
  mcpServerStatus(): Promise<McpServerStatus[]>;

  // 获取账户信息
  accountInfo(): Promise<AccountInfo>;

  // 流式输入用户消息
  streamInput(stream: AsyncIterable<UserMessage>): Promise<void>;
}
```
### Constants

typescript
```
// 所有支持的 Hook 事件
const HOOK_EVENTS: readonly [
  'PreToolUse',
  'PostToolUse',
  'PostToolUseFailure',
  'Notification',
  'UserPromptSubmit',
  'SessionStart',
  'SessionEnd',
  'Stop',
  'SubagentStart',
  'SubagentStop',
  'PreCompact',
  'PermissionRequest',
  'WorktreeCreate',
  'WorktreeRemove'
];

// 所有退出原因
const EXIT_REASONS: readonly [
  'user_cancelled',
  'tool_error',
  'max_turns',
  'max_budget_usd',
  'completed',
  'interrupted',
  'hook_blocked'
];
```
### Errors

typescript
```
class AbortError extends Error {
  // 当操作被中止时抛出
}
```
## Unstable V2 API

> **警告**：以下 API 处于实验阶段，接口可能在未来版本中变更。

### unstable\_v2\_createSession()

创建新的交互式会话。

typescript
```
function unstable_v2_createSession(options: SessionOptions): Session;
```
### unstable\_v2\_resumeSession()

恢复现有会话。

typescript
```
function unstable_v2_resumeSession(
  sessionId: string,
  options: SessionOptions
): Session;
```
### unstable\_v2\_prompt()

单次查询便捷函数。

typescript
```
function unstable_v2_prompt(
  message: string,
  options: SessionOptions
): Promise<Message[]>;
```
### unstable\_v2\_authenticate()

发起交互式登录流程，支持多环境认证（海外版、国内版等）。

typescript
```
function unstable_v2_authenticate(options: AuthenticateOptions): Promise<AuthenticateResponse>;
```
**参数**：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `onAuthUrl` | `(authState: AuthState) => Promise<void>` | 认证 URL 回调，用于打开浏览器或显示链接 |
| `environment` | `'external' | 'internal' | 'ioa' | 'cloudhosted'` | 预定义环境（与 endpoint 二选一） |
| `endpoint` | `string` | 自定义 endpoint URL（用于 selfhosted，与 environment 二选一） |
| `methodId` | `string` | 认证方法 ID，默认 'external' |
| `timeout` | `number` | 超时时间（毫秒），默认 300000 |
| `pathToCodebuddyCode` | `string` | CLI 可执行文件路径（可选） |
| `env` | `Record<string, string>` | 环境变量（可选） |

**返回值**：`Promise<AuthenticateResponse>`

- `userinfo` \- 用户信息对象，包含 userId、userName、userNickname、token 等字段

**示例**：

typescript
```
import { unstable_v2_authenticate } from '@tencent-ai/agent-sdk';
import open from 'open';

// 海外版登录
const result = await unstable_v2_authenticate({
  environment: 'external',
  onAuthUrl: async (authState) => {
    console.log('请登录:', authState.authUrl);
    await open(authState.authUrl);
  }
});

console.log('登录成功:', result.userinfo.userName);

// 私有化部署登录
const result2 = await unstable_v2_authenticate({
  endpoint: 'https://your-company.com',
  onAuthUrl: async (authState) => {
    console.log('请登录:', authState.authUrl);
    await open(authState.authUrl);
  }
});
```
**行为说明**：

- 如果已有有效 token，直接返回用户信息，不会触发登录流程
- 否则通过 `onAuthUrl` 回调通知用户打开登录链接
- 登录成功后 token 会被缓存，下次调用自动复用

### unstable\_v2\_logout()

登出并清除缓存的认证 token，下次调用 `authenticate()` 将重新登录。

typescript
```
function unstable_v2_logout(options?: LogoutOptions): Promise<void>;
```
**参数**：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `environment` | `'external' | 'internal' | 'ioa' | 'cloudhosted'` | 预定义环境（与 endpoint 二选一） |
| `endpoint` | `string` | 自定义 endpoint URL（与 environment 二选一） |
| `pathToCodebuddyCode` | `string` | CLI 可执行文件路径（可选） |
| `env` | `Record<string, string>` | 环境变量（可选） |

**示例**：

typescript
```
import { unstable_v2_authenticate, unstable_v2_logout } from '@tencent-ai/agent-sdk';

// 登录
const result = await unstable_v2_authenticate({
  environment: 'external',
  onAuthUrl: (authState) => console.log('Login:', authState.authUrl),
});

// 登出
await unstable_v2_logout({ environment: 'external' });

// 以不同用户重新登录
const newUser = await unstable_v2_authenticate({
  environment: 'external',
  onAuthUrl: (authState) => console.log('Login:', authState.authUrl),
});
```
### Session 接口

typescript
```
interface Session {
  // 会话 ID（初始化后可用）
  readonly sessionId: string;

  // 发送消息
  send(message: string | UserMessage): Promise<void>;

  // 获取响应流
  stream(): AsyncGenerator<Message, void>;

  // 关闭会话
  close(): void;

  // 异步释放
  [Symbol.asyncDispose](): Promise<void>;
}
```
### SessionOptions

typescript
```
type SessionOptions = {
  model: string;
  pathToCodebuddyCode?: string;
  executable?: 'node' | 'bun';
  executableArgs?: string[];
  env?: Record<string, string | undefined>;
  canUseTool?: CanUseTool;
};
```
## Types

### Options

完整配置选项：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `abortController` | `AbortController` | 用于取消请求 |
| `executable` | `'bun' | 'deno' | 'node'` | 运行时 |
| `executableArgs` | `string[]` | 运行时参数 |
| `pathToCodebuddyCode` | `string` | CLI 路径 |
| `cwd` | `string` | 工作目录 |
| `additionalDirectories` | `string[]` | 额外的目录 |
| `env` | `Record<string, string | undefined>` | 环境变量 |
| `model` | `string` | 指定模型 |
| `fallbackModel` | `string` | 备用模型 |
| `maxThinkingTokens` | `number` | 最大思考 token 数（已废弃，请使用 `thinking`） |
| `thinking` | `ThinkingConfig` | 思考模式配置：`{ type: 'adaptive' }`、`{ type: 'enabled', budgetTokens: N }` 或 `{ type: 'disabled' }` |
| `effort` | `'low' | 'medium' | 'high' | 'xhigh'` | 模型推理努力程度 |
| `allowedTools` | `string[]` | 允许的工具白名单 |
| `disallowedTools` | `string[]` | 禁止的工具黑名单 |
| `canUseTool` | `CanUseTool` | 权限回调函数 |
| `permissionMode` | `PermissionMode` | 权限模式 |
| `allowDangerouslySkipPermissions` | `boolean` | 允许跳过权限 |
| `permissionPromptToolName` | `string` | 权限提示工具名 |
| `continue` | `boolean` | 继续最近的会话 |
| `resume` | `string` | 要恢复的会话 ID |
| `resumeSessionAt` | `string` | 恢复到特定消息位置 |
| `persistSession` | `boolean` | 持久化会话 |
| `forkSession` | `boolean` | 分叉会话 |
| `agents` | `Record<string, AgentDefinition>` | 自定义 Agent |
| `hooks` | `Partial<Record<HookEvent, HookCallbackMatcher[]>>` | Hook 配置 |
| `outputFormat` | `OutputFormat` | 输出格式 |
| `systemPrompt` | `string | { append: string }` | 系统提示词 |
| `includePartialMessages` | `boolean` | 包含部分消息 |
| `maxTurns` | `number` | 最大对话轮数 |
| `mcpServers` | `Record<string, McpServerConfig>` | MCP 服务器配置 |
| `strictMcpConfig` | `boolean` | 严格 MCP 配置 |
| `sandbox` | `SandboxSettings` | 沙箱设置 |
| `settingSources` | `SettingSource[]` | 配置源，控制加载哪些文件系统配置。默认不加载任何配置 |

### SettingSource

控制 SDK 从哪些文件系统位置加载配置。

typescript
```
type SettingSource = 'user' | 'project' | 'local';
```

| 值 | 说明 | 位置 |
| --- | --- | --- |
| `'user'` | 全局用户设置 | `~/.codebuddy/settings.json` |
| `'project'` | 项目共享设置 | `.codebuddy/settings.json` |
| `'local'` | 项目本地设置 | `.codebuddy/settings.local.json` |

**默认行为**：当 `settingSources` 未指定时，SDK **不加载任何文件系统配置**。这提供了完全干净的运行环境。

typescript
```
// 默认：不加载任何配置（干净环境）
const q = query({ prompt: '...' });

// 加载项目配置
const q = query({
  prompt: '...',
  options: { settingSources: ['project'] }
});

// 加载所有配置（类似 CLI 行为）
const q = query({
  prompt: '...',
  options: { settingSources: ['user', 'project', 'local'] }
});
```
### PermissionMode

typescript
```
type PermissionMode =
  | 'default'           // 默认模式，所有操作需确认
  | 'acceptEdits'       // 自动批准文件编辑
  | 'bypassPermissions' // 跳过所有权限检查
  | 'plan'              // 规划模式，仅允许读取
```
### PermissionResult

typescript
```
type PermissionResult =
  | {
      behavior: 'allow';
      updatedInput: Record<string, unknown>;
      updatedPermissions?: PermissionUpdate[];
      toolUseID?: string;
    }
  | {
      behavior: 'deny';
      message: string;
      interrupt?: boolean;
      toolUseID?: string;
    };
```
### CanUseTool

typescript
```
type CanUseTool = (
  toolName: string,
  input: Record<string, unknown>,
  options: CanUseToolOptions
) => Promise<PermissionResult>;

type CanUseToolOptions = {
  signal: AbortSignal;
  suggestions?: PermissionUpdate[];
  blockedPath?: string;
  decisionReason?: string;
  toolUseID: string;
  agentID?: string;
};
```
### AgentDefinition

typescript
```
type AgentDefinition = {
  description: string;          // Agent 描述
  prompt: string;               // 系统提示词
  tools?: string[];             // 允许的工具
  disallowedTools?: string[];   // 禁止的工具
  model?: string;               // 使用的模型
};
```
### ModeInfo

typescript
```
interface ModeInfo {
  id: string;           // 模式 ID
  name: string;         // 显示名称
  description: string;  // 模式说明
}
```
### ModelInfo

typescript
```
interface ModelInfo {
  modelId: string;       // 模型 ID
  name: string;          // 显示名称
  description?: string;  // 模型说明
}
```
### McpServerConfig

typescript
```
// Stdio 类型
type McpStdioServerConfig = {
  type?: 'stdio';
  command: string;
  args?: string[];
  env?: Record<string, string>;
};

// SSE 类型
type McpSSEServerConfig = {
  type: 'sse';
  url: string;
  headers?: Record<string, string>;
};

// HTTP 类型
type McpHttpServerConfig = {
  type: 'http';
  url: string;
  headers?: Record<string, string>;
};

type McpServerConfig =
  | McpStdioServerConfig
  | McpSSEServerConfig
  | McpHttpServerConfig;
```
### HookEvent

typescript
```
type HookEvent =
  | 'PreToolUse'
  | 'PostToolUse'
  | 'PostToolUseFailure'
  | 'Notification'
  | 'UserPromptSubmit'
  | 'SessionStart'
  | 'SessionEnd'
  | 'Stop'
  | 'SubagentStart'
  | 'SubagentStop'
  | 'PreCompact'
  | 'PermissionRequest'
  | 'WorktreeCreate'
  | 'WorktreeRemove';
```
### HookCallback

typescript
```
type HookCallback = (
  input: HookInput,
  toolUseID: string | undefined,
  options: { signal: AbortSignal }
) => Promise<HookJSONOutput>;

interface HookCallbackMatcher {
  matcher?: string;        // 匹配模式（支持正则）
  hooks: HookCallback[];   // 回调函数列表
  timeout?: number;        // 超时时间（毫秒）
}
```
### HookJSONOutput

typescript
```
// 同步输出
type SyncHookJSONOutput = {
  continue?: boolean;
  suppressOutput?: boolean;
  stopReason?: string;
  decision?: 'approve' | 'block';
  systemMessage?: string;
  reason?: string;
  hookSpecificOutput?: Record<string, unknown>;
};

// 异步输出
type AsyncHookJSONOutput = {
  async: true;
  asyncTimeout?: number;
};

type HookJSONOutput = SyncHookJSONOutput | AsyncHookJSONOutput;
```
## Message Types

### Message

所有消息类型的联合：

typescript
```
type Message =
  | SystemMessage
  | UserMessage
  | AssistantMessage
  | PartialAssistantMessage
  | ResultMessage
  | CompactBoundaryMessage
  | StatusMessage
  | TaskStartedMessage
  | TaskNotificationMessage
  | ToolProgressMessage;
```
### SystemMessage

typescript
```
type SystemMessage = {
  type: 'system';
  subtype: 'init';
  uuid: string;
  session_id: string;
  apiKeySource?: string;
  cwd?: string;
  tools: string[];
  mcp_servers?: Array<{ name: string; status: string }>;
  model: string;
  permissionMode: PermissionMode;
  slash_commands?: string[];
  codebuddy_code_version?: string;
  skills?: string[];
  plugins?: Array<{ name: string; path: string }>;
};
```
### TaskStartedMessage

后台任务（Bash / PowerShell / Workflow / Agent，`run_in_background: true`）进入运行态时发出的 `system` 事件。并发任务靠 `task_id` 区分，`tool_use_id` 关联回发起该任务的 tool\_use。

typescript
```
interface TaskStartedMessage {
  type: 'system';
  subtype: 'task_started';
  task_id: string;
  tool_use_id?: string;
  description: string;
  task_type?: string; // "Bash" / "PowerShell" / "Workflow" / "Agent"
  uuid: string;
  session_id: string;
}
```
### TaskUsage

`task_progress` / `task_notification` 携带的用量统计（对齐 Claude Code 的 `TaskUsage`）。sub\-agent（`task_type: 'Agent'`）后台任务有值；后台 shell（Bash/PowerShell）任务通常省略 `usage`。

typescript
```
interface TaskUsage {
  total_tokens: number;
  tool_uses: number;
  duration_ms: number;
}
```
### TaskProgressMessage

后台任务进度事件。**事件驱动**（非定时）：每完成一次 tool\_use（`usage.tool_uses` 增长）推一条，携带累计 `usage` 与最近工具名 `last_tool_name`。后台 shell 任务不发 progress（对齐 CC——只有 sub\-agent/workflow 类任务发 progress）。

typescript
```
interface TaskProgressMessage {
  type: 'system';
  subtype: 'task_progress';
  task_id: string;
  tool_use_id?: string;
  description: string;
  usage: TaskUsage;
  last_tool_name?: string;
  uuid: string;
  session_id: string;
}
```
### TaskUpdatedMessage

后台任务状态变迁事件。`patch` 携带本次变更的字段（至少 `status`，终态补 `end_time`）。

> 生命周期提示：后台任务的终态**有时只来 `task_updated`（`patch.status` 为终态）而没有配套的 `task_notification`**。跟踪"活跃任务"的消费方应对 `TaskNotificationMessage` 与 `TaskUpdatedMessage` 二者的终态 status（`completed` / `failed` / `stopped` / `killed`）一视同仁地清理。

typescript
```
interface TaskUpdatedMessage {
  type: 'system';
  subtype: 'task_updated';
  task_id: string;
  patch: Record<string, unknown>; // e.g. { status, end_time }
  status?: 'pending' | 'running' | 'paused' | 'completed' | 'failed' | 'killed';
  uuid?: string;
  session_id?: string;
}
```
### TaskNotificationMessage

后台任务完成 / 失败 / 被停止时发出。在 stdio `stream-json` 长连接模式下，任务若在触发它的那轮 `result` 之后才完成，该消息会被主动推回同一输出流——消费方需**持续读取**才能收到。据 `task_id` 路由，`output_file` 指向落盘的完整输出。`usage` 在 sub\-agent 任务上携带，shell 任务省略。

> ⚠️ `query()` 在首个 `ResultMessage` 处 `break` 并关闭子进程，**会错过**在该 `result` 之后才回推的后台完成事件。要接收跨轮完成事件，请用 V2 Session（`unstable_v2_createSession`）并在 `send()` 后反复调用 `stream()` 持续消费后台任务完成触发的后续轮次（对应 Python SDK 的 `receive_messages()` 持续读语义）。
> 
> **`query()` 已自动禁用后台任务**：由于上述结构性限制，SDK 在 `query()` 路径下会自动注入 `CODEBUDDY_CODE_DISABLE_BACKGROUND_TASKS=1`（Bash / PowerShell / Agent 的 `run_in_background` 被隐藏/降级为前台），避免后台任务被 `query()` 悄悄丢弃。若你确有理由要在 `query()` 下保留后台任务，显式在 `options.env` 或进程环境里设置该变量（任意值，包括 `0`）即可覆盖此默认。V2 Session 路径不受影响。

typescript
```
interface TaskNotificationMessage {
  type: 'system';
  subtype: 'task_notification';
  task_id: string;
  tool_use_id?: string;
  status: 'completed' | 'failed' | 'stopped';
  summary: string;
  output_file?: string;
  output_stderr_file?: string;
  usage?: TaskUsage;
  uuid: string;
  session_id: string;
}
```
用法示例（并发后台任务，靠 `task_id` 区分并在整体完成后接收通知）：

typescript
```
import { unstable_v2_createSession, type Message } from '@tencent-ai/agent-sdk';

const session = unstable_v2_createSession({ permissionMode: 'bypassPermissions' });
const started = new Map<string, Message>();
const notified = new Map<string, Message>();

await session.send('并行跑两个后台命令，完成后告诉我结果');

// stream() 在每轮 result 处返回（但不关闭子进程）。反复调用它即可继续消费由后台
// 任务完成触发的后续 drain-run 轮次，直到集齐所有 task_notification。
while (notified.size < 2) {
  let sawResult = false;
  for await (const message of session.stream()) {
    if (message.type === 'system' && message.subtype === 'task_started') {
      started.set(message.task_id, message);
      console.log('started', message.task_id, message.description);
    } else if (message.type === 'system' && message.subtype === 'task_notification') {
      notified.set(message.task_id, message);
      console.log('done', message.task_id, message.status, message.output_file);
    } else if (message.type === 'result') {
      sawResult = true;
    }
  }
  if (!sawResult) break; // 子进程已关闭，避免空转
}

session.close();
```
### UserMessage

typescript
```
type UserMessage = {
  type: 'user';
  uuid?: string;
  session_id: string;
  message: {
    role: 'user';
    content: string | ContentBlock[];
  };
  parent_tool_use_id: string | null;
  isSynthetic?: boolean;
  tool_use_result?: unknown;
};
```
### AssistantMessage

typescript
```
type AssistantMessage = {
  type: 'assistant';
  uuid: string;
  session_id: string;
  message: {
    id: string;
    type: 'message';
    role: 'assistant';
    model: string;
    content: ContentBlock[];
    stop_reason: StopReason | null;
    stop_sequence: string | null;
    usage: Usage;
  };
  parent_tool_use_id: string | null;
  error?: string;
};
```
### ResultMessage

typescript
```
type ResultMessage =
  | {
      type: 'result';
      subtype: 'success';
      uuid: string;
      session_id: string;
      duration_ms: number;
      duration_api_ms: number;
      is_error: boolean;
      num_turns: number;
      result: string;
      total_cost_usd: number;
      usage: Usage;
      permission_denials: PermissionDenial[];
      structured_output?: unknown;
    }
  | {
      type: 'result';
      subtype: 'error_during_execution' | 'error_max_turns' | 'error_max_budget_usd';
      uuid: string;
      session_id: string;
      duration_ms: number;
      duration_api_ms: number;
      is_error: boolean;
      num_turns: number;
      total_cost_usd: number;
      usage: Usage;
      permission_denials: PermissionDenial[];
      errors?: string[];
      /**
       * Structured error info aligned with `errors[]` by index.
       * - Length always equals `errors.length` when present
       * - `errors_info[i]` describes `errors[i]`; `null` if no structured dimension could be extracted
       * - Entire field is omitted when all entries are null (backward compatible: legacy consumers reading only `errors` are unaffected)
       * - `category` values align with ACP error categories: `network` / `quota` / `auth` / `model_service` / `cancelled` / `internal`
       */
      errors_info?: Array<
        | {
            /** HTTP status code (e.g. 502, 429, 401) */
            status?: number;
            /** SDK/business error code (number like 10006 or string like `ECONNRESET`) */
            code?: string | number;
            /** Error category — same taxonomy as ACP `classifyErrorAsRequestError` */
            category?: string;
            /** Human-readable, sanitised error message */
            details?: string;
          }
        | null
      >;
    };
```
### ContentBlock

typescript
```
// 文本内容块
interface TextContentBlock {
  type: 'text';
  text: string;
}

// 工具调用块
interface ToolUseContentBlock {
  type: 'tool_use';
  id: string;
  name: string;
  input: Record<string, unknown>;
}

// 工具结果块
interface ToolResultContentBlock {
  type: 'tool_result';
  tool_use_id: string;
  content?: string | ContentBlock[];
  is_error?: boolean;
}

type ContentBlock =
  | TextContentBlock
  | ToolUseContentBlock
  | ToolResultContentBlock;
```
### Usage

typescript
```
interface Usage {
  input_tokens: number;
  output_tokens: number;
  cache_read_input_tokens?: number | null;
  cache_creation_input_tokens?: number | null;
}
```
## Input Types

### AskUserQuestionInput

typescript
```
interface AskUserQuestionInput {
  // 要询问的问题列表（1-4 个问题）
  questions: AskUserQuestionQuestion[];
  // 用户答案（由权限组件收集）
  answers?: Record<string, string>;
}
```
### AskUserQuestionQuestion

typescript
```
interface AskUserQuestionQuestion {
  // 完整问题文本（应以 ? 结尾）
  question: string;
  // 简短标签（最多 12 个字符）
  header: string;
  // 可用选项（2-4 个选项）
  options: AskUserQuestionOption[];
  // 是否允许多选
  multiSelect: boolean;
}
```
### AskUserQuestionOption

typescript
```
interface AskUserQuestionOption {
  // 显示文本（1-5 个单词）
  label: string;
  // 选项说明
  description: string;
}
```
### ToolInputMap

typescript
```
interface ToolInputMap {
  AskUserQuestion: AskUserQuestionInput;
}

type KnownToolName = keyof ToolInputMap;
```
## 相关文档

- [SDK 概览](./sdk) \- 快速入门和使用示例
- [Hook 参考指南](./hooks) \- 详细的 Hook 配置说明
- [MCP 集成](./mcp) \- MCP 服务器配置指南