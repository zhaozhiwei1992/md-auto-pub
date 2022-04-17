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
        cookiePath = os.path.abspath(rootPath + 'cookie/juejin_cookie.json')

        # 如果文件不存在则先登录
        if not os.path.exists(cookiePath):
            driver.maximize_window()
            driver.get(url)

            # 睡一份中等你登录
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
            # 用保存的cookie访问豆瓣
            driver.get(url)

    # 录入内容,
    # 这部分根据实际情况调整坐标
    def write(self, config, markdownProperties):
        time.sleep(3)
        # 写文章 318, 339
        pyautogui.click(x=318, y=339, button='left')

        # 标题 176, 163
        time.sleep(3)
        pyautogui.click(x=176, y=163, button='left')

        time.sleep(1)
        pyperclip.copy(markdownProperties['title'])

        time.sleep(2)
        pyautogui.hotkey('ctrl', 'v')

        # 内容区 156, 289
        # tab键到内容
        time.sleep(3)
        pyautogui.click(x=156, y=289, button='left')

        time.sleep(1)
        pyperclip.copy(markdownProperties['content'])
        time.sleep(3)
        pyautogui.hotkey('ctrl', 'v')

        # 发布按钮 1414, 162
        time.sleep(2)
        pyautogui.click(x=1414, y=162, button='left')

        # 分类 1081, 296
        time.sleep(2)
        pyautogui.click(x=1081, y=296, button='left')
        # 添加标签 1103, 411
        time.sleep(2)
        pyautogui.click(x=1103, y=411, button='left')
        # 选择标签 1052, 525
        time.sleep(2)
        pyautogui.click(x=1052, y=525, button='left')

        # 摘要 1115, 734
        # 默认会根据文章自动写入, 30秒内自己调整
        time.sleep(2)
        pyautogui.click(x=1115, y=734, button='left')
        time.sleep(30)

        # 确认发布 1411, 867
        time.sleep(2)
        pyautogui.click(x=1411, y=867, button='left')
