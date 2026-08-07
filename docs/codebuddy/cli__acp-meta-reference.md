# ACP `codebuddy.ai/*` 扩展命名空间参考

> CodeBuddy 在 ACP（Agent Client Protocol）上的全部私有扩展清单：`_meta` 扩展键 \+ `_codebuddy.ai/*` 扩展方法。
> 
> 面向两类读者：① 第三方 ACP 客户端（Zed 等）——想知道哪些扩展**可以读**、哪些**绝不该自己造**； ② CodeBuddy / WorkBuddy 内部开发者——改准入链路时，需要知道哪条键属于标准面、哪条属于多租户私有通道。

## 0\. 最重要的一条：标准 ACP 面零 `_meta` 可用

**`cbc --acp` 的 `initialize` / `session/new` / `session/prompt` 全链路，客户端可以一个 `codebuddy.ai/*` `_meta` 都不带，且必须完整可用。** 这是硬契约，不是「目前碰巧能跑」。

机制上由 **process\-login 组合根**保证（profile `cbc-tui` / `cbc-headless` / `agent-sdk-js-single`）：

- `src/node/session/process-login-admission-authority.ts` —— 进程内自持 transport credential 与 principal， `issueMainAdmission()` 在同一处同时构造准入 envelope 与其 grant；
- `src/node/session/process-login-acp-admission-service.ts:60-84` —— `admitAndActivate()` 里**整体替换**`metadata` 为本进程自产的 ticket。原文注释即为契约：「客户端 `_meta` 完全不参与身份决策」。

外部 ACP 客户端既不可能、也不应该构造 runtime 准入 envelope，因此这条零 meta 路径是标准面的唯一正确形态。

常驻防线：`src/e2e/acp-zero-meta-contract.spec.ts` —— 裸 stdio NDJSON 驱动 `bin/codebuddy --acp`， 全程零 meta 跑 `initialize → session/new → session/prompt`，并对「missing … metadata」类错误直接判红。

**对照面**：multi\-owner\-headless 走的是 **session\-payload 组合根**，它的 `session/new`**强制**显式携带 `_meta['codebuddy.ai/sessionAdmissionV2']`（见 `runtime-admission-acp-adapter.ts:47-48` 抛 `ACP Session request is missing sessionAdmissionV2 metadata`）。那是**私有通道，不是 ACP 协议要求**—— 两条组合根的差别只在「envelope 的生产者是谁」，与标准面无关。

> **C3 变更（workbuddy\-single 形态正名 B1）**：WorkBuddy 桌面端（`workbuddy-single`）与 `workbuddy-completion-warm` 已从「per\-session wire 身份 envelope」改为**进程级身份注入**—— daemon 在 `initialize` 之后经 `_codebuddy.ai/activateWorkbuddyOwnerRuntime` （warm 侧是 `_codebuddy.ai/activateCompletionRuntime`）注入一次 owner 授权，此后 CLI 进程内 **自产** envelope。这两条面的 `session/new` **不再携带 `sessionAdmissionV2` / `authSession`**， 只保留 launcher 的 `runtimeTransportCredential`（transport 认证不变式，自签之前逐次校验） 与两个**非身份**业务授权键 `sessionGrantV1` / `completionDispatchGrantV1`（§3\.1）。
> 
> `sessionAdmissionV2` 的生产面收敛为三处，**只有第一处仍过 daemon→CLI 的 wire**： ① host control sidecar（daemon 侧 `workbuddy-host-control-authority.ts`）； ② teammate leader 进程内自签、经 bootstrap channel 下发给 child （`workbuddy-admission-security.ts` `issueTeammateAdmissionMetadata`）； ③ C3 后 workbuddy\-single / completion\-warm 进程内自签的主 envelope（同文件 `issueMainAdmissionMetadata` / `issueCompletionDispatchMetadata`）。

## 1\. 分类口径

| 标注 | 含义 |
| --- | --- |
| **公共** | 公共可选扩展。标准 ACP 面（`cbc --acp`）可见或可选携带；缺失不影响协议可用；第三方客户端可以安全地读取、按需忽略。 |
| **私有** | 多租户私有通道，**仅 session\-payload 组合根**（WorkBuddy daemon ↔ CLI、multi\-owner\-headless）生产与消费。第三方 ACP 客户端**不得生产**这些键；标准面永远不会要求它们。 |

方向记法：`A→C` \= Agent 发给 Client（响应 / 通知）；`C→A` \= Client 发给 Agent（请求参数）；`双向` \= 两个方向都出现。

## 2\. 清单口径与对账

> **行号锚点免责**：本文档所有 `文件:行号` 锚点对应撰写（及最近一次校对）时点的源码，仅供快速定位； 源码演进后行号必然漂移。**以「文件 \+ 引用文案 / 符号」grep 为准**，行号只作辅助。

**canonical grep（可复核）**：

bash
```
# 在 genie 仓根执行；git grep 天然排除 node_modules / dist / lib / out-tsc 等构建产物
git grep --untracked -hoE "codebuddy\.ai/[A-Za-z0-9_.-]*" -- 'packages/**/*.ts' 'packages/**/*.tsx' | sort -u | wc -l
# => 195（去重后的 token 数）
```

> **`--untracked` 是必须的**：不带它只统计已跟踪文件，任何尚未提交的新增源文件都会 被漏掉，对账数字随提交时机漂移。**只对账 token 数，不对账命中行数** —— 行数对 无关的注释改动都敏感，做不成稳定锚点。

> 注意：`-oE` 的字符类不含 `/`，所以 `_codebuddy.ai/foo` 会被切出 token `codebuddy.ai/foo`（丢掉前导下划线）， `_codebuddy.ai/session/rollback` 会被切成 `codebuddy.ai/session`。**195 是 token 数，不是 key 数**， 需要按下表四分后才等于真实清单。

**195 \= 142 \+ 44 \+ 3 \+ 6**，逐项在本文档内可查：

| 桶 | 数量 | 是什么 | 落在本文档 |
| --- | --- | --- | --- |
| A | **142** | 真正的 `_meta` 扩展键 | §3（全部列出） |
| B | **44** | JSON\-RPC 扩展方法/通知名（`_codebuddy.ai/*`），被 grep 切掉了下划线 | §4（全部列出） |
| C | **3** | 命名空间前缀 / 通配写法，不是独立键 | §5\.1 |
| D | **6** | 产品站 URL 路径伪命中（`https://www.codebuddy.ai/...`） | §5\.2 |

> **C3 对账变更（194→195）**：A 桶净额不变（删 `completionDispatchId` / `completionExecutionDigest`，加 `sessionGrantV1` / `completionDispatchGrantV1`）； B 桶 43→44（新增 `_codebuddy.ai/activateWorkbuddyOwnerRuntime`）。

判别方法（可复现）：对每个 token，看它在源码里出现时**前一个字符**——`_` ⇒ 扩展方法（B）， `.` 或 `/` ⇒ URL（D），其余 ⇒ `_meta` 键（A）；再把「后面还能接 `/` 或 `*`」的通配前缀挑出来（C）。

## 3\. `_meta` 扩展键全清单（142 条）

### 3\.1 准入 / 身份 / 凭据（14 条）

本组是「公共 vs 私有」分界最要紧的地方。

| 键 | 方向 | 分类 | 生产者 | 消费者 | 语义 |
| --- | --- | --- | --- | --- | --- |
| `runtimeAdmission` | A→C | 公共 | CLI，`runtime-admission-acp-adapter.ts:10-11,30-39`（`initialize` 响应） | session\-payload 侧的 daemon（据此构造 envelope）；标准面客户端可忽略 | 进程准入握手：`schemaVersion` / `runtimeProfile` / `runtimeConfigSha256` / `processInstanceId` / `handshakeNonce`。**两条组合根都发**，零 meta e2e 用它锚定 `runtimeProfile === 'cbc-headless'` |
| `sessionAdmissionV2` | C→A | **私有** | multi\-owner issuer（进程外签发）；WorkBuddy 家族现仅剩 host control sidecar（`workbuddy-host-control-authority.ts`） | `runtime-admission-acp-adapter.ts:47-53`、`multi-owner-acp-admission-service.ts:164` | `session/new` / `session/load` 的准入 envelope。缺失即 `ACP Session request is missing sessionAdmissionV2 metadata`。**process\-login 与 C3 后的 workbuddy\-single / completion\-warm 均由 CLI 自产覆盖，客户端无需也不应携带** |
| `sessionGrantV1` | C→A | **私有** | daemon，`workbuddy-runtime-admission.ts` `buildSessionGrantMetadata`（C3 新增） | `workbuddy-single-admission-authority.ts` `readWorkbuddySessionGrant`（仅 workbuddy\-single 装配） | 身份撤出 `_meta` 后仍需过 wire 的**非身份**业务授权：`canonicalSessionId`（daemon 的会话主键，`captureRuntimeBinding` 断言回报相等）/ `environment.values`（prewarm 命中路径下 session 增量 env 的唯一送达通道）/ `workspace{root,cwd,allowedRoots}`。**不参与身份决策**；标准 ACP 面不读该键 |
| `completionDispatchGrantV1` | C→A | **私有** | daemon，`workbuddy-runtime-admission.ts` `buildCompletionDispatchGrantMetadata`（C3 新增） | `workbuddy-single-admission-authority.ts` `readWorkbuddyCompletionDispatchGrant`（仅 completion\-warm 装配） | completion warm 的 per\-dispatch **执行授权**：`executionSubPolicyId` \+ 其 digest / `dispatchId` / `executionDigest` / `workspace`。身份来自进程级注入，执行天花板仍逐 dispatch 由 daemon 下达；缺该键即 fail\-closed |
| `authSession` | C→A | **私有** | daemon（session\-payload 身份种子） | `acp-agent.ts:2141-2143` → per\-session auth holder | `{ auth: { accessToken, tokenType?, domain?, refreshToken? }, account?: { uid? } }`。account 字段一律由 JWT 派生，绝不采信客户端自报 |
| `productConfig` | C→A | **私有** | daemon（`workbuddy-server/src/agent/cli-product-env.ts:170`） | `acp-agent.ts:2144-2146` | per\-session 产品配置注入：`endpoint` / `networkEnvironment` |
| `runtimeTransportCredential` | 双向 | **私有** | 准入核心（`multi-owner-acp-admission-service.ts:38-39`、`host-teammate-admission-security.ts:41`） | 同上 | 绑定 transport 的一次性凭据，用于 admit 时证明连接身份 |
| `runtimeSessionBindingV2` | A→C | **私有** | `multi-owner-acp-admission-service.ts:40-41`、`workbuddy-session-admission-authority.ts:18` | daemon | 准入成功后回带的 exact binding 投影：ownerId / ownerGeneration / canonicalSessionId / sessionGeneration / resourceId |
| `runtimeBindingToken` | C→A | **私有** | daemon | `agent-client-protocol/src/common/runtime-wire-authority.ts:1`、`acp-agent.ts:2147-2155` | wire 请求的 binding token；非空字符串否则 `RUNTIME_BINDING_TOKEN_INVALID` |
| `runtimeAuthority` | 双向 | **私有** | daemon / CLI | `runtime-wire-authority.ts:2` | wire fencing 权威快照（processIncarnation / connectionEpoch / owner / session / run 各代际），失配抛 `RUNTIME_*_STALE` |
| `teamNamespaceActivation` | C→A | 公共 | leader 启动 teammate 时注入（`host-teammate-launch.ts:138`、`workbuddy-teammate-launch.ts:124`） | teammate 子进程 | team 命名空间激活声明。**两条组合根共用**，不是 session\-payload 独有；第三方客户端不会遇到。**限定**：唯一消费通道是 teammate bootstrap 启动链（`teammate-runner.ts:272` 从 `receiveWorkbuddyTeammateBootstrap` 返回的 bootstrap metadata 上读取），不是 ACP wire 上的客户端 `_meta`；第三方客户端在标准 ACP 面生产该键不会被任何路径消费 |
| `userinfo` | A→C | 公共 | `acp-agent.ts:1963-1974`（`authenticate` 响应） | 客户端 UI | 登录用户信息：userId / userName / userNickname / enterpriseId / enterpriseName / authType |
| `accessToken` | —— | **私有** | **无生产者**（协议上不存在） | —— | 仅出现在日志脱敏覆盖用例（`workbuddy-core/.../conversation-file-logger.spec.ts:44`）：验证「带命名空间前缀的 token 键同样被 `[redacted]`」。列在此处防止今后误当作可用键 |
| `homeDir` | —— | 公共 | **已退役** | —— | **已退役死字段，生产与消费两侧代码均已物理删除**（D6\-7）：全仓唯一命中是反向门禁用例 `settings-persession-invariants.spec.ts:10`，断言 `acp-agent.ts` 里不再出现该键——**连存量兼容读侧都没有**，客户端携带不会被任何路径读取。homeDir 恒由 JWT 派生（`resolveControlledHomeDir`）。仅为「不要重新启用该键名」而留档 |

### 3\.2 请求关联与追踪（16 条）

全部 **公共**：Agent 在响应 / 通知的 `_meta` 上回带，客户端可选消费；`requestId` / `messageRequestId` / `userMessageId` / `messageId` 也接受客户端在 `session/prompt` 上先行下发（`acp-agent.ts:2925-2938`），缺省则由 CLI 自产。

| 键 | 方向 | 生产者 | 语义 |
| --- | --- | --- | --- |
| `requestId` | 双向 | `acp-agent.ts:2925,3412` | 一次模型请求的全链路关联 ID（命中数最高的键） |
| `messageId` | 双向 | `acp-agent.ts:2937,3349` | 消息级 ID |
| `messageRequestId` | 双向 | `acp-agent.ts:2932,3423` | 消息 ↔ 请求的关联 ID |
| `userMessageId` | 双向 | `acp-agent.ts:2931` | 用户消息 ID（`session/prompt` 响应也回带） |
| `promptRequestId` | 双向 | `acp-agent.ts:3415-3416` | Renderer 每次 send/resend 生成的业务关联 ID，供 Desktop 埋点 \+ Galileo 串联 |
| `clientRequestId` | C→A | 客户端 | 工具调用上的客户端自定义关联 ID（`workbuddy-server/src/session/handlers.ts:1634`） |
| `modelRequestId` | A→C | `acp-view.ts:694` | 模型侧请求 ID |
| `traceId` | A→C | `acp-agent.ts:3075` | CLI 侧 trace ID |
| `traceparent` | A→C | `acp-agent.ts:2866,3429` | W3C traceparent 回传，使 renderer 的 stream\_render span 能挂到 prompt.send 下 |
| `runId` | A→C | `acp-agent.ts:263` | SessionRunStateMachine 的 run ID |
| `runStateRevision` | A→C | `acp-agent.ts:262` | run 状态快照 revision |
| `agentPhase` | A→C | `acp-agent.ts:261` | Agent 执行阶段（`AgentPhaseInfo`） |
| `timestamp` | A→C | `acp-timestamp-meta.ts:124-128` | 时间戳（归一化时会删除该扁平键，统一走规范位置） |
| `sendTime` | C→A | Renderer | 用户点击发送的时间戳，供 message 维度用户视角 TTFT 计算（`galileo-timing-hook.ts:110`） |
| `lfConvId` | A→C | 上游 | LF 会话 ID（扁平透传，`agent-ui/src/adapters/acp-message-accumulator.spec.ts:1132`） |
| `lfConvReqId` | A→C | 上游 | LF 会话请求 ID（同上） |

### 3\.3 会话属性与模式（14 条）

| 键 | 方向 | 分类 | 生产者 → 消费者 | 语义 |
| --- | --- | --- | --- | --- |
| `mode` | 双向 | 公共 | `acp-agent.ts:2984,3072` | 场景模式（scene mode） |
| `userId` | C→A | 公共 | Renderer → `session.meta`（`acp-agent.ts:2888`） | 埋点 / trace attribute 用的用户 ID（**不参与身份决策**，身份只认 JWT） |
| `conversationId` | 双向 | 公共 | `acp-agent.ts:2889` / `workbuddy-app/.../stream-span-manager.ts:144` | 上游会话 ID |
| `locale` | C→A | 公共 | `acp-agent.ts:2890`（兼容 `language`） | 语言 / 区域 |
| `expertId` | 双向 | 公共 | `acp-agent.ts:2891,2987` | 专家（expert）ID |
| `expertSelection` | A→C | 公共 | `workbuddy-server/.../expert-selection-reminder.ts:7` | 专家选择提醒块标记 |
| `parentSessionId` | A→C | 公共 | `acp-protocol.ts:319,342` | 子代理会话的父 session ID |
| `isSubAgent` | A→C | 公共 | `acp-protocol.ts:319,342` | 是否子代理会话（注意与下面 `isSubagent` 大小写不同，属历史遗留双写） |
| `isSubagent` | A→C | 公共 | `api-schema.ts:1803`、`use-acp.ts:284` | 工具调用维度「是否子代理调用」 |
| `subagentType` | A→C | 公共 | `api-schema.ts:1804` | 子代理类型（默认 `general-purpose`） |
| `isBackground` | A→C | 公共 | `api-schema.ts:1805` | 是否后台执行 |
| `isPlayground` | A→C | 公共 | `stream-span-manager.ts:148` | 是否 playground 场景 |
| `continue` | C→A | 公共 | `acp-agent.ts:2560` | `session/new` 上声明「继续上次对话」 |
| `sessionControl` | 双向 | 公共 | `workbuddy-core/.../conversation-prompt-operations.ts:12` | 会话控制指令载荷 |

### 3\.4 会话生命周期与错误（12 条）

| 键 | 方向 | 分类 | 生产者 | 语义 |
| --- | --- | --- | --- | --- |
| `errorMessage` | A→C | 公共 | `acp-agent.ts:414,3066` | 与 `stopReason: 'refusal'` 并列的可读错误文案 |
| `finishReason` | A→C | 公共 | `acp-view.ts:703` | 模型 finish reason |
| `outcome` | A→C | 公共 | `acp-agent.ts:3087-3088` | prompt 结果判定（`SUCCESS` 等） |
| `businessFailed` | A→C | 公共 | `acp-utils.ts:1004` | 业务失败标记，供 UI renderer 与传输失败区分 |
| `cancelReason` | A→C | 公共 | `acp-protocol.ts:973` | 取消原因 |
| `cancelCause` | A→C | 公共 | `automation-prompt-builder.ts:285` | prompt result 上的取消成因（automation 优先读它） |
| `terminationReason` | A→C | 公共 | `acp-broadcast-service.ts:435` | 终止原因（如 `prompt_timeout`） |
| `promptFailurePhase` | A→C | 公共 | `workbuddy-server/src/backend/prompt-replay-safety.ts:2` | prompt 失败发生的阶段 |
| `promptFailureReason` | A→C | 公共 | 同上 `:3` | prompt 失败原因 |
| `promptReplaySafe` | A→C | 公共 | 同上 `:1` | 该次失败是否可安全重放 |
| `transportLost` | A→C | 公共 | `workbuddy-agent-adapter-next.ts:10689` | 传输连接丢失标记 |
| `transportError` | A→C | 公共 | 同上 `:10690` | 传输错误码（如 `ws_rpc_connection_lost`） |

### 3\.5 工具调用扩展（20 条）

全部 **公共**，绝大多数由 `acp-agent.ts:5013-5064` 一段集中从 provider data 复制到 `toolCallMeta`。

| 键 | 生产者 | 语义 |
| --- | --- | --- |
| `toolName` | `acp-agent.ts:4093,4168` | 工具名 |
| `toolCallId` | `acp-broadcast-service.ts:287` | 关联的工具调用 ID |
| `parentToolCallId` | `acp-agent.ts:3949,4004` | 父工具调用 ID（子代理嵌套） |
| `toolCancelReason` | `acp-agent.ts:578` | 工具取消原因（`permission_denied` 用于与普通取消区分） |
| `toolFailReason` | `acp-agent.ts:650` | 工具失败原因分类 |
| `toolResultTitle` | `persisted-transcript-projector.ts:72` | 工具结果标题（转写投影用） |
| `description` | `acp-agent.ts:5047,6344` | 工具调用描述 |
| `operation` | `acp-agent.ts:5046,6343` | 操作类型（如 `mcp-ui reverse tools/call`） |
| `target` | `acp-agent.ts:5045,6342` | 操作目标（如 MCP server 名） |
| `filename` | `acp-utils.ts:654` | 关联文件名 |
| `images` | `acp-broadcast-service.ts:684` | 图片载荷 |
| `rawResponse` | `acp-utils.ts:997` | 工具原始结构化结果，透传给 UI renderer（如 web\-search） |
| `bulkDeleteInfo` | `acp-agent.ts:5059-5060` | 批量删除信息 |
| `bypassHint` | `acp-agent.ts:5056-5057` | 旁路提示 |
| `interceptType` | `acp-agent.ts:5044,6758` | 拦截类型 |
| `sandboxIntercept` | `acp-agent.ts:5013,5043` | 沙箱拦截标记 |
| `sandboxApprovalMode` | `acp-agent.ts:5053-5054` | 沙箱审批模式 |
| `mcpUiIntercept` | `acp-agent.ts:4853,6341` | MCP\-UI 反向调用拦截标记 |
| `hook` | `acp-utils.ts:770`、`session-manager.ts:766` | Hook 结构化阻断信息 |
| `details` | `acp-agent.ts:6800` | 事件补充明细 |

### 3\.6 权限 / 计划 / 目标（8 条）

全部 **公共**。

| 键 | 生产者 | 语义 |
| --- | --- | --- |
| `decision` | `acp-broadcast-service.ts:289` | 权限决策结果 |
| `permissionResolved` | `acp-broadcast-service.ts:286` | 权限已解决通知 |
| `planContent` | `api-schema.ts:1808` | ExitPlanMode 的计划正文 |
| `goalProgress` | `use-acp.ts:491-492` | 目标进度 |
| `goalRecap` | `acp-broadcast-service.ts:487` | 目标回顾 |
| `goalStatus` | `use-acp.ts:522-523` | 目标状态 |
| `interruptionRequest` | `acp-broadcast-service.ts:221`、`session-replay.ts:692` | 中断（HITL）请求载荷 |
| `promptSuggestion` | `prompt-suggestion-service.ts:502` | Prompt 建议 |

### 3\.7 历史回放与转写投影（10 条）

| 键 | 方向 | 分类 | 生产者 | 语义 |
| --- | --- | --- | --- | --- |
| `historyReplay` | A→C | 公共 | `session-replay.ts:392` | 历史回放边界标记（`start` / 结束） |
| `historyReplayTotalItems` | A→C | 公共 | `session-replay.ts:393` | 回放总条目数（仅 `start` 时） |
| `rendererHistoryReplay` | A→C | 公共 | `conversation-frame-classifier.ts:83`、`replay-event-classifier.ts:82` | 渲染层回放标记 |
| `ownerSnapshotHistoryReplay` | A→C | **私有** | `replay-event-classifier.ts:87`、`conversation-frame-classifier.ts:84` | owner 快照回放标记——owner 概念只在 session\-payload 多租户下成立 |
| `isSessionSeparator` | A→C | 公共 | `conversation-frame-classifier.ts:91` | 会话分隔帧标记 |
| `separatorExtra` | A→C | 公共 | 同上 `:94` | 分隔帧附加信息 |
| `createTime` | A→C | 公共 | 同上 `:93` | 帧创建时间 |
| `offset` | A→C | 公共 | `workbuddy-agent-adapter-next.ts:6458` | 转写源 offset（旧键） |
| `sourceOffset` | A→C | 公共 | `agent-member-utils.ts:242`、`team-runtime.ts:461` | 转写源 offset（新键，优先于 `offset`） |
| `originalBytes` | A→C | 公共 | `persisted-transcript-projector.ts:71` | 转写截断前的原始字节数 |

### 3\.8 上下文压缩 compact（6 条）

全部 **公共**，走 `session_info_update._meta`。

| 键 | 生产者 | 语义 |
| --- | --- | --- |
| `compactType` | `context-protocol.ts:231` | 压缩类型，desktop adapter 据此决定呈现 |
| `compactStatus` | `conversation-frame-classifier.ts:231` | 压缩状态 |
| `compact-cancelled` | `context-protocol.ts:287` | `{ cancelled: true }` —— 压缩被取消 |
| `compact-limit-reached` | `context-protocol.ts:295` | `{ limitReached: true }` —— 触达压缩上限 |
| `compactTruncated` | `persisted-transcript-projector.ts:70` | 该帧在压缩中被截断 |
| `isCompactInternal` | `acp-agent.ts:3200,3396` | 该 prompt 是 compact 内部触发（不计入用户可见轮次） |

### 3\.9 Team / teammate（7 条）

| 键 | 方向 | 分类 | 生产者 | 语义 |
| --- | --- | --- | --- | --- |
| `teamUpdate` | A→C | 公共 | `acp-team-bridge.ts:745,779` | Team 状态事件（成员状态变更等） |
| `memberEvent` | A→C | 公共 | `acp-team-bridge.ts:602` | 成员流式消息的归属标签（成员名） |
| `memberName` | A→C | 公共 | `acp-agent.ts:5037` | 工具调用所属成员名 |
| `isTeamMember` | A→C | 公共 | `acp-agent.ts:5036` | 该工具调用来自 team 成员 |
| `agentColor` | A→C | 公共 | `acp-agent.ts:5039` | 成员展示色 |
| `syntheticTeammateMessage` | A→C | 公共 | `team-runtime-loader.ts:691`、`workbuddy-agent-adapter-next.ts:4945` | 合成的 teammate 消息（非模型直出） |
| `teammateSummary` | A→C | 公共 | 同上 `:693` / `:4946` | teammate 摘要文本 |

### 3\.10 Workflow（14 条）

全部 **公共**，由 `src/node/workflow/acp/workflow-acp-bridge.ts:146-190` 一处集中生产，键空间统一为 `codebuddy.ai/workflow*`。

| 键 | 行 | 语义 |
| --- | --- | --- |
| `workflowEventKind` | `:151` | 事件类型 |
| `workflowRunId` | `:156,168` | 运行 ID |
| `workflowName` | `:157` | 工作流名 |
| `workflowStatus` | `:158` | 运行状态 |
| `workflowAgentCount` | `:159` | agent 总数 |
| `workflowCachedCount` | `:160` | 命中缓存的 agent 数 |
| `workflowPhaseCount` | `:161` | 阶段总数 |
| `workflowError` | `:163` | 运行级错误 |
| `workflowPhase` | `:169` | 当前阶段 |
| `workflowAgentKey` | `:175` | agent key |
| `workflowAgentLabel` | `:177` | agent 展示名 |
| `workflowAgentPhase` | `:180` | agent 阶段 |
| `workflowAgentError` | `:183` | agent 级错误 |
| `workflowAgentTokens` | `:186` | agent token 消耗 |

### 3\.11 外部渠道接入 channel（6 条）

全部 **公共**，由 `acp-utils.ts:481-491` 生产、Web UI `use-acp.ts:202-213` 消费。承载企业微信等外部渠道的来源信息。

| 键 | 语义 |
| --- | --- |
| `channelSource` | 渠道来源标识 |
| `channelSender` | 发送者 ID |
| `channelSenderName` | 发送者展示名 |
| `channelChatId` | 会话 ID |
| `channelChatType` | 会话类型（`single` / `group`） |
| `commandKind` | 命令种类（`slash`） |

### 3\.12 MCP\-UI 与消息队列（4 条）

| 键 | 方向 | 分类 | 生产者 | 语义 |
| --- | --- | --- | --- | --- |
| `sendMessageMode` | C→A | 公共 | MCP\-UI widget（`mcp-app-handlers.ts:79,112`） | widget 回写消息的行为路由：`send` / `fill` |
| `message_queue_update` | A→C | 公共 | `acp-broadcast-service.ts:462` | 消息队列增量更新 |
| `newSessionId` | A→C | 公共 | `acp-command-attachment-router.ts:73` | 命令触发新建会话后的新 sessionId |
| `sessionReset` | A→C | 公共 | `acp-command-attachment-router.ts:72` | 会话被重置（如 `/clear`） |

### 3\.13 内容与用量（5 条）

| 键 | 方向 | 分类 | 生产者 | 语义 |
| --- | --- | --- | --- | --- |
| `usageByCategory` | A→C | 公共 | `acp-protocol.ts:64,1331` | `usage_update` 的分类用量；不变式：`sum(usageByCategory) === update.used` |
| `contentFilterNotice` | A→C | 公共 | `context-protocol.ts:258` | 内容过滤提示（`true` 时该 text 块是过滤告知） |
| `hiddenPromptContext` | C→A | 公共 | `colleague-mention-context.ts:15` | 该 prompt 块是隐藏上下文，不在 UI 呈现 |
| `progress` | A→C | 公共 | `acp-agent.ts:3820`、`stream-json-protocol.ts:554` | `session_info_update` 上的进度载荷 |
| `sourceEvent` | A→C | 公共 | `acp-utils.ts:146` | 该 update 的来源事件客观描述（facets），供 adapter 分流 |

### 3\.14 模型标识（4 条）

全部 **公共**，`acp-agent.ts:3437-3447` 集中回填。

| 键 | 语义 |
| --- | --- |
| `requestModelId` | 请求所用模型 ID |
| `requestModelName` | 请求所用模型名 |
| `responseModelId` | 实际响应模型 ID |
| `responseModelName` | 实际响应模型名（`conversation-event-machine.ts:334`） |

### 3\.15 completion warm 与其它（2 条）

> C3 变更：`completionDispatchId` / `completionExecutionDigest` 两个扁平键已随 `buildEphemeralMetadata` 一并**物理删除**，其语义并入 §3\.1 的 `completionDispatchGrantV1`（结构化的 per\-dispatch 执行授权）。

| 键 | 方向 | 分类 | 生产者 | 语义 |
| --- | --- | --- | --- | --- |
| `status` | A→C | 公共 | `acp-session-info-router.ts:136-137`、`conversation-event-machine.ts:763` | `session_info_update` 的状态字段 |
| `model` | A→C | 公共 | `stream-span-manager.ts:145` | 扁平模型名（span 归因用） |

**私有键小计（10 条）**：`sessionAdmissionV2`、`sessionGrantV1`、`completionDispatchGrantV1`、 `authSession`、`productConfig`、`runtimeTransportCredential`、`runtimeSessionBindingV2`、 `runtimeBindingToken`、`runtimeAuthority`、`ownerSnapshotHistoryReplay` —— 再加上「无生产者但归属凭据面」的 `accessToken`，共 **11 条**在标准 ACP 面永远不出现。 其余 131 条为公共可选扩展。

## 4\. `_codebuddy.ai/*` 扩展方法 / 通知全清单（44 条）

ACP 规定自定义方法以下划线前缀 \+ 反向域名命名空间。这些**不是 `_meta` 键**，但共享同一命名空间， 第三方客户端同样需要知道它们的公共 / 私有归属。清单入口：`packages/agent-client-protocol/src/common/types.ts:25-35`。

| 方法名 | 方向 | 分类 | 语义 |
| --- | --- | --- | --- |
| `_codebuddy.ai/question` | A→C（request） | 公共 | HITL 提问，等待客户端应答（`acp-protocol.ts:900`） |
| `_codebuddy.ai/resolveInterruption` | C→A（request） | 公共 | 客户端回答中断请求（`acp-agent.ts:5565-5570`） |
| `_codebuddy.ai/artifact` | A→C（notify） | 公共 | 产物推送（`session-replay.ts:523`） |
| `_codebuddy.ai/command` | A→C（notify） | 公共 | 命令事件（`types.ts:25`） |
| `_codebuddy.ai/checkpoint` | A→C（notify） | 公共 | checkpoint 事件（`session-replay.ts:601`） |
| `_codebuddy.ai/session/rollback` | C→A（request） | 公共 | 会话回滚（`acp-agent.ts:5812`） |
| `_codebuddy.ai/session/rollbackFiles` | C→A（request） | 公共 | 文件级回滚 |
| `_codebuddy.ai/session/previewFileRollback` | C→A（request） | 公共 | 回滚预览 |
| `_codebuddy.ai/file_history_snapshot` | A→C（notify） | 公共 | 文件历史快照（`types.ts:29`） |
| `_codebuddy.ai/fileTreeChanged` | A→C（notify） | 公共 | 文件树变更（须带 filePath） |
| `_codebuddy.ai/authUrl` | A→C（notify） | 公共 | 登录跳转 URL（`types.ts:27`） |
| `_codebuddy.ai/getUserInfo` | C→A（request） | 公共 | 拉取用户信息（`acp-agent.ts:5578`） |
| `_codebuddy.ai/uiControl` | A→C（request） | 公共 | UI 控制指令（`types.ts:35`） |
| `_codebuddy.ai/system_init` | A→C（notify） | 公共 | 系统初始化通知 |
| `_codebuddy.ai/tool_input` | A→C（request） | 公共 | 工具输入征询（`agent-provider/examples/question-example.ts:16`） |
| `_codebuddy.ai/delegateTool` | A→C（request） | 公共 | 工具代理执行（`delegate-tool-manager.ts:299`） |
| `_codebuddy.ai/delegateToolsChanged` | C→A（notify） | 公共 | 客户端可代理工具集变更（`acp-agent.ts:5580`） |
| `_codebuddy.ai/refreshPlugins` | C→A（request） | 公共 | 请求刷新插件（`acp-agent.ts:5584`） |
| `_codebuddy.ai/plugins_changed` | A→C（notify） | 公共 | 插件集变更 |
| `_codebuddy.ai/mcp_servers_changed` | A→C（notify） | 公共 | MCP server 集变更 |
| `_codebuddy.ai/models_changed` | A→C（notify） | 公共 | 模型列表变更 |
| `_codebuddy.ai/product_config_changed` | A→C（notify） | 公共 | 产品配置变更 |
| `_codebuddy.ai/identity_changed` | A→C（notify） | 公共 | 身份变更广播（主进程写入后广播到所有 live session） |
| `_codebuddy.ai/queue_state_changed` | A→C（notify） | 公共 | 队列状态变更 |
| `_codebuddy.ai/message_queue_snapshot_changed` | A→C（notify） | 公共 | 消息队列快照变更 |
| `_codebuddy.ai/automation_snapshot` | A→C（notify） | 公共 | automation 快照 |
| `_codebuddy.ai/interaction_timeout` | A→C（notify） | 公共 | 交互超时（`cloud-agent-event-bridge.ts:10`） |
| `_codebuddy.ai/teams` | A→C（notify） | 公共 | Team SSE 事件（`use-collab-queue.ts:5`） |
| `_codebuddy.ai/conversation` | A→C（notify） | 公共 | 会话事件（`use-conversation-events.ts:50`） |
| `_codebuddy.ai/mcpUiCallTool` | C→A（request） | 公共 | MCP\-UI 反向 tools/call |
| `_codebuddy.ai/mcpUiReadResource` | C→A（request） | 公共 | MCP\-UI 读资源 |
| `_codebuddy.ai/mcpUiUpdateModelContext` | C→A（request） | 公共 | MCP\-UI 更新模型上下文 |
| `_codebuddy.ai/mcpUiRequestDisplayMode` | C→A（request） | 公共 | MCP\-UI 请求显示模式 |
| `_codebuddy.ai/mcpUiResourceTeardown` | C→A（request） | 公共 | MCP\-UI 资源释放 |
| `_codebuddy.ai/respondToSandboxIntercept` | C→A（request） | 公共 | 应答沙箱拦截（`codebuddy-code-backend.ts:1909`） |
| `_codebuddy.ai/admitControl` | C→A（request） | **私有** | control Session 准入。process\-login 组合根直接 `throw`（`process-login-acp-admission-service.ts:87-90`），仅 `workbuddy-host-sidecar` 用 |
| `_codebuddy.ai/runtimeCredentialUpdate` | C→A（request） | **私有** | per\-session exact 凭据更新（`acp-agent.ts:5595`） |
| `_codebuddy.ai/runtimeControlCredentialUpdate` | C→A（request） | **私有** | control binding 凭据更新（`acp-agent.ts:5597`） |
| `_codebuddy.ai/runtimeOwnerCredentialUpdate` | C→A（request） | **私有** | owner 级批量凭据更新（`acp-agent.ts:5599`），对应 `bulkApplyExactCredentialUpdates` |
| `_codebuddy.ai/activateWorkbuddyOwnerRuntime` | C→A（request） | **私有** | **C3 新增**：向 workbuddy\-single 进程注入一次 owner 授权（authSession \+ product 材料 \+ 凭据句柄），此后 `session/new` 零身份 meta。载荷 \= `{proof, processInstanceId, handshakeNonce, runtimeConfigSha256, ownerGeneration}`，验证点 `workbuddy-admission-security.ts` `activateOwnerRuntime` |
| `_codebuddy.ai/activateCompletionRuntime` | C→A（request） | **私有** | 激活 completion warm 运行时；**C3 起 claims 追加 `credentialMaterial`**，同时承担 warm 侧的进程级 owner 注入，且凭据刷新后会以同 ownerGeneration、新 proof 重复调用（整体替换语义） |
| `_codebuddy.ai/completionDispatch` | C→A（request） | **私有** | 分发一次 completion（`acp-agent.ts:5738`） |
| `_codebuddy.ai/completionRuntimeDiagnostics` | C→A（request） | **私有** | completion 运行时诊断（`acp-agent.ts:5708`） |
| `_codebuddy.ai/disposeEphemeralSession` | C→A（request） | **私有** | 销毁 ephemeral session（`acp-agent.ts:5676`） |
| `_codebuddy.ai/disposePersistentSession` | C→A（request） | **私有** | 销毁 persistent session（`acp-agent.ts:5705`） |
| `_codebuddy.ai/example` | —— | —— | **测试用占位方法名**，仅出现在 `workbuddy-server/src/server-owned-handlers.spec.ts:2113`，无生产实现 |

> 表内 46 行 \= 44 个 grep token \+ `session/rollbackFiles` / `session/previewFileRollback` 两个子路径 （它们与 `session/rollback` 共享 token `codebuddy.ai/session`，grep 只算一次）。

## 5\. 非键命中（9 条）

### 5\.1 命名空间前缀 / 通配写法（3 条）

| token | 出现形态 | 说明 |
| --- | --- | --- |
| `codebuddy.ai/` | `startsWith('codebuddy.ai/')` / `startsWith('_codebuddy.ai/')` | 命名空间前缀本身。守卫点：`workflow-acp-bridge.spec.ts:82`、`sandbox-proxy/src/handler/artifacts-proxy.ts:70`、`sandbox-proxy/src/replay/replay.ts:1047` |
| `codebuddy.ai/workflow` | 注释里的 `codebuddy.ai/workflow*` | 键空间通配写法（`workflow-acp-bridge.ts:146`），不是独立键 |
| `codebuddy.ai/mcpUi` | 注释里的 `_codebuddy.ai/mcpUi*` | 5 个 MCP\-UI 扩展方法的通配写法（`mcp-apps-extmethod.spec.ts:4`） |

### 5\.2 产品站 URL 路径伪命中（6 条）

以下 token 出自 `https://www.codebuddy.ai/...` / `https://code.codebuddy.ai/...` 这类 URL，与协议无关：

| token | 出处 |
| --- | --- |
| `codebuddy.ai/docs` | `keybinding-template.ts:18,52`、`mcp-approval-box.tsx:16` |
| `codebuddy.ai/schemas` | `keybinding-template.ts:17,51` |
| `codebuddy.ai/login` | `chat-ui/src/browser/login/login.tsx:149` |
| `codebuddy.ai/agents` | `agent-ui/src/utils/workbuddy-share-origin.spec.ts:312` |
| `codebuddy.ai/profile` | `use-error-banner.tsx:186`（`.../profile/plan`） |
| `codebuddy.ai/v2` | `model-provider.spec.ts:454,520`（API baseURL） |

## 6\. 给第三方 ACP 客户端的规则

1. **不要生产任何 `codebuddy.ai/*` `_meta` 键来做身份或准入**。§3\.1 标注为「私有」的键由 CodeBuddy 内部 组合根签发，客户端自造只会被拒（envelope 校验、digest 比对、fencing 全都过不去）。
2. **可以安全读取所有「公共」键，并按需忽略**。它们全部是可选增量信息，语义变化不会破坏基础 ACP 流程。
3. **`session/prompt` 上可选携带的关联 ID**（`requestId` / `messageId` / `messageRequestId` / `userMessageId` / `promptRequestId` / `clientRequestId` / `sendTime` / `traceparent`）是唯一推荐客户端 主动生产的一组——它们只影响埋点与链路串联，不参与任何鉴权判断。
4. **`_codebuddy.ai/*` 扩展方法**：§4 里标注「私有」的 9 个（`admitControl` \+ 三个 `runtime*CredentialUpdate`
	- completion 三件套 \+ dispose 两件套）只在 WorkBuddy 内部通道出现，标准面调用会被拒绝。

## 7\. 相关文档

- [ACP 协议集成](./acp) —— `--acp` 启动方式、Zed 配置、协议特性
- 零 `_meta` 常驻 e2e：`src/e2e/acp-zero-meta-contract.spec.ts`
- 准入契约实现：`src/node/session/runtime-admission-acp-adapter.ts`、 `src/node/session/process-login-acp-admission-service.ts`、 `src/node/session/multi-owner-acp-admission-service.ts`
- profile 注册表：`packages/runtime-admission-protocol/src/runtime-admission-contract.ts`