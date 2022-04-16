"""
处理markdown文件

解析头信息, 获取发布日期，标题, 分类等

"""
import os


class MarkdownParser:

    # 解析markdown文件, 放到字典
    # title: 标题
    # tag: 标签, 逗号分隔
    # content: 内容
    def parse(self, fileName):
        curPath = os.path.abspath(os.path.dirname(__file__))
        # MdAutoPub，也就是项目的根路径
        rootPath = curPath[:curPath.find("MdAutoPub/") + len("MdAutoPub/")]
        # 获取xx.md文件的路径
        markdownPath = os.path.abspath(rootPath + 'markdown/' + fileName)

        markdownObj = {"title": "", "tag": "", "content": ""}
        contentList = []
        # 读取文件内容
        if os.path.exists(markdownPath):
            try:
                # 读取数据
                readFile = open(markdownPath)
                while True:
                    line = readFile.readline()

                    if len(line) == 0:
                        break
                    if line.startswith("---"):
                        continue
                    elif line.startswith("title:"):
                        markdownObj['title'] = line[6:].replace("\n", "")
                    elif line.startswith("tag:"):
                        markdownObj['tag'] = line[4:].replace("\n", "")
                    else:
                        contentList.append(line)
            finally:
                readFile.close()
            markdownObj['content'] = "".join(contentList)
            return markdownObj
