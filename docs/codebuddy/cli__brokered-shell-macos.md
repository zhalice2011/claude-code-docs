# macOS Brokered Shell 方案设计

## 背景与目标

macOS 的 Bash 沙箱需要同时解决两个问题：

1. 沙箱内命令必须被文件系统策略约束，越权读写要经过 CodeBuddy 的权限判断。
2. 当命令会修改已有文件时，必须在真实修改发生前接入 `ModifyBackup`，让 `sandbox-cli` 能保存修改前版本，并在本轮结束时通过 `CommitModifyBackup` 固化备份周期。

仅依赖普通 shell 或系统命令做不到这一点。原因是：

- `>` / `>>` 等重定向由 shell 自己执行，外层只能看到整条命令，看不到打开目标文件的准确时机。
- `sed -i`、`mv` 这类命令可能通过临时文件加 `rename` 覆盖目标文件，不一定表现为对目标文件的直接写入。
- `truncate` 会通过 `open(O_WRONLY)` 加 `ftruncate` 改变文件内容，如果命令没有进入 brokered runtime，就没有修改前备份时机。
- macOS Seatbelt 的 `sandbox_extension` token 只能由沙箱外进程签发，沙箱内进程不能自行扩大权限。

因此当前方案采用自编 `zsh` \+ 自编 `toybox` \+ agent\-cli broker 的组合：

- 自编 `zsh` 负责 shell 语义层，覆盖重定向、glob、条件判断、目录访问等 shell 内部文件访问。
- 自编 `toybox` 负责常见命令层，覆盖由 `PATH` 命中的基础命令及其 `open` / `rename` / `delete` 等文件操作。
- `agent-cli` 作为 broker 层，负责权限策略、用户审批、macOS sandbox extension token 签发、host operation 执行，以及 `ModifyBackup` 触发。
- `sandbox-cli` 作为沙箱执行与备份存储层，负责运行沙箱内进程，并持久化 `ModifyBackup` / `CommitModifyBackup` 数据。

目标不是给每个命令写一套备份逻辑，而是在关键语义层拿到“真实修改前”的统一时机。

## 总体架构

mermaid
```
flowchart LR
  UserTurn["用户 turn"] --> Interceptor["SandboxAgentRunInterceptor"]
  Interceptor --> SandboxCLI["sandbox-cli session"]
  Interceptor --> BackupConfig["EnableModifyBackup"]

  BashTool["Bash 工具"] --> SandboxShell["SandboxShellService"]
  SandboxShell --> BrokerIPC["BrokeredSandboxIpcServer<br/>Unix socket"]
  SandboxShell --> Zsh["自编 zsh"]
  Zsh --> BrokerEnv["brokered-sandbox-bash-env.sh"]
  BrokerEnv --> BrokeredBin["brokered-bin PATH"]
  BrokeredBin --> Toybox["自编 toybox"]

  Zsh -->|"text token request<br/>read/write path"| BrokerIPC
  Toybox -->|"text token request<br/>open/fopen"| BrokerIPC
  Toybox -->|"JSON HostFileOperation<br/>delete/rename"| BrokerIPC

  BrokerIPC --> HostService["BrokeredSandboxHostService"]
  HostService --> Policy["sandbox fileSafety / approval"]
  HostService --> ModifyBackup["ModifyBackup"]
  HostService --> Token["sandbox_extension_issue_file"]
  HostService --> HostOp["host delete/rename/copy/..."]

  ModifyBackup --> SandboxCLI
  FinalStop["FINAL_STOP hook"] --> CommitBackup["CommitModifyBackup"]
  CommitBackup --> SandboxCLI
```
核心代码与产物位置：

| 模块 | 位置 | 职责 |
| --- | --- | --- |
| 沙箱 turn 配置 | `src/node/agent/interceptors/sandbox-interceptor.ts` | 读取 `sandbox.fileBackup`，启动并同步 `sandbox-cli`，发送 `EnableModifyBackup` |
| 沙箱 shell 执行 | `src/node/sandbox-cli/sandbox-shell-service.ts` | 启动 broker IPC，注入 broker env，macOS 下切到自编 `zsh` |
| runtime env | `src/node/shell/shell-runtime-env.ts` / `src/node/shell/brokered-shell-env.ts` | 注入 `CODEBUDDY_SANDBOX_BROKER_*`、toybox、zsh、brokered bin 路径 |
| broker IPC | `src/node/permission/brokered-sandbox/ipc-server.ts` | 接收 zsh/toybox 请求，分发 token request 和 host operation |
| host service | `src/node/permission/brokered-sandbox/host-service.ts` | 权限判断、token 签发、host 操作执行、`ModifyBackup` |
| host dispatcher | `src/node/permission/brokered-sandbox/host-dispatcher.ts` | JSON `HostFileOperation` 路由 |
| 收尾提交 | `src/node/hooks/finalization-modify-backup-hook.ts` | `FINAL_STOP` 时发送 `CommitModifyBackup` |
| brokered shim | `vendor/shim/brokered-sandbox-bash-env.sh` / `vendor/shim/brokered-bin/*` | 将常见命令路由到自编 toybox |
| 自编 zsh 产物 | `vendor/zsh-macos/bin/zsh` | macOS brokered shell |
| 自编 toybox 产物 | `vendor/toybox-macos/toybox` | macOS brokered command runtime |
| toybox sandbox profile | `vendor/toybox-macos/toybox.sb` | toybox 的 Seatbelt 沙箱规则（见下文） |
| zsh/toybox 源码 | `tsbx-macos` 仓库 | 可复现构建和底层 hook 源码 |

## 启用条件与运行时注入

### 开关生效矩阵

Bash 命令是否进入 brokered shell 以及是否启用修改前备份，取决于多个条件的组合：

| 条件 | 不满足时的行为 |
| --- | --- |
| `sandbox.enabled = true` | `SandboxOrchestrator` 直接走 local 执行，不进入沙箱，brokered shell 和备份均不生效 |
| `darwin` 平台 | brokered shell runtime 不注入（brokered shell 是 macOS 专有方案） |
| WorkBuddy Desktop 环境 | `injectBrokeredShellEnv()` 不注入托管 runtime 产物 |
| brokered shell shim 完整（`shell-runtime-bash-env.sh`、`brokered-sandbox-bash-env.sh`、`brokered-bin/codebuddy-toybox-dispatch`、`brokered-bin/ls` 存在） | 基础 brokered shell runtime 不注入；zsh、toybox、toybox.sb 是可选产物，缺 zsh 则不切自编 shell，缺 toybox/toybox.sb 则不注入 toybox runtime |
| `WORKBUDDY_MANAGED_RUNTIME_DISABLED` 不含 `brokeredShell` | 含 `brokeredShell` 时跳过 brokered shell runtime 注入 |
| 命令不在 `sandbox.excludedCommands` 中 | 命中 excludedCommands 的命令直接 fallback local 执行 |
| 非 `dangerouslyDisableSandbox` | 模型请求 bypass 时走用户审批 → 通过则 local 执行，不进沙箱 |
| 非 `rawCommand` 模式 | rawCommand 直接 spawn 可执行文件，不经 shell wrapping，不前置 `brokered-bin`，不切自编 zsh；WorkBuddy Desktop 的默认 sandbox env 仍会注入基础 broker 变量 |
| `sandbox.fileBackup.enabled !== false` | 备份不启用，brokered shell 仍然生效（权限控制和 token 签发正常），但不触发 `ModifyBackup` |

典型正常链路：以上条件全部满足 → 命令进入自编 zsh \+ toybox brokered shell → 写操作经 broker 权限判断 → 已有普通文件触发 `ModifyBackup` → `FINAL_STOP` 时 `CommitModifyBackup`。

### 文件备份开关

文件备份开关由 `SandboxAgentRunInterceptor` 在每个真实用户 turn 开始时解析：

- 支持平台：`win32` 和 `darwin`。Windows 侧的文件备份通过独立机制实现，不涉及 brokered shell runtime，不在本文档范围内。
- macOS 上 `sandbox.fileBackup.enabled !== false` 时开启，未显式关闭时默认开启。
- 开启后会确保 `sandbox-cli` session ready，并向 `sandbox-cli` 发送 `EnableModifyBackup`。
- 如果 `sandbox-cli` 不可用或 `EnableModifyBackup` 同步失败，本轮会关闭 `enableFileBackup`，避免进入半开状态。

brokered shell runtime 只在 macOS 的沙箱 Bash 执行链路中注入。`SandboxShellService.execute()` 的关键步骤是：

1. `waitReady()` / `ensureAlive()` / `switchToSession()` 准备 `sandbox-cli` session。
2. `BrokeredSandboxIpcServer.ensureStarted()` 创建沙箱外 Unix socket。
3. `buildShellRuntimeEnv()` 注入 broker env。
4. `_resolveSandboxShellConfiguration()` 在 `darwin` 且存在自编 zsh 和 broker IPC 时使用 `vendor/zsh-macos/bin/zsh -f -c`。
5. `buildShellRuntimePosixCommand()` source `brokered-sandbox-bash-env.sh`，把 `brokered-bin` 前置到 `PATH`。

关键环境变量：

| 变量 | 用途 |
| --- | --- |
| `CODEBUDDY_SANDBOX_BROKER_IPC_ADDRESS` | agent\-cli broker Unix socket 路径 |
| `CODEBUDDY_SANDBOX_BROKER_SESSION_ID` | 当前 CodeBuddy session，用于防串 session |
| `CODEBUDDY_SANDBOX_BROKER_TOOL_CALL_ID` | 当前 Bash tool call，用于审计与备份归属 |
| `CODEBUDDY_SANDBOX_BROKER_TRACE_ID` | 单次执行 trace id，便于日志关联 |
| `CODEBUDDY_SANDBOX_HOST_FILE_OPERATION_COMMAND` | JSON host\-op command 名，当前为 `HostFileOperation` |
| `CODEBUDDY_TOYBOX_BIN` | 自编 toybox 二进制路径 |
| `CODEBUDDY_TOYBOX_SANDBOX_PROFILE` | toybox sandbox profile 路径 |
| `CODEBUDDY_BROKERED_SHELL_ENV` | brokered shell bootstrap 脚本 |
| `CODEBUDDY_BROKERED_BIN_DIR` | brokered command shim 目录 |
| `CODEBUDDY_SANDBOX_ZSH_BIN` | 自编 zsh 二进制路径 |
| `TOYBOX_SANDBOX_SOCK` | toybox 连接 broker 的 socket，通常由 bootstrap 从 broker IPC 地址派生 |

`injectBrokeredShellEnv()` 还会检查运行环境：

- 非 `darwin` 不注入任何 brokered 环境变量。
- **Broker IPC 环境变量**（`CODEBUDDY_BROKERED_FS_HOOK_ENABLED`、`CODEBUDDY_SANDBOX_BROKER_IPC_ADDRESS` 等）仅在 WorkBuddy Desktop 环境下注入，非 WorkBuddy Desktop 环境会清理调用方遗留的 broker IPC 和 toybox socket 地址；在 WorkBuddy Desktop 内不受 `brokeredShell` 开关影响。这使得 safe\-delete shim（bash/Node.js/Python）即使在 brokeredShell 关闭时也能通过 broker IPC 发送 `HostFileOperation delete`，统一走 host service 的权限检查和 `ModifyBackup`。
- **托管 runtime 产物**（toybox、zsh、brokered\-bin）仅在以下条件全部满足时注入：非 `WORKBUDDY_MANAGED_RUNTIME_DISABLED=brokeredShell`、是 WorkBuddy Desktop 环境。

## macOS 文件修改识别链路

当前有两类 IPC 协议。

### text token request

用于 zsh 和 toybox 的 `open` 类文件访问：

text
```
<extension-class>\t<absolute-path>\t<session-id>\t<tool-call-id>\n
```
`extension-class` 当前有两种：

- `com.workbuddy.sandbox.read`
- `com.workbuddy.sandbox.read-write`

agent\-cli 收到后：

1. 校验 session id 必须等于当前 session。
2. 根据 `fileSafety` 判断路径是 `grant-token`、`sandbox`、`deny` 还是需要审批。
3. 如果命中需要审批的规则，broker 记录 prompt block，当前 IPC 请求返回 `DENY`，外层 `SandboxOrchestrator` 负责统一审批和 native rerun。
4. 如果是写操作且最终不是 deny，先执行 `ModifyBackup`。
5. 返回 sandbox extension token、`SANDBOX` 或 `DENY`。
6. zsh/toybox 收到 token 后 `sandbox_extension_consume()`，再执行真实 `open`。

agent\-cli 的响应是单行文本，有三种形式：

- sandbox extension token 字符串：zsh/toybox 调用 `sandbox_extension_consume()` 后再执行真实 `open`。
- `SANDBOX`：现有沙箱规则已经允许访问，不需要 consume token；但写操作仍然会先走 `ModifyBackup`。
- `DENY`：拒绝访问，zsh/toybox 不执行真实 `open`。

### JSON HostFileOperation

用于沙箱内不应该自己完成、或需要 host 语义的文件操作：

json
```
{
  "id": "req-1",
  "command": "HostFileOperation",
  "operation": "rename",
  "from": "/absolute/source",
  "to": "/absolute/target",
  "sessionId": "...",
  "toolCallId": "...",
  "brokerTraceId": "..."
}
```
`id` 用于 request\-response 匹配；`brokerTraceId` 用于日志关联。两者均可选，但推荐携带以方便审计。

agent\-cli 的 JSON 响应结构：

json
```
{
  "id": "req-1",
  "ok": true,
  "operation": "rename",
  "path": "/absolute/source",
  "normalisedPath": "/resolved/source",
  "decision": "host-op",
  "to": "/absolute/target",
  "normalisedTo": "/resolved/target"
}
```
失败时 `ok` 为 `false`，并附带 `error` 字段。`decision` 可能为 `grant-token`、`host-op`、`sandbox` 或 `deny`。（`prompt` 是审批过程中间状态，不会作为最终 IPC 响应返回给 toybox。）

当前 agent\-cli TS 侧支持的 host operation 包括：

| operation | 额外参数 | 说明 |
| --- | --- | --- |
| `delete` | `deleteMode?: 'trash' | 'unlink'`、`recursive?`、`force?`、`safeDeleteReportPath?` | macOS 默认 `deleteMode='trash'`（移入回收站），非 macOS 默认 `unlink` |
| `mkdir` | `recursive?`、`mode?` | 创建目录 |
| `rename` | `from`、`to` | 重命名/移动 |
| `copy` | `from`、`to`、`recursive?` | 复制文件或目录 |
| `chmod` | `path`、`mode` | 修改权限 |
| `link` | `from`、`to`、`symbolic?` | 硬链接（默认）或符号链接。硬链接校验 source 的 read 权限 \+ target 的 write 权限；符号链接只校验 target 的 write 权限 |
| `touch` | `path` | 创建或更新文件时间戳 |

当前 macOS toybox runtime 明确上报的关键 host operation 是：

- `delete`：`rm` / `rmdir` / `unlink` 通过 `toybox_host_delete()` 上报，host 侧接入回收站（`deleteMode='trash'`）。
- `rename`：`rename()` 宏替换为 `toybox_rename()`，覆盖 `mv`、`sed -i` 等临时文件覆盖场景。

`copy`、`touch` 等 TS 分支用于 broker 能力完整性和未来扩展；当前 `cp` 覆盖主要来自 open 写目标文件的 text token request，而不是 toybox 主动发送 JSON `copy`。

## 自编 zsh 的职责

自编 zsh 的核心价值是拿到 shell 自身的文件访问时机，尤其是重定向。

源码在 `tsbx-macos/zsh-macos`，当前 patch 基于 zsh 5\.9\.1，主要修改：

- `Src/exec.c`：把重定向相关 `open()` 改成 `codebuddy_brokered_open()`。
- `Src/zsh_system.h`：新增 broker 连接、路径规范化、token request、`sandbox_extension_consume()`、brokered `open/stat/access/opendir/chdir` 等 helper。
- `Src/init.c` / `Src/glob.c` / `Src/cond.c` / `Src/compat.c`：把 shell 初始化、glob、条件判断、目录切换等文件访问改成 brokered 版本。

zsh 负责的典型场景：

- `echo hi > a.txt`
- `cat < input.txt`
- `[[ -f a.txt ]]`
- `cd some-dir`
- glob 展开过程中需要 `stat` / `lstat` 的路径

其中 `>` / `>>` 是备份链路最关键的场景。真实流程是：

1. zsh 解析重定向。
2. 执行 `codebuddy_brokered_open(path, O_WRONLY | O_CREAT | O_TRUNC, ...)`。
3. `codebuddy_brokered_authorize_path(path, "write")` 向 agent\-cli broker 发 text token request。
4. agent\-cli 放行前对已有普通文件发 `ModifyBackup`。
5. zsh 拿到 token 或 `SANDBOX` 后再执行真实 `open()`。

这就是为什么 `>` 的时机必须在自编 zsh 内暴露，而不是只靠 agent\-cli 解析命令字符串。

## 自编 toybox 的职责

自编 toybox 的核心价值是把常见基础命令统一收口到一个可控 runtime。

agent\-cli vendor 中的 `brokered-bin` 目录包含 dispatcher 入口 `codebuddy-toybox-dispatch` 和一组命令名 shim：

text
```
codebuddy-toybox-dispatch   # dispatcher 入口
cat chmod cp dd find grep head ln ls mkdir mv readlink realpath rm rmdir sed tail tee touch truncate unlink wc
```
每个命令名 shim 都是指向 `codebuddy-toybox-dispatch` 的链接。执行流程：

1. `brokered-sandbox-bash-env.sh` 把 `CODEBUDDY_BROKERED_BIN_DIR` 前置到 `PATH`。
2. 用户命令里的 `sed` / `mv` / `truncate` 优先命中 brokered shim。
3. `codebuddy-toybox-dispatch` 根据自身文件名得到 toybox applet 名。
4. dispatcher 执行 `CODEBUDDY_TOYBOX_BIN <applet> ...`。
5. 如果 toybox 不支持该 applet 或选项，dispatcher 会从 `PATH` 移除 brokered bin 后 fallback 到系统同名命令。

toybox 源码层的关键 hook 在 `tsbx-macos/toybox-0.8.13`：

- `toys.h` 宏替换 `open/openat/creat/fopen/freopen/rename`。
- `lib/iolog.c` 实现 `toybox_open()`、`toybox_openat()`、`toybox_creat()`、`toybox_fopen()`、`toybox_freopen()`。
- open 类 wrapper 在真实 open 前发送 text token request。
- `toybox_rename()` 发送 JSON `HostFileOperation rename`，由 host 执行真实 rename。
- `toybox_host_delete()` 发送 JSON `HostFileOperation delete`，由 host 执行安全删除。

toybox 的 open hook 是 eager 模式：不是等 macOS sandbox 拒绝后再申请 token，而是在每次 open 前主动请求 broker。这样 agent\-cli 能在真实写入前完成备份。

### toybox sandbox profile (`toybox.sb`)

`vendor/toybox-macos/toybox.sb` 是 toybox 运行时的 Seatbelt 沙箱规则，由 `sandbox-cli` 在启动 toybox 进程时通过 `sandbox-exec` 加载。核心策略：

- `(deny default)`：默认拒绝所有文件系统访问。
- `(allow file-read* (subpath "/"))`：允许全局读取（read token request 仍然会走 broker，但 Seatbelt 层不阻拦）。
- `(allow file-write* (subpath "/dev") (subpath "/private/var/folders"))`：允许写 `/dev`（stdout/stderr）和临时目录（sed \-i 等中间文件）。
- `(allow file-read* (extension "com.workbuddy.sandbox.read"))`：持有 read token 后允许读取对应路径。
- `(allow file-read* file-write* (extension "com.workbuddy.sandbox.read-write"))`：持有 read\-write token 后允许读写对应路径。

这是 brokered shell 安全模型的底层执行机制：toybox 必须先从 broker 获得 sandbox extension token，Seatbelt 才会允许写操作。eager token 请求确保 broker 能在 Seatbelt 放行前完成权限判断和修改前备份。

## 关键命令覆盖方式

### `>`

`>` 是 zsh 重定向，不是外部命令。

bash
```
echo hi > a.txt
```
链路：

1. 自编 zsh 在重定向阶段调用 `codebuddy_brokered_open()`。
2. zsh 发送 `com.workbuddy.sandbox.read-write` text token request。
3. agent\-cli 判断权限。
4. 如果 `a.txt` 已存在且是普通文件，agent\-cli 在返回 token 或 `SANDBOX` 前发送 `ModifyBackup`。
5. zsh 执行真实 `open(O_TRUNC)`，文件才被截断。

### `cp`

bash
```
cp source.txt target.txt
```
链路：

1. `cp` 命中 `brokered-bin/cp`。
2. dispatcher 执行 toybox `cp`。
3. toybox `cp` 打开源文件时发 read token request。
4. toybox `cp` 打开目标文件时发 write token request，覆盖已有目标通常会走 `openat(..., O_TRUNC, ...)`。
5. agent\-cli 在目标写 token 放行前对已有目标文件执行 `ModifyBackup`。

当前不依赖 JSON `copy` host\-op 覆盖 `cp`。TS 侧有 `copyPath()` 能力，但 macOS toybox 的 `cp` 覆盖主要来自 open 写目标。

### `mv`

bash
```
mv source.txt target.txt
```
链路：

1. `mv` 命中 `brokered-bin/mv`。
2. toybox `mv` 调用 `rename()`。
3. `rename()` 被宏替换为 `toybox_rename()`。
4. `toybox_rename()` 发送 JSON `HostFileOperation rename`，包含 `from` 和 `to`。
5. agent\-cli host service 分别校验 source 的 delete 权限和 target 的 write 权限。
6. 执行 host rename 前，对已存在的 source 和 target 普通文件执行 `ModifyBackup`。
7. host 侧执行真实 `rename(from, to)`，toybox 收到 ok 后认为命令成功。

如果 host rename 返回跨设备错误，toybox 会把错误映射为 `EXDEV`，保留 `mv` 自身的 copy \+ delete fallback 语义。fallback 中的 copy 写目标和 delete 源文件仍会分别经过 brokered open 或 host delete。

### `sed -i`

bash
```
sed -i '' 's/a/b/g' file.txt
```
macOS / toybox 的 `sed -i` 常见实现是：

1. 读取原文件。
2. 写临时文件。
3. 用 `rename(temp, file.txt)` 覆盖原文件。

如果只监听写目标文件，会漏掉真正覆盖原文件的时机，因为写入发生在临时文件上。当前方案通过 toybox `rename` hook 解决：

1. `sed` 命中 `brokered-bin/sed`。
2. toybox `sed` 写临时文件，临时文件的 open 会走 write token；因为临时文件通常不存在，不产生备份。
3. toybox `sed` 调用 `rename(temp, file.txt)`。
4. `toybox_rename()` 发送 JSON `HostFileOperation rename`。
5. agent\-cli 在 host rename 前对已存在的 `file.txt` 执行 `ModifyBackup`。
6. host 侧执行 rename 覆盖。

这就是 `mv` 和 `sed -i` 被归为同一类问题的原因：本质都是“rename 覆盖目标文件前”的备份时机。

### `truncate`

bash
```
truncate -s 0 file.txt
```
toybox `truncate` 的实现不是直接 `open(O_TRUNC)`，而是：

1. `loopfiles_rw(..., O_WRONLY | O_CLOEXEC | ...)` 打开目标文件。
2. 对 fd 调用 `ftruncate(fd, size)`。

当前覆盖依赖第一步：

1. `truncate` 命中 `brokered-bin/truncate`。
2. toybox `truncate` 打开目标文件时触发 `toybox_open()`。
3. 因为 flags 包含 `O_WRONLY`，toybox 发送 write token request。
4. agent\-cli 在返回 token 或 `SANDBOX` 前对已有普通文件执行 `ModifyBackup`。
5. toybox 随后调用 `ftruncate()` 修改文件长度。

当前没有单独 hook `ftruncate()`。因此 brokered toybox 的 `truncate` 可以覆盖；外部二进制如果绕开 brokered toybox 并直接 `ftruncate()`，不属于本方案覆盖范围。

### `dd`

bash
```
dd if=source.bin of=file.bin bs=1M
```
toybox `dd` 对输出目标的写入方式和 `truncate`/`cp` 类似（`open` 目标路径），但 `of=` 是 `key=value` 形式的操作数，不是位置参数，`codebuddy-toybox-dispatch` 在调用 toybox 之前额外做了一次 shell 层预备份：

1. `dd` 命中 `brokered-bin/dd`。
2. dispatcher 解析全部操作数，找到 `of=<path>` 并对已存在的普通文件执行一次 write token 预检 \+ `ModifyBackup`（复用 `truncate`/`tee` 的 `__cb_prebackup_path`）。
3. dispatcher 执行 toybox `dd`，toybox 打开 `of=` 目标时会再触发一次 `toybox_open()` write token request。
4. 两次备份写入前内容相同（预备份和 toybox 自身 open hook 之间没有发生真实写入），不影响正确性，只是多一次 IPC 往返。

`dd` 不指定 `of=` 时输出到 stdout，不落盘，不触发预备份。

## ModifyBackup / CommitModifyBackup 调用链路

### 启用备份

每个真实用户 turn 开始时：

1. `SandboxAgentRunInterceptor` 读取 `sandbox.fileBackup`。
2. 写入 `SandboxTurnConfig.enableFileBackup` 和 `fileBackupMaxSizeMB`。
3. 确保 `sandbox-cli` session ready。
4. 发送 `EnableModifyBackup`：

json
```
{
  "enabled": true,
  "fileBackupMaxSizeMB": 10
}
```
`fileBackupMaxSizeMB` 会经过最小值、最大值和默认值归一化，实际存储限制由 `sandbox-cli` 执行。

### 修改前备份

有两条入口会发送 `ModifyBackup`。

text token request 写路径：

- 入口：`BrokeredSandboxIpcServer.handleToyboxTextLine()`。
- 条件：operation 是 `write`，权限结果不是 deny，`enableFileBackup=true`。
- 行为：如果目标已存在且是普通文件，发送 `ModifyBackup { targetPath }`。
- 失败策略：备份失败则返回 `DENY`，真实写入不继续。

JSON host operation：

- 入口：`BrokeredSandboxHostService`。
- 条件：host operation 会修改已有内容，`enableFileBackup=true`。
- `delete` / `touch`：备份 `path` 中已存在的普通文件。
- `rename`：备份 `from` 和 `to` 中已存在的普通文件。
- `copy`：备份 `to` 中已存在的普通文件。
- `chmod` / `mkdir`：不触发备份（`chmod` 只改元数据，`mkdir` 创建新目录）。
- `link`：不触发备份。
- 失败策略：备份失败则 host action 不执行，operation 返回失败。

这两个入口都只备份“已存在的普通文件”。新建文件、目录、特殊文件、纯元数据恢复不在当前内容备份语义内。

### 收尾提交

本轮结束进入 `FINAL_STOP` 时，`FinalizationModifyBackupHook` 执行：

1. 检查 `enableFileBackup`。
2. 检查是否存在已打开的 sandbox session。
3. 从最近真实用户消息生成短 commit message。
4. 发送 `CommitModifyBackup { commitMsg }` 到 `sandbox-cli`。

该 hook 不按 `final_stop_reason` 过滤。只要本轮启用了文件备份且 sandbox session 存在，就尝试提交备份周期。提交失败只记录日志，不阻断 agent 收尾。

## 权限审批与备份的先后顺序

顺序是安全语义的核心。

text token request 写路径：

text
```
zsh/toybox 请求 write token
  -> agent-cli 校验 session
  -> fileSafety 策略判断
  -> 若需要审批，记录 brokered prompt block 并向 zsh/toybox 返回 DENY
  -> SandboxOrchestrator 合并 prompt block，统一请求用户审批
  -> 用户允许后 native rerun 整条命令；用户拒绝则保留沙箱失败结果
```
无需审批或已经被规则直接放行的写路径：

text
```
zsh/toybox 请求 write token
  -> agent-cli 校验 session
  -> fileSafety 策略判断通过
  -> ModifyBackup 已有普通文件
  -> 返回 token 或 SANDBOX
  -> zsh/toybox 执行真实 open/write/truncate
```
JSON host operation：

text
```
toybox 请求 HostFileOperation
  -> agent-cli 校验 session
  -> source/target 权限判断
  -> resolved path 安全校验
  -> 若需要审批，记录 brokered prompt block 并向 toybox 返回失败
  -> SandboxOrchestrator 合并 prompt block，统一请求用户审批
  -> 用户允许后 native rerun 整条命令；用户拒绝则保留沙箱失败结果
```
无需审批或已经被规则直接放行的 host operation：

text
```
toybox 请求 HostFileOperation
  -> agent-cli 校验 session
  -> source/target 权限判断
  -> resolved path 安全校验通过
  -> ModifyBackup 受影响的已有普通文件
  -> host 侧执行 delete/rename/copy/...
  -> 返回结果给 toybox
```
关键原则：

- 当前主链路不在 IPC 内等待用户审批；brokered shell 只记录 prompt block，外层审批通过后走 native rerun。
- 权限未通过或需要审批但尚未获得外层批准时，不备份、不执行真实修改。
- 权限通过但备份失败时不执行真实修改。
- 备份必须早于 token 返回或 host action 执行。
- `SANDBOX` 代表沙箱规则已允许访问，但不会跳过写前备份。

## 运行时行为约束

### 并发模型

当前 agent\-cli 侧的 `BrokeredSandboxIpcServer` 是单实例 Unix socket server，所有 Bash tool call 共享同一个 socket 端点。并发请求通过 Node.js 事件循环串行处理，不做显式加锁。

隔离粒度由 `toolCallId` 提供：每次 Bash tool call 注入独立的 `CODEBUDDY_SANDBOX_BROKER_TOOL_CALL_ID`，用于审计和备份归属。`sessionId` 校验防止跨 session 串请。

TOCTOU 风险评估：对于 text token request 路径，备份完成到 token 返回之间存在时间窗口，但沙箱内进程在收到 token 前无法通过 Seatbelt 执行真实写入，因此不存在传统 TOCTOU 的"check 后 use 前被篡改"问题。对于 host\-op 路径（rename/delete 等），backup \+ 真实操作都在 broker 侧的同一个 async 函数内顺序执行（check\-then\-act），Node.js 事件循环保证中间不会插入同一 socket 的其他请求，但不阻止沙箱外进程在窗口内修改文件——这是已知的信任边界。

### 超时与阻塞

zsh 侧有 socket 级超时设置；toybox 侧当前没有显式客户端超时。当前 agent\-cli 主链路不会在 broker IPC 内等待用户审批：需要审批时，broker 记录 prompt block 并返回拒绝/失败，让 sandbox attempt 结束，再由 `SandboxOrchestrator` 发起统一审批和 native rerun。

如果 broker 进程崩溃或 socket 被关闭，zsh/toybox 侧 `read()` 返回 EOF，命令会以 I/O 错误终止。

### 性能影响

toybox 的 open hook 是 eager 模式，每次 `open` 调用都会产生一次 IPC round\-trip。对于高频 open 的命令（如 `find`、`grep` 遍历大目录树），这会引入逐文件的 socket 通信开销。

当前没有 token 缓存或批量请求机制。read\-only 命令（如 `grep`）的每次 open 也会走 broker，但 broker 侧 read 路径不触发备份、不需要审批，处理开销较低。

实测在典型沙箱工作目录规模下（数百到数千文件），延迟影响可接受。如果未来需要覆盖大型 codebase 遍历场景，可以考虑引入 read token 缓存。

### 安全信任边界

broker IPC 的 Unix socket 使用文件权限隔离：

- socket 目录：`chmod 0o700`（仅当前用户可进入）。
- socket 文件：`chmod 0o600`（仅当前用户可读写）。

这意味着同机器上其他用户的进程无法连接 broker socket。但沙箱内进程与 agent\-cli 运行在同一用户下，因此沙箱内任何进程只要知道 socket 路径都能连接。

`sessionId` 通过环境变量 `CODEBUDDY_SANDBOX_BROKER_SESSION_ID` 注入沙箱，broker 侧校验请求中的 `sessionId` 必须匹配当前 session。沙箱内恶意进程可以读取环境变量获得合法 session ID，但这在当前威胁模型下是可接受的：沙箱内进程已经处于 Seatbelt 约束中，即使能发送请求，仍需通过 `fileSafety` 策略和用户审批才能获取写 token。broker 不是唯一防线，而是与 Seatbelt 沙箱、文件策略、用户审批共同构成纵深防御。

### symlink 路径解析

host service 对文件路径使用三种解析策略：

- `resolveExistingPath`：解析到真实路径，路径不存在时拒绝。用于 `chmod`（目标必须存在）和硬链接 source。
- `resolvePathThroughParent`：解析父目录到真实路径后拼接文件名，允许目标尚不存在。用于 `delete`、`mkdir`、`rename`/`copy` 的 source 和 target。
- `resolveExistingOrCreatablePath`：路径存在时解析到真实路径，不存在时解析父目录。用于 `touch`（可能创建新文件）和 token request。

所有策略都会在解析后执行 `refuseIfResolvedPathNotAllowed`：如果 symlink 解析后的真实路径落在安全策略不允许的范围内，即使 symlink 自身路径被允许，操作也会被拒绝。这防止通过 symlink 绕过沙箱文件策略边界。

### 路径规范化与规则匹配

排查"为什么某条规则没有命中"时，需要了解三层路径规范化：

**zsh 侧**：自编 zsh 的 `codebuddy_brokered_authorize_path()` 在发送 token request 前会对路径做 `/private/var` → `/var`、`/private/tmp` → `/tmp` 的 alias 归一化（macOS 特有的 firmlink 映射），确保请求路径与用户感知一致。

**toybox 侧**：`toybox_open()` 等 wrapper 在发送 text token request 前使用 `realpath` 风格解析，会解析 symlink、消除 `.`/`..`。但 `toybox_rename()` 使用 lexical absolute path（不解析 symlink），以保留 rename 操作本身的语义（rename 可能作用于 symlink 自身而非其目标）。

**agent\-cli 侧**：`normalisePathForRuleMatch()` 在做 fileSafety 规则匹配前执行：

- 反斜杠 → 正斜杠
- 去除 macOS BSD `sed -i` 产生的临时文件前缀（`.!<PID>!filename` → `filename`）
- home 目录前缀 → `~`
- `normaliseSandboxWritePath()` 额外做 `/private/var` → `/var`、`/private/tmp` → `/tmp`

调试时可以在日志中搜索 `phase=ipc-token` 或 `phase=host-policy`，日志会同时输出原始路径和规范化后路径（`path=` vs `normalisedPath=`），对照规则配置判断命中逻辑。

## 已知边界与不覆盖范围

当前方案覆盖的是“进入 macOS brokered shell runtime 的 Bash 命令”。

### 不进入 brokered shell 的执行路径

以下情况命令不会经过 brokered shell runtime，brokered 层的权限控制和备份均不生效：

- `sandbox.enabled = false` 或 `SandboxOrchestrator` 判定为 local 执行。
- `sandbox.excludedCommands` 命中：`SandboxShellService` 检查命令根后 fallback local。
- `dangerouslyDisableSandbox = true`：模型请求 bypass → 用户审批通过 → local 执行。
- 用户在沙箱执行失败后批准 native rerun（session\-scoped approval cache）：后续相同命令直接 local。
- `rawCommand` 模式：直接 spawn 可执行文件，不经 shell bootstrap，不前置 `brokered-bin`，不切自编 zsh。基础 sandbox/broker env 仍会注入，但 brokered shell 的 hook 链路不生效。
- vendor bundle 不完整：`brokered-sandbox-bash-env.sh`、`brokered-bin/codebuddy-toybox-dispatch`、`toybox`、`toybox.sb`、`zsh` 任一缺失会导致对应能力降级——缺 zsh 则不切自编 shell（重定向 hook 失效）；缺 toybox 或 brokered\-bin 则命令不经 toybox hook（open/rename hook 失效）。

### 进入 brokered shell 但不被覆盖的场景

- 绝对路径调用系统命令，例如 `/usr/bin/sed -i ...`，会绕开 `brokered-bin`，toybox hook 不生效。
- 命令显式重写 `PATH` 并把 `brokered-bin` 移到后面，可能绕开 toybox shim。
- dispatcher 遇到 toybox 不支持的 applet 或选项会 fallback 到系统命令；fallback 后不再具备 toybox open/rename hook。
- 外部二进制的内部写入、`ftruncate()`、`mmap` 写、原生 `rename()` 等不会被 toybox hook 看到。
- zsh 能覆盖 shell 自身重定向，但不能自动 hook 任意外部二进制的 libc 调用。

### 备份语义边界

- 当前内容备份只处理已存在的普通文件；目录、socket、设备文件、symlink 元数据、权限、mtime 等不是完整恢复对象。
- `touch` 主要是元数据修改。TS host service 可以在 host\-op 路径备份已有普通文件内容，但当前没有元数据级恢复语义。
- `cp` 当前主要依赖写目标的 open token 覆盖，不代表 toybox 已主动发送 JSON `copy`。
- 备份提交依赖 `FINAL_STOP` 的 `CommitModifyBackup`。如果进程异常退出，`sandbox-cli` 侧未提交备份周期的处理要按其存储策略判断。
- brokered shell 与 Write/Edit/MultiEdit 是不同链路。工具级文件编辑应该直接在工具写入前调用 `ModifyBackup`，不应依赖 shell runtime（当前 macOS 侧工具级备份尚未接入，详见"后续扩展建议"）。

## 验证方法

### agent\-cli 单元测试

重点测试：

bash
```
TS_NODE_PROJECT=tsconfig.tsnode.json npx mocha --require ts-node/register \
  --config ../../dev-packages/component/configs/mocharc.yml \
  --parallel=false \
  "./src/node/shell/brokered-bin-dispatch.spec.ts" \
  "./src/node/permission/brokered-sandbox/ipc-server.spec.ts" \
  "./src/node/permission/brokered-sandbox/host-service.spec.ts" \
  "./src/node/hooks/finalization-modify-backup-hook.spec.ts"
```
覆盖点：

- `truncate` shim 必须存在，并指向 `codebuddy-toybox-dispatch`。
- text write token 在已有普通文件上触发 `ModifyBackup`。
- `rename` host\-op 在 source / target 上触发 `ModifyBackup`。
- 备份失败时拒绝继续写入或 host operation。
- `FINAL_STOP` 时发送 `CommitModifyBackup`。

### toybox 构建与静态检查

在 `tsbx-macos` 仓库：

bash
```
./build-toybox-macos.sh
lipo toybox-0.8.13/toybox -verify_arch arm64 x86_64
strings toybox-0.8.13/toybox | grep '"operation":"rename"'
```
覆盖点：

- 产物是 macOS universal binary。
- 二进制包含 `HostFileOperation rename` 标记。

### fake broker 行为验证

用本地 fake broker 接收 socket 请求，分别执行：

bash
```
echo changed > file.txt
cp source.txt file.txt
mv source.txt file.txt
sed -i '' 's/a/b/g' file.txt
truncate -s 0 file.txt
```
预期：

- `>` 产生 zsh text write token request。
- `cp` 对目标产生 toybox text write token request。
- `mv` 产生 toybox JSON `HostFileOperation rename`。
- `sed -i` 在覆盖原文件时产生 toybox JSON `HostFileOperation rename`。
- `truncate` 产生 toybox text write token request。

### 产品级验证

在 WorkBuddy 开发版中：

1. 打开文件安全自动备份。
2. 运行沙箱 Bash 命令覆盖已有文件。
3. 查看 `~/.codebuddy/` 和 WorkBuddy dev 日志中的 broker shell 日志：
	- `phase=ipc-token`
	- `phase=ipc-token-backup`
	- `phase=ipc-host-op`
	- `phase=host-modify-backup`
	- `finalization-modify-backup`
4. 在备份查看入口确认备份记录存在，能定位备份并人工恢复（见下节）。

### 备份查看与恢复入口

当前备份查看入口在 WorkBuddy 设置页的文件安全面板（`SecurityCenterPanel` → `FileDetail`）：

1. 用户点击"查看备份" → UI 发送 `open-modify-backup-dir` 事件，携带当前会话 `sessionId`。
2. `workbuddy-server` 的 `SecurityCenterService.openModifyBackupDir()` 拼接备份目录路径：`<configDir>/workspace/sessions/<sessionId>/modify_backup`。
3. 调用 `openPath()` 在 Finder 中打开该目录。

当前是"打开备份目录"操作，不是一键恢复 UI。用户需要手动从目录中找到备份文件并恢复。如果目录不存在（本轮未产生备份），UI 会提示"当前会话无备份记录"。

## 后续扩展建议

### Write/Edit/MultiEdit 工具级备份

Brokered shell 只覆盖 Bash 命令。Write/Edit/MultiEdit/NotebookEdit 等工具不经过 zsh/toybox，应在工具写入前直接复用 `ModifyBackup`：

text
```
工具解析目标路径
  -> 权限判断
  -> 如果目标已存在且是普通文件，发送 ModifyBackup
  -> 工具执行真实写入
```
这条链路不应该依赖 broker shell，也不应该模拟 shell 命令。它和 brokered shell 共享的是 `sandbox-cli` 的备份存储协议，而不是 zsh/toybox runtime。

**当前状态**：`SandboxWriteRuleGuard` 已为 Write/Edit/MultiEdit/NotebookEdit 实现了工具级 guard（`GUARDED_WRITE_TOOLS`），能在沙箱模式下对写目标做权限判断和规则匹配。`ModifyBackup` 由 `isModifyBackupSupportedPlatform()` 门控，当前在 `win32` 与 `darwin` 上均启用；auto\-grant 由独立的 `supportsAutoGrantRuleEffect()` 门控，避免与备份平台能力耦合。

### 更完整的 syscall 覆盖

如果未来要覆盖任意外部二进制，toybox shim 不够，需要更底层方案，例如：

- 对外部二进制引入受控 wrapper。
- 使用可审计的动态库 interpose，但要评估 SIP、签名、稳定性和安全边界。
- 在 sandbox\-cli 层增强文件事件观测，但 macOS 对“修改前”备份时机的可控性有限。

当前方案选择 zsh \+ toybox，是在可控性、改动量、可维护性之间的折中。

### 元数据备份

当前 `ModifyBackup` 语义主要面向文件内容恢复。如果要支持 `touch` / `chmod` / `chown` / xattr 等元数据恢复，需要扩展备份记录结构：

- mode
- owner / group
- atime / mtime
- xattr
- symlink 本体和目标

这应作为独立能力设计，避免把内容备份语义复杂化。

### tsbx 文档同步

`tsbx-macos` 仓库应继续记录底层二进制构建、patch 和 demo。agent\-cli 本文档记录产品化集成链路。后续如果修改 zsh 或 toybox hook，需要同时更新：

- `tsbx-macos/README.md`
- `tsbx-macos/zsh-macos/README.md`
- `packages/agent-cli/docs/brokered-shell-macos.md`

## safe\-delete → broker IPC 统一删除链路

### 背景

safe\-delete shim（bash `rm`/`unlink`/`rmdir`、Node.js `fs.unlinkSync` 等、Python `os.remove` 等）原本各自通过 `genie-trash` 二进制或平台回收站 API 直接移入回收站。这条链路**缺少**以下能力：

1. fileSafety 策略检查（权限判断）
2. 符号链接解析安全校验
3. `ModifyBackup`（修改前备份）
4. 集中审计

而 brokered shell 的 toybox `rm` 已通过 `HostFileOperation delete → broker IPC → host service → trash` 实现了上述能力。

### 设计

将 safe\-delete 的删除入口统一路由到 broker IPC，使得**无论 brokeredShell 开关是否打开**，删除操作都经过 host service 的权限检查和备份。

```
safe-delete shim (bash/Node/Python)
  └─ try_broker_delete()
       ├─ broker 成功 (ok=true) → 完成，文件已移入回收站
       ├─ broker 拒绝 (deny) → fail-closed，不降级
       └─ broker 不可用 (exit 2) → fallback 到本地 trash_one() / trashItem()
```
### 关键改动

1. **`brokered-shell-env.ts`**：broker IPC 环境变量（`CODEBUDDY_BROKERED_FS_HOOK_ENABLED`、`CODEBUDDY_SANDBOX_BROKER_IPC_ADDRESS` 等）仅在 WorkBuddy Desktop 环境下注入，但不受 `brokeredShell` disabled 开关控制。`brokeredShell` 仅控制托管 runtime 产物（toybox、zsh、brokered\-bin）的注入。
2. **`safe-delete-broker-delete.cjs`**（新增）：独立 CJS 脚本，bash shim 可通过 `node safe-delete-broker-delete.cjs <path>` 调用。连接 broker IPC Unix socket，发送 `HostFileOperation delete` 请求。Exit code: 0\=成功，1\=拒绝（fail\-closed），2\=不可用（fallback）。
3. **`safe-delete-common.sh`**：`try_trash()` 前新增 `try_broker_delete()`，优先走 broker IPC。
4. **`node-safe-delete-shim.cjs`**：`tryTrash()` 前新增 `tryBrokerDelete()`，同步调用 broker IPC（`spawnSync` \+ helper script 模式，与 `node-brokered-fs-shim.cjs` 一致）。
5. **`safe-delete-env.ts`**：注入 `CODEBUDDY_SAFE_DELETE_BROKER_DELETE` 环境变量（指向 `safe-delete-broker-delete.cjs` 路径）。

### 旧代码的保留

本地 trash 逻辑（`trash_darwin()` / `trashOnMac()` / `_platform_trash()` / `genie-trash` 二进制）**不删除**，作为 broker IPC 不可用时的 fallback：

- 非 macOS 平台
- sandbox 未启用（IPC server 不存在）
- agent\-cli 独立 CLI 模式
- IPC server 未启动或 socket 连接失败