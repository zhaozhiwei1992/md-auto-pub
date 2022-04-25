"""
思否自动提交实现
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

    # 登录并跳转到写入界面
    def loginAndForward(self, driver, url):

        curPath = os.path.abspath(os.path.dirname(__file__))
        # MdAutoPub，也就是项目的根路径
        rootPath = curPath[:curPath.find("MdAutoPub/") + len("MdAutoPub/")]
        cookiePath = os.path.abspath(rootPath + 'cookie/segmentfault_cookie.json')

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

        # 撰写 x=1171, y=155
        time.sleep(3)
        pyautogui.click(x=1171, y=155, button='left')

        # 写文章 x=1178, y=230
        time.sleep(3)
        pyautogui.click(x=1178, y=230, button='left')

        # 可能有弹框提示 x掉 x=1021, y=186
        time.sleep(3)
        pyautogui.click(x=1021, y=186, button='left')

        # 标题 x=210, y=233
        time.sleep(3)
        pyautogui.click(x=210, y=233, button='left')
        time.sleep(2)
        pyperclip.copy(markdownProperties['title'])

        time.sleep(2)
        pyautogui.hotkey('ctrl', 'v')

        # 添加标签 x=77, y=288
        time.sleep(2)
        pyautogui.click(x=77, y=288, button='left')
        # 搜索标签 x=144, y=367
        time.sleep(2)
        pyautogui.click(x=144, y=367, button='left')
        # 输入标签 回车, 每次只能录入一个
        time.sleep(1)
        # tags = str(markdownProperties['tag'])
        # tagList = tags.split(",")
        # for tag in tagList:
        #     pyperclip.copy(tag)
        #     time.sleep(2)
        #     pyautogui.hotkey('ctrl', 'v')
        # 标签不存在无法添加,随意指定其他
        pyperclip.copy("其他")
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(2)
        pyautogui.hotkey('enter')
        # 这里留点时间30s, 可以加其它标签
        # time.sleep(30)

        # 内容区 x=339, y=689
        time.sleep(3)
        pyautogui.click(x=339, y=689, button='left')

        time.sleep(1)
        pyperclip.copy(markdownProperties['content'])
        time.sleep(3)
        pyautogui.hotkey('ctrl', 'v')

        # 发布文章 x=1501, y=153
        time.sleep(2)
        pyautogui.click(x=1501, y=153, button='left')

        # 确认发布 x=1384, y=624
        time.sleep(2)
        pyautogui.click(x=1384, y=624, button='left')
