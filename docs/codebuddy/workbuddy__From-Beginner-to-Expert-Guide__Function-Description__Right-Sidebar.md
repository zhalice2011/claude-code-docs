# 右侧边栏

> 在同一面板中预览文件、查看产物与追踪变更。

## 概述

右侧边栏是 WorkBuddy 的核心工作面板，集文件预览编辑、产物管理、变更追踪和网页预览于一体。任务产生对话后，从右上角展开该面板，即可在同一界面完成阅读、编辑与核对。

右侧边栏包含以下功能区：

| 功能 | 说明 |
| --- | --- |
| **产物** | 查看当前对话中新生成的文件 |
| **工作空间文件** | 以树状结构浏览当前工作目录 |
| **变更** | 记录并对比 WorkBuddy 对文件的修改 |
| **浏览器** | 内置浏览器预览开发中的网页 |

![右侧边栏展开](https://download.codebuddy.cn/web/docs/58cb23ac03eddfd4f57622ab247bb99af32bf29e/docs/static/right-sidebar-1.B4zO-GkC.png)

![右侧边栏概览展开](https://download.codebuddy.cn/web/docs/58cb23ac03eddfd4f57622ab247bb99af32bf29e/docs/static/right-sidebar-2.C4qCVUNh.png)

## 产物

展示当前对话中新生成的文件（PPT、PDF、文档等），点击可查看任务列表及生成内容。

![产物标签页](https://download.codebuddy.cn/web/docs/58cb23ac03eddfd4f57622ab247bb99af32bf29e/docs/static/image-42.Coht1O8L.png)

右键选择**打开文件夹**，可在系统文件管理器（macOS Finder / Windows 文件资源管理器）中打开文件所在位置。

![在文件管理器中打开](https://download.codebuddy.cn/web/docs/58cb23ac03eddfd4f57622ab247bb99af32bf29e/docs/static/image-43.Bd-Q6UDE.png)

## 工作空间文件

以树状结构展示当前工作目录下的所有文件，便于直接浏览。

![工作空间文件](https://download.codebuddy.cn/web/docs/58cb23ac03eddfd4f57622ab247bb99af32bf29e/docs/static/image-44.B3YM_-Da.png)

在右侧栏打开**本地 Excel** 后，选中单元格区域并**右键**，菜单第一行提供**「AI 编辑」**：点击即可直接对选中区域发起 AI 修改，不必再翻到选区右下角找入口（原入口仍然保留）。

![本地 Excel 的右键菜单第一行「AI 编辑」](https://download.codebuddy.cn/web/docs/58cb23ac03eddfd4f57622ab247bb99af32bf29e/docs/static/right-sidebar-excel-ai-edit.Bl-lmRkH.png)

## 变更

记录 WorkBuddy 对文件的所有修改，展开可查看具体变更文件，通过差异对比快速确认改动。

![变更标签页](https://download.codebuddy.cn/web/docs/58cb23ac03eddfd4f57622ab247bb99af32bf29e/docs/static/image-45.FKMyYQIE.png)

## 浏览器

### 多标签浏览

在产物栏点击「\+」即可新建内置浏览器标签页、输入网址，支持同时打开多个标签页，网页间互不干扰。

也可以使用 `Cmd+T` / `Ctrl+T` 新建标签页（右侧边栏收起时会先展开），用鼠标中键点击标签页即可关闭。

![多标签浏览](https://download.codebuddy.cn/web/docs/58cb23ac03eddfd4f57622ab247bb99af32bf29e/docs/static/browser-multitab.sf_Mas5P.png)

### 网址栏访问与搜索

浏览器顶部的网址栏既能输入网址，也能直接输入关键词，按 `Enter` 后：

- 输入的是网址（如 `example.com`、`localhost:3000`）：直接访问；
- 输入的是其他内容：使用搜狗搜索，并打开搜索结果页。

![在网址栏输入关键词后，下方出现搜索入口](https://download.codebuddy.cn/web/docs/58cb23ac03eddfd4f57622ab247bb99af32bf29e/docs/static/browser-omnibox-search.qfQFlqXh.png)

输入过程中，网址栏下方首行是「搜索网页」，选择后即用搜狗搜索当前输入；使用一段时间后，下方还会列出匹配的**浏览历史**和**搜索历史**。可用鼠标点选，或用 `↑` `↓` 选择后按 `Enter`：选择浏览历史会直接打开该页面，选择搜索历史会用该关键词重新搜索。

### 登录态持久复用

访问需要登录的页面（企业内网、SaaS 后台、社交 / 电商网站等）并登录后，登录态会**持续保留**：切换会话、新建标签页都不会丢失，便于持续操作。

### 账号隔离与数据清除

- 登录态**按账号隔离**：同一台电脑切换不同 WorkBuddy 账号，不会串用彼此的网站登录态；
- 支持**主动清除**登录 Cookie 与缓存，清除后相关网站的登录状态将失效。

![清除浏览数据](https://download.codebuddy.cn/web/docs/58cb23ac03eddfd4f57622ab247bb99af32bf29e/docs/static/browser-clear-data.C69aA4u2.png)

### 页面查找、缩放与截图

点击浏览器右上角的**更多（⋯）**，菜单中提供以下页面工具：

![浏览器右上角「更多」菜单](https://download.codebuddy.cn/web/docs/58cb23ac03eddfd4f57622ab247bb99af32bf29e/docs/static/browser-more-menu.kuwScFtl.png)

| 菜单项 | 说明 |
| --- | --- |
| **查找页面内容** | 在当前网页中查找关键词，也可在浏览器页面内按 `Cmd+F` / `Ctrl+F` 打开 |
| **缩放** | 点击 **−** / **\+** 缩小或放大页面，点击重置按钮恢复原始大小 |
| **显示设备工具栏** | 打开设备调试工具栏，详见下方[设备调试工具栏](#设备调试工具栏) |
| **截取屏幕截图** | 截取当前页面可视区域，并复制到剪贴板 |

**查找**：输入关键词后，可通过上一个 / 下一个按钮在匹配项之间跳转，按 `Esc` 关闭查找条。

提示

对话区顶部的 `Cmd+F` / `Ctrl+F` 搜索的是对话内容；焦点在浏览器页面里时，同样的快捷键查找的是当前网页。

**缩放**：也可使用 `Cmd` / `Ctrl` 加 `+`、`-`、`0` 放大、缩小和重置。使用触控板时，还可以双指捏合放大查看页面局部细节。

**截图**：截图完成后会提示「截图已复制到剪贴板」，可直接粘贴使用。

本地 HTML 产物的「更多」菜单提供同样的工具，详见[查看 HTML 产物](./Library/Content-Management)。

### 设备调试工具栏

点击浏览器右上角的**更多（⋯）→ 显示设备工具栏**，即可在浏览器顶部打开设备工具栏，一键切换**手机 / 平板 / 桌面**视口，或自定义宽高，方便验证页面在不同设备下的响应式表现。

![设备调试工具栏](https://download.codebuddy.cn/web/docs/58cb23ac03eddfd4f57622ab247bb99af32bf29e/docs/static/browser-device-toolbar.CW3QxART.png)

## 消息中心

点击左侧边栏底部的**铃铛**图标，唤起**消息中心**：消息中心以整页形式平铺展示（替代旧版弹框样式），可呈现更多消息内容。点击右上角 **×** 或再次点击铃铛即可退出；没有消息时显示「暂无消息」。

**消息类型与交互**：

| 消息 | 说明 | 点击行为 |
| --- | --- | --- |
| **任务操作待您确认** | 任务有操作需要你的确认，请点击查看 | 点击直接跳转到对应任务 |
| **任务已成功完成** | 任务执行完成，请点击查看结果 | 点击直接跳转到对应任务 |

![消息中心](https://download.codebuddy.cn/web/docs/58cb23ac03eddfd4f57622ab247bb99af32bf29e/docs/static/right-sidebar-notification.B0am2Q5Q.png)

## 声明

本节说明，构成[服务协议](https://rule.tencent.com/rule/202603180001)和[隐私保护](https://privacy.qq.com/document/preview/771d9a58551449e9a7e7445ebfe04966)指引的组成部分，具有同等法律效力。如有不一致之处，以前述协议原文为准。