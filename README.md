# mcp-middleware-server

### [Python版本](https://github.com/409232112/mcp-middleware-server/tree/mcp-middleware-server-python)
### [Nodejs版本](https://github.com/409232112/mcp-middleware-server/tree/mcp-middleware-server-nodejs)


## 理念

还在为不知道让如何自己的系统如何接入MCP？还在头疼系统使用的是JDK8而无法兼容MCP SDK？没有什么是不能通过加一个中间层解决的！

mcp-middleware-server通过在业务系统与MCP客户端之间加一层中间层，对业务系统屏蔽掉MCP Server细节，业务系统只需要项目内置的网页API接口转换工具将系统API转换成mcp-middleware-server可识别的JSON文件即可对接MCP，尽情享用大模型与MCP带来的便捷！

## 优点

1、将MCP服务端与业务系统解耦，对原本系统无侵入，如果将来不用MCP协议或者有新的协议，只需要将中间层移除或者替换。

2、与业务系统技术栈无关系，不管业务系统是使用JDK8还是使用python构建，都能通过mcp-middleware-server接入MCP。

3、改造工作量非常小，只需要将原有业务系统需要提供方法调用的API接口能够适配mcp-middleware-server支持调用的Post请求Json数据传输方式即可。

## 缺点

1、引入中间层增加了系统复杂型，增加了MCP链路调用。

2、这个也可能是临时解决方案。

## 架构图
### 单机版
![single](https://github.com/user-attachments/assets/86c9473e-55bb-4c45-8a7a-7cdeb9cd3cc2)

### 集群版
![cluster](https://github.com/user-attachments/assets/bfaf60ec-a81b-4022-bee1-13448cb97cc7)
