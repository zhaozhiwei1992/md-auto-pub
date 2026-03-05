#!/bin/bash
# 微信公众号发布工具 - 依赖安装脚本

echo "🔧 检查 Python 环境..."
python3 --version || { echo "❌ Python3 未安装"; exit 1; }

echo "📦 检查 pip..."
if ! python3 -m pip --version 2>/dev/null; then
    echo "⚠️  pip 未安装，尝试安装..."

    # Arch Linux
    if command -v pacman &> /dev/null; then
        echo "📥 使用 pacman 安装 python-pip..."
        sudo pacman -S python-pip python-setuptools python-wheel
    # Ubuntu/Debian
    elif command -v apt-get &> /dev/null; then
        echo "📥 使用 apt 安装 python3-pip..."
        sudo apt-get update
        sudo apt-get install -y python3-pip python3-setuptools python3-wheel
    # macOS
    elif command -v brew &> /dev/null; then
        echo "📥 使用 brew 安装..."
        brew install python3
    else
        echo "❌ 无法自动安装 pip，请手动安装后重试"
        exit 1
    fi
fi

echo "📦 安装 Python 依赖包..."
python3 -m pip install --user requests markdown pillow pyyaml

echo "✅ 安装完成！"
echo ""
echo "📝 配置环境变量（可选）："
echo "  cp ~/.openclaw/workspace/tools/.env.example ~/.openclaw/workspace/tools/.env"
echo "  编辑 .env 文件填入你的 AppID 和 AppSecret"
echo ""
echo "🚀 开始使用："
echo "  cd ~/.openclaw/workspace/tools"
echo "  python3 wechat_mp_publisher.py test_article.md --appid <appid> --secret <secret> --author \"离线请留言\""
