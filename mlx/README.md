# MLX Server 配置指南

## 🎯 快速开始

### 1. 启动服务器
```bash
cd ~/mlx_server
./start_mlx_server.sh
```

### 2. 等待模型下载
- 首次启动需要下载约 15GB 模型文件
- 下载完成后会自动启动服务器
- 看到 `Serving on http://127.0.0.1:8080` 即表示成功

### 3. OpenClaw 配置

在 OpenClaw 的 `~/.openclawcn/config.yaml` 中添加：

```yaml
models:
  - id: local-qwen
    name: "本地千问2.5"
    provider: openai
    api_base: http://127.0.0.1:8080/v1
    api_key: mlx-local
    model: mlx-community/Qwen2.5-7B-Instruct-MLX
    max_tokens: 4096
    temperature: 0.7
```

## 📡 API 端点

- **聊天**: `POST http://127.0.0.1:8080/v1/chat/completions`
- **模型列表**: `GET http://127.0.0.1:8080/v1/models`

## 🔧 与 Claude Code 集成

在 Claude Code 设置中添加：
```json
{
  "model": "mlx-community/Qwen2.5-7B-Instruct-MLX",
  "apiBase": "http://127.0.0.1:8080/v1"
}
```

## 🖥️ 系统要求

| 项目 | 最低要求 |
|------|----------|
| macOS | 12.0+ (Apple Silicon 推荐) |
| RAM | 16GB+ |
| 存储 | 20GB+ 可用空间 |
| Python | 3.9+ |

## 📝 常用命令

```bash
# 启动服务器
./start_mlx_server.sh

# 后台运行
nohup ./start_mlx_server.sh > mlx_server.log 2>&1 &

# 停止服务器
pkill -f mlx_lm.server

# 查看日志
tail -f mlx_server.log

# 测试 API
curl http://127.0.0.1:8080/v1/models
```

## 🎉 优势

- ⚡ **极速响应**: 本地运行，无需网络延迟
- 🔒 **隐私安全**: 数据不上传云端
- 💰 **免费使用**: 无 API 调用费用
- 🚀 **性能优秀**: MLX 针对 Apple Silicon 优化

## 📚 参考

- [MLX-LM GitHub](https://github.com/ml-explore/mlx-lm)
- [MLX 文档](https://ml-explore.github.io/mlx/)
- [Qwen 模型](https://huggingface.co/Qwen)