from typing import Optional, List
from mcp.server.fastmcp import FastMCP
import logging
import os
from src.config import pg_config
from src.database import PGClient
from logging.handlers import RotatingFileHandler

# 配置日志
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(
            os.path.join(log_dir, 'server.log'),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'  # 设置UTF-8编码以支持中文
        ),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# 初始化MCP服务
mcp = FastMCP("postgresql-mcp-server", host=pg_config.mcp_host, port=pg_config.mcp_port)
pg_client = PGClient()


@mcp.tool()
async def pg_execute_query(sql: str, params: Optional[List] = None) -> str:
    """
    执行PostgreSQL SQL查询（支持SELECT/INSERT/UPDATE/DELETE）。
    
    参数:
        sql: SQL语句（例如："SELECT * FROM users WHERE id = %s"）
        params: SQL参数列表（避免注入，例如：[1]）
    """
    try:
        result = pg_client.execute_query(sql, params)
        return str(result)  # 返回字符串便于Cherry Studio的AI解析
    except Exception as e:
        return f"执行失败: {str(e)}"


@mcp.tool()
async def pg_get_table_schema(table_name: str) -> str:
    """
    查询PostgreSQL表的结构（字段名、类型、主键等）。
    
    参数:
        table_name: 表名（例如："users"）
    """
    try:
        result = pg_client.get_table_schema(table_name)
        return str(result)
    except Exception as e:
        return f"查询失败: {str(e)}"


@mcp.tool()
async def pg_get_table_row_count(table_name: str) -> str:
    """
    查询PostgreSQL表的总行数。
    
    参数:
        table_name: 表名（例如："users"）
    """
    try:
        result = pg_client.get_table_row_count(table_name)
        return str(result)
    except Exception as e:
        return f"查询失败: {str(e)}"


@mcp.tool()
async def pg_list_tables() -> str:
    """
    获取数据库中所有用户创建的表。
    """
    try:
        result = pg_client.list_tables()
        return str(result)
    except Exception as e:
        return f"查询失败: {str(e)}"

def main():
    # 启动事件
    logger.info("=" * 50)
    logger.info("MCP SSE Service Starting")
    logger.info(f"Server: {pg_config.mcp_host}:{pg_config.mcp_port}")
    logger.info("=" * 50)
    
    # 启动MCP服务，指定传输方式为SSE（官网示例支持transport参数）
    mcp.run(transport='sse')

if __name__ == "__main__":

    main()
    