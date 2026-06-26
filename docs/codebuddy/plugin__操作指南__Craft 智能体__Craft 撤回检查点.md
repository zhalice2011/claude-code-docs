当使用 Craft 编码智能体时，每次对话发生文件变更后，Craft 会对这轮对话的文件变更自动创建一轮检查点，并自动做一轮版本化管理。现在，撤回检查点的入口已经固定展示，您可以根据需要进行操作。下面以一个操作示例，为您进行介绍。

## 撤回文件变更

1. 以 EsProductServicelmpl.java 发生的文件变更为例，当模型修改完代码并停止后，会在这轮对话上自动创建一轮检查点，固定显示**回退改动**入口按钮。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/ebf2af4f818111f0b3fe525400bf7822.png)
2. 单击**回退改动**，Craft 会向您请求是否继续回退版本。单击**继续**就会撤回到 “**请优化当前代码的可读性和可维护性**”这个检查点之前的状态，这个检查点对应所进行的任务都会被撤销。若点击**取消**则会取消当前的操作。也可以选择勾选右侧的**不再提示**，此后回退改动的请求确认弹窗都不会再弹出，因此需要**谨慎**操作。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/fc636fa5818211f0854e5254001c06ec.png)
3. 选择**继续**后，回退版本后的效果如下图所示。此时您可以基于当前撤回后的版本，输入需求描述继续完成任务。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/d3af8208818311f0a8ae5254005ef0f7.png)

## 恢复到撤回前的内容

为了防止您误触后还期望还原，只要没有发送新的对话，Craft 都支持 undo 回退的操作。版本回退后，如果希望恢复回退版本，单击**恢复**即可。恢复入口有两个，功能点是相同的。

### 恢复入口

- 撤回后在输入框下的恢复入口。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/30311715818411f0840d525400454e06.png)
- 在对话底部的恢复入口。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/5c5afc88818411f0840d525400454e06.png)

### 恢复回退版本

单击**恢复**后，便会恢复到撤回前的对话版本，效果如下所示：

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/9b214ea8818411f0ac3c525400e889b2.png)

此时，恢复回退版本后，默认包含之前对话的上下文内容，您就可以基于当前对话版本继续进行技术对话，如下图所示：

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/df3fb48c818411f0ac3c525400e889b2.png)