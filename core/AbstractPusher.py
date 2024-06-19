"""
抽象发布者, 负责定义整体发布流程

自定义各个网站的发布流程
"""
import importlib
import json
import os
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException

from core.ConfigParser import ConfigParser
from core.MarkdownParser import MarkdownParser


def getCookiePath(param):
    pass


class AbstractPusher:

    # 博客发布核心入口
    def push(self, path):
        # 获取要发布的markdown文件, 并解析处理
        markdownDict = MarkdownParser().parse(path)

        # 解析conf获取登录信息, 遍历发布, 如zhihu.json, 处理ENABLE==true的
        # 返回所有网站配置信息
        allConfig = ConfigParser().trans()

        # 发布, 遍历返回的key信息, key作为目录名称, 分别去各个目录找到处理方式
        for platform, config in allConfig.items():
            print(f'Platform: {platform}, Config: {config}')

            # 动态导入模块和函数
            try:
                moduleSrc = f"core.{platform}.Pusher"
                lib = importlib.import_module(moduleSrc)
                lib.Pusher().pushExt(config, markdownDict)
            except ModuleNotFoundError:
                print(f"暂不支持 {platform}")

    # 扩展实现该方法
    def pushExt(self, config, markdownProperties):
        # # 登录
        # self.login(config)
        # # 跳转不同发布界面
        # self.forward()
        # # 填入文章内容, 并根据不同网站自定义发布
        # self.write(config, markdownProperties)
        # self.submit()
        driver = webdriver.Chrome(executable_path="/tmp/chromedriver")
        driver.set_page_load_timeout(10)
        self.loginAndForward(driver, config.get("URL"))
        self.write(driver, config, markdownProperties)
        # 关掉浏览器
        time.sleep(10)
        driver.quit()

    # 登录并跳转
    def loginAndForward(self, driver, url):
        curPath = os.path.abspath(os.path.dirname(__file__))
        rootPath = curPath[:curPath.find("md-auto-pub/") + len("md-auto-pub/")]
        cookiePath = self.getCookiePath(rootPath)

        if not os.path.exists(cookiePath):
            driver.maximize_window()
            driver.get(url)
            # 等待用户手动登录
            time.sleep(30)
            dictCookies = driver.get_cookies()
            jsonCookies = json.dumps(dictCookies)
            with open(cookiePath, 'w') as f:
                f.write(jsonCookies)
        else:
            try:
                driver.get(url)
                driver.delete_all_cookies()
                with open(cookiePath, 'r', encoding='utf8') as f:
                    cookies = json.load(f)
                for cookie in cookies:
                    driver.add_cookie(cookie)
                driver.get(url)
            except TimeoutException:
                print('timeout')

    def write(self, config, markdownProperties):
        pass
