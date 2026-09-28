# 任务执行与对话

## 一、入口

任务发送后，WorkBuddy 自动拆解并逐步执行。

![任务执行](https://download.codebuddy.cn/web/docs/0c6eecdbb4e15781e51229882560e9ea0b367fe3/docs/static/image28.C6FRYO4b.png)## 二、步骤拆解

任务被自动拆分为多个阶段，每个阶段以卡片形式展示：

- **「拆解为 N 个步骤」**：显示该阶段包含的子步骤数量
- **「已完成」**（绿色标签）：该步骤已执行完毕
- 点击卡片右侧 **\>** 可展开查看详细过程

![步骤拆解](https://download.codebuddy.cn/web/docs/0c6eecdbb4e15781e51229882560e9ea0b367fe3/docs/static/image29.C-OOCsMI.png)## 三、继续追问

任务完成后可在同一对话中继续追问，例如：

- "把表格按销售额排序"
- "再加一个饼图"
- "导出成 PDF"

**WorkBuddy 会保持上下文，无需重复描述背景。**

## 四、中断执行

任务进行中时，输入栏会显示停止按钮（■），点击可随时中断当前执行。中断后仍可继续补充说明或调整需求。

![中断执行](https://download.codebuddy.cn/web/docs/0c6eecdbb4e15781e51229882560e9ea0b367fe3/docs/static/image30.D8dCRWhI.png)## 五、查看引用来源

WorkBuddy 在回答中引用了外部资料时，会在回答末尾汇总一个**来源入口**，显示来源图标与数量（例如「3 个来源」）。

![回答末尾的来源入口](https://download.codebuddy.cn/web/docs/0c6eecdbb4e15781e51229882560e9ea0b367fe3/docs/static/task-source-entry.Cs612kHy.png)

1. 点击来源入口，从屏幕底部弹出**来源列表**；
2. 点右上角的 **×**，或点击列表外的遮罩区域即可关闭；
3. 点击列表中的某条来源，会自动**复制该来源的链接**，并提示「已复制链接，请前往浏览器打开」——粘贴到浏览器即可查看原文。

![从底部弹出的参考来源列表](https://download.codebuddy.cn/web/docs/0c6eecdbb4e15781e51229882560e9ea0b367fe3/docs/static/task-source-list.Ee2ZwsVD.png)

可查询到的来源包括：公开信息源（含 ima 公开知识库），以及你已授权的个人资料（文档知识库、ima 个人 / 共享知识库、乐享知识库等）。