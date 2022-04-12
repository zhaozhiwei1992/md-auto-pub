"""
处理markdown文件

解析头信息, 获取发布日期，标题, 分类等

"""

class MarkdownParser:

    # 解析markdown文件, 发挥字典
    # title: 标题
    # tag: 标签, 逗号分隔
    # content: 内容
    def parse(self, path):
        # path为markdown全路径, 默认读取本地markdown目录
        # path中带有　/表示带有路径
        pass