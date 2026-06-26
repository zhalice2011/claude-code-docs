## 引言

制作企业微信的提醒机器人是工作中经常遇到的场景，借助代码助手，可以将制作成本大大降低，轻松完成接入。本文将以制作一个企微提醒机器人为例，为您演示如何借助代码助手为开发工作提效，制作好的企微提醒机器人效果如下：

- 文字消息：

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032954869/0760ae74719711efaa4b525400d5f8ef.png)
- Markdown 消息：

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032954869/ed7d1de5719811ef8829525400fdb830.png)

## 准备腾讯云代码助手

### 介绍

打开 [腾讯云代码助手介绍页](https://cloud.tencent.com/product/acc)，通过介绍可以知道腾讯云代码助手是基于混元代码大模型构建的，该模型具备深度理解和生成代码的能力。在混元代码大模型的支持下，腾讯云代码助手能够提供以下核心功能：

- 技术对话：能够理解和回答与编程、技术架构相关的问题，提供技术咨询和解决方案。
- 代码补全：根据已有代码上下文，智能补全代码片段，提高编程效率。
- 代码诊断：自动检测代码中的错误和潜在问题，提供修复建议，提升代码质量。
- 代码优化：分析代码并提出优化建议，帮助开发者提高代码性能和可读性。

通过这些功能，腾讯云代码助手旨在为开发者提供全方位的编程辅助，从代码编写到调试优化，全面提升开发效率和代码质量。它是基于混元代码大模型的智能编程助手，旨在让编程变得更加高效、智能和轻松。

### 下载和安装

1. 在编程工具里搜索或单击页面上**立即安装**，跳转到插件详情页进行安装，本次教程以 JetBrains 为例进行安装。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032954869/1420ac5d719711ef825d525400bdab9d.png)
2. 打开 JetBrains 软件，例如我使用的是 IntelliJ IDEA，在设置里找到插件，然后搜索腾讯云代码助手或 Tencent Cloud CodeBuddy 然后进行安装，安装完成后，需要重启。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/8c0f637d147f11f0a9cd5254007c27c5.png)

### 登录和使用

重启完 IntelliJ IDEA 后，就会进入腾讯云代码助手提示页，根据这个提示页面，进行登录。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/3ce43c9b11ec11f09fca52540099c741.png)

然后单击侧边栏，进入助手聊天界面。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/6d704a5a11ec11f0a9cd5254007c27c5.png)

输入您想让代码帮您完成的事项，例如“写一个 php 获取当前时间戳的代码”。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/a5ad63e611ec11f0a63e5254005ef0f7.png)

## 进入企业微信，创建机器人

### 创建机器人

进入企微群聊后，单击右上角三个点进入群操作页面，然后添加群机器人，根据提示创建机器人。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032954869/3ece8a0f719711ef8631525400a9236a.png)

单击**新创建一个机器人。**

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032954869/5d45e935719711ef82535254002693fd.png)

创建完成后，复制 Webhook 地址。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032954869/4c88c04c719711ef852f52540075b605.png)

### 复制机器人参数

复制好上面的链接后，将 `send?` 后面的参数截取下来，然后单独保存好，后面的代码对接就需要用到这个参数。

## 对话 AI 生成机器人运行代码

用一句话让腾讯云代码助手帮您生成代码。

1. 打开助手的聊天窗口，然后输入我们需要实现的功能，例如需要它帮我写一个 php 的企业微信群机器人文本消息代码，那么可以这样对它说。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/95cbe95311ee11f09fca52540099c741.png)
2. 腾讯云代码助手理解了我的需求，然后回复了上面的代码，我们将这段代码复制到一个 php 文件里，然后将刚才创建机器人时得到 webhook 地址后面的参数复制到助手生成代码上，也就是下面这一段。

php
```
$webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_WEBHOOK_KEY"; // 替换为您的 webhook 地址
```
3. 将 YOUR\_KEY 改成我们提取的参数，然后需要注意的地方是，复制时看一下有没有空格，如果有需要删除空格。

php
```
$webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=86c70996-fa50-406c-9227-72c21d9ef1c9"; // 替换为您的 webhook 地址
```
4. 然后进行运行代码（此步骤是已经安装了 php 运行环境，如果没有安装的可以前往百度搜索 php 环境安装，下载宝塔或 PHP study 工具）。

浏览器运行一下代码。

![浏览器运行一下代码](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032954869/d40e7ac5719711efa87e52540055f650.png)

运行发送成功。

![运行发送成功](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032954869/dd694c77719711ef8829525400fdb830.png)
5. 同样如果您需要发送 Markdown 消息的话，可以直接在助手的聊天窗口里给助手进行提问。应用代码时把 content 改成自己想要的内容即可。 ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/382d4258120011f0a9cd5254007c27c5.png)

发送 Markdown 消息效果如下：

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/472474b511fd11f0ae09525400bf7822.png)
6. 如果您还需要其他类型的消息，请参见 [企业微信群机器人](https://developer.work.weixin.qq.com/document/path/91770)，然后将文档内容复制给助手，让助手学习一下，告诉您其它几个类型的消息的 php 代码该怎么写。
7. 下面是以上的两种消息类型全部代码，需要哪个类型的消息，直接关闭注释即可，也就是代码前面的斜杠 //。

php
```

<?php
// 设置企业微信 webhook 地址
$webhookUrl = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY';

// 设置要发送的消息内容
//$message = [
//    'msgtype' => 'markdown',
//    'markdown' => [
//        'content' => '这是一条来自腾讯云代码助手的 **Markdown** 消息'
//    ]
//];
//
//
//$message = [
//    'msgtype' => 'text',
//    'text' => [
//        'content' => '这是一条来自腾讯云代码助手的消息'
//    ]
//];

// 使用 cURL 发送 POST 请求
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $webhookUrl);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($message));
$response = curl_exec($ch);

// 检查请求是否成功
if (curl_errno($ch)) {
    echo '请求失败: ' . curl_error($ch);
} else {
    $status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    if ($status_code == 200) {
        echo '请求成功';
    } else {
        echo '请求失败，状态码: ' . $status_code;
    }
}

// 关闭 cURL 会话
curl_close($ch);
?>
```

## 总结

写完这篇文章，其实大部分时间都是截图和文字介绍，编程代码占用了很少的一部分时间，而以前在编写代码时都需要用一半的时间去写代码，现如今，只需简洁地表达我们的需求，代码助手就能迅速生成高质量的代码，这一转变不仅节省了大量时间，更释放了我们的创造力，使我们能够专注于更高级别的设计和创新工作。腾讯云代码助手的智能代码生成和优化功能，显著提升了代码质量，使代码不仅功能完善，而且结构清晰、性能优越。

在个人技能层面，与腾讯云代码助手的互动成为了学习新技术和解决复杂问题的有效途径。它就像一位耐心的导师，通过实践引导我们深入理解编程概念，加速了技能的提升和专业知识的积累。无论是新手还是有经验的开发者，都能从中受益匪浅。

可以想象得到腾讯云代码助手预示着一个更加智能、高效和创新的编程时代。随着 AI 技术的不断进步，所以期待它未来在代码生成、优化、错误检测等方面发挥更大的作用，甚至在项目管理和团队协作中扮演更重要的角色。想象一下，未来的工作流程中，代码助手能够自动分析项目需求，生成初步代码框架，甚至自动进行代码审查和优化，这将极大提升开发效率，促进团队创新。