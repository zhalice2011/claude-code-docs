## MCP 的介绍

MCP (Model Context Protocol，模型上下文协议) ，旨在解决大模型语言（LLM）与外部数据源及工具之间无缝集成的需求。它通过标准化 AI 系统与数据源的交互方式，帮助模型获取更丰富的上下文信息，从而生成更准确、更相关的响应。其主要的功能如下：

- 上下文共享：应用程序可以通过 MCP 向模型提供所需的上下文信息（如文件内容、数据库记录等），增强模型的理解能力。
- 工具暴露：MCP 允许应用程序将功能（如文件读写、API 调用）暴露给模型，模型可以调用这些工具完成复杂任务。
- 可组合的工作流：开发者可以利用 MCP 集成多个服务和组件，构建灵活、可扩展的 AI 工作流。
- 安全性：通过本地服务器运行，MCP 避免将敏感数据上传至第三方平台，确保数据隐私。 腾讯云代码助手 Craft 开发智能体支持您进行本地 MCP Server 配置，扩展您的应用程序的功能。腾讯云代码助手提供两种 MCP Server 安装方式：
- 预置的 MCP Server 市场，支持您一键进行安装，详情请参见 [MCP 市场安装](#mcp-市场安装)。
- 通过配置文件进行本地 MCP Server 配置，详情请参见 [自定义配置 MCP Server](#自定义配置-mcp-server)。

> **说明：**

> **微信开发者工具**暂不支持 MCP Server，请持续关注支持时间。

## 安装 MCP Server

### MCP 市场安装

1. 单击对话面板右上方的 MCP 市场按钮。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/5a381b7f848711f0ae9d5254001c06ec.png)
2. 然后，即可以看到丰富的、预置的 MCP Server，支持您一键进行**安装**。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/d1017d9b848311f093f45254005ef0f7.png)
3. 选择需要安装的服务。例如选择 **Context7 MCP** 进行安装，单击**安装**后，会先对当前依赖环境进行检测，如果检测到没有依赖环境则会进行报错提醒。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/362274ae848411f0992e52540044a08e.png)
4. 如果没有安装依赖环境，您可以根据提示选择**尝试安装**。依赖环境安装完成后，可以重新一键安装 **MCP Server**，安装结果如下。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/15727663848511f0b321525400e889b2.png)

> **说明：**
> 
> 
> 	- 如果依赖环境安装失败，则可以选择**手动安装指引**按钮去手动安装。
> 	- 有些 MCP Server 在运行使用时需要提供 `PERSONAL_ACCESS_TOKEN` 或 `API Key`，因此您需要申请对应的`PERSONAL_ACCESS_TOKEN` 或 `API Key`。例如：

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/9764a455848511f0992e52540044a08e.png)
5. 接下来，您可以选择调用工具去验证 **MCP Server** 是否能正常工作。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/c643d2d6848511f093f45254005ef0f7.png) Context7 MCP 的验证如下，成功调用了 mcp\_resolve\-library\-id 和 mcp\_get\-library\-docs 这两个工具进行演示。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/701dfd1f848611f0992e52540044a08e.png)

### 自定义配置 MCP Server

与 Cursor、Claude Desktop、Cherry Studio 等这些 MCP Host（支持了 MCP 的应用程序）一样，腾讯云代码助手也提供了配置 MCP Server 的入口。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/fd11af3d192e11f0b5c65254001c06ec.png)

下面以 [Time MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/time) 为例，为您介绍如何进行本地 MCP Server 配置，连接 `Time MCP Server`。

#### 步骤1：安装依赖环境

在开始安装 Time MCP Server 之前，请确保您的开发环境满足具备安装 Time MCP Server 的包管理工具，常见的有 NPX、UVX 和 PIP。

- **NPX** NPX 是 Node.js 的一个命令行工具，用于直接运行 npm 包中的命令，无需全局安装或显式指定路径，安装 Node.js 就默认自带这个工具。如果您未安装，请进行安装 [Node.js](https://nodejs.org/zh-cn)。安装好后，可以用以下命令查看是否安装成功：

bash
```
node -v  # 查看 Node.js 版本
npm -v   # 查看 npm 版本
```
- **UV** uvx 是 uv 工具链的扩展命令，是一个用 Rust 编写的极快的 Python 包和项目管理器。具体的安装方式请参见 [uv 安装](https://github.com/astral-sh/uv)。
- **PIP** PIP 是 Python 的包管理工具，您可以访问 [Python 官网](https://www.python.org/downloads/windows/) 下载并安装最新版本 Python 3。安装完后可以使用如下命令查看是否安装成功。

bash
```
pip --version
```
下面以 PIP 的安装方式为例进行介绍。

> **说明：**

> 使用 PIP 进行安装时，需要确保 Python 版本为3\.10及以上版本。

#### 步骤2：安装 Time MCP Server 包

通过以下命令安装 `Time MCP Server` 包。

bash
```
pip install mcp-server-time
```
#### 步骤3：配置 Time MCP Server

1. 在对话面板右上方，单击 **MCP 市场**按钮。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/3d6b5fa2848811f081b5525400bf7822.png)
2. 如果没有已安装的 MCP Server，直接单击**配置 MCP Server** 进行配置。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/0fd81fa61a8611f08ac55254007c27c5.png) 如果有已安装的 MCP Server，单击下方**配置**按钮。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/fc2d84a3848811f0818a52540099c741.png)
3. 在 **settings.json** 配置文件中添加 `Time MCP Server` 服务器的配置。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/7dfeea2b848a11f093f45254005ef0f7.png) 配置格式如下：

json
```
{
"mcpServers": {
 "mcp-server-time": {
   "command": "python",
   "args": [
     "-m",
     "mcp_server_time",
     "--local-timezone",
     "Asia/Shanghai"
   ],
   "disabled": false
 }
}
}
```

> **说明：**

> "args" 字段是命令参数，除了需要 "`-m`" 和 "`mcp_server_time`" 参数之外，还需要添加 "Asia/Shanghai"。当不提供 `--local-timezone` 参数时，服务器会使用系统默认时区（这里的例子中是“中国标准时间”），这个名称不是标准的 IANA 时区标识符，因此对于中国标准时区，还需要添加 "Asia/Shanghai" 作为中国标准时区的时区标识符。
4. 配置文件填写完成并保存后，可在 MCP Server 配置列表查看是否配置生效。`mcp-server-time` 服务器的状态为绿色，表示生效，红色表示未生效，如下图。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/18cca9ad849111f093f45254005ef0f7.png)

## 使用 MCP Server

以上面章节中安装好的`mcp-server-time` 为例，`mcp-server-time` 服务器提供两个工具。

- get\_current\_time：获取特定时区或系统时区的当前时间。
- convert\_time：在时区之间转换时间。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/3f6983c1849111f093f45254005ef0f7.png) 因此，您可以通过服务器来调用这两个工具。
- 在 Craft 模式下，输入框输入问题进行提问，如下图： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/8fe6d5d9849211f097755254007c27c5.png) 可以看到，`mcp-server-time`服务器能够调用 get\_current\_time 工具来获取当前时区的时间。
- 或者 ，您也可以单击下方图中的按钮让 Craft 自动进行验证。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/725fca12849111f0b321525400e889b2.png) 从下图的验证结果中可以看到，`mcp-server-time` 服务器能够正常调用\*\* mcp\_get\_current\_time \*\*工具来获取当前时区的时间。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/b9b999d1849111f097755254007c27c5.png)