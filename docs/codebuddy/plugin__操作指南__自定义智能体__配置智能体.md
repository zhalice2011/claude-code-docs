## 前提条件

> **说明：**

> 配置智能体前，您需要先创建智能体并为其部署服务访问地址，具体操作请参见 [自定义服务接入智能体](./自定义服务接入智能体)。

- 已创建智能体。
- 已为智能体部署服务访问地址。

## 智能体定义字典

### 上下文变量 ContextVariable

定义结构：

javascript
```
/**
 * 上下文变量对象
 * 每一种上下文对象对应一种具体数据结构
 */
interface ContextVariable{
      // 上下文类型，全局唯一，决定 value 的数据结构
      name: string
      // 上下文解析器参数，Agent 发布时定义，Client 可根据此策略调整上下文收集细节，如文本截取长度等
      resolverOptions: any;
}
```
- 用户自定义 prompt：

	- name：`userInputPrompt`
	- 描述：用户对话时手动输入的原始内容。
	- 解析参数：无
	- 采集结果：
	
	javascript
	```
	interface UserInputPromptContextVariable{
	      name: "userInputPrompt";
	      value: string;
	}
	```
- 用户信息：

	- name：`userInfo`
	- 描述：当前用户相关信息。
	- 解析参数：无
	- 采集结果：
	
	javascript
	```
	interface UserInfoContextVariable{
	      name: "userInfo";
	      value: {
	          id: string;            // 用户 ID
	         name: string;         // 用户英文名
	          nickname: string;     // 用户昵称
	    }
	}
	```
- 工作空间版本控制信息：

	- name：`vcs`
	- 描述：当前工作空间对应的版本控制信息。
	- 解析参数：无
	- 采集结果：
	
	javascript
	```
	interface VCSContextVariable{
	      name: "vcs";
	      value: {
	          type: string;                // vcs 类型，如 git
	        branchName: string;         // 分支名
	        upstreamBranchName: string;    // 远端分支名
	        remoteUrl: string;            // 远端仓库地址
	        remotes: string[];            // 远端仓库列表
	    }
	}
	```
- 知识库：

	- name：`knowledgeBase`
	- 描述：知识库列表。
	- 解析参数：
	
	javascript
	```
	  interface KnowledgeBaseResolverOptions{
	      knowledgeBaseIds?: string[]; // 目标知识库 id 列表
	      recallByAgent?: boolean;              // 是否由 Agent 执行召回，为 false 时，由客户端执行召回动作，此时上报的上下文中应包含 references 属性内容
	}
	```
	- 采集结果：
	
	javascript
	```
	interface KnowledgeBaseContextVariable{
	      name: "knowledgeBase";
	      value: {
	        knowledgeBaseId: string; // 知识库 id
	          references?: {
	          score: number; // 检索得分
	          chunk: string; // 句向量对应的文本块
	          metadata: {
	            fileName: string; //  文件名称，例如：/指南/开发指南.md
	            sourceType: 'doc' | 'code'; // 文件类型 doc or code
	            source: string; // 文件来源，例如：/home/xxx/xxx.py 或者 github.com/xxx/xxx/xxx/xxx.py
	            startPos?: number; // chunk 开始行号(可为空)
	            endPos?: number; // chunk 结束行号（可为空）
	          };
	        }[]
	    }[];
	}
	```
- 激活的编辑器内容：

	- name：`activeEditor`
	- 描述：激活的编辑器内容。
	- 解析参数：
	
	javascript
	```
	 interface ActiveEditorResolverOptions{
	      contentBeforeSelectionLines?: number; // 选区前文本行数，为空时不获取，为0时仅获取当前行选区前的内容
	      contentAfterSelectionLines?: number; // 选区后文本行数，为空时不获取，为0时仅获取当前行选区后的内容
	}
	```
	- 采集结果：
	
	javascript
	```
	interface ActiveEditorContextVariable{
	      name: "activeEditor";
	      value: {
	        filePath: string;                     // 文件路径
	        language: string;                     // 内容语言：java/javascript/...
	          content: string;                    // 文件内容
	          cursorOffset: number;                // 光标位置，从0开始
	          startLine: number;                    // 起始行，从1开始
	          startColumn: number;                // 起始列，从1开始
	          endLine: number;                    // 结束行，从1开始
	          endColumn: number;                    // 结束列，从1开始
	          selectedRanges: {
	            content: string;                    // 选中文件内容
	            startLine: number;                    // 起始行，从1开始
	            startColumn: number;                // 起始列，从1开始
	            endLine: number;                    // 结束行，从1开始
	            endColumn: number;                    // 结束列，从1开始
	            contentBeforeSelection?: string;    // 选区前文本
	            contentAfterSelection?: string;        // 选区后文本
	        }[];
	          visibleRange: {
	            content: string;                    // 可视区文件内容
	            startLine: number;                    // 起始行，从1开始
	            startColumn: number;                // 起始列，从1开始
	            endLine: number;                    // 结束行，从1开始
	            endColumn: number;                    // 结束列，从1开始
	        }
	    };
	}
	```
- 全局提示词：

	- name：`globalPrompts`
	- 描述：全局提示词，作为限定规则置于用户问题之前。
	- 解析参数：无
	- 采集结果：
	
	javascript
	```
	  interface GlobalPromptsContextVariable{
	      name: "globalPrompts";
	      value: {
	          role: string; // 角色
	        content: string; // 全局提示词内容
	    }[];
	}
	```
- 包管理文件：

	- name：`packageFiles`
	- 描述：项目包管理文件列表。
	- 解析参数：
	
	javascript
	```
	  interface PackageFilesResolverOptions{
	      maximumNumber: number;         // 最大文件个数
	}
	```
	- 采集结果：
	
	javascript
	```
	interface PackageFilesContextVariable{
	      name: "packageFiles";
	      value: [{
	      filepath: string; // 文件本地路径
	      content: string;     // 文件内容
	    }];
	}
	```

### 交互动作 Action

支持**确认按钮**和**树状结构**两种交互动作的智能体下发。

【确认按钮】

javascript
```
interface ConfirmAction{
    action: "confirm";
      state: any;
      data: {
      title: string; // 按钮文本
      message: string; // 描述信息
      command?: string; // 可选，有值时以此 command 发起标准 Agent 对话请求，不再发送 Action 反馈请求
      prompt?: string; // 可选，有值时以此 prompt 发起标准 Agent 对话请求，不再发送 Action 反馈请求
    }
}
```
【树状结构】

javascript
```
interface TreeAction{
    action: "tree";
      state: any;
      data: {
          treeId: string;// 树 ID，agent 下唯一
          rootPId: string; // 根节点的父 ID
          // 树节点列表
        nodes : {
          id: string; // 节点 ID
          pId: string; // 父节点 ID
          type: string; // 节点类型
          name: string; // 节点名称
          description: string;// 描述
          labels : string[];// 标签列表
        }[];
          // 树节点支持的操作列表
          nodeActions: {
              nodeType: string;    // 树节点类型
            nodeAction : "expand" | "click";    // 树节点操作类型，展开、点击
            command?: string; // 可选，有值时以此 command 发起标准 Agent 对话请求，不再发送 Action 反馈请求
            prompt?: string; // 可选，有值时以此 prompt 发起标准 Agent 对话请求，不再发送 Action 反馈请求
              promptByNodeProperty?: string; // 可选，有值时以此 node 的某个属性发起标准 Agent 对话请求，不再发送 Action 反馈请求
        }[];
    }
}
```
### 示例

智能体服务的实现不限语言，下面以 javascript 为例，实现智能体接收请求、处理参数、请求对话模型、响应数据的过程。

javascript
```
const http = require('http');

// 创建HTTP服务器
const server = http.createServer(async (req, res) => {
    const { 
      agent,    // agent 名称
      command,    // command 名称
      agentDefinition, // agent 原始定义
      contextVariables    // 上下文变量列表
    } = await parseBody(req);
    // 从请求中获取body
    console.log('agent:', agent);
    console.log('command:', command);
    // 获取上下文信息
    const userInfo = contextVariables?.find(ctx => ctx.name === 'userInfo') || {};

    // 设置响应头，指定内容类型为 text/event-stream，这是 SSE 所需的
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');

    // 生成消息ID，在一次响应中需要保持唯一
    const messageId = Date.now();

    // 根据 command 执行不同业务
    if (command == 'default') {
        // 默认指令推送欢迎信息文本
        res.write(createMessageChunk(messageId, `你好，${userInfo.value?.nickname} !\n`));
        res.write(createMessageChunk(messageId, `欢迎访问 Agent hello !`));
        // 推送一个交互按钮 action
        res.write(
            createActionChunk(
                'confirm',
                {},
                {
                    title: '获取版本号',
                    command: 'version',
                    prompt: ''
                }
            )
        );
        // 发送响应数据结束标识
        res.write(`data: [Done]\n`);
        // 结束响应
        res.end();
    } else if (command == 'version') {
        // 版本指令返回版本信息
        res.write(createMessageChunk(messageId, `当前版本是 v1.0.0 \n`));
        // 发送响应数据结束标识
        res.write(`data: [Done]\n`);
        // 结束响应
        res.end();
    } else if (command == 'xxx') {
          // 如果是 xxx 指令，则发起对话请求

          // 获取配置的消息模版
           const messageTemplates = getMessageTemplates(command, agentDefinition);

          // 根据消息模板和上下文变量列表，拼装 prompt 消息列表
        const messages = [{
            role : 'system',
              content : 'xxxxx'
        },{
            role : 'user',
              content : 'xxxxx'
        }];
        const baseRequestConfig = {
          headers: cropHeadersreq.headers), // 复用原请求头中的认证信息
          responseType: 'stream',
          timeout: 180 * 1000,
        };

        const payload = {
          ...req.body,    // 附加原请求中的其他参数
          contextVariables: null,    // 移除
          messageTemplates: null,    // 移除
          agentDefinition: null,    // 移除
          modelConfiguration: null,    // 移除
          messages,    // 处理后的消息列表
          stream: true,    // 流式
        };

          // 请求平台的模型对话接口
        const fetcher = axios.create({
          baseURL: CPILOT_SERVER_ENDPOINT,    // 平台 API 地址
          timeout: 3000 * 1000,
        });
        const { stream, headers } = await fetcher.post('/chat/completions', payload, baseRequestConfig);
          // 直接将请求返回的 res 对接 pipe 给客户端响应输出流中
        res.writeHead(200);
          stream.pipe(res);
    }
});

// 创建一个文本消息 chunk
function createMessageChunk(id, content) {
    const msg = JSON.stringify({
        id: id,
        model: 'happy',
        object: '',
        created: Date.now() / 1000,
        choices: [{ index: 0, delta: { role: 'assistant', content: content }, logprobs: null, finish_reason: '' }],
        usage: { prompt_tokens: 0, completion_tokens: 0, total_tokens: 0 }
    });
    return `data: ${msg}\n\n`;
}

// 创建一个 action chunk
function createActionChunk(action, state, data) {
    const msg = JSON.stringify({
        action,
        state,
        data
    });
    return `event: copilot_action\ndata: ${msg}\n\n`;
}

// 解析请求体
async function parseBody(req) {
    return new Promise((resolve, reject) => {
        let body = '';
        req.on('data', chunk => {
            body += chunk.toString();
        });
        req.on('end', () => {
            if (req.headers['content-type'] === 'application/json') {
                try {
                    const data = JSON.parse(body);
                    resolve(data); // 这里可以访问到解析后的 JSON 数据
                } catch (error) {
                    reject(error);
                }
            } else {
                reject(new Error('content-type error'));
            }
        });
    });
}

// 从 agent 定义中获取配置的消息模板
function getMessageTemplates(command, agent) {
    const messageTemplates = [];
    agent?.commands?.find(commandDefinition => {
      if (commandDefinition.name === command) {
        messageTemplates.push(...commandDefinition?.messageTemplates);
      }
    });
    return messageTemplates;
}

// 复制原请求头
function cropHeaders(headers) {
    const croppedHeaders = JSON.parse(JSON.stringify(headers));
    delete croppedHeaders['Host'];
    delete croppedHeaders['Host'.toLowerCase()];
    delete croppedHeaders['Content-Length'];
    delete croppedHeaders['Content-Length'.toLowerCase()];
    return croppedHeaders;
 }

// 监听端口
const PORT = 18080;
server.listen(PORT, () => {
    console.log(`Server is running at http://localhost:${PORT}`);
});
```