from typing import Any, Dict, List, Optional
import psycopg2
from psycopg2 import OperationalError, ProgrammingError
import logging
from src.config import pg_config

logger = logging.getLogger(__name__)

class PGClient:
    """PostgreSQL客户端类，用于处理数据库连接和操作"""
    def __init__(self):
        self.conn: Optional[psycopg2.extensions.connection] = None

    def connect(self):
        """建立数据库连接"""
        if not self.conn or self.conn.closed:
            try:
                self.conn = psycopg2.connect(
                    host=pg_config.pg_host,
                    port=pg_config.pg_port,
                    user=pg_config.pg_user,
                    password=pg_config.pg_password,
                    dbname=pg_config.pg_db
                )
                logger.info("PostgreSQL连接成功")
            except OperationalError as e:
                logger.error(f"数据库连接失败: {str(e)}")
                raise

    def close(self):
        """关闭连接"""
        if self.conn and not self.conn.closed:
            self.conn.close()
            logger.info("PostgreSQL连接已关闭")

    def execute_query(self, sql: str, params: Optional[List] = None) -> Dict[str, Any]:
        """执行SQL查询（工具核心实现）"""
        self.connect()
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql, params or [])
            if sql.strip().upper().startswith("SELECT"):
                # 处理查询结果（返回字段名+数据）
                columns = [desc[0] for desc in cursor.description]
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]
                return {
                    "status": "success",
                    "data": data,
                    "row_count": len(data),
                    "message": "查询成功"
                }
            else:
                # 处理写入操作（提交事务）
                self.conn.commit()
                return {
                    "status": "success",
                    "row_count": cursor.rowcount,
                    "message": f"影响行数: {cursor.rowcount}"
                }
        except ProgrammingError as e:
            self.conn.rollback()
            return {"status": "error", "message": f"SQL错误: {str(e)}"}
        finally:
            cursor.close()

    def get_table_schema(self, table_name: str) -> Dict[str, Any]:
        """查询表结构"""
        sql = """
            SELECT 
                column_name, 
                data_type, 
                character_maximum_length,
                is_nullable,
                column_default
            FROM 
                information_schema.columns 
            WHERE 
                table_name = %s AND table_schema = 'public'
            ORDER BY 
                ordinal_position;
        """
        return self.execute_query(sql, (table_name,))

    def get_table_row_count(self, table_name: str) -> Dict[str, Any]:
        """统计表行数"""
        sql = f"SELECT COUNT(*) AS row_count FROM {table_name}"
        result = self.execute_query(sql)
        if result["status"] == "success":
            return {
                "status": "success",
                "table_name": table_name,
                "row_count": result["data"][0]["row_count"]
            }
        return result
    
    def list_tables(self) -> Dict[str, Any]:
        """
        获取数据库中所有用户创建的表（排除系统表）
        返回表名和备注信息（如果有）
        """
        self.connect()
        cursor = self.conn.cursor()
        try:
            # 查询用户创建的表（排除系统表和视图）
            sql = """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """
            cursor.execute(sql)
            columns = [desc[0] for desc in cursor.description]
            data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return {
                "status": "success",
                "table_count": len(data),
                "tables": data,  # 包含table_name和table_comment字段
                "message": f"找到{len(data)}个用户表"
            }
        except ProgrammingError as e:
            self.conn.rollback()
            return {"status": "error", "message": f"查询表列表失败: {str(e)}"}
        finally:
            cursor.close()