# 配置集成

CodeBuddy 集成了 Supabase 和 Tencent CloudBase 后端服务，无需进行繁琐的配置，即可获得一个可运行的后端环境。

### 功能特性

- **开箱即用**：无需手动配置数据库、认证等后端服务
- **多平台支持**：支持 Supabase 和腾讯云 CloudBase 两大主流后端平台
- **一键连接**：通过简单的授权流程即可完成后端服务接入

### Supabase

Supabase 是一个开源的 Firebase 替代方案，主要提供以下后端服务：

| 服务类型 | 说明 |
| --- | --- |
| **数据库服务** | 托管的 SQL 数据库，无需担心数据库运维 |
| **身份验证服务** | 用于应用程序的用户登录和用户管理 |
| **边缘函数** | 用于 API 需求，支持与 Stripe 等第三方服务通信 |

#### 连接 Supabase

1. 在侧栏对话框中，按路径找到并点击 **Supabase** 进行连接

![](/docs/static/Pasted%20image%2020260112204400.qEKtjWNi.png)
2. 登录或注册 Supabase 账号

![](/docs/static/Pasted%20image%2020260112204630.4gkNjt-Z.png)
3. 完成 API 授权即可

![](/docs/static/Pasted%20image%2020260112204855.Baf7-GTl.png)

#### 在项目中使用 Supabase

1. 选择要连接的现有 Supabase 项目，或创建一个新项目
2. 单击 **Connect project** 进行连接
3. 连接成功
4. 在您的项目中，选择需要增加的服务即可

#### 断开 Supabase 连接

1. 在侧栏对话框中，单击 **Integration** 右侧的设置，进入 CodeBuddy 的配置页
2. 在设置页中，切换到 **Integrations** 标签

![切换标签](/docs/static/config-integration-disconnect-tcb-2.EjLxOSv4.png)
3. 点击所连接的 Supabase 项目右侧的 **DisableConnect** 即可

![断开连接](/docs/static/config-integration-disconnect-supabase-3.DMhOo6FO.png)

### Tencent CloudBase

Tencent CloudBase（简称 TCB）是腾讯云提供的云原生一体化开发平台，主要提供以下后端服务：

| 服务类型 | 说明 |
| --- | --- |
| **登录认证** | 完整的用户身份管理和访问控制解决方案 |
| **数据库** | 基于 Serverless 架构，开通即用的数据管理服务 |
| **云函数** | 无需管理服务器即可运行后端代码 |
| **云存储** | 支持图片、文档、音视频等非结构化数据存储 |

![alt text](/docs/static/cloudbase.DjnO-MXB.png)

### 常见问题

#### 连接失败怎么办？

请检查以下几点：

- 确保网络连接正常
- 确认账号已正确登录
- 检查是否已完成必要的授权步骤

#### 如何切换不同的后端服务？

在 **Integrations** 设置页中，可以断开当前连接的服务，然后重新连接其他服务。