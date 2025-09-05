#!/bin/bash

# 设置颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}    社区志愿服务系统启动脚本${NC}"
echo -e "${BLUE}========================================${NC}"
echo

# 检查是否安装了必要的依赖
echo -e "${YELLOW}[INFO] 检查系统依赖...${NC}"

# 检查Python
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo -e "${RED}[ERROR] Python未安装，请先安装Python 3.7+${NC}"
    exit 1
fi

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}[ERROR] Node.js未安装，请先安装Node.js 14+${NC}"
    exit 1
fi

# 检查npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}[ERROR] npm未安装，请先安装npm${NC}"
    exit 1
fi

echo -e "${GREEN}[SUCCESS] 系统依赖检查通过${NC}"
echo

# 启动后端服务
echo -e "${YELLOW}[INFO] 正在启动后端服务...${NC}"
cd backend

# 检查虚拟环境
if [ -d "venv" ]; then
    echo -e "${YELLOW}[INFO] 激活虚拟环境...${NC}"
    source venv/bin/activate
fi

# 启动后端（后台运行）
python run.py &
BACKEND_PID=$!
echo -e "${GREEN}[SUCCESS] 后端服务已启动 (PID: $BACKEND_PID)${NC}"

# 等待后端启动
echo -e "${YELLOW}[INFO] 等待后端服务完全启动...${NC}"
sleep 5

# 启动前端服务
echo -e "${YELLOW}[INFO] 正在启动前端服务...${NC}"
cd ../frontend
npm run serve &
FRONTEND_PID=$!
echo -e "${GREEN}[SUCCESS] 前端服务已启动 (PID: $FRONTEND_PID)${NC}"

echo
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}    服务启动完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo
echo -e "服务地址："
echo -e "  ${BLUE}后端API:${NC} http://localhost:5000"
echo -e "  ${BLUE}前端应用:${NC} http://localhost:8081"
echo
echo -e "${YELLOW}按 Ctrl+C 停止所有服务${NC}"
echo

# 创建停止函数
stop_services() {
    echo
    echo -e "${YELLOW}[INFO] 正在停止服务...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}[SUCCESS] 所有服务已停止${NC}"
    exit 0
}

# 捕获Ctrl+C信号
trap stop_services SIGINT

# 等待用户中断
while true; do
    sleep 1
done