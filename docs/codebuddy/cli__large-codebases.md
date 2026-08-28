# 在 Monorepo 或大型代码库中设置 CodeBuddy Code

> 为 monorepo 和大型单树代码库配置 CodeBuddy Code，使用嵌套的 CODEBUDDY.md 文件、稀疏 worktrees、代码智能和按包技能，使 CodeBuddy 专注于你正在处理的代码。

大型代码库可以是拥有数百万行代码的单个存储库，也可以是包含许多包的 monorepo。 CodeBuddy Code 可以在任何规模下工作，但随着代码库的增长，为较小项目调整的默认设置可能会用与任务无关的指令和文件读取填满上下文窗口，浪费 tokens 并降低 CodeBuddy 的性能。

本指南向个人开发者和工程团队展示如何将 CodeBuddy 的范围限制在任务涉及的代码库部分。每个部分都说明该设置是个人的还是提交到存储库的。

## 本指南涵盖的内容

下面的[表格](#本页面的设置)列出了每个设置及其作用。[之后的文件树](#示例-monorepo)是本页面每个代码示例所引用的示例 monorepo。

### 本页面的设置

下面的每个设置都是独立的。它们相互叠加而不是相互替换，因此应用适合你的存储库的任何设置。[选择从哪里启动 CodeBuddy](#选择从哪里启动-codebuddy) 决定了你的设置文件的位置，所以先阅读它。[将其整合在一起](#将其整合在一起)展示了所有这些设置的组合。

| 我想要 | 使用 |
| --- | --- |
| 仅加载你接触的代码的约定，而不是一个根文件覆盖每个子系统 | 按目录的 [CODEBUDDY.md 文件](#按目录分层-codebuddy-md-文件) |
| 阻止 CodeBuddy 打开构建输出、生成的代码和供应商依赖 | `permissions.deny` 中的 [`Read` 拒绝规则](#阻止读取生成的和供应商代码) |
| 通过语言服务器而不是扫描文件来查找符号的定义或调用者 | [代码智能插件](#使用代码智能减少文件读取) |
| 当 CodeBuddy 创建 worktree 时仅检出任务需要的目录 | [`worktree.sparsePaths`](#仅检出你需要的目录) |
| 从同一会话中读取和编辑同级包或另一个存储库 | [`--add-dir`](#跨包或存储库授予访问权限) 或 `additionalDirectories` |
| 给 CodeBuddy 特定于一个区域的程序，仅在相关时加载 | 按目录的 [skills](#添加按目录-skills) |
| 用一套每个人都安装的约定替换许多按目录的 CODEBUDDY.md 文件 | 内部市场中的 [plugin](#当分层停止扩展时集中约定) |

> **提示**：有关在任何存储库中保持上下文较小的工作流技术，例如[在子代理中运行探索](./best-practices#用子代理做调研)以使文件读取不会进入主对话，请参阅 [CodeBuddy Code 最佳实践](./best-practices)。

### 示例 monorepo

本页面的示例引用了一个包含三个包的 monorepo。相同的模式适用于大型单树代码库：其中示例使用 `packages/api/`，替换为你自己的子系统目录，例如 `src/backend/` 或 `lib/core/`。

text
```
monorepo/
  CODEBUDDY.md                # 根指令
  packages/
    api/
      CODEBUDDY.md              # API 特定指令
      .codebuddy/skills/
      src/
    web/
      CODEBUDDY.md              # 前端特定指令
      .codebuddy/skills/
      src/
    shared/
      CODEBUDDY.md              # 共享库指令
      src/
```
## 选择从哪里启动 CodeBuddy

你启动 `codebuddy` 的位置决定了 CodeBuddy 可以读取和编辑哪些文件而无需额外权限授予、在启动时加载哪些 CODEBUDDY.md 文件，以及哪些项目设置适用。

| 从以下位置启动 | 文件访问 | 启动时加载的 CODEBUDDY.md | 使用场景 |
| --- | --- | --- | --- |
| 存储库根目录 | 每个文件 | 仅根目录；当 CodeBuddy 在那里读取时，子目录文件按需加载 | 任务跨越多个包或子系统 |
| 子目录 | 仅该子树，直到你授予更多权限 | 该目录的加上每个祖先的 | 工作范围限于一个包或子系统 |

`.codebuddy/settings.json` 中的项目设置仅从你的启动目录加载，不像 CODEBUDDY.md 文件那样从父目录继承：存储库根目录的 `.codebuddy/settings.json` 仅在你从根目录启动时适用。

下面的每个部分都说明其设置文件应该位于存储库根目录还是你启动的子目录中，以及它是提交的还是保持本地的。

## 按目录分层 CODEBUDDY.md 文件

在大型代码库中，存储库根目录的单个 CODEBUDDY.md 往往要么增长到覆盖每个子系统的约定，在与当前任务无关的指令上浪费上下文，要么保持太通用而无用。将指令分散在按目录的文件中意味着 CodeBuddy 加载存储库范围的规则加上仅你正在处理的代码的约定。

CodeBuddy Code 在启动时从你的工作目录和每个父目录加载每个 [CODEBUDDY.md](./memory) 文件，然后当它在那里读取文件时按需加载每个子目录的文件。根文件设置存储库范围的规则，每个子目录添加自己的规则。

常见的分割是两个级别：

- **根 `CODEBUDDY.md`**：适用于任何地方的指令，例如编码标准、提交约定和存储库布局
- **按子目录 `CODEBUDDY.md`**：特定于该区域堆栈的约定。在 monorepo 中，这是每个包一个。在大型单树中，它是每个子系统一个，例如 `src/db/` 或 `src/api/`

将这些文件提交到存储库，以便队友继承它们。每个目录的所有者通常维护其文件。

根 `CODEBUDDY.md` 将 CodeBuddy 定向到存储库结构：

markdown
```
# CODEBUDDY.md

这是一个 monorepo，在 packages/ 下有三个包：

- packages/api：使用 Express、TypeScript 和 PostgreSQL 的 Node.js REST API
- packages/web：使用 Vite、TypeScript 和 TailwindCSS 的 React 前端
- packages/shared：由 api 和 web 都使用的共享 TypeScript 实用程序

从包目录运行命令，而不是从 monorepo 根目录。
每个包都有自己的 tsconfig.json、package.json 和测试套件。
```
每个子目录的 `CODEBUDDY.md`，这里是 `packages/api/CODEBUDDY.md`，添加特定于该区域堆栈的上下文：

markdown
```
# packages/api/CODEBUDDY.md

这个包是 REST API 服务器。

- 运行测试：`npm test`（使用 Vitest）
- 运行开发服务器：`npm run dev`（端口 3001）
- 数据库迁移：`npm run migrate`
- 环境变量：将 `.env.example` 复制到 `.env`

API 路由在 src/routes/ 中。每个路由文件导出一个 Express 路由器。
数据库查询在 src/db/ 中使用 Knex。永远不要在路由处理程序中写原始 SQL 字符串。
```
当你从 `packages/api/` 启动 CodeBuddy 时，它加载 `packages/api/CODEBUDDY.md` 和根 `CODEBUDDY.md`。CodeBuddy 看到本地指令与存储库范围的规则一起，上下文中没有来自 `packages/web/` 的指令。对于非 monorepo 树中的任何子目录也是如此。

保持文件随着代码库和模型变化而最新的几种方法：

- **在拉取请求中审查**：像对待任何其他文档更改一样对待 CODEBUDDY.md 编辑，以便约定跟踪代码
- **在主要模型发布后重新访问**：适用于较旧模型限制的指令一旦较新模型自己处理该情况，可能会变成开销。例如，强制单文件重构的规则一旦限制消失就可以删除
- **添加一个 Stop hook 来提议更新**：[`Stop` hook](./hooks#stop) 在 CodeBuddy 完成响应时接收会话记录的路径，所以脚本可以审查会话并在暴露的差距仍然新鲜时提议 CODEBUDDY.md 更新

有关 CODEBUDDY.md 文件如何加载和交互的更多信息，请参阅 [内存和项目指令](./memory)。

### 在按目录 CODEBUDDY.md 和路径范围规则之间选择

按目录的 `CODEBUDDY.md` 文件和 `.codebuddy/rules/` 下的[路径范围规则](./memory#使用-codebuddy-rules-实现模块化规则)都允许你将指令定向到树的一部分。它们在文件位置和加载时间上有所不同。

| 方法 | 文件位置 | 加载时间 | 使用场景 |
| --- | --- | --- | --- |
| 按目录 `CODEBUDDY.md` | 在目录内，与其代码一起 | 从该目录启动时在启动时，或当 CodeBuddy 在那里读取文件时按需 | 目录所有者维护自己的约定；指令与代码一起版本化 |
| `.codebuddy/rules/` 中的路径范围规则 | 存储库根目录的中央 `.codebuddy/` | 当 CodeBuddy 处理与规则的 `paths:` glob 匹配的文件时 | 你想要一个地方的所有约定，或相同的规则适用于许多分散的路径 |

## 减少 CodeBuddy 读取的内容

指令只是最终进入 CodeBuddy 上下文的一部分。文件读取是另一个随着代码库增长而增加的成本。下面的设置阻止读取不相关的路径，并用语言服务器查找替换详尽的文件扫描。

### 阻止读取生成的和供应商代码

CodeBuddy 的内容搜索默认尊重 `.gitignore`，所以已列在其中的路径，例如 `node_modules/`、`dist/` 和 `build/`，无需额外配置就会保持在搜索结果之外。

对于已检入的路径，例如供应商 SDK 或提交的生成代码，在 `permissions.deny` 中添加 `Read` 拒绝规则以阻止 CodeBuddy 打开这些文件，即使搜索列出了它们。

要为在存储库中工作的每个人应用这些排除，将它们提交到 `.codebuddy/settings.json`。要保持个人，改用 `.codebuddy/settings.local.json`。与本页面的其他项目设置一样，这些文件仅从你的启动目录加载。如果你从那里启动 CodeBuddy，将它们放在存储库根目录，或如果你从子目录启动，放在每个包的 `.codebuddy/` 中。

下面的示例阻止构建工件和供应商 SDK：

json
```
// .codebuddy/settings.json
{
  "permissions": {
    "deny": [
      "Read(./**/dist/**)",
      "Read(./**/build/**)",
      "Read(./**/*.generated.*)",
      "Read(./vendor/**)"
    ]
  }
}
```
拒绝规则涵盖 CodeBuddy 的内置文件工具和识别的 Bash 文件命令，包括 `cat`、`head`、`grep` 和 `find`，当拒绝的路径作为参数传递时。它们不会从递归搜索的输出中过滤拒绝的路径，也不涵盖自己打开文件的任意子进程。有关完整的模式语法，请参阅 [Read 和 Edit 权限规则](./permissions#read-edit-write)。

### 使用代码智能减少文件读取

在大型代码库中，查找符号的定义或使用位置可能需要许多文件读取和 grep 调用。[代码智能插件](./plugins)将 CodeBuddy 连接到语言服务器，以便它可以跳转到定义、查找引用和直接显示类型错误，而不是扫描树。

官方市场有 TypeScript、Python、Go、Rust 和其他常见语言的插件。下面的示例安装 TypeScript 插件：

bash
```
/plugin install typescript-lsp@claude-plugins-official
```
要为存储库中的每个人启用插件而不是自己安装，将其添加到 [`enabledPlugins` 项目设置](./settings#插件设置)。

代码智能插件需要每个开发者机器上的语言的语言服务器二进制文件。从官方市场安装需要网络访问 GitHub，市场在那里托管。在受限网络上，[从内部 Git 主机或本地路径添加市场](./plugin-marketplaces#其他-git-主机)。

这与上面的 `Read` 拒绝规则配对良好。拒绝规则保持不相关的内容不进入上下文，代码智能保持 CodeBuddy 不读取剩余的内容来定位定义。

## 范围 Worktrees 和文件访问

这些设置控制 worktrees 中磁盘上的内容以及 CodeBuddy 可以读取和写入的超出启动点的目录。

### 仅检出你需要的目录

`--worktree` 标志在新的 git worktree 中启动会话，以便更改与主检出隔离。默认情况下，它检出整个存储库。在大型存储库中，`worktree.sparsePaths` 设置使用 git sparse\-checkout 仅将列出的目录加上根级文件写入磁盘，以便 worktrees 启动更快并使用更少空间。

如果在此目录中工作的每个人都需要相同的路径，将设置提交到 `.codebuddy/settings.json`。要为自己添加路径，使用 `.codebuddy/settings.local.json`：列表在范围内合并，所以本地文件可以向提交的列表添加路径但不能删除它们。下面的示例显示提交的文件：

json
```
// .codebuddy/settings.json
{
  "worktree": {
    "sparsePaths": [
      ".codebuddy",
      "packages/api",
      "packages/shared"
    ]
  }
}
```
当 CodeBuddy 创建 worktree 时，它仅检出 `.codebuddy/`、`packages/api/` 和 `packages/shared/` 而不是完整树。`sparsePaths` 中的路径相对于存储库根目录，无论你从哪个子目录启动 CodeBuddy。任何目录路径都可以在这里工作，不仅仅是包根。

这对于[子代理 worktree 隔离](./worktree#子代理隔离)特别有用。子代理是为子任务生成的并行 CodeBuddy 实例，每个在 worktree 中运行的都获得轻量级检出而不是完整树。会话中的所有 worktrees 共享相同的 `sparsePaths`，所以如果一个子代理需要 `packages/api/` 而另一个需要 `packages/web/`，列出两者。

在`sparsePaths` 中列出目录，而不是单个文件。根级文件如 `package.json`、`tsconfig.base.json` 和锁文件始终与你列出的目录一起检出。根级目录不是，所以如果你想要存储库根目录的 `.codebuddy/settings.json`、`.codebuddy/rules/` 或 `.codebuddy/skills/` 在 worktree 内可用，请在列表中包含 `.codebuddy`。

要避免在 worktrees 中复制大型目录如 `node_modules`，将 `sparsePaths` 与同一 `.codebuddy/settings.json` 中的 `symlinkDirectories` 配对：

json
```
// .codebuddy/settings.json
{
  "worktree": {
    "sparsePaths": [
      ".codebuddy",
      "packages/api",
      "packages/shared"
    ],
    "symlinkDirectories": [
      "node_modules"
    ]
  }
}
```
这创建了一个从每个 worktree 的 `node_modules/` 回到主存储库副本的符号链接，而不是在磁盘上复制它。

> **注意**：`sparsePaths` 和 `symlinkDirectories` 设置在创建 worktree 之前从你的启动目录读取。创建后，会话的工作目录是 worktree 根，而不是你启动的子目录。因此，worktree 内的项目设置从 worktree 根的 `.codebuddy/settings.json`（存储库根文件的检出副本）加载。将你在 worktrees 内需要的任何其他设置（例如权限规则或 hooks）放在存储库根的 `.codebuddy/settings.json` 中。

有关完整的 worktree 设置参考，请参阅 [Worktree 设置](./worktree)。

### 跨包或存储库授予访问权限

当你从子目录启动 CodeBuddy 时，或当任务跨越多个检出时，本部分适用。如果你在单个大型树中从存储库根目录启动，CodeBuddy 已经可以访问每个文件，你可以跳过此部分。

当你从 `packages/api/` 启动 CodeBuddy 时，它可以读取和写入该目录内的文件。如果任务需要跨包更改，例如更新 `api` 和 `web` 都导入的共享类型，你需要授予对同级目录的访问权限。相同的机制授予对单独检出的存储库的访问权限。

`.codebuddy/settings.json` 中的 `additionalDirectories` 设置给 CodeBuddy 访问工作目录外的目录。下面的示例授予对两个同级包的访问权限：

json
```
// .codebuddy/settings.json
{
  "permissions": {
    "additionalDirectories": [
      "../shared",
      "../web"
    ]
  }
}
```
相对路径相对于你启动 CodeBuddy 的目录解析。使用此配置，CodeBuddy 可以在从 `packages/api/` 工作时读取和编辑 `packages/shared/` 和 `packages/web/` 中的文件。

你也可以在运行时不编辑设置而授予访问权限，通过在启动 CodeBuddy 时传递 `--add-dir`：

bash
```
codebuddy --add-dir ../shared
```
无论你如何添加目录，CodeBuddy 都可以读取和编辑其中的文件。目录的 CODEBUDDY.md、`.codebuddy/rules/` 文件和 skills 是否也加载取决于你如何添加它：

| 添加方式 | 加载 CODEBUDDY.md 和规则 | 加载 skills |
| --- | --- | --- |
| `additionalDirectories` 设置 | 从不 | 从不 |
| `--add-dir` 标志或 `/add-dir` 命令 | 仅使用下面的环境变量 | 是 |

要从使用 `--add-dir` 或 `/add-dir` 添加的目录加载 CODEBUDDY.md 和规则文件，设置 `CODEBUDDY_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` 环境变量：

bash
```
CODEBUDDY_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 codebuddy --add-dir ../shared
```
环境变量对 `additionalDirectories` 设置中列出的目录没有影响。详见[记忆文档](./memory)。

对于此区域中的每个人都需要的同级目录，将 `additionalDirectories` 提交到 `.codebuddy/settings.json`。对于个人选择或一次性访问，使用 `.codebuddy/settings.local.json` 或在启动时传递 `--add-dir`。

## 添加按目录 Skills

任何子目录都可以定义 [skills](./skills) 范围限于其自己的堆栈。skill 在 CodeBuddy 确定其相关时按需加载，所以 API 特定的工具在前端工作期间不会消耗上下文。

Skills 位于目录内的 `.codebuddy/skills/` 下。将它们与该区域的代码一起提交，以便克隆存储库的任何人都能获得它们。在 monorepo 中，这可以是每个包一套 skills。在大型单树代码库中，它是每个子系统一套，例如 `src/db/.codebuddy/skills/`。

在子目录内创建一个 skill 目录：

bash
```
mkdir -p packages/api/.codebuddy/skills/api-testing
```
然后在该目录内写 `SKILL.md`，这里是 `packages/api/.codebuddy/skills/api-testing/SKILL.md`。此示例教 CodeBuddy API 包的测试模式：

markdown
```
---
name: api-testing
description: API 包的测试模式。在 packages/api/ 中编写或修改测试时使用。
---

## 测试结构

测试在 `src/__tests__/` 中，镜像 `src/` 目录结构。
每个路由文件都有一个对应的 `.test.ts` 文件。

## 运行测试

- 所有测试：`npm test`
- 单个文件：`npm test -- src/__tests__/routes/users.test.ts`
- 监视模式：`npm test -- --watch`

## 测试实用程序

- `src/__tests__/helpers/db.ts`：提供 `setupTestDb()` 和 `teardownTestDb()` 用于数据库测试
- `src/__tests__/helpers/auth.ts`：提供 `createTestUser()` 和 `getAuthToken()` 用于认证端点

## 模式

- 使用 `supertest` 进行 HTTP 断言，而不是原始 fetch
- 始终在回滚的事务中包装数据库测试
- 在 `src/__tests__/mocks/` 中模拟外部服务
```
不同的子目录以相同的方式保存不同的 skills：`packages/web/.codebuddy/skills/component-patterns/` 描述前端的组件约定而不是测试。当 CodeBuddy 处理 `packages/api/` 中的文件时，它加载 api\-testing skill。当它在 `packages/web/` 中工作时，它加载 component\-patterns 代替。在另一个的任务期间，两个目录的 skills 都不加载。

你也可以按文件模式而不是按位置范围 skill。[`paths` frontmatter 字段](./skills#frontmatter-字段)采用 glob 模式，CodeBuddy 仅在处理匹配文件时自动加载 skill。对于位于存储库根目录的 `.codebuddy/skills/` 中但仅适用于某些文件（无论它们出现在哪里）的 skill，使用此功能，例如范围限于 `**/migrations/**` 的数据库迁移 skill。

有关创建和组织 skills 的更多信息，请参阅 [Skills](./skills)。

### 保持 Skills 可发现

随着 skills 分散在许多目录中，CodeBuddy 选择的列表可能会增长很大。CodeBuddy 通过读取每个发现的 skill 的名称和描述来选择 skill，只有选定的 skill 的完整内容加载到上下文中。本部分涵盖如何保持该列表较小以及编写在缩短时幸存的描述。

哪些 skills 在范围内取决于你从哪里启动 CodeBuddy：

- **从子目录如 `packages/api/`**：来自该目录、每个父目录直到存储库根目录以及用户级别的 skills
- **从存储库根目录**：来自 CodeBuddy 在会话期间接触的每个子目录的 skills，可能累积到数百个
- **在使用 [`--add-dir`](#跨包或存储库授予访问权限) 添加同级后**：该同级的 skills 也加载。`additionalDirectories` 设置仅授予文件访问权限，不加载 skills

名称始终加载，但当有许多时描述会被缩短，这可能会剥离 CodeBuddy 用来决定 skill 是否适用的关键字。保持描述简短并以请求会包含的词开头，例如"在 `packages/api/` 中编写或修改测试"。

对于许多目录共享的 skills，例如 PR 约定或部署检查清单，将它们放在存储库根目录的 `.codebuddy/skills/` 中，以便从任何启动目录加载。当共享 skills 需要自己的版本历史或必须跨存储库工作时，改为将它们打包为 [插件](./plugins)。插件 skills 使用 `plugin-name:skill-name` 命名空间，所以它们永远不会与按目录的 skills 冲突。平台团队可以在一个地方对它们进行版本化和更新。

## 当分层停止扩展时集中约定

随着代码库的增长，按目录的 CODEBUDDY.md 文件可能变得难以管理。约定漂移，文件变得陈旧，没有人拥有根目录。解决这个问题通常落在维护存储库 CodeBuddy Code 设置的团队身上，而不是在自己的区域中工作的每个开发者。

将约定和参考内容从始终加载的 CODEBUDDY.md 移出到按需加载的机制中：

- [Skills](./skills)：CodeBuddy 仅在与任务相关时加载的参考材料
- [Plugins](./plugins)：平台团队集中拥有的 skills、hooks 和命令的版本化包
- [MCP servers](./mcp)：如果你的组织已经在存储库上运行代码搜索或 RAG 索引，将其公开为 MCP 工具，以便 CodeBuddy 查询它而不是直接读取文件

### 在会话启动时推荐正确的插件

一旦约定位于插件中，在树的陌生部分启动 CodeBuddy 的队友就没有关于该区域所有者维护哪个插件的信号。[`SessionStart` hook](./hooks#sessionstart) 可以弥补这个差距，因为 hook 打印到 stdout 的任何内容都会在第一个提示之前添加到 CodeBuddy 的上下文中。

例如，你可以编写一个脚本，从 [hook 输入](./hooks#hook-输入)读取启动目录，在提交到存储库的路径到插件映射中查找它，并打印建议供 CodeBuddy 在其第一个回复中中继。查看[使用 hooks 自动化操作](./hooks-guide)来编写和注册 hook。

## 将其整合在一起

下面的组合配置使用 monorepo 布局。相同的文件适用于大型单树中的任何子目录。项目设置仅从你启动 CodeBuddy 的目录加载，所以每个子目录的 `.codebuddy/settings.json` 必须是自包含的而不是分层在根文件上。

示例在 `.codebuddy/settings.json` 中提交 `worktree`、`additionalDirectories` 和 `Read` 拒绝规则，以便 `packages/api/` 中的每个开发者获得相同的同级访问、稀疏路径和排除。下面的文件是 `packages/api/` 的提交的按区域设置：

json
```
// packages/api/.codebuddy/settings.json
{
  "worktree": {
    "sparsePaths": [
      ".codebuddy",
      "packages/api",
      "packages/shared"
    ],
    "symlinkDirectories": [
      "node_modules"
    ]
  },
  "permissions": {
    "additionalDirectories": [
      "../shared"
    ],
    "deny": [
      "Read(./**/dist/**)",
      "Read(./**/build/**)"
    ]
  }
}
```
因为此会话从 `packages/api/` 启动，同级包的 CODEBUDDY.md 文件已经超出范围。如果你也从根目录启动会话，可以将排除规则添加到存储库根目录的 `.codebuddy/settings.local.json`。

`additionalDirectories` 条目在你直接从 `packages/api/` 启动 CodeBuddy 时适用。在从此会话创建的 worktree 内，工作目录是 worktree 根，所以此设置文件不加载。同级包已经在 worktree 内可达而无需它，但拒绝规则需要在存储库根目录的 `.codebuddy/settings.json` 中的第二个副本，以便 worktree 会话获取它们，如 [worktree 设置注释](#仅检出你需要的目录) 所述：

json
```
// .codebuddy/settings.json
{
  "permissions": {
    "deny": [
      "Read(./**/dist/**)",
      "Read(./**/build/**)"
    ]
  }
}
```
设置后，存储库具有此布局：

text
```
monorepo/
  CODEBUDDY.md
  .codebuddy/settings.json                # worktree 会话的拒绝规则
  packages/
    api/
      CODEBUDDY.md
      .codebuddy/settings.json                    # worktree、additionalDirectories、拒绝规则
      .codebuddy/skills/api-testing/SKILL.md
    web/
      CODEBUDDY.md
      .codebuddy/skills/component-patterns/SKILL.md
    shared/
      CODEBUDDY.md
```
使用此设置，从 `packages/api/` 启动 CodeBuddy：

- 加载根 CODEBUDDY.md 和 `packages/api/CODEBUDDY.md`，跳过 `packages/web/CODEBUDDY.md`
- 可以读取和编辑 `packages/api/` 和 `packages/shared/` 中的文件
- 跳过 `packages/api/` 中 `dist/` 和 `build/` 下的构建输出读取
- 有 api\-testing skill 按需可用
- 创建包含 `.codebuddy/`、`packages/api/`、`packages/shared/` 和根级文件的 worktrees，拒绝规则从根设置文件应用于整个 worktree

## 范围和计划跨包的更改

上面的配置控制 CodeBuddy 看到的内容。当单个更改涉及多个包时，例如更新共享类型以及使用它的每个调用站点，你如何范围和排序任务也会影响结果。

两种技术帮助保持跨包更改的一致性：

- **在一个会话中给 CodeBuddy 整个更改**：将共享编辑及其调用站点一起交付保持每个编辑背后的决策一致，而不是按包重新推导它们
- **在编辑前将计划保存到文件**：[先计划](./best-practices#先探索-再规划-后编码)并要求 CodeBuddy 将计划写入存储库中的 markdown 文件。长的跨包会话在进行中压缩其上下文，保存的计划在对话历史可能不会的地方幸存

## 后续步骤

一旦此配置就位，你可以细化它：

- 使用 [hooks](./hooks-guide) 在 CodeBuddy 编辑文件后运行按目录的 linters 或类型检查器
- 查看 [有效管理成本](./costs) 以了解代码库大小如何影响 token 使用以及如何在更广泛推出前设置支出限制