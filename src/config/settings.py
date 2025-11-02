from pydantic_settings import BaseSettings


class PGConfig(BaseSettings):
    """PostgreSQL配置类"""
    pg_host: str = "localhost"
    pg_port: int = 5432
    pg_user: str = "postgres"
    pg_password: str = "123456"
    pg_db: str = "test_db"
    mcp_host: str = "0.0.0.0"
    mcp_port: int = 8000

    class Config:
        env_file = ".env"

pg_config = PGConfig()
