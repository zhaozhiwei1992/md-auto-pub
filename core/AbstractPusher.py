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


class AbstractPusher:

    def getCookiePath(self, rootPath):
        pass

    # 博客发布核心入口
    def push(self, path, pform):
        # 获取要发布的markdown文件, 并解析处理
        markdownDict = MarkdownParser().parse(path)

        # 解析conf获取登录信息, 遍历发布, 如zhihu.json, 处理ENABLE==true的
        # 返回所有网站配置信息
        allConfig = ConfigParser().trans()

        options = webdriver.ChromeOptions()                  # 创建一个配置对象

        # options.add_argument('--headless')                 # 开启无界面模式
        options.add_argument("--disable-gpu")              # 禁用gpu
        # options.add_argument('--user-agent=Mozilla/5.0 HAHA')  # 配置对象添加替换User-Agent的命令
        # options.add_argument('--window-size=1366,768')    # 设置浏览器分辨率（窗口大小）
        options.add_argument('--start-maximized')         # 最大化运行（全屏窗口）,不设置，取元素会报错
        # options.add_argument('--disable-infobars')        # 禁用浏览器正在被自动化程序控制的提示
        # options.add_argument('--incognito')               # 隐身模式（无痕模式）
        # options.add_argument('--disable-javascript')      # 禁用javascript

        # 发布, 遍历返回的key信息, key作为目录名称, 分别去各个目录找到处理方式
        for platform, config in allConfig.items():
            if platform != pform:
                continue
            print(f'Platform: {platform}, Config: {config}')

            # 动态导入模块和函数
            try:
                moduleSrc = f"core.{platform}.Pusher"
                lib = importlib.import_module(moduleSrc)
                # driver = webdriver.Chrome(chrome_options=options, executable_path="/home/zhaozhiwei/workspace/md-auto-pub/driver/chromedriver")
                driver = webdriver.Chrome(chrome_options=options)
                driver.set_page_load_timeout(10)
                lib.Pusher().pushExt(config, markdownDict, driver)
                # 关掉浏览器
                time.sleep(10)
                driver.quit()
            except ModuleNotFoundError:
                print(f"暂不支持 {platform}")

    # 扩展实现该方法
    def pushExt(self, config, markdownProperties, driver):
        self.loginAndForward(driver, config.get("URL"))
        self.write(driver, config, markdownProperties)

    # 登录并跳转
    def loginAndForward(self, driver, url):
        rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        cookiePath = self.getCookiePath(os.path.join(rootPath, "cookie"))

        # 查看文件修改日期是否超过10分钟, 如果超过则重新登录
        if os.path.exists(cookiePath):
            mtime = os.path.getmtime(cookiePath)
            now = time.time()
            if now - mtime > 600:
                os.remove(cookiePath)

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
            except Exception as e:
                print(f'An error occurred: {e}')

    def write(self, driver, config, markdownProperties):
        pass
