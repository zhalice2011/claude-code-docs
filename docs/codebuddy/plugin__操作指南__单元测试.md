腾讯云代码助手单元测试功能的定位是辅助用户全面、精细化地生成每个单元测试代码，并确保每个单元测试代码的正确性和高覆盖率，促使用户关注业务代码的正确性，以此提升整体代码库的质量。

## VS Code

### 触发单元测试生成

#### 方法级触发单元测试生成

- 在打开的文件编辑区中，单击函数上方快捷功能按钮生成单元测试。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/73698f44978711f0af98525400454e06.png)
- 圈选代码后，右键选择**腾讯云代码助手 CodeBuddy** \> **生成测试**。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/737a5942978711f0ad595254007c27c5.png)
- 在左侧对话面板中，圈选代码区域后通过 `/tests` 指令生成单元测试。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/73667083978711f0b5725254001c06ec.png)
- 选中代码后，将鼠标悬浮圈选代码后出现功能面板，选择生成测试。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/7f02edcd978711f0b5725254001c06ec.png)
- 圈选代码后，单击显示操作的小灯泡，选择 **CodeBuddy**：**生成测试**。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/7362e49d978711f0a7c6525400e889b2.png)

#### 文件/目录级触发单元测试生成

- 在对话输入框中，输入 `/tests` 指令，然后通过 `@ Add` 添加单个或多个文件或目录，最多可以选择15个文件。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/7f0f798c978711f09b0c525400bf7822.png)
- 在资源管理器的文件树中，可以右键选择 **CodeBuddy** \> **生成测试**。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/7f5d28a6978711f093df52540099c741.png)

### 生成单元测试代码

1. 触发单元测试生成后，代码助手会先进行分析项目结构、查找现有的测试文件、确认测试目录等一系列操作。可以点击**继续**，让代码助手继续生成单元测试代码。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/73856d01978711f09b0c525400bf7822.png)
2. 基于对所需测试代码内容的分析后，生成了完整的单元测试代码。此外，还提供了测试说明，以及注意事项等内容，辅助进行测试。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/7f4dcae5978711f0ad595254007c27c5.png)
3. 应用单元测试代码。 生成单元测试代码后，您可以根据实际情况来选择不同的应用代码方式，支持**插入到 IDE**、**复制**、**新建文件**以及**保存到本地**的方式。应用代码后，可以根据测试说明来运行测试进行验证。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/7f19881c978711f0ad595254007c27c5.png)

## JetBrains IDE

JetBrains IDE 的单元测试功能使用方法基本上与 VS Code 一致，可以根据方法级和文件或目录级选择多种触发方式触发单元测试生成。

### 触发单元测试生成

#### 方法级触发单元测试生成

- 圈选代码后，右键选择 **CodeBuddy** \> **生成测试** 直接触发单元测试生成。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/7f4490c2978711f0b95552540044a08e.png)
- 在右侧对话面板中，圈选代码区域后通过 `/tests` 指令生成单元测试。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/7f4ff99f978711f0b5725254001c06ec.png)

#### 文件/目录级触发单元测试生成

- 在对话面板中，可以通过 `/tests` 指令，然后选择单个或多个文件或目录即可，最多可以选择15个文件。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/7f383b8a978711f0ad595254007c27c5.png)

> **说明：**

> 这里文件列表中如果没有需要选择添加的文件或目录，可以使用退格键删除左侧的 @ 字符 ，然后手动单击 **@ Add** ，选择 **File \& Folders**，此时就可以通过搜索框进行输入搜索。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/7f2ebf0b978711f08ceb5254005ef0f7.png)
- 在左侧项目的文件树中，可以右键文件或目录，然后选择**腾讯云代码助手 CodeBuddy** \> **生成测试**，即可直接触发单元测试生成。这里也可以选择**添加到对话**，将文件或目录作为上下文，然后在输入框中通过 `/tests` 指令触发。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/7f2b86b9978711f0b5725254001c06ec.png)

### 生成单元测试代码

1. 触发单元测试生成后，代码助手会先对测试代码内容进行分析，并选择合适的测试框架生成单元测试代码。同时，也生成了测试说明、运行测试指令等内容，辅助进行测试。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/7f42088e978711f0af98525400454e06.png)
2. 应用单元测试代码。 生成单元测试代码后，您可以根据实际情况来选择不同的应用代码方式，支持**插入到 IDE**、**复制**、**新建文件**以及**保存到本地**的方式。应用代码后，可以根据测试说明来运行测试进行验证。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/7f147e01978711f09b0c525400bf7822.png)

## 微信开发者工具 IDE

您可以根据方法级或文件/目录级选择多种触发方式触发单元测试生成。

### 触发单元测试生成

#### 方法级触发单元测试

- 在打开的文件编辑区中，可以单击函数或方法前的快捷方式触发单元测试生成。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/7f2a610c978711f08ceb5254005ef0f7.png)
- 圈选代码后，可以右键选择 **Tencent Cloud CodeBuddy** \> **Generate Tests** 触发单元测试生成 。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/7f4d3b04978711f093df52540099c741.png)
- 圈选代码后，将鼠标悬浮在代码上，在弹出的悬浮菜单中可以选择 **Generate unit tests** 触发单元测试生成。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/7f0c8068978711f08ceb5254005ef0f7.png)
- 圈选代码后，在左侧对话框中，可以通过`/tests`指令触发单元测试生成。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/7f2b1238978711f0af98525400454e06.png)
- 圈选代码后，会弹出一个小灯泡，单击后在弹出菜单中可以选择 **CodeBuddy:Generate unit tests** 触发单元测试生成。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/7f4aaf6e978711f0b95552540044a08e.png)

#### 文件/目录级触发单元测试生成

- 在对话输入框中，您可以直接输入 `/tests` 指令，然后通过 `@ Add`添加单个或多个文件 / 目录，最多可以选择15个文件。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/7375447a978711f093df52540099c741.png)
- 在文件树中，可以右键单击文件 / 目录，然后选择 **Tencent Cloud CodeBuddy \> Generate Tests** 触发单元测试生成。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/736f3c6f978711f0ad595254007c27c5.png)

### 生成单元测试代码

1. 触发单元测试生成后，代码助手会先对测试代码内容和项目结构进行分析，并选择合适的测试框架生成单元测试代码。同时，也生成了测试覆盖范围、执行建议等内容，辅助进行测试。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/7f4b49db978711f08ceb5254005ef0f7.png)
2. 生成单元测试代码后，您可以根据实际情况来选择不同的应用代码方式，支持**插入**到 IDE、**复制**、**新建文件**以及**保存**到本地、**应用代码**的方式。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100024491917/7f54a120978711f093df52540099c741.png)