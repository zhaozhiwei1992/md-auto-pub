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
        driver.close()

    def loginAndForward(self, driver, url):

        curPath = os.path.abspath(os.path.dirname(__file__))
        # MdAutoPub，也就是项目的根路径
        rootPath = curPath[:curPath.find("MdAutoPub/") + len("MdAutoPub/")]
        cookiePath = os.path.abspath(rootPath + 'cookie/cnblog_cookie.json')

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
        # 添加新随笔
        pyautogui.click(x=1383, y=157, button='left')
        # pyautogui.click(writeLocation)

        # 通过pyautogui 定位到标题, 写入内容
        time.sleep(3)
        pyautogui.click(x=233, y=399, button='left')

        # 删除Backspace
        time.sleep(1)
        pyperclip.copy(markdownProperties['title'])

        time.sleep(2)
        pyautogui.hotkey('ctrl', 'v')

        # 通过pyautogui 定位到内容区, 写入内容
        # tab键到内容
        time.sleep(1)
        pyautogui.press("tab")
        time.sleep(1)
        pyautogui.press("tab")

        time.sleep(1)
        pyperclip.copy(markdownProperties['content'])
        time.sleep(3)
        pyautogui.hotkey('ctrl', 'v')

        # 增加tag, 回车确认标签生效 296, 710
        time.sleep(3)
        pyautogui.scroll(-500, x=992, y=231)
        time.sleep(2)
        pyautogui.click(x=296, y=710, button='left')
        # 添加tag, 逗号换成回车符
        time.sleep(1)
        pyperclip.copy(str(markdownProperties['tag']).replace(",", "\n") + "\n")
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(2)
        pyautogui.press('enter')

        # 通过pyautogui获取到提交按钮, 点击发布
        time.sleep(2)
        # pyautogui.click(x=217, y=791, button='left')
