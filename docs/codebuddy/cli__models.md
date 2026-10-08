# models.json 配置指南

## 概述

`models.json` 是一个配置文件，用于自定义模型列表和控制模型下拉列表的显示。该配置支持两个级别：

- **用户级**: `~/.codebuddy/models.json` \- 全局配置，适用于所有项目
- **项目级**: `<workspace>/.codebuddy/models.json` \- 项目特定配置，优先级高于用户级

## 配置文件位置

### 用户级配置

```
~/.codebuddy/models.json
```
### 项目级配置

```
<project-root>/.codebuddy/models.json
```
## 配置优先级

配置合并优先级从高到低：

1. 项目级 models.json
2. 用户级 models.json
3. 内置默认配置

项目级配置会覆盖用户级配置中的相同模型定义（基于 `id` 字段匹配）。`availableModels` 字段：项目级完全覆盖用户级，不进行合并。

## 配置结构

json
```
{
  "models": [
    {
      "id": "model-id",
      "name": "Model Display Name",
      "vendor": "vendor-name",
      "apiKey": "sk-actual-api-key-value",
      "maxInputTokens": 200000,
      "maxOutputTokens": 8192,
      "url": "https://api.example.com/v1/chat/completions",
      "temperature": 0.7,
      "supportsToolCall": true,
      "supportsImages": true
    }
  ],
  "availableModels": ["model-id-1", "model-id-2"]
}
```
## 配置字段说明

### models

类型： `Array<LanguageModel>`

定义自定义模型列表。可以添加新模型或覆盖内置模型配置。

#### LanguageModel 字段

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | string | ✓ | 模型唯一标识符 |
| `name` | string | \- | 模型显示名称 |
| `vendor` | string | \- | 模型供应商 （如 OpenAI, Google) |
| `apiKey` | string | \- | API 密钥，支持环境变量引用（见下方安全配置说明） |
| `maxInputTokens` | number | \- | 最大输入 token 数 |
| `maxOutputTokens` | number | \- | 最大输出 token 数 |
| `url` | string | \- | API 端点 URL，支持环境变量引用 (必须是接口完整路径,一般以 `/chat/completions` 结尾） |
| `api` | string | \- | 请求协议，取值同 pi 的 `api`。设为 `openai-responses` 时改走 OpenAI Responses API，`url` 填 base URL，见 [OpenAI Responses API 配置示例](#openai-responses-api-配置示例) |
| `temperature` | number | \- | 采样温度，范围 0\-2，值越高输出越随机，值越低输出越确定 |
| `supportsToolCall` | boolean | \- | 是否支持工具调用 |
| `supportsImages` | boolean | \- | 是否支持图片输入 |
| `supportsReasoning` | boolean | \- | 是否支持推理模式 |
| `relatedModels` | object | \- | 关联模型配置，指定在不同场景（`lite`/`reasoning`/`vision`/`longContext`/`subagent`）下使用哪个模型 id。详见[配置关联模型](#配置关联模型) |

**重要说明：**

- 目前仅支持 OpenAI 接口格式的 API
- `url` 字段必须是接口完整路径,一般以 `/chat/completions` 结尾
- 例如: `https://api.openai.com/v1/chat/completions` 或 `http://localhost:11434/v1/chat/completions`

### 安全配置：使用环境变量引用

为避免 API 密钥明文存储在配置文件中，`apiKey` 和 `url` 字段支持环境变量引用语法 `${VAR_NAME}`。

**语法格式：**

```
${环境变量名}
```
**配置示例：**

json
```
{
  "models": [
    {
      "id": "gpt-4o",
      "name": "GPT-4o",
      "vendor": "OpenAI",
      "apiKey": "${OPENAI_API_KEY}",
      "url": "https://api.openai.com/v1/chat/completions"
    }
  ]
}
```
**设置环境变量：**

bash
```
# 在 ~/.zshrc 或 ~/.bashrc 中添加
export OPENAI_API_KEY="sk-your-actual-api-key"

# 或者在启动时临时设置
OPENAI_API_KEY="sk-xxx" codebuddy
```
**使用系统 Keychain（macOS）：**

bash
```
# 存储密钥到 Keychain
security add-generic-password -a "$USER" -s "openai-api-key" -w "sk-xxx"

# 在 ~/.zshrc 中配置自动导出
export OPENAI_API_KEY=$(security find-generic-password -s "openai-api-key" -w 2>/dev/null)
```
**注意事项：**

- 环境变量在 CLI 启动时解析
- 如果环境变量不存在，将保留原始占位符（会导致 API 调用失败）
- 建议将 `models.json` 文件权限设置为 `600`（仅所有者可读写）
- 不要将包含实际密钥的配置文件提交到版本控制系统

### availableModels

类型： `Array<string>`

控制模型下拉列表中显示哪些模型。只有在此数组中列出的模型 ID 才会在 UI 中显示。

- 如果未配置或为空数组，则显示所有模型
- 配置后，只显示列出的模型 ID
- 可以同时包含内置模型和自定义模型的 ID

## 使用场景

### 1\. 添加自定义模型

在用户级或项目级添加新的模型配置：

json
```
{
  "models": [
    {
      "id": "my-custom-model",
      "name": "My Custom Model",
      "vendor": "OpenAI",
      "apiKey": "sk-custom-key-here",
      "maxInputTokens": 128000,
      "maxOutputTokens": 4096,
      "url": "https://api.myservice.com/v1/chat/completions",
      "supportsToolCall": true
    }
  ]
}
```
### 2\. 覆盖内置模型配置

修改内置模型的默认参数：

json
```
{
  "models": [
    {
      "id": "gpt-4-turbo",
      "name": "GPT-4 Turbo (Custom Endpoint)",
      "vendor": "OpenAI",
      "url": "https://my-proxy.example.com/v1/chat/completions",
      "apiKey": "sk-your-key-here"
    }
  ]
}
```
### 3\. 限制可用模型列表

只在下拉列表中显示特定模型：

json
```
{
  "availableModels": [
    "gpt-4-turbo",
    "gpt-4o",
    "my-custom-model"
  ]
}
```
### 4\. 项目特定配置

为特定项目使用不同的模型或 API 端点：

**项目 A** (`.codebuddy/models.json`):

json
```
{
  "models": [
    {
      "id": "project-a-model",
      "name": "Project A Model",
      "vendor": "OpenAI",
      "url": "https://project-a-api.example.com/v1/chat/completions",
      "apiKey": "sk-project-a-key",
      "maxInputTokens": 100000,
      "maxOutputTokens": 4096
    }
  ],
  "availableModels": ["project-a-model", "gpt-4-turbo"]
}
```
## 热重载

配置文件支持热重载：

- 文件变更会被自动检测
- 使用 1 秒防抖延迟避免频繁重载
- 配置更新后会自动同步到应用

监听的文件：

- `~/.codebuddy/models.json` （用户级）
- `<workspace>/.codebuddy/models.json` （项目级）

## 标签系统

通过 `models.json` 添加的模型会自动标记 `custom` 标签，便于在 UI 中识别和过滤。

## 合并策略

配置使用 `SmartMerge` 策略：

- 相同 ID 的模型配置会被覆盖
- 不同 ID 的模型会被追加
- 项目级配置优先于用户级配置
- `availableModels` 过滤在所有合并完成后执行

## 示例配置

### API 端点 URL 格式说明

**必须使用完整路径：** 所有自定义模型的 `url` 字段一般以 `/chat/completions` 结尾。

✅ **正确示例：**

```
https://api.openai.com/v1/chat/completions
https://api.myservice.com/v1/chat/completions
http://localhost:11434/v1/chat/completions
https://my-proxy.example.com/v1/chat/completions
```
❌ **错误示例：**

```
https://api.openai.com/v1
https://api.myservice.com
http://localhost:11434
```
### OpenRouter 平台配置示例

使用 OpenRouter 访问多种模型：

json
```
{
  "models": [
    {
      "id": "openai/gpt-4o",
      "name": "open-router-model",
      "url": "https://openrouter.ai/api/v1/chat/completions",
      "apiKey": "sk-or-v1-your-openrouter-api-key",
      "maxInputTokens": 128000,
      "maxOutputTokens": 4096,
      "supportsToolCall": true,
      "supportsImages": false
    }
  ]
}
```
### DeepSeek 平台配置示例

使用 DeepSeek 模型（配置 `url` 后，即使与云端同 id 也会按"完全替换"语义生效，不会被云端默认项合并覆盖）：

json
```
{
  "models": [
    {
      "id": "deepseek-v4-pro",
      "name": "DeepSeek V4 Pro",
      "vendor": "DeepSeek",
      "url": "https://api.deepseek.com/v1/chat/completions",
      "apiKey": "${DEEPSEEK_API_KEY}",
      "maxInputTokens": 128000,
      "maxOutputTokens": 8192,
      "supportsToolCall": true,
      "supportsImages": false
    },
    {
      "id": "deepseek-v4-flash",
      "name": "DeepSeek V4 Flash",
      "vendor": "DeepSeek",
      "url": "https://api.deepseek.com/v1/chat/completions",
      "apiKey": "${DEEPSEEK_API_KEY}",
      "maxInputTokens": 128000,
      "maxOutputTokens": 8192,
      "supportsToolCall": true,
      "supportsImages": false
    }
  ],
  "availableModels": [
    "deepseek-v4-pro",
    "deepseek-v4-flash"
  ]
}
```
设置 API 密钥环境变量后启动：

bash
```
export DEEPSEEK_API_KEY="<your-deepseek-api-key>"
codebuddy --model deepseek-v4-pro
```

> **提示**：如果不希望维护 `models.json`，也可以完全通过环境变量对接 DeepSeek，见 [env\-vars.md 对接 DeepSeek 示例](./env-vars#对接-deepseek-示例)。

### OpenAI Responses API 配置示例

`api` 设为 `openai-responses` 后，该模型改用 OpenAI Responses API：请求发往 `{url}/responses`，多轮对话会原样回放上一轮返回的加密推理（`encrypted_content`）。以 aihub 上的 `gpt-6-sol` 为例：

json
```
{
  "models": [
    {
      "id": "gpt-6-sol",
      "name": "GPT-6 Sol",
      "api": "openai-responses",
      "url": "http://api.aihub.woa.com/openai/v1",
      "apiKey": "${AIHUB_KEY}?provider=azure&cache_task_id=${CODEBUDDY_SESSION_ID}&timeout=3600",
      "supportsReasoning": true,
      "supportsToolCall": true,
      "maxOutputTokens": 128000,
      "reasoning": { "defaultEffort": "max", "supportedEfforts": ["low", "medium", "high", "xhigh", "max"] }
    }
  ]
}
```
- `url` 填 base URL，末尾带不带 `/responses` 都可以。
- 只有模型配置里显式写的 `api` 会切换协议；模型目录里标注为 `openai-responses` 的内置模型仍走原有链路。
- apiKey 里的 `${CODEBUDDY_SESSION_ID}`（或 `${CLAUDE_SESSION_ID}`）在每次请求时替换为主会话 id。subagent、标题和 WebFetch 摘要等一次性辅助调用、`/btw`，以及 fork 出的会话（`/fork`、`--fork-session`、ACP fork）都沿用来源会话的值，这样回放的加密推理始终落在能解密它的上游账号上；会话 JSONL 里每条 Responses 条目的 `providerData.upstream.rootSessionId` 记录了这个值，fork 和 `--resume` 据此沿用。加载期的 `${ENV}` 展开会跳过这两个名字，即使进程环境里有同名变量（例如从另一个会话的 shell 启动 CLI）也不会被提前写死。aihub 用它作 `cache_task_id`，把同一任务的所有请求固定在同一个上游账号；需要固定会话 id 时配合 `--session-id` 使用。
- aihub 限流时返回 HTTP 200，在流里下发 `error` / `response.failed`。CLI 把输出开始前的流内错误还原成 OpenAI 普通接口返回的 HTTP 状态，重试与模型切换和 chat completions 一致：限流按 429 退避重试；额度耗尽（`insufficient_quota`）同为 429，但不重试，直接交给备用模型；上下文超长、请求内容或图片无效按 400，不重试（上下文超长会触发自动压缩）；`server_error` 按 500，不重试。其他流内错误仍按原有的流式错误处理。无人值守跑批建议设 `CODEBUDDY_RETRY_WATCHDOG=1`（或调大 `CODEBUDDY_MAX_RETRIES`）。
- 与 pi 一致，只有声明了 `supportsReasoning: true` 的模型、且这次请求带推理参数（开启了思考）时，才携带 `include: ["reasoning.encrypted_content"]`，与 `store` 无关。
- 工具结果与用户消息里的图片（含会话恢复后的 blob 引用）会还原为 `input_image`，`detail` 默认 `auto`；工具结果的形状与 pi 一致：文本合并成一段放在前面，图片随后，没有图片时仍是字符串。`supportsImages: false` 时替换为省略提示。
- 回放历史时，其他模型产生的条目、以及推理条目无法回放的那次调用，都不带上游 `fc_` / `msg_` id，避免 API 的 reasoning 配对校验报错；call id 规范为 `[A-Za-z0-9_-]`、最长 64 字符，空工具输出发送 `(no tool output)`。
- 执行中途插入的消息（`steer` 控制请求、后台任务通知等排队消息）在 Responses 下同样生效。stream\-json 输入的普通 user 消息按独立一轮排队，不做中途插入。
- `max` / `xhigh` 档位要在 `reasoning.supportedEfforts` 里声明，否则会降级为 `high`。
- 请求总是显式携带 `store`：默认 `false`，产品特性 `ResponsesStore` 开启时为 `true`。wb 用 `--features '{"rollout":true}'` 打开；直接运行 CLI 时设 `CODEBUDDY_RESPONSES_STORE_ENABLED=1`。
- 推理耗时较长时调大 `CODEBUDDY_FIRST_TOKEN_TIMEOUT_MS` 和 `CODEBUDDY_STREAM_TIMEOUT_MS`（单位毫秒）。
- 会话 JSONL 中 reasoning 条目的 `providerData.encrypted_content` 是原样保存的密文，`providerData.upstream` 记录 `model`、`region`（`x-ms-region`）、`accountId`（`x-account-id`）和 `rootSessionId`（这次调用的 `cache_task_id`）。
- 需要每次调用实际发出的完整请求（`instructions`、`tools`、`input`）时，设 `OTEL_LOG_RAW_API_BODIES=file:<dir>`，见 [Monitoring](./monitoring)。

### 配置关联模型

CodeBuddy Code 在一次会话中会根据场景切换模型，避免用大模型处理简单任务、或用通用模型处理需要推理 / 视觉 / 长上下文的请求。这些场景通过模型条目的 `relatedModels` 字段声明。

**支持的场景（variant type）：**

| 场景 | 用途 | 当前状态 |
| --- | --- | --- |
| `lite` | 轻量快速模型，用于后台提取、摘要等低价值请求；也是 Agent 工具 `model: "lite"` 参数对应的模型 | **已生效** |
| `reasoning` | 推理增强模型，用于需要深度思考的复杂推理；Agent 工具 `model: "reasoning"` 参数对应的模型 | **已生效** |
| `subagent` | 子代理和团队成员默认使用的模型 | **预留未启用**——子代理使用独立的 `subagents` 解析链，不读取本字段 |
| `vision` | 视觉理解模型，用于需要处理图片的请求 | **预留未启用**——类型已定义，尚无调用点消费此 variant |
| `longContext` | 长上下文模型，用于上下文超长的请求 | **预留未启用**——类型已定义，尚无调用点消费此 variant |

> **当前实际可用**：只有 `lite` 和 `reasoning` 两个 variant 在 agent\-manager 中被消费并映射到模型切换逻辑。`subagent` / `vision` / `longContext` 三项仅保留在类型定义中，为后续迭代预留，现在写进 `relatedModels` 不会报错但也不会生效。

**关键规则（自定义模型必读）：**

> 通过 `models.json` 添加的自定义模型**不会继承**产品内置的 `defaultRelatedModels`。 如果自定义主模型没有声明 `relatedModels`，且没有环境变量或 `variantModels` 覆盖，`lite` 和 `reasoning` 会回退到主模型。子代理不读取 `relatedModels.subagent`，但配置为 `lite` 或 `reasoning` 的子代理仍会走这条场景变体解析链。

**配置示例（DeepSeek 主模型 \+ flash 作为 lite / reasoning）：**

json
```
{
  "models": [
    {
      "id": "deepseek-v4-pro",
      "name": "DeepSeek V4 Pro",
      "vendor": "DeepSeek",
      "url": "https://api.deepseek.com/v1/chat/completions",
      "apiKey": "${DEEPSEEK_API_KEY}",
      "maxInputTokens": 128000,
      "maxOutputTokens": 8192,
      "supportsToolCall": true,
      "relatedModels": {
        "lite": "deepseek-v4-flash",
        "reasoning": "deepseek-v4-pro"
      }
    },
    {
      "id": "deepseek-v4-flash",
      "name": "DeepSeek V4 Flash",
      "vendor": "DeepSeek",
      "url": "https://api.deepseek.com/v1/chat/completions",
      "apiKey": "${DEEPSEEK_API_KEY}",
      "maxInputTokens": 128000,
      "maxOutputTokens": 8192,
      "supportsToolCall": true
    }
  ],
  "availableModels": [
    "deepseek-v4-pro",
    "deepseek-v4-flash"
  ]
}
```
**场景变体解析优先级（从高到低，当前仅 `lite` / `reasoning` 会走这个解析链）：**

1. 对应的环境变量（`CODEBUDDY_SMALL_FAST_MODEL` 对应 `lite`、`CODEBUDDY_BIG_SLOW_MODEL` 对应 `reasoning`）
2. 项目级 `variantModels[variant]`
3. 用户全局 `variantModels[variant]`
4. 当前主模型条目里的 `relatedModels[variant]`
5. 产品内置的 `defaultRelatedModels[variant]`（仅对内置模型生效，自定义模型跳过这步）
6. 回落到主模型自身

`variantModels` 保存在 `settings.json` 中，也可通过 `/model:lite` / `/model:reasoning` 命令编辑。它适合在用户或项目范围内将 `lite` / `reasoning` 固定映射到具体模型；`relatedModels` 则适合让映射跟随当前主模型。

**内置子代理解析优先级（从高到低）：**

1. `CODEBUDDY_CODE_SUBAGENT_MODEL`，统一覆盖所有子代理
2. 本次 Agent 工具调用的 `model` 入参（模型 ID、名称、别名或 `default` / `lite` / `reasoning`）
3. 项目级 `subagents.agents.<子代理名>.model`
4. 用户全局 `subagents.agents.<子代理名>.model`
5. 产品内置声明，如 `Explore` 使用 `lite`
6. 继承主对话模型

子代理模型不读取 `relatedModels.subagent`。当子代理配置为 `lite` 或 `reasoning` 时，会继续通过上面的场景变体解析链得到具体模型。

以下配置应写入用户级或项目级 `settings.json`：

json
```
{
  "subagents": {
    "agents": {
      "Explore": { "model": "lite" },
      "Plan": { "model": "reasoning" }
    }
  },
  "variantModels": {
    "lite": "<fast-model-id>",
    "reasoning": "<reasoning-model-id>"
  }
}
```
**不同配置方式的适用场景：**

- 使用 `relatedModels`，让场景映射跟随主模型。
- 使用 `variantModels` 或 `/model`，在用户或项目范围内固定 `lite` / `reasoning` 的具体模型。
- 使用 `subagents.agents.<子代理名>.model` 或 `/agents`，为内置子代理分别选择模型或场景变体。
- 使用模型环境变量进行运维或 CI 级覆盖。环境变量优先于持久化设置；取消后，低优先级设置会恢复生效。

### 完整示例

json
```
{
  "models": [
    {
      "id": "gpt-4o",
      "name": "GPT-4o",
      "vendor": "OpenAI",
      "apiKey": "sk-your-openai-key",
      "maxInputTokens": 128000,
      "maxOutputTokens": 16384,
      "supportsToolCall": true,
      "supportsImages": true
    },
    {
      "id": "my-local-llm",
      "name": "My Local LLM",
      "vendor": "Ollama",
      "url": "http://localhost:11434/v1/chat/completions",
      "apiKey": "ollama",
      "maxInputTokens": 8192,
      "maxOutputTokens": 2048,
      "supportsToolCall": true
    }
  ],
  "availableModels": [
    "gpt-4o",
    "my-local-llm"
  ]
}
```
## 故障排查

### 配置未生效

1. 检查 JSON 格式是否正确
2. 确认文件路径是否正确
3. 查看日志输出确认配置是否被加载
4. 确认环境变量中的 API 密钥是否已设置

### 模型未在列表中显示

1. 检查模型 ID 是否在 `availableModels` 中列出
2. 确认 `models` 配置是否正确
3. 验证必填字段 （`id`, `name`, `provider`) 是否都已提供

### 热重载未触发

- 配置文件变更有 1 秒防抖延迟
- 确保文件确实被保存到磁盘
- 检查文件监听是否正常启动 （查看调试日志）