Craft 在安装 MCP 服务器的过程中，在终端下执行命令时可能会出现 “Shell Integration Unavailable” 的问题，即 shell 集成不可用的问题。本文将针对此类问题，提供问题排查指导，帮助您排查问题。

本文以 VS Code 为例进行介绍，您可以按照如下方法进行排查。

> **说明：**

> 本文适用于 Windows、MacOS 和 Linux 操作系统。

## 问题排查一：配置正确的 shell

### 步骤1：更新 VS Code，确保使用的是最新版本的 VS Code

1. 打开 VS Code。
2. 按 Cmd\+Shift\+P（Mac）或 Ctrl\+Shift\+P（Windows/Linux）。
3. 输入并选择 “检查更新” 或 “尝试更新” 。
4. 更新后重新启动 VS Code。

### 步骤2：在 VS Code 中配置使用正确的 shell

1. 打开 VS Code。
2. 按 Cmd\+Shift\+P（Mac）或 Ctrl\+Shift\+P（Windows/Linux）。
3. 输入并选择“终端：选择默认配置文件”。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/1e5f3ab918f511f0b04252540044a08e.png)
4. 选择其中一个支持的 shell，例如：zsh、bash、fish 或 PowerShell。

以 Windows 为例，建议选择 PowerShell 或 Git Bash。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/929effb518f511f09240525400bf7822.png)

> **说明：**

> 这里 PowerShell 的版本要求 v7及以上。您可以：
> 
> - 输入并运行`$PSVersionTable.PSVersion` 命令检查当前的 PowerShell 版本。
> - 如果您的版本低于 v7，请 [更新 powershell v7](https://learn.microsoft.com/en-us/powershell/scripting/whats-new/migrating-from-windows-powershell-51-to-powershell-7?view=powershell-7.4#installing-powershell-7)。

默认情况下，出于安全原因，PowerShell 会限制脚本执行。因此，您可能还需要调整 PowerShell 执行策略，使用执行策略来确定哪些脚本可以在您的系统上运行。以下是最常见的策略：

- `Restricted`：无法运行 PowerShell 脚本（默认设置）。
- `AllSigned`：所有脚本（包括本地脚本）都必须由受信任的发布者签名。
- `RemoteSigned`：本地创建的脚本可以运行，但必须对从 Internet 下载的脚本进行签名。
- `Unrestricted`：没有限制。任何脚本都可以运行，但在运行 Internet 下载的脚本之前，系统会警告您。

**更改执行策略的步骤**

4\.1 以管理员身份打开 PowerShell：按下 `Win+X` 并选择 “Windows PowerShell（管理员）” 或 “Windows 终端（管理员）”。

4\.2 通过执行如下命令检查当前执行策略。如果不为 `RemoteSigned`，则可以继续下一步进行更改。

plaintext
```
   Get-ExecutionPolicy
```
4\.3 通过执行如下命令，针对当前用户，更改执行策略。

plaintext
```
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```
### 步骤3：重启 VS Code

重启 VS Code 后，重新开启新的 Craft 会话，或继续上一个会话并尝试再次运行命令，看是否能解决问题。当选择 PowerShell 时，如果问题仍然存在，则可以切换选择 Git Bash 再次尝试。

## 问题排查二：手动安装 shell 集成

如果您在尝试了以上基本的问题排除步骤后仍然遇到问题，可以参考 [手动安装 shell 集成](https://code.visualstudio.com/docs/terminal/shell-integration#_manual-installation)。例如：

### 如果您使用的是 PowerShell

1. 在终端中运行如下命令以打开您的 PowerShell 配置文件。

bash
```
code $Profile
```
2. 在文件中添加如下内容。

bash
```
  if ($env:TERM_PROGRAM -eq "vscode") { . "$(code --locate-shell-integration-path pwsh)" }
```

### 如果您使用的是 zsh

1. 在终端中运行如下命令以打开您的 zsh 配置文件。

bash
```
code ~/.zshrc
```
2. 在文件中添加如下内容。

bash
```
  [[ "$TERM_PROGRAM" == "vscode" ]] && . "$(code --locate-shell-integration-path zsh)"
```

## 异常终端输出

如果您看到带有矩形、线条、转义序列或控制字符的异常输出，则可能与终端自定义工具有关，常见的包括：

- Powerlevel10k：一个 zsh 主题，用于向提示符添加视觉元素。
- Oh My Zsh：管理 zsh 配置的框架。
- Fish shell themes。

您可以按照如下步骤进行排查解决：
1. 在 shell 配置文件中暂时禁用这些工具。例如：如果您在 Zsh 中使用 Powerlevel10k，则可以通过打开配置文件（`~/.zshrc`）注释掉文件中的相关行来禁用 Powerlevel10k。bash
```
# Comment out the Powerlevel10k source line
# source /path/to/powerlevel10k/powerlevel10k.zsh-theme
```
2. 如果问题解决，请逐个重新启用工具，以排查具体导致问题的工具，然后查找 VSCode 的 shell 集成功能兼容的替代工具。