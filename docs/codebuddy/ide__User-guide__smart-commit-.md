# 智能提交

智能提交（Smart Commit）是 CodeBuddy 提供的 Git 提交辅助功能，能够自动分析代码变更内容，智能生成规范的 commit message，帮助开发者规范开发流程，提升团队协作效率。

### 功能特性

- **智能分析**：自动分析代码变更内容，理解修改意图
- **规范生成**：生成符合 Conventional Commits 规范的提交信息
- **一键提交**：简化 Git 提交流程，提升开发效率
- **多语言支持**：支持中英文 commit message 生成

### 使用智能提交

#### 通过 Git 面板触发

点击将单个或全部文件添加到暂存区。然后点击消息右部的“AI COMMIT”按钮

![alt text](/docs/static/Pasted%20image%2020260112213623.DJphmnXe.png)

1. 在 IDE 的 Git 面板中，查看待提交的文件变更
2. 点击 CodeBuddy 的智能提交按钮
3. Agent 自动分析变更内容，生成 commit message
4. 确认无误后，点击提交即可

### Commit Message 规范

智能提交生成的 commit message 遵循 Conventional Commits 规范：

text
```
<type>(<scope>): <subject>

<body>
```
#### 常用类型（type）

| 类型 | 说明 |
| --- | --- |
| `feat` | 新功能 |
| `fix` | 修复 bug |
| `docs` | 文档变更 |
| `style` | 代码格式调整（不影响代码逻辑） |
| `refactor` | 代码重构（既不是新功能也不是修复 bug） |
| `perf` | 性能优化 |
| `test` | 添加或修改测试 |
| `chore` | 构建过程或辅助工具的变动 |

### 使用示例

假设您修改了登录模块的验证逻辑，智能提交可能生成如下 commit message：

text
```
fix(auth): 修复登录验证失败时的错误提示

- 修复用户名为空时未显示错误提示的问题
- 优化密码错误时的提示文案
- 添加登录失败次数限制
```
### 常见问题

#### 如何修改已生成的 commit message？

生成的 commit message 可以在提交前进行手动编辑，根据实际情况进行调整。

#### 支持哪些 Git 操作？

智能提交主要支持：

- 生成 commit message
- 执行 git commit
- 可配合其他 Git 操作使用（如 push、merge 等）