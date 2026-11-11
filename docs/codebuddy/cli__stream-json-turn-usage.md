# 流式 JSON 每轮用量事件（usage\_update）

> 适用：以 `--output-format stream-json` 运行 `codebuddy` 的接入方，尤其是通过 `--input-format stream-json` 长连接持续发送多轮 prompt 的 SDK、IDE 后端和平台服务。 目标：**一轮还没结束时就拿到这一轮已经发生的 token 与积分（credits）消耗**，并在 恢复会话时按原轮次还原。

## TL;DR

1. 每次模型调用完成、或受支持的生成类工具完成时，stdout 会多出一条 `{"type":"system","subtype":"usage_update", ...}`，元数据 `kind: "stage"`。
2. 一轮结束前先输出一条 `kind: "snapshot"` 的 `usage_update`，紧接着是本轮 `result`； `result._meta["codebuddy.ai/turnUsage"]` 与这条快照**完全相同**。
3. 按 `(session_id, requestId, stage.id)` 归集并**覆盖**同一阶段；不要把 stage、delta、 total 和 snapshot 叠加求和。
4. `result.usage` 仍是**会话累计** token，`total_cost_usd` 仍是美元字段；积分不会写进这两个字段。
5. 不认识 `usage_update` 的旧消费方可以直接忽略它，其余输出不变。

---

## 1\. 事件时序

一个调用两次模型、中间执行一次工具的用户轮次，与用量有关的顺序如下：

text
```
init -> user -> 模型调用 1 的内容/工具调用 + usage_update(stage, M1)
     -> 工具结果 -> 模型调用 2 的内容 + usage_update(stage, M2)
     -> usage_update(snapshot) -> result（_meta 携带同一份快照）
```
- 阶段事件可能与内容帧、工具帧交错出现，只保证：**本轮所有 usage\_update 都在本轮 `result` 之前**，且快照事件紧挨在 `result` 之前。
- 若 M1、M2 各消耗 2\.5 积分，两条阶段事件的 `delta.credits` 依次为 `2.5`、`2.5`， `total.credits` 依次为 `2.5`、`5`，终态快照为 `5`。
- 下一条用户消息拥有新的 `requestId`，从空的阶段集合重新统计。

## 2\. 阶段事件（kind: stage）

json
```
{
  "type": "system",
  "subtype": "usage_update",
  "uuid": "0198a1b2c3d47e5f8a9b0c1d2e3f4a60",
  "session_id": "session-id",
  "_requestId": "0198a1b2c3d47e5f8a9b0c1d2e3f4a5b",
  "_messageId": "0198a1b2c3d47e5f8a9b0c1d2e3f4a5c",
  "_meta": {
    "codebuddy.ai/requestId": "0198a1b2c3d47e5f8a9b0c1d2e3f4a5b",
    "codebuddy.ai/messageId": "0198a1b2c3d47e5f8a9b0c1d2e3f4a5c",
    "codebuddy.ai/turnUsage": {
      "version": 1,
      "scope": "turn",
      "kind": "stage",
      "requestId": "0198a1b2c3d47e5f8a9b0c1d2e3f4a5b",
      "stage": {
        "id": "model:0198a1b2c3d47e5f8a9b0c1d2e3f4a5c",
        "source": "model",
        "messageId": "0198a1b2c3d47e5f8a9b0c1d2e3f4a5c",
        "model": "reported-model-id",
        "usage": {
          "input_tokens": 100,
          "output_tokens": 10,
          "cache_read_input_tokens": 20,
          "cache_creation_input_tokens": 5
        },
        "credits": 2.5
      },
      "delta": {
        "usage": {
          "input_tokens": 100,
          "output_tokens": 10,
          "cache_read_input_tokens": 20,
          "cache_creation_input_tokens": 5
        },
        "credits": 2.5
      },
      "total": {
        "usage": {
          "input_tokens": 100,
          "output_tokens": 10,
          "cache_read_input_tokens": 20,
          "cache_creation_input_tokens": 5
        },
        "credits": 2.5,
        "creditStatus": "known"
      }
    }
  }
}
```
### 字段说明

| 字段 | 含义 |
| --- | --- |
| `_requestId`、`_meta["codebuddy.ai/requestId"]`、`requestId` | 本次用户轮次。客户端可在输入消息的 `_meta["codebuddy.ai/conversationRequestId"]` 中指定，见[无头模式](./headless)。 |
| `_messageId`、`_meta["codebuddy.ai/messageId"]` | 仅阶段事件携带，等于 `stage.messageId`。 |
| `stage.id` | 阶段的稳定身份，用于去重和覆盖。模型调用为 `model:<messageId>`；工具为 `generation-tool:<工具名>:<调用 ID>`。 |
| `stage.source` | `model` 或 `tool`。 |
| `stage.messageId` | 模型阶段：该次模型调用的生成 ID（不是帧 `uuid`，也不是历史条目 ID）。工具阶段：发起该工具调用的模型调用 ID，可能缺省。 |
| `stage.model` / `stage.tool` | 可选的模型名 / 工具名，终态时可能被补全；补全不改变阶段身份与数值。 |
| `stage.usage` | 该阶段上报的计费 token。工具阶段恒为 0。 |
| `stage.credits` | 该阶段上报的积分；未上报时**省略**，不会补 0。 |
| `delta` | 本条事件相对**同一阶段上一次上报值**的变化，首次上报等于 `stage` 本身；同一阶段被修正时可能为 0 或负数。 |
| `total` | 到目前为止本轮所有阶段之和，是快照而不是增量。 |

同一阶段可能被上报不止一次，例如工具先完成但积分稍后才确定。数值未变化时不会重复发送。

## 3\. 终态快照与 result

一轮结束时（成功、取消或出错），先输出一条快照事件：

- `kind: "snapshot"`，包含 `total` 与完整的 `stages` 数组；
- 不含 `stage`、`delta`，外层也没有 `_messageId`；
- 若本轮 `result` 带有上下文元数据（如 `codebuddy.ai/contextUsed`、 `codebuddy.ai/contextWindow`、`codebuddy.ai/usageByCategory`），快照事件的 `_meta` 也会同样携带。

随后输出本轮唯一的 `result`，其 `_meta["codebuddy.ai/turnUsage"]` 与上面的快照完全相同：

json
```
{
  "type": "result",
  "subtype": "success",
  "is_error": false,
  "result": "最终回答",
  "session_id": "session-id",
  "_requestId": "0198a1b2c3d47e5f8a9b0c1d2e3f4a5b",
  "usage": {
    "input_tokens": 100,
    "output_tokens": 10,
    "cache_read_input_tokens": 20,
    "cache_creation_input_tokens": 5
  },
  "total_cost_usd": 0,
  "_meta": {
    "codebuddy.ai/requestId": "0198a1b2c3d47e5f8a9b0c1d2e3f4a5b",
    "codebuddy.ai/turnUsage": {
      "version": 1,
      "scope": "turn",
      "kind": "snapshot",
      "requestId": "0198a1b2c3d47e5f8a9b0c1d2e3f4a5b",
      "total": {
        "usage": {
          "input_tokens": 100,
          "output_tokens": 10,
          "cache_read_input_tokens": 20,
          "cache_creation_input_tokens": 5
        },
        "credits": 2.5,
        "creditStatus": "known"
      },
      "stages": [
        {
          "id": "model:0198a1b2c3d47e5f8a9b0c1d2e3f4a5c",
          "source": "model",
          "messageId": "0198a1b2c3d47e5f8a9b0c1d2e3f4a5c",
          "model": "reported-model-id",
          "usage": {
            "input_tokens": 100,
            "output_tokens": 10,
            "cache_read_input_tokens": 20,
            "cache_creation_input_tokens": 5
          },
          "credits": 2.5
        }
      ]
    }
  }
}
```
以上为字段节选，省略了耗时、权限、`modelUsage` 等既有字段。示例是会话第一轮，所以 `result.usage` 恰好等于本轮合计；从第二轮起，`result.usage` 是整个会话的累计值，而 `turnUsage.total.usage` 只覆盖本轮。

## 4\. 归集规则

- 以 `(session_id, requestId, stage.id)` 为键保存阶段，收到同键的新事件时**覆盖**旧值。 不同 `stage.id` 即使金额相同也是两次独立消耗。
- 已经按阶段归集时，不要再额外累加 `delta`；`delta` 只是方便只做增量展示的消费方。
- `total` 和 `snapshot` 都是快照，可直接替换展示值，不能与阶段值相加。
- 终态快照和 `result` 中的快照是同一份事实，不要重复计入。
- 迟到的事件始终带着它原本的 `requestId`，应计入对应轮次，而不是消费方当前正在展示的轮次。
- 帧 `uuid` 只是投递身份，不能用来做计费去重。

## 5\. 统计范围

计入本轮的消耗包括：

- 本轮所有已完成的模型调用，包括工具循环中的多次调用；
- 前台子代理（`Agent` 工具）内部的模型调用，计入发起它的根请求；
- 返回了完成结果的生成类工具：`ImageGen`、`ImageEdit`、`VideoGen`、`AudioTranscribe`；
- 上游已计费但没有产生任何输出的模型调用（例如只有推理内容的空响应），同样作为该调用 的阶段上报，并保存在会话历史中，恢复会话后仍可回放。

其他工具不会根据名称、token 数或输出中的数字推算价格。

## 6\. 积分完整度（creditStatus）

`credits` 只来自模型或工具上报的积分事实，不做 token 到价格的换算，也不代表货币或 上下文占用。

| 值 | 含义 |
| --- | --- |
| `known` | 所有已记录阶段都上报了积分（合法的 0 也算）。 |
| `partial` | 部分阶段上报了积分，其余未上报。 |
| `unknown` | 没有任何阶段上报积分，或本轮还没有阶段。此时 `total` 不含 `credits`。 |

非法或缺失的积分一律省略，不会被当成 0。执行过程中即使是 `known`，也只代表**已经发生** 的消耗，不预测后续调用。

## 7\. 取消与出错

- 取消或出错时，已上报的消耗仍保留在终态快照中。
- 如果在任何模型调用完成之前就取消，快照为 `stages: []`、token 全为 0、 `creditStatus: "unknown"` 且没有 `credits`，不会带上上一轮的消耗。
- 取消后的 `result` 仍沿用既有终态语义（`subtype: "success"`、`is_error: false`、 `terminal_reason`）。若本轮在中断前没有完成的回答，`result.result` 为空字符串， 不会返回上一轮的回答。

## 8\. 恢复会话（\-\-resume）

恢复会话回放历史时，CLI 会在回放结束的 `result` 之前，为历史中每个记录过阶段的轮次 （包括积分为 `unknown` 的轮次）各输出一条 `kind: "snapshot"` 的 `usage_update`：

- 使用原来的 `requestId` 和 `stage.id`，不含 `delta`，表示已有事实而不是新的消耗；
- 阶段在 `stages` 中的顺序不保证与当初一致，请按 `stage.id` 匹配；
- 回放的 `result` 不附带 `turnUsage`；恢复后发起的新一轮按第 1～3 节独立统计。

## 9\. 兼容性

| 既有字段 | 行为 |
| --- | --- |
| `assistant.message.usage` | 不变：单次调用的 token，不含积分。 |
| `result.usage` | 不变：会话累计 token。 |
| `result.total_cost_usd` | 不变：美元字段，积分不会写入。 |
| 上下文元数据（`contextUsed` / `contextWindow` / `usageByCategory`） | 不变：当前上下文占用快照，不要与计费 token 相加。 |
| 终态类型与 `terminal_reason` | 不变。 |

## 10\. 与 ACP usage\_update 的关系

ACP 模式（`--acp`）同样使用 `usage_update` 事件族，两者共享请求与生成归属的元数据键， 但载荷不同：

|  | ACP | 流式 JSON |
| --- | --- | --- |
| 外层 | JSON\-RPC 通知 `session/update` | stdout 消息 `type: "system"` |
| 判别字段 | `update.sessionUpdate: "usage_update"` | `subtype: "usage_update"` |
| 请求归属 | `update._meta["codebuddy.ai/requestId"]` | 同名键，另有 `_requestId` |
| 生成归属 | `update._meta["codebuddy.ai/messageId"]` | 同名键，另有 `_messageId` |
| 消耗载荷 | `cost.amount`（积分，`currency` 为空）与 `_meta["codebuddy.ai/requestCredits"]` | `_meta["codebuddy.ai/turnUsage"]` |
| 上下文占用 | `used` / `size` | 上下文元数据，见第 9 节 |

ACP 的载荷格式保持原样；流式 JSON 额外提供稳定的阶段身份和积分完整度。