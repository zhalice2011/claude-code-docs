代码诊断是指通过检查和分析源代码，发现并定位其中的错误、缺陷或不规范之处。传统的代码诊断方法主要依赖于人工审查和简单的静态分析工具，结合流水线的自动化能力并且结合质量门禁建立不同的质量阈值关卡。

而基于 AI 的代码诊断是在传统的能力基础上再次进行质量左移，通过代码助手在 IDE 的嵌入，结合先进的人工智能技术，赋予代码诊断过程更高的智能化水平，从而提升诊断的准确性和效率。基于 AI 的代码诊断不仅仅是自动化代码分析，更是通过智能算法对代码进行深度理解和分析，识别出潜在的问题并提供相应的解决方案。本文将为您介绍基于 AI 代码诊断的应用实践。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/23817110136f11f09fca52540099c741.png)

## AI 在代码诊断的应用

腾讯云代码助手通过感知能力针对光标所在位置的上下文进行分析，能够自动提示当前位置代码的状态，通过触发代码修复功能自动提供当前代码问题对应的解决方案，同时提供修复的实例代码进行参考，确保整体的完整性和修改后功能的稳定性。

1. 代码诊断。 通过对话框中的 /fix 触发代码诊断，或者使用 IDE 编码区域中使用每个功能方法的快捷键**代码修复**来触发该方法的代码诊断。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/bd98ddc6148911f0aaa3525400e889b2.png)
2. 多轮对话优化代码诊断。 通过多轮对话，告诉 AI 更多的信息，让代码诊断的内容更符合研发人员的预期。例如，可以指定业务边界条件、特殊的异常处理逻辑、数据处理方式等。代码助手的对话模型会识别用户意图结合上下文对话内容优化代码诊断结果。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/e903264b148911f0854e525400454e06.png)
3. 一键应用代码诊断内容。 通过对话框结果中的快捷按钮，例如**应用**、**插入到 IDE** 等，开发者可以快速判断与接受生成的诊断建议代码。![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/d282d648137211f0a9cd5254007c27c5.png)
4. 可以选择**应用代码**，并且**接受**将对话诊断建议代码的结果，直接插入到对应的代码文件中。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/0db725d5137311f0854e525400454e06.png)
5. 可以在 IDE 编码区域看到**应用**这部分通过 diff 的能力进行高亮地区分诊断建议代码和当前文件代码的对比修改情况，让研发人员快速识别到改动并判断是否接受。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/8d7cea43137411f0854e525400454e06.png)

## 实际场景演示

### Debug 调试时诊断修复

在开发过程中，开发者常常会通过 DeBug 方式进行程序代码的调试，调试过程中会遇到各种突发的小错误。通过对 DeBug 断点的快速定位异常信息，能够实时监控代码编辑器，即时提示语法错误、异常错误等问题，通过代码修复能力帮助开发者迅速修正，避免问题积累。

1. 启动 Debug 时出现异常： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/3672c90d148b11f0a9cd5254007c27c5.png)
2. 通过 **CodeBuddy：优化代码**功能获取解决方案： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/cd3b1afc137911f09fca52540099c741.png)
3. 正在获取解决方案： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/29d59961137a11f0ae09525400bf7822.png)
4. 可以选择采纳对代码进行修复。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/94b6f6e6137a11f09b3252540044a08e.png)

### 程序运行错误时定位及修复

软件运行过程中常常也会出现异常问题，包含数组越界、空指针、类型不匹配等报错情况，通过代码诊断结合多轮对话获取解决方案，帮助开发者快速的定位并解决问题。

1. 运行错误报错： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100025099277/5ae1890ec1cf11efbaf8525400454e06.png)
2. 选中异常报错信息通过 **CodeBuddy：解释代码**功能进行问题分析： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/0cf12958137c11f0854e525400454e06.png)
3. 获取异常问题解释并结合多轮对话进一步分析问题： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/5d1695ae137d11f0854e525400454e06.png)
4. 获取最终解决方案，通过代码助手对话框的应用能力把修复代码插入到方法中： ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/08457c06137e11f0854e525400454e06.png)

## 总结

腾讯云代码助手的代码诊断能力可以很好地为开发者提供有效的修复建议，通过对异常问题的快速定位及修复，能够缩短研发周期，提升效率，提高软件代码质量。相信在未来，随着人工智能技术的快速发展，基于 AI 的代码诊断能力会愈发强大。