# PostgreSQL MCP Server

This project implements a Server-Sent Events (SSE) service using FastMCP and PostgreSQL. 

## Project Structure

```
pg-mcp-server/
├── src/                       # 源代码目录
│   ├── __init__.py
│   ├── mcp_server.py          # 主应用入口点
│   ├── database/              # 数据库连接和模型
│   │   ├── __init__.py
│   │   └── connection.py      # 数据库连接管理
│   └── config/                # 配置设置
│       ├── __init__.py
│       └── settings.py        # 应用配置
├── tests/                     # 单元测试
│   ├── __init__.py
│   └── test.py                # 应用测试
├── logs/                      # 日志文件
│   └── server.log             # 应用日志文件（自动生成）
├── requirements.txt           # 项目依赖
├── .env.example               # 环境变量示例
├── .env                       # 实际环境变量（需复制.env.example并修改）
├── pg_mcp_server.py           # 旧版入口（兼容用）
└── README.md                  # 项目文档
```

## 快速开始

### 1. 配置环境变量

复制示例配置文件并修改：

```bash
cp .env.example .env
```

编辑`.env`文件，设置正确的数据库连接信息：

```
# Database Configuration
PG_HOST=localhost
PG_PORT=5432
PG_USER=postgres
PG_PASSWORD=your_password
PG_DB=your_database

# Server Configuration
MCP_HOST=0.0.0.0
MCP_PORT=8000
```

### 2. 运行服务

使用Docker Compose直接运行：

```bash
docker-compose up -d
```

## API工具列表

服务提供以下MCP工具：

1. **pg_execute_query**：执行SQL查询
2. **pg_get_table_schema**：获取表结构
3. **pg_get_table_row_count**：统计表行数
4. **pg_list_tables**：列出所有用户表

## 注意事项

- 确保PostgreSQL服务正在运行且可访问
- 提供的数据库用户需要有相应的操作权限
- 日志文件将自动创建在logs目录中

## Usage

- **SSE Endpoint:** Access the SSE service at `http://127.0.0.1:8000/sse` to retrieve all available tools.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.