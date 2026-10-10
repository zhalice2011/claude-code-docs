# 小程序开发与发布

WorkBuddy 可以根据需求生成微信原生小程序，按需接入云数据库、登录认证和文件存储等能力，并通过托管发布流程，协助完成代码上传、提交审核和版本发布。

## 概述

本功能适合希望将业务想法、活动、商品服务或内部工具做成微信小程序的个人、商家和团队。你不需要了解小程序工程结构，也不需要在本地搭建开发环境。小程序账号始终归你所有。

常见场景包括：

- 品牌展示：公司主页、产品手册、电子名片；
- 预约服务：到店预约、维修登记、摄影预约；
- 活动服务：活动报名、现场签到、问卷调查；
- 内部协作：器材借用、事项申报、进度登记；
- 轻量工具：报价器、计算器、抽奖转盘。

## 生成微信小程序

可以通过以下两种方式创建：

1. 在 WorkBuddy 首页进入「代码开发」，选择「小程序」，使用推荐场景开始创建；
2. 直接描述需求，建议在需求中明确写出「微信小程序」。

如果需要云服务，不必写具体的技术方案，直接说明数据长期保存、用户登录、图片上传或多人参与等实际需求即可。例如：

```
制作一个读书清单微信小程序。用户可以通过微信登录，添加正在阅读和已经读完的书籍，阅读记录需要保存到云端。
```
部分行业或功能需要满足微信规定的服务类目和资质要求，具体请查看[微信小程序平台运营规范](https://developers.weixin.qq.com/miniprogram/product/)。

## 预览和修改

生成完成后，对话中会出现「微信小程序」产物卡片。点击卡片，可以在右侧预览区查看效果，并继续通过对话修改页面、文案和功能。

说明

WorkBuddy 中的预览主要用于检查页面样式和基础交互，与微信内的实际运行效果可能存在差异。微信登录等能力，需要发布为试用版或体验版后，再通过微信进行真机测试。

## 开启云服务

当应用需要保存数据、用户登录或上传文件时，WorkBuddy 会在生成过程中提示是否开启对应云服务。确认开启后，WorkBuddy 会继续完成相关配置，无需你手动填写技术参数。具体的功能介绍和使用方式请参见[云服务](./Cloud-Services)。

| 对应能力 | 使用场景 |
| --- | --- |
| 云数据库 | 保存和管理用户提交的信息 |
| 登录认证 | 通过手机号、微信或邮箱登录，并区分不同用户的数据或权限 |
| 文件存储 | 上传并保存图片或附件 |
| 数据统计 | 查看小程序的访问和使用情况 |

## 发布微信小程序

小程序制作完成后，点击预览区右上角的「分享」按钮，进入发布流程。

![点击预览区右上角的分享按钮进入发布流程](https://download.codebuddy.cn/web/docs/1fd9c48bbf93dc8e5bc5a2622d78cebdfa6a21d4/docs/static/miniprogram-publish-share.CSd2_-yA.png)

发布时，WorkBuddy 会以微信第三方服务商身份接入你授权的小程序账号，协助完成代码上传、试用版生成、提交审核和版本发布。账号注册、认证、备案、审核及后续运营规则以微信官方要求为准。

绑定小程序账号后可以发布体验版或正式版，根据使用阶段，可以选择试用版、体验版或正式版：

| 版本 | 主要用途 | 需要已有账号 | 需要微信审核 | 主要限制 |
| --- | --- | --- | --- | --- |
| 试用版 | 快速验证效果 | 否 | 否 | 14 天有效，到期后自动注销 |
| 体验版 | 上线前调试和验收 | 是 | 否 | 仅有体验权限的用户可以访问 |
| 正式版 | 对外发布和长期运营 | 是 | 是 | 需完成备案并通过微信审核 |

注意

同一个 WorkBuddy 应用一旦创建试用版，暂不支持再绑定已有小程序账号，也不能将该试用版转为正式版。如需长期运营，建议从一开始就绑定自己的小程序账号。

### 发布试用版

试用版不需要提前注册微信小程序账号，适合快速验证效果。

![在发布面板中选择创建试用版小程序](https://download.codebuddy.cn/web/docs/1fd9c48bbf93dc8e5bc5a2622d78cebdfa6a21d4/docs/static/miniprogram-trial-create.-KpT-eyD.png)

1. 在发布面板中选择「创建试用版小程序」；
2. 使用微信扫码并关注 WorkBuddy 服务号；
3. 在服务号中点击「创建试用小程序」，按页面提示完成授权；

![微信扫码关注 WorkBuddy 服务号](https://download.codebuddy.cn/web/docs/1fd9c48bbf93dc8e5bc5a2622d78cebdfa6a21d4/docs/static/miniprogram-trial-follow.7hAMTUlx.png)![在服务号中创建试用小程序](https://download.codebuddy.cn/web/docs/1fd9c48bbf93dc8e5bc5a2622d78cebdfa6a21d4/docs/static/miniprogram-trial-create-mobile.3jNuUJBw.png)![按页面提示完成授权](https://download.codebuddy.cn/web/docs/1fd9c48bbf93dc8e5bc5a2622d78cebdfa6a21d4/docs/static/miniprogram-trial-auth.CsqGuD4Y.png)4. 收到授权成功通知后，返回 WorkBuddy，点击「发布」。发布成功后，可以点击小程序码图标查看并分享。

![返回 WorkBuddy 点击发布试用版](https://download.codebuddy.cn/web/docs/1fd9c48bbf93dc8e5bc5a2622d78cebdfa6a21d4/docs/static/miniprogram-trial-publish.BKn7UDIM.png)

![试用版发布成功后的小程序码入口](https://download.codebuddy.cn/web/docs/1fd9c48bbf93dc8e5bc5a2622d78cebdfa6a21d4/docs/static/miniprogram-trial-qrcode.Br3v_wlw.png)

试用版存在以下限制：

- 一个微信号最多可以创建 5 个试用版小程序；
- 有效期为 14 天，到期后会自动注销，原小程序码将无法继续访问；
- 最多支持 15 人体验。

### 绑定已有小程序

已有微信小程序账号时，可以绑定账号并发布体验版或正式版。如果还没有账号，可先前往[微信公众平台](https://mp.weixin.qq.com/)注册。完成一次账号绑定后，可以使用同一账号发布体验版或正式版，无需分别绑定。

![在发布面板中选择绑定已有小程序账号](https://download.codebuddy.cn/web/docs/1fd9c48bbf93dc8e5bc5a2622d78cebdfa6a21d4/docs/static/miniprogram-bind-entry.fIBl-F7d.png)

1. 在发布面板中选择「绑定已有小程序账号」；
2. 使用小程序管理员的微信扫描二维码，选择要发布的小程序账号，根据页面提示完成授权；

![使用小程序管理员微信扫描二维码](https://download.codebuddy.cn/web/docs/1fd9c48bbf93dc8e5bc5a2622d78cebdfa6a21d4/docs/static/miniprogram-bind-scan.D6l196It.png)![选择要发布的小程序账号](https://download.codebuddy.cn/web/docs/1fd9c48bbf93dc8e5bc5a2622d78cebdfa6a21d4/docs/static/miniprogram-bind-select.BZo0OBqo.png)![根据页面提示完成授权](https://download.codebuddy.cn/web/docs/1fd9c48bbf93dc8e5bc5a2622d78cebdfa6a21d4/docs/static/miniprogram-bind-auth.QQMRVAht.png)3. 返回 WorkBuddy，勾选需要发布的版本并点击「发布」，成功后即可获得小程序码。

![勾选需要发布的版本并点击发布](https://download.codebuddy.cn/web/docs/1fd9c48bbf93dc8e5bc5a2622d78cebdfa6a21d4/docs/static/miniprogram-bind-publish.O1E0XeHW.png)

![发布体验版后点击小程序码图标查看](https://download.codebuddy.cn/web/docs/1fd9c48bbf93dc8e5bc5a2622d78cebdfa6a21d4/docs/static/miniprogram-bind-success.BSZYa-Yx.png)

### 发布体验版

体验版用于上线前调试和验收，无需微信审核，最多支持 15 名体验成员。分享给其他人后，对方首次打开体验版时，需要申请体验权限。小程序管理员批准后，对方才可以访问。

管理员可以在[微信公众平台](https://mp.weixin.qq.com/)进入「管理 \> 成员设置 \> 体验成员」，管理体验权限。

![在微信公众平台管理体验成员](https://download.codebuddy.cn/web/docs/1fd9c48bbf93dc8e5bc5a2622d78cebdfa6a21d4/docs/static/miniprogram-exp-member.DGrSwT-t.png)

### 发布正式版

正式版用于对外发布，需要提交微信审核。

完成设置后，在发布面板中勾选「正式版」并点击「发布」。提交后可在发布面板中查看审核进度；审核通过并完成发布后，即可通过正式版小程序码访问和分享。

![在发布面板中勾选正式版并发布](https://download.codebuddy.cn/web/docs/1fd9c48bbf93dc8e5bc5a2622d78cebdfa6a21d4/docs/static/miniprogram-release-publish.m_iD0xdH.png)

发布前，请在发布面板中点击「小程序设置」，依次检查以下三项：

![点击发布面板中的小程序设置](https://download.codebuddy.cn/web/docs/1fd9c48bbf93dc8e5bc5a2622d78cebdfa6a21d4/docs/static/miniprogram-release-settings-entry.Ce_5jm6L.png)

![小程序设置中的备案、隐私保护指引与 UGC 声明](https://download.codebuddy.cn/web/docs/1fd9c48bbf93dc8e5bc5a2622d78cebdfa6a21d4/docs/static/miniprogram-release-settings.DP4FowCE.png)

| 设置项 | 处理说明 |
| --- | --- |
| 小程序备案 | 境内小程序应完成备案，以保证正式版可以正常访问。具体流程可参考微信官方的[备案操作指引](https://developers.weixin.qq.com/miniprogram/product/record_guidelines.html) |
| 用户隐私保护指引 | 小程序涉及处理用户个人信息时，需要按实际情况填写信息类型、收集目的、变动通知方式，以及用于联系开发者的手机号和邮箱。 |
| 用户生成内容场景（UGC）信息安全声明 | 提审类目包含社区、论坛、笔记、问答等用户生成内容场景时，需要按页面提示填写。 |

正式版审核期间不能再次提交新的正式版更新。在 WorkBuddy 中，每个微信小程序每周可以提交 3 次正式版审核，剩余次数以发布面板显示为准。

### 更新和下线

修改应用后，可以在发布面板中点击「更新」。更新正式版需要重新提交微信审核。新版本审核通过并完成发布前，用户会继续使用当前已上线的版本。

如需停止正式版对外提供服务，可以在发布面板中点击「下线」。下线后，正式版小程序将无法继续访问。

### 管理已创建的应用

![在设置的数据管理中查看已创建的应用](https://download.codebuddy.cn/web/docs/1fd9c48bbf93dc8e5bc5a2622d78cebdfa6a21d4/docs/static/miniprogram-manage-apps.DP6FTZrK.png)

若要统一查看已创建的全部应用，可进入「设置 \> 数据管理 \> 应用」。在这里可以：

- 查看各应用的发布状态；
- 管理各应用的云服务；
- 找到已发布的小程序码；
- 返回对应的任务继续修改。

## 常见问题

### 可以代注册微信小程序账号吗

不可以。WorkBuddy 可以协助创建试用版小程序，但不能代替你注册用于长期运营的微信小程序账号。如需发布体验版或正式版，请先在[微信公众平台](https://mp.weixin.qq.com/)注册小程序账号，再授权给 WorkBuddy。

### 预览就是最终小程序的效果吗

不完全是。WorkBuddy 预览用于快速检查页面样式和基础交互，不代表小程序在微信中的完整运行效果。登录认证、数据保存、图片上传以及微信内的实际表现，需要先发布试用版或体验版，再通过微信进行真机测试。正式发布前，建议至少完成一次真机测试。

### 为什么发布时提示授权异常

如果提示「授权异常，请尝试重新授权小程序」，请先在[微信公众平台](https://mp.weixin.qq.com/)进入「管理 \> 账号设置 \> 第三方设置 \> 第三方平台授权管理」，检查第三方平台授权状态，并尝试在微信侧重新授权。

![在微信公众平台检查第三方平台授权状态](https://download.codebuddy.cn/web/docs/1fd9c48bbf93dc8e5bc5a2622d78cebdfa6a21d4/docs/static/miniprogram-auth-exception.DONJCfzJ.png)

同一个小程序不能同时授权给多个第三方代开发平台。如果已经授权给其他平台，请先解除原平台授权，再返回 WorkBuddy 重新扫码授权。

### 为什么发布后扫码提示小程序已暂停

小程序提交发布并通过微信代码审核后，扫描小程序码提示「小程序已暂停」。可以在[微信公众平台](https://mp.weixin.qq.com/)进入「管理 \> 账号设置 \> 账号信息」，在「暂停服务」一栏点击「恢复服务」。恢复后，再次扫描小程序码确认是否可以正常访问。

![在微信公众平台恢复小程序服务](https://download.codebuddy.cn/web/docs/1fd9c48bbf93dc8e5bc5a2622d78cebdfa6a21d4/docs/static/miniprogram-resume-service.BuPHpgUF.png)

### 正式版审核未通过

发布面板会展示微信返回的完整审核原因，手机微信中的「服务通知」也会发送审核消息提醒。请根据审核原因修改应用或完善相关信息，修改后建议先发布体验版完成真机验证，确认功能和内容无误后，再重新提交正式版审核。

## 声明

本节说明，构成[服务协议](https://rule.tencent.com/rule/202603180001)和[隐私保护](https://privacy.qq.com/document/preview/771d9a58551449e9a7e7445ebfe04966)指引的组成部分，具有同等法律效力。 如有不一致之处，以前述协议原文为准。