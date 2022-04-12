"""
抽象发布者, 负责定义整体发布流程

自定义各个网站的发布流程
"""
from core.ConfigParser import ConfigParser
from core.MarkdownParser import MarkdownParser
import core.zhihu.Pusher


class AbstractPusher:

    # 博客发布核心入口
    def push(self):
        # 获取要发布的markdown文件, 并解析处理
        markdownParser = MarkdownParser()
        markdownDict = markdownParser.parse("test.md")

        # 解析conf获取登录信息,遍历发布, 如zhihu.json, 处理ENABLE==true的
        configParser = ConfigParser()
        # 返回所有网站配置信息
        allConfig = configParser.trans()

        # 发布, 遍历返回的key信息, key作为目录名称,分别去各个目录找到处理方式
        for config in allConfig:
            # key, 根据key找到目录下的Pusher作为入口, 没有反射只能判断了
            if config == "zhihu":
                core.zhihu.Pusher().pushExt("config", markdownDict)
            elif config == "cnblog":
                core.cnblog.Pusher().pushExt("config", markdownDict)
            else:
                print("暂不支持", config)

    # 扩展实现该方法
    def pushExt(self):
        # 登录
        self.login()
        # 跳转不同发布界面
        self.forward()
        # 填入文章内容,并根据不同网站自定义发布
        self.write()
        self.submit()

    # 1. 登录
    def login(self):
        pass

    def forward(self):
        pass

    def write(self):
        pass

    def submit(self):
        pass