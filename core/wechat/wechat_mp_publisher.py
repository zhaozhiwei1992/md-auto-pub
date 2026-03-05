#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号发布工具 - 从 Markdown 发布到公众号草稿

使用方法:
    python wechat_mp_publisher.py <markdown_file> --appid <appid> --secret <secret>

依赖:
    pip install requests markdown pillow
"""

import os
import sys
import json
import re
import time
import requests
from pathlib import Path
from typing import Optional, Dict, List
import markdown
from io import BytesIO
from PIL import Image

# ==================== 配置 ====================
# API 端点
API_BASE = "https://api.weixin.qq.com/cgi-bin"
TOKEN_URL = f"{API_BASE}/token"
UPLOAD_IMG_URL = f"{API_BASE}/media/uploadimg"
ADD_MATERIAL_URL = f"{API_BASE}/material/add_material"
DRAFT_ADD_URL = f"{API_BASE}/draft/add"

# ==================== 工具类 ====================

class WechatMPAPI:
    """微信公众号 API 客户端"""

    def __init__(self, appid: str, secret: str):
        self.appid = appid
        self.secret = secret
        self.access_token: Optional[str] = None
        self.token_expires_at: float = 0

    def get_access_token(self) -> str:
        """获取 access_token（带缓存）"""
        now = time.time()

        # 检查缓存
        if self.access_token and now < self.token_expires_at - 300:  # 提前5分钟刷新
            return self.access_token

        # 请求新 token
        params = {
            "grant_type": "client_credential",
            "appid": self.appid,
            "secret": self.secret
        }

        response = requests.get(TOKEN_URL, params=params)
        result = response.json()

        if "errcode" in result:
            raise Exception(f"获取 token 失败: {result['errmsg']} (errcode: {result['errcode']})")

        self.access_token = result["access_token"]
        self.token_expires_at = now + result["expires_in"]

        return self.access_token

    def upload_article_image(self, image_path: str) -> str:
        """上传文章图片，返回 URL"""
        token = self.get_access_token()
        url = f"{UPLOAD_IMG_URL}?access_token={token}"

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片文件不存在: {image_path}")

        with open(image_path, "rb") as f:
            files = {"media": f}
            response = requests.post(url, files=files)

        result = response.json()

        if "errcode" in result:
            raise Exception(f"上传图片失败: {result['errmsg']} (errcode: {result['errcode']})")

        return result["url"]

    def upload_cover_image(self, image_path: str) -> str:
        """上传封面图片（永久素材），返回 media_id"""
        token = self.get_access_token()
        url = f"{ADD_MATERIAL_URL}?access_token={token}&type=image"

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"封面图片不存在: {image_path}")

        with open(image_path, "rb") as f:
            files = {"media": f}
            response = requests.post(url, files=files)

        result = response.json()

        if "errcode" in result:
            raise Exception(f"上传封面失败: {result['errmsg']} (errcode: {result['errcode']})")

        return result["media_id"]

    def create_draft(self, articles: List[Dict]) -> str:
        """创建草稿，返回 media_id"""
        token = self.get_access_token()
        url = f"{DRAFT_ADD_URL}?access_token={token}"

        data = {"articles": articles}
        print('articles', data)
        # 接口发布草稿上去乱码，变成了unicode, 必须按照下边的写法来
        data = bytes(json.dumps(data, ensure_ascii=False).encode('utf-8'))
        header_dict = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
                        'Content-Type': 'application/json; charset=utf-8'
                        }
        resp = requests.post(
                    url=DRAFT_ADD_URL,
                    params={'access_token': token},
                    headers=header_dict,
                    data=data,
                    )
        # 这个写法上传直接乱码，垃圾
        # response = requests.post(url, json=data)
        result = response.json()

        if "errcode" in result:
            raise Exception(f"创建草稿失败: {result['errmsg']} (errcode: {result['errcode']})")

        return result["media_id"]


class MarkdownProcessor:
    """Markdown 处理器，转换为微信公众号格式"""

    def __init__(self, base_dir: str = None):
        self.base_dir = base_dir or os.getcwd()

    def parse_markdown(self, file_path: str) -> Dict:
        """解析 Markdown 文件，提取元信息和内容"""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 提取 YAML front matter
        metadata = {}
        body = content

        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 2:
                try:
                    import yaml
                    metadata = yaml.safe_load(parts[1])
                    body = parts[2] if len(parts) > 2 else ""
                except ImportError:
                    body = content

        # 提取标题（如果 YAML 中没有）
        if not metadata.get("title"):
            title_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
            if title_match:
                metadata["title"] = title_match.group(1).strip()

        # 提取摘要（如果 YAML 中没有）
        if not metadata.get("digest"):
            # 取正文前 100 个字作为摘要
            text_only = re.sub(r'[#\*\`\[\]()]+', '', body)
            metadata["digest"] = text_only[:100].strip()

        return {
            "metadata": metadata,
            "content": body,
            "file_path": file_path
        }

    def extract_images(self, content: str, md_file_path: str) -> List[Dict]:
        """
        提取 Markdown 中的图片

        返回: [
            {"local_path": "/path/to/image.jpg", "markdown": "![alt](path/to/image.jpg)", "index": 0}
        ]
        """
        images = []
        md_dir = os.path.dirname(os.path.abspath(md_file_path))

        # 匹配图片语法: ![alt text](image.jpg)
        pattern = r'!\[([^\]]*)\]\(([^)]+)\)'

        for match in re.finditer(pattern, content):
            alt = match.group(1)
            img_path = match.group(2)

            # 跳过网络图片
            if img_path.startswith("http://") or img_path.startswith("https://"):
                continue

            # 解析本地路径（相对于 Markdown 文件）
            local_path = os.path.join(md_dir, img_path)
            if os.path.exists(local_path):
                images.append({
                    "local_path": local_path,
                    "markdown": match.group(0),
                    "alt": alt
                })

        return images

    def convert_to_html(self, markdown_content: str, image_map: Dict[str, str] = None) -> str:
        """
        将 Markdown 转换为微信公众号 HTML 格式

        Args:
            markdown_content: Markdown 内容
            image_map: {本地路径: 微信图片URL} 映射

        Returns:
            HTML 内容
        """
        # 替换本地图片链接为微信 URL
        if image_map:
            for local_path, wechat_url in image_map.items():
                # 匹配 ![alt](local_path)
                pattern = re.escape(local_path)
                markdown_content = re.sub(
                    rf'!\[([^\]]*)\]\({pattern}\)',
                    rf'<img src="{wechat_url}" alt="\1" style="max-width: 100%; display: block; margin: 20px auto;">',
                    markdown_content
                )

        # 配置 markdown 扩展
        extensions = [
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.tables'
        ]

        # 转换为 HTML
        html = markdown.markdown(markdown_content, extensions=extensions)

        # 添加微信样式
        styled_html = self._add_wechat_style(html)

        return styled_html

    def _add_wechat_style(self, html: str) -> str:
        """添加微信公众号专用样式"""
        styles = """
        <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            line-height: 1.8;
            color: #333;
            max-width: 677px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            margin-top: 30px;
            margin-bottom: 15px;
            font-weight: 600;
        }
        h1 { font-size: 24px; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        h2 { font-size: 20px; }
        h3 { font-size: 18px; }
        p { margin-bottom: 15px; text-align: justify; }
        strong { color: #e74c3c; font-weight: bold; }
        code {
            background-color: #f6f8fa;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 14px;
        }
        pre {
            background-color: #f6f8fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            margin: 15px 0;
        }
        pre code {
            background-color: transparent;
            padding: 0;
        }
        blockquote {
            border-left: 4px solid #3498db;
            padding-left: 15px;
            color: #666;
            margin: 20px 0;
            font-style: italic;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th { background-color: #3498db; color: white; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 20px auto;
            border-radius: 5px;
        }
        ul, ol { padding-left: 20px; margin-bottom: 15px; }
        li { margin-bottom: 8px; }
        a { color: #3498db; text-decoration: none; }
        a:hover { text-decoration: underline; }
        </style>
        """

        return f"{styles}\n{html}"

    def generate_cover_image(self, title: str, output_path: str = None) -> str:
        """
        生成封面图片（如果未提供）

        使用 Pillow 创建简单的封面
        """
        if output_path is None:
            output_path = os.path.join(self.base_dir, ".tmp_cover.jpg")

        # 微信封面尺寸: 900x383
        width, height = 900, 383

        # 创建图片
        from PIL import Image, ImageDraw, ImageFont

        img = Image.new('RGB', (width, height), color='#3498db')
        draw = ImageDraw.Draw(img)

        # 尝试加载字体（系统字体）
        try:
            # Linux
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        except:
            try:
                # macOS
                font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 40)
            except:
                # 回退
                font = ImageFont.load_default()

        # 绘制标题（自动换行）
        text_color = (255, 255, 255)
        draw.text((50, 150), title[:15] + "..." if len(title) > 15 else title,
                  fill=text_color, font=font)

        # 保存
        img.save(output_path, 'JPEG', quality=85)

        return output_path


# ==================== 主函数 ====================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="从 Markdown 发布到微信公众号草稿")
    parser.add_argument("markdown_file", help="Markdown 文件路径")
    parser.add_argument("--appid", required=True, help="微信 AppID")
    parser.add_argument("--secret", required=True, help="微信 AppSecret")
    parser.add_argument("--author", default="离线请留言", help="文章作者")
    parser.add_argument("--cover", help="封面图片路径（可选）")
    parser.add_argument("--dry-run", action="store_true", help="只转换不发布")

    args = parser.parse_args()

    # 检查文件
    if not os.path.exists(args.markdown_file):
        print(f"❌ 错误: 文件不存在: {args.markdown_file}")
        sys.exit(1)

    print(f"📖 读取 Markdown 文件: {args.markdown_file}")

    # 处理 Markdown
    processor = MarkdownProcessor()
    parsed = processor.parse_markdown(args.markdown_file)

    # 元信息
    metadata = parsed["metadata"]
    title = metadata["title"]
    author = metadata["author"]
    digest = metadata["digest"]

    print(f"   标题: {title}")
    print(f"   作者: {author}")
    print(f"   摘要: {digest[:50]}...")

    # 提取图片
    images = processor.extract_images(parsed["content"], args.markdown_file)
    print(f"   发现图片: {len(images)} 张")

    if args.dry_run:
        # 只转换 HTML，不上传
        html = processor.convert_to_html(parsed["content"])
        output_file = args.markdown_file.replace(".md", ".html")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"\n✅ HTML 已保存到: {output_file}")
        return

    # 调用微信 API
    print("\n🔗 连接微信 API...")
    api = WechatMPAPI(args.appid, args.secret)

    # 上传文章图片
    image_map = {}
    if images:
        print(f"\n📤 上传文章图片...")
        for i, img_info in enumerate(images, 1):
            try:
                print(f"   [{i}/{len(images)}] {img_info['local_path']}")
                wechat_url = api.upload_article_image(img_info["local_path"])
                image_map[img_info["local_path"]] = wechat_url
                print(f"      ✅ {wechat_url}")
            except Exception as e:
                print(f"      ❌ 失败: {e}")
                continue

    # 处理封面图
    print("\n📤 处理封面图...")
    if args.cover and os.path.exists(args.cover):
        cover_media_id = api.upload_cover_image(args.cover)
        print(f"   ✅ 封面已上传")
    else:
        # 生成默认封面
        print(f"   ⚠️  未提供封面，生成默认封面...")
        cover_path = processor.generate_cover_image(title)
        cover_media_id = api.upload_cover_image(cover_path)
        print(f"   ✅ 默认封面已上传")
        # 清理临时文件
        os.remove(cover_path)

    # 转换为 HTML
    print(f"\n🔄 转换 Markdown 到 HTML...")
    html_content = processor.convert_to_html(parsed["content"], image_map)

    # 检查长度
    if len(html_content) > 20000:
        print(f"   ⚠️  警告: HTML 内容过长 ({len(html_content)} 字符)，微信限制 20000 字符")
        html_content = html_content[:20000]

    # 创建草稿
    print(f"\n📝 创建公众号草稿...")
    article = {
        "title": title,
        "author": author,
        "digest": digest,
        "content": html_content,
        "thumb_media_id": cover_media_id,
        "show_cover_pic": 1,
        "need_open_comment": 1,
        "only_fans_can_comment": 0
    }

    draft_media_id = api.create_draft([article])

    print(f"\n✅ 成功!")
    print(f"   草稿 ID: {draft_media_id}")
    print(f"   请到公众号后台查看并发布")


if __name__ == "__main__":
    main()
