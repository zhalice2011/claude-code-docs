# 云服务

云服务让[网页应用](./Web-App)和[微信小程序](./Mini-Program)不只展示内容，还能保存和管理用户提交的信息。

开启后，报名、预约、订单等数据，以及用户上传的图片和文档，都会保存在云端，关闭页面或更换设备后仍会保留。应用还可以按需支持用户登录，并查看用户数量和注册趋势。

例如，制作活动报名应用时，参与者可以填写信息并上传资料，主办方可以集中查看报名名单和进度。这些后台能力可以按需开启，无需自行搭建数据库、部署服务器或维护运行环境。

![云服务概览](https://download.codebuddy.cn/web/docs/3754a028cd26c05d858852b7fbcedeb54159906e/docs/static/cloud-overview.BKsT43NE.png)

不确定是否需要云服务，或者不知道如何设置时，都可以直接问 WorkBuddy。需要查询数据、调整设置或排查问题，也可以直接提出需求，WorkBuddy 会帮助查看、分析或处理，并在需要你确认或手动完成时说明下一步。

## 云服务能力

### 数据库

数据库用于保存报名、预约、订单和打卡等业务记录。需要核对、补录或导出时，可以在「数据」页找到对应的数据表；「函数」和「权限」页则用于了解应用如何处理数据，以及不同用户可以访问哪些内容。

![数据库数据页](https://download.codebuddy.cn/web/docs/3754a028cd26c05d858852b7fbcedeb54159906e/docs/static/cloud-database-data.BWgScMsK.png)

![数据库函数页](https://download.codebuddy.cn/web/docs/3754a028cd26c05d858852b7fbcedeb54159906e/docs/static/cloud-database-function.DQI7mEeI.png)

![数据库权限页](https://download.codebuddy.cn/web/docs/3754a028cd26c05d858852b7fbcedeb54159906e/docs/static/cloud-database-permission.yK0NJSne.png)

### 身份认证

身份认证用于管理应用的登录方式。网页应用和微信小程序都支持邮箱、手机验证码和微信登录；进入身份认证页面后，可以查看各登录方式的开启状态。

开启云服务不会自动为应用添加登录功能。需要用户登录时，直接告诉 WorkBuddy 使用场景和登录方式，让它帮你添加。

![身份认证页面查看登录方式开启状态](https://download.codebuddy.cn/web/docs/3754a028cd26c05d858852b7fbcedeb54159906e/docs/static/cloud-auth-status.DyZOSqxR.png)

![配置登录方式](https://download.codebuddy.cn/web/docs/3754a028cd26c05d858852b7fbcedeb54159906e/docs/static/cloud-auth-config.CmVabOhP.png)

### 文件存储

文件存储让应用能够保存用户上传的图片和文档，适合作品征集、资料提交和报修等场景。

在管理页中，你也可以新建文件夹，或上传单个不超过 20 MB 的文件，用于预置共享资料和分类整理内容。

![文件存储管理页](https://download.codebuddy.cn/web/docs/3754a028cd26c05d858852b7fbcedeb54159906e/docs/static/cloud-storage.SK84rwDx.png)

### 数据统计

用于了解应用的用户增长情况。你可以查看总用户数、今日新增、本周新增，以及近 7 天、近 30 天或近 90 天的注册趋势；下方还会显示用户名称和邮箱。

![数据统计页面](https://download.codebuddy.cn/web/docs/3754a028cd26c05d858852b7fbcedeb54159906e/docs/static/cloud-stats.h2HXcXa7.png)

## 开启云服务

你可以通过以下两种方式开启云服务：

1. **通过自然语言提出需求**：在创建或修改应用时，说明需要保存什么、谁需要登录，以及是否需要上传文件。WorkBuddy 判断应用需要云服务时，会询问你是否开启，确认后继续处理。例如：

```
制作一个宠物健康档案应用。家庭成员登录后可以共同记录并上传检查单，
所有内容保存到云端。
```
2. **在应用页面开启**：打开应用卡片，点击应用标题旁的「云服务」，直接点击开启。

![点击应用标题旁的云服务](https://download.codebuddy.cn/web/docs/3754a028cd26c05d858852b7fbcedeb54159906e/docs/static/cloud-enable-entry.CBNK8SxW.png)

![云服务开启面板](https://download.codebuddy.cn/web/docs/3754a028cd26c05d858852b7fbcedeb54159906e/docs/static/cloud-enable-panel.u0JsvsTZ.png)

## 通过 WorkBuddy 使用云服务

你不需要使用数据库或权限规则等技术术语，直接说明想实现的业务结果即可。

### 创建或调整功能

说明用户要完成什么、哪些内容需要保存，以及保存后由谁使用。例如：

```
用户可以提交活动报名，报名记录保存到云端，管理员可以查看完整名单。
```
### 设置登录和权限

如果数据属于不同用户，说明使用哪种登录方式，以及每种角色可以查看和操作什么。例如：

```
给应用增加手机验证码登录。普通用户只能查看自己的记录，管理员可以查看全部记录并进行审核。
```
### 查看数据和排查问题

需要了解应用的数据、文件或使用情况，或者遇到错误时，可以把问题告诉 WorkBuddy，请它帮助查看和分析。例如：

```
这个应用最近一周新增了多少用户？
帮我看看最近的报名为什么提交失败，并告诉我可以怎么处理。
```
## 管理云服务

需要直接核对数据、用户、文件或服务状态时，可以通过以下两种方式进入云服务管理页：

- 在对话中打开应用预览，点击应用标题旁的「云服务」；
- 进入「设置 \> 数据管理 \> 应用」，点击已开启应用的云服务图标。

![应用预览标题旁的云服务入口](https://download.codebuddy.cn/web/docs/3754a028cd26c05d858852b7fbcedeb54159906e/docs/static/webapp-cloud-entry.BYkfGfvj.png)

![数据管理的应用列表中点击云服务图标](https://download.codebuddy.cn/web/docs/3754a028cd26c05d858852b7fbcedeb54159906e/docs/static/cloud-manage-list.CgeYY4Ib.png)

预览版和已发布版本使用同一个云服务，因此预览时提交的测试内容也会进入正式数据。发布前请检查并清理不需要的测试数据。

取消发布不会删除云服务数据。删除应用时，关联的数据、文件和注册用户会一并删除且无法恢复；如果只是暂时不希望别人访问，请选择取消发布。

云服务的可用资源额度由当前套餐决定。达到限制或会员状态发生变化时，云服务页面会显示具体影响和处理方式，请根据页面提示处理。具体额度以[套餐页](./../../../Pricing)为准。