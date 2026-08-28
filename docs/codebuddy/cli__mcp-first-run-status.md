# stdio 常驻模式：首个 prompt 的 MCP 加载状态（mcp\_status）

> 适用：以 `stdio + stream-json` 长连接方式把 `codebuddy` 当子进程调用的接入方 （SDK / daemon / IDE 后端）。目标：**新建会话发出第一个 prompt 时，实时拿到"正在 阻塞本次 prompt 的 MCP 连接状态"**，并可按需**调大首轮预热（prewait）超时窗口**。

## TL;DR

1. 以 stream\-json 长连接启动（**不要带 `-p`**）：bash
```
codebuddy --input-format stream-json --output-format stream-json -y \
  --mcp-config /path/to/mcp.json --strict-mcp-config
```
2. 想让某个 MCP 的加载被展示，就让它**真正阻塞首个 prompt**——在 `mcp.json` 里给它加 `"alwaysLoad": true`（或 `"defer_loading": false`）。纯 defer 的 MCP 首轮不阻塞、也不展示。
3. 调大首轮预热窗口（stdio 默认 **2000ms**）：bash
```
CODEBUDDY_FIRST_RUN_MCP_PREWAIT_TIMEOUT_MS=30000 codebuddy --input-format stream-json ...
```
4. 发出第一条 user 消息后，stdout会按ndjson 逐条吐出： `{type:"system", subtype:"mcp_status", event:"start"|"server"|"finish", ...}`。

---

## 1\. 启动方式（stdio 常驻）

bash
```
codebuddy \
  --input-format stream-json \
  --output-format stream-json \
  -y \
  --mcp-config /abs/path/to/mcp.json \
  --strict-mcp-config
```
要点：

- **不能带 `-p`**。`-p`（print）是单次请求模式，不会输出 mcp\_status；只有 stream\-json 长连接模式才会把 mcp\_status 转发到 stdout。
- **无需先发 `initialize`**：发出**首个 user 消息**时，CLI 会自动进入已初始化状态并触发 首轮 prewait，从而输出 mcp\_status。
- 首个 user 消息的 shape（与ACP/SDK 客户端一致）：json
```
{"type":"user","message":{"role":"user","content":[{"type":"text","text":"hi"}]}}
```

---

## 2\. 让MCP 的加载被"展示" \= 让它真正阻塞首个 prompt

**展示集合恒等于真正阻塞首个 prompt 的集合**（PR \#84819 起对齐）。一个 MCP 是否阻塞首个 prompt，取决于它是否进入 prewait 名单：

| mcp.json 里的写法 | 是否进 prewait 名单（阻塞 \+ 展示） |
| --- | --- |
| `"alwaysLoad": true` | ✅ 是（最直接，第一优先级，绕过defer 判定） |
| `"defer_loading": false` | ✅ 是（server 级显式声明为 inline） |
| 不写（默认 defer） | ❌ 否——首轮不阻塞（模型要用时自己调 `ToolSearch`/`WaitForMcpServers`），**不展示** |

示例 `mcp.json`（让`slow-mcp` 阻塞并展示）：

json
```
{
  "mcpServers": {
    "slow-mcp": {
      "type": "stdio",
      "command": "node",
      "args": ["/path/to/slow-mcp.mjs"],
      "alwaysLoad": true
    }
  }
}
```

> 为什么这样设计：全 defer 的 MCP 首轮本就不该拖慢 prompt，所以不阻塞也不显示——"展示什么， 就是在等什么"，不会给接入方虚假的"正在加载 N 个"却其实没等的错觉。

---

## 3\. 调大首轮预热（prewait）超时

首轮 prewait 是首个 prompt 派发前对"阻塞集合"MCP 的**有界等待窗口**，超时后放行（未连上的标 `timeout`，后台继续 reconcile）。

| 场景 | 环境变量 | 默认值 |
| --- | --- | --- |
| **stdio / SDK / headless** | `CODEBUDDY_FIRST_RUN_MCP_PREWAIT_TIMEOUT_MS` | **2000** |
| TUI 交互 | `CODEBUDDY_TUI_FIRST_RUN_MCP_PREWAIT_TIMEOUT_MS` | 30000 |

- **调大**（接入方本诉求，给慢 MCP 更多首轮等待时间）：bash
```
CODEBUDDY_FIRST_RUN_MCP_PREWAIT_TIMEOUT_MS=30000 codebuddy --input-format stream-json ...
```
- **完全跳过**首轮等待（首个 prompt 立即派发，MCP 全部后台连）：设为 `0`。
- 取值：非负整数毫秒；空/非法值回退默认。

---

## 4\. stdout 事件 schema（`system/mcp_status`）

三类事件，均为 ndjson（每行一个 JSON 对象）。

### event: "start" —— 首轮开始，带阻塞集合

json
```
{
  "type": "system", "subtype": "mcp_status", "event": "start",
  "servers": ["slow-mcp"],       // ★ 正在阻塞首个 prompt 的 MCP 名单
  "total_count": 1,
  "uuid": "...", "__timestamp": "2026-08-07T09:13:00.000Z"
}
```
### event: "server" —— 单个 MCP 状态过渡

json
```
{
  "type": "system", "subtype": "mcp_status", "event": "server",
  "name": "slow-mcp",
  "state": "connecting",// connecting | ready | failed | timeout
  "error": "...",                // 仅 failed 时可能有
  "completed": 0, "total": 1,
  "uuid": "...", "__timestamp": "..."
}
```
`state` 取值：

- `connecting`：正在连接
- `ready`：连接成功（正常终态）
- `failed`：连接失败（异常终态）
- `timeout`：预热窗口结束仍未连上（异常终态）

### event: "finish" —— 首轮结束，汇总异常

json
```
{
  "type": "system", "subtype": "mcp_status", "event": "finish",
  "failed": [],                  // 连接失败的 MCP
  "timed_out": ["slow-mcp"],     // 超时未连上的 MCP（窗口到期/被打断时未ready 的自动归此）
  "uuid": "...", "__timestamp": "..."
}
```
`finish` 触发时机：预热窗口 deadline 到期、或首轮被打断（如用户新消息）。收到 `finish` 即本 会话首轮状态流结束（后续不再有 first\-run 事件）。

---

## 5\. 接入伪代码

ts
```
const child = spawn('codebuddy', [
  '--input-format', 'stream-json', '--output-format', 'stream-json', '-y',
  '--mcp-config', mcpConfigPath, '--strict-mcp-config',
], { env: { ...process.env, CODEBUDDY_FIRST_RUN_MCP_PREWAIT_TIMEOUT_MS: '30000' } });

let buf = '';
child.stdout.on('data', chunk => {
  buf += chunk;
  let i;
  while ((i = buf.indexOf('\n')) >= 0) {
    const line = buf.slice(0, i).trim(); buf = buf.slice(i + 1);
    if (!line) continue;
    const msg = JSON.parse(line);
    if (msg.type === 'system' && msg.subtype === 'mcp_status') {
      switch (msg.event) {
        case 'start':  showLoading(msg.servers); break;      // 展示"正在加载：slow-mcp"
        case 'server': updateServer(msg.name, msg.state); break;
        case 'finish': hideLoading(msg.failed, msg.timed_out); break;
      }
    }
  }
});

// 新建会话 → 发首个 prompt（无需先发 initialize）
child.stdin.write(JSON.stringify({
  type: 'user',
  message: { role: 'user', content: [{ type: 'text', text: '你的第一个 prompt' }] },
}) + '\n');
```

---

## 6\. 注意事项

- **stdout 是 ndjson**（每行一个对象），不是 SSE 的 `event:/data:` 帧——按行 `JSON.parse`。
- `mcp_status` 事件可被晚订阅者拿到最近一条 `start`（幂等）：即使你在 CLI 启动后稍晚才开始 读stdout，仍能收到本轮的 `start` 事件，不会漏掉首帧。
- `--mcp-config` 文件路径必须落在 CLI 工作目录内，否则会被拒收（报 "MCP config escapes the admitted Workspace"）。
- 首轮之后新连上的 MCP 工具会在后续自动并入，无需接入方额外处理。