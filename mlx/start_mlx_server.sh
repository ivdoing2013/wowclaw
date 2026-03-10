#!/bin/bash
# WowOclaw MLX Server 启动脚本
# 使用方法: ./start_mlx_server.sh

echo "🚀 启动 MLX Server with Qwen2.5..."

# 添加 PATH
export PATH="/Users/simon/Library/Python/3.9/bin:$PATH"

# 检查 mlx-lm 是否安装
if ! command -v mlx_lm.server &> /dev/null; then
    echo "❌ mlx-lm 未安装，正在安装..."
    pip3 install mlx-lm
fi

# 启动服务器
echo "📥 正在加载模型 mlx-community/Qwen2.5-7B-Instruct-MLX..."
echo "⏳ 首次启动需要下载模型（约 15GB），请耐心等待..."
echo ""

mlx_lm.server \
    --model mlx-community/Qwen2.5-7B-Instruct-MLX \
    --port 8080 \
    --host 127.0.0.1 \
    --trust-remote-code

echo "✅ MLX Server 已启动！"
echo "📍 API 地址: http://localhost:8080/v1"
echo "📝 在 OpenClaw 中配置: http://127.0.0.1:8080/v1/chat/completions"