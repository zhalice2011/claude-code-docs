内联对话（Inline Chat）是在代码编辑区中嵌入输入框，并在输入框里直接输入需求或调用 / 指令后，直接生成代码并插入到当前光标下。这种效果极大地加强并拓展了编码过程中代码生成的能力。

## 开启内联对话

【VS Code】

1. 单击底部腾讯云代码助手的按钮，弹出顶部菜单条，选中**高级设置**进入。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/e84d95bf977d11f0b95552540044a08e.png)
2. 确认 **Enable Inline Chat** 已经开启。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/f276d719977d11f0af98525400454e06.png)

【JetBrains IDE】

1. 单击底部腾讯云代码助手的按钮，弹出菜单条，选择**高级设置**进入。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/03b5f92d977e11f0a7c6525400e889b2.png)
2. 确认**启用内联对话功能**已开启。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/0a7e04c1977e11f0b95552540044a08e.png)

【微信开发者工具 IDE】

1. 单击底部腾讯云代码助手的 icon 按钮，在弹出菜单中选择**高级设置**进入。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/17dcbe46977e11f0ad595254007c27c5.png)
2. 确认**启用内联对话功能**已开启。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/1e065eda977e11f0b95552540044a08e.png)

## 使用内联对话

可通过如下方式唤起内联对话功能。

【VS Code】

在编辑区的右上方，单击腾讯云代码助手的 icon 图标，可唤起内联对话功能。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/55e1db1161f711f0bac1525400454e06.png)

【JetBrains IDEs】

圈选代码区域后，在侧边弹出腾讯云代码助手的 icon 图标，单击可唤起内联对话功能。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/f6d22bf361f611f0b324525400e889b2.png)

【微信开发者工具 IDE】

在编辑区的右上方，单击腾讯云代码助手的 icon 图标，可唤起内联对话功能。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/4ef32117768111f084fc525400bf7822.png)

此外，也可以通过快捷键的方式快速唤起内联对话功能。首先确保插件快捷键没有冲突。我们唤起内联对话的快捷键如下：

| 系统 | 操作 | 描述 |
| --- | --- | --- |
| Windows | Alt \+ K | 在编辑区内唤起内联对话的输入框。 |
| Mac | Command \+ K | 在编辑区内唤起内联对话的输入框。 |

唤起内联对话之后，您可以输入自然语言描述的需求，或者通过指令`/`做快捷场景。**典型的应用场景**有：

- 快速生成或插入常用代码模板，例如函数、类、配置等。
- 对现有代码进行重构、重命名、逻辑优化。
- 实时代码诊断及修复提示，例如类型校验、安全检测等。
- 在开发新功能时，通过自然语言快速实现思路落地。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/f8cc2fa1621011f0ad0f5254005ef0f7.gif)

如上面视频所示，使用`/doc`生成注释后，开发者可以选择接受或者取消。具体的快捷键如下表所示：

| 系统 | 操作 | 描述 |
| --- | --- | --- |
| Windows | Alt \+ A | 接受（Accept）内联对话生成的代码 |
|  | Alt \+ Z | 取消内联对话生成 |
|  | Alt \+ X | 拒绝（Reject）内联对话生成的代码 |
| Mac | Opt \+ A | 接受（Accept）内联对话生成的代码 |
|  | Opt \+ Z | 取消内联对话生成 |
|  | Opt \+ X | 拒绝（Accept）内联对话生成的代码 |