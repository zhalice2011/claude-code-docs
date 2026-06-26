在云端开发平台 Cloud Studio 之上，通过代码助手的加持，可以快速搭建并开发一个过年都用得到的在线相册的小应用。 请单击 [体验地址](https://club.cloudstudio.net/a/16254042041167872) 前往。

## 应用架构

为了更快的进行开发，前端方面选择了 TDesign Mobile\+Vue3，实现注册、登录、上传图片、看图片，并且支持移动端浏览器访问。

后端采用了 Node.js\+ 数据库。数据库用于记录 ID 等 COS 文件信息。图片的 raw data 通过 COSClient SDK 存入 COS 桶中。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/4f955b53147e11f09b3252540044a08e.png)

### 启动一个开发环境

1. 打开 [腾讯云 Cloud Studio](https://cloud.tencent.com/product/cloudstudio)，单击左下角**新建工作空间**。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100025099277/0433b287ea4c11ee91ba525400aa857d.png)
2. 选择一个 Node.js 开发环境，单击**新建**之后，即可进入开发环境。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032954869/b5daf0d3df7911ee9f745254008eb8a8.png)
3. 在界面导航栏中选择**终端** \> **新建终端**，查看安装版本。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100025099277/1a6e5ca1ea4c11eebbb2525400564496.png)

### 后端应用

1. 选择拓展图标 \> ![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100025099277/2eff8c32ea4c11ee91ba525400aa857d.png) \> **从 VSIX 安装**，即可安装本地代码助手的插件安装包。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100025099277/468c0debea4c11eeb0c55254001a1c03.png)
2. 接下来开始创建 Node.js 后端服务。基于代码助手的对话能力，输入提示词**初始化一个 Node.js 项目的后端工程。**![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/22c6f2cf150c11f0aaa3525400e889b2.png)

后端服务至少应包含：
- 登录服务。
- 注册服务。
- 图片预览服务。
- 图片上传保存服务。

### 登录服务

在对话里继续提问：**基于 koa 框架，创建一个登录接口的服务，期望在通过用户名 username 和 password 来确定用户身份，通过 JsonDB 来快速保存相关记录**。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/375ea358150d11f09fca52540099c741.png)

接着插入到当前工程，进行代码补全的**代码微调**，例如我们要对传过来的密码进行 md5加解密，我通过行内注释输入 **// 对 password 进行 md5，如果登录成功，返回 token，否则返回失败**，接着代码助手触发了代码补全，智能根据当前光标上下文，进行行或者块补全。如下：

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032954869/eff36ce2df7911eea462525400bb593a.png)

#### 注册服务

AI 的联想能力（FIM \- Fill in Middle），由于上文已完成注册用户的代码逻辑，当描述注册接口的时候，可以给予初步的补全建议。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032954869/f7134648df7911eeb419525400ea3514.png)

此处对代码逻辑进行调整。例如针对109行做一些代码调整，增加兜底逻辑。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032954869/feb17099df7911eea462525400bb593a.png)

#### COS 桶

上传的图片需要存放到 COS 桶，接下来向代码助手提问：**用腾讯云的 COS 桶 qcloud\-cos\-sts，存储图片。通过获取临时密钥，实现图片上传和分片**。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/3496f55a150e11f0a63e5254005ef0f7.png)

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/da91233c150e11f0ae09525400bf7822.png)

#### 图片预览服务

输入：生成相册的 POST 请求 /photo\-wall，随机生成 ID，并保存到数据库中，图片文件上传到刚刚的 COS 桶里。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/3521b774150f11f09b3252540044a08e.png)

找到核心代码逻辑，复制到编辑器中，触发补全进行**代码微调。**

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/24e7f616151011f09fca52540099c741.png)

#### 图片相册列表服务

输入代码注释：查询相册 GET 请求/photo\-wall，根据上文的 POST 请求，猜出 GET 请求的编码。在此基础上，进行代码补全的微调就快速完成了相似的列表服务。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100032954869/2e03eb49df7a11eeb419525400ea3514.png)

### 前端应用

前端应用采用 [Koa2\+TDesign\_Mobile 组件库](https://github.com/Tencent/tdesign-mobile-vue)。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/f82c67b6151011f0a9cd5254007c27c5.png)

#### Vue 页面

创建对应几个 Vue 文件，如图，通过对话**实现一个 Login.vue 页面**先去生成个大概。然后通过插入代码之后，再进行代码补全微调，从而生成自己想要的代码逻辑。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/c94c9627151111f09fca52540099c741.png)

操作方式类似，由于篇幅有限，这里不一一截取。通过组合拳，对话\+补全，加上多文件能力，使得前后端的开发工作效率得到提升加速。

### 最后的预览效果

在 Cloud IDE 里遇到了问题，例如转发问题和 AllowHost 问题，可以通过代码助手对话解决。

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100039847436/c3a70a16151211f0854e525400454e06.png)

也通过了 Cloud Studio 的协作能力排查错误：

![](https://write-document-release-1258344699.cos.ap-guangzhou.tencentcos.cn/100025099277/e7f77909e4d011ee9ca3525400bb593a.png)

最后成功，效果演示视频如下：