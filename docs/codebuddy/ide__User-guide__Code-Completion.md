# 代码补全

CodeBuddy IDE 在您编写代码时提供智能代码补全，帮助您更快、更高效地编写代码。

## 关于代码补全

CodeBuddy 在您编码时提供内联补全。基于当前代码内容和项目上下文分析，提供多行代码补全，帮助您更高效地完成代码编写。

CodeBuddy 支持众多编程语言和各种框架，包括 Python、JavaScript、TypeScript、Java、C/C\+\+、Go、Ruby 等。

## 触发代码补全

### 自动触发

代码补全会在您输入时自动触发。当您：

- 开始新的一行
- 在缩进后输入
- 输入括号或其他分隔符
- 将光标移动到行尾

CodeBuddy 会分析您的上下文并生成适当的补全。

### 手动触发

您可以使用快捷键手动触发代码补全：

| 平台 | 快捷键 |
| --- | --- |
| macOS | `Option + \` |
| Windows/Linux | `Alt + \` |

## 接受补全

当补全出现时，您有以下几个选项：

### 接受全部补全

按 `Tab` 键接受完整的补全。

### 逐行接受

仅接受补全的下一行：

| 平台 | 快捷键 |
| --- | --- |
| macOS | `Cmd + Down` |
| Windows/Linux | `Ctrl + Down` |

### 逐词接受

仅接受补全的下一个词：

| 平台 | 快捷键 |
| --- | --- |
| macOS | `Cmd + Right` |
| Windows/Linux | `Ctrl + Right` |

## 取消补全

要取消补全而不接受它，请按 `Escape` 键。

## 下一步编辑建议 (NES)

下一步编辑建议是一项高级功能，它根据您的编辑历史和上下文预测您下一步可能的编辑操作。与仅从光标位置继续编写的传统内联补全不同，NES 可以在代码的不同位置建议编辑。

### NES 工作原理

- 分析您最近的编辑模式
- 预测您接下来可能想要编辑的内容
- 显示可能跨越多行或影响代码不同部分的建议

### 手动触发 NES

| 平台 | 快捷键 |
| --- | --- |
| 所有平台 | `Ctrl + Shift + Enter` |

### 接受 NES 建议

当 NES 建议出现时，按 `Tab` 键接受。按 `Escape` 键取消。

### 启用/禁用 NES

NES 默认启用。要切换它：

1. 打开命令面板 (`Cmd/Ctrl + Shift + P`)
2. 搜索 "CodeBuddy: Quick Settings"
3. 切换 "Next Edit Suggestions"

或在设置中配置：

1. 打开设置 (`Cmd/Ctrl + ,`)
2. 搜索 `codingcopilot.enableNextEditSuggestions`
3. 切换该设置

## 切换补全模型

您可以在不同的 AI 模型之间切换用于代码补全：

1. 打开命令面板 (`Cmd/Ctrl + Shift + P`)
2. 搜索 "CodeBuddy: Change Completions Model"
3. 选择您要使用的模型

或通过快速设置访问：

1. 点击状态栏中的 CodeBuddy 图标
2. 选择 "Change Completions Model"

## 配置代码补全

### 全局启用/禁用自动补全

1. 打开设置 (`Cmd/Ctrl + ,`)
2. 搜索 `codingcopilot.enableAutoCompletions`
3. 切换该设置

或使用快速设置：

1. 打开命令面板 (`Cmd/Ctrl + Shift + P`)
2. 搜索 "CodeBuddy: Quick Settings"
3. 切换 "Auto Completions"

### 为特定语言启用/禁用

您可以控制特定编程语言的代码补全：

1. 打开设置 (`Cmd/Ctrl + ,`)
2. 搜索 `codingcopilot.enableCompletionLanguage`
3. 配置特定语言的设置

`settings.json` 中的配置示例：

json
```
{
  "codingcopilot.enableCompletionLanguage": {
    "python": true,
    "javascript": true,
    "markdown": false,
    "plaintext": false
  }
}
```
您也可以通过快速设置切换当前文件语言的补全。

### 生成偏好

控制代码补全的风格：

1. 打开设置 (`Cmd/Ctrl + ,`)
2. 搜索 `codingcopilot.generationPreference`
3. 选择：
	- **智能模式**：根据上下文提供多行补全
	- **单行模式**：将补全限制为单行

## IDE 设置配置

您也可以通过 IDE 设置面板配置代码补全：

1. 点击侧边栏或状态栏中的 CodeBuddy 图标
2. 打开设置
3. 导航到 **Tab** 部分

![alt text](/docs/static/ide-settings-tab.DIExMfnu.png)

Tab 设置页面提供：

- **Auto Completion**：切换开关以启用/禁用实时代码补全
- **Language Rules**：配置各个语言是否启用自动补全。语言级别的规则会覆盖全局设置——即使 Auto Completion 关闭，在此处明确启用的语言仍会提供补全
- **Generation Preference**：选择智能模式（基于上下文的多行补全）或单行模式

## 快捷键参考

| 操作 | macOS | Windows/Linux |
| --- | --- | --- |
| 触发补全 | `Option + \` | `Alt + \` |
| 接受全部 | `Tab` | `Tab` |
| 接受一行 | `Cmd + Down` | `Ctrl + Down` |
| 接受一词 | `Cmd + Right` | `Ctrl + Right` |
| 取消 | `Escape` | `Escape` |
| 触发 NES | `Ctrl + Shift + Enter` | `Ctrl + Shift + Enter` |