# Mods

> **状态**：Beta。API 与运行时约束仍在演进；默认开启，无需任何环境变量，`--plugin-dir` 装载即可使用。 **与传统 Hooks 的关系**：不替换。传统 shell / prompt hooks（见 [`hooks.md`](./hooks)）继续可用；Mods 是并行的、类型化的中间件层，两者可同时启用。

![Mods](https://iili.io/nEwXhpR.png)

**Mods 是 CodeBuddy Code 引擎关键路径上的 TypeScript 中间件层。** 引擎把工具调用、命令、Prompt 组装、Session 生命周期、UI 渲染等关键路径暴露成一组带类型的事件，你写一个 `register.ts` 就能对每个事件做：

- **观察**（打日志、埋点）
- **改写**（在参数进模型前修一句、在工具结果发出前压缩或脱敏）
- **拒绝**（在工具真正执行前 `{ deny }` 短路）
- **替换**（返回 `{ value }` 顶替宿主默认实现）
- **加能力**（往 `$` 上挂一个自己的 noun，供其他 Mod 或后续代码调用）

每个这样的扩展称为一个 **Mod**：目录里放一个 `plugin.json` \+ 一份 `hooks/register.ts`，`--plugin-dir` 装载即用。同一个 Mod 同时运行在终端（TUI）、Web UI、Desktop 以及任何实现了对应 ACP 扩展消息的客户端上（见[跨面机制](#跨面机制acp-扩展)）。

---

## 典型示例

下面几个例子覆盖了 Mods 最常见的用法，每个都是一份独立的 `hooks/register.ts`，可以直接拷走改。

### 示例一：常驻面板与输入框控制

Mod 可以持续提供操作面板，把按钮动作写回输入框或直接提交。终端热键与 Web 点击使用同一套元素 key 和事件协议。

**TUI 动态演示**

![Mods 常驻面板与输入框控制 - TUI 动态演示](https://iili.io/n7EaX7n.gif)

**Web UI**

![Mods 常驻面板与输入框控制 - Web UI](https://iili.io/n7EAkTQ.png)

### 示例二：危险命令二次确认（自定义问答）

拦截 `rm -rf`，调用跨端 UI 让用户确认；拒绝后工具根本不会执行：

ts
```
import type { On } from 'codebuddy-code';

export function register(on: On): void {
  on('tool.call', { tool: 'Bash' }, async ($, e, next) => {
    const cmd = String((e.input as { command?: unknown })?.command ?? '');
    if (/\brm\s+-rf\b/.test(cmd)) {
      const answer = await $.ui.ask(`About to run "${cmd}". Continue?`, ['yes', 'no']);
      if (answer !== 'yes') {
        return { deny: 'user cancelled rm -rf' };
      }
    }
    return next(e);
  });
}
```
调用同一个 `$.ui.ask`，TUI 使用终端选择器，Web UI 使用原生表单，答案最终回到同一条 Hook 链。

**TUI**

![Mods 自定义问答 - TUI](https://iili.io/n7EAj3u.png)

**Web UI**

![Mods 自定义问答 - Web UI](https://iili.io/n7EAwYb.png)

### 示例三：团队护栏策略

禁用 `git reset --hard`，并要求 `pnpm install` 只能在仓库根目录执行：

ts
```
export function register(on: On): void {
  on('tool.call', { tool: 'Bash' }, async ($, e, next) => {
    const cmd = String((e.input as { command?: unknown })?.command ?? '');
    const root = await $.session.root();
    const cwd = await $.session.cwd();

    if (/\bgit\s+reset\s+--hard\b/.test(cmd)) {
      return { deny: 'org policy: git reset --hard is disabled; use git stash' };
    }
    if (/\bpnpm\s+install\b/.test(cmd) && root !== cwd) {
      return { deny: `run pnpm install at repo root (${root}), not ${cwd}` };
    }
    return next(e);
  });
}
```
把 Mod 放进共享 git 仓库，团队每个人 `codebuddy --plugin-dir .../team-guard` 即可生效。

### 示例四：自定义 ToolResult 渲染

工具结果不再局限于纯文本；同一份结构化结果可以由不同宿主映射为适合自己的展示。

**TUI**

![Mods 自定义 ToolResult 渲染 - TUI](https://iili.io/n7EAWG9.png)

**Web UI**

![Mods 自定义 ToolResult 渲染 - Web UI](https://iili.io/n7EANvj.png)

### 示例五：ToolResult 安全脱敏

在工具结果进入上下文和 UI 之前，把 `sk-` 前缀的密钥统一替换为 `[REDACTED]`，对内置工具与 MCP 工具同时生效：

ts
```
export function register(on: On): void {
  on('tool.call', async ($, e, next) => {
    const r = await next(e);
    if (typeof r.result === 'string') {
      return { ...r, result: r.result.replace(/\bsk-[A-Za-z0-9_-]{16,}/g, '[REDACTED]') };
    }
    return r;
  });
}
```
下面的 TUI 示例中，两个 `sk-` 前缀密钥已替换为 `[REDACTED]`，普通文本保持不变：

![Mods 对 ToolResult 做密钥脱敏](https://iili.io/n7EAX4e.png)

同一返回路径也可以用来压缩长输出：当 `r.result` 过长时调用 `$.model.complete` 生成摘要再返回，单点接入即可对所有工具生效。

### 示例六：把团队知识源接进上下文

让 `TEAM.md`、`docs/PLAYBOOK.md` 这类文件在每次会话首个 user message 里“永远看得见”：

ts
```
on('prompt.context', async ($, e, next) => {
  const root = await $.session.root();
  if (root === undefined) return next(e);

  const found = await $.fs.ancestors({
    names: ['TEAM.md', 'docs/PLAYBOOK.md'],
    below: root,
  });
  const added = (e.instructionFiles ?? []).concat(
    found.map(a => ({ path: `${a.dir}/${a.name}`, content: a.content }))
  );
  return next({ ...e, instructionFiles: added });
});
```
### 示例七：生成式 UI，模型输出 XML，Mod 画成可交互卡片

Mod 给模型约定一套 XML 输出规则，再接管 Web UI 的助手消息渲染：回复里的 `<genui:menu>`、`<genui:order/>` 被画成菜单、购物车、订单卡片，按钮点击回到 Mod 执行。下面是真实模型下的「点餐 → 下单 → 退单」全流程：

**Web UI 动态演示**

![Mods 生成式 UI - 点餐下单退单](https://iili.io/nEwYcyF.gif)

1. 用户说「我想点餐」，模型调用 Mod 注册的 `genui_order_menu` 工具，回复中输出 `<genui:menu>`，消息被替换成菜单卡片；
2. 在卡片上「加入 / ＋」，合计实时刷新；点「下单」生成订单 O\-1001，购物车清空；
3. 用户问「帮我看看订单」，模型调用 `genui_order_list`，输出 `<genui:order id="O-1001"/>`；点「退单」后卡片变为「已退单」。

做法分三步，全部走公开的 Mod 事件：

**① 用 `prompt.section` 教模型一套 XML 输出规则**

ts
```
on('prompt.section', { name: 'rules' }, async ($, e, next) => {
  const beneath = await next(e);
  const base = typeof beneath.text === 'string' ? beneath.text : (e.text ?? '');
  return { ...beneath, text: `${base}\n<system-reminder data-role="genui-order">${GENUI_RULES}</system-reminder>` };
});
```
规则里约定一组固定标签（不允许模型自创）：

| 标签 | 渲染成 |
| --- | --- |
| `<genui:menu title="…"><genui:dish id="…"/></genui:menu>` | 菜单卡片：加入 / ＋ / －，底部合计 \+ 下单 |
| `<genui:cart/>` | 购物车：增减、清空、下单 |
| `<genui:order id="O-1001"/>` | 订单详情；退单时限内带「退单」 |
| `<genui:orders/>` | 订单列表 |
| `<genui:notice tone="success">…</genui:notice>` | 提示条 |

模型只给菜品 id，菜名、价格、订单状态都由 Mod 从自己的数据里取：模型就算写了 `price="1"` 也不会生效。

**② 用 `ui.render { component: 'AssistantMessage' }` 接管助手消息**

tsx
```
on('ui.render', { component: 'AssistantMessage' }, async ($, e, next) => {
  const segments = parseGenui(String(e.text ?? ''));
  if (!hasComponents(segments)) return next(e);   // 没有组件标签：交回默认 Markdown
  const beneath = await next(e);
  return { ...beneath, tree: (
    <Box flexDirection="column" gap={1}>
      {segments.map((s, i) => s.kind === 'markdown'
        ? <Markdown key={`md:${i}`} text={s.text} />
        : componentView(s.node, i))}             // 菜单 / 购物车 / 订单卡片
    </Box>
  ) };
});
```
解析只认自己的闭集标签：未知标签、半截标签、代码块里的标签都原样留给 Markdown。

**③ 用 `ui.press` \+ `tool.call` 闭环交互**

ts
```
on('ui.press', async ($, e, next) => {
  const action = decodeAction(e.element);         // 按钮 key 形如 genui-order:inc:kungpao
  if (!action) return next(e);                    // 不是自己的按钮，交给下一层
  await runAction($, action);                     // 改订单状态 → $.store 持久化
  await $.ui.invalidate('ui.render');             // 已挂载的卡片按最新状态重画
  return { value: { element: e.element } };
});

on('tool.call', { tool: 'genui_order_place' }, async ($, e) => { /* 同一份状态下单 */ });
```
按钮动作编码在元素 `key` 里，闭包不需要跨进程；卡片按钮与模型侧的 `genui_order_*` 工具改的是同一份状态，用户「点按钮」和「对模型说再来一份」效果一致。

---

## 目录

- [典型示例](#典型示例)
- [快速开始](#快速开始)
- [为什么不用传统 Shell Hooks](#为什么不用传统-shell-hooks)
- [核心概念](#核心概念)
	- [Mod \= plugin.json \+ register.ts](#mod-pluginjson-registerts)
	- [Tier 与 `next`](#tier-与-next)
	- [事件家族](#事件家族)
	- [`$` 能力面（Engine Interface）](#能力面engine-interface)
	- [Pattern 与 Matcher](#pattern-与-matcher)
- [装载与运行](#装载与运行)
- [跨面机制（ACP 扩展）](#跨面机制acp-扩展)
- [类型契约](#类型契约)
- [事件参考（速查）](#事件参考速查)
- [`$` API 速查](#api-速查)
- [测试你的 Mod](#测试你的-mod)
- [内置 Mod](#内置-mod)
- [与传统 Hooks 的兼容性](#与传统-hooks-的兼容性)
- [失败隔离与诊断](#失败隔离与诊断)

---

## 快速开始

Mods 默认开启，不需要设置任何环境变量。

### 1\. 创建一个最小 Mod

```
hello-mod/
├── .codebuddy-plugin/
│   └── plugin.json
└── hooks/
    ├── hooks.json
    └── register.ts
```
`plugin.json`：

json
```
{
  "name": "hello-mod",
  "version": "0.1.0",
  "description": "Say hi on every session start"
}
```
`hooks/hooks.json`：

json
```
{
  "description": "hello-mod entrypoints",
  "modules": ["./register.ts"]
}
```
`hooks/register.ts`：

ts
```
import type { On } from 'codebuddy-code';

export function register(on: On): void {
  on('session.start', ($, e, next) => {
    $.ui.log(`hello from hello-mod, cwd=${e.cwd}`);
    return next(e);
  });
}
```
### 2\. 启动 CLI 并加载它

bash
```
codebuddy --plugin-dir ./hello-mod
```
CLI 首屏 stderr 会打印 Mod 装载结果，包括每个 Mod 实际挂上的事件清单。

> **兼容识别**：`.claude-plugin/plugin.json` 与 `.codebuddy-plugin/plugin.json` 均被识别；两者同时存在时以 `.codebuddy-plugin` 为准。官方 Claude Code 生态的 Mod 目录可原样通过 `--plugin-dir` 加载。

---

## 为什么不用传统 Shell Hooks

Shell Hooks 适合简单拦截，但复杂扩展会遇到四个限制：

1. **性能**：每次事件都 fork shell 进程，工具调用密集时会累积明显延迟。
2. **组合**：脚本之间没有 `next`、参数改写和短路语义，多个策略难以稳定协作。
3. **类型**：只有字符串输入和 JSON 输出，复杂逻辑依赖 bash 与 `jq`，难维护、难测试。
4. **跨端 UI**：Shell 脚本无法用同一套代码在终端和 Web UI 中渲染交互界面。

Mods 把这些能力放进同一条类型化中间件链，并让引擎成为唯一的状态与执行入口。

---

## 核心概念

### Mod \= plugin.json \+ register.ts

一个 Mod 的物理形态：

```
my-mod/
├── .codebuddy-plugin/plugin.json     # 身份 { name, version, description, author, types? }
├── hooks/
│   ├── hooks.json                    # { description, modules: ["./register.ts"] }
│   └── register.ts                   # export function register(on, options)
├── types/index.d.ts                  # 可选：为 $ 增加自有 noun 的契约（纯类型）
└── tests/*.test.ts                   # 可选：单元测试
```
`register` 是唯一入口：

ts
```
import type { On, PluginOptions } from 'codebuddy-code';

export function register(on: On, options: PluginOptions): void {
  // 用 on(...) 挂 hooks
}
```
`options` 由宿主注入，来源是 `plugin.json` 或用户配置里的键值对，只能是 `string | number | boolean | readonly string[]`。

### Tier 与 `next`

Mod 组织成一条**中间件链**。链上分五层（tier），外层先执行：

```
prepend → user → append → builtin → core
```

| Tier | 谁在这里 |
| --- | --- |
| `prepend` | 企业**强制最外层**策略（预先绑定） |
| `user` | 用户 / 项目 `--plugin-dir` 装载的 Mod |
| `append` | 企业**兜底**策略（预先绑定） |
| `builtin` | 引擎自带 Mod（`cbc-sec-default` / `cbc-telemetry`） |
| `core` | 引擎自己的行为 |

每个 hook 签名都是**中间件**：

ts
```
type Hook<E> = ($: EngineInterface, e: E, next: Next<E>) => Result | Promise<Result>;
```
`next` 的可选动作：

| 用法 | 作用 |
| --- | --- |
| `next(e)` | 透传，让下一层继续处理 |
| `next({ ...e, mut })` | 改写事件参数后继续 |
| `return { deny: '原因' }` | **短路拒绝**，宿主不再落地 |
| `return { value: ... }` | **短路替换**（op 事件专用） |
| `return { result: ... }` | 顶替 middleware 事件结果 |
| `next.to(e, 'append')` | 跳到指定 tier（只能往内跳） |
| `next.origin` | **调用方**身份 `{ plugin, tier }`，不是自己的 tier |
| `next.signal` | `AbortSignal`：超时 / 短路时被 abort |
| `next.trace` | 每层的执行轨迹（plugin / tier / outcome / ms） |
| `next.budget` | `{ ms, remainingMs }` 剩余预算 |
| `next.is(pattern, e)` | glob hook 内的事件类型守卫 |

多个 Mod 之间自然形成组合关系，谁在外、谁在内由 tier 决定，没有中心化的 `if...else` 负责协调——链本身就是协议。

### 事件家族

事件分两类：

1. **Middleware 事件**（38 个）—— 引擎关键路径的埋点，返回专属结果字段：`tool.call` / `command.run` / `prompt.submit` / `session.start` / `ui.render` / `engine.create` / …
2. **Op 事件**（54 个）—— 每次 `$.<noun>.<op>(...)` 都会先分发同名事件，上层可 `{ value }` 顶替、`{ deny }` 拒绝，否则落到宿主真实实现。这是审计 / 沙箱 / 覆盖能力的核心机制。

除此之外还有 **`classic.<HookEvent>`** 一族：把传统 shell hooks 桥接进这套体系，方便新老共存（见[兼容性](#与传统-hooks-的兼容性)）。

### `$` 能力面（Engine Interface）

`$` 是引擎注入给 hook 的第一个参数，暴露 19 个 noun：

```
plugin  ui   model   audio   mcp   session   turn   prompt   tool
command config agent  fs      store clock     http   process  settings env
```
例如：

ts
```
on('session.start', async ($, e, next) => {
  const cwd = await $.session.cwd();
  const settings = await $.settings.read({ source: 'user' });
  await $.store.set('lastCwd', cwd);
  $.ui.toast(`Session started at ${cwd}`);
  return next(e);
});
```
`$` 上的每一次调用**自身也是事件**，可以被上层拦截或替换。这让「审计每个 Mod 读了什么文件、跑了什么进程、请求了哪个 URL」变成注册几个 `on('fs.read', ...)` / `on('http.fetch', ...)` 就能做到的事。

`$` 在 `engine.create` fold 结束后被冻结，运行时不能挂新 noun。要给 `$` 加自己的 noun，只在 `engine.create` 里通过 fold 返回：

ts
```
on('engine.create', async ($, e, next) => {
  const beneath = await next(e);
  return { ...beneath, mytoolkit: { hello: () => 'hi' } };
});
```
### Pattern 与 Matcher

`on(pattern, hook)` 或 `on(pattern, matcher, hook)` 支持四种 pattern：

| 形态 | 例子 |
| --- | --- |
| 具名事件 | `on('tool.call', ...)` |
| 命名空间 glob | `on('classic.*', ...)` / `on('ui.*', ...)` |
| 全局 glob | `on('*', ...)`（审计 / 日志） |
| 否定 | `on('!tool.call', ...)`（排除某事件） |

matcher 支持深度匹配：

ts
```
on('tool.call', { tool: 'Read' }, ($, e, next) => next(e));                 // 值相等
on('tool.call', { tool: ['Read', 'Grep'] }, ...);                            // 数组任一
on('tool.call', { tool: /^Web/, input: { headers: {...} } }, ...);           // RegExp / 深嵌套
on('tool.call', { tool: v => v.startsWith('mcp__') }, ...);                  // 谓词
on('agent.spawn', { fork: true }, ...);                                      // 布尔
```

---

## 装载与运行

### CLI 参数

bash
```
codebuddy --plugin-dir <dir> [--plugin-dir <dir2> ...]
```
- `--plugin-dir` 可以重复，按声明顺序装载。
- 目录须包含 `.codebuddy-plugin/plugin.json` 或 `.claude-plugin/plugin.json`（两者同存以前者优先）。
- 用户手动装载的 Mod 全部落到 **`user` tier**。
- 无需额外开关或环境变量。

### 运行时通道

Mod 的 `register.ts` 是 TypeScript 源码。CLI 在三条通道里自动选：

1. **原生**（Bun 等）—— runtime 本身支持 TS \+ Bun 式模块解析。
2. **Node 内建**（22\.15\+）—— `module.registerHooks()` 补齐目录 import 与 `.js`→`.ts` 解析，`process.features.typescript` 擦掉类型注解。
3. **转译器**（esbuild，可选依赖）—— 含 JSX / 老 Node（20\.x 等）自动降级。

含 JSX 的 Mod（例如做自定义面板）**必须**走转译器通道。

产物会按内容寻址落到 `${CODEBUDDY_CONFIG_DIR:-~/.codebuddy}/cache/mods/<key>.mjs`，命中缓存靠 `mtime + size` 比对，不重新读文件内容。

---

## 跨面机制（ACP 扩展）

Mods 的 UI 面**不是终端专用**。CodeBuddy Code 在 [Agent Client Protocol (ACP)](./acp) 上定义了一组 `_codebuddy.ai/mod*` 扩展消息，把 Mod 的 UI 与交互抽象成“两个方向的可序列化消息”：

| 方向 | 消息 | 用途 |
| --- | --- | --- |
| Agent → Client | `_codebuddy.ai/modRender` (extNotification) | 推送 `ui.render` 返回的元素树 |
| Agent → Client | `_codebuddy.ai/modRenderFold` (extNotification) | 推送到具名 slot / Pane 的分块树 |
| Client → Agent | `_codebuddy.ai/modRenderRequest` (extMethod) | 客户端挂载后主动 pull 一次首帧 |
| Client → Agent | `_codebuddy.ai/modPress` (extMethod) | Button 按下 / TUI hotkey 命中 |
| Client → Agent | `_codebuddy.ai/modInput` (extMethod) | Input 组件变化 |
| Client → Agent | `_codebuddy.ai/modSelect` (extMethod) | Select 组件变化 |
| Client → Agent | `_codebuddy.ai/modFocus` (extMethod) | 焦点移动 |
| Client → Agent | `_codebuddy.ai/modScroll` (extMethod) | 视口滚动 |

**序列化规则**：

- `ui.render` 返回的树中，函数型 prop（`onPress` / `onInput` / `onChange` / `onSelect` / `onFocus` / `onScroll`）被摘掉，树上只留元素 `key`；
- 元素表是**闭集**：`Box` / `Text` / `Button` / `Input` / `Select` / `Link` / `Code` / `Markdown` / `Image` / `Svg` / `Raster` / `Client`。未知 tag 在序列化这一层就被挡住；
- 交互回传时按 key 找回原始闭包，**在 agent 侧、Mod 自己的执行环境里跑**——客户端不承载业务逻辑，也不需要理解 Mod 内部状态。

**首帧同步**（重要）：Web UI / ACP 客户端连上时，agent 侧可能已经画完帧了。客户端在挂完 `modRender` 监听后**主动发一次** `_codebuddy.ai/modRenderRequest`，agent 现算 snapshot 通过 `modRender` extNotification 回推。这保证“晚到的客户端”也能看到当前状态。

### 已接线的面

| 面 | 状态 |
| --- | --- |
| TUI（终端 / Ink） | ✅ hotkey → `ui.press`；本地绘制；`Input` / `Select` 只读显示（终端 raw stdin 归 chat InputBox 独占） |
| Web UI（`GET /acp` SSE \+ ACP） | ✅ `Button` / `Input` / `Select` / focus 全部通；DOM `onScroll` 通道已挂但暂未启用节流 |
| Desktop 壳 / VSCode 插件 | 🚧 走同一套 ACP 扩展，接线中；已能加载并 push 首帧 |
| 第三方 ACP 客户端 | ✅ 只要实现上表的 extMethod / extNotification handler，即可承载 Mod UI |

### 写 Mod 需要注意什么

对 Mod 作者来说：**面不用感知**。写一次 `on('ui.render', ...)`，`$.ui.log/toast/status/ask` 用同一套 API，宿主决定推给哪些面。禁止的只是把闭包塞到 tree 里非白名单的地方（会被序列化摘除），以及依赖客户端记住状态（客户端只画树，状态是 agent 侧的）。

---

## 类型契约

Mod 写 `register.ts` 时用：

ts
```
import type { On, Register, PluginOptions } from 'codebuddy-code';
```
`codebuddy-code` 的类型声明**随 CLI 的 npm 包一起发布**，一个自包含的 `codebuddy-code.d.ts` 文件躺在 CLI tarball 的 `types/` 里，文件本身自带 `declare module 'codebuddy-code' { … }` 包裹。你不需要额外装第二个 npm 包、不用配 `paths`、也不会有 `.d.ts` 被写到你的项目下。

Mod 作者自己写 `tsconfig.json`，把这份声明挂到 `types` 字段（TS 会通过 node\_modules 子路径解析到自带 namespace 的那份 .d.ts）：

jsonc
```
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "jsx": "preserve",
    "strict": true,
    "types": ["@tencent-ai/codebuddy-code/types/codebuddy-code"]
  },
  "include": ["hooks/**/*.ts", "hooks/**/*.tsx"]
}
```
之后 `import type { On } from 'codebuddy-code'` 直接可解析、`<Box><Button hotkey="p"/></Box>` 也能通过类型检查（`codebuddy-code.d.ts` 首行的 `/// <reference path="./codebuddy-code-globals.d.ts" />` 会把 JSX 命名空间和 `Box`/`Text`/`Button` 等闭表标签函数一同带进来，不用再单独引一份；`<Box>` → `SerializedElement` 的运行时转换发生在 `--plugin-dir` 装载时，声明只提供类型形状）。

想给 `$` 加自己的 noun（如 `$.mytoolkit`），用声明合并：

ts
```
// hooks/mytoolkit.d.ts
export interface MyToolkit {
  hello(): string;
}

declare module 'codebuddy-code' {
  interface EngineInterface {
    mytoolkit: MyToolkit;
  }
}
```
在 `tsconfig.json` `include` 里带上这个 `.d.ts` 即可；其他挂载了 `$.mytoolkit` 的 Mod 只要 `import type { MyToolkit } from '...'` 也能看到同一份类型。

---

## 事件参考（速查）

### Middleware 事件

| 分组 | 事件 | 用途 |
| --- | --- | --- |
| **Tool** | `tool.call` | 拦截 / 改写 / 拒绝工具调用；`{ deny }` 阻止，`{ result }` 顶替结果 |
|  | `tool.check` | 权限决策，`{ decision, reason?, rule? }` |
|  | `tool.describe` / `tool.list` / `tool.register` | 描述缓存、清单渲染、注册准入 |
| **Command** | `command.run` / `command.describe` | 斜杠命令执行 / 清单 |
| **Prompt** | `prompt.submit` | 用户输入进入 turn 前的最后改写点 |
|  | `prompt.section` / `prompt.context` / `prompt.attachment` | 系统提示分节 / 首个 user message context / 附件 |
|  | `prompt.fill` / `prompt.suggest` / `prompt.edit` | 输入框写字 / 候选 / 编辑 |
|  | `skill.prompt` / `attribution.text` | Skill 拼装、commit / PR 归属文案 |
| **Session** | `session.start` / `.end` / `.attach` / `.detach` / `.receive` / `.compact` / `.measure` | 生命周期 |
| **Turn** | `turn.start` / `turn.step` / `turn.complete` | 每次模型交互 |
| **Agent** | `agent.offer` / `agent.spawn` | 子 agent 类型可见性、模型解析 |
| **Config** | `config.set` / `config.describe` | `/config` 行写入 / 清单 |
| **UI** | `ui.render` / `.resolve` / `.press` / `.input` / `.select` / `.message` / `.scroll` / `.focus` | 组件树 / 交互 / 视口 |
| **Plugin/Engine** | `plugin.register` / `engine.create` | plugin 入场（可 refuse） / 装配 fold `$` |
| **Legacy** | `classic.<HookEvent>` | 老 shell hooks 桥接（每一个老事件对应一个 `classic.*`） |

### Op 事件

`$.<noun>.<op>()` 每次调用对应一个同名 op 事件；它是短路模型（`{ value }` 顶替 / `{ deny }` 拒绝 / 返回 `undefined` 视为不干预）。覆盖 54 个 op，例如：

`model.complete` · `mcp.call` · `session.messages` · `tool.list` / `.register` · `command.list` / `.register` · `agent.list` / `.register` · `ui.toast` / `.status` / `.log` / `.notice` / `.open` / `.close` / `.blit` / `.invalidate` · `fs.read` / `.write` / `.list` / `.stat` / `.exists` / `.ancestors` · `store.get` / `.set` / `.delete` / `.keys` · `clock.now` / `.sleep` / `.after` / `.every` · `http.fetch` · `process.run` · `env.get` / `.set` · `settings.read` · `session.cwd` / `.root` / `.model` / `.id` / …

---

## `$` API 速查

按 noun 分组的最常用方法（完整签名以 `codebuddy-code.d.ts` 为准）：

| Noun | 方法 |
| --- | --- |
| `$.plugin` | `name: string` · `root: string` |
| `$.session` | `id()` · `cwd()` · `root()` · `model()` · `turns()` · `messages()` · `surfaces()` · `usage()` · `authorize()` · `compact()` |
| `$.turn` | `abort()` |
| `$.prompt` | `submit()` · `read()` · `fill()` · `suggest()` |
| `$.tool` | `list()` · `call()` · `check()` · `register(spec)` |
| `$.command` | `list()` · `run()` · `register(spec)` |
| `$.agent` | `list()` · `spawn()` · `register(spec)` |
| `$.config` | `list()` · `set()` |
| `$.settings` | `read({ source? })` |
| `$.fs` | `read(path)` · `write(path, text)` · `list(path?)` · `exists(path)` · `stat(path, opts?)` · `ancestors({ names, of?, below? })` |
| `$.store` | `get(key)` · `set(key, value)` · `delete(key)` · `keys()` |
| `$.clock` | `now()` · `sleep(ms)` · `after(ms, fn)` · `every(ms, fn)` |
| `$.http` | `fetch(url, init?)`（当前 CLI 未开放，见下方说明） |
| `$.process` | `run(argv, init?)`（当前 CLI 未开放，见下方说明；走 `execFile` 而非 shell） |
| `$.env` | `get(name)` · `set(name, value)` |
| `$.ui` | `log()` · `status()` · `toast()` · `notice()` · `ask()` · `open()` · `close()` · `panes()` · `scroll()` · `focus()` · `invalidate()` · `resolve()` · `blit()` |
| `$.model` | `complete()` · `classify()` · `fork()` |
| `$.mcp` | `call(server, tool, args?)` |
| `$.audio` | `play()` · `speak()` |

**暂未开放的两个能力**：`$.http.fetch` 与 `$.process.run` 让第三方 Mod 代码出网 / 起子进程，风险不对等，不应由「忘了配置」默认打开。当前版本 CodeBuddy Code 不提供开启这两项能力的配置项或环境变量，调用会以 `{ deny: '$.http.fetch is unavailable: ...' }` 的形式明确回报，不做静默 undefined。

---

## 测试你的 Mod

ts
```
import { describe, expect, mock, test, tier } from 'codebuddy-code/testing';

tier('user');

describe('guard-rm', () => {
  test('blocks rm -rf', async ($, on) => {
    mock.clock(on);
    on('ui.ask', () => ({ value: 'no' }));

    const result = await $.tool.call({
      tool: 'Bash',
      input: { command: 'rm -rf /tmp/x' },
    });
    expect(result.deny).toBeTruthy();
  });

  test('lets safe commands through', async ($, on) => {
    on('ui.ask', () => ({ value: 'yes' }));
    on('tool.call', () => ({ result: { stdout: 'ok', stderr: '', exitCode: 0 } }));

    const result = await $.tool.call({
      tool: 'Bash',
      input: { command: 'echo hi' },
    });
    expect(result.result.stdout).toBe('ok');
  });
});
```
关键点：

- `tier(t)` 声明被测 Mod **所在层**；`test(name, ($, on) => ...)` 里的 `on` 是**世界那一层**（在被测 Mod 更外面），用它桩接任何 `$` 调用。
- 未桩接的 `$` 调用**抛错并命名事件** —— 逼你在测试里显式把边界画出来，避免「测试看着过、真实环境挂」。
- `mock.clock(on)` / `mock.env(on, {...})` / `mock.store(on, {...})` 是常用桩。

---

## 内置 Mod

CLI 自带两个 Mod，坐 **`builtin` tier**（在 user 之内，可以被用户装的 Mod 观察 / 改写 / 覆盖）：

### `cbc-telemetry`

- 只 hook `engine.create`，往 `$` 上加一个 `$.telemetry` noun：`log(name, data?)` / `mark(name, data?)` / `rows()` / `flush()`。
- 计数落 `$.store`，会话结束自动 `flush`；`$.store` 按 plugin 隔离，键不会撞上其他 Mod。
- 官方生态里 Mod 常常把 `$.telemetry` 调用写成「可能为空」的容错分支，内置一份让埋点路径**始终是通的**，而不是「看起来在跑其实什么都没记」。

### `cbc-sec-default`

- 只拦「几乎不可能有正当理由」的路径，其余一律放行：
	- `fs.read` 与 `fs.write` 都拦：SSH 私钥、AWS/K8s/GnuPG/gh 凭据、`.env`、浏览器登录数据、`.netrc`；
	- `fs.write` 额外拦：shell 启动文件（`.bashrc` / `.zshrc` / `.zprofile` / `.zshenv` 等）—— 往里写一行就是持久化任意代码执行。
- 拒绝原因都带上本 Mod 名字与命中的类别，避免用户以为是文件系统错误。
- 坐 builtin tier，因此**可被用户覆盖**：真正不可绕过的边界在宿主自己的权限系统（`PreToolUse` hook、permission mode），那一层 Mod 动不了。内置策略是**缺省值**不是沙箱。

---

## 与传统 Hooks 的兼容性

Mods **不替换**传统 hooks。两者协作：

| 传统资产 | 现在的位置 | Mods 侧 |
| --- | --- | --- |
| `settings.json` 里的 `hooks` | shell 命令 \+ matcher | 不变。老配置继续按老语义跑 |
| `HookEvent.PreToolUse` / `.PostToolUse` / … | 老枚举 | 每一个老事件对应一个 `classic.<HookEvent>` 中间件事件 |
| `HookOutput` JSON 协议（`decision:'block'` / `continue:false` / exit 2） | 老脚本继续解析 | Legacy adapter 保留完整 JSON 序列化路径；`decision:'block'` / exit 2 会被翻译成 `{ deny }` |
| `--plugin-dir` 的老 shell hook 目录 | `hooks/hooks.json` 里没有 `modules` | 走老通道 |
| `--plugin-dir` 的 Mod | `hooks/hooks.json.modules` 存在 | 走 Mods 通道 |

---

## 失败隔离与诊断

`--plugin-dir` 位于 CLI 启动链上，Mod 出错**绝不阻塞宿主**。分层兜底：

| 出错的位置 | 后果 | 报告字段 |
| --- | --- | --- |
| 目录不是 Mod / manifest 读不出 / TS 加载失败 | 其余目录照常 | `skipped[]` |
| 某 Mod 的 `register()` 抛错 | **该 Mod 已注册的 hook 全部回滚**，其余 Mod 照常 | `failures[]` phase\=`register` |
| 某 Mod 的 `engine.create` fold 想替换核心 noun | 该 noun 换回核心原值，其他 Mod 与宿主照常拿到 `$` | `failures[]` phase\=`engine.create` |
| 任何未预料异常 | 就地咽下并记日志 | logger.error |

启动时 stderr 会打印一份加载报告，包括每个 Mod 的：源目录、命中的 manifest（`.codebuddy-plugin` / `.claude-plugin`）、实际挂上的事件清单、跳过 / 失败原因。用户显式提了 `--plugin-dir`，因此加载了什么、为什么没加载**必须看得见**；未装载任何 Mod 时默认路径一行不多。

### 运行时约束

| 项 | 值 |
| --- | --- |
| 单个 hook 预算 | `10_000` ms |
| `.catch(handler)` 预算 | `1_000` ms |
| Linger（返回后仍在跑的 `next`） | `5_000` ms |
| 超时 / 抛错形态 | `HookFailure { kind: 'throw' | 'timeout', message?, budget }` |
| `next.signal` | `AbortSignal`：超时 / 短路时被 abort |
| 坏 hook 不阻断链 | 无 `.catch` 时按未干预继续下游 |

单条 hook 想吃掉自己的错误，用 `Registration.catch`：

ts
```
on('tool.call', async ($, e, next) => {
  const r = await next(e);
  throw new Error('boom');
}).catch(($, e, next) => {
  // next.error 里有 HookFailure，next.called 告诉你有没有跑过 next
  return undefined; // 视为未干预
});
```

---

## 参考

- 传统 shell / prompt hooks：[`hooks.md`](./hooks)
- 插件目录结构与市场：[`plugins.md`](./plugins) · [`plugins-reference.md`](./plugins-reference)
- CLI 参考（`--plugin-dir` 等）：[`cli-reference.md`](./cli-reference)
- Agent Client Protocol（跨面通道）：[`acp.md`](./acp)
- Web UI（浏览器面接入）：[`web-ui.md`](./web-ui)
- 权限系统（真正不可绕过的边界）：[`permissions.md`](./permissions) · [`permission-modes.md`](./permission-modes)