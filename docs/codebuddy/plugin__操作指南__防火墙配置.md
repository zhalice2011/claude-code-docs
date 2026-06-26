在企业的网络环境中，可能会使用防火墙或代理服务器等安全策略。为了正常使用腾讯云代码助手，可将以下 URL 与出口 IP 添加到防火墙的白名单中。

| 适用版本 | URL | 用途 | 出口 IP | 端口 |
| --- | --- | --- | --- | --- |
| 个人版/旗舰版 | \- copilot.tencent.com\- copilot\-invite.tencent.com | 主服务 | 均为：111\.206\.99\.85;211\.100\.0\.108;111\.206\.149\.15;39\.156\.140\.64 | 均为：80/443 |
| \- api.copilot.tencent.com | OpenAPI 能力 |
| \- | 企业 SSO 登录 |
| \- open.weixin.qq.com\- long.weixin.qq.com\- res.weixin.qq.com\- localhost.weixin.qq.com | 微信登录 | 动态 IP，不支持全量获取 |
| \- acc\-1258344699\.cos.accelerate.myqcloud.com\- cs\-res\-1258344699\.file.myqcloud.com | 静态资源，若加载失败不影响主要功能 | 动态 IP，不支持全量获取 |
| 专享版 | \- | 主服务 | 专享版 IP 请 [联系我们](../联系我们) 获取 | |
| \- acc\-1258344699\.cos.accelerate.myqcloud.com\- cs\-res\-1258344699\.file.myqcloud.com | 静态资源，若加载失败不影响主要功能 |

## 「腾讯统一身份」相关域名

- 自 2025 年 12 月 16 日起，腾讯云代码助手 CodeBuddy 旗舰版将使用「腾讯统一身份」进行企业身份管理；
- 企业成员需使用「腾讯统一身份」完成登录认证，相关域名详见 [腾讯统一身份：防火墙配置](https://identity.tencent.com/docs/guides/SystemConfig/firewallConfig/)。