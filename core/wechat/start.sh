#!/bin/bash
# 快速开始 - 微信公众号发布工具

set -e

# 颜色
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  微信公众号发布工具 - 快速开始${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 工作目录
cd "$(dirname "$0")"

# 1. 检查 Python
echo -e "🔧 ${BLUE}检查 Python 环境...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 未安装${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python3: $(python3 --version)${NC}"

# 2. 检查依赖
echo ""
echo -e "📦 ${BLUE}检查 Python 依赖...${NC}"
MISSING_DEPS=0

for dep in requests markdown PIL yaml; do
    if ! python3 -c "import $dep" 2>/dev/null; then
        echo -e "  ${YELLOW}⚠️  缺少: $dep${NC}"
        MISSING_DEPS=1
    fi
done

if [ $MISSING_DEPS -eq 1 ]; then
    echo ""
    echo -e "${YELLOW}⚠️  缺少依赖包${NC}"
    read -p "是否立即安装? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ./install.sh
    else
        echo -e "${RED}❌ 请先安装依赖: ./install.sh${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ 所有依赖已安装${NC}"
fi

# 3. 配置检查
echo ""
echo -e "⚙️  ${BLUE}检查配置...${NC}"

if [ -f ".env" ]; then
    echo -e "${GREEN}✅ 找到 .env 配置文件${NC}"
    source .env
    echo -e "   AppID: ${WECHAT_APPID:0:8}***"
    echo -e "   Author: ${WECHAT_AUTHOR}"
else
    echo -e "${YELLOW}⚠️  未找到 .env 文件${NC}"
    read -p "是否创建配置文件? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cp .env.example .env
        echo -e "${GREEN}✅ 已创建 .env${NC}"
        echo -e "${YELLOW}⚠️  请编辑 .env 填入真实凭证${NC}"
        exit 0
    fi
fi

# 4. 测试
echo ""
echo -e "🧪 ${BLUE}测试工具 (dry-run 模式)...${NC}"
python3 wechat_mp_publisher.py test_article.md \
    --appid "${WECHAT_APPID:-yourappid}" \
    --secret "${WECHAT_SECRET:-yoursecret}" \
    --author "${WECHAT_AUTHOR:-离线请留言}" \
    --dry-run

if [ -f "test_article.html" ]; then
    echo ""
    echo -e "${GREEN}✅ 测试成功!${NC}"
    echo -e "   预览文件: ${PWD}/test_article.html"
else
    echo -e "${RED}❌ 测试失败${NC}"
    exit 1
fi

# 5. 使用说明
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}🎉 工具已就绪！${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "发布文章到草稿:"
echo ""
echo -e "  ${YELLOW}方法 1: 使用完整参数${NC}"
echo -e "  python3 wechat_mp_publisher.py your-article.md \\"
echo -e "    --appid <APPID> --secret <SECRET> --author \"离线请留言\""
echo ""
echo -e "  ${YELLOW}方法 2: 使用快捷脚本${NC}"
echo -e "  ./wxpub your-article.md"
echo ""
echo -e "  ${YELLOW}方法 3: 只转换 HTML${NC}"
echo -e "  python3 wechat_mp_publisher.py your-article.md --dry-run"
echo ""
echo -e "${BLUE}📚 更多信息:${NC}"
echo -e "   查看 使用指南.md"
echo -e "   查看 README.md"
echo ""
