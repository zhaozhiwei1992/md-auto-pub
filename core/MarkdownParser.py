"""
处理markdown文件

解析头信息, 获取发布日期，标题, 分类等

"""
import os
import re


class MarkdownParser:

    def parse(self, fileName):
        curPath = os.path.abspath(os.path.dirname(__file__))
        # 获取项目根路径
        rootPath = curPath[:curPath.find("md-auto-pub/") + len("md-auto-pub/")]
        # 获取markdown文件的路径
        markdownPath = os.path.abspath(os.path.join(rootPath, 'markdown', fileName))

        markdownObj = {
            "title": "",
            "date": "",
            "updated": "",
            "tags": [],
            "categories": [],
            "content": ""
        }
        contentList = []
        front_matter = False
        first_h1_removed = False

        # 检查文件是否存在
        if os.path.exists(markdownPath):
            try:
                with open(markdownPath, 'r', encoding='utf-8') as readFile:
                    for line in readFile:
                        line = line.strip()
                        if line == "---":
                            front_matter = not front_matter
                            continue
                        if front_matter:
                            if line.startswith("title:"):
                                markdownObj['title'] = line[6:].strip()
                            elif line.startswith("date:"):
                                markdownObj['date'] = line[5:].strip()
                            elif line.startswith("updated:"):
                                markdownObj['updated'] = line[8:].strip()
                            elif line.startswith("tags:"):
                                tags = re.findall(r"\[([^\]]+)\]", line)
                                if tags:
                                    markdownObj['tags'] = [tag.strip() for tag in tags[0].split(",")]
                            elif line.startswith("categories:"):
                                categories = re.findall(r"\[([^\]]+)\]", line)
                                if categories:
                                    markdownObj['categories'] = [category.strip() for category in
                                                                 categories[0].split(",")]
                        else:
                            if line.startswith("# ") and not first_h1_removed:
                                first_h1_removed = True
                                continue
                            contentList.append(line)
            except Exception as e:
                print(f"Error reading file {markdownPath}: {e}")

            markdownObj['content'] = "\n".join(contentList)
        else:
            print(f"File {markdownPath} does not exist.")

        return markdownObj