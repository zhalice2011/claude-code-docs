腾讯云代码助手支持企业管理员在企业管理后台进行多模型的部署和管理，包括对话模型和补全模型。管理员可以根据不同的企业人员进行配置不同类型的模型，实现对模型的灵活管理和控制，助力企业效能提升。接下来为您介绍如何进行部署和管理。

## 模型部署

1. 登录 [企业管理后台](https://copilot.tencent.com/login/?platform=admin&state=0&redirect_uri=https%3A%2F%2Fcopilot.tencent.com%2Fadmin%2Foverview)。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/f7c1a313114211f08c275254001c06ec.png)
2. 在左侧导航栏**企业设置**中选择**模型设置**。列表中展示企业下的所有模型，包括腾讯云代码助手内置的官方模型和企业自添加的模型。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/1aa7a962114311f08c275254001c06ec.png)
3. 单击**新建模型**。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/36173270114311f08c275254001c06ec.png)
4. 填写模型信息。例如部署 hunyuan\-turbo 模型，填写信息示例如下：

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032786634/c6b123b7147f11f0854e525400454e06.png)

> **说明：**

> **API\_KEY **和**模型部署地址**需要去模型服务商获取，例如部署混元大模型可以去 [腾讯混元大模型官网平台](https://cloud.tencent.com/product/hunyuan) 进行采购。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/b710cc6dff2a11efaf3d52540099c741.png)
5. 填写信息完成后可以先进行**测试**模型配置是否通过。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032786634/dbde7199147f11f0a63e5254005ef0f7.png)
6. 测试通过后单击**创建**，自动返回模型列表。您可以看到自定义部署的模型，默认为关闭状态。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032786634/edf09d08147f11f0a63e5254005ef0f7.png)
7. 模型启用后，稍微静待一会，即可在 VS Code、JetBrains IDEs 等 IDE 插件端看到部署的模型。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/f6317e43ffaf11ef9f695254007c27c5.png)
8. 切换到自定义部署的模型，即可开始使用。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/bad3b53d146d11f0ae09525400bf7822.gif)

## 模型管理

1. 在 [企业管理后台](https://copilot.tencent.com/admin/overview)，可以对模型进行**启用**/**关闭**、**编辑**、**删除**的操作。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032786634/0146afa4148011f09b3252540044a08e.png)

> **说明：**

> 仅支持对自定义部署的模型进行**启用**/**关闭**、**编辑**、**删除**的操作，内置的模型不支持操作。
2. 在**编辑模型**中，可以对模型进行编辑，包括用户**可见范围、模型部署地址**等设置。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032786634/115b4843148011f0a9cd5254007c27c5.png)