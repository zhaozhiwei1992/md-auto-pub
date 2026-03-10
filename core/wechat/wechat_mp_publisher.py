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
from typing import Optional, Dict, List
import markdown

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
        """获取 access_token（带缓存，提前5分钟刷新）"""
        now = time.time()

        # 检查缓存是否有效
        if self.access_token and now < self.token_expires_at - 300:
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
        """上传文章图片，返回微信图片 URL"""
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
        # 接口发布草稿会乱码，必须使用以下方式编码
        data = bytes(json.dumps(data, ensure_ascii=False).encode('utf-8'))
        header_dict = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Content-Type': 'application/json; charset=utf-8'
        }
        response = requests.post(
            url=DRAFT_ADD_URL,
            params={'access_token': token},
            headers=header_dict,
            data=data,
        )
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
        提取 Markdown 中的本地图片

        Returns:
            图片列表，每项包含 local_path, markdown, alt
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
            带内联样式的 HTML 内容
        """
        # 替换本地图片链接为微信 URL
        if image_map:
            for local_path, wechat_url in image_map.items():
                pattern = re.escape(local_path)
                markdown_content = re.sub(
                    rf'!\[([^\]]*)\]\({pattern}\)',
                    rf'<img src="{wechat_url}" alt="\1" style="max-width: 100%; display: block; margin: 20px auto;">',
                    markdown_content
                )

        # 预处理代码块：先提取出来，避免 markdown 扩展破坏格式
        code_blocks = []

        def save_code_block(m):
            """保存代码块，用 HTML 注释占位"""
            lang = m.group(1) or ''
            code = m.group(2)
            code_blocks.append((lang, code))
            return f'<!--CODE_BLOCK_{len(code_blocks) - 1}-->'

        # 匹配代码块 ```lang ... ```
        markdown_content = re.sub(
            r'```(\w*)\n(.*?)```',
            save_code_block,
            markdown_content,
            flags=re.DOTALL
        )

        # 配置 markdown 扩展（不使用 codehilite，我们自己处理）
        extensions = [
            'markdown.extensions.extra',
            'markdown.extensions.toc',
            'markdown.extensions.tables'
        ]

        # 转换为 HTML
        html = markdown.markdown(markdown_content, extensions=extensions)

        # 恢复代码块，添加语言标记
        def restore_code_block(m):
            """恢复代码块，转为带语言标记的 pre/code 格式"""
            idx = int(m.group(1))
            if idx < len(code_blocks):
                lang, code = code_blocks[idx]
                # 转义 HTML 特殊字符
                escaped_code = (code.replace('&', '&amp;')
                                   .replace('<', '&lt;')
                                   .replace('>', '&gt;')
                                   .replace('"', '&quot;'))
                lang_attr = f' class="language-{lang}"' if lang else ''
                return f'<div class="codehilite"><pre><code{lang_attr}>{escaped_code}</code></pre></div>'
            return m.group(0)

        html = re.sub(r'<!--CODE_BLOCK_(\d+)-->', restore_code_block, html)

        # 添加微信内联样式
        styled_html = self._add_wechat_style(html)

        return styled_html

    def _add_wechat_style(self, html: str) -> str:
        """
        为 HTML 添加微信公众号兼容的内联样式

        微信公众号对 CSS 样式支持有限，需要将样式内联到标签中。
        同时处理以下特殊场景：
        1. 代码块：使用 blockquote 包裹，左侧蓝色条，等宽字体
        2. 列表：将 ul/li 转换为 p 标签加符号/编号
        3. 其他标签：添加预定义的内联样式

        Args:
            html: markdown 转换后的原始 HTML

        Returns:
            带内联样式的 HTML
        """
        from html.parser import HTMLParser
        from html import unescape

        # 各标签的内联样式映射
        styles_map = {
            'h1': 'font-size: 22px; font-weight: 600; color: #2c3e50; margin-top: 30px; margin-bottom: 15px; border-bottom: 2px solid #3498db; padding-bottom: 10px;',
            'h2': 'font-size: 20px; font-weight: 600; color: #2c3e50; margin-top: 25px; margin-bottom: 12px;',
            'h3': 'font-size: 18px; font-weight: 600; color: #2c3e50; margin-top: 20px; margin-bottom: 10px;',
            'h4': 'font-size: 16px; font-weight: 600; color: #2c3e50; margin-top: 15px; margin-bottom: 8px;',
            'p': 'margin-bottom: 15px; text-align: justify; line-height: 1.8; color: #333; font-size: 16px;',
            'strong': 'color: #e74c3c; font-weight: bold;',
            'b': 'color: #e74c3c; font-weight: bold;',
            'em': 'font-style: italic; color: #555;',
            'blockquote': 'border-left: 4px solid #3498db; padding-left: 15px; margin: 20px 0; color: #666; font-style: italic; background-color: #f9f9f9; padding: 10px 15px;',
            'ul': 'margin-bottom: 15px;',
            'ol': 'padding-left: 20px; margin-bottom: 15px;',
            'a': 'color: #3498db; text-decoration: none;',
            'table': 'width: 100%; border-collapse: collapse; margin: 20px 0;',
            'th': 'border: 1px solid #ddd; padding: 12px; text-align: left; background-color: #3498db; color: white;',
            'td': 'border: 1px solid #ddd; padding: 12px; text-align: left;',
        }

        class StyleInlineParser(HTMLParser):
            """HTML 解析器，将样式内联到标签中，并处理特殊格式"""

            def __init__(self):
                super().__init__()
                self.result = []              # 最终输出结果
                self.pre_content = []         # 代码块内容收集
                self.in_pre = False           # 是否在 pre 标签内
                self.in_code = False          # 是否在 code 标签内
                self.in_ul = False            # 是否在 ul 标签内
                self.ul_content = []          # ul 内容收集
                self.in_ol = False            # 是否在 ol 标签内
                self.ol_content = []          # ol 内容收集

            def handle_starttag(self, tag, attrs):
                attrs_dict = dict(attrs)

                # === 处理代码块 ===
                if tag == 'pre':
                    self.in_pre = True
                    return

                if tag == 'code':
                    self.in_code = True
                    return

                # 代码块内部不处理其他标签
                if self.in_pre or self.in_code:
                    return

                # === 处理列表 ===
                if tag == 'ul':
                    self.in_ul = True
                    self.ul_content = []
                    return

                if tag == 'ol':
                    self.in_ol = True
                    self.ol_content = []
                    return

                if tag == 'li':
                    return  # li 内容在 handle_data 中收集

                # === 处理普通标签 ===
                # 图片样式
                if tag == 'img':
                    style = 'max-width: 100%; height: auto; display: block; margin: 20px auto; border-radius: 5px;'
                    attrs_dict['style'] = style
                else:
                    # 添加预定义样式
                    if tag in styles_map:
                        existing_style = attrs_dict.get('style', '')
                        new_style = styles_map[tag]
                        attrs_dict['style'] = f'{existing_style}; {new_style}' if existing_style else new_style

                # 重建带样式的标签
                if attrs_dict:
                    attrs_str = ' ' + ' '.join(f'{k}="{v}"' for k, v in attrs_dict.items())
                else:
                    attrs_str = ''
                self.result.append(f'<{tag}{attrs_str}>')

            def handle_endtag(self, tag):
                # === 结束 code 标签 ===
                if tag == 'code' and self.in_code:
                    self.in_code = False
                    return

                # === 结束 pre 标签，生成代码块 HTML ===
                if tag == 'pre' and self.in_pre:
                    self.in_pre = False
                    code_content = ''.join(self.pre_content).strip()
                    self.pre_content = []

                    if code_content:
                        lines = code_content.split('\n')
                        lines = [line.rstrip() for line in lines]

                        if lines:
                            # 代码块使用 blockquote 样式：左侧蓝色条
                            quote_style = 'border-left: 4px solid #3498db; margin: 15px 0; padding: 15px; background-color: #f6f8fa; font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; font-size: 14px; line-height: 1.6;'
                            line_style = 'padding: 2px 0; min-height: 20px; margin: 0;'

                            result_lines = []
                            for line in lines:
                                escaped_line = (line.replace('&', '&amp;')
                                                   .replace('<', '&lt;')
                                                   .replace('>', '&gt;')
                                                   .replace('"', '&quot;'))
                                # 空行用 &nbsp; 保持高度
                                if not escaped_line.strip():
                                    escaped_line = '&nbsp;'
                                result_lines.append(f'<p style="{line_style}"><span style="white-space: pre-wrap;">{escaped_line}</span></p>')

                            self.result.append(f'<blockquote style="{quote_style}">')
                            self.result.extend(result_lines)
                            self.result.append('</blockquote>')
                    return

                # === 结束 ul 标签，生成无序列表 HTML ===
                if tag == 'ul' and self.in_ul:
                    self.in_ul = False
                    if self.ul_content:
                        p_style = 'margin: 5px 0; line-height: 1.6;'
                        for li_content in self.ul_content:
                            li_content = li_content.strip()
                            if li_content:
                                self.result.append(f'<p style="{p_style}">• {li_content}</p>')
                        self.ul_content = []
                    return

                # === 结束 ol 标签，生成有序列表 HTML ===
                if tag == 'ol' and self.in_ol:
                    self.in_ol = False
                    if self.ol_content:
                        p_style = 'margin: 5px 0; line-height: 1.6;'
                        for i, li_content in enumerate(self.ol_content, 1):
                            li_content = li_content.strip()
                            if li_content:
                                self.result.append(f'<p style="{p_style}">{i}. {li_content}</p>')
                        self.ol_content = []
                    return

                if tag == 'li':
                    return

                if self.in_pre or self.in_ul or self.in_ol:
                    return

                self.result.append(f'</{tag}>')

            def handle_data(self, data):
                """处理文本内容"""
                if self.in_pre or self.in_code:
                    self.pre_content.append(data)
                elif self.in_ul:
                    self.ul_content.append(data)
                elif self.in_ol:
                    self.ol_content.append(data)
                else:
                    self.result.append(data)

            def handle_entityref(self, name):
                """处理 HTML 实体引用，如 &amp;"""
                char = unescape(f'&{name};')
                if self.in_pre or self.in_code:
                    self.pre_content.append(char)
                elif self.in_ul:
                    self.ul_content.append(char)
                elif self.in_ol:
                    self.ol_content.append(char)
                else:
                    self.result.append(char)

            def handle_charref(self, name):
                """处理字符引用，如 &#123;"""
                char = unescape(f'&#{name};')
                if self.in_pre or self.in_code:
                    self.pre_content.append(char)
                elif self.in_ul:
                    self.ul_content.append(char)
                elif self.in_ol:
                    self.ol_content.append(char)
                else:
                    self.result.append(char)

        # 解析并添加内联样式
        parser = StyleInlineParser()
        parser.feed(html)
        result = ''.join(parser.result)

        # 添加整体容器样式
        container_style = 'font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; line-height: 1.8; color: #333; max-width: 677px; margin: 0 auto; padding: 20px;'
        result = f'<section style="{container_style}">{result}</section>'

        return result

    def generate_cover_image(self, title: str, output_path: str = None) -> str:
        """
        生成默认封面图片（微信封面尺寸: 900x383）
        """
        if output_path is None:
            output_path = os.path.join(self.base_dir, ".tmp_cover.jpg")

        from PIL import Image, ImageDraw, ImageFont

        width, height = 900, 383
        img = Image.new('RGB', (width, height), color='#3498db')
        draw = ImageDraw.Draw(img)

        # 尝试加载系统字体
        try:
            # Linux
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        except:
            try:
                # macOS
                font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 40)
            except:
                font = ImageFont.load_default()

        # 绘制标题（限制长度）
        text_color = (255, 255, 255)
        display_title = title[:15] + "..." if len(title) > 15 else title
        draw.text((50, 150), display_title, fill=text_color, font=font)

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

    if not os.path.exists(args.markdown_file):
        print(f"❌ 错误: 文件不存在: {args.markdown_file}")
        sys.exit(1)

    print(f"📖 读取 Markdown 文件: {args.markdown_file}")

    # 处理 Markdown
    processor = MarkdownProcessor()
    parsed = processor.parse_markdown(args.markdown_file)

    # 提取元信息
    metadata = parsed["metadata"]
    print(" 元信息:", metadata)
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
        print(f"   ⚠️  未提供封面，生成默认封面...")
        cover_path = processor.generate_cover_image(title)
        cover_media_id = api.upload_cover_image(cover_path)
        print(f"   ✅ 默认封面已上传")
        os.remove(cover_path)  # 清理临时文件

    # 转换为 HTML
    print(f"\n🔄 转换 Markdown 到 HTML...")
    html_content = processor.convert_to_html(parsed["content"], image_map)

    # 检查长度（微信限制 20000 字符）
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
