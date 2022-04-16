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
        # 关掉浏览器
        driver.close()

    def loginAndForward(self, driver, url):

        curPath = os.path.abspath(os.path.dirname(__file__))
        # MdAutoPub，也就是项目的根路径
        rootPath = curPath[:curPath.find("MdAutoPub/") + len("MdAutoPub/")]
        cookiePath = os.path.abspath(rootPath + 'cookie/jianshu_cookie.json')

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
    def write(self, config, markdownProperties):
        curPath = os.path.abspath(os.path.dirname(__file__))
        # MdAutoPub，也就是项目的根路径
        rootPath = curPath[:curPath.find("MdAutoPub/") + len("MdAutoPub/")]
        positionPath = os.path.abspath(rootPath + 'position/jianshu/')
        # 跳转到文章写入界面
        # writeLocation = pyautogui.locateOnScreen(positionPath + "/img_1.png")  # 传入按钮的图片
        # print("写文章按钮坐标: ", writeLocation)
        # 转化为 x,y坐标
        # x, y = pyautogui.center(writeLocation)
        time.sleep(3)
        # 鼠标左击一下 x表横坐标， y表示纵坐标 单位像素， button=left 表示左键
        pyautogui.click(x=1437, y=151, button='left')
        # pyautogui.click(writeLocation)

        # 新建文章
        time.sleep(3)
        pyautogui.click(x=365, y=159, button='left')

        # 通过pyautogui 定位到标题, 写入内容
        # 删除Backspace
        time.sleep(3)
        pyperclip.copy(markdownProperties['title'])
        time.sleep(2)
        # pyperclip.paste()

        # 千万不要用typewrite输入大片文章。。
        # pyautogui.typewrite(markdownProperties['title'])
        pyautogui.hotkey('ctrl', 'v')

        # tab键到内容
        time.sleep(3)
        pyautogui.press("tab")
        # 通过pyautogui 定位到内容区, 写入内容
        time.sleep(1)
        pyperclip.copy(markdownProperties['content'])
        time.sleep(3)
        # pyperclip.paste()
        pyautogui.hotkey('ctrl', 'v')

        # 通过pyautogui获取到提交按钮, 点击发布
        # pyautogui.click(x=365, y=159, button='left')
