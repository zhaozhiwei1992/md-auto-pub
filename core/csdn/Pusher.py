"""
自定义CSDN pusher
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
        cookiePath = os.path.abspath(rootPath + 'cookie/csdn_cookie.json')

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

        # x掉模板库弹框 x=1139, y=266
        time.sleep(3)
        pyautogui.click(x=1139, y=266, button='left')

        # 标题 x=317, y=156
        time.sleep(3)
        pyautogui.click(x=317, y=156, button='left')
        time.sleep(1)
        pyperclip.copy(markdownProperties['title'])
        # 覆盖原标题
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')

        # 内容区x=186, y=366
        time.sleep(3)
        pyautogui.click(x=186, y=366, button='left')
        time.sleep(1)
        pyperclip.copy(markdownProperties['content'])
        # 覆盖原标题
        time.sleep(3)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')

        # 发布文章 x=1442, y=150
        time.sleep(2)
        pyautogui.click(x=1442, y=150, button='left')

        # 文章标签 x=578, y=527
        # 标签无法自定义的话时间拉长，手选了只能
        time.sleep(2)
        pyautogui.click(x=578, y=527, button='left')
        time.sleep(2)
        pyautogui.click(x=604, y=609, button='left')
        time.sleep(2)
        pyperclip.copy("其他")
        time.sleep(2)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(5)
        pyautogui.click(x=594, y=664, button='left')
        # 移除弹框
        time.sleep(3)
        pyautogui.click(x=486, y=623, button='left')

        # 文章类型x=551, y=626
        time.sleep(3)
        pyautogui.click(x=551, y=626, button='left')

        # 发布形式 x=551, y=727
        time.sleep(3)
        pyautogui.click(x=551, y=727, button='left')

        # 内容等级 x=648, y=776
        time.sleep(3)
        pyautogui.click(x=648, y=776, button='left')

        # 确认发布 x=1084, y=833
        time.sleep(3)
        pyautogui.click(x=1084, y=833, button='left')
