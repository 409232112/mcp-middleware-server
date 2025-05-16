import contextlib
import logging
import json
from collections.abc import AsyncIterator
from typing import Any

import click
import uvicorn
import mcp.types as types
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.responses import JSONResponse
from starlette.types import Receive, Scope, Send

from mcp.server.lowlevel import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager

import utils
from mcp_tools import Tools

# 初始化日志记录器
logger = logging.getLogger(__name__)


class MCPServer:
    """MCP 服务器核心类，封装主要服务逻辑"""

    def __init__(self, port: int, log_level: str, json_response: bool):
        """初始化服务器配置"""
        self.port = port
        self.log_level = log_level
        self.json_response = json_response

        # 配置日志
        self._configure_logging()

        # 初始化核心组件
        self.server = Server("mcp-middleware-server")
        self.tools = Tools()
        self.session_manager = self._create_session_manager()

        # 注册工具和路由
        self._register_tools()
        self.starlette_app = self._create_starlette_app()

    def _configure_logging(self) -> None:
        """配置日志格式和级别"""
        logging.basicConfig(
            level=getattr(logging, self.log_level.upper()),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

    def _create_session_manager(self) -> StreamableHTTPSessionManager:
        """创建流式HTTP会话管理器"""
        return StreamableHTTPSessionManager(
            app=self.server,
            event_store=None,
            json_response=self.json_response,
            stateless=True,
        )

    def _register_tools(self) -> None:
        """注册工具函数"""

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> types.TextContent:
            """处理工具调用请求"""
            result = utils.function_call(self.tools.get_json_tools()[name]["api"],arguments)

            return [
                types.TextContent(
                    type="text",
                    text=result
                )
            ]
        @self.server.list_tools()
        async def list_tools() -> list[types.Tool]:
            """获取工具列表"""
            return self.tools.get_tools()

    async def _handle_streamable_http(self, scope: Scope, receive: Receive, send: Send) -> None:
        """处理流式HTTP请求"""
        await self.session_manager.handle_request(scope, receive, send)

    async def _set_tools(self, request: Any) -> JSONResponse:
        """
        处理设置工具的POST请求
        Args:
            request: Starlette 请求对象
        Returns:
            JSONResponse: 包含操作结果的响应
        """
        try:
            data = await request.json()
            self.tools.set_tools(data)
            return JSONResponse({"message": "success"}, status_code=200)
        except json.JSONDecodeError:
            return JSONResponse({"error": "Invalid JSON"}, status_code=400)
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return JSONResponse({"error": "Internal Server Error"}, status_code=500)

    @contextlib.asynccontextmanager
    async def _lifespan(self, app: Starlette) -> AsyncIterator[None]:
        """应用生命周期管理器"""
        async with self.session_manager.run():
            logger.info("Application started with StreamableHTTP session manager!")
            try:
                yield
            finally:
                logger.info("Application shutting down...")

    def _create_starlette_app(self) -> Starlette:
        """创建Starlette应用实例"""
        return Starlette(
            debug=True,
            routes=[
                # MCP协议路由
                Mount("/mcp", app=self._handle_streamable_http),
                # API路由
                Mount("/api", routes=[
                    Route("/set_tools", self._set_tools, methods=["POST"]),
                ]),
            ],
            lifespan=self._lifespan,
        )

    def run(self) -> None:
        """启动服务器"""
        uvicorn.run(
            self.starlette_app,
            host="0.0.0.0",
            port=self.port,
        )


@click.command()
@click.option("--port", default=3000, help="服务监听端口")
@click.option(
    "--log-level",
    default="INFO",
    help="日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
)
@click.option(
    "--json-response",
    is_flag=True,
    default=True,
    help="启用JSON响应(默认)或SSE流",
)
def main(port: int, log_level: str, json_response: bool) -> int:
    """
    MCP中间件服务器主入口

    Args:
        port: 服务监听端口
        log_level: 日志级别
        json_response: 是否使用JSON响应

    Returns:
        int: 退出状态码
    """
    try:
        server = MCPServer(port, log_level, json_response)
        server.run()
        return 0
    except Exception as e:
        logger.error(f"Server failed to start: {str(e)}")
        return 1


if __name__ == "__main__":
    main()