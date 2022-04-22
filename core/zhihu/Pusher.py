"""
自定义pusher, 继承core.AbstractPusher
"""
from selenium import webdriver
import json
import os
import time
import pyautogui
import pyperclip
from selenium.common.exceptions import TimeoutException


class Pusher:

    # 扩展实现入口
    def pushExt(self, config, markdownProperties):
        driver = webdriver.Firefox()
        # 控制网站打开超时，否则get会阻塞
        driver.set_page_load_timeout(2)
        self.loginAndForward(driver, config.get("URL"))
        self.write(driver, config, markdownProperties)
        # 关掉浏览器
        driver.close()

    def loginAndForward(self, driver, url):

        curPath = os.path.abspath(os.path.dirname(__file__))
        # MdAutoPub，也就是项目的根路径
        rootPath = curPath[:curPath.find("MdAutoPub/") + len("MdAutoPub/")]
        cookiePath = os.path.abspath(rootPath + 'cookie/zhihu_cookie.json')

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
    def write(self, driver, config, markdownProperties):
        # 写文章界面
        # 标题 x=505, y=294
        time.sleep(3)
        pyautogui.click(x=505, y=294, button='left')
        time.sleep(2)
        pyperclip.copy(markdownProperties['title'])
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'v')

        # 正文
        # 知乎目前不支持直接输入markdown, 所以转换后给它塞进去, 懒得整它的导入了
        # 跳转到转换页面，把markdown进行格式转换
        transMdUrl = config.get("TRANS_MD")
        pyperclip.copy(markdownProperties['content'])
        # 打开转换页面 https://md.phodal.com/
        try:
            driver.get(transMdUrl)
        except TimeoutException:
            print('timeout')
        # 写入左侧页面 x=182, y=263
        time.sleep(1)
        pyautogui.click(x=182, y=263, button='left')
        time.sleep(2)
        # 全选 /删除
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(2)
        pyautogui.hotkey('backspace')
        # 将markdown内容写入到左侧
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'v')

        # 点击复制 并复制到剪贴板 x=857, y=170
        time.sleep(1)
        pyautogui.click(x=857, y=170, button='left')
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'c')

        # 回到主页签, 第一个
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[0])

        # 定位到内容区, 写入转换内容 x=516, y=409
        time.sleep(2)
        pyautogui.click(x=516, y=409, button='left')
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'v')

        # 发布设置 x=429, y=860
        time.sleep(1)
        pyautogui.click(x=429, y=860, button='left')
        # 文章话题/添加话题x=581, y=782
        time.sleep(1)
        pyautogui.click(x=581, y=782, button='left')
        # 光标定位录入框
        time.sleep(1)
        pyautogui.click(x=581, y=782, button='left')
        # 录入一个后选择搜索内容
        tags = str(markdownProperties['tag'])
        tagList = tags.split(",")
        pyperclip.copy(tagList[0])
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')
        # 选择搜索结果最上边的 x=554, y=613
        pyautogui.click(x=554, y=613, button='left')

        # 发布 x=1170, y=862
        time.sleep(2)
        # pyautogui.click(x=1170, y=862, button='left')