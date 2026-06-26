本文将为您介绍如何以自定义服务接入的方式来创建智能体。

## 定义智能体基础信息

通过 JSON 格式对智能体基础信息进行定义，包括以下信息：

- 智能体的基本信息。
- 智能体的**服务访问地址**。
- 智能体的模型配置。
- 智能体的命令列表。

> **说明：**

> 在创建自定义服务接入的智能体前需要定义智能体的域名，例如："endpoint": "<http://localhost:18080>"。

定义智能体基础信息的示例如下：

javascript
```
{
    "name": "happy",    // Agent 的名称，可使用[a-zA-Z-_中文]，客户端看到的 @happy
    "version": "1.0.0",    // 版本
    "type": "proxy",    // 类型，当前固定为 proxy
    "description": "happy",    // 描述信息
    "publisherType": "enterprise",    // 发布者类型，企业用户固定为 enterprise，个人 agent 为 user
    "publisher": "",    // 发布者名称
    "service": { 
      "endpoint": "http://localhost:18080"  // 服务地址
    },
    "modelConfiguration": { 
        "modelName": "hunyuan",    // 模型名称，当前仅作为配置使用，如 Agent 访问私有模型，则忽略此配置
    },
    "commands": [    // 命令列表
        {
            "name": "default",    // 指令名称。default 为必须的默认指令，当客户端不指定指令时，默认发送此指令
            "description": "happy",    // 指令描述
            "modelConfiguration": { "modelName": "hunyuan" },    // 指令模型配置
            "messageTemplates"?: [    // 指令消息模板列表，用于在服务内部处理生成 prompt 时，作为预置模板使用
                  {
                  role : "system",
                  template : '你是一个世界级程序员'
                }
            ],
            "contextVariableCollectionStrategy": { // 指令所需上下文变量
                "type": "specify",    // 收集策略，当前固定为 specify
                "contextVariables": [    // 上下文列表
                    {
                        "name": "userInfo",        // 上下文变量名称
                        "resolveOptions": {}    //上下文采集策略
                    },
                    {
                        "name": "vcs"
                    },
                    {
                        "name": "activeEditdor"
                    },
                    {
                        "name": "knowledgeBase"
                    }
                ]
            }
        },
        {
            "name": "version",
            "description": "获取版本信息",
            "contextVariableCollectionStrategy": {
                "type": "specify",
                "contextVariables": [
                    {
                        "name": "userInfo"
                    }
                ]
            }
        }
    ]
}
```
## 创建智能体

1\.登录 [企业后台管理](https://copilot.tencent.com/admin/overview) 端，选择**智能体**，然后单击**新建智能体**。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/96d70032692e11f09dc95254007c27c5.png)

2. 填写智能体信息，类型选择**自定义服务接入**。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/b3875d82692e11f094035254001c06ec.png)

填写智能体相关信息如下：
- **智能体名称**：智能体的名称。

注意：智能体的名称不能重复，包括不能与代码助手内自带的智能体名称重复，以及不能与企业内的智能体名称重名。

- **智能体描述**：智能体的描述，可展示在本地 IDE 中。
- **服务地址**：填入定义好的服务访问地址。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/8b912caa692f11f08eae52540044a08e.png)
- **上下文**：可选择**添加知识库**，功能启用后，调用指令即可关联知识库。
- **触发区**：默认仅在聊天区触发。
- **可见范围**：可以设定成员的使用权限，包括企业内**所有成员**和**部分成员**。当选择**部分成员**可见时，可直接单击**添加成员**按钮去进行添加，支持全选和根据 ID、姓名、账号进行输入搜索选择，如下图所示。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/17667616692f11f09dc95254007c27c5.png)

3\.填写信息完成后，单击**保存**，例如： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/db9f7d37692f11f088f3525400e889b2.png)

4\.智能体创建完成后，默认已经启用智能体。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/0a4d1f04693011f0a1c55254005ef0f7.png)

5\.启用智能体后，打开本地 IDE 即可查看。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/924a18c4693011f094035254001c06ec.png)

> **说明：**

> 建议重启一下 IDE。

## 后续步骤

接下来，您还需要配置智能体，比如需要配置上下文变量及交互动作等，配置完成后才算真正地完成，详情请参见 [配置智能体](./配置智能体)。