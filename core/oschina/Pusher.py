"""
自定义博客园 pusher, 继承core.AbstractPusher
"""
from selenium import webdriver
import json
import os
import time
import pyautogui
import pyperclip


class Pusher:

    # 扩展实现入口
    def pushExt(self, config, markdownProperties):
        driver = webdriver.Firefox()
        self.loginAndForward(driver, config.get("URL"))
        self.write(config, markdownProperties)
        # 关掉浏览器 20s后
        time.sleep(20)
        # driver.close()
        pyautogui.hotkey('alt', 'f4')
        time.sleep(10)

    def loginAndForward(self, driver, url):

        curPath = os.path.abspath(os.path.dirname(__file__))
        # MdAutoPub，也就是项目的根路径
        rootPath = curPath[:curPath.find("MdAutoPub/") + len("MdAutoPub/")]
        cookiePath = os.path.abspath(rootPath + 'cookie/oschina_cookie.json')

        # 如果文件不存在则先登录
        if not os.path.exists(cookiePath):
            driver.maximize_window()
            driver.get(url)

            # 睡30秒等你登录
            time.sleep(30)

            dictCookies = driver.get_cookies()
            jsonCookies = json.dumps(dictCookies)
            # print(jsonCookies)
            with open(cookiePath, 'w') as f:
                f.write(jsonCookies)
        else:
            driver.get(url)
            # 删掉cookies
            driver.delete_all_cookies()
            with open(cookiePath, 'r', encoding='utf8') as f:
                cookies = json.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)
                # print(cookie)
            # 用保存的cookie访问
            driver.get(url)

    # 录入内容,
    # 这部分根据实际情况调整坐标
    def write(self, config, markdownProperties):
        time.sleep(3)
        # 写博客 1027, 211
        pyautogui.click(x=1027, y=211, button='left')

        # 通过pyautogui 定位到标题, 写入内容
        time.sleep(3)
        pyperclip.copy(markdownProperties['title'])

        time.sleep(2)
        pyautogui.hotkey('ctrl', 'v')

        # 切换为markdown模式 373, 334
        time.sleep(2)
        pyautogui.click(x=373, y=334, button='left')

        # 通过pyautogui 定位到内容区, 写入内容
        time.sleep(2)
        pyperclip.copy(markdownProperties['content'])
        time.sleep(3)
        pyautogui.hotkey('ctrl', 'v')

        # 通过pyautogui获取到提交按钮, 点击发布
        time.sleep(3)
        # 发布文章 x=1328, y=276
        pyautogui.click(x=1328, y=276, button='left')
        # 确认发布 x=1288, y=505
        time.sleep(3)
        pyautogui.click(x=1288, y=505, button='left')
