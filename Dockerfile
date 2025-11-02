# 使用官方Python镜像作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /usr/src/app

# 复制项目依赖文件
COPY requirements.txt ./

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt python-multipart -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制项目文件
COPY . .

# 暴露服务端口
EXPOSE 8000

# 启动服务
CMD ["python", "-m", "src.mcp_server"]