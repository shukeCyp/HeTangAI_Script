#!/bin/bash
set -e

# 切换到脚本所在目录
cd "$(dirname "$0")"

echo "========================================="
echo "  荷塘AI生成器 - 构建并启动"
echo "========================================="

# 1. 构建前端
echo ""
echo "[1/2] 构建前端..."
cd frontend
npm install --silent
npm run build
cd ..
echo "前端构建完成 -> web/"

# 2. 启动 pywebview
echo ""
echo "[2/2] 启动应用..."
uv run python -m backend.main
