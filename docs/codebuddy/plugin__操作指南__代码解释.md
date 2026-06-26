代码解释主要用于给定一段代码，通过大模型输出容易理解的解释。

## VSCode

代码助手提供多种方式触发代码解释功能，您既可以在代码编辑区域中进行触发代码解释，也可以在代码助手对话输入框中使用 `/explain` 指令进行触发，方式如下：

### 文件或目录级触发

在代码助手对话输入框中，输入 `/explain` ，然后选择**文件**或**目录**进行触发。触发后，代码助手会根据所选内容生成详细的解释，例如代码逻辑和目的、关键组件与设计、关键变量与函数、编程模式与最佳实践等等，帮助您快速理解。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/10e104d1608a11f0bac1525400454e06.png)

### 方法或片段级触发

- **方式一**：圈选代码片段后，在左侧对话输入框输入`/explain` 指令进行触发代码解释。但这里有个点需要注意，输入`/explain` 指令后会自动调用 **@** 来添加上下文，这里已经选择了代码片段，不用添加其它上下文，可以直接按退格键（Backspace）删除 **@** 即可。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/7f0093c7608b11f092fe525400bf7822.png)

> **说明：**

> 如果不圈选代码块，则默认对整个代码编辑区中的代码进行解释。
- **方式二**：在方法或函数上方的操作条中，选择**解释代码**即可。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/3a97ffa1609011f0b30d5254007c27c5.png)
- **方式三**：圈选代码后，在编辑区域中直接右键选择 **腾讯云代码助手 CodeBuddy** \> **解释代码**，即可获得代码解释。或者根据右侧提示的快捷键进行快速触发。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/a0b8b1c4608c11f0a64452540099c741.png)
- **方式四**：在圈选代码块后会出现一个类似小灯泡的小图标，单击后出现一个功能对话框，选择 **CodeBuddy：解释代码**。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/be6dbeeb110011f08c275254001c06ec.png)
- **方式五**：在圈选代码块后，将鼠标光标悬浮在所选代码，会弹出一个工具条，选择**解释代码**即可。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/0f3a98f3608d11f092fe525400bf7822.png)

## JetBrains IDE

JetBrains IDE 的操作和 VSCode 的类似，如下：

### 文件或目录级触发

在代码助手对话输入框中，输入 `/explain` ，然后选择**文件**或**目录**进行触发。触发后，代码助手会根据所选内容生成详细的解释，例如代码逻辑和目的、关键组件与设计、关键变量与函数、编程模式与最佳实践等等，帮助您快速理解。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/dbaae7f6608e11f0ad0f5254005ef0f7.png)

### 方法或片段级触发

- **方式一**：圈选代码后，打开侧栏对话，在输入框输入 `/explain` 即可对编辑区选中的代码进行解释。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/76896f10608f11f0ad0f5254005ef0f7.png)

> **说明：** 如果不圈选代码块，则默认对整个代码编辑区中的代码进行解释。
- **方式二**：在每个方法或函数的上方操作条中，单击选择**解释代码。**![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/97fc2841609011f0b30d5254007c27c5.png)
- **方式三**：在圈选代码块后，右键选择 **CodeBuddy \> 解释代码**，即可获得代码解释。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/bf96617d609011f0bac1525400454e06.png)

## 微信开发者工具 IDE

### 文件或目录级触发

在代码助手对话输入框中，输入 `/explain` ，然后选择**文件**或**目录**进行触发。触发后，代码助手会根据所选内容生成详细的解释，例如整体架构、关键设计、关键变量与函数、编程模式与最佳实践、优化建议等等，帮助您快速理解。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/7559982c743611f0b9a25254007c27c5.png)

### 方法或片段级触发

- **方式一**：圈选代码片段后，在左侧对话输入框输入`/explain` 指令进行触发代码解释。但这里有个点需要注意，输入`/explain` 指令后会自动调用 **@** 来添加上下文，这里已经选择了代码片段，不用添加其它上下文，可以直接按退格键（Backspace）删除 **@** 即可。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/14f6e37a743411f09f3d52540099c741.png)

> **说明：**

> 如果不圈选代码块，则默认对整个代码编辑区中的代码进行解释。
- **方式二**：在方法或函数前的快捷方式中，选择 **Explain code** 即可。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/0415fd60743511f09f3d52540099c741.png)
- **方式三**：圈选代码后，在编辑区域中直接右键选择 **Tencent Cloud** **CodeBuddy** **\>** **Explain Code**，即可获得代码解释。或者根据右侧提示的快捷键进行快速触发。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/58bb8b2a743511f09f3d52540099c741.png)
- **方式四**：在圈选代码块后，将鼠标悬浮在所选代码，在弹出菜单中选择 **Explain code** 即可。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/aebd8764743511f09e39525400454e06.png)
- **方式五**：在圈选代码块后会出现一个类似小灯泡的小图标，单击后在弹出菜单中选择 **CodeBuddy：Explain code** 进行触发。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/e9ae4522743511f0b9a25254007c27c5.png)