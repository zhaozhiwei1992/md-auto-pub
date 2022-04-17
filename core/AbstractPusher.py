"""
抽象发布者, 负责定义整体发布流程

自定义各个网站的发布流程
"""
from core.ConfigParser import ConfigParser
from core.MarkdownParser import MarkdownParser
import core.jianshu.Pusher as JianshuPusher
import core.zhihu.Pusher as ZhihuPusher
import core.cnblog.Pusher as CnblogPusher
import importlib


class AbstractPusher:

    # 博客发布核心入口
    def push(self, path):
        # 获取要发布的markdown文件, 并解析处理
        markdownDict = MarkdownParser().parse(path)

        # 解析conf获取登录信息,遍历发布, 如zhihu.json, 处理ENABLE==true的
        # 返回所有网站配置信息
        allConfig = ConfigParser().trans()

        # 发布, 遍历返回的key信息, key作为目录名称,分别去各个目录找到处理方式
        for item in allConfig.items():
            print('item中key %s value %s' % (item[0], item[1]))

            # key, 根据key找到目录下的Pusher作为入口, 没有反射只能判断了
            # if item[0] == "zhihu":
            #     ZhihuPusher.Pusher().pushExt(item[1], markdownDict)
            # elif item[0] == "cnblog":
            #     CnblogPusher.Pusher().pushExt(item[1], markdownDict)
            # elif item[0] == "jianshu":
            #     JianshuPusher.Pusher().pushExt(item[1], markdownDict)
            # else:
            #     print("暂不支持", item[0])

            # 动态导入
            moduleSrc = "core." + item[0] + ".Pusher"
            # 动态导入模块，此时，lib就相当于core.jianshu.Pusher
            lib = importlib.import_module(moduleSrc)
            # 动态导入函数
            lib.Pusher().pushExt(item[1], markdownDict)

    # 扩展实现该方法
    def pushExt(self):
        # 登录
        self.login()
        # 跳转不同发布界面
        self.forward()
        # 填入文章内容,并根据不同网站自定义发布
        self.write()
        self.submit()

    # 登录并跳转
    def loginAndForward(self, driver, url):
        pass

    def write(self, config, markdownProperties):
        pass
